#!/usr/bin/env python3
"""
experiments/ultralytics_patch.py
---------------------------------
Person-vanishing adversarial patch attack against Ultralytics YOLO models.
Works with YOLOv8 / YOLO11 / YOLO26. No ART, no Docker, no GAN required.

Attack mechanism
----------------
Call the inner DetectionModel directly (bypasses Ultralytics predict()'s
no_grad wrapper) to get differentiable raw predictions.

For YOLOv8 / YOLO11: inner_model returns (B, 84, 8400) — channels 0-3 are box
  coordinates, channels 4-83 are class scores. Person = channel 4.

For YOLO26 (end2end=True): inner_model returns (y, preds_dict). y=(B,300,6)
  is post-processed and has no useful gradients. preds_dict["one2many"]["scores"]
  is (B, 80, 8400) raw class logits computed from non-detached features —
  this is the differentiable tensor used for gradient-based optimization.
  (one2one is computed from detached features → no gradient flow.)

Loss: L_total = L_det + tv_weight * L_tv
  L_det : mean of top-k person class scores (sigmoid-scaled to [0,1])
  L_tv  : total variation — keeps patch smooth (printability proxy)

EoT (Expectation over Transformations):
  Random ±position jitter per iteration to improve spatial robustness.

Usage
-----
    # Single model, manifest subset
    python experiments/ultralytics_patch.py \
        --model yolov8n --manifest data/manifests/common_14.txt \
        --seed 42 --epochs 1000

    # Cross-version transfer eval
    python experiments/ultralytics_patch.py \
        --model yolo11n --eval-only \
        --load-patch outputs/yolov8n_patch_v2/patches/patch.png \
        --manifest data/manifests/common_14.txt
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

# COCO: class 0 = person.
# In YOLOv8/v11 (B, 84, 8400): channels 0-3 are box coords, channel 4 = person.
# In YOLO26 scores (B, 80, 8400): pure class scores, person = channel 0.
PERSON_CLASS_ID = 0
PERSON_CHANNEL = 4  # for v8/v11 (B, 84, 8400) layout


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    # MPS (Apple Silicon) has incomplete autograd support for some Ultralytics
    # operations — fall back to CPU on Mac.
    return "cpu"


def total_variation(patch: torch.Tensor) -> torch.Tensor:
    """Penalize high-frequency noise in the patch."""
    tv_h = torch.abs(patch[:, :, 1:] - patch[:, :, :-1]).sum()
    tv_w = torch.abs(patch[:, 1:, :] - patch[:, :-1, :]).sum()
    return (tv_h + tv_w) / patch.numel()


def block_erase(patch: torch.Tensor, prob: float, n_blocks: int = 3) -> torch.Tensor:
    """DePatch (Cheng 2024): randomly zero one block of the patch each forward pass.
    Prevents self-coupling — any single block being degraded cannot destroy the whole effect.
    n_blocks=3 divides the patch into a 3x3 grid; one cell is zeroed at random.
    """
    if prob <= 0.0 or float(np.random.random()) > prob:
        return patch
    p = patch.clone()
    ph, pw = p.shape[1], p.shape[2]
    bh, bw = ph // n_blocks, pw // n_blocks
    bi = np.random.randint(0, n_blocks)
    bj = np.random.randint(0, n_blocks)
    p[:, bi * bh : (bi + 1) * bh, bj * bw : (bj + 1) * bw] = 0.0
    return p


def patch_cutout(patch: torch.Tensor, prob: float, size: int) -> torch.Tensor:
    """T-SEA (Huang 2022): randomly zero a square region of the patch.
    Improves black-box transfer by preventing the patch from over-fitting to
    any single localized feature of the source model's gradient landscape.
    """
    if prob <= 0.0 or float(np.random.random()) > prob:
        return patch
    p = patch.clone()
    ph, pw = p.shape[1], p.shape[2]
    t = np.random.randint(0, max(1, ph - size + 1))
    l = np.random.randint(0, max(1, pw - size + 1))
    p[:, t : t + size, l : l + size] = 0.0
    return p


def rotate_patch_eot(patch: torch.Tensor, rot_max: float) -> torch.Tensor:
    """EoT rotation (Schack 2024): rotate patch by a random angle in [-rot_max, rot_max] degrees.
    Rotation >20° Z-axis is the primary physical degradation mode per Schack 2024.
    Uses differentiable affine_grid + grid_sample so gradients flow back to patch pixels.
    """
    if rot_max <= 0.0:
        return patch
    import math
    angle_deg = float(np.random.uniform(-rot_max, rot_max))
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    theta = torch.tensor(
        [[cos_a, -sin_a, 0.0], [sin_a, cos_a, 0.0]],
        dtype=patch.dtype,
        device=patch.device,
    ).unsqueeze(0)
    grid = torch.nn.functional.affine_grid(
        theta,
        (1, patch.shape[0], patch.shape[1], patch.shape[2]),
        align_corners=False,
    )
    rotated = torch.nn.functional.grid_sample(
        patch.unsqueeze(0), grid, align_corners=False,
        mode="bilinear", padding_mode="zeros",
    ).squeeze(0)
    return rotated


# 30-color printable palette (covers the sRGB printer gamut, inspired by Thys 2019 / DePatch).
# Used by nps_loss to penalize non-printable colors.
_NPS_PALETTE = torch.tensor([
    [0.000, 0.000, 0.000], [1.000, 1.000, 1.000], [1.000, 0.000, 0.000],
    [0.000, 1.000, 0.000], [0.000, 0.000, 1.000], [1.000, 1.000, 0.000],
    [0.000, 1.000, 1.000], [1.000, 0.000, 1.000], [0.500, 0.500, 0.500],
    [0.753, 0.753, 0.753], [0.502, 0.000, 0.000], [0.000, 0.502, 0.000],
    [0.000, 0.000, 0.502], [0.502, 0.502, 0.000], [0.000, 0.502, 0.502],
    [0.502, 0.000, 0.502], [0.753, 0.251, 0.000], [0.000, 0.753, 0.251],
    [0.251, 0.000, 0.753], [0.753, 0.502, 0.251], [0.251, 0.753, 0.502],
    [0.502, 0.251, 0.753], [1.000, 0.502, 0.000], [0.000, 1.000, 0.502],
    [0.502, 0.000, 1.000], [1.000, 0.753, 0.502], [0.502, 1.000, 0.753],
    [0.753, 0.502, 1.000], [0.251, 0.251, 0.251], [0.878, 0.878, 0.878],
], dtype=torch.float32)  # shape (30, 3)


def nps_loss(patch: torch.Tensor, palette: torch.Tensor) -> torch.Tensor:
    """Non-Printability Score (Thys 2019, DePatch): penalize colors far from the nearest
    palette entry. A lower score means the patch will look more accurate when printed.
    patch:   (3, H, W) float32 in [0, 1]
    palette: (N, 3) float32, same device as patch
    Returns: mean min-L2-distance across all patch pixels (scalar).
    """
    pixels = patch.permute(1, 2, 0).reshape(-1, 3)          # (H*W, 3)
    pal = palette.to(patch.device)
    dists = torch.cdist(pixels.unsqueeze(0), pal.unsqueeze(0)).squeeze(0)  # (H*W, N)
    return dists.min(dim=1).values.mean()


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
# YOLO26 hook state (bypasses preds_dict for gradient access)
# ---------------------------------------------------------------------------
# In newer Ultralytics, YOLO26's one2many head only populates preds_dict when
# training targets are provided. Without targets (our use case), preds_dict
# ["one2many"] is an empty dict {}. Solution: hook the one2many Detect
# submodule directly and capture its raw per-scale feature tensors.

_v26_hook_tensors: dict[int, list] = {}  # model_id -> list of captured tensors
_v26_hook_handles: dict[int, list] = {}  # model_id -> list of hook handles


def install_v26_hook(inner_model: torch.nn.Module) -> None:
    """
    Find the one2many Detect submodule and install a forward hook that captures
    its raw output tensors. In train mode, Detect.forward returns a list of
    (B, no, H, W) tensors — one per detection scale — with grad_fn intact.
    Idempotent: calling twice for the same model is a no-op.
    """
    mid = id(inner_model)
    if mid in _v26_hook_handles:
        return  # already installed

    # Navigate to E2EDetect head: usually model.model[-1]
    detect_head = None
    if hasattr(inner_model, "model"):
        for layer in reversed(list(inner_model.model)):
            if hasattr(layer, "one2many"):
                detect_head = layer
                break

    if detect_head is None or not hasattr(detect_head, "one2many"):
        names = [type(m).__name__ for m in getattr(inner_model, "model", [])]
        raise RuntimeError(
            f"Cannot find E2EDetect head with 'one2many' in YOLO26.\n"
            f"Layer types: {names}"
        )

    captured: list = []
    _v26_hook_tensors[mid] = captured

    def _hook(m: torch.nn.Module, inp, out) -> None:
        captured.clear()
        if isinstance(out, (list, tuple)):
            captured.extend(out)
        elif isinstance(out, torch.Tensor):
            captured.append(out)

    handle = detect_head.one2many.register_forward_hook(_hook)
    _v26_hook_handles[mid] = [handle]
    print(f"  [v26] Hook installed on {type(detect_head.one2many).__name__} "
          f"(one2many); class tensors captured per forward pass")


def _extract_v26_cls_tensor(tensors: list, nc: int = 80) -> torch.Tensor:
    """
    Given a list of raw Detect-head tensors (B, no, H, W) or (B, no, H*W),
    extract the class-score channels (last nc channels), flatten spatial dims,
    and concatenate across scales → (B, nc, total_anchors).
    Works regardless of reg_max / DFL channel count.
    """
    chunks = []
    for t in tensors:
        if not isinstance(t, torch.Tensor):
            continue
        if t.dim() == 4:          # (B, no, H, W)
            cls = t[:, -nc:, :, :].flatten(2)   # → (B, nc, H*W)
        elif t.dim() == 3:        # (B, no, H*W) already flat
            cls = t[:, -nc:, :]
        else:
            continue
        chunks.append(cls)
    if not chunks:
        raise RuntimeError(
            f"[v26] Hook captured {len(tensors)} tensors but none had usable shape.\n"
            f"Shapes: {[t.shape if isinstance(t, torch.Tensor) else type(t) for t in tensors]}"
        )
    return torch.cat(chunks, dim=2)   # (B, nc, total_anchors)


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
    loss_source: str = "auto",
    model_name: str = "",
) -> torch.Tensor:
    """
    Run the inner DetectionModel with gradients enabled.

    YOLOv8 / YOLO11: returns (B, 84, 8400) raw predictions (box+class channels).
    YOLO26 (end2end=True): returns preds["one2many"]["scores"] (B, 80, 8400),
      raw class logits, pre-sigmoid, with gradient flow intact.
      one2one is computed from detached features and cannot be used for training.
    """
    is_v26 = "26" in model_name

    if is_v26:
        # YOLO26 hook path: the hook on one2many captures raw (B, no, H, W)
        # feature tensors with grad_fn guaranteed. preds_dict["one2many"] is
        # unreliable across Ultralytics versions (may be empty without targets).
        mid = id(inner_model)
        if mid not in _v26_hook_handles:
            raise RuntimeError(
                "[v26] install_v26_hook() was not called before predict_with_grad(). "
                "Call it after prepare_inner_for_grad()."
            )
        _v26_hook_tensors[mid].clear()
        with torch.enable_grad():
            inner_model(image_bchw)
        raw = _v26_hook_tensors[mid]
        if not raw:
            raise RuntimeError(
                "[v26] Hook captured no tensors. "
                "Check that install_v26_hook() targeted the correct submodule."
            )
        return raw  # list of (B, no, H, W); detection_loss handles this

    with torch.enable_grad():
        out = inner_model(image_bchw)

    if not isinstance(out, (list, tuple)):
        return out  # export mode, unlikely in training

    # v8/v11: out[0] is (B, 84, 8400)
    return out[0]


def detection_loss(preds, topk: int = 10, is_v26: bool = False) -> torch.Tensor:
    """
    Minimize the person class score across anchor points.
    Applies sigmoid to guarantee loss stays in [0, 1].

    preds for v8/v11: (B, 84, 8400) — person score at channel 4
    preds for v26:    list of (B, no, H, W) raw hook tensors per scale;
                      _extract_v26_cls_tensor concatenates them → (B, 80, total)
                      person at channel 0 (COCO class 0 = person in 80-class head)
    """
    if is_v26:
        if isinstance(preds, list):
            # Hook path: concat class channels across scales
            cls_tensor = _extract_v26_cls_tensor(preds, nc=80)  # (B, 80, total)
        else:
            cls_tensor = preds  # legacy path, (B, 80, 8400)
        person_scores = cls_tensor[:, PERSON_CLASS_ID, :].sigmoid()
    else:
        person_scores = preds[:, PERSON_CHANNEL, :].sigmoid()
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


def load_images_from_manifest(manifest_path: Path, image_size: int) -> tuple[list[np.ndarray], list[Path]]:
    """Load and resize images listed in a manifest file (one path per line)."""
    paths = [Path(l.strip()) for l in manifest_path.read_text().splitlines() if l.strip()]
    if not paths:
        raise ValueError(f"Manifest {manifest_path} is empty")
    arrays = []
    for p in paths:
        img = Image.open(p).convert("RGB").resize((image_size, image_size))
        arrays.append(np.asarray(img, dtype=np.float32) / 255.0)
    return arrays, paths


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
    p.add_argument("--manifest", type=Path, default=None,
                   help="Path to manifest .txt (one image path per line); overrides --images-dir")
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
    p.add_argument("--loss-source", default="auto",
                   choices=["auto", "one2many", "one2one"],
                   help="Raw score tensor for YOLO26 gradient loss (default: auto=one2many)")
    p.add_argument("--grad-clip", type=float, default=0.0,
                   help="Max gradient norm for patch update (0 = disabled)")
    p.add_argument("--seed", type=int, default=None,
                   help="Random seed for reproducibility")

    # ---- Literature-backed robustness improvements (all default off) --------
    p.add_argument("--block-erase-prob", type=float, default=0.0,
                   help="DePatch (Cheng 2024): probability of erasing a random 3x3 block "
                        "of the patch each forward pass. Improves physical robustness. "
                        "Recommended: 0.5")
    p.add_argument("--cutout-prob", type=float, default=0.0,
                   help="T-SEA (Huang 2022): probability of zeroing a random square region "
                        "of the patch each step. Improves black-box transfer. "
                        "Recommended: 0.3")
    p.add_argument("--cutout-size", type=int, default=20,
                   help="T-SEA cutout: side length of zeroed region in pixels (default: 20)")
    p.add_argument("--rot-max", type=float, default=0.0,
                   help="EoT rotation (Schack 2024): max rotation angle in degrees. "
                        "Rotation >20° is the primary physical degradation mode. "
                        "Recommended: 15.0")
    p.add_argument("--nps-weight", type=float, default=0.0,
                   help="Non-Printability Score loss weight (Thys 2019 / DePatch). "
                        "Penalizes non-printable colors. Recommended: 0.01")
    p.add_argument("--co-model", type=str, default=None,
                   help="Second model for joint multi-model training (e.g. yolo11n). "
                        "Both model losses are averaged. Improves cross-model transfer.")

    # ---- Checkpoint / resume (Colab disconnect safety) ----------------------
    p.add_argument("--checkpoint-interval", type=int, default=100,
                   help="Save checkpoint every N epochs so a disconnected Colab run can "
                        "resume. Set 0 to disable. (default: 100)")
    p.add_argument("--resume", action="store_true",
                   help="Resume from the latest checkpoint.pt in the run directory if "
                        "it exists. Skips already-completed epochs.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.seed is not None:
        torch.manual_seed(args.seed)
        np.random.seed(args.seed)

    device = get_device()
    is_v26 = "26" in args.model
    print(f"Device: {device}")
    print(f"Model:  {args.model}  (end2end={'yes' if is_v26 else 'no'})")

    # Output directory — eval-only runs get a distinct name so they don't
    # overwrite training results for the same model.
    if args.eval_only and args.load_patch:
        source_model = args.load_patch.parts[-3] if len(args.load_patch.parts) >= 3 else "unknown"
        run_name = f"{args.model}_from_{source_model}_transfer"
    elif args.co_model:
        run_name = f"{args.model}+{args.co_model}_joint_patch_v2"
    else:
        run_name = f"{args.model}_patch_v2"
    run_dir = args.output_dir / run_name
    for sub in ("original", "patched", "patches"):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)

    # Load images
    if args.manifest:
        print(f"\nLoading images from manifest {args.manifest} ...")
        raw_arrays, image_paths = load_images_from_manifest(args.manifest, args.image_size)
    else:
        print(f"\nLoading images from {args.images_dir} ...")
        raw_arrays, image_paths = load_and_resize_images(args.images_dir, args.image_size)
    images_nchw = torch.from_numpy(np.stack(raw_arrays)).permute(0, 3, 1, 2)
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

    # YOLO26 (end2end=True): preds_dict["one2many"] is unreliable across
    # Ultralytics versions (empty dict when no training targets are provided).
    # Use a forward hook on the one2many Detect submodule instead — it captures
    # raw per-scale feature tensors with grad_fn regardless of version.
    if is_v26 and not args.eval_only:
        inner.train()   # train mode ensures one2many head runs its full forward
        install_v26_hook(inner)

    # Load co-model for joint multi-model training (optional).
    co_inner = None
    is_v26_co = False
    if args.co_model and not args.eval_only:
        print(f"\nLoading co-model {args.co_model} for joint training ...")
        co_yolo = YOLO(f"{args.co_model}.pt")
        co_inner = co_yolo.model.to(device)
        co_inner.eval()
        for param in co_inner.parameters():
            param.requires_grad_(False)
        is_v26_co = "26" in args.co_model
        # Warm up co-model so anchor/stride tensors are initialized.
        _dummy = np.zeros((args.image_size, args.image_size, 3), dtype=np.uint8)
        co_yolo.predict(_dummy, verbose=False)
        prepare_inner_for_grad(co_inner)
        if is_v26_co:
            co_inner.train()
            install_v26_hook(co_inner)
        print(f"  Co-model ready: {args.co_model}")

    train_images = images_nchw[training_indices]
    train_paths = [image_paths[i] for i in training_indices]

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
    last_preds_shape: list[int] | None = None
    start_epoch = 1
    checkpoint_path = run_dir / "checkpoint.pt"

    if not args.eval_only:
        optimizer = torch.optim.Adam([patch], lr=args.lr, betas=(0.9, 0.999))

        # Resume from checkpoint if requested and file exists.
        if args.resume and checkpoint_path.exists():
            ckpt = torch.load(checkpoint_path, map_location=device)
            with torch.no_grad():
                patch.copy_(ckpt["patch"])
            optimizer.load_state_dict(ckpt["optimizer"])
            loss_history = ckpt.get("loss_history", [])
            start_epoch = ckpt["epoch"] + 1
            print(f"\nResumed from checkpoint at epoch {ckpt['epoch']} "
                  f"(continuing from epoch {start_epoch})")
        else:
            print(f"\nTraining for {args.epochs} epochs ...")

        for epoch in tqdm(range(start_epoch, args.epochs + 1), desc="Training"):
            batch_idx = torch.randperm(len(train_images_dev))[: args.batch_size].tolist()
            epoch_loss_det = 0.0

            for idx in batch_idx:
                img = train_images_dev[idx]
                top, left = placements[idx]

                j = args.jitter
                t_jit = int(np.clip(top + np.random.randint(-j, j + 1), 0,
                                    args.image_size - args.patch_size))
                l_jit = int(np.clip(left + np.random.randint(-j, j + 1), 0,
                                    args.image_size - args.patch_size))

                patch_c = patch.clamp(0, 1)

                # Apply literature-backed augmentations to the patch before pasting.
                # Each operates on a clone so the stored patch tensor is untouched.
                # Gradient flows back through all non-zeroed regions.
                patch_aug = block_erase(patch_c, args.block_erase_prob)   # DePatch
                patch_aug = patch_cutout(patch_aug, args.cutout_prob, args.cutout_size)  # T-SEA
                patch_aug = rotate_patch_eot(patch_aug, args.rot_max)      # EoT rotation

                patched_img = apply_patch(img, patch_aug, t_jit, l_jit)

                preds = predict_with_grad(
                    inner, patched_img.unsqueeze(0),
                    loss_source=args.loss_source,
                    model_name=args.model,
                )
                if last_preds_shape is None:
                    if isinstance(preds, list):
                        last_preds_shape = [list(t.shape) for t in preds if isinstance(t, torch.Tensor)]
                    else:
                        last_preds_shape = list(preds.shape)

                loss_det = detection_loss(preds, topk=args.topk, is_v26=is_v26)

                # Joint multi-model loss: average with co-model if present.
                if co_inner is not None:
                    co_preds = predict_with_grad(
                        co_inner, patched_img.unsqueeze(0),
                        loss_source=args.loss_source,
                        model_name=args.co_model,
                    )
                    co_loss_det = detection_loss(co_preds, topk=args.topk, is_v26=is_v26_co)
                    loss_det = (loss_det + co_loss_det) * 0.5

                # NPS loss uses the unaugmented patch_c (physical constraint on the
                # stored patch, not the augmented version used in the forward pass).
                loss_tv = total_variation(patch_c)
                loss_nps = (nps_loss(patch_c, _NPS_PALETTE)
                            if args.nps_weight > 0 else patch_c.new_tensor(0.0))
                loss = loss_det + args.tv_weight * loss_tv + args.nps_weight * loss_nps

                optimizer.zero_grad()
                loss.backward()

                if args.grad_clip > 0:
                    torch.nn.utils.clip_grad_norm_([patch], args.grad_clip)

                optimizer.step()
                epoch_loss_det += loss_det.item()

            avg = epoch_loss_det / len(batch_idx)
            loss_history.append(avg)

            if epoch % 50 == 0 or epoch == 1:
                tqdm.write(f"  Epoch {epoch:4d}/{args.epochs} — det_loss: {avg:.4f}")

            if args.checkpoint_interval > 0 and epoch % args.checkpoint_interval == 0:
                torch.save({
                    "epoch": epoch,
                    "patch": patch.detach().clamp(0, 1).cpu(),
                    "optimizer": optimizer.state_dict(),
                    "loss_history": loss_history,
                }, checkpoint_path)

        patch_final = patch.detach().clamp(0, 1).cpu()
        patch_save = (patch_final.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
        Image.fromarray(patch_save).save(run_dir / "patches" / "patch.png")
        print(f"\nPatch saved → {run_dir}/patches/patch.png")
        (run_dir / "loss_history.json").write_text(json.dumps(loss_history))

    # -----------------------------------------------------------------------
    # Evaluation
    # -----------------------------------------------------------------------
    print("\nEvaluating attack effectiveness ...")
    total_clean = sum(len(b) for b in training_boxes)
    total_patched = 0
    total_clean_conf = sum(b[4] for boxes in training_boxes for b in boxes)
    total_patched_conf = 0.0
    patch_eval = patch.detach().clamp(0, 1) if not args.eval_only else patch.clamp(0, 1)

    for idx in range(len(train_images)):
        img = train_images_dev[idx]
        top, left = placements[idx]
        patched_img = apply_patch(img, patch_eval, top, left)
        hwc_uint8 = (patched_img.cpu().permute(1, 2, 0).numpy() * 255).clip(0, 255).astype(np.uint8)
        patched_dets = run_predict(yolo, hwc_uint8, args.conf_threshold)
        total_patched += len(patched_dets)
        total_patched_conf += sum(b[4] for b in patched_dets)

        if idx < args.display:
            save_image_with_boxes(
                patched_img.cpu(),
                [(*b[:4], b[4]) for b in patched_dets],
                color=(0, 0, 255),
                path=run_dir / "patched" / f"patched_{idx:02d}_{train_paths[idx].stem}.png",
            )

    suppression_pct = (1.0 - total_patched / max(1, total_clean)) * 100.0
    mean_conf_clean = round(total_clean_conf / max(1, total_clean), 4)
    mean_conf_patched = round(total_patched_conf / max(1, total_patched), 4) if total_patched else 0.0

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    summary = {
        "model": args.model,
        "co_model": args.co_model,
        "epochs": args.epochs,
        "training_images": len(train_images),
        "subset_size": len(train_images),
        "patch_size": args.patch_size,
        "final_det_loss": round(loss_history[-1], 5) if loss_history else None,
        "clean_person_detections": total_clean,
        "patched_person_detections": total_patched,
        "detection_suppression_pct": round(suppression_pct, 1),
        "mean_conf_clean": mean_conf_clean,
        "mean_conf_patched": mean_conf_patched,
        "loss_source": "one2many_scores" if is_v26 else "channel4",
        "score_tensor_shape": last_preds_shape,
        "head_end2end": is_v26,
        "lr": args.lr,
        "tv_weight": args.tv_weight,
        "nps_weight": args.nps_weight,
        "block_erase_prob": args.block_erase_prob,
        "cutout_prob": args.cutout_prob,
        "cutout_size": args.cutout_size,
        "rot_max": args.rot_max,
        "grad_clip": args.grad_clip,
        "checkpoint_interval": args.checkpoint_interval,
        "resumed": args.resume,
        "device": device,
    }
    (run_dir / "results.json").write_text(json.dumps(summary, indent=2))

    print(f"\n{'='*52}")
    print(f"  Model              : {args.model}")
    print(f"  Training images    : {len(train_images)}")
    print(f"  Epochs             : {args.epochs}")
    if loss_history:
        print(f"  Final det loss     : {loss_history[-1]:.4f}  (↓ = more effective)")
    print(f"  Person dets BEFORE : {total_clean}  (mean conf {mean_conf_clean:.3f})")
    print(f"  Person dets AFTER  : {total_patched}  (mean conf {mean_conf_patched:.3f})")
    print(f"  Detection suppression: {suppression_pct:.1f}%")
    print(f"  Output dir         : {run_dir}/")
    print(f"{'='*52}")


if __name__ == "__main__":
    main()
