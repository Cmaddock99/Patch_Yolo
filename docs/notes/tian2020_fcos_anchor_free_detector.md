# Tian et al. (2020) — FCOS: A Simple and Strong Anchor-Free Object Detector

## Citation

- Title: *FCOS: A Simple and Strong Anchor-Free Object Detector*
- Authors: Zhi Tian, Chunhua Shen, Hao Chen, Tong He
- Venue / Year: IEEE TPAMI 2020
- DOI: 10.1109/TPAMI.2020.3032166
- arXiv: 2006.09214
- URL: https://arxiv.org/abs/2006.09214
- PDF: `docs/papers/fcos_anchor_free_object_detector_2006.09214.pdf`

## Problem

- What problem is the paper solving? Remove anchor boxes from one-stage detection while keeping the detector simple, fully convolutional, and strong.
- What model family is studied? FCOS, compared against RetinaNet, Faster R-CNN, YOLOv3, CenterNet, and related detectors.
- Why this matters to the repo: It is the cleanest control paper for separating **anchor-free design** from the later end-to-end one-to-one / Hungarian-matching changes.

## Method

- Core idea: predict a bounding box `(l, t, r, b)` at each foreground pixel directly, instead of regressing from predefined anchors (p. 1).
- Ambiguity handling: if a location falls in multiple boxes, FCOS assigns it to the smallest-area target; with FPN and center sampling, ambiguous positives fall below 3% of all positive samples (p. 6).
- Center-ness: add a parallel branch that predicts how close a location is to the center of the object, then multiply center-ness with the class score before NMS to suppress low-quality off-center boxes (p. 6).
- Key architectural point: FCOS is **anchor-free but not NMS-free**. It still uses NMS during inference (pp. 1, 6).

## Experimental Setup

- Dataset: COCO
- Metrics: AP, AP50, AP75, APS, APM, APL, best possible recall (BPR)
- Baselines: RetinaNet, Faster R-CNN, YOLOv3, CornerNet, CenterNet

## Results

- Recall sanity check: FCOS with FPN reaches `98.95%` BPR, very close to the best anchor-based RetinaNet setting at `99.32%`, so removing anchors does not destroy recall (p. 6, Table 1).
- Main COCO results (p. 10, Table 8):
  - FCOS with ResNet-101-FPN: `43.2 AP`
  - RetinaNet with ResNet-101-FPN: `39.1 AP`
  - Faster R-CNN with ResNet-101-FPN: `36.2 AP`
  - FCOS with deformable conv + BiFPN + test-time augmentation: `50.4 AP`
- Real-time variant: FCOS-RT reaches `40.3 AP` at `46 FPS`, and a shared-head variant still beats CenterNet at the same speed tier (p. 9).

## Relevance to My Capstone

- Direct relevance to YOLOv8: Medium. It helps explain anchor-free dense detection, which is closer to later YOLO heads than classic anchor-box formulations.
- Direct relevance to YOLO11: Medium for the same reason.
- Direct relevance to YOLO26: Medium as a control paper. FCOS shows that going anchor-free alone does **not** imply one-to-one prediction or NMS removal. That makes it a useful negative control for the repo's `YOLO26n` problem: if `YOLO26n` is unusually hard to attack, anchor-free design by itself is probably not the whole explanation. That last sentence is my inference from this paper plus the repo's results.
- What I can cite: anchor removal simplifies the dense detector, but final inference logic is still NMS-based, so anchor-free should not be conflated with end-to-end one-to-one detection.

## Open Questions

- Is `YOLO26n` closer to FCOS-style anchor-free dense detection or to a one-to-one end-to-end detector?
- If the repo attack already works on dense anchor-free models, does the failure on `YOLO26n` come from one-to-one matching rather than anchor removal?
- Would a detector-side analysis of selected final predictions clarify whether `YOLO26n` is still dense like FCOS or behaves more like RT-DETR / YOLOv10?

## Normalized Extraction

- Canonical slug: `tian2020_fcos_anchor_free_detector`
- Canonical source record: `docs/papers/fcos_anchor_free_object_detector_2006.09214.pdf`
- Evidence state: `page_cited`
- Threat model: Not an adversarial paper; anchor-free one-stage detector reference.
- Detector family and exact version: FCOS.
- Attack or defense goal: Remove anchor boxes while preserving strong dense object detection.
- Loss or objective: Per-pixel classification, regression, and center-ness prediction in an anchor-free one-stage detector.
- Transforms / EoT: None.
- Dataset: COCO.
- Metrics: AP, AP50, AP75, APS, APM, APL, BPR, FPS.
- Strongest quantitative result: FCOS with ResNet-101-FPN reaches 43.2 AP on COCO test-dev and strongly outperforms RetinaNet with the same backbone (p. 10); BPR remains 98.95% with FPN (p. 6).
- Transfer findings: None.
- Physical findings: None.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Useful as an anchor-free control; strongest value is ruling out anchor-free design as a sufficient explanation for the repo's hardest transfer case.
- Reproducible technique to borrow: Treat anchor-free dense detection as distinct from end-to-end one-to-one detection when building architectural explanations or attack losses.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
