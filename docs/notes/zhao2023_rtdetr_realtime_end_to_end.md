# Zhao et al. (2023) — RT-DETR: Real-Time End-to-End Object Detection

## Citation

- Title: *DETRs Beat YOLOs on Real-time Object Detection*
- Authors: Yian Zhao, Wenyu Lv, Shangliang Xu, Jinman Wei, Guanzhong Wang, Qingqing Dang, Yi Liu, Jie Chen
- Venue / Year: arXiv 2023
- DOI: 10.48550/arXiv.2304.08069
- arXiv: 2304.08069
- URL: https://arxiv.org/abs/2304.08069
- PDF: `docs/papers/rtdetr_beats_yolos_2304.08069.pdf`

## Problem

- What problem is the paper solving? Bring end-to-end DETR-style detection into the real-time regime and beat YOLO detectors in both speed and accuracy.
- What model family is studied? RT-DETR, compared against advanced YOLO detectors and DETR variants.
- Why this matters to the repo: It is the most direct real-time end-to-end DETR comparison point for understanding why a YOLO-family attack may fail when the target detector becomes one-to-one and NMS-free.

## Method

- Core idea: redesign DETR for real-time use by reducing encoder cost and improving query initialization (pp. 1-2, 4-5).
- Efficient hybrid encoder:
  - decouple **intra-scale interaction** and **cross-scale fusion**
  - perform attention-based intra-scale interaction mainly on high-level features
  - use CNN-based cross-scale fusion for efficiency
  - this becomes the AIFI + CCFF encoder design (pp. 4-5)
- Uncertainty-minimal query selection:
  - current DETR query selection overuses classification confidence
  - RT-DETR explicitly minimizes disagreement between classification and localization predictions when choosing initial queries (p. 5)
- Practical feature: flexible speed tuning by changing decoder depth without retraining (abstract, p. 1)

## Experimental Setup

- Dataset: COCO, with additional Objects365 pretraining for larger results
- Metrics: AP, AP50, AP75, APS, APM, APL, FPS
- Speed benchmark: end-to-end speed on T4 GPU with TensorRT FP16, including the practical effect of NMS for YOLO comparisons (pp. 3-4)

## Results

- Main headline from the abstract: RT-DETR-R50 / R101 reaches `53.1% / 54.3% AP` on COCO at `108 / 74 FPS` on T4 GPU, outperforming advanced YOLOs in both speed and accuracy (p. 1).
- DETR comparison: RT-DETR-R50 beats DINO-Deformable-DETR-R50 by **2.2 AP** and runs at roughly **21x** the FPS (`108` vs `5`) (pp. 1-2, 7).
- Objects365 pretraining boosts RT-DETR-R50 / R101 to `55.3% / 56.2% AP` (pp. 1-2).
- Table 2 results (p. 7):
  - RT-DETR-R50: `53.1 AP`, `108 FPS`
  - RT-DETR-R101: `54.3 AP`, `74 FPS`
  - YOLOv8-L: `52.9 AP`, `71 FPS`
  - YOLOv8-X: `53.9 AP`, `50 FPS`
- NMS analysis matters:
  - the paper explicitly shows that NMS thresholds change both runtime and accuracy for YOLO detectors
  - this is part of the motivation for a true end-to-end benchmark (pp. 3-4)

## Relevance to My Capstone

- Direct relevance to YOLOv8: Medium. It is the clearest paper showing where fast YOLO pipelines lose time and stability because of NMS.
- Direct relevance to YOLO11: Medium, as a nearby real-time baseline.
- Direct relevance to YOLO26: High. RT-DETR is the strongest real-time one-to-one detector reference in the current packet, so it is a good analogue if `YOLO26n` behaves more like an end-to-end query-based detector than a dense post-NMS YOLO. That analogy is my inference rather than a claim made in the paper.
- What I can cite: NMS has real speed and threshold-selection costs for YOLOs, and real-time one-to-one detectors can outperform YOLOs once the encoder and query initialization are redesigned properly.

## Open Questions

- Does `YOLO26n` use a query-selection or one-to-one decoding path that is functionally closer to RT-DETR than to YOLOv8?
- Would the repo attack improve if it targeted the subset of features or predictions that initialize the one-to-one decoder path?
- Is poor transfer into `YOLO26n` partly a result of attacking dense outputs while the model's final decisions are made through a different selected-query pathway?

## Normalized Extraction

- Canonical slug: `zhao2023_rtdetr_realtime_end_to_end`
- Canonical source record: `docs/papers/rtdetr_beats_yolos_2304.08069.pdf`
- Evidence state: `page_cited`
- Threat model: Not an adversarial paper; real-time end-to-end detector reference.
- Detector family and exact version: RT-DETR-R50 and RT-DETR-R101.
- Attack or defense goal: Build a real-time one-to-one detector that outperforms YOLO-class real-time detectors.
- Loss or objective: DETR-style end-to-end detection with an efficient hybrid encoder and uncertainty-minimal query selection.
- Transforms / EoT: None.
- Dataset: COCO and Objects365 pretraining.
- Metrics: AP, AP50, AP75, APS, APM, APL, FPS.
- Strongest quantitative result: RT-DETR-R50 / R101 reaches 53.1 / 54.3 AP at 108 / 74 FPS on T4 GPU, and pretraining lifts them to 55.3 / 56.2 AP (pp. 1, 7).
- Transfer findings: None directly, but the paper is a strong architecture analogue for one-to-one inference behavior.
- Physical findings: None.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Strong architecture reference for interpreting one-to-one real-time detection; highest value for YOLO26-style mismatch reasoning.
- Reproducible technique to borrow: Distinguish dense feature maps from the selected-query pathway when analyzing or attacking end-to-end real-time detectors.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
