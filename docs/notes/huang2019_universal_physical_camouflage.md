# Huang et al. (2019) — Universal Physical Camouflage Attacks on Object Detectors

## Citation

- Title: *Universal Physical Camouflage Attacks on Object Detectors*
- Authors: Lifeng Huang, Chengying Gao, Yuyin Zhou, Cihang Xie, Alan Yuille, Changqing Zou, Ning Liu
- Venue / Year: arXiv 1909.04326 (April 2020 update); CVPR 2020 accepted
- URL: https://arxiv.org/abs/1909.04326
- Code: https://mesunhlf.github.io/index_physical.html
- Access: Open access preprint; code released

## Triage Summary (from PDF pages 1–5)

### Problem

Universal Physical Camouflage (UPC) attacks object detectors to hide **all instances of a target category** simultaneously (universal across persons of different sizes, poses, lighting). This is contrasted with instance-specific attacks (earlier work) and single-model attacks. The attack targets faster-rcnn (VGG16, ResNet50) — **not YOLO directly** in the primary experiments, though the paper frames itself as a universal detector attack.

### Method Overview

UPC constructs a universal adversarial pattern through three steps:
1. **RPN Attack** (L_rpn): Fool the Region Proposal Network to generate low-quality proposals — reduces the number of high-confidence candidate bounding boxes reaching the classifier head.
2. **Classifier and Regressor Attack** (L_cls + L_reg): Mislead classification and corrupt bounding box predictions simultaneously.
3. **Physical Simulation** (L_tv + semantic constraint): Enforces the pattern to be visually natural (semantic constraint via projection onto natural image manifold) and physically plausible (deformation transforms T_r, T_c simulating cloth bending, viewpoint, lighting).

The semantic constraint enforces that the generated patterns look similar to natural images during optimization — making them appear as camouflage patterns on clothing or accessories rather than psychedelic noise. This is a key distinction from non-naturalistic patches.

Two attack modes:
- **Untargeted attack**: maximize detection failure for person class
- **Targeted attack**: maximize probability of outputting a specific wrong class

### Experimental Setup

- **Dataset**: 200 human images collected with varied body attributes (body size, posture, etc.) — called the training set X; also evaluated on AttackScenes (first standardized virtual benchmark database with 20 virtual scenes — 10 indoor, 10 outdoor, 18 cameras per scene, 3 illumination levels)
- **Detectors evaluated**: Faster R-CNN (VGG16-07, VGG16-0712, RES101-07, RES101-0712) — primary evaluation. Not directly YOLOv3/v5/v8.
- **Metric**: p_{0.5} — probability the detector correctly identifies the attacked instance above NMS threshold 0.3 and confidence 0.5
- **Comparison**: vs. DPatch (Liu et al.), Accessorize to a Crime (Sharif et al.), Chen et al. physical attack

### Key Results (from Table 1 caption and experimental section visible in pages 1–5)

- UPC achieves single-digit mAP values on attacked instances across multiple Faster R-CNN variants
- Comparison shown: Ours (Cnt=0.001): mAP=0.28, Smallest AP (Aeroplane)=0, Largest AP (Sports Ball)=2.2 [Table 1 rows visible] — substantially outperforms DPatch which stays at ~9 mAP
- **Physical attack demonstrated**: Pattern printed as garment texture; evaluated under varied viewpoints in AttackScenes and physical scenes. Physical attack performance is qualitatively shown (persons missed by detector when wearing UPC garment)
- UPC achieves stronger attacks by targeting both RPN and classification+regression heads jointly — DPatch (which targets classification only) is substantially weaker

### Limitations

- Primary evaluation is on Faster R-CNN only — YOLO not directly tested in the main experiments
- AttackScenes is virtual/simulated — physical world evaluation is qualitative only
- Semantic constraint may not transfer well to non-naturalistic patch types (aggressive texture patches may be stronger)

## Relevance to Capstone

- **YOLOv8**: Indirect — UPC is a Faster R-CNN paper, but the semantic constraint (naturalistic appearance) and deformation transforms (T_r, T_c) are directly portable to any YOLO training loop
- **YOLO11**: Indirect — same
- **YOLO26**: Indirect — same; however, UPC's RPN attack is specific to two-stage detectors; YOLO26 uses end-to-end matching, so only the C&R (classifier + regressor) component is transferable
- **What to cite**: As the first standardized virtual benchmark (AttackScenes) for physical adversarial patch evaluation; for the joint RPN + C&R attack design; for the semantic constraint approach to natural-looking patches
- **What to reproduce**: The deformation transforms T_r (external/viewpoint) and T_c (internal/cloth deformation) as enhancements to the repo's EoT pipeline

## Evidence Confidence

Medium — PDF read (5 pages, abstract through experimental setup intro); exact per-YOLO numbers not available since YOLO is not the primary evaluated model.

## Open Questions

- Do the authors test YOLO in supplementary or later sections? The paper evaluates Faster R-CNN; YOLO mention in intro as a detector class but not the primary victim.
- Does the code (mesunhlf.github.io) include YOLO integration?
- What is the physical ASR on real humans (not AttackScenes virtual)?
