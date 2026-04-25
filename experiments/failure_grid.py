#!/usr/bin/env python3
"""
experiments/failure_grid.py
---------------------------
Digital failure-grid evaluation for adversarial patches.

Measures how suppression changes when only one nuisance factor varies at a time:
  - patch brightness
  - patch hue
  - patch scale
  - patch rotation

This complements `experiments/physical_benchmark.py` by giving a fast digital
screening pass before a printed-camera benchmark.

Usage
-----
    python experiments/failure_grid.py \
        --patch outputs/yolov8n_patch_v2/patches/patch.png \
        --model yolov8n \
        --manifest data/manifests/common_all_models.txt \
        --output-dir outputs/failure_grid
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Sequence

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

PERSON_CLASS_ID = 0
PLACEMENT_LARGEST_PERSON_TORSO = "largest_person_torso"
PLACEMENT_OFF_OBJECT_FIXED = "off_object_fixed"
PLACEMENT_REGIMES = (PLACEMENT_LARGEST_PERSON_TORSO, PLACEMENT_OFF_OBJECT_FIXED)

DEFAULT_BRIGHTNESS = [0.6, 0.8, 1.0, 1.2, 1.4]
DEFAULT_HUE_DEGREES = [-20, -10, 0, 10, 20]
DEFAULT_SCALE = [0.5, 0.75, 1.0, 1.25]
DEFAULT_ROTATION = [0, 10, 20, 30]


def run_predict(yolo: YOLO, img_hwc_uint8: np.ndarray, conf: float) -> list[dict]:
    """Return person detections on a HWC uint8 RGB image."""
    results = yolo.predict(img_hwc_uint8, verbose=False, conf=conf)
    dets: list[dict] = []
    for box in results[0].boxes:
        if int(box.cls.item()) == PERSON_CLASS_ID:
            dets.append(
                {
                    "xyxy": box.xyxy[0].cpu().numpy().tolist(),
                    "conf": float(box.conf.item()),
                }
            )
    return dets


def load_images_from_manifest(manifest_path: Path, image_size: int) -> list[np.ndarray]:
    raw_paths = [line.strip() for line in manifest_path.read_text().splitlines() if line.strip()]
    if not raw_paths:
        raise ValueError(f"Manifest {manifest_path} is empty")

    arrays: list[np.ndarray] = []
    for raw in raw_paths:
        path = Path(raw)
        if not path.is_absolute():
            path = Path.cwd() / path
        img = Image.open(path).convert("RGB").resize((image_size, image_size))
        arrays.append(np.asarray(img, dtype=np.uint8))
    return arrays


def apply_patch_hwc(img_hwc: np.ndarray, patch_hwc: np.ndarray, top: int, left: int) -> np.ndarray:
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
    top = int(np.clip(round(image_height * margin_ratio), 0, max(image_height - patch_height, 0)))
    left = int(np.clip(round(image_width * margin_ratio), 0, max(image_width - patch_width, 0)))
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


def adjust_patch_brightness(patch_hwc: np.ndarray, factor: float) -> np.ndarray:
    return np.clip(patch_hwc.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def shift_patch_hue(patch_hwc: np.ndarray, degrees: float) -> np.ndarray:
    hsv = cv2.cvtColor(patch_hwc, cv2.COLOR_RGB2HSV).astype(np.int16)
    delta = int(round(degrees / 2.0))
    hsv[..., 0] = (hsv[..., 0] + delta) % 180
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


def scale_patch(patch_hwc: np.ndarray, scale: float) -> np.ndarray:
    h, w = patch_hwc.shape[:2]
    new_h = max(1, int(round(h * scale)))
    new_w = max(1, int(round(w * scale)))
    interp = cv2.INTER_LINEAR if scale >= 1.0 else cv2.INTER_AREA
    return cv2.resize(patch_hwc, (new_w, new_h), interpolation=interp)


def rotate_patch(patch_hwc: np.ndarray, degrees: float) -> np.ndarray:
    h, w = patch_hwc.shape[:2]
    center = ((w - 1) / 2.0, (h - 1) / 2.0)
    matrix = cv2.getRotationMatrix2D(center, degrees, 1.0)
    return cv2.warpAffine(
        patch_hwc,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def evaluate_variant(
    *,
    yolo: YOLO,
    images: list[np.ndarray],
    clean_boxes: list[list[dict]],
    patch_hwc: np.ndarray,
    conf: float,
    placement_regime: str,
) -> dict[str, float | int]:
    total_clean = sum(len(boxes) for boxes in clean_boxes)
    total_patched = 0
    clean_frame_hits = sum(1 for boxes in clean_boxes if boxes)
    patched_frame_hits = 0
    patch_h, patch_w = patch_hwc.shape[:2]

    for img_hwc, boxes in zip(images, clean_boxes):
        top, left = compute_patch_top_left(
            boxes,
            img_hwc.shape[0],
            patch_h,
            placement_regime=placement_regime,
            image_width=img_hwc.shape[1],
            patch_width=patch_w,
        )
        patched = apply_patch_hwc(img_hwc, patch_hwc, top, left)
        patched_dets = run_predict(yolo, patched, conf)
        total_patched += len(patched_dets)
        if patched_dets:
            patched_frame_hits += 1

    n_images = len(images)
    return {
        "n_images": n_images,
        "clean_detections": total_clean,
        "patched_detections": total_patched,
        "frame_detection_rate_clean": round(clean_frame_hits / max(n_images, 1), 4),
        "frame_detection_rate_patched": round(patched_frame_hits / max(n_images, 1), 4),
        "detection_suppression_pct": round(
            (1.0 - total_patched / max(total_clean, 1)) * 100.0,
            2,
        ),
    }


def evaluate_axis(
    *,
    yolo: YOLO,
    images: list[np.ndarray],
    clean_boxes: list[list[dict]],
    patch_hwc: np.ndarray,
    axis_name: str,
    values: Sequence[float],
    transform_fn: Callable[[np.ndarray, float], np.ndarray],
    conf: float,
    placement_regime: str,
) -> list[dict]:
    rows: list[dict] = []
    for value in values:
        transformed = transform_fn(patch_hwc, value)
        metrics = evaluate_variant(
            yolo=yolo,
            images=images,
            clean_boxes=clean_boxes,
            patch_hwc=transformed,
            conf=conf,
            placement_regime=placement_regime,
        )
        rows.append(
            {
                "axis": axis_name,
                "value": value,
                "patch_height": int(transformed.shape[0]),
                "patch_width": int(transformed.shape[1]),
                **metrics,
            }
        )
    return rows


def axis_markdown_table(title: str, rows: list[dict]) -> str:
    lines = [
        f"## {title}",
        "",
        "| value | patch_size | suppression | clean_detections | patched_detections | clean_frame_rate | patched_frame_rate |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['value']}` | `{row['patch_width']}x{row['patch_height']}` | "
            f"{float(row['detection_suppression_pct']):.2f}% | "
            f"{int(row['clean_detections'])} | {int(row['patched_detections'])} | "
            f"{float(row['frame_detection_rate_clean']):.4f} | "
            f"{float(row['frame_detection_rate_patched']):.4f} |"
        )
    lines.append("")
    return "\n".join(lines)


def load_patch_artifact_metadata(patch_path: Path) -> dict:
    sidecar = patch_path.parent / "patch_artifact.json"
    if not sidecar.is_file():
        return {}
    try:
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def summarize_failure_grid_rows(axes: dict[str, list[dict]]) -> dict:
    flat_rows = [row for axis_rows in axes.values() for row in axis_rows]
    if not flat_rows:
        return {"best_cell": None, "worst_cell": None}
    best_cell = max(flat_rows, key=lambda item: float(item["detection_suppression_pct"]))
    worst_cell = min(flat_rows, key=lambda item: float(item["detection_suppression_pct"]))
    return {
        "best_cell": {
            "axis": best_cell["axis"],
            "value": best_cell["value"],
            "suppression_pct": best_cell["detection_suppression_pct"],
        },
        "worst_cell": {
            "axis": worst_cell["axis"],
            "value": worst_cell["value"],
            "suppression_pct": worst_cell["detection_suppression_pct"],
        },
    }


def format_report(payload: dict) -> str:
    lines = [
        f"# Failure Grid Report — {payload['artifact_name']}",
        "",
        f"- Model: `{payload['model']}`",
        f"- Patch: `{payload['patch_path']}`",
        f"- Manifest: `{payload['manifest']}`",
        f"- Placement: `{payload['placement_regime']}`",
        f"- Images: `{payload['n_images']}`",
        "",
    ]
    for axis in ("brightness", "hue_degrees", "scale", "rotation_degrees"):
        title = axis.replace("_", " ").title()
        lines.append(axis_markdown_table(title, payload["axes"][axis]))
    summary = payload.get("summary") or {}
    if summary.get("best_cell") is not None:
        best = summary["best_cell"]
        lines.append(
            f"Best cell: `{best['axis']}={best['value']}` → {float(best['suppression_pct']):.2f}% suppression"
        )
    if summary.get("worst_cell") is not None:
        worst = summary["worst_cell"]
        lines.append(
            f"Worst cell: `{worst['axis']}={worst['value']}` → {float(worst['suppression_pct']):.2f}% suppression"
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Digital failure-grid evaluation for adversarial patches")
    p.add_argument("--patch", type=Path, required=True,
                   help="Path to patch.png artifact to benchmark")
    p.add_argument("--model", type=str, default="yolov8n",
                   help="YOLO model for evaluation (default: yolov8n)")
    p.add_argument("--manifest", type=Path, default=Path("data/manifests/common_all_models.txt"),
                   help="Image list (one path per line)")
    p.add_argument("--output-dir", type=Path, default=Path("outputs/failure_grid"),
                   help="Directory for JSON and Markdown reports")
    p.add_argument("--conf", type=float, default=0.5,
                   help="Detection confidence threshold (default: 0.5)")
    p.add_argument("--image-size", type=int, default=640,
                   help="Image size for loading (default: 640)")
    p.add_argument("--placement-regime", default=None,
                   choices=list(PLACEMENT_REGIMES),
                   help="Patch placement regime used for the digital grid. "
                        "Defaults to the patch_artifact.json sidecar when available.")
    p.add_argument("--brightness-values", nargs="+", type=float, default=DEFAULT_BRIGHTNESS,
                   help="Brightness multipliers for the grid")
    p.add_argument("--hue-values", nargs="+", type=float, default=DEFAULT_HUE_DEGREES,
                   help="Hue shifts in degrees for the grid")
    p.add_argument("--scale-values", nargs="+", type=float, default=DEFAULT_SCALE,
                   help="Patch-scale multipliers for the grid")
    p.add_argument("--rotation-values", nargs="+", type=float, default=DEFAULT_ROTATION,
                   help="Patch rotation angles in degrees for the grid")
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.patch.exists():
        raise FileNotFoundError(f"Patch not found: {args.patch}")
    if not args.manifest.exists():
        raise FileNotFoundError(f"Manifest not found: {args.manifest}")

    artifact_name = args.patch.parent.parent.name if len(args.patch.parts) >= 3 else args.patch.stem
    patch_metadata = load_patch_artifact_metadata(args.patch)
    placement_regime = str(
        args.placement_regime
        or patch_metadata.get("placement_regime")
        or PLACEMENT_LARGEST_PERSON_TORSO
    )
    run_dir = args.output_dir / f"{artifact_name}_on_{args.model}"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print("  Failure Grid")
    print(f"  Artifact  : {artifact_name}")
    print(f"  Patch     : {args.patch}")
    print(f"  Model     : {args.model}")
    print(f"  Manifest  : {args.manifest}")
    print(f"  Placement : {placement_regime}")
    print(f"{'='*60}")

    print(f"\nLoading {args.model} ...")
    yolo = YOLO(f"{args.model}.pt")

    print(f"Loading images from {args.manifest} ...")
    images = load_images_from_manifest(args.manifest, args.image_size)
    clean_boxes = [run_predict(yolo, img, args.conf) for img in images]
    print(f"  {len(images)} images loaded.")

    patch_hwc = np.asarray(Image.open(args.patch).convert("RGB"), dtype=np.uint8)

    axes = {
        "brightness": evaluate_axis(
            yolo=yolo,
            images=images,
            clean_boxes=clean_boxes,
            patch_hwc=patch_hwc,
            axis_name="brightness",
            values=args.brightness_values,
            transform_fn=adjust_patch_brightness,
            conf=args.conf,
            placement_regime=placement_regime,
        ),
        "hue_degrees": evaluate_axis(
            yolo=yolo,
            images=images,
            clean_boxes=clean_boxes,
            patch_hwc=patch_hwc,
            axis_name="hue_degrees",
            values=args.hue_values,
            transform_fn=shift_patch_hue,
            conf=args.conf,
            placement_regime=placement_regime,
        ),
        "scale": evaluate_axis(
            yolo=yolo,
            images=images,
            clean_boxes=clean_boxes,
            patch_hwc=patch_hwc,
            axis_name="scale",
            values=args.scale_values,
            transform_fn=scale_patch,
            conf=args.conf,
            placement_regime=placement_regime,
        ),
        "rotation_degrees": evaluate_axis(
            yolo=yolo,
            images=images,
            clean_boxes=clean_boxes,
            patch_hwc=patch_hwc,
            axis_name="rotation_degrees",
            values=args.rotation_values,
            transform_fn=rotate_patch,
            conf=args.conf,
            placement_regime=placement_regime,
        ),
    }

    payload = {
        "artifact_name": artifact_name,
        "model": args.model,
        "patch_path": str(args.patch),
        "manifest": str(args.manifest),
        "placement_regime": placement_regime,
        "n_images": len(images),
        "axes": axes,
        "summary": summarize_failure_grid_rows(axes),
    }

    json_path = run_dir / "failure_grid_results.json"
    md_path = run_dir / "failure_grid_report.md"
    json_path.write_text(json.dumps(payload, indent=2))
    md_path.write_text(format_report(payload))

    print(f"\nJSON results → {json_path}")
    print(f"Markdown report → {md_path}")
    if payload["summary"]["best_cell"] is not None:
        print(
            "Best cell → "
            f"{payload['summary']['best_cell']['axis']}={payload['summary']['best_cell']['value']} "
            f"({float(payload['summary']['best_cell']['suppression_pct']):.2f}% suppression)"
        )
    if payload["summary"]["worst_cell"] is not None:
        print(
            "Worst cell → "
            f"{payload['summary']['worst_cell']['axis']}={payload['summary']['worst_cell']['value']} "
            f"({float(payload['summary']['worst_cell']['suppression_pct']):.2f}% suppression)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
