#!/usr/bin/env python3
"""
experiments/build_intersection_manifest.py
------------------------------------------
Builds a common-image manifest: the subset of images in data/custom_images/
where ALL THREE of yolov8n, yolo11n, and yolo26n detect at least one person
at conf=0.5, imgsz=640.

Output: data/manifests/common_14.txt  (one absolute path per line)

Run from the repo root:
    python experiments/build_intersection_manifest.py
"""

from __future__ import annotations

from pathlib import Path

from ultralytics import YOLO

CONF = 0.5
IMG_SIZE = 640
PERSON_CLASS_ID = 0
MODELS = ["yolov8n", "yolo11n", "yolo26n"]
IMAGES_DIR = Path("data/custom_images")
MANIFEST_DIR = Path("data/manifests")
MANIFEST_PATH = MANIFEST_DIR / "common_14.txt"


def person_detected(yolo: YOLO, img_path: Path) -> int:
    """Return number of person detections above threshold."""
    results = yolo.predict(str(img_path), verbose=False, conf=CONF, imgsz=IMG_SIZE)
    return sum(1 for b in results[0].boxes if int(b.cls.item()) == PERSON_CLASS_ID)


def main() -> None:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    all_images = sorted(p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in exts)
    if not all_images:
        raise ValueError(f"No images found in {IMAGES_DIR}")
    print(f"Found {len(all_images)} images in {IMAGES_DIR}\n")

    # Per-model detection counts: {path: {model: count}}
    det_counts: dict[Path, dict[str, int]] = {p: {} for p in all_images}

    for model_name in MODELS:
        print(f"Running {model_name} ...")
        yolo = YOLO(f"{model_name}.pt")
        for img_path in all_images:
            det_counts[img_path][model_name] = person_detected(yolo, img_path)
        print(f"  Done.\n")

    # Intersection: all models must detect ≥1 person
    common = [
        p for p in all_images
        if all(det_counts[p][m] >= 1 for m in MODELS)
    ]

    # Print summary table
    header = f"{'Image':<45}" + "".join(f"{m:>10}" for m in MODELS) + f"{'IN SET':>8}"
    print(header)
    print("-" * len(header))
    for p in all_images:
        in_set = "YES" if p in common else "-"
        counts = "".join(f"{det_counts[p][m]:>10}" for m in MODELS)
        print(f"{p.name:<45}{counts}{in_set:>8}")

    print(f"\nCommon subset: {len(common)} / {len(all_images)} images\n")

    # Write manifest
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text("\n".join(str(p.resolve()) for p in common) + "\n")
    print(f"Manifest written → {MANIFEST_PATH}")
    print(f"  ({len(common)} paths, absolute)")


if __name__ == "__main__":
    main()
