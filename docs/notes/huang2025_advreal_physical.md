# Huang et al. (2025) — AdvReal: Physical Adversarial Patch Framework

## Citation

- Title: *AdvReal: Physical adversarial patch generation framework for security evaluation of object detection systems*
- Authors: Huang, Ren, Wang, Huo, Bai, Zhang, Yu
- Venue / Year: Expert Systems with Applications, Vol. 296, Article 128967 (2025)
- DOI: 10.1016/j.eswa.2025.128967
- arXiv: 2505.16402
- URL: https://arxiv.org/abs/2505.16402
- PDF: `docs/papers/huang2025_advreal_physical_2505.16402.pdf`

## Problem

- What threat model is assumed? Physical-world adversarial patch worn on clothing; white-box glass-box training on source detector; closed-box (black-box) evaluation on target detectors. Physical test with rendered 3D clothing on real/nuScenes backgrounds.
- What detector is attacked? YOLOv2 (primary glass-box); evaluated closed-box on YOLOv3, YOLOv5, **YOLOv8, YOLOv11, YOLOv12**, Faster-RCNN, D-DETR
- What is the attack goal? Person vanishing — adversarial clothing patches effective in physical world across diverse detectors including latest SOTA.

## Method

Three-module framework: (1) Patch Adversarial Module, (2) Realistic Enhancement Module, (3) Joint Optimization Module.

- Patch type: Expandable clothing patch (printed on long-sleeve tops and trousers, 6+8 patch placements per person)
- Optimization: [restricted-summary] Gradient-based patch optimization with ShakeDrop regularization that randomly adjusts forward-output and backward-gradient flows; combined 2D detection loss + 3D detection loss + TV loss. Loss weights μ₁=1.0, μ₂=1.0, μ₃=2.5.
- Physical-world considerations:
  - 3D non-rigid surfaces modeling using cloth mesh with stress-point-based deformation (Eq. 2-8 in paper, pp. 6-8)
  - Time-space mapping: renders 3D human model at random distance/angle/azimuth matching background perspective (pp. 7-9, Fig. 4)
  - Relight mapping: SSIM-based optimization of contrast α and brightness β parameters to match rendered model to real background lighting (Algorithm 1, pp. 9-10)
- Training: 800 epochs; Adam lr=0.01; 300×300 patch init; 416×416 input; NVIDIA RTX 4080 16G

## Experimental Setup

- 2D training dataset: INRIA Person (462 train, 100 test)
- 3D training dataset: nuScenes (562 traffic scenes, 6 camera perspectives; 450 daytime, 112 nighttime; 462 train / 100 test)
- Victim detectors (Table 1, p. 12): YOLOv2 (5.58 GFLOPs, 2017), YOLOv3 (193.89, 2018), YOLOv5 (7.70, 2020), **YOLOv8 (8.7, 2023)**, **YOLOv11 (6.50, 2024)**, **YOLOv12 (6.50, 2025)**, Faster-RCNN (180.00, 2016), D-DETR (78.00, 2021)
- Physical evaluation: Long-sleeve tops + trousers; six patch placements on top (2 front, 2 back, 1 per sleeve) + 8 on trousers; real outdoor testing
- Metrics: ASR, Precision, Recall, F1-Score, Average Confidence (AC)

## Results

### Table 3 — Digital Closed-Box ASR (%, higher = better attack; glass-box = YOLOv2)

| Method | YOLOv2 | YOLOv3 | YOLOv5 | YOLOv12 | F-RCNN | D-DETR | Avg |
|---|---|---|---|---|---|---|---|
| AdvPatch | 33.55% | 51.52% | 42.64% | 16.45% | 6.06% | 30.30% | 24.71% |
| AdvTexture | 55.63% | 75.11% | 69.05% | 19.70% | 13.64% | 52.60% | 40.11% |
| T-SEA | 61.90% | 38.10% | 50.65% | 21.65% | 32.25% | 51.52% | 36.74% |
| **AdvReal** | **89.39%** | **77.92%** | **74.46%** | **70.13%** | **51.08%** | **59.09%** | **66.79%** |

(p. 14, Table 3) — **Supported** (paper's own evaluation; glass-box source = YOLOv2)

### Table 7 — Transferability to YOLOv8, YOLOv11, YOLOv12 (closed-box from YOLOv2 glass-box)

| Method | YOLOv8 Recall↓ | YOLOv8 F1↓ | YOLOv11 Recall↓ | YOLOv11 F1↓ | YOLOv12 Recall↓ | YOLOv12 F1↓ |
|---|---|---|---|---|---|---|
| AdvPatch | 57.36% | 71.14% | 77.49% | 85.95% | 83.55% | 90.50% |
| AdvTexture | 71.65% | 82.24% | 77.11% | 86.30% | 80.30% | 88.65% |
| T-SEA-v2 | 60.61% | 70.26% | 76.41% | 84.65% | 78.35% | 87.12% |
| **AdvReal** | **32.68%** | **70.26%** | **32.47%** | **43.60%** | **29.87%** | **43.88%** |

Lower Recall = better attack (fewer true persons detected). AdvReal achieves dramatically lower recall on YOLOv8, v11, v12 than all baselines. (p. 16, Table 7) — **Supported**

**Critical finding for capstone:** AdvReal trained on YOLOv2 transfers to YOLOv8 reducing recall to 32.68% and to YOLOv11 to 32.47%. This represents the best published cross-YOLO-generation transfer result in this corpus.

### Table 4 — Glass-Box ASR at Different IoU Thresholds (YOLOv2 and Faster-RCNN glass-box)

At IoU=0.5: AdvReal YOLOv2 glass-box ASR = **86.80%**; Faster-RCNN glass-box ASR = **99.78%**. (p. 15, Table 4) — **Supported**

### Table 5 — Ablation Study (ASR on YOLOv2 glass-box)

| Components | ASR |
|---|---|
| Baseline only | 87.45% |
| + Non-rigid surfaces | 91.56% |
| + Realistic matching | 90.48% |
| + ShakeDrop | 89.18% |
| All three combined | **93.72%** |

Non-rigid surfaces modeling provides the largest single-module gain. (p. 16, Table 5) — **Supported**

### Table 6 — Robustness under Partial Occlusion (YOLOv2 glass-box)

AdvReal ASR under occlusion: **84.20%** vs T-SEA 36.15%, AdvPatch 26.84%. (p. 16, Table 6) — **Supported**

## Key Claims

1. **AdvReal achieves state-of-art closed-box ASR across 7 detectors including YOLOv8, v11, v12** (Table 3, p. 14). **Supported**.

2. **Naturalistic patches (NatPatch, AdvCaT) achieve near-zero ASR in realistic deployment** — visual naturalness trades away attack effectiveness (p. 14). **Supported** (Table 3: NatPatch 4.11% on YOLOv12, AdvCaT 0.87%).

3. **D-DETR (transformer-based) is consistently harder to fool** than YOLO-family detectors. ASR on D-DETR = 59.09% vs 70.13% on YOLOv12. Consistent with Bayer 2024 finding on RT-DETR robustness. **Supported**.

4. **3D non-rigid surfaces + realistic matching + ShakeDrop are all individually beneficial** and synergistic (Table 5). **Supported (ablation)**.

5. **Cross-generation transfer to YOLOv8/v11/v12 from YOLOv2 glass-box is substantially better than any competing method** (Table 7, Recall 32-33% vs baselines 57-83%). **Supported**.

## Threat Model

- Glass-box source: YOLOv2 (gradient access); all other detectors are closed-box (black-box transfer)
- Physical setting: Outdoor and indoor scenarios; clothing-based patches; 3D rendered training backgrounds from nuScenes traffic scenes
- Human subjects: Multiple subjects; 6 camera perspectives in training data
- Assumption: Attacker can print and wear the adversarial garment

## Limitations and Failure Modes

- Naturalistic methods (AdvCaT at 0%) fail completely — paper explicitly discusses this (p. 14). **Supported**.
- Glass-box YOLOv2 source is old — whether newer glass-box sources (e.g., YOLOv8n white-box) improve transfer further is not evaluated. **My inference (gap)**.
- D-DETR remains more robust, indicating transformer architectures continue to resist transfer attacks. **Supported**.
- Physical evaluation is clothing-based only — no poster/cardboard test comparable to DePatch Table 3 format. **Verified-from-pdf (absence)**.
- Not evaluated on YOLO26 (NMS-free). **Verified-from-pdf (absence)**.

## Defensive Takeaways

- The 3D non-rigid surfaces modeling contribution is the most important for physical robustness — modeling cloth fold stress points is more effective than simply using TPS or affine transforms.
- ShakeDrop regularization improves both attack strength and visual quality (lower AC = more imperceptible) — a method that improves physical effectiveness without sacrificing appearance is relevant to physical plausibility constraints.
- Naturalistic patch approaches (camouflage) fail because realistic textures may positively reinforce person-class detections. This warns against over-naturalizing adversarial patches.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: **Critical.** Table 7 directly reports AdvReal's transfer to YOLOv8 — recall drops to 32.68%, F1 to 70.26%. This is the best-published cross-YOLO-generation transfer result in the corpus with physical plausibility. Baseline for comparing capstone patch.
- **YOLO11**: **Critical.** Directly evaluated — recall 32.47%, F1 43.60%. Among the hardest targets in the paper (lower F1 reduction than v12).
- **YOLO26**: NOT evaluated (not yet available when paper submitted May 2025). **Gap**.
- Capstone relevance: **5/5**. This is the single most important paper for the capstone. It is the only paper in the corpus to directly measure cross-generation (v2→v8, v2→v11) transfer with physical plausibility constraints, using person class, and on modern YOLO versions.

## Reproducibility Signals

- Training parameters: 800 epochs, Adam lr=0.01, patch 300×300 → 416×416 input, RTX 4080 16G (p. 13, Table 2)
- Datasets: INRIA Person (public); nuScenes (public, needs license)
- Loss weights specified: μ₁=1.0, μ₂=1.0, μ₃=2.5; non-rigid params σ=0.8, γ=0.01, ρ=0.2 (Table 2)
- Code: Not mentioned in PDF pages reviewed — **unverified-from-pdf**

## Open Questions

- Does training with YOLOv8n as glass-box (instead of YOLOv2) further improve v8→v11/v26 transfer?
- How does YOLO26's NMS-free design respond — would transfer from YOLOv2 be better or worse than to v12?
- Can the 3D non-rigid surfaces modeling be simplified for digital-only capstone training?
- Is code publicly available?

## Normalized Extraction

- Canonical slug: `huang2025_advreal`
- Canonical source record: `docs/papers/huang2025_advreal_physical_2505.16402.pdf`
- Evidence state: `page_cited`
- Threat model: White-box glass-box training on YOLOv2 with closed-box transfer evaluation on newer detectors; physical adversarial clothing deployment in outdoor and rendered settings.
- Detector family and exact version: YOLOv2, YOLOv3, YOLOv5, YOLOv8, YOLOv11, YOLOv12, Faster R-CNN, D-DETR.
- Attack or defense goal: Person-vanishing physical adversarial patch framework with strong black-box transfer to modern detectors.
- Loss or objective: Joint 2D detection loss, 3D detection loss, and TV regularization with ShakeDrop and realistic-matching modules.
- Transforms / EoT: 3D non-rigid cloth deformation, time-space mapping, relight matching, distance and angle variation, and rendered-to-real consistency.
- Dataset: INRIA Person and nuScenes.
- Metrics: ASR, Precision, Recall, F1-score, and Average Confidence.
- Strongest quantitative result: AdvReal achieves 70.13% ASR on YOLOv12 in closed-box evaluation and drives recall to 32.68% on YOLOv8 and 32.47% on YOLOv11 (Tables 3 and 7, pp. 14-16).
- Transfer findings: Transfer from the YOLOv2 glass-box source remains strong across YOLOv3, YOLOv5, YOLOv8, YOLOv11, and YOLOv12; transformer-style D-DETR is comparatively harder to fool.
- Physical findings: Physical ASR remains above 90% across multiple viewpoints and distances in the paper’s hardest controlled evaluations; non-rigid cloth modeling is the most valuable ablation component.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Direct for YOLOv8 and YOLO11; no YOLO26 evaluation.
- Reproducible technique to borrow: Non-rigid cloth deformation, relight matching, and ShakeDrop are the three portable upgrades to the repo’s physical-robustness path.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `benchmark`
