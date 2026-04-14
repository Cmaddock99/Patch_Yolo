#!/usr/bin/env python3
"""
experiments/physical_benchmark.py
-----------------------------------
Structured physical benchmark for adversarial patches.

Records detection suppression across a fixed condition matrix of
distance × yaw × lighting using a live webcam. Designed to run
alongside a printed patch held in front of the camera.

Usage
-----
    # Benchmark the v8n patch (print and hold at each condition)
    python experiments/physical_benchmark.py \
        --patch outputs/yolov8n_patch_v2/patches/patch.png \
        --artifact-name v8n_patch_v2 \
        --model yolov8n \
        --output-dir outputs/physical_benchmark

    # Resume / add second artifact later
    python experiments/physical_benchmark.py \
        --patch outputs/yolov8n+yolo11n+yolo26n_joint_patch_v1/patches/patch.png \
        --artifact-name tri_model_patch_v1 \
        --model yolov8n \
        --output-dir outputs/physical_benchmark

Protocol
--------
For each condition the script prompts you to:
  1. Run the clean baseline capture (5 s, no patch).
  2. Hold the printed patch toward the camera and run patched capture (5 s).
  3. Repeat each window a second time for a total of 2 trials per condition.

Condition matrix: 4 distances × 3 yaw angles × 3 lighting levels = 36 conditions,
72 measurement windows per artifact (2 trials × 2 windows each).
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

PERSON_CLASS_ID = 0

# ---------------------------------------------------------------------------
# Condition matrix
# ---------------------------------------------------------------------------

DISTANCES = [0.5, 1.0, 1.5, 2.0]            # metres
YAWS      = [0, 15, 30]                       # degrees from camera axis
LIGHTINGS = ["bright_300lux", "normal_150lux", "dim_45lux"]
TRIALS    = 2
CAPTURE_SECONDS = 5


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_predict(yolo: YOLO, frame_bgr: np.ndarray, conf: float) -> list[dict]:
    """Run YOLO on a BGR frame; return person detections as list of dicts."""
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = yolo.predict(frame_rgb, verbose=False, conf=conf)
    detections = []
    for box in results[0].boxes:
        if int(box.cls.item()) == PERSON_CLASS_ID:
            detections.append({
                "xyxy": box.xyxy[0].cpu().numpy().tolist(),
                "conf": float(box.conf.item()),
            })
    return detections


def synthetic_capture(
    seconds: float,
    is_patched: bool = False,
    has_person_rate_clean: float = 0.75,
    has_person_rate_patched: float = 0.20,
) -> tuple[list[list[dict]], np.ndarray]:
    """
    Generate synthetic frame data for dry-run mode. No camera required.
    Simulates ~30 fps for `seconds`. Returns (per_frame, still).
    """
    n_frames = max(1, int(seconds * 30))
    rate = has_person_rate_patched if is_patched else has_person_rate_clean
    rng = random.Random(42)
    per_frame = []
    for _ in range(n_frames):
        if rng.random() < rate:
            per_frame.append([{"xyxy": [160, 80, 400, 560], "conf": 0.72}])
        else:
            per_frame.append([])
    still = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(still, "DRY-RUN SYNTHETIC FRAME", (60, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (180, 180, 180), 2)
    return per_frame, still


def capture_window(
    cap: cv2.VideoCapture,
    yolo: YOLO,
    conf: float,
    seconds: float,
    label: str,
) -> tuple[list[list[dict]] | None, np.ndarray | None]:
    """
    Capture `seconds` of video from `cap`, running YOLO on each frame.
    Returns:
      - per_frame_detections: list of detection lists (one per frame),
        or None if the user aborted mid-window with 'q'
      - representative_still: the middle frame (BGR), or None on abort

    Callers must check for None and skip logging aborted windows.
    """
    print(f"  [{label}] Capturing {seconds:.0f}s... press 'q' to abort.")
    per_frame: list[list[dict]] = []
    start = time.time()
    frames_collected: list[np.ndarray] = []
    aborted = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        elapsed = time.time() - start
        if elapsed > seconds:
            break
        dets = run_predict(yolo, frame, conf)
        per_frame.append(dets)
        frames_collected.append(frame.copy())

        # Live display with detection count
        disp = frame.copy()
        cv2.putText(disp, f"{label} | {len(dets)} person(s) | {elapsed:.1f}s",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Physical Benchmark", disp)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            aborted = True
            break

    if aborted:
        print(f"  [{label}] Aborted — {len(per_frame)} partial frames discarded.")
        return None, None

    still = frames_collected[len(frames_collected) // 2] if frames_collected else None
    print(f"  [{label}] Done — {len(per_frame)} frames captured.")
    return per_frame, still


def compute_stats(per_frame: list[list[dict]]) -> dict:
    """Aggregate per-frame detection stats."""
    n = len(per_frame)
    if n == 0:
        return {
            "frames": 0, "frame_detection_rate": 0.0,
            "mean_person_count": 0.0, "mean_top_person_conf": 0.0,
        }
    frames_with_person = sum(1 for f in per_frame if f)
    person_counts = [len(f) for f in per_frame]
    top_confs = [max((d["conf"] for d in f), default=0.0) for f in per_frame]
    return {
        "frames": n,
        "frame_detection_rate": round(frames_with_person / n, 4),
        "mean_person_count": round(float(np.mean(person_counts)), 4),
        "mean_top_person_conf": round(float(np.mean(top_confs)), 4),
    }


def prompt_continue(msg: str) -> bool:
    """Wait for user to press Enter. Returns False if user types 'skip'."""
    resp = input(f"\n  {msg} [Enter to continue, 'skip' to skip, 'quit' to stop]: ").strip().lower()
    if resp == "quit":
        raise KeyboardInterrupt
    return resp != "skip"


def save_still(still: np.ndarray | None, path: Path) -> None:
    if still is not None:
        Image.fromarray(cv2.cvtColor(still, cv2.COLOR_BGR2RGB)).save(path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Structured physical adversarial patch benchmark")
    p.add_argument("--patch", type=Path, required=True,
                   help="Path to patch.png artifact to benchmark")
    p.add_argument("--artifact-name", type=str, required=True,
                   help="Short label for this artifact in output rows (e.g. v8n_patch_v2)")
    p.add_argument("--model", type=str, default="yolov8n",
                   help="YOLO model for evaluation (default: yolov8n)")
    p.add_argument("--camera", type=int, default=0,
                   help="Webcam device index (default: 0)")
    p.add_argument("--output-dir", type=Path, default=Path("outputs/physical_benchmark"),
                   help="Directory for CSV, JSON summary, and stills")
    p.add_argument("--conf", type=float, default=0.5,
                   help="Detection confidence threshold (default: 0.5)")
    p.add_argument("--capture-seconds", type=float, default=float(CAPTURE_SECONDS),
                   help=f"Seconds of video per window (default: {CAPTURE_SECONDS})")
    p.add_argument("--trials", type=int, default=TRIALS,
                   help=f"Number of trials per condition (default: {TRIALS})")
    p.add_argument("--dry-run", action="store_true",
                   help="Run one condition only with a 2 s window; for testing without camera")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # Output layout
    out_dir = args.output_dir
    stills_dir = out_dir / "stills" / args.artifact_name
    stills_dir.mkdir(parents=True, exist_ok=True)

    csv_path  = out_dir / f"benchmark_{args.artifact_name}.csv"
    json_path = out_dir / f"summary_{args.artifact_name}.json"

    print(f"\n{'='*60}")
    print(f"  Physical Benchmark")
    print(f"  Artifact   : {args.artifact_name}  ({args.patch})")
    print(f"  Eval model : {args.model}")
    print(f"  Output dir : {out_dir}/")
    print(f"{'='*60}")

    # Load YOLO
    print(f"\nLoading {args.model} ...")
    yolo = YOLO(f"{args.model}.pt")

    # Open camera — skipped in dry-run mode
    cap = None
    if not args.dry_run:
        cap = cv2.VideoCapture(args.camera)
        if not cap.isOpened():
            raise RuntimeError(
                f"Could not open camera {args.camera}. "
                "Check --camera index or connect a webcam."
            )
        print(f"Camera opened (device {args.camera}).")
    else:
        print("Dry-run mode — no camera opened, using synthetic frames.")

    # CSV header
    fieldnames = [
        "artifact", "distance_m", "yaw_deg", "lighting", "trial",
        "frames_clean", "frames_patched",
        "frame_detection_rate_clean", "frame_detection_rate_patched",
        "mean_person_count_clean", "mean_person_count_patched",
        "mean_top_person_conf_clean", "mean_top_person_conf_patched",
        "suppression_vs_clean",
    ]
    csv_exists = csv_path.exists()
    csv_file = csv_path.open("a", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    if not csv_exists:
        writer.writeheader()

    all_rows: list[dict] = []

    # Limit to one condition in dry-run mode
    distances = [DISTANCES[0]] if args.dry_run else DISTANCES
    yaws = [YAWS[0]] if args.dry_run else YAWS
    lightings = [LIGHTINGS[0]] if args.dry_run else LIGHTINGS
    trials = 1 if args.dry_run else args.trials
    cap_secs = 2.0 if args.dry_run else args.capture_seconds

    conditions = [
        (d, y, l)
        for d in distances
        for y in yaws
        for l in lightings
    ]
    total = len(conditions) * trials
    done = 0

    try:
        for dist, yaw, lighting in conditions:
            for trial in range(1, trials + 1):
                done += 1
                cond_label = f"{dist}m  yaw={yaw}°  {lighting}  trial={trial}/{trials}"
                print(f"\n[{done}/{total}] Condition: {cond_label}")

                if not args.dry_run:
                    print(f"  → Set distance to {dist} m, rotate to yaw {yaw}°,")
                    print(f"    set lighting to {lighting}.")
                    if not prompt_continue("Ready for CLEAN baseline?"):
                        print("  Skipped.")
                        continue

                # Clean capture
                if args.dry_run:
                    clean_frames, clean_still = synthetic_capture(cap_secs, is_patched=False)
                else:
                    clean_frames, clean_still = capture_window(
                        cap, yolo, args.conf, cap_secs,
                        label=f"CLEAN  {cond_label}"
                    )
                    if clean_frames is None:
                        print("  Clean window aborted — skipping this trial.")
                        continue
                clean_stats = compute_stats(clean_frames)

                if not args.dry_run:
                    if not prompt_continue("Now HOLD THE PRINTED PATCH toward camera — ready?"):
                        print("  Skipped.")
                        continue

                # Patched capture
                if args.dry_run:
                    patched_frames, patched_still = synthetic_capture(cap_secs, is_patched=True)
                else:
                    patched_frames, patched_still = capture_window(
                        cap, yolo, args.conf, cap_secs,
                        label=f"PATCHED  {cond_label}"
                    )
                    if patched_frames is None:
                        print("  Patched window aborted — skipping this trial.")
                        continue
                patched_stats = compute_stats(patched_frames)

                # Suppression relative to clean detection rate
                clean_rate = clean_stats["frame_detection_rate"]
                patched_rate = patched_stats["frame_detection_rate"]
                suppression = round(
                    (1.0 - patched_rate / max(clean_rate, 1e-6)) * 100.0, 2
                ) if clean_rate > 0 else 0.0

                row = {
                    "artifact": args.artifact_name,
                    "distance_m": dist,
                    "yaw_deg": yaw,
                    "lighting": lighting,
                    "trial": trial,
                    "frames_clean": clean_stats["frames"],
                    "frames_patched": patched_stats["frames"],
                    "frame_detection_rate_clean": clean_stats["frame_detection_rate"],
                    "frame_detection_rate_patched": patched_stats["frame_detection_rate"],
                    "mean_person_count_clean": clean_stats["mean_person_count"],
                    "mean_person_count_patched": patched_stats["mean_person_count"],
                    "mean_top_person_conf_clean": clean_stats["mean_top_person_conf"],
                    "mean_top_person_conf_patched": patched_stats["mean_top_person_conf"],
                    "suppression_vs_clean": suppression,
                }
                writer.writerow(row)
                csv_file.flush()
                all_rows.append(row)

                # Save representative stills
                cond_key = f"{dist}m_{yaw}deg_{lighting}_t{trial}"
                save_still(clean_still,   stills_dir / f"{cond_key}_clean.png")
                save_still(patched_still, stills_dir / f"{cond_key}_patched.png")

                print(f"  Suppression: {suppression:.1f}%  "
                      f"(clean rate={clean_rate:.2f}, patched rate={patched_rate:.2f})")

    except KeyboardInterrupt:
        print("\nBenchmark stopped by user.")
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        csv_file.close()

    # Write JSON summary
    if all_rows:
        supp_vals = [r["suppression_vs_clean"] for r in all_rows]
        summary = {
            "artifact": args.artifact_name,
            "model": args.model,
            "conditions_completed": len(all_rows),
            "suppression_mean": round(float(np.mean(supp_vals)), 2),
            "suppression_std":  round(float(np.std(supp_vals)), 2),
            "suppression_min":  round(float(np.min(supp_vals)), 2),
            "suppression_max":  round(float(np.max(supp_vals)), 2),
            "by_distance": {
                str(d): {
                    "mean_suppression": round(
                        float(np.mean([r["suppression_vs_clean"] for r in all_rows if r["distance_m"] == d])), 2
                    )
                }
                for d in set(r["distance_m"] for r in all_rows)
            },
            "by_lighting": {
                l: {
                    "mean_suppression": round(
                        float(np.mean([r["suppression_vs_clean"] for r in all_rows if r["lighting"] == l])), 2
                    )
                }
                for l in set(r["lighting"] for r in all_rows)
            },
        }
        json_path.write_text(json.dumps(summary, indent=2))
        print(f"\nJSON summary → {json_path}")
        print(f"Mean suppression across {len(all_rows)} conditions: {summary['suppression_mean']:.1f}%")

    print(f"CSV log → {csv_path}")
    print(f"Stills  → {stills_dir}/")


if __name__ == "__main__":
    main()
