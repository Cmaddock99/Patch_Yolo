#!/usr/bin/env python3
"""
experiments/defense_eval.py
-----------------------------
Evaluate preprocessing-based defenses against adversarial patches.

Tests three defense families applied at inference time:
  - JPEG re-encoding: quality {95, 85, 75, 50}
  - Gaussian blur:    sigma {1.0, 2.0, 3.0}
  - Random crop-resize: retained area {95%, 90%, 85%} × 10 seeds

For each patch × defense × setting computes:
  - frame_detection_rate_clean (undefended clean baseline)
  - detection_suppression_pct_undefended (attack effectiveness, no defense)
  - detection_suppression_pct_defended (attack effectiveness with defense)
  - clean_cost_pp (clean detection rate drop vs. undefended clean)
  - attack_reduction_pp (suppression drop from defense, positive = defense helps)

A defense passes if attack_reduction_pp > 0 and clean_cost_pp < 5.

Usage
-----
    # Fast dev pass on common_all_models.txt
    python experiments/defense_eval.py \
        --patches outputs/yolov8n_patch_v2/patches/patch.png \
                  outputs/yolov8n+yolo11n+yolo26n_joint_patch_v1/patches/patch.png \
        --model yolov8n \
        --manifest data/manifests/common_all_models.txt \
        --output-dir outputs/defense_eval

    # Multiple patches (can repeat --patches)
    python experiments/defense_eval.py \
        --patches outputs/yolov8n_patch_v2/patches/patch.png \
        --patches outputs/yolo26n_patch_v3_one2one/patches/patch.png \
        --model yolov8n \
        --manifest data/manifests/common_all_models.txt \
        --output-dir outputs/defense_eval
"""

from __future__ import annotations

import argparse
import io
import json
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

PERSON_CLASS_ID = 0

# ---------------------------------------------------------------------------
# Defense implementations
# ---------------------------------------------------------------------------

def defend_jpeg(img_hwc: np.ndarray, quality: int) -> np.ndarray:
    """Re-encode image as JPEG at given quality and decode back."""
    img_pil = Image.fromarray(img_hwc)
    buf = io.BytesIO()
    img_pil.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return np.asarray(Image.open(buf).convert("RGB"))


def defend_blur(img_hwc: np.ndarray, sigma: float) -> np.ndarray:
    """Apply Gaussian blur with given sigma."""
    ksize = max(1, int(6 * sigma) | 1)  # odd kernel, at least 1
    blurred = cv2.GaussianBlur(img_hwc, (ksize, ksize), sigma)
    return blurred


def defend_crop_resize(img_hwc: np.ndarray, retain_frac: float, seed: int) -> np.ndarray:
    """Random crop to `retain_frac` of area, then resize back to original."""
    rng = random.Random(seed)
    h, w = img_hwc.shape[:2]
    crop_h = int(h * retain_frac ** 0.5)
    crop_w = int(w * retain_frac ** 0.5)
    top  = rng.randint(0, h - crop_h)
    left = rng.randint(0, w - crop_w)
    cropped = img_hwc[top : top + crop_h, left : left + crop_w]
    resized = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
    return resized


DEFENSES: dict[str, list[tuple]] = {
    "jpeg": [
        ({"quality": q}, lambda img, q=q: defend_jpeg(img, q))
        for q in [95, 85, 75, 50]
    ],
    "blur": [
        ({"sigma": s}, lambda img, s=s: defend_blur(img, s))
        for s in [1.0, 2.0, 3.0]
    ],
    "crop_resize": [
        ({"retain_frac": f, "seed": seed}, lambda img, f=f, seed=seed: defend_crop_resize(img, f, seed))
        for f in [0.95, 0.90, 0.85]
        for seed in range(10)
    ],
}

# ---------------------------------------------------------------------------
# Evaluation helpers
# ---------------------------------------------------------------------------

def run_predict(yolo: YOLO, img_hwc_uint8: np.ndarray, conf: float) -> list[dict]:
    """Return person detections on a HWC uint8 RGB image."""
    results = yolo.predict(img_hwc_uint8, verbose=False, conf=conf)
    dets = []
    for box in results[0].boxes:
        if int(box.cls.item()) == PERSON_CLASS_ID:
            dets.append({
                "xyxy": box.xyxy[0].cpu().numpy().tolist(),
                "conf": float(box.conf.item()),
            })
    return dets


def load_images_from_manifest(manifest_path: Path, image_size: int) -> list[np.ndarray]:
    """Load images listed in manifest as HWC uint8 RGB arrays."""
    raw_paths = [l.strip() for l in manifest_path.read_text().splitlines() if l.strip()]
    imgs = []
    for raw in raw_paths:
        p = Path(raw) if Path(raw).is_absolute() else Path.cwd() / raw
        img = Image.open(p).convert("RGB").resize((image_size, image_size))
        imgs.append(np.asarray(img, dtype=np.uint8))
    return imgs


def apply_patch_hwc(img_hwc: np.ndarray, patch_hwc: np.ndarray,
                    top: int, left: int) -> np.ndarray:
    ph, pw = patch_hwc.shape[:2]
    result = img_hwc.copy()
    result[top : top + ph, left : left + pw] = patch_hwc
    return result


def compute_torso_top_left(boxes: list[dict], image_size: int, patch_size: int) -> tuple[int, int]:
    if not boxes:
        mid = image_size // 2 - patch_size // 2
        return mid, mid
    biggest = max(boxes, key=lambda b: (b["xyxy"][2] - b["xyxy"][0]) * (b["xyxy"][3] - b["xyxy"][1]))
    x1, y1, x2, y2 = biggest["xyxy"]
    cx = int((x1 + x2) / 2)
    cy = int(y1 + 0.35 * (y2 - y1))
    top  = int(np.clip(cy - patch_size // 2, 0, image_size - patch_size))
    left = int(np.clip(cx - patch_size // 2, 0, image_size - patch_size))
    return top, left


def evaluate_patch_on_images(
    yolo: YOLO,
    images: list[np.ndarray],
    patch_hwc: np.ndarray,
    conf: float,
    defense_fn=None,
) -> dict:
    """
    Run clean inference + patched inference (with optional defense) on all images.
    Returns aggregated stats.
    """
    total_clean = 0
    total_patched = 0
    frames_clean_with_person = 0
    frames_patched_with_person = 0
    patch_size = patch_hwc.shape[0]

    for img_hwc in images:
        # Clean detections (no defense on clean — this is the undefended baseline)
        clean_dets = run_predict(yolo, img_hwc, conf)
        total_clean += len(clean_dets)
        if clean_dets:
            frames_clean_with_person += 1

        top, left = compute_torso_top_left(clean_dets, img_hwc.shape[0], patch_size)
        patched = apply_patch_hwc(img_hwc, patch_hwc, top, left)

        # Apply defense to patched image if provided
        if defense_fn is not None:
            patched = defense_fn(patched)

        patched_dets = run_predict(yolo, patched, conf)
        total_patched += len(patched_dets)
        if patched_dets:
            frames_patched_with_person += 1

    n = len(images)
    return {
        "n_images": n,
        "total_clean_detections": total_clean,
        "total_patched_detections": total_patched,
        "frame_detection_rate_clean": round(frames_clean_with_person / max(n, 1), 4),
        "frame_detection_rate_patched": round(frames_patched_with_person / max(n, 1), 4),
        "detection_suppression_pct": round(
            (1.0 - total_patched / max(total_clean, 1)) * 100.0, 2
        ),
    }


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

PASS_CLEAN_COST_THRESHOLD_PP = 5.0   # defence costs < 5 pp clean detection rate
PASS_MIN_ATTACK_REDUCTION_PP = 0.0   # defence must reduce suppression at all


def format_markdown_table(rows: list[dict], patch_name: str) -> str:
    header = (
        f"\n### {patch_name}\n\n"
        "| defense | setting | suppression_undefended | suppression_defended | "
        "attack_reduction_pp | clean_cost_pp | PASS |\n"
        "|---------|---------|------------------------|----------------------|"
        "--------------------|--------------:|------|\n"
    )
    lines = []
    for r in rows:
        passed = (
            r["attack_reduction_pp"] > PASS_MIN_ATTACK_REDUCTION_PP and
            r["clean_cost_pp"] < PASS_CLEAN_COST_THRESHOLD_PP
        )
        lines.append(
            f"| {r['defense']} | {r['setting']} "
            f"| {r['suppression_undefended']:.1f}% "
            f"| {r['suppression_defended']:.1f}% "
            f"| {r['attack_reduction_pp']:+.1f} pp "
            f"| {r['clean_cost_pp']:+.1f} pp "
            f"| {'✓' if passed else '✗'} |"
        )
    return header + "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Preprocessing defense sweep for adversarial patches")
    p.add_argument("--patches", type=Path, action="append", dest="patches",
                   help="Path to a patch.png to evaluate (repeatable: --patches a --patches b)")
    p.add_argument("--model", type=str, default="yolov8n",
                   help="YOLO model for evaluation (default: yolov8n)")
    p.add_argument("--manifest", type=Path,
                   default=Path("data/manifests/common_all_models.txt"),
                   help="Image list (one path per line)")
    p.add_argument("--output-dir", type=Path, default=Path("outputs/defense_eval"),
                   help="Directory for CSV and markdown report")
    p.add_argument("--conf", type=float, default=0.5,
                   help="Detection confidence threshold (default: 0.5)")
    p.add_argument("--image-size", type=int, default=640,
                   help="Image size for loading (default: 640)")
    p.add_argument("--defenses", nargs="+", default=["jpeg", "blur", "crop_resize"],
                   choices=["jpeg", "blur", "crop_resize"],
                   help="Defense families to evaluate (default: all)")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    patch_paths: list[Path] = [p for p in (args.patches or []) if str(p).strip()]

    if not patch_paths:
        raise ValueError("No --patches provided.")

    for p in patch_paths:
        if not p.exists():
            raise FileNotFoundError(f"Patch not found: {p}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Defense Eval")
    print(f"  Model    : {args.model}")
    print(f"  Manifest : {args.manifest}")
    print(f"  Patches  : {[str(p) for p in patch_paths]}")
    print(f"{'='*60}")

    print(f"\nLoading {args.model} ...")
    yolo = YOLO(f"{args.model}.pt")

    print(f"Loading images from {args.manifest} ...")
    images = load_images_from_manifest(args.manifest, args.image_size)
    print(f"  {len(images)} images loaded.")

    all_results: list[dict] = []
    markdown_sections: list[str] = []

    for patch_path in patch_paths:
        patch_name = patch_path.parent.parent.name  # outputs/<run>/patches/patch.png
        print(f"\n{'─'*50}")
        print(f"Patch: {patch_name}  ({patch_path})")

        patch_pil = Image.open(patch_path).convert("RGB")
        patch_hwc = np.asarray(patch_pil, dtype=np.uint8)

        # Undefended baseline: clean + patched without any defense
        print("  Computing undefended baseline ...")
        baseline = evaluate_patch_on_images(yolo, images, patch_hwc, args.conf, defense_fn=None)
        supp_undefended = baseline["detection_suppression_pct"]
        clean_rate_undefended = baseline["frame_detection_rate_clean"]
        print(f"  Undefended suppression: {supp_undefended:.1f}%  "
              f"(clean frame rate: {clean_rate_undefended:.3f})")

        patch_rows: list[dict] = []

        for defense_name in args.defenses:
            settings_list = DEFENSES[defense_name]
            for params, fn in settings_list:
                setting_str = "  ".join(f"{k}={v}" for k, v in params.items())
                print(f"  Defense: {defense_name}  {setting_str} ...", end=" ", flush=True)

                defended = evaluate_patch_on_images(
                    yolo, images, patch_hwc, args.conf, defense_fn=fn
                )
                supp_defended = defended["detection_suppression_pct"]
                clean_rate_defended = defended["frame_detection_rate_clean"]

                attack_reduction_pp = supp_undefended - supp_defended
                clean_cost_pp = (clean_rate_undefended - clean_rate_defended) * 100.0

                row = {
                    "patch": patch_name,
                    "defense": defense_name,
                    "setting": setting_str,
                    "suppression_undefended": supp_undefended,
                    "suppression_defended": supp_defended,
                    "attack_reduction_pp": round(attack_reduction_pp, 2),
                    "clean_cost_pp": round(clean_cost_pp, 2),
                    "clean_rate_undefended": clean_rate_undefended,
                    "clean_rate_defended": clean_rate_defended,
                    "n_images": baseline["n_images"],
                }
                all_results.append(row)
                patch_rows.append(row)

                passed = (
                    attack_reduction_pp > PASS_MIN_ATTACK_REDUCTION_PP and
                    clean_cost_pp < PASS_CLEAN_COST_THRESHOLD_PP
                )
                print(f"supp={supp_defended:.1f}%  attack_reduction={attack_reduction_pp:+.1f}pp  "
                      f"clean_cost={clean_cost_pp:+.1f}pp  {'PASS' if passed else 'FAIL'}")

        markdown_sections.append(format_markdown_table(patch_rows, patch_name))

    # Write JSON
    json_path = args.output_dir / "defense_results.json"
    json_path.write_text(json.dumps(all_results, indent=2))
    print(f"\nJSON results → {json_path}")

    # Write markdown report
    md_path = args.output_dir / "defense_report.md"
    md_content = (
        f"# Defense Evaluation Report\n\n"
        f"Model: `{args.model}` | "
        f"Manifest: `{args.manifest}` | "
        f"Images: {len(images)}\n\n"
        f"Pass criteria: attack_reduction > {PASS_MIN_ATTACK_REDUCTION_PP} pp  AND  "
        f"clean_cost < {PASS_CLEAN_COST_THRESHOLD_PP} pp\n"
    )
    md_content += "".join(markdown_sections)
    md_path.write_text(md_content)
    print(f"Markdown report → {md_path}")

    # Print best defense per patch
    print(f"\n{'─'*50}")
    print("Best defense per patch (highest attack_reduction that passes clean_cost gate):")
    from itertools import groupby
    for patch_name, group in groupby(all_results, key=lambda r: r["patch"]):
        candidates = [
            r for r in group
            if r["clean_cost_pp"] < PASS_CLEAN_COST_THRESHOLD_PP
        ]
        if candidates:
            best = max(candidates, key=lambda r: r["attack_reduction_pp"])
            print(f"  {patch_name}: {best['defense']} {best['setting']} "
                  f"→ attack_reduction={best['attack_reduction_pp']:+.1f}pp  "
                  f"clean_cost={best['clean_cost_pp']:+.1f}pp")
        else:
            print(f"  {patch_name}: no defense passed the clean_cost gate")


if __name__ == "__main__":
    main()
