"""
live_demo.py — Adversarial patch live webcam demonstration.

Modes
-----
digital  : Split-screen. Left = clean YOLO detections. Right = same frame with
           patch overlaid digitally → fewer / no detections.
physical : Single-panel live feed with detection count. Hold a printed patch in
           front of the camera to observe suppression in real time.

Print export
------------
Pass --export-print 300 to generate a print-ready PNG (300 DPI) and exit.
Print at 100 % scale (disable "fit to page") for accurate physical size.

Usage examples
--------------
# Digital split-screen demo
python experiments/live_demo.py --patch outputs/yolov8n_patch_v2/patches/patch.png --mode digital

# Physical demo (run detection live while holding printed patch)
python experiments/live_demo.py --patch outputs/yolov8n_patch_v2/patches/patch.png --mode physical

# Generate print-ready PNG and exit (no camera needed)
python experiments/live_demo.py --patch outputs/yolov8n_patch_v2/patches/patch.png --export-print 300
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Import shared helpers from the training script
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent))
from ultralytics_patch import apply_patch, compute_torso_placement, run_predict

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------
FONT = cv2.FONT_HERSHEY_SIMPLEX
GREEN = (0, 200, 0)
RED   = (0, 60, 220)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PATCH_BORDER = (0, 165, 255)   # orange border around patch region


def draw_boxes(frame_bgr: np.ndarray, boxes: list, color: tuple) -> np.ndarray:
    out = frame_bgr.copy()
    for box in boxes:
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        conf = float(box[4]) if len(box) > 4 else 0.0
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        label = f"person {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(label, FONT, 0.45, 1)
        cv2.rectangle(out, (x1, max(0, y1 - th - 4)), (x1 + tw + 2, y1), color, -1)
        cv2.putText(out, label, (x1 + 1, max(th, y1 - 3)), FONT, 0.45, WHITE, 1, cv2.LINE_AA)
    return out


def put_label(frame_bgr: np.ndarray, text: str, pos: tuple, scale: float = 0.7,
              color: tuple = WHITE, thickness: int = 2) -> None:
    x, y = pos
    cv2.putText(frame_bgr, text, (x + 1, y + 1), FONT, scale, BLACK, thickness + 1, cv2.LINE_AA)
    cv2.putText(frame_bgr, text, (x, y), FONT, scale, color, thickness, cv2.LINE_AA)


# ---------------------------------------------------------------------------
# Print export
# ---------------------------------------------------------------------------

def export_print(patch_path: Path, dpi: int) -> None:
    patch_img = Image.open(patch_path).convert("RGB")
    pw, ph = patch_img.size          # should be 100×100
    scale = 24                        # 100px × 24 = 2400px → 8 inches at 300 DPI
    new_w, new_h = pw * scale, ph * scale
    big = patch_img.resize((new_w, new_h), Image.NEAREST)
    out_path = patch_path.parent / f"patch_print_{dpi}dpi.png"
    big.save(out_path, dpi=(dpi, dpi))
    print(f"Saved: {out_path}")
    print(f"Size:  {new_w}×{new_h} px  →  {new_w/dpi:.1f}\" × {new_h/dpi:.1f}\" at {dpi} DPI")
    print()
    print("Print instructions:")
    print("  1. Open the PNG in Preview (macOS) or any photo viewer.")
    print("  2. Print at 100% / Actual Size — disable 'Fit to Page'.")
    print("  3. For best results, laminate after printing.")
    print("  4. Hold at 0.5–2 m from the camera, patch facing forward.")
    print("  5. Test against yolov8n — this patch achieves 90% digital suppression.")


# ---------------------------------------------------------------------------
# Digital split-screen mode
# ---------------------------------------------------------------------------

def run_digital(args: argparse.Namespace, yolo: YOLO, patch_t: torch.Tensor) -> None:
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        sys.exit(f"Error: cannot open camera index {args.camera}")

    ph, pw = patch_t.shape[1], patch_t.shape[2]
    # Upscale patch for the digital overlay (preserves adversarial pattern)
    s = args.patch_scale
    patch_scaled = torch.nn.functional.interpolate(
        patch_t.unsqueeze(0), scale_factor=s, mode="nearest"
    ).squeeze(0)

    history: deque[float] = deque(maxlen=30)

    print("Digital demo running — press Q to quit.")
    while True:
        ret, frame_bgr = cap.read()
        if not ret:
            break

        frame_bgr = cv2.flip(frame_bgr, 1)   # mirror so it feels like a selfie cam
        h, w = frame_bgr.shape[:2]
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        # --- Clean detections ---
        clean_boxes = run_predict(yolo, frame_rgb, args.conf)

        # --- Build patched frame ---
        img_t = torch.from_numpy(frame_rgb).permute(2, 0, 1).float() / 255.0
        top, left = compute_torso_placement(clean_boxes, h, w,
                                            patch_scaled.shape[1], patch_scaled.shape[2])
        # clamp so patch stays in frame
        top  = max(0, min(top,  h - patch_scaled.shape[1]))
        left = max(0, min(left, w - patch_scaled.shape[2]))
        patched_t = apply_patch(img_t, patch_scaled, top, left)
        patched_rgb = (patched_t.permute(1, 2, 0).numpy() * 255).clip(0, 255).astype(np.uint8)
        patched_bgr = cv2.cvtColor(patched_rgb, cv2.COLOR_RGB2BGR)

        # --- Patched detections ---
        patched_boxes = run_predict(yolo, patched_rgb, args.conf)

        # --- Draw boxes ---
        left_panel  = draw_boxes(frame_bgr, clean_boxes, GREEN)
        right_panel = draw_boxes(patched_bgr, patched_boxes, RED)

        # Draw patch border on right panel
        py1, px1 = top, left
        py2 = py1 + patch_scaled.shape[1]
        px2 = px1 + patch_scaled.shape[2]
        cv2.rectangle(right_panel, (px1, py1), (px2, py2), PATCH_BORDER, 2)

        # --- Labels ---
        put_label(left_panel,  "CLEAN",   (10, 30))
        put_label(left_panel,  f"Persons: {len(clean_boxes)}", (10, 60))
        put_label(right_panel, "PATCHED", (10, 30), color=(100, 180, 255))
        put_label(right_panel, f"Persons: {len(patched_boxes)}", (10, 60), color=(100, 180, 255))

        # --- Suppression meter ---
        if clean_boxes:
            supp = 1.0 - len(patched_boxes) / len(clean_boxes)
        else:
            supp = 0.0
        history.append(supp)
        avg_supp = sum(history) / len(history)
        supp_pct = int(avg_supp * 100)
        supp_color = GREEN if supp_pct >= 50 else (WHITE if supp_pct >= 20 else RED)

        # --- Compose split screen ---
        canvas = np.hstack([left_panel, right_panel])
        bar_h = 40
        bar = np.zeros((bar_h, canvas.shape[1], 3), dtype=np.uint8)
        put_label(bar, f"Suppression (30-frame avg): {supp_pct}%",
                  (canvas.shape[1] // 2 - 200, 26), scale=0.75, color=supp_color)
        put_label(bar, "Q = quit", (canvas.shape[1] - 100, 26), scale=0.55)
        display = np.vstack([canvas, bar])

        cv2.imshow("Adversarial Patch Demo", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Physical mode
# ---------------------------------------------------------------------------

def run_physical(args: argparse.Namespace, yolo: YOLO) -> None:
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        sys.exit(f"Error: cannot open camera index {args.camera}")

    print("Physical demo running — hold printed patch in front of camera. Press Q to quit.")
    while True:
        ret, frame_bgr = cap.read()
        if not ret:
            break

        frame_bgr = cv2.flip(frame_bgr, 1)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        boxes = run_predict(yolo, frame_rgb, args.conf)
        display = draw_boxes(frame_bgr, boxes, GREEN)

        put_label(display, f"Persons detected: {len(boxes)}", (10, 35), scale=0.9)
        put_label(display, "Hold printed patch toward camera to test suppression",
                  (10, display.shape[0] - 15), scale=0.55, color=(200, 200, 200))
        put_label(display, "Q = quit", (display.shape[1] - 100, 35), scale=0.55)

        cv2.imshow("Adversarial Patch — Physical Demo", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Adversarial patch live demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--patch",  type=Path, required=True,
                   help="Path to patch.png (e.g. outputs/yolov8n_patch_v2/patches/patch.png)")
    p.add_argument("--model",  default="yolov8n",
                   help="YOLO model name (default: yolov8n)")
    p.add_argument("--mode",   choices=["digital", "physical"], default="digital",
                   help="Demo mode (default: digital)")
    p.add_argument("--conf",   type=float, default=0.5,
                   help="Detection confidence threshold (default: 0.5)")
    p.add_argument("--camera", type=int, default=0,
                   help="Webcam index (default: 0)")
    p.add_argument("--patch-scale", type=int, default=4,
                   help="Upscale factor for digital overlay patch (default: 4 → 400×400px)")
    p.add_argument("--export-print", type=int, metavar="DPI", default=0,
                   help="Export print-ready PNG at given DPI and exit (e.g. 300)")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if not args.patch.exists():
        sys.exit(f"Patch not found: {args.patch}")

    # Print export — no camera or model needed
    if args.export_print:
        export_print(args.patch, args.export_print)
        return

    # Load patch tensor (CHW float [0,1])
    patch_img = Image.open(args.patch).convert("RGB")
    patch_t = torch.from_numpy(np.array(patch_img)).permute(2, 0, 1).float() / 255.0

    # Load YOLO model
    print(f"Loading {args.model}...")
    yolo = YOLO(f"{args.model}.pt")

    if args.mode == "digital":
        run_digital(args, yolo, patch_t)
    else:
        run_physical(args, yolo)


if __name__ == "__main__":
    main()
