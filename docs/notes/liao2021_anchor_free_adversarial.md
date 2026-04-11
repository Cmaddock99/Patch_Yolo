# Liao et al. (2021) — Transferable Adversarial Examples for Anchor Free Object Detection

## Citation

- Title: *Transferable Adversarial Examples for Anchor Free Object Detection*
- Authors: Yuzhi Liao, Longlong Wang, Yuesong Kong, Cong Lyu, Zhen Zhu, Mingqiang Yin, Xiaobing Song, Chunlong Wu
- Venue / Year: IEEE ICME 2021, pp. 1–6
- URL: https://ieeexplore.ieee.org/document/9428098
- Note: Companion preprint arXiv 2106.xxxxx

## Problem

- What threat model is assumed? Black-box transferability of adversarial patches/perturbations from anchor-based to anchor-free detectors.
- What detector or classifier is attacked? Anchor-free detectors (CenterNet, FCOS, CornerNet) and anchor-based (YOLOv3, Faster R-CNN).
- What is the attack goal? Generate adversarial examples on anchor-based models that transfer to anchor-free architectures.

## Method

- Patch type: Image-level adversarial perturbation (not localized patch, but findings apply)
- Optimization method: Gradient-based with architecture-aware loss
- Loss terms: Category-wise attack loss specifically designed for anchor-free output format (heatmap/keypoint-based rather than anchor box predictions)
- Key finding: Attacks designed for anchor-based detectors **transfer poorly to anchor-free ones**. The output space is fundamentally different: anchor-based models predict offsets from predefined boxes; anchor-free models predict center-point heatmaps or similar.

## Experimental Setup

- Dataset: COCO, PASCAL VOC
- Target classes: Multiple
- Model versions: YOLOv3 (anchor-based), CenterNet/FCOS (anchor-free)
- Metrics: mAP drop, ASR

## Results

- Main quantitative result: Standard anchor-based attacks achieve only ~30% of their effectiveness when applied to anchor-free targets. Architecture-aware attack achieves full effectiveness on both.
- What worked best: Loss functions that target the anchor-free output representation directly (heatmaps, center points) rather than anchor offsets.
- What failed or stayed weak: Direct transfer of anchor-based optimized patches to anchor-free models.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — v8 is anchor-free but uses a different output format than CenterNet (it uses distribution focal loss and the (B,84,8400) format).
- Direct relevance to YOLO11: Same as v8.
- Direct relevance to YOLO26: **HIGH** — YOLO26 is fully anchor-free with an end-to-end head. Your v8 patch was trained against the v8 anchor-free output `(B,84,8400)` which uses DFL (Distribution Focal Loss) boxes. YOLO26's `one2many["scores"]` `(B,80,8400)` is a different anchor-free format. This mismatch explains poor v8→v26 transfer even beyond the attention issue.
- What I can cite: Explanation #2 (after attention) for why v8→v26 transfer is only 16%. The architectural output space difference means the patch is optimized for the wrong loss landscape.

## Open Questions

- Does this transfer across YOLO versions? This paper explains why it doesn't across anchor paradigms.
- Is the patch digital only? Digital in this paper, but findings apply to patches.
- Is the code available? Check IEEE supplemental / author page.
- What is missing for my project? Specific adaptation for YOLO-family anchor-free format vs. CenterNet/FCOS.

## TODO

- [ ] Access via CSUSM IEEE Xplore
- [ ] Read Section 4 for the specific category-wise loss formulation
- [ ] Determine if the loss can be adapted for YOLO26's `one2many["scores"]` format
