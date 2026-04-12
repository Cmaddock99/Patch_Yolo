# Paper Review: PatchZero — Defending against Adversarial Patch Attacks

## Citation

- Title: *PatchZero: Defending against Adversarial Patch Attacks by Detecting and Zeroing the Patch*
- Authors: Ke Xu*, Yao Xiao*, Zhaoheng Zheng, Kaijie Cai, Ram Nevatia (* equal contribution)
- Venue / Year: WACV 2023 (IEEE Workshop on Applications of Computer Vision)
- DOI: 10.1109/WACV56688.2023.00461
- arXiv: https://arxiv.org/abs/2207.01795
- Code: https://github.com/Trusted-AI/adversarial-robustness-toolbox (uses ART for attacks)

## Triage Summary (from PDF pages 1–5)

### Problem

Adversarial patches evade existing defenses because: (1) patch-size-based defenses (PatchGuard, PatchCleanser) require prior knowledge of attack patch size; (2) adversarial training only works for trained patch types; (3) most defenses are task-specific. PatchZero exploits the observation that adversarial patches are **highly textured and visually different from natural image regions** — this property holds even for naturalistic patches at the pixel distribution level.

The paper frames PatchZero as a **general pipeline** that does not require retraining the downstream classifier or detector, and does not require knowing the patch size in advance.

### Method Overview

**Two-stage pipeline**:

1. **Patch Detector** (d): Takes input image X, outputs a pixel-wise probability map. Binarized via threshold ε_0 = 0.5 to produce binary mask M ∈ {0,1}^{H×W}. The detector is a PSPNet (ResNet-50 backbone) pretrained on ImageNet, trained on a mixture of benign and adversarial images using a patch-segmentation loss (cross-entropy + two auxiliary terms).

2. **Zeroing Step**: Masked region X ⊙ M (adversarial pixels) is filled with mean pixel value X̄ (dataset mean). Produces cleaned image X' = X ⊙ M + X̄ ⊙ (1-M).

**Two-stage adversarial training** to handle adaptive attacks:
- Stage 1: Train patch detector d using DO (Downstream-Only) attack gradients from the downstream classifier/detector
- Stage 2: Switch to BPDA (Backward Pass Differentiable Approximation) attack that considers gradients from BOTH patch detector and downstream model — simulates a white-box adversary who knows about the defense

This two-stage training "accelerates training and improves robustness under the stronger adaptive attacks."

### Experimental Scope

- **Tasks evaluated**: Image classification (ImageNet, RESISC-45), object detection (PASCAL VOC), video classification (UCF101)
- **Object detection model**: Standard detector on PASCAL VOC — not explicitly named as YOLO in the triage pages, but the paper is cited alongside YOLO defenses and the ART codebase is used
- **Attacks compared against**: PatchGuard, PatchCleanser, JPEG compression, adversarial training

### Key Results

**Image classification (Table 1 — ImageNet)**:
| Defense | Benign | MPGD | MAPGD | MCW |
|---------|--------|------|-------|-----|
| Undefended | 81.62% | 14.35% | 9.40% | 49.57% |
| PatchGuard | 60.40% | 48.91% | 48.91% | 56.95% |
| PatchCleanser | 80.54% | 64.30% | 63.57% | 73.12% |
| **PZ (DO)** | **81.47%** | **75.80%** | **76.80%** | **74.24%** |
| PZ (BPDA) | 81.48% | 55.46% | 70.02% | — |

**Image classification (Table 2 — RESISC-45)**:
| Defense | Benign | MPGD | MAPGD |
|---------|--------|------|-------|
| JPEG Comp. | 91.0% | 44.1% | 1.7% |
| Adv. Training | 83.9% | 71.8% | 67.2% |
| **PZ (DO)** | **92.9%** | **87.5%** | **85.0%** |
| PZ (BPDA) | 92.9% | 81.2% | 76.4% |

**Key finding**: PatchZero (DO) outperforms PatchGuard by 26% and PatchCleanser by 13% on MPGD/MAPGD attacks. Performance is not strongly dependent on patch size (except at 2% patch size). Neither PatchGuard nor PatchCleanser can be easily adapted for adaptive attacks.

**Object detection**: Paper confirms evaluation on PASCAL VOC but exact numbers are in later pages (not captured in triage read). The detection figure (Figure 1, middle row) shows correct predictions restored after PatchZero preprocessing on images of bicycles and chairs.

**Limitation noted in paper**: Neither PatchGuard nor PatchCleanser handle adaptive attacks well; PatchZero's DO variant also shows vulnerability to stronger BPDA adaptive attack — performance drops from 87.5% → 81.2% on RESISC-45 MPGD. The BPDA variant is more robust to adaptive attacks.

### Physical World Considerations

"Patch attacks can be highly effective in a variety of tasks and physically realizable via attachment (e.g., a sticker) to real-world objects." The zeroing approach works pre-detection on any input image, so physical patches captured by camera are also handled if they appear in the image as textured regions.

## Relevance to Capstone

- **YOLOv8**: Defense comparison table — PatchZero is one of 5 defense paradigms (detect-and-zero). No retraining needed for the detector; applicable directly to any YOLOv8 deployment.
- **YOLO11**: Same as v8 — detector-agnostic approach.
- **YOLO26**: Same — detector-agnostic preprocessing; does not depend on YOLO architecture.
- **What to cite**: As the "detect and zero" defense paradigm; as a contrast to Ad-YOLO (patch class, needs retraining), NAPGuard (semantic patch detection), SAC/SAR (segment and recover), XAIAD-YOLO (test-time XAI purification), Tereshonok (anomaly reconstruction). PatchZero is distinguished by not requiring retraining and being detector-agnostic.
- **Practical note**: The ART codebase used for attacks in this paper is the same framework used in this repo's baseline (`create_adv_patch.py`).

## Evidence Confidence

High (PDF read; quantitative tables extracted; method fully described).

## Open Questions

- What are the exact object detection (PASCAL VOC) numbers? These are in later pages of the paper.
- Does PatchZero work against naturalistic patches (DAP, Diff-NAT)? The paper notes that naturalistic patches are visually different from random patches but still exhibit texture anomalies; performance against them is not fully characterized in the triage pages.
- Is false positive rate (benign regions incorrectly zeroed) characterized for diverse natural textures?
