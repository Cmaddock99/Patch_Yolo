# Paper Review: FRAN — Frequency Attention Module for Adversarial Patches Against Person Detectors

## Citation

- Title: Using Frequency Attention to Make Adversarial Patch Powerful Against Person Detector
- Authors: Chang Lu, Linjun Lu, Xiang Cai, Xiaochun Lei, Zetao Jiang
- Venue / Year: IEEE Access, 2022
- DOI: 10.1109/ACCESS.2022.3215762
- arXiv: 2205.04638
- URL: https://ieeexplore.ieee.org/document/9923929
- PDF: `docs/papers/lu2022_fran_frequency_attention_2205.04638.pdf`

## Problem

- What threat model is assumed? Digital and physical adversary; patch worn on or near the target person
- What detector is attacked? Person detectors (YOLOv2, YOLOv3, YOLOv4)
- What is the attack goal? Person vanishing — increase effectiveness of small/medium patches that lose effectiveness when scaled down

## Method

- Patch type: Gradient-based adversarial patch with frequency domain guidance
- Key insight: When a patch is physically small (or resized), it undergoes shrinking — high-frequency components are lost. Standard gradient patches optimize features that are destroyed at smaller scales.
- FRAN module: Frequency-domain attention module that guides patch optimization to rely on low-frequency signals, which survive the shrinking process better than high-frequency perturbations
- First paper to introduce frequency domain attention into adversarial patch optimization

## Experimental Setup

- Dataset: COCO / person detection datasets
- Target classes: Person
- Model versions: YOLOv2, YOLOv3, YOLOv4
- Metrics: ASR, AP drop at various patch scales

## Results

- Main quantitative result: TODO — 9 citations; read full paper for numbers
- Key finding: FRAN patches remain effective at small patch sizes where standard patches fail
- What worked best: Low-frequency guidance for small-target scenarios

## Relevance to My Capstone

- Direct relevance to YOLOv8: Medium — frequency guidance concept is architecture-agnostic; small patch effectiveness is relevant to real-world deployment
- Direct relevance to YOLO11: Medium — same principle
- Direct relevance to YOLO26: Medium — no architecture-specific dependence
- What I can cite: Frequency-domain loss as a third patch optimization paradigm alongside spatial gradient (standard) and naturalism constraints (GAN/entropy/diffusion)
- Open access PDF available (IEEE Access + arXiv)

## Open Questions

- Quantitative improvement vs. baseline at small patch sizes?
- Is code available?
- Does it apply to anchor-free detectors?
