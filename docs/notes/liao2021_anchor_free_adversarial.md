# Liao et al. (2021) — Transferable Adversarial Examples for Anchor Free Object Detection

## Citation

- Title: *Transferable Adversarial Examples for Anchor Free Object Detection*
- Authors: Quanyu Liao, Xin Wang, Bin Kong, Siwei Lyu, Bin Zhu, Youbing Yin, Qi Song, Xi Wu
- Venue / Year: IEEE ICME 2021
- arXiv: 2106.01618
- URL: https://arxiv.org/abs/2106.01618
- PDF: `docs/papers/transferable_anchor_free_2106.01618.pdf`

## Problem

- What problem is the paper solving? Attack anchor-free detectors directly instead of assuming anchor-based losses will transfer cleanly into heatmap-style object detection.
- What model family is studied? CenterNet with Resdcn18 and DLA34 backbones as the main anchor-free targets, plus transfer evaluation against CornerNet, Faster R-CNN, and SSD300.
- Why this matters to the repo: It is the clearest local-PDF evidence that attack objectives tuned for one detector output format do not automatically transfer into another detection regime.

## Method

- Core idea: a **Category-wise Attack (CW-Attack)** targets all objects of a category simultaneously rather than attacking one proposal at a time (pp. 1-2).
- The paper introduces two variants:
  - **SCA**: Sparse Category-wise Attack, optimized under an `L0`-style objective to perturb very few pixels.
  - **DCA**: Dense Category-wise Attack, optimized under an `L∞`-style objective using a PGD-like update (pp. 3-4).
- Why category-wise matters: the method attacks both currently detected pixels and "runner-up" pixels near the visual threshold so the detector cannot simply recover by switching to neighboring heatmap peaks (pp. 2-3).
- Key architectural point: anchor-free detectors detect keypoints from heatmaps rather than selecting boxes from anchors, so the attack loss has to target the heatmap/keypoint mechanism directly (pp. 1-2).

## Experimental Setup

- Datasets: PascalVOC and MS-COCO (p. 4).
- Main attacked models: CenterNet with Resdcn18 and DLA34 backbones (p. 5).
- Transfer targets:
  - PascalVOC: Resdcn101, Faster R-CNN, SSD300
  - MS-COCO: CornerNet (pp. 5-6)
- Metrics:
  - `ASR = 1 - mAP_attack / mAP_clean`
  - `ATR = ASR_target / ASR_origin`
  - perceptibility via `PL2` and `PL0` (pp. 4-6).

## Results

- White-box attack performance is strong on anchor-free CenterNet (Table 1, p. 5):
  - PascalVOC, Resdcn18:
    - SCA: clean `0.67` -> attack `0.060`, `ASR 0.91`
    - DCA: clean `0.67` -> attack `0.070`, `ASR 0.90`
  - PascalVOC, DLA34:
    - SCA: clean `0.77` -> attack `0.110`, `ASR 0.86`
    - DCA: clean `0.77` -> attack `0.050`, `ASR 0.94`
  - MS-COCO:
    - Resdcn18 DCA: clean `0.29` -> attack `0.002`, `ASR 0.99`
    - DLA34 DCA: clean `0.37` -> attack `0.002`, `ASR 0.99`
- Black-box transfer remains meaningful across both backbone and detector changes (Tables 2-3, pp. 5-6):
  - PascalVOC, DLA34-SCA -> Faster R-CNN: `mAP 0.44`, `ATR 0.82`
  - PascalVOC, DLA34-SCA -> SSD300: `mAP 0.62`, `ATR 0.42`
  - MS-COCO, DLA34-SCA -> CornerNet: `mAP 0.12`, `ATR 0.88`
- The sparse variant is extremely low-footprint (Table 4, p. 6):
  - `PL0` stays under `1%` on all reported settings
  - e.g. PascalVOC DLA34 SCA uses `0.27%` of pixels.
- The paper explicitly concludes that both SCA and DCA outperform DAG on transferability and robustness to JPEG compression (p. 6).

## Relevance to My Capstone

- Direct relevance to YOLOv8: Medium. YOLOv8 is also anchor-free, but its output format is not the same as CenterNet's heatmap formulation.
- Direct relevance to YOLO11: Medium for the same reason.
- Direct relevance to YOLO26: High as an architecture-mechanism reference. The useful lesson is not that YOLO26 equals CenterNet, but that **output-format mismatch is enough to break naive transfer assumptions**. That sentence is my inference from this paper plus the repo's results.
- What I can cite safely:
  - anchor-free detectors need attack objectives that target their own detection mechanism
  - strong white-box attack performance does not require dense full-image perturbation
  - transfer can survive backbone and detector changes if the attack objective matches the target detector family.

## Open Questions

- How much of the repo's v8 -> v26 drop is caused by anchor-free output mismatch versus one-to-one matching?
- Is there a YOLO-family analogue of the paper's category-wise heatmap attack that would fit YOLO26's one-to-many or one-to-one branches?
- Would a direct attack on selected final predictions outperform the repo's current dense suppression loss on newer YOLO heads?

## Normalized Extraction

- Canonical slug: `liao2021_anchor_free`
- Canonical source record: `docs/papers/transferable_anchor_free_2106.01618.pdf`
- Evidence state: `page_cited`
- Threat model: White-box and black-box digital adversarial examples against anchor-free object detectors.
- Detector family and exact version: CenterNet (Resdcn18, DLA34), CornerNet, Faster R-CNN, SSD300.
- Attack or defense goal: Improve direct and transferable attacks on anchor-free detection by using a category-wise objective.
- Loss or objective: Category-wise attack with sparse (`L0`) and dense (`L∞`) variants operating over target-pixel heatmap sets.
- Transforms / EoT: JPEG recompression is used in transfer evaluation as a realistic degradation step; no physical EoT pipeline is the focus.
- Dataset: PascalVOC, MS-COCO.
- Metrics: mAP, ASR, ATR, PL2, PL0.
- Strongest quantitative result: DCA drives MS-COCO CenterNet mAP down to `0.002` with `ASR 0.99` on both Resdcn18 and DLA34 (Table 1, p. 5).
- Transfer findings: DLA34-SCA reaches `ATR 0.82` on Faster R-CNN in PascalVOC and `ATR 0.88` on CornerNet in MS-COCO (Tables 2-3, pp. 5-6).
- Physical findings: None.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Best used as a detector-output-mismatch reference rather than a direct YOLO benchmark.
- Reproducible technique to borrow: Attack all object instances of a category simultaneously and include near-threshold runner-up detections in the attack target set.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
