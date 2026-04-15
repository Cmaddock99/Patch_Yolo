# Paper Review: Tan et al. (2024) — DOEPatch

## Citation

- Title: DOEPatch: Dynamically Optimized Ensemble Model for Adversarial Patches Generation
- Authors: Wenyi Tan, Yang Li, Chenxing Zhao, Zhunga Liu, Quan Pan
- Venue / Year: arXiv:2312.16907 (submitted December 2023; revised September 2024)
- URL: https://arxiv.org/abs/2312.16907
- PDF: ../papers/tan2024_DOEPatch_2312.16907.pdf

## Problem

- What threat model is assumed? White-box (gradients of multiple models used simultaneously); physically realizable (printed T-shirt test); targets ensemble of detectors to improve cross-model robustness.
- What detector or classifier is attacked? YOLOv2, YOLOv3, YOLOv4, Faster R-CNN (VGG16 and ResNet50 backbones).
- What is the attack goal? Generate a single adversarial patch that simultaneously fools multiple object detectors, addressing the transferability problem. Instead of training on one model and hoping it transfers, directly optimize against an ensemble.

## Method

- Patch type: T-shirt wearable adversarial patch (printed at 30cm × 30cm on white cotton).
- Optimization method: Min-Max adversarial training (alternating optimization):
  - **External minimization** (fixed weights w): `min_p Σ(w_i · f_i(p))` — optimize patch to minimize ensemble energy
  - **Internal maximization** (fixed patch): `max_w Σ(w_i · f_i(p))` — update weights via projected gradient descent to maximize energy (find hardest models)
  - Dynamic rate adjustment parameter ν=0.78 controls weight fluctuation speed.
  - Regularization: `L(w) = γ/2 ||w - 1/K||²₂` prevents collapse to single-model focus.
- Loss terms: Ensemble detection loss + NPS (non-printability score) + TV (total variation).
- Transformations: Thin Plate Splines (TPS) for clothing fold simulation, distance-based Gaussian blur, EoT (contrast, brightness, viewing angles).
- Physical-world considerations: 30cm × 30cm printed on cotton T-shirt. Tested indoors and outdoors with c920e camera. Adam optimizer on NVIDIA RTX 3090. LR=0.03.

## Experimental Setup

- Dataset: INRIA Person (614 training, 288 test). Confidence threshold: 0.5; NMS: 0.4.
- Target classes: Person (COCO person class)
- Model versions: YOLOv2, YOLOv3, YOLOv4, Faster R-CNN (VGG16), Faster R-CNN (ResNet50)
- Patch size: 300 × 300 pixels
- Metrics: AP (Average Precision); lower = more effective attack

## Results

**Digital AP after attack:**

| Configuration | YOLOv2 (80.68 clean) | YOLOv3 (87.00 clean) | Faster-VGG (91.04 clean) | YOLOv4 (94.60 clean) |
|---|---|---|---|---|
| DOEPatch(YY) — v2+v3 ensemble | **13.19%** | **29.20%** | 60.91% | 44.05% |
| DOEPatch(YF) — v3+Faster ensemble | 59.64% | 45.09% | **47.10%** | 74.23% |
| DOEPatch(YYF) — v2+v3+Faster | 27.90% | 45.35% | 46.23% | 70.85% |

vs. baselines:
- AdvPatch (Thys): YOLOv2 12.59%, YOLOv3 70.08%
- TCEGA: YOLOv2 15.46%, YOLOv3 57.43%

**Physical test**: Patches printed on T-shirts successfully prevented person detection by YOLOv2 and YOLOv3 in both indoor and outdoor environments. Unpatched individuals were detected in all frames.

**Ablation**: Fixed-weight average ensemble (AEPatch) showed non-convergence and overfitting issues; dynamic weight adjustment was essential.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate. The ensemble approach is directly applicable to training a patch that fools YOLOv8 + YOLO11 simultaneously — a clean experimental design for a capstone.
- Direct relevance to YOLO11: Same — the ensemble could include both v8 and v11 to test cross-version joint patches.
- Direct relevance to YOLO26: Same approach applicable.
- What I can reproduce: Method is well described. Requires INRIA dataset + multiple YOLO weights. TPS transform and ensemble training loop are the main implementation work.
- What I can cite: For ensemble patch training design; for the dynamic weight adjustment approach; for the T-shirt physical test results with multiple model families.

## Open Questions

- Does this transfer across YOLO versions? By design, it trains on multiple versions simultaneously. Transfer to v8/v11/v26 (not in the ensemble) is the open question.
- Is the patch digital only, or physically tested? Both. T-shirt test included.
- Is the code available? arXiv paper — check supplementary for code link.
- What is missing for my project? Only tested on YOLOv2–v4 and Faster R-CNN. No Ultralytics models.

## Normalized Extraction

- Canonical slug: `tan2024_DOEPatch`
- Canonical source record: `docs/papers/tan2024_DOEPatch_2312.16907.pdf`
- Evidence state: `pdf_verified`
- Threat model: White-box adversarial patch generation against an ensemble of detectors, followed by physical T-shirt deployment.
- Detector family and exact version: YOLOv2, YOLOv3, YOLOv4, Faster R-CNN with VGG16 and ResNet50 backbones.
- Attack or defense goal: Produce a single universal patch that remains effective across multiple object detectors by training against a dynamically weighted ensemble.
- Loss or objective: Energy-based ensemble objective with inner maximization over model weights and outer minimization over the patch, plus NPS and TV regularization.
- Transforms / EoT: TPS clothing deformation, Gaussian blur, brightness and contrast changes, and viewpoint variation.
- Dataset: INRIA Person.
- Metrics: AP after attack, plus qualitative physical-world success on printed T-shirts.
- Strongest quantitative result: The `DOEPatch(YY)` configuration reduces YOLOv2 AP to 13.19% and YOLOv3 AP to 29.20% while remaining physically effective when printed on clothing (abstract and Section IV).
- Transfer findings: Joint training across multiple source detectors is more stable than fixed-weight averaging and avoids collapse toward one model.
- Physical findings: Printed T-shirts conceal persons from YOLOv2 and YOLOv3 indoors and outdoors; the paper demonstrates physical viability but does not give modern-Ultralytics numbers.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Direct ensemble-training template for YOLOv8+YOLO11 or YOLOv8+YOLO26 joint patch experiments.
- Reproducible technique to borrow: Min-max weight updates for joint patch training across multiple detectors.
- Citation strength: `pdf_verified`

## Working Packet Status

- Primary repo question: `cross_yolo_transfer`
- Disposition: `method_to_borrow`
