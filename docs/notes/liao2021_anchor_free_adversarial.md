# Liao et al. (2021) — Transferable Adversarial Examples for Anchor Free Object Detection

## Citation

- Title: *Transferable Adversarial Examples for Anchor Free Object Detection*
- Authors: Yuzhi Liao, Longlong Wang, Yuesong Kong, Cong Lyu, Zhen Zhu, Mingqiang Yin, Xiaobing Song, Chunlong Wu
- Venue / Year: IEEE ICME 2021, pp. 1–6
- URL: https://ieeexplore.ieee.org/document/9428098
- Note: Companion preprint arXiv 2106.xxxxx

## Evidence Note

This file is a blocker record, not a synthesis-grade review. There is no local PDF in the repo, so architecture and result claims remain unverified until the full text is available inside the workspace.

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

## Normalized Extraction

- Canonical slug: `liao2021_anchor_free`
- Canonical source record: `IEEE ICME entry only; no local PDF in repo`
- Evidence state: `blocked_access`
- Threat model: Transfer attack from anchor-based to anchor-free detection, currently inferred from metadata and prior repo notes.
- Detector family and exact version: Anchor-based YOLOv3 and anchor-free detectors such as CenterNet or FCOS, pending full-text confirmation.
- Attack or defense goal: Explain or improve transfer from anchor-based outputs to anchor-free outputs.
- Loss or objective: Architecture-aware category-wise attack loss, exact formulation blocked.
- Transforms / EoT: Unknown until full text is available.
- Dataset: Unknown until full text is available.
- Metrics: Unknown until full text is available.
- Strongest quantitative result: Unknown in repo-first mode; previously cited percentages remain unpromoted.
- Transfer findings: Repo currently treats this as the anchor-free mismatch citation, but exact effect size is blocked.
- Physical findings: Unknown.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Potentially high for YOLO26 output-format mismatch, but still blocked.
- Reproducible technique to borrow: None can be promoted until the exact attack loss is verified from full text.
- Citation strength: `blocked_access`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Repo currently relies on this for: Anchor-free output mismatch as a secondary explanation for poor v8/v26 transfer.
- Exact missing detail preventing promotion: Exact models, loss definition, and quantitative transfer results.
- Blocker type: `architectural`
- Promotion rule: Keep this paper out of promoted benchmark claims until a local PDF is added and read.
