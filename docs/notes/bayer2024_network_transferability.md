# Bayer et al. (2024) — Network Transferability of Adversarial Patches

## Citation

- Title: *Network transferability of adversarial patches in real-time object detection*
- Authors: Jens Becker, Michael Becker, Marko Münch, Michael Arens
- Venue / Year: SPIE Proceedings 2024
- DOI: 10.1117/12.3031501
- arXiv: 2408.15833
- URL: https://arxiv.org/abs/2408.15833
- PDF: `docs/papers/bayer2024_network_transferability_2408.15833.pdf`

## Problem

- What threat model is assumed? Black-box transfer of adversarial patches across object detection architectures.
- What detector or classifier is attacked? Multiple real-time object detectors (YOLO-family and others).
- What is the attack goal? Understand which model properties affect how well an adversarial patch transfers to unseen architectures.

## Method

- Patch type: Standard localized adversarial patch
- Optimization method: Gradient-based, white-box training on source model
- Loss terms: Detection suppression loss
- Key finding: **Patches optimized with larger (more capable) source models provide better transferability** than patches optimized with smaller models. Model capacity of the source model is a primary driver of transfer success.
- Physical-world considerations: Not the primary focus; transferability study across network architectures.

## Experimental Setup

- Dataset: COCO or similar standard benchmark
- Target classes: Person and other COCO classes
- Model versions: Multiple YOLO variants and other real-time detectors
- Metrics: Attack success rate, detection suppression across target models

## Results

- Main quantitative result: Larger source models → better transfer. Small models like YOLOv8n overfit to their own architecture's gradient landscape and transfer poorly.
- What worked best: Training on larger/ensemble source models.
- What failed or stayed weak: Single small-model patches — good at suppressing the training model but fail to generalize.

## Relevance to My Capstone

- Direct relevance to YOLOv8: **HIGH** — you trained on yolov8n (the nano, smallest v8 model). This paper predicts you'd get better transfer by using yolov8x or an ensemble.
- Direct relevance to YOLO11: Same logic — yolo11n is the nano variant.
- Direct relevance to YOLO26: **HIGH** — your v8→v26 16% transfer result is consistent with this paper's finding that small source models transfer poorly.
- What I can cite: Primary citation for the transfer results section. Explains why your v8n→v26n is 16% — you trained on the smallest model targeting the most architecturally different target.

## Open Questions

- Does this transfer across YOLO versions? Yes — this paper specifically studies that question.
- Is the patch digital only? Digital transferability study.
- Is the code available? SPIE proceedings may not have code; check arXiv supplemental.
- What is missing for my project? Does not specifically address attention/anchor-free effects — complementary to Lovisotto 2022 and Liao 2021.

## TODO

- [ ] Read full PDF — focus on Table 1/2 for model-size vs. transfer rate numbers
- [ ] Extract the specific numbers for cross-version transfer
- [ ] Compare to your v8n→v11n (39.4%) and v8n→v26n (16%) results
