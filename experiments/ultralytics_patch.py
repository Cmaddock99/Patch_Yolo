#!/usr/bin/env python3
"""
experiments/ultralytics_patch.py
---------------------------------
Person-vanishing adversarial patch attack against Ultralytics YOLO models.
Works with YOLOv8 / YOLO11 / YOLO26. No ART, no Docker, no GAN required.

Attack mechanism
----------------
Call the inner DetectionModel directly (bypasses Ultralytics predict()'s
no_grad wrapper) to get differentiable raw predictions (B, 4+80, 8400).
The patch is optimized by minimizing the person class score across all
anchor points in the image.

Loss: L_total = L_det + tv_weight * L_tv
  L_det : mean of top-k person class scores over all anchor points
  L_tv  : total variation — keeps patch smooth (printability proxy)

EoT (Expectation over Transformations):
  Random ±position jitter per iteration to improve spatial robustness.

Usage
-----
    # Mac CPU (baseline test — expect ~2–3 min for 100 epochs)
    python experiments/ultralytics_patch.py --model yolov8n --epochs 100

    # Full run
    python experiments/ultralytics_patch.py --model yolov8n --epochs 500

    # On Google Colab (auto-detects CUDA, ~15× faster)
    python experiments/ultralytics_patch.py --model yolov8n --epochs 1000

Cross-version transfer (capstone experiments)
---------------------------------------------
Train on yolov8n, then evaluate the saved patch against yolo11n and yolo26n:
    python experiments/ultralytics_patch.py --model yolo11n --eval-only \
        --load-patch outputs/yolov8n_patch_v1/patches/patch.png
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
from ultralytics import YOLO

# COCO: class 0 = person. In (B, 84, 8400) output: channels 0-3 are box
# coordinates, channel 4 is person class score.
PERSON_CLASS_ID = 0
PERSON_CHANNEL = 4  # index into the 84-channel dimension


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    # MPS (Apple Silicon) has incomplete autograd support for some Ultralytics
    # operations — fall back to CPU on Mac. On Colab with a GPU, CUDA is used.
    return "cpu"


def total_variation(patch: torch.Tensor) -> torch.Tensor:
    """Penalize high-frequency noise in the patch."""
    tv_h = torch.abs(patch[:, :, 1:] - patch[:, :, :-1]).sum()
    tv_w = torch.abs(patch[:, 1:, :] - patch[:, :-1, :]).sum()
    return (tv_h + tv_w) / patch.numel()


def apply_patch(image: torch.Tensor, patch: torch.Tensor, top: int, left: int) -> torch.Tensor:
    """Overlay patch on a single CHW image. Returns patched image."""
    ph, pw = patch.shape[1], patch.shape[2]
    result = image.clone()
    result[:, top : top + ph, left : left + pw] = patch
    return result


def save_image_with_boxes(
    img_chw: torch.Tensor,
    boxes: list,
    color: tuple,
    path: Path,
) -> None:
    canvas = (img_chw.permute(1, 2, 0).cpu().numpy() * 255).clip(0, 255).astype(np.uint8).copy()
    for box in boxes:
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        conf = float(box[4]) if len(box) > 4 else 0.0
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color, 2)
        label = f"person:{conf:.2f}" if conf else "person"
        cv2.putText(canvas, label, (x1, max(16, y1 - 4)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)
    Image.fromarray(canvas).save(path)


def compute_torso_placement(boxes: list, image_size: int, patch_size: int) -> tuple[int, int]:
    """Return (top, left) to place the patch on the largest person's chest area."""
    if not boxes:
        mid = image_size // 2 - patch_size // 2
        return mid, mid
    box = max(boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    x1, y1, x2, y2 = box[:4]
    cx = int((x1 + x2) / 2)
    cy = int(y1 + 0.35 * (y2 - y1))   # 35% down from top of person = chest
    top = int(np.clip(cy - patch_size // 2, 0, image_size - patch_size))
    left = int(np.clip(cx - patch_size // 2, 0, image_size - patch_size))
    return top, left


# ---------------------------------------------------------------------------
# Core inference (differentiable)
# ---------------------------------------------------------------------------

def prepare_inner_for_grad(inner_model: torch.nn.Module) -> None:
    """
    Ultralytics lazily initializes `anchors` and `strides` on first inference
    inside torch.inference_mode(), making those tensors unusable for autograd.
    Clone them to normal tensors so gradient computation works.
    Call this AFTER the first yolo.predict() run.
    """
    for m in inner_model.modules():
        for attr in ("anchors", "strides"):
            tensor = getattr(m, attr, None)
            if isinstance(tensor, torch.Tensor):
                setattr(m, attr, tensor.clone().detach())


def predict_with_grad(
    inner_model: torch.nn.Module,
    image_bchw: torch.Tensor,
) -> torch.Tensor:
    """
    Run the inner DetectionModel with gradients enabled.
    Returns raw predictions: (B, 4+num_classes, num_anchors).
    Calls inner_model directly — bypasses YOLO.predict()'s no_grad wrapper.
    """
    with torch.enable_grad():
        out = inner_model(image_bchw)
    if isinstance(out, (list, tuple)):
        return out[0]
    return out


def detection_loss(preds: torch.Tensor, topk: int = 10) -> torch.Tensor:
    """
    Minimize the person class score across anchor points.
    Uses mean of top-k to focus on the strongest detections.
    preds: (B, 4+num_classes, num_anchors)
    """
    person_scores = preds[:, PERSON_CHANNEL, :]  # (B, num_anchors)
    topk_scores = person_scores.topk(min(topk, person_scores.shape[1]), dim=1).values
    return topk_scores.mean()


# ---------------------------------------------------------------------------
# Detection helpers (no-grad, for evaluation)
# ---------------------------------------------------------------------------

def run_predict(yolo: YOLO, img_hwc_uint8: np.ndarray, conf: float) -> list:
    """Run Ultralytics predict on a single HWC uint8 image. Returns person boxes."""
    results = yolo.predict(img_hwc_uint8, verbose=False, conf=conf)
    boxes = []
    for box in results[0].boxes:
        if int(box.cls.item()) == PERSON_CLASS_ID:
            xyxy = box.xyxy[0].cpu().numpy()
            conf_val = box.conf.item()
            boxes.append((*xyxy, conf_val))
    return boxes


def load_and_resize_images(
    images_dir: Path, image_size: int
) -> tuple[list[np.ndarray], list[Path]]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    paths = sorted(p for p in images_dir.iterdir() if p.suffix.lower() in exts)
    if not paths:
        raise ValueError(f"No images found in {images_dir}")
    arrays = []
    for p in paths:
        img = Image.open(p).convert("RGB").resize((image_size, image_size))
        arrays.append(np.asarray(img, dtype=np.float32) / 255.0)
    return arrays, paths


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Adversarial patch vs Ultralytics YOLO")
    p.add_argument("--model", default="yolov8n",
                   help="Ultralytics model name: yolov8n, yolo11n, yolo26n, ...")
    p.add_argument("--images-dir", default="data/custom_images", type=Path)
    p.add_argument("--output-dir", default="outputs", type=Path)
    p.add_argument("--patch-size", default=100, type=int,
                   help="Patch height = width in pixels")
    p.add_argument("--epochs", default=500, type=int)
    p.add_argument("--lr", default=0.01, type=float)
    p.add_argument("--tv-weight", default=0.05, type=float,
                   help="Weight for total-variation smoothness loss")
    p.add_argument("--topk", default=10, type=int,
                   help="Number of anchor points used in detection loss")
    p.add_argument("--image-size", default=640, type=int)
    p.add_argument("--conf-threshold", default=0.5, type=float)
    p.add_argument("--batch-size", default=4, type=int)
    p.add_argument("--jitter", default=10, type=int,
                   help="EoT patch position jitter in pixels (each axis)")
    p.add_argument("--display", default=5, type=int,
                   help="Number of sample images to save")
    p.add_argument("--eval-only", action="store_true",
                   help="Skip training, only evaluate an existing patch")
    p.add_argument("--load-patch", type=Path, default=None,
                   help="Path to an existing patch.png to load (for eval or transfer)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    device = get_device()
    print(f"Device: {device}")
    print(f"Model:  {args.model}")

    # Output directories — eval-only runs get a distinct name so they don't
    # overwrite training results for the same model.
    if args.eval_only and args.load_patch:
        source_model = args.load_patch.parts[-3] if len(args.load_patch.parts) >= 3 else "unknown"
        run_name = f"{args.model}_from_{source_model}_transfer"
    else:
        run_name = f"{args.model}_patch_v1"
    run_dir = args.output_dir / run_name
    for sub in ("original", "patched", "patches"):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)

    # Load images
    print(f"\nLoading images from {args.images_dir} ...")
    raw_arrays, image_paths = load_and_resize_images(args.images_dir, args.image_size)
    # (N, H, W, 3) float32 [0,1]
    images_nhwc = np.stack(raw_arrays)
    # (N, 3, H, W) float32 [0,1] tensor
    images_nchw = torch.from_numpy(images_nhwc).permute(0, 3, 1, 2)
    print(f"  Loaded {len(image_paths)} images.")

    # Load YOLO
    print(f"\nLoading {args.model} ...")
    yolo = YOLO(f"{args.model}.pt")
    inner = yolo.model.to(device)
    inner.eval()
    for param in inner.parameters():
        param.requires_grad_(False)

    # Clean inference: find person images + get bounding boxes
    print("\nRunning clean inference to select training images ...")
    training_indices: list[int] = []
    training_boxes: list[list] = []
    for i, arr in enumerate(raw_arrays):
        hwc_uint8 = (arr * 255).astype(np.uint8)
        boxes = run_predict(yolo, hwc_uint8, args.conf_threshold)
        if boxes:
            training_indices.append(i)
            training_boxes.append(boxes)

    if not training_indices:
        raise ValueError(
            f"No person detected in any image above conf={args.conf_threshold}. "
            "Lower --conf-threshold or add more full-body photos."
        )
    print(f"  Selected {len(training_indices)}/{len(image_paths)} images with person detections.")

    # Ultralytics lazily initializes anchor/stride tensors on first inference
    # inside torch.inference_mode(). Clone them so autograd can use them.
    prepare_inner_for_grad(inner)

    train_images = images_nchw[training_indices]   # (M, 3, H, W)
    train_paths = [image_paths[i] for i in training_indices]

    # Compute patch placements (torso center per image)
    placements = [
        compute_torso_placement(boxes, args.image_size, args.patch_size)
        for boxes in training_boxes
    ]

    # Save clean detection samples
    for idx in range(min(args.display, len(train_images))):
        raw_boxes_with_conf = [(*b[:4], b[4]) for b in training_boxes[idx]]
        save_image_with_boxes(
            train_images[idx],
            raw_boxes_with_conf,
            color=(0, 255, 0),
            path=run_dir / "original" / f"clean_{idx:02d}_{train_paths[idx].stem}.png",
        )

    # Move training images to device
    train_images_dev = train_images.to(device)

    # Initialize or load patch
    if args.load_patch and args.load_patch.exists():
        print(f"\nLoading patch from {args.load_patch} ...")
        patch_img = Image.open(args.load_patch).convert("RGB").resize(
            (args.patch_size, args.patch_size)
        )
        patch_np = np.asarray(patch_img, dtype=np.float32) / 255.0
        patch = torch.from_numpy(patch_np).permute(2, 0, 1).to(device).requires_grad_(not args.eval_only)
    else:
        patch = torch.rand(3, args.patch_size, args.patch_size,
                           device=device, requires_grad=True)

    # -----------------------------------------------------------------------
    # Training loop
    # -----------------------------------------------------------------------
    loss_history: list[float] = []

    if not args.eval_only:
        optimizer = torch.optim.Adam([patch], lr=args.lr, betas=(0.9, 0.999))
        print(f"\nTraining for {args.epochs} epochs ...")

        for epoch in tqdm(range(1, args.epochs + 1), desc="Training"):
            # Random mini-batch indices
            batch_idx = torch.randperm(len(train_images_dev))[: args.batch_size].tolist()
            epoch_loss_det = 0.0

            for idx in batch_idx:
                img = train_images_dev[idx]               # (3, H, W)
                top, left = placements[idx]

                # EoT: small random jitter on patch placement
                j = args.jitter
                t_jit = int(np.clip(top + np.random.randint(-j, j + 1), 0,
                                    args.image_size - args.patch_size))
                l_jit = int(np.clip(left + np.random.randint(-j, j + 1), 0,
                                    args.image_size - args.patch_size))

                patch_c = patch.clamp(0, 1)
                patched_img = apply_patch(img, patch_c, t_jit, l_jit)

                # Forward (differentiable)
                preds = predict_with_grad(inner, patched_img.unsqueeze(0))

                # Loss
                loss_det = detection_loss(preds, topk=args.topk)
                loss_tv = total_variation(patch_c)
                loss = loss_det + args.tv_weight * loss_tv

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                epoch_loss_det += loss_det.item()

            avg = epoch_loss_det / len(batch_idx)
            loss_history.append(avg)

            if epoch % 50 == 0 or epoch == 1:
                tqdm.write(f"  Epoch {epoch:4d}/{args.epochs} — det_loss: {avg:.4f}")

        # Save patch
        patch_final = patch.detach().clamp(0, 1).cpu()
        patch_save = (patch_final.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        Image.fromarray(patch_save).save(run_dir / "patches" / "patch.png")
        print(f"\nPatch saved → {run_dir}/patches/patch.png")

        # Save loss history
        (run_dir / "loss_history.json").write_text(json.dumps(loss_history))

    # -----------------------------------------------------------------------
    # Evaluation: before vs after detection counts
    # -----------------------------------------------------------------------
    print("\nEvaluating attack effectiveness ...")
    total_clean = sum(len(b) for b in training_boxes)
    total_patched = 0
    patch_eval = patch.detach().clamp(0, 1) if not args.eval_only else patch.clamp(0, 1)

    for idx in range(len(train_images)):
        img = train_images_dev[idx]
        top, left = placements[idx]
        patched_img = apply_patch(img, patch_eval, top, left)
        hwc_uint8 = (patched_img.cpu().permute(1, 2, 0).numpy() * 255).clip(0, 255).astype(np.uint8)
        patched_dets = run_predict(yolo, hwc_uint8, args.conf_threshold)
        total_patched += len(patched_dets)

        # Save sample patched images
        if idx < args.display:
            save_image_with_boxes(
                patched_img.cpu(),
                [(*b[:4], b[4]) for b in patched_dets],
                color=(0, 0, 255),
                path=run_dir / "patched" / f"patched_{idx:02d}_{train_paths[idx].stem}.png",
            )

    suppression_pct = (1.0 - total_patched / max(1, total_clean)) * 100.0

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    summary = {
        "model": args.model,
        "epochs": args.epochs,
        "training_images": len(train_images),
        "patch_size": args.patch_size,
        "final_det_loss": round(loss_history[-1], 5) if loss_history else None,
        "clean_person_detections": total_clean,
        "patched_person_detections": total_patched,
        "detection_suppression_pct": round(suppression_pct, 1),
        "device": device,
    }
    (run_dir / "results.json").write_text(json.dumps(summary, indent=2))

    print(f"\n{'='*52}")
    print(f"  Model              : {args.model}")
    print(f"  Training images    : {len(train_images)}")
    print(f"  Epochs             : {args.epochs}")
    if loss_history:
        print(f"  Final det loss     : {loss_history[-1]:.4f}  (↓ = more effective)")
    print(f"  Person dets BEFORE : {total_clean}")
    print(f"  Person dets AFTER  : {total_patched}")
    print(f"  Detection suppression: {suppression_pct:.1f}%")
    print(f"  Output dir         : {run_dir}/")
    print(f"{'='*52}")


if __name__ == "__main__":
    main()
