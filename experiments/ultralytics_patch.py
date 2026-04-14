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
  is post-processed and has no useful gradients. By default (--loss-source auto),
  compute_v26_one2one_scores() is used: a pre-hook captures the feature maps
  entering the Detect head before the internal detach fires, then applies
  detect_head.one2one_cv3 on live tensors → (B, 80, total_anchors) with
  grad_fn intact. This matches the inference objective exactly.
  (--loss-source one2many uses the restored one2many head as an ablation path.)

Loss: L_total = L_det + tv_weight * L_tv
  L_det : mean of top-k person class scores (sigmoid-scaled to [0,1])
  L_tv  : total variation — keeps patch smooth (printability proxy)

EoT (Expectation over Transformations):
  Random ±position jitter per iteration to improve spatial robustness.

Usage
-----
    # Single model, manifest subset
    python experiments/ultralytics_patch.py \
        --model yolov8n --manifest data/manifests/common_all_models.txt \
        --seed 42 --epochs 1000

    # Warm-start v11n from v8n patch (full gradient budget, info via initialization)
    python experiments/ultralytics_patch.py \
        --model yolo11n --run-name yolo11n_warmstart_from_v8n \
        --load-patch outputs/yolov8n_patch_v2/patches/patch.png \
        --manifest data/manifests/common_all_models.txt --seed 42 --epochs 1000

    # Cross-version transfer eval
    python experiments/ultralytics_patch.py \
        --model yolo11n --eval-only \
        --load-patch outputs/yolov8n_patch_v2/patches/patch.png \
        --manifest data/manifests/common_all_models.txt
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
# YOLO26 gradient fix
# ---------------------------------------------------------------------------
# YOLO('yolo26n.pt') auto-fuses the model on load, setting cv2 = cv3 = None.
# The one2many property returns dict(box_head=None, cls_head=None), so
# forward_head() returns {} immediately — that's why preds_dict["one2many"]
# is always an empty dict and no differentiable scores can be found.
#
# Fix: restore cv2/cv3 from the one2one_cv2/cv3 weights (which survive fuse).
# This gives forward_head() live convolutions, so scores are computed and
# gradients flow patch → feature maps → cv3 → scores → loss.

def restore_v26_one2many_head(inner_model: torch.nn.Module) -> None:
    """
    Undo the fuse() that YOLO loading applies automatically to YOLO26.
    After fuse(), cv2 = cv3 = None, making one2many return {}.
    Restores cv2/cv3 from the one2one_cv2/cv3 modules (same architecture,
    different weights — close enough for adversarial gradient purposes).
    Idempotent: no-op if cv2 is already non-None.
    """
    detect_head = None
    if hasattr(inner_model, "model"):
        detect_head = inner_model.model[-1]

    if detect_head is None:
        raise RuntimeError("[v26] Cannot find inner_model.model[-1]")

    if getattr(detect_head, "cv2", None) is not None:
        return  # not fused, nothing to do

    if not hasattr(detect_head, "one2one_cv2") or not hasattr(detect_head, "one2one_cv3"):
        raise RuntimeError(
            "[v26] Model is fused (cv2=None) but one2one_cv2/cv3 not found. "
            f"Detect head type: {type(detect_head).__name__}, "
            f"attrs: {[a for a in dir(detect_head) if 'cv' in a]}"
        )

    detect_head.cv2 = detect_head.one2one_cv2
    detect_head.cv3 = detect_head.one2one_cv3
    print("  [v26] Restored cv2/cv3 from one2one_cv2/cv3 (fuse() had cleared them); "
          "one2many head is now live and differentiable")


def compute_v26_one2one_scores(
    inner_model: torch.nn.Module,
    image_bchw: torch.Tensor,
) -> torch.Tensor:
    """
    Compute YOLO26 one2one class scores from non-detached feature maps.

    The Detect head internally detaches feature maps before passing them to
    one2one_cv2/cv3, which breaks gradient flow (grad_fn is None on
    preds_dict["one2one"]["scores"]). This function bypasses that detach by:
      1. Registering a forward pre-hook on the Detect head to capture the
         live feature map list before the head's forward() runs.
      2. Applying detect_head.one2one_cv3[i] directly on each captured tensor.

    Returns (B, 80, total_anchors) with grad_fn intact, matching the inference
    objective exactly (inference uses one2one, not one2many).
    """
    detect_head = inner_model.model[-1]
    captured: dict = {}

    def _pre_hook(module, inp):
        # inp is a tuple; inp[0] is the list/tuple of per-scale feature tensors.
        x = inp[0]
        captured["x"] = list(x) if isinstance(x, (list, tuple)) else [x]

    h = detect_head.register_forward_pre_hook(_pre_hook)
    was_training = inner_model.training
    try:
        with torch.inference_mode(False), torch.enable_grad():
            inner_model.train()
            inner_model(image_bchw)
    finally:
        inner_model.train(was_training)
        h.remove()

    if "x" not in captured:
        raise RuntimeError(
            "[v26-one2one] Pre-hook did not fire — Detect head may not be "
            "inner_model.model[-1]. Check model architecture."
        )

    x = captured["x"]  # list of (B, C, H, W) with grad_fn
    cls_preds = [detect_head.one2one_cv3[i](x[i]) for i in range(len(x))]
    scores = torch.cat([c.flatten(2) for c in cls_preds], dim=2)  # (B, 80, A)

    if scores.grad_fn is None:
        raise RuntimeError(
            "[v26-one2one] scores.grad_fn is None after hook-based forward.\n"
            "Ensure image_bchw or model params have requires_grad=True, "
            "and that one2one_cv3 layers exist on the Detect head."
        )
    return scores


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

    v8/v11 : returns (B, 84, 8400) — person class at channel 4.
    v26     : default (auto/one2one) delegates to compute_v26_one2one_scores(),
              returning (B, 80, total_anchors) with grad_fn intact.
              With --loss-source one2many: extracts preds_dict["one2many"]["scores"]
              from the standard forward (ablation path, requires
              restore_v26_one2many_head() to have been called first).

    The model is temporarily put in train() mode for the forward pass so that:
      1. The v26 Detect head returns a raw dict (no postprocessing / NMS).
      2. torch.enable_grad() works reliably — newer ultralytics wraps predict()
         in @smart_inference_mode, which leaves inference-tensor state that
         torch.enable_grad() alone cannot override; switching to train mode
         forces a clean differentiable forward path.
    eval() is restored immediately after.
    """
    is_v26 = "26" in model_name

    # v26 one2one path: delegate immediately to avoid a redundant forward pass.
    # compute_v26_one2one_scores() runs its own forward internally via the hook.
    if is_v26:
        resolved = loss_source if loss_source != "auto" else "one2one"
        if resolved == "one2one":
            return compute_v26_one2one_scores(inner_model, image_bchw)
        # resolved == "one2many" — fall through to standard forward below

    was_training = inner_model.training
    inner_model.train()
    try:
        with torch.inference_mode(False), torch.enable_grad():
            out = inner_model(image_bchw)
    finally:
        if not was_training:
            inner_model.eval()

    if not is_v26:
        # v8/v11: out is a tuple; out[0] is (B, 84, 8400)
        return out[0] if isinstance(out, (tuple, list)) else out

    # v26 one2many ablation path — requires restore_v26_one2many_head()
    # v26: train mode → {"one2many": {...}, "one2one": {...}}
    #      eval  mode → (postprocessed_y, {"one2many": {...}, "one2one": {...}})
    if isinstance(out, dict):
        preds_dict = out                     # train mode (expected)
    elif isinstance(out, (tuple, list)) and len(out) == 2 and isinstance(out[1], dict):
        preds_dict = out[1]                  # eval mode fallback
    else:
        raise RuntimeError(
            f"[v26] Unexpected output structure: "
            f"{[type(o).__name__ for o in out] if isinstance(out, (tuple, list)) else type(out).__name__}\n"
            f"Did restore_v26_one2many_head() run? cv2 should be non-None."
        )

    one2many = preds_dict.get("one2many", {})
    scores = one2many.get("scores") if isinstance(one2many, dict) else None

    if scores is None:
        raise RuntimeError(
            f"[v26] preds_dict['one2many'] has no 'scores' key.\n"
            f"one2many type={type(one2many).__name__}, "
            f"keys={list(one2many.keys()) if isinstance(one2many, dict) else 'N/A'}\n"
            f"Did restore_v26_one2many_head() run successfully?"
        )
    if scores.grad_fn is None:
        raise RuntimeError(
            "[v26] scores.grad_fn is None even after train() + inference_mode(False).\n"
            "Check that at least one of: model params or image_bchw has requires_grad=True."
        )
    return scores  # (B, 80, total_anchors)


def detection_loss(preds: torch.Tensor, topk: int = 10, is_v26: bool = False) -> torch.Tensor:
    """
    Minimize the person class score across anchor points.
    Applies sigmoid to guarantee loss stays in [0, 1].

    preds for v8/v11: (B, 84, 8400) — person score at channel 4
    preds for v26:    (B, 80, total_anchors) — person score at channel 0
    """
    if is_v26:
        person_scores = preds[:, PERSON_CLASS_ID, :].sigmoid()
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
    """Load and resize images listed in a manifest file (one path per line).
    Relative paths are resolved against the current working directory so the
    manifest works both locally and on Colab after %cd into the repo root.
    """
    raw_paths = [l.strip() for l in manifest_path.read_text().splitlines() if l.strip()]
    if not raw_paths:
        raise ValueError(f"Manifest {manifest_path} is empty")
    paths: list[Path] = []
    for raw in raw_paths:
        p = Path(raw)
        if not p.is_absolute():
            p = Path.cwd() / p
        paths.append(p)
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
                   help="Path to an existing patch.png. Without --eval-only: warm-start "
                        "training from this patch instead of random noise (each model still "
                        "gets its full gradient budget; information is shared via "
                        "initialization). With --eval-only: transfer/evaluation mode.")
    p.add_argument("--loss-source", default="auto",
                   choices=["auto", "one2many", "one2one"],
                   help="Raw score tensor for YOLO26 gradient loss. "
                        "auto → one2one for v26 (matches inference objective); "
                        "one2many → ablation path using restored one2many head; "
                        "ignored for v8/v11 (always channel4). Default: auto")
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
    p.add_argument("--co-model", type=str, action="append", default=None,
                   dest="co_models",
                   help="Additional model for joint multi-model training (repeatable). "
                        "E.g. --co-model yolo11n --co-model yolo26n. "
                        "Each --co-model must be paired with a --co-weight.")
    p.add_argument("--co-weight", type=float, action="append", default=None,
                   dest="co_weights",
                   help="Loss weight for the corresponding --co-model (repeatable). "
                        "Primary model receives (1 - sum(co_weights)); sum must be < 1.0. "
                        "E.g. --co-weight 0.20 --co-weight 0.55 gives primary 0.25.")

    # ---- Run identity and checkpoint location --------------------------------
    p.add_argument("--run-name", type=str, default=None,
                   help="Override the auto-generated output directory name. Prevents "
                        "overwriting an existing run. Example: --run-name yolov8n_patch_v3")
    p.add_argument("--checkpoint-dir", type=Path, default=None,
                   help="Directory for checkpoint.pt (default: run output dir). "
                        "Set to a Drive path on Colab so checkpoints survive runtime resets. "
                        "Example: --checkpoint-dir /content/drive/MyDrive/AP_checkpoints")

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
        import random as _random
        _random.seed(args.seed)
        torch.manual_seed(args.seed)
        torch.cuda.manual_seed_all(args.seed)
        np.random.seed(args.seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    device = get_device()
    is_v26 = "26" in args.model
    print(f"Device: {device}")
    print(f"Model:  {args.model}  (end2end={'yes' if is_v26 else 'no'})")

    # Normalize co-model / co-weight lists and validate.
    co_models: list[str] = args.co_models or []
    co_weights: list[float] = args.co_weights or []
    if len(co_models) != len(co_weights):
        raise ValueError(
            f"--co-model and --co-weight must be paired: "
            f"got {len(co_models)} model(s) but {len(co_weights)} weight(s)."
        )
    if co_models and sum(co_weights) >= 1.0:
        raise ValueError(
            f"sum(co_weights)={sum(co_weights):.3f} must be < 1.0 "
            f"(primary model needs a positive share of the gradient budget)."
        )
    primary_weight = 1.0 - sum(co_weights) if co_models else 1.0

    # Output directory — eval-only runs get a distinct name so they don't
    # overwrite training results for the same model.
    if args.eval_only and args.load_patch:
        source_model = args.load_patch.parts[-3] if len(args.load_patch.parts) >= 3 else "unknown"
        run_name = f"{args.model}_from_{source_model}_transfer"
    elif co_models:
        co_str = "+".join(co_models)
        run_name = f"{args.model}+{co_str}_joint_patch_v2"
    else:
        run_name = f"{args.model}_patch_v2"
    # --run-name overrides the auto-generated name so new runs don't clobber old ones.
    if args.run_name:
        run_name = args.run_name
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

    if args.batch_size > len(training_indices):
        print(f"  Warning: --batch-size {args.batch_size} > training images "
              f"{len(training_indices)}; clamping to {len(training_indices)}.")
        args.batch_size = len(training_indices)

    # Ultralytics lazily initializes anchor/stride tensors on first inference
    # inside torch.inference_mode(). Clone them so autograd can use them.
    prepare_inner_for_grad(inner)

    # YOLO26: undo the auto-fuse that YOLO() applies on load.
    # Only needed for the one2many ablation path; compute_v26_one2one_scores()
    # uses a hook and does not require this. Restore anyway so the one2many
    # ablation path is always available without a restart.
    if is_v26 and not args.eval_only:
        restore_v26_one2many_head(inner)

    # Load co-models for joint multi-model training (optional, repeatable).
    co_inners: list[torch.nn.Module] = []
    co_is_v26s: list[bool] = []
    if co_models and not args.eval_only:
        _dummy = np.zeros((args.image_size, args.image_size, 3), dtype=np.uint8)
        for co_model_name in co_models:
            print(f"\nLoading co-model {co_model_name} for joint training ...")
            co_yolo_i = YOLO(f"{co_model_name}.pt")
            co_inner_i = co_yolo_i.model.to(device)
            co_inner_i.eval()
            for param in co_inner_i.parameters():
                param.requires_grad_(False)
            is_v26_co_i = "26" in co_model_name
            # Warm up so anchor/stride tensors are initialized.
            co_yolo_i.predict(_dummy, verbose=False)
            prepare_inner_for_grad(co_inner_i)
            if is_v26_co_i:
                restore_v26_one2many_head(co_inner_i)
            co_inners.append(co_inner_i)
            co_is_v26s.append(is_v26_co_i)
            print(f"  Co-model ready: {co_model_name}")

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
    if args.load_patch and not args.eval_only and not args.load_patch.exists():
        raise FileNotFoundError(
            f"--load-patch path does not exist: {args.load_patch}\n"
            "Check that the source patch was committed and pulled before running."
        )
    if args.load_patch and args.load_patch.exists():
        print(f"\nLoading patch from {args.load_patch} ...")
        patch_img = Image.open(args.load_patch).convert("RGB").resize(
            (args.patch_size, args.patch_size)
        )
        patch_np = np.asarray(patch_img, dtype=np.float32) / 255.0
        patch = torch.from_numpy(patch_np).permute(2, 0, 1).to(device).requires_grad_(not args.eval_only)
    else:
        patch = torch.rand(3, args.patch_size, args.patch_size,
                           device=device, requires_grad=not args.eval_only)

    # -----------------------------------------------------------------------
    # Training loop
    # -----------------------------------------------------------------------
    det_history:  list[float] = []   # per-epoch avg detection loss (kept in checkpoint)
    tv_history:   list[float] = []   # per-epoch avg TV loss
    nps_history:  list[float] = []   # per-epoch avg NPS loss
    last_preds_shape: list[int] | None = None
    start_epoch = 1
    resumed_from_epoch = 0

    # Checkpoint location: Drive-backed dir if provided, else run output dir.
    if args.checkpoint_dir:
        args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_path = args.checkpoint_dir / f"{run_name}_checkpoint.pt"
    else:
        checkpoint_path = run_dir / "checkpoint.pt"

    if not args.eval_only:
        optimizer = torch.optim.Adam([patch], lr=args.lr, betas=(0.9, 0.999))

        # Resume from checkpoint if requested and file exists.
        # NOTE: checkpoint ALWAYS takes priority over --load-patch. On reconnect,
        # the patch printed above as "Loading patch from X" is immediately
        # overwritten here with the checkpoint state. This is correct behavior.
        if args.resume and checkpoint_path.exists():
            ckpt = torch.load(checkpoint_path, map_location=device)
            with torch.no_grad():
                patch.copy_(ckpt["patch"])
            optimizer.load_state_dict(ckpt["optimizer"])
            det_history = ckpt.get("loss_history", [])   # backward-compat key name
            resumed_from_epoch = ckpt["epoch"]
            start_epoch = resumed_from_epoch + 1
            if args.load_patch and args.load_patch.exists():
                print(f"  (warm-start PNG superseded by checkpoint — patch state loaded from epoch {resumed_from_epoch})")
            if start_epoch > args.epochs:
                print(f"\nRun already COMPLETE at epoch {resumed_from_epoch} "
                      f"(TARGET_EPOCH={args.epochs}). "
                      "Raise --epochs to continue training. Running eval only.")
                args.eval_only = True
            else:
                print(f"\nResumed from checkpoint at epoch {resumed_from_epoch} "
                      f"(continuing from epoch {start_epoch} → {args.epochs})")
        else:
            if args.load_patch and args.load_patch.exists():
                print(f"\nWarm-start: initialized from {args.load_patch}")
            print(f"Training for {args.epochs} epochs ...")

        for epoch in tqdm(range(start_epoch, args.epochs + 1), desc="Training"):
            batch_idx = torch.randperm(len(train_images_dev))[: args.batch_size].tolist()
            epoch_loss_det = 0.0
            epoch_loss_tv  = 0.0
            epoch_loss_nps = 0.0

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
                    last_preds_shape = list(preds.shape)

                loss_det = detection_loss(preds, topk=args.topk, is_v26=is_v26) * primary_weight

                # Joint multi-model loss: sum co-model contributions.
                for co_inner_i, co_model_i, co_weight_i, is_v26_co_i in zip(
                    co_inners, co_models, co_weights, co_is_v26s
                ):
                    co_preds = predict_with_grad(
                        co_inner_i, patched_img.unsqueeze(0),
                        loss_source=args.loss_source,
                        model_name=co_model_i,
                    )
                    loss_det = loss_det + detection_loss(
                        co_preds, topk=args.topk, is_v26=is_v26_co_i
                    ) * co_weight_i

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
                epoch_loss_tv  += loss_tv.item()
                epoch_loss_nps += loss_nps.item()

            n = len(batch_idx)
            avg_det = epoch_loss_det / n
            avg_tv  = epoch_loss_tv  / n
            avg_nps = epoch_loss_nps / n
            det_history.append(avg_det)
            tv_history.append(avg_tv)
            nps_history.append(avg_nps)

            if epoch % 50 == 0 or epoch == 1:
                tqdm.write(
                    f"  Epoch {epoch:4d}/{args.epochs} — "
                    f"det: {avg_det:.4f}  tv: {avg_tv:.5f}  nps: {avg_nps:.5f}"
                )

            if args.checkpoint_interval > 0 and epoch % args.checkpoint_interval == 0:
                torch.save({
                    "epoch": epoch,
                    "patch": patch.detach().clamp(0, 1).cpu(),
                    "optimizer": optimizer.state_dict(),
                    "loss_history": det_history,   # keep backward-compat key name
                }, checkpoint_path)

        # Only write patch.png if training actually ran this session.
        # If the run was already COMPLETE (start_epoch > args.epochs caused
        # args.eval_only to be set True above), saving from the Drive checkpoint
        # would overwrite a committed patch with a stale copy — skip it.
        if start_epoch <= args.epochs:
            patch_final = patch.detach().clamp(0, 1).cpu()
            patch_save = (patch_final.permute(1, 2, 0).numpy() * 255).astype(np.uint8)
            Image.fromarray(patch_save).save(run_dir / "patches" / "patch.png")
            print(f"\nPatch saved → {run_dir}/patches/patch.png")
        else:
            print(f"\nPatch save skipped — run was already COMPLETE, no new training occurred.")
        (run_dir / "loss_history.json").write_text(
            json.dumps({"det": det_history, "tv": tv_history, "nps": nps_history})
        )

    # -----------------------------------------------------------------------
    # Evaluation
    # -----------------------------------------------------------------------
    print("\nEvaluating attack effectiveness ...")
    total_clean = sum(len(b) for b in training_boxes)
    total_patched = 0
    total_clean_conf = sum(b[4] for boxes in training_boxes for b in boxes)
    total_patched_conf = 0.0
    patch_eval = patch.detach().clamp(0, 1)  # always detach — patch is never used for grad after this point

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
    # Resolve loss_source label for results.json.
    if is_v26:
        _resolved_src = args.loss_source if args.loss_source != "auto" else "one2one"
        loss_source_label = f"{_resolved_src}_scores"
    else:
        loss_source_label = "channel4"

    summary = {
        # Identity
        "run_name": run_name,
        "model": args.model,
        "joint_models": [args.model] + co_models if co_models else None,
        "joint_weights": [round(primary_weight, 4)] + [round(w, 4) for w in co_weights] if co_models else None,
        # Training provenance
        "epochs": args.epochs,
        "resumed_from_epoch": resumed_from_epoch,
        "manifest_path": str(args.manifest) if args.manifest else None,
        "manifest_count": len(image_paths),
        "training_images": len(train_images),
        "subset_size": len(train_images),
        "warm_start_from": str(args.load_patch) if (args.load_patch and not args.eval_only) else None,
        # Results
        "patch_size": args.patch_size,
        "final_det_loss": round(det_history[-1], 5) if det_history else None,
        "clean_person_detections": total_clean,
        "patched_person_detections": total_patched,
        "detection_suppression_pct": round(suppression_pct, 1),
        "mean_conf_clean": mean_conf_clean,
        "mean_conf_patched": mean_conf_patched,
        # Architecture
        "loss_source": loss_source_label,
        "score_tensor_shape": last_preds_shape,
        "head_end2end": is_v26,
        # Hyperparameters
        "lr": args.lr,
        "tv_weight": args.tv_weight,
        "nps_weight": args.nps_weight,
        "block_erase_prob": args.block_erase_prob,
        "cutout_prob": args.cutout_prob,
        "cutout_size": args.cutout_size,
        "rot_max": args.rot_max,
        "grad_clip": args.grad_clip,
        "checkpoint_interval": args.checkpoint_interval,
        "checkpoint_path": str(checkpoint_path),
        "resumed": args.resume,
        "device": device,
    }
    (run_dir / "results.json").write_text(json.dumps(summary, indent=2))

    print(f"\n{'='*52}")
    print(f"  Model              : {args.model}")
    print(f"  Training images    : {len(train_images)}")
    print(f"  Epochs             : {args.epochs}")
    if det_history:
        print(f"  Final det loss     : {det_history[-1]:.4f}  (↓ = more effective)")
    print(f"  Person dets BEFORE : {total_clean}  (mean conf {mean_conf_clean:.3f})")
    print(f"  Person dets AFTER  : {total_patched}  (mean conf {mean_conf_patched:.3f})")
    print(f"  Detection suppression: {suppression_pct:.1f}%")
    print(f"  Output dir         : {run_dir}/")
    print(f"{'='*52}")


if __name__ == "__main__":
    main()
