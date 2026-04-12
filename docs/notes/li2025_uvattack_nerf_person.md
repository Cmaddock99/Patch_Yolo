# Paper Review: UV-Attack — NeRF-based UV Mapping for Person Detection Evasion

## Citation

- Title: UV-Attack: Physical-World Adversarial Attacks for Person Detection via Dynamic-NeRF-based UV Mapping
- Authors: Yanjie Li, Wenxuan Zhang, Kaisheng Liang, Bin Xiao
- Venue / Year: ICLR 2025
- DOI: 10.48550/arXiv.2501.05783
- arXiv: 2501.05783
- URL: https://arxiv.org/abs/2501.05783
- PDF: `docs/papers/li2025_uvattack_nerf_person_2501.05783.pdf`

## Problem

- What threat model is assumed? Physical adversary applying adversarial texture to clothing worn by a person; target is human motion with deformation
- What detector is attacked? YOLOv8 (explicitly stated in abstract), plus other person detectors
- What is the attack goal? Person vanishing — adversarial texture on clothing that remains effective across diverse human actions and viewpoints

## Method

- Patch type: Full-clothing adversarial texture (not a localized patch)
- Key technique: Dynamic-NeRF-based UV mapping — uses a neural radiance field to model human body deformation across actions, then maps the adversarial texture onto the 3D UV surface
- Optimization method: Gradient-based; patch trained in UV space and rendered to 2D via NeRF-based differentiable rendering
- Key advantage over prior work: Standard EoT and affine transforms can't model non-rigid cloth deformation; NeRF models the actual geometry of clothing across unseen actions by sampling from SMPL parameter space
- Physical-world considerations: Optimized for printing; tested in real physical settings

## Experimental Setup

- Dataset: Persons with diverse actions
- Target classes: Person (YOLOv8 specifically mentioned)
- Model versions: YOLOv8, other detectors
- Metrics: ASR across actions and viewpoints

## Results

- Main quantitative result: TODO — 8 citations, ICLR paper; read for full numbers
- What worked best: NeRF-based deformation modeling enables high ASR across unseen human actions — addresses the key failure mode of static patch approaches (degradation under cloth folding/motion)

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — paper explicitly targets YOLOv8; numbers directly comparable
- Direct relevance to YOLO11: Medium — likely tested but need to verify
- Direct relevance to YOLO26: Low — not likely tested; use as comparison
- What I can cite: State-of-the-art physical person evasion technique (2025, ICLR); YOLOv8 ASR as a benchmark number above your baseline
- What I can reproduce: NeRF-based rendering is complex; the attack itself is not easily replicated. Cite for context/comparison only.

## Open Questions

- What is the exact ASR on YOLOv8 (digital and physical)?
- Is code available?
- How does it compare to DAP and Xu T-shirt numbers?
- TODO: read full paper for quantitative results
