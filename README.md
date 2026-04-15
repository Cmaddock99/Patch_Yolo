# Adversarial Patch Attacks on Ultralytics YOLO

A research pipeline for training, evaluating, and demonstrating adversarial patches that suppress person detection across YOLOv8n, YOLO11n, and YOLO26n.

This repository is a research and artifact workspace. It is **not** the canonical
attack-defend-fortify runtime. The canonical executable pipeline lives in
`YOLO-Bad-Triangle`, and any future digital or printable patch support should
enter that pipeline as an attack extension rather than as a second runner.

An adversarial patch is a small image region, optimized via gradient descent, that causes a neural network to stop detecting objects when the patch is present in the scene — either overlaid digitally or printed and placed physically.

---

## Results

### Direct Training (patch trained and evaluated on the same model)

| Model | Suppression | Clean → Patched |
|---|---|---|
| YOLOv8n | **90.0%** | 20 → 2 detections |
| YOLO11n | **72.7%** | 33 → 9 detections |
| YOLO26n | **16.3%** | 43 → 36 detections |

YOLO26n's low suppression despite full loss convergence (`final_det_loss: 0.108`) is a structural finding: training optimizes the auxiliary `one2many` head, but inference uses the `one2one` (Hungarian matching) head. These are architecturally separate.

### Transfer Matrix (patch from one model evaluated on another)

| Patch Source → Eval Model | Suppression |
|---|---|
| v8n → v11n | 33.3% |
| v11n → v8n | 50.0% |
| v26n → v8n | 45.0% |
| v26n → v11n | 24.2% |
| v8n → v26n | 14.0% |
| v11n → v26n | 9.3% |

### Joint Patches (one patch trained against two models simultaneously)

| Joint Patch → Eval Model | Suppression |
|---|---|
| v8n + v11n → v8n | 85.0% |
| v8n + v11n → v11n | 66.7% |
| v8n + v26n → v26n | 18.6% |

### Warm-Start Experiment (v26n initialized from v8n 90% patch, 2000 epochs)

| Direction | Suppression |
|---|---|
| v26n warmstart → v26n | 14.0% |
| v26n warmstart → v8n | 90.0% |
| v26n warmstart → v11n | 36.4% |

Warm-starting confirmed that the v26n barrier is initialization-independent — the optimizer finds the same local minimum regardless of where it starts.

---

## Live Demo

### Setup

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
```

### Digital split-screen demo (no printing needed)

Shows a split-screen: clean YOLO detections on the left, the same frame with the patch digitally overlaid on the right. A running suppression percentage updates every 30 frames.

```bash
python experiments/live_demo.py \
  --patch outputs/yolov8n_patch_v2/patches/patch.png \
  --mode digital
```

Press **Q** to quit.

### Physical demo (print and hold patch in front of camera)

First, generate the print-ready file:

```bash
python experiments/live_demo.py \
  --patch outputs/yolov8n_patch_v2/patches/patch.png \
  --export-print 300
```

This saves `outputs/yolov8n_patch_v2/patches/patch_print_300dpi.png` — an 8" × 8" patch at 300 DPI.

**Print instructions:**
1. Open `patch_print_300dpi.png` in Preview (macOS)
2. Print at **Actual Size / 100%** — disable "Fit to Page"
3. Laminating improves color accuracy
4. Hold at 0.5–2 m from the camera, patch facing forward

Then run the live detection feed:

```bash
python experiments/live_demo.py \
  --patch outputs/yolov8n_patch_v2/patches/patch.png \
  --mode physical
```

Physical suppression will be lower than digital because printer color shift, lighting, and viewing angle perturb the patch. The patch was trained with Non-Printability Score (NPS) loss to partially compensate. Use `experiments/physical_benchmark.py` for a structured physical benchmark instead of quoting a fixed percentage from the deck.

### Demo options

| Flag | Default | Description |
|---|---|---|
| `--patch` | required | Path to `patch.png` |
| `--model` | `yolov8n` | YOLO model to run against |
| `--mode` | `digital` | `digital` or `physical` |
| `--conf` | `0.5` | Detection confidence threshold |
| `--camera` | `0` | Webcam index |
| `--patch-scale` | `4` | Digital overlay upscale factor (4 → 400×400px on screen) |
| `--export-print` | — | Generate print PNG at given DPI and exit |

---

## Training Pipeline

Training runs in Google Colab (GPU required). Open the notebook:

[experiments/colab_run.ipynb](experiments/colab_run.ipynb)

Or open directly in Colab:

```
https://colab.research.google.com/github/Cmaddock99/Patch_Yolo/blob/main/experiments/colab_run.ipynb
```

The notebook runs top to bottom. Edit the parameters cell (§2) to select model, run name, and epoch target before running §5.

The training script (`experiments/ultralytics_patch.py`) supports:
- **Source-only training**: single model gradient descent on the patch
- **Warm-start**: initialize patch from an existing PNG (`--load-patch`)
- **Joint training**: optimize one patch against two models simultaneously (`--co-model`)
- **Robustness augmentations**: DePatch block erasing, T-SEA cutout, EoT rotation, NPS loss, TV loss
- **Drive checkpointing**: saves to Google Drive every 100 epochs for safe Colab reconnect

Outputs from this repo should be treated as external research artifacts and
manual inputs to the broader project, not as canonical run outputs.

---

## Key Technical Findings

**Why YOLO26n is hard:** YOLO26n uses end-to-end Hungarian matching (`head_end2end: true`). During training, gradients flow through the `one2many` auxiliary head. During inference, detections come from the `one2one` head. These heads are architecturally separate — minimizing `one2many` scores does not suppress `one2one` detections. This explains why `final_det_loss` converges lower than v8n/v11n yet suppression is far weaker.

**Transfer asymmetry:** v11n → v8n transfers better (50%) than v8n → v11n (33.3%), suggesting v11n's adversarial features are a superset. v26n patches transfer well to v8n/v11n despite low self-suppression.

**Joint patches:** Joint training with equal gradient weight produces patches that generalize better, at a modest cost to per-model peak suppression.

---

## Project Structure

```
experiments/
  ultralytics_patch.py   # Core training script (all models)
  colab_run.ipynb        # Colab notebook (run this for training)
  live_demo.py           # Webcam demo (digital + physical modes)

outputs/
  yolov8n_patch_v2/      # 90% suppression patch + results
  yolo11n_patch_v2/      # 72.7% suppression patch + results
  yolo26n_patch_v2/      # 16.3% suppression patch + results
  yolov8n+yolo11n_joint_patch_v2/
  yolov8n+yolo26n_joint_patch_v2/
  yolo26n_patch_v2_warmstart/

data/
  manifests/             # Image manifest files (48 shared images)
  custom_images/         # Training images (not committed)

docs/research/           # Literature review, verified sources, study roadmap
```

---

## Setup

```bash
./scripts/bootstrap.sh       # creates .venv, installs requirements.txt
source .venv/bin/activate
python scripts/verify_setup.py
```

Python 3.12. Dependencies: `ultralytics`, `torch`, `torchvision`, `opencv-python`, `pillow`, `numpy`, `tqdm`.
