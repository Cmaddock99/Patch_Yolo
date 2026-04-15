# Alam et al. (2023) — Attention Deficit is Ordered!

## Citation

- Title: *Attention Deficit is Ordered! Fooling Deformable Vision Transformers with Collaborative Adversarial Patches*
- Authors: Mobarakol Islam Alam, Ben Tarchoun, Ihsen Alouani, Nael Abu-Ghazaleh
- Venue / Year: arXiv 2311.12914 (2023)
- URL: https://arxiv.org/abs/2311.12914
- PDF: `docs/papers/alam2023_attention_deficit_2311.12914.pdf`

## Problem

- What threat model is assumed? White-box adversarial patch attack against deformable vision transformers (e.g., Deformable DETR).
- What detector or classifier is attacked? Deformable DETR and related attention-based object detectors.
- What is the attack goal? Achieve complete detection suppression against attention-based detectors that are resistant to standard patch attacks.

## Method

- Patch type: Collaborative adversarial patches — multiple patches placed strategically to manipulate attention weights
- Optimization method: Gradient-based optimization targeting attention maps
- Loss terms: Attention manipulation loss + detection suppression loss
- Key finding: Standard adversarial patches **do not transfer to deformable transformers**. The attack must explicitly manipulate attention to point toward adversarial noise rather than the target object.
- Transformations / EoT details: Not the primary focus — architecture-specific approach
- Physical-world considerations: Primarily digital; the <1% image area result suggests very small patches are sufficient

## Experimental Setup

- Dataset: COCO
- Target classes: Multiple object classes
- Model versions: Deformable DETR, related architectures
- Metrics: Average Precision (AP)

## Results

- Main quantitative result: Achieved **complete 0% AP** by altering less than 1% of the image area.
- What worked best: Collaborative patches that explicitly redirect attention weights toward adversarial noise rather than the target object.
- What failed or stayed weak: Standard single adversarial patch approaches — attention in deformable transformers routes around naive patches.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Low — v8 does not use deformable attention.
- Direct relevance to YOLO11: Low.
- Direct relevance to YOLO26: **CRITICAL** — YOLO26 incorporates deformable attention-style mechanisms in its end-to-end head. This paper explains EXACTLY why your v1 YOLO26 result was poor even after fixing the loss path: the gradient landscape through deformable attention requires a fundamentally different optimization strategy than the standard top-k person score minimization used for v8/v11.
- What I can cite: Primary citation for "why YOLO26 resists standard patches." The 0% AP result shows that when done correctly, attention-based detectors can be attacked MORE effectively — but only with architecture-specific methods.

## Open Questions

- Does this transfer across YOLO versions? This paper is the reason it doesn't from v8→v26.
- Is the patch digital only? Yes, primarily digital analysis.
- Is the code available? Check arXiv supplemental / author GitHub.
- What is missing for my project? Adaptation from DETR to YOLO26's specific attention implementation.

## TODO

- [ ] Read Section 3 (collaborative patch optimization) for the specific loss formulation
- [ ] Check if the attention manipulation loss can be adapted to `preds["one2many"]` in YOLO26
- [ ] Compare with Lovisotto 2022 — both explain attention vulnerability but from different angles

## Normalized Extraction

- Canonical slug: `alam2023_attention_deficit`
- Canonical source record: `docs/papers/alam2023_attention_deficit_2311.12914.pdf`
- Evidence state: `page_cited`
- Threat model: White-box adversarial patch attack against deformable vision transformers, including collaborative multi-patch attacks.
- Detector family and exact version: Deformable DETR and MVDeTr.
- Attack or defense goal: Manipulate sparse deformable attention pointers and attention scores so that a small patch can collapse detector performance.
- Loss or objective: Pointer loss plus attention loss, optionally combined with model loss; collaborative patch attack separates source and target patches.
- Transforms / EoT: Small fixed patch areas; physical deployment is discussed conceptually for some attack variants but not benchmarked as a physical study.
- Dataset: MS COCO and Wildtrack.
- Metrics: AP for single-view detection and MODA for multi-view detection.
- Strongest quantitative result: Altering less than 1% of the image area drops Deformable DETR to 0% AP on COCO and MVDeTr to 0% MODA on Wildtrack (abstract, p. 1).
- Transfer findings: Dense-attention attacks do not transfer cleanly to deformable attention; pointer-specific losses are required.
- Physical findings: The paper notes that some attacks could be realized with printed shirts plus static props, but the evaluation remains digital.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: High only for YOLO26-style attention reasoning; low for YOLOv8 and YOLO11.
- Reproducible technique to borrow: Split the attack objective into pointer-routing and downstream detector-loss components when targeting sparse attention heads.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
