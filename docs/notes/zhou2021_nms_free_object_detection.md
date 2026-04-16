# Zhou et al. (2021) — Object Detection Made Simpler by Eliminating Heuristic NMS

## Citation

- Title: *Object Detection Made Simpler by Eliminating Heuristic NMS*
- Authors: Qiang Zhou, Chaohui Yu, Chunhua Shen, Zhibin Wang, Hao Li
- Venue / Year: IEEE Transactions on Multimedia 2023 (arXiv 2021)
- DOI: 10.1109/TMM.2023.3248966
- arXiv: 2101.11782
- URL: https://arxiv.org/abs/2101.11782
- PDF: `docs/papers/nms_free_object_detection_2101.11782.pdf`

## Problem

- What problem is the paper solving? Remove heuristic NMS from a one-stage detector while keeping the detector fully convolutional and simple.
- What model family is studied? FCOS and ATSS-style one-stage detectors.
- Why this matters to the repo: It is a useful bridge paper between dense YOLO-style detectors and end-to-end one-to-one prediction, without requiring a full DETR architecture.

## Method

- Core idea: attach a compact **positive sample selector (PSS)** head to FCOS so the detector learns to choose one and only one positive sample per object instance (p. 1).
- Model change: the PSS head has only **two convolution layers** and is the only architectural modification to FCOS (p. 1).
- Training objective:
  - keep the original FCOS loss
  - add a PSS classification loss over one-to-one positives
  - optionally add a ranking loss for positive versus negative samples (pp. 3-4)
- Key optimization trick: use **stop-gradient** from the PSS branch into the main FCOS network so one-to-many and one-to-one labels do not fight each other during training (pp. 1, 6-7).
- Matching score: the one-to-one selector uses the multiplicative score `sigma(pss) * sigma(classification) * sigma(center-ness)` (p. 5).

## Experimental Setup

- Dataset: COCO
- Baselines: FCOS, ATSS, DeFCN
- Metrics: mAP, mAR, network forward time, post-processing time
- Training: 3x schedule, multi-scale augmentation, ResNet / ResNeXt / Res2Net backbones

## Results

- Table 1 (p. 4):
  - FCOSPSS with ResNet-50 reaches `42.3 mAP`, slightly above FCOS at `42.0`
  - ATSSPSS with ResNet-50 reaches `42.6 mAP`, close to ATSS at `42.8`
  - ATSSPSS reaches `48.5 mAP` with R2N-101-DCN
  - Both NMS-free variants outperform DeFCN's `41.5 mAP`
- Stop-gradient is important (pp. 6-7):
  - FCOSPSS improves from `41.5` to `42.3 mAP`
  - ATSSPSS improves from `41.6` to `42.6 mAP`
  - end-to-end training beats two-step training for ATSSPSS (`42.6` vs `42.3`)
- Small design choices matter:
  - two conv layers for the PSS head work best (p. 9, Table 5)
  - ranking loss adds about `0.2-0.3 mAP` (p. 9, Table 9)

## Relevance to My Capstone

- Direct relevance to YOLOv8: Medium. This is a one-stage dense detector paper and is a better conceptual neighbour to YOLO than DETR is.
- Direct relevance to YOLO11: Medium for the same reason.
- Direct relevance to YOLO26: Medium to high as a training and inference-logic reference. It shows that once final prediction is driven by one-to-one selected positives, optimization conflicts appear unless the selector pathway is handled carefully. The exact link to `YOLO26n` is my inference, not a claim from the paper.
- What I can cite: NMS-free one-stage detection can be built by layering a one-to-one selector on top of a dense detector, and stop-gradient is a practical way to handle the one-to-many / one-to-one conflict.

## Open Questions

- Does the repo's `YOLO26n` have an internal selector or one-to-one ranking mechanism analogous to PSS?
- Would an attack objective that explicitly targets the selected positive prediction outperform a dense-score-only attack loss?
- Is there an attack-side analogue to the paper's stop-gradient trick when optimizing through mixed one-to-many and one-to-one branches?

## Normalized Extraction

- Canonical slug: `zhou2021_nms_free_object_detection`
- Canonical source record: `docs/papers/nms_free_object_detection_2101.11782.pdf`
- Evidence state: `page_cited`
- Threat model: Not an adversarial paper; NMS-free one-stage detector reference.
- Detector family and exact version: FCOS, ATSSPSS, FCOSPSS.
- Attack or defense goal: Show that one-stage detectors can remove heuristic NMS by learning a positive-sample selector.
- Loss or objective: FCOS loss plus PSS classification loss, with optional ranking loss and stop-gradient between the selector and the base detector.
- Transforms / EoT: None.
- Dataset: COCO.
- Metrics: mAP, mAR, network forward time, post-processing time.
- Strongest quantitative result: FCOSPSS reaches 42.3 mAP and ATSSPSS reaches 42.6 mAP on COCO while remaining NMS-free; ATSSPSS scales to 48.5 mAP with R2N-101-DCN (pp. 4, 9).
- Transfer findings: None directly.
- Physical findings: None.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Useful one-stage analogue for end-to-end prediction logic; strongest as a conceptual bridge into newer one-to-one detector behavior.
- Reproducible technique to borrow: Target the selected positive prediction explicitly and treat one-to-many versus one-to-one supervision as a real optimization conflict rather than a bookkeeping detail.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `method_to_borrow`
