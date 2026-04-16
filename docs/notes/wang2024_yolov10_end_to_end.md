# Wang et al. (2024) — YOLOv10: Real-Time End-to-End Object Detection

## Citation

- Title: *YOLOv10: Real-Time End-to-End Object Detection*
- Authors: Ao Wang, Hui Chen, Lihao Liu, Kai Chen, Zijia Lin, Jungong Han, Guiguang Ding
- Venue / Year: NeurIPS 2024
- DOI: 10.48550/arXiv.2405.14458
- arXiv: 2405.14458
- URL: https://arxiv.org/abs/2405.14458
- PDF: `docs/papers/yolov10_end_to_end_detection_2405.14458.pdf`

## Problem

- What problem is the paper solving? Push YOLO into true end-to-end detection by removing NMS without giving up the latency advantages of CNN-style real-time detectors.
- What model family is studied? YOLOv10 N / S / M / B / L / X.
- Why this matters to the repo: It is the clearest paper in the current queue explaining how a YOLO-family detector changes once inference is driven by one-to-one predictions instead of dense one-to-many outputs plus NMS.

## Method

- Core idea: train YOLO with **dual label assignments** so the model gets rich one-to-many supervision during training but uses a one-to-one prediction head during inference (pp. 3-4).
- Key mechanism: introduce a second one-to-one head with the same structure as the one-to-many head, then discard the one-to-many head at inference (p. 4).
- Matching rule: use a **consistent matching metric** so the one-to-one head ranks samples in a way that stays aligned with the one-to-many branch; the paper sets `alpha_o2o = alpha_o2m` and `beta_o2o = beta_o2m` by default (pp. 4-5).
- Architecture changes beyond NMS removal:
  - lightweight classification head
  - spatial-channel decoupled downsampling
  - rank-guided block design
  - large-kernel depthwise convolutions on small models
  - partial self-attention (PSA) to add global modeling at low cost (pp. 2, 6, 8-9)

## Experimental Setup

- Dataset: COCO
- Baseline family: YOLOv8
- Comparison set: YOLOv6, YOLOv8, YOLOv9, Gold-YOLO, RT-DETR
- Metrics: AP, parameter count, FLOPs, end-to-end latency, forward-only latency
- Latency measurement: TensorRT FP16 on T4 GPU using official pretrained models (p. 7)

## Results

- Main headline: YOLOv10-S is **1.8x faster than RT-DETR-R18** at similar AP, and YOLOv10-B reaches the same AP as YOLOv9-C with **46% lower latency** (pp. 2-3, 7).
- Table 1 results (p. 7):
  - YOLOv10-S: `46.3 AP`, `2.49 ms`
  - RT-DETR-R18: `46.5 AP`, `4.58 ms`
  - YOLOv10-B: `52.5 AP`, `5.74 ms`
  - YOLOv9-C: `52.5 AP`, `10.57 ms`
  - YOLOv10-L / X exceed YOLOv8-L / X by `0.3 AP` / `0.5 AP` with far fewer parameters
- Ablation study (p. 8):
  - Moving YOLOv10-S from the YOLOv8-style baseline to NMS-free dual assignments cuts latency from `7.07 ms` to `2.44 ms` while AP moves from `44.9` to `44.3`
  - Adding the efficiency-driven design keeps latency low and adding the accuracy-driven design raises YOLOv10-S to `46.3 AP`
- Limitation the paper admits: NMS-free one-to-one training still trails original one-to-many training on smaller models; the appendix notes a gap of `1.0 AP` on YOLOv10-N and `0.5 AP` on YOLOv10-S (pp. 8, 21)

## Relevance to My Capstone

- Direct relevance to YOLOv8: Medium. It uses YOLOv8 as the architectural baseline and shows what changes when a dense YOLO detector becomes end-to-end and one-to-one.
- Direct relevance to YOLO11: Medium. It does not evaluate YOLO11, but it clarifies the design direction of newer YOLO-family real-time detectors.
- Direct relevance to YOLO26: High as an architecture reference. If the repo's `YOLO26n` behaves like an end-to-end one-to-one YOLO head, then the attack objective likely needs to care about the selected one-to-one predictions rather than only dense pre-NMS style outputs. That last sentence is my inference from the paper plus the repo results.
- What I can cite: the architectural shift from one-to-many + NMS toward one-to-one end-to-end YOLO inference, and the fact that this shift changes the supervision and matching regime materially.

## Open Questions

- Does `YOLO26n` use a dual-assignment regime that is closer to YOLOv10 or closer to DETR-style Hungarian matching?
- Is the repo's current attack loss suppressing the branch that actually determines one-to-one final predictions?
- Would a hybrid attack objective over both dense supervision and selected predictions improve transfer into `YOLO26n`?

## Normalized Extraction

- Canonical slug: `wang2024_yolov10_end_to_end`
- Canonical source record: `docs/papers/yolov10_end_to_end_detection_2405.14458.pdf`
- Evidence state: `page_cited`
- Threat model: Not an adversarial paper; architecture reference for end-to-end YOLO detection.
- Detector family and exact version: YOLOv10 N / S / M / B / L / X.
- Attack or defense goal: Explain how YOLO-family detectors can remove NMS and infer from one-to-one predictions.
- Loss or objective: Dual label assignments with a consistent matching metric across one-to-many and one-to-one heads.
- Transforms / EoT: None.
- Dataset: COCO.
- Metrics: AP, parameters, FLOPs, end-to-end latency, forward-only latency.
- Strongest quantitative result: YOLOv10-S is 1.8x faster than RT-DETR-R18 at similar AP, and YOLOv10-B matches YOLOv9-C with 46% lower latency (pp. 2-3, 7).
- Transfer findings: None directly; the paper is architecture and training focused.
- Physical findings: None.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Best direct architecture reference for reasoning about one-to-one YOLO behavior; strongest for YOLO26-style mismatch questions.
- Reproducible technique to borrow: Evaluate or optimize against both one-to-many supervision signals and one-to-one selected predictions instead of assuming dense pre-NMS outputs are the whole inference story.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
