# Zong et al. (2022) — Co-DETR: Collaborative Hybrid Assignments Training

## Citation

- Title: *DETRs with Collaborative Hybrid Assignments Training*
- Authors: Zhuofan Zong, Guanglu Song, Yu Liu
- Venue / Year: ICCV 2023 (arXiv 2022)
- DOI: 10.1109/ICCV51070.2023.00621
- arXiv: 2211.12860
- URL: https://arxiv.org/abs/2211.12860
- PDF: `docs/papers/codetr_collaborative_hybrid_assignments_2211.12860.pdf`

## Problem

- What problem is the paper solving? One-to-one set matching in DETR gives too few positive samples, which weakens encoder feature learning and decoder attention learning.
- What model family is studied? DETR variants including Conditional DETR, DAB-DETR, Deformable-DETR, and DINO-Deformable-DETR.
- Why this matters to the repo: It is a direct explanation for why end-to-end one-to-one detectors may need auxiliary one-to-many supervision even if inference remains one-to-one.

## Method

- Core idea: train a DETR with **collaborative hybrid assignments**, meaning one-to-many auxiliary heads supervise the encoder while the original one-to-one branch remains the final inference path (pp. 2-4).
- Auxiliary heads: Faster R-CNN, ATSS, RetinaNet, and FCOS style heads can be attached to encoder features; the paper defaults to ATSS and Faster R-CNN for `K = 2` (pp. 4, 6).
- Customized positive queries: extract positive coordinates from the auxiliary heads and feed them into the decoder as extra positive queries to improve attention learning efficiency (p. 4).
- Training objective: combine the original one-to-one decoder loss with auxiliary decoder losses and encoder losses; auxiliary heads are removed at inference so they add **no inference-time parameters or compute** (p. 4, Eq. 6).

## Experimental Setup

- Dataset: COCO, LVIS, Objects365 pretraining for large models
- Baselines: Conditional DETR, DAB-DETR, Deformable-DETR, improved Deformable-DETR++, DINO-Deformable-DETR
- Metrics: AP on COCO val/test-dev and LVIS val

## Results

- Main headline from the introduction: Co-DETR improves basic Deformable-DETR by **5.8 AP** in the 12-epoch setting and **3.2 AP** in the 36-epoch setting, boosts DINO-Deformable-DETR with Swin-L from `58.5` to `59.5 AP`, and reaches `66.0 AP` on COCO test-dev plus `67.9 AP` on LVIS val with ViT-L (pp. 1-2).
- Table 2, plain baselines (p. 6):
  - Deformable-DETR, 12 epochs: `37.1 -> 42.9 AP` with `K = 2`
  - Deformable-DETR, 36 epochs: `43.3 -> 46.5 AP` with `K = 2`
  - Conditional DETR-C5: `39.4 -> 41.8 AP`
  - DAB-DETR-C5: `41.2 -> 43.5 AP`
- Table 3, strong baselines (p. 6):
  - Deformable-DETR++ with Swin-L: `55.2 -> 56.9 AP`
  - DINO-Deformable-DETR with Swin-L: `58.5 -> 59.5 AP`
- Important nuance: more heads are not always better; the paper reports that a small number of complementary heads (`K <= 2`) works best and too many diverse heads create optimization conflicts (p. 9).

## Relevance to My Capstone

- Direct relevance to YOLOv8: Low. It is not a YOLO paper.
- Direct relevance to YOLO11: Low to medium as a conceptual reference.
- Direct relevance to YOLO26: High. If `YOLO26n` is difficult because inference is effectively one-to-one or end-to-end, this paper suggests that dense auxiliary supervision may still be the missing ingredient during optimization. That is my inference from the paper's training mechanics plus the repo's failure mode.
- What I can cite: one-to-one detectors often need one-to-many auxiliary supervision to learn strong encoder features and useful positive queries.

## Open Questions

- Can the repo's `YOLO26n` attack loss be split into a one-to-one target term plus an auxiliary dense or anchor-style term?
- Would a hybrid attack objective improve direct suppression on `YOLO26n` without hurting transfer?
- Which auxiliary supervision is the closest analogue in the repo setting: ATSS-style positive sampling, FCOS-style center priors, or something closer to the current YOLO loss?

## Normalized Extraction

- Canonical slug: `zong2022_codetr_hybrid_assignments`
- Canonical source record: `docs/papers/codetr_collaborative_hybrid_assignments_2211.12860.pdf`
- Evidence state: `page_cited`
- Threat model: Not an adversarial paper; training-method reference for one-to-one object detectors.
- Detector family and exact version: Conditional DETR, DAB-DETR, Deformable-DETR, DINO-Deformable-DETR, Co-DETR variants.
- Attack or defense goal: Improve end-to-end detector training by combining one-to-one inference with one-to-many auxiliary supervision.
- Loss or objective: Original one-to-one decoder loss plus auxiliary encoder and decoder losses from one-to-many heads; customized positive queries are injected into the decoder.
- Transforms / EoT: None.
- Dataset: COCO, LVIS, Objects365.
- Metrics: AP on COCO val/test-dev and LVIS val.
- Strongest quantitative result: Deformable-DETR improves by 5.8 AP in the 12-epoch setting, and ViT-L Co-DETR reaches 66.0 AP on COCO test-dev plus 67.9 AP on LVIS val (pp. 1-2, 6, 9).
- Transfer findings: None directly; the paper is about training efficiency and supervision density.
- Physical findings: None.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Strongest for YOLO26-style one-to-one mismatch questions; low direct benchmark relevance for YOLOv8 and YOLO11.
- Reproducible technique to borrow: Add auxiliary one-to-many supervision or positive-query surrogates when optimizing against an end-to-end one-to-one detector.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `method_to_borrow`
