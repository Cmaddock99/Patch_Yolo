# Ji et al. (2021) — Adversarial YOLO Defense

## Citation

- Title: *Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches*
- Authors: Ji, Feng, Xie, Xiang, Liu
- Venue / Year: arXiv 2103.08860 (2021)
- URL: https://arxiv.org/abs/2103.08860
- PDF: `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf`

## Problem

- What threat model is assumed? Defense against adversarial patch attacks on human detection.
- What detector or classifier is attacked? YOLOv2-based person detector.
- What is the attack goal? Detect adversarial patches explicitly and recover person detection performance with minimal clean-data degradation.

## Method

- Patch type: Defense-side "patch" class added to YOLO
- Optimization method: Adversarial training on a constructed Inria-Patch dataset
- Loss terms: Standard YOLOv2 loss plus an added conditional patch-class loss
- Transformations / EoT details: Patch diversity introduced during adversarial training
- Physical-world considerations: Includes physical-world attack evaluation in addition to digital tests

## Experimental Setup

- Dataset: Pascal VOC 2007/2012, INRIA, Inria-Patch
- Target classes: Person and patch
- Model versions: YOLOv2 baseline vs. Ad-YOLO
- Metrics: mAP on VOC, AP on INRIA / Inria-Patch, white-box and physical-world evaluations

## Results

- Main quantitative result: Ad-YOLO reduces VOC 2007 mAP by only 0.70% (73.07% -> 72.35%) while achieving 80.31% AP for persons under white-box patch attacks.
- What worked best: Adding an explicit patch class and training on diverse generated patches
- What failed or stayed weak: Patch overlap can still cause missed patch detections in some scenarios

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — useful defense baseline if the write-up includes countermeasures
- Direct relevance to YOLO11: Moderate
- Direct relevance to YOLO26: Moderate — conceptually portable, though not validated on end-to-end detectors
- What I can reproduce: Add a patch class or detector-side patch head as a defense experiment
- What I can cite: Strong defense benchmark showing patch detection can work with limited clean-performance loss

## Open Questions

- Does this transfer across YOLO versions? Not shown directly
- Is the patch digital only, or physically tested? Both digital and physical evaluations are included
- Is the code available? TODO
- What is missing for my project? Modern YOLOv8/11/26 replication

## TODO

- [ ] Extract the physical-world comparison numbers versus vanilla YOLOv2
- [ ] Check whether the patch-class idea can be adapted to Ultralytics detectors
- [ ] Use 80.31% AP and 0.70% mAP-drop figures in the defenses section
