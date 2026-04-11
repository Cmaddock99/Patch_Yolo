# Xu et al. (2020) — Adversarial T-shirt

## Citation

- Title: *Adversarial T-shirt! Evading Person Detectors in A Physical World*
- Authors: Kaidi Xu, Gaoyuan Zhang, Sijia Liu, Quanfu Fan, Mengshu Sun, Hongge Chen, Pin-Yu Chen, Yanzhi Wang, Xue Lin
- Venue / Year: ECCV 2020
- arXiv: 1910.11099
- URL: https://arxiv.org/abs/1910.11099
- PDF: `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf`
- Cited by: 520+

## Problem

- What threat model is assumed? Physical-world adversarial patch printed on a T-shirt worn by a person. White-box optimization, black-box physical-world test.
- What detector or classifier is attacked? YOLOv2, Faster R-CNN
- What is the attack goal? Evade person detection in a physical environment where the patch deforms with body movement and cloth wrinkles.

## Method

- Patch type: Printable patch affixed to a T-shirt (deformable surface)
- Optimization method: TPS (Thin-Plate Spline) transformation to simulate cloth deformation during optimization
- Loss terms: Detection confidence suppression + TPS warp transforms
- Transformations / EoT details: TPS warping to model non-rigid cloth deformation — goes beyond rigid EoT (random rotation/scale). This is the key technical innovation.
- Physical-world considerations: Printed on real T-shirts, tested with humans walking in various conditions.

## Experimental Setup

- Dataset: Custom person photos, physical-world video
- Target classes: Person
- Model versions: YOLOv2, Faster R-CNN
- Metrics: Attack Success Rate (ASR) digital and physical

## Results

- Main quantitative result: **74% ASR digital, 57% ASR physical** against YOLOv2.
- Previous SOTA achieved only 18% physical — Xu et al. improved it 3×.
- What worked best: TPS warp modeling of cloth deformation during training.
- What failed or stayed weak: At angles >45° and in very bright lighting, effectiveness dropped.

## Relevance to My Capstone

- Direct relevance to YOLOv8: **HIGH** — your 85% digital on v8 is stronger than this 2020 baseline. Important benchmark context.
- Direct relevance to YOLO11: Similar comparison point — your 78.8% v11 exceeds this baseline.
- Direct relevance to YOLO26: After the loss fix, your v26 result will need to be compared here.
- What I can cite: **Primary physical-world baseline benchmark**. Your 85% digital result beats the 74% digital from 2020 — shows progress. The 57% physical is the baseline to beat for any physical deployment claim.
- What I can reproduce: TPS warp is complex but the idea of cloth-deformation-aware EoT is the key technique in DAP (Guesmi 2024) as well.

## Open Questions

- Does this transfer across YOLO versions? Paper tested on YOLOv2 and FRCNN — limited transfer study.
- Is the patch digital only? **No — physical T-shirt test is the main contribution.**
- Is the code available? Check arXiv supplemental / GitHub.
- What is missing for my project? Newer YOLO versions (v8/v11/v26) not tested; your project extends this.

## TODO

- [ ] Read to get the exact digital/physical ASR numbers table
- [ ] Note the TPS warp parameters — relevant if adding cloth-deformation EoT to your pipeline
- [ ] Use as the primary physical-world comparison number in the capstone
