# Paper Review: DePatch — Decoupled Adversarial Patch for Person Detectors

## Citation

- Title: DePatch: Towards Robust Adversarial Patch for Evading Person Detectors in the Real World
- Authors: Jikang Cheng, Ying Zhang, Zhongyuan Wang, Zou Qin, Chen Li
- Venue / Year: arXiv, 2024
- arXiv: 2408.06625
- URL: https://arxiv.org/abs/2408.06625
- PDF: `docs/papers/cheng2024_depatch_person_detector_2408.06625.pdf`

## Problem

- What threat model is assumed? Physical adversary deploying a printed patch on or near a person
- What detector is attacked? Person detectors (YOLO-family)
- What is the attack goal? Person vanishing — patch robust to real-world physical transformations

## Method

- Patch type: Block-wise segmented adversarial patch
- Key insight: "Self-coupling issue" — in standard patches, degradation to any small segment from physical transforms (print quality, viewing angle, lighting) causes complete adversarial failure because all segments are jointly optimized
- Optimization method: Divide patch into block-wise segments; randomly erase segments during training to reduce inter-dependency between blocks; each block learns to be independently adversarial
- Physical-world considerations: Specifically designed to address print-and-wear degradation; more robust to partial occlusion and deformation than monolithic patches

## Experimental Setup

- Dataset: Person detection datasets
- Target classes: Person
- Model versions: YOLO-family person detectors
- Metrics: ASR (digital and physical), robustness to transforms

## Results

- Main quantitative result: TODO — 4 citations, read full paper for numbers
- What worked best: Block-wise decoupling significantly improves physical robustness vs. standard gradient patches

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — decoupled training is a drop-in improvement to any YOLO patch optimization loop
- Direct relevance to YOLO11: High — same principle applies
- Direct relevance to YOLO26: Medium — the decoupling trick is architecture-agnostic; cite as physical robustness improvement technique
- What I can cite: Physical robustness improvement technique; 2024 paper filling gap between EoT and DAP's Creases Transform
- What I can reproduce: Block-wise random erasing during training is simple to implement — potential improvement for your v2 runs

## Open Questions

- Exact ASR improvement vs. baseline?
- Is code available?
- How does it compare to DAP's Creases Transform for physical robustness?
