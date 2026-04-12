# Huang et al. (2022) — T-SEA: Transfer-based Self-Ensemble Attack

## Citation

- Title: *T-SEA: Transfer-based Self-Ensemble Attack on Object Detection*
- Authors: Hao Huang, Ziyan Chen, Huanran Chen, Yongtao Wang
- Venue / Year: CVPR 2023 (arXiv 2211.09773, Nov 2022)
- arXiv: 2211.09773
- URL: https://arxiv.org/abs/2211.09773
- Code: https://github.com/VDIGPKU/T-SEA
- PDF: `docs/papers/huang2022_tsea_transfer_2211.09773.pdf`

## Problem

- What threat model is assumed? Black-box transfer: white-box training on single source model (YOLOv5); black-box evaluation on 7 other detectors. No access to target models during training.
- What detector is attacked? YOLOv5 (white-box source); black-box: YOLOv2, v3, v3tiny, v4, v4tiny, Faster-RCNN, SSD
- What is the attack goal? Improve cross-model transfer of adversarial patches using only a single source model — no ensemble of external models required.

## Method

- Patch type: Standard rectangular adversarial patch; "person" class target
- Optimization method: Self-ensemble across three dimensions applied to a single source model: (1) constrained data augmentation on input images, (2) ShakeDrop model regularization creating implicit model variants, (3) patch cutout (random masking of patch subregions)
- Loss terms: Detection suppression (mAP-reduction objective)
- Key mechanism: ShakeDrop randomly adjusts forward-output and backward-gradient flows in residual blocks, simulating diverse model states without separate model instantiation. Combined with data and patch augmentation, this prevents gradient overfitting to a single model's loss landscape.
- Training details: INRIA Person; patch 300x300; input 416x416; batch 8; max 1000 epochs; Adam
- Physical-world considerations: One qualitative demo — patch displayed on iPad causes YOLOv5 and SSD to miss person (Figure 5, Section 4.6). Not a systematic physical evaluation.

## Experimental Setup

- Dataset: INRIA Person (614 train, 288 test); secondary: COCO-person (1684 images), CCTV-person (559 images)
- Target classes: Person
- Model versions: White-box YOLOv5; black-box: YOLOv2, v3, v3tiny, v4, v4tiny, Faster-RCNN, SSD
- Metrics: mAP (lower = better attack)

## Results

### Table 1 — Black-Box Transfer mAP (YOLOv5 white-box, lower = better) (p. 5)

| Method | v2 | v3 | v3tiny | v4 | v4tiny | v5 | F-RCNN | SSD | BB Avg |
|---|---|---|---|---|---|---|---|---|---|
| AdvPatch (Adam) | 5.66 | 40.26 | 18.07 | 48.49 | 24.44 | 43.38 | 39.27 | 41.28 | 36.46 |
| T-SEA | 1.73 | 4.48 | 2.41 | 5.68 | 7.75 | 6.91 | 16.38 | 20.55 | 9.16 |

T-SEA black-box avg mAP: 9.16% vs AdvPatch 36.46%. Supported (paper's own evaluation).

### Table 3 — SOTA Comparison (p. 8)

| Method | White Box | Black-Box Avg |
|---|---|---|
| NPAP | 38.03 | 61.45 |
| AdvCloak | 33.74 | 59.42 |
| AdvPatch | 5.66 | 36.46 |
| T-SEA | 1.73 | 9.16 |

T-SEA achieves best white-box AND black-box simultaneously. Supported.

### Table 4 — Ablation: Self-Ensemble Strategies (p. 8)

| Strategy | White Box | Black Box |
|---|---|---|
| E-baseline | 13.39 | 48.25 |
| + Constrained Data Aug | 18.47 | 42.42 |
| + Model ShakeDrop | 12.54 | 39.40 |
| + Patch cutout | 6.80 | 32.54 |
| All combined | 1.37 | 19.59 |

All three strategies contribute; combined is best. Supported.

### Table 5 — Cross-Dataset Transfer (p. 9)

T-SEA COCO-person: white-box 37.28, black-box 38.87 vs AdvPatch 45.83 / 52.54.
T-SEA CCTV-person: white-box 38.71, black-box 19.91 vs AdvPatch 38.07 / 34.08.
Particularly strong black-box CCTV transfer (surveillance footage). Supported.

### AdvReal Context (Huang 2025, cross-reference)

In AdvReal Table 3: T-SEA closed-box ASR on YOLOv12 = 21.65% vs AdvReal 70.13%. T-SEA is competitive but below AdvReal's dedicated 3D physical framework.

## Key Claims

1. Single-model self-ensemble achieves black-box transfer comparable to multi-model ensembles. Supported (Tables 1, 3).
2. All three self-ensemble dimensions are individually beneficial and synergistic. Supported (Table 4).
3. Physical viability suggested but not systematically evaluated. Weak (one qualitative demo).
4. Cross-dataset surveillance (CCTV) generalization substantially better than AdvPatch. Supported (Table 5).

## Threat Model

- White-box: YOLOv5; black-box: 7 detectors (YOLO v2-v4tiny, F-RCNN, SSD)
- Dataset: INRIA Person
- Physical: One qualitative iPad demo only

## Limitations and Failure Modes

- YOLOv8, v11, v26 not evaluated. Verified-from-pdf (absence).
- AdvReal reports T-SEA at 21.65% physical ASR on YOLOv12 vs AdvReal 70.13% — physical robustness lags. Supported (cross-reference).
- ShakeDrop is residual-architecture-specific — may need modification for YOLOv8/v11/v26 (C2f blocks). My inference.
- One qualitative physical demonstration insufficient to claim physical robustness. Verified-from-pdf.

## Defensive Takeaways

- ShakeDrop + patch cutout combination is a concrete, implementable improvement to any single-model patch training loop that improves black-box transfer.
- Patch cutout overlaps with DePatch block-wise decoupling — both independently validate segment-erasing as beneficial; corroborates the approach.
- Black-box average mAP of 9.16% is a benchmark to compare capstone patch performance against.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- YOLOv8: High. Self-ensemble approach directly applicable — train on YOLOv8n with ShakeDrop + data aug + patch cutout to improve v11/v26 transfer without accessing those models.
- YOLO11: High. Same reasoning.
- YOLO26: Medium. Technique should help but effect size on NMS-free architecture unknown.
- Capstone relevance: 4/5. Code available (GitHub). Actionable improvement for v2 run if v8->v26 transfer remains below 30%.

## Reproducibility Signals

- Code: https://github.com/VDIGPKU/T-SEA
- Training: INRIA Person; YOLOv5; Adam; 1000 epochs max; 300x300 patch; batch 8
- All ablation configs in Table 4

## Open Questions

- How does T-SEA perform on YOLOv8, v11, v26 as black-box targets?
- Does ShakeDrop work with YOLOv8n C2f blocks?
- Can T-SEA + DePatch block-wise decoupling be combined for additive benefit?
- Is CCTV-person dataset publicly available?
