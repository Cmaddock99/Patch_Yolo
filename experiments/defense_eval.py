#!/usr/bin/env python3
"""
experiments/defense_eval.py
-----------------------------
Legacy preprocessing-baseline evaluation for adversarial patches.

Tests three defense families applied at inference time:
  - JPEG re-encoding: quality {95, 85, 75, 50}
  - Gaussian blur:    sigma {1.0, 2.0, 3.0}
  - Random crop-resize: retained area {95%, 90%, 85%} × 10 seeds

This script is intentionally frozen as the lightweight local baseline.
New defense families should land in `YOLO-Bad-Triangle`.

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
        --patches outputs/yolov8n+yolo11n+yolo26n_joint_patch_v1/patches/patch.png \
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
from typing import Sequence

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

PERSON_CLASS_ID = 0
PLACEMENT_LARGEST_PERSON_TORSO = "largest_person_torso"
PLACEMENT_OFF_OBJECT_FIXED = "off_object_fixed"
PLACEMENT_REGIMES = (PLACEMENT_LARGEST_PERSON_TORSO, PLACEMENT_OFF_OBJECT_FIXED)

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


def compute_torso_top_left(
    boxes: list[dict],
    image_height: int,
    patch_height: int,
    image_width: int | None = None,
    patch_width: int | None = None,
) -> tuple[int, int]:
    image_width = image_height if image_width is None else image_width
    patch_width = patch_height if patch_width is None else patch_width
    if not boxes:
        top = image_height // 2 - patch_height // 2
        left = image_width // 2 - patch_width // 2
        return top, left
    biggest = max(boxes, key=lambda b: (b["xyxy"][2] - b["xyxy"][0]) * (b["xyxy"][3] - b["xyxy"][1]))
    x1, y1, x2, y2 = biggest["xyxy"]
    cx = int((x1 + x2) / 2)
    cy = int(y1 + 0.35 * (y2 - y1))
    top = int(np.clip(cy - patch_height // 2, 0, image_height - patch_height))
    left = int(np.clip(cx - patch_width // 2, 0, image_width - patch_width))
    return top, left


def compute_off_object_top_left(
    image_height: int,
    patch_height: int,
    image_width: int | None = None,
    patch_width: int | None = None,
    margin_ratio: float = 0.05,
) -> tuple[int, int]:
    image_width = image_height if image_width is None else image_width
    patch_width = patch_height if patch_width is None else patch_width
    margin_top = int(round(image_height * margin_ratio))
    margin_left = int(round(image_width * margin_ratio))
    top = int(np.clip(margin_top, 0, max(image_height - patch_height, 0)))
    left = int(np.clip(margin_left, 0, max(image_width - patch_width, 0)))
    return top, left


def compute_patch_top_left(
    boxes: list[dict],
    image_height: int,
    patch_height: int,
    *,
    placement_regime: str,
    image_width: int | None = None,
    patch_width: int | None = None,
) -> tuple[int, int]:
    if placement_regime == PLACEMENT_OFF_OBJECT_FIXED:
        return compute_off_object_top_left(
            image_height,
            patch_height,
            image_width=image_width,
            patch_width=patch_width,
        )
    if placement_regime != PLACEMENT_LARGEST_PERSON_TORSO:
        raise ValueError(
            f"Unsupported placement_regime '{placement_regime}'. "
            f"Expected one of {PLACEMENT_REGIMES}."
        )
    return compute_torso_top_left(
        boxes,
        image_height,
        patch_height,
        image_width=image_width,
        patch_width=patch_width,
    )


def evaluate_patch_on_images(
    yolo: YOLO,
    images: list[np.ndarray],
    patch_hwc: np.ndarray,
    conf: float,
    placement_regime: str,
    defense_fn=None,
) -> dict:
    """
    Run clean inference + patched inference (with optional defense) on all images.

    When defense_fn is provided it is applied to BOTH clean and patched images:
    - clean + defense → frame_detection_rate_clean_defended (measures clean cost)
    - patch + defense → frame_detection_rate_patched (measures attack success)
    - clean undefended → used for torso placement and suppression_pct denominator

    suppression_pct is always vs undefended clean (ASR framing).
    frame_detection_rate_clean_defended enables correct clean_cost_pp in main().
    """
    total_clean = 0
    total_patched = 0
    frames_clean_with_person = 0
    frames_clean_defended_with_person = 0
    frames_patched_with_person = 0
    patch_h, patch_w = patch_hwc.shape[:2]

    for img_hwc in images:
        # Undefended clean — used for torso placement and suppression denominator
        clean_dets = run_predict(yolo, img_hwc, conf)
        total_clean += len(clean_dets)
        if clean_dets:
            frames_clean_with_person += 1

        # Defended clean — measures what the defense costs on a clean scene
        if defense_fn is not None:
            defended_clean_img = defense_fn(img_hwc.copy())
            defended_clean_dets = run_predict(yolo, defended_clean_img, conf)
            if defended_clean_dets:
                frames_clean_defended_with_person += 1

        top, left = compute_patch_top_left(
            clean_dets,
            img_hwc.shape[0],
            patch_h,
            placement_regime=placement_regime,
            image_width=img_hwc.shape[1],
            patch_width=patch_w,
        )
        patched = apply_patch_hwc(img_hwc, patch_hwc, top, left)

        # Apply defense to patched image if provided
        if defense_fn is not None:
            patched = defense_fn(patched)

        patched_dets = run_predict(yolo, patched, conf)
        total_patched += len(patched_dets)
        if patched_dets:
            frames_patched_with_person += 1

    n = len(images)
    # frame_detection_rate_clean_defended equals the undefended rate when no
    # defense is active (baseline call), so clean_cost_pp is 0 in that case.
    clean_defended_rate = (
        round(frames_clean_defended_with_person / max(n, 1), 4)
        if defense_fn is not None
        else round(frames_clean_with_person / max(n, 1), 4)
    )
    return {
        "n_images": n,
        "total_clean_detections": total_clean,
        "total_patched_detections": total_patched,
        "frame_detection_rate_clean": round(frames_clean_with_person / max(n, 1), 4),
        "frame_detection_rate_clean_defended": clean_defended_rate,
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


def passes_gate(attack_reduction_pp: float, clean_cost_pp: float) -> bool:
    return (
        attack_reduction_pp > PASS_MIN_ATTACK_REDUCTION_PP and
        clean_cost_pp < PASS_CLEAN_COST_THRESHOLD_PP
    )


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
        lines.append(
            f"| {r['defense']} | {r['setting']} "
            f"| {r['suppression_undefended']:.1f}% "
            f"| {r['suppression_defended']:.1f}% "
            f"| {r['attack_reduction_pp']:+.1f} pp "
            f"| {r['clean_cost_pp']:+.1f} pp "
            f"| {'✓' if r['passes_gate'] else '✗'} |"
        )
    return header + "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Preprocessing defense sweep for adversarial patches")
    p.add_argument("--patches", type=Path, action="append", dest="patches",
                   help="Path to a patch.png to evaluate (repeatable: --patches a --patches b)")
    p.add_argument("--model", type=str, default="yolov8n",
                   help="YOLO model for evaluation (default: yolov8n)")
    p.add_argument("--manifest", type=Path,
                   default=Path("data/manifests/common_all_models.txt"),
                   help="Image list (one path per line)")
    p.add_argument("--output-dir", type=Path, default=Path("outputs/defense_eval"),
                   help="Directory for JSON results and markdown report")
    p.add_argument("--conf", type=float, default=0.5,
                   help="Detection confidence threshold (default: 0.5)")
    p.add_argument("--image-size", type=int, default=640,
                   help="Image size for loading (default: 640)")
    p.add_argument("--defenses", nargs="+", default=["jpeg", "blur", "crop_resize"],
                   choices=["jpeg", "blur", "crop_resize"],
                   help="Defense families to evaluate (default: all)")
    p.add_argument("--placement-regime", default=PLACEMENT_LARGEST_PERSON_TORSO,
                   choices=list(PLACEMENT_REGIMES),
                   help="Patch placement regime used for defended evaluation. "
                        "largest_person_torso pastes on the largest detected torso; "
                        "off_object_fixed pastes at a deterministic upper-left location.")
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    patch_paths: list[Path] = [p for p in (args.patches or []) if str(p).strip()]

    if not patch_paths:
        raise ValueError("No --patches provided.")
    if not args.manifest.exists():
        raise FileNotFoundError(f"Manifest not found: {args.manifest}")

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
        baseline = evaluate_patch_on_images(
            yolo,
            images,
            patch_hwc,
            args.conf,
            placement_regime=args.placement_regime,
            defense_fn=None,
        )
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
                    yolo,
                    images,
                    patch_hwc,
                    args.conf,
                    placement_regime=args.placement_regime,
                    defense_fn=fn,
                )
                supp_defended = defended["detection_suppression_pct"]
                clean_rate_defended = defended["frame_detection_rate_clean_defended"]

                attack_reduction_pp = supp_undefended - supp_defended
                clean_cost_pp = (clean_rate_undefended - clean_rate_defended) * 100.0
                passed = passes_gate(attack_reduction_pp, clean_cost_pp)

                row = {
                    "patch": patch_name,
                    "patch_path": str(patch_path),
                    "defense": defense_name,
                    "setting": setting_str,
                    "suppression_undefended": supp_undefended,
                    "suppression_defended": supp_defended,
                    "attack_reduction_pp": round(attack_reduction_pp, 2),
                    "clean_cost_pp": round(clean_cost_pp, 2),
                    "clean_rate_undefended": clean_rate_undefended,
                    "clean_rate_defended": clean_rate_defended,
                    "n_images": baseline["n_images"],
                    "placement_regime": args.placement_regime,
                    "passes_gate": passed,
                }
                all_results.append(row)
                patch_rows.append(row)

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
        f"Images: {len(images)} | "
        f"Placement: `{args.placement_regime}`\n\n"
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
            if r["passes_gate"]
        ]
        if candidates:
            best = max(candidates, key=lambda r: r["attack_reduction_pp"])
            print(f"  {patch_name}: {best['defense']} {best['setting']} "
                  f"→ attack_reduction={best['attack_reduction_pp']:+.1f}pp  "
                  f"clean_cost={best['clean_cost_pp']:+.1f}pp")
        else:
            print(f"  {patch_name}: no defense passed the clean_cost gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
