#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MODULES = [
    "cv2",
    "fitz",
    "matplotlib",
    "numpy",
    "torch",
    "torchvision",
    "yolov5",
    "PIL",
    "art",
    "feedparser",
    "requests",
    "yaml",
]

OPTIONAL_MODULES = [
    ("ultralytics", "Needed for YOLOv8, YOLO11, and YOLO26 workflows."),
]


def check_module(name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(name)
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"
    return True, "ok"


def main() -> int:
    failures = 0

    print("== Python ==")
    print(sys.version.split()[0])
    print()

    print("== Required Modules ==")
    for module in REQUIRED_MODULES:
        ok, message = check_module(module)
        status = "OK" if ok else "FAIL"
        print(f"{status:4} {module:<14} {message}")
        if not ok:
            failures += 1
    print()

    print("== Optional Modules ==")
    for module, note in OPTIONAL_MODULES:
        ok, message = check_module(module)
        status = "OK" if ok else "MISS"
        suffix = message if ok else f"{message} | {note}"
        print(f"{status:4} {module:<14} {suffix}")
    print()

    print("== Paths ==")
    paths = {
        "config": ROOT / "data/configs/adv_patch_default_config.json",
        "images_dir": ROOT / "data/custom_images",
        "weights": ROOT / "yolov5s.pt",
        "knowledge_base": ROOT / "docs/research/YOLO_Adversarial_Patch_Knowledge_Repo.md",
        "roadmap": ROOT / "docs/research/study_roadmap.md",
        "research_config": ROOT / "research/config/research_queries.yaml",
        "research_seeds": ROOT / "research/config/seed_papers.yaml",
        "research_schema": ROOT / "research/schemas/paper_record.example.json",
        "research_auto_note": ROOT / "research/scripts/auto_note.py",
    }

    for label, path in paths.items():
        exists = path.exists()
        status = "OK" if exists else "MISS"
        print(f"{status:4} {label:<14} {path}")
        if not exists and label in {
            "config",
            "images_dir",
            "knowledge_base",
            "roadmap",
            "research_config",
            "research_seeds",
            "research_schema",
        }:
            failures += 1

    image_dir = paths["images_dir"]
    if image_dir.exists():
        image_count = sum(1 for path in image_dir.iterdir() if path.is_file() and not path.name.startswith("."))
        print(f"INFO images_dir count={image_count}")
        if image_count == 0:
            print("INFO add JPG/PNG images to data/custom_images before running create_adv_patch.py")

    if not paths["weights"].exists():
        print("INFO yolov5s.pt is missing; the baseline script expects local weights or an explicit --weights path")

    print()
    print("== Result ==")
    if failures:
        print(f"Setup check finished with {failures} blocking issue(s).")
        return 1

    print("Setup check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
