# Huang et al. (2025) — AdvReal: Physical Adversarial Patch Framework

## Citation

- Title: *AdvReal: Physical adversarial patch generation framework for security evaluation of object detection systems*
- Authors: Huang, Ren, Wang, Huo, Bai, Zhang, Yu
- Venue / Year: Expert Systems with Applications, Vol.296, Article 128967 (2025/2026)
- DOI: 10.1016/j.eswa.2025.128967
- arXiv: 2505.16402
- URL: https://arxiv.org/abs/2505.16402
- PDF: `docs/papers/huang2025_advreal_physical_2505.16402.pdf`
- Access: arXiv preprint open; full version via ScienceDirect / CSUSM

## Problem

- What threat model is assumed? Physical-world adversarial patch attack; white-box optimization, physical-world test.
- What detector or classifier is attacked? YOLOv12 (primary); comparison against other YOLO versions.
- What is the attack goal? Person/object detection evasion in physical environments.

## Method

- Patch type: Printable adversarial patch
- Optimization method: Physical-aware gradient optimization
- Loss terms: Detection suppression + physical robustness terms
- Transformations / EoT details: Physical-world transformations including distance variation, angle variation, and lighting changes
- Physical-world considerations: Tested at multiple distances (up to 4m), multiple viewing angles (frontal and oblique)

## Experimental Setup

- Dataset: Custom physical capture dataset
- Target classes: Person
- Model versions: YOLOv12, comparison against T-SEA, AdvTexture
- Metrics: Attack Success Rate (ASR) physical

## Results

- Main quantitative result: **70.13% ASR on YOLOv12 in physical scenarios**
- Average ASR >90% under frontal/oblique views at 4m distance
- Outperforms T-SEA: 21.65% ASR physical
- Outperforms AdvTexture: 19.70% ASR physical
- What worked best: Physical-aware optimization with multi-angle, multi-distance EoT.
- What failed or stayed weak: T-SEA and AdvTexture underperform significantly in physical conditions despite being strong digitally.

## Relevance to My Capstone

- Direct relevance to YOLOv8: **HIGH** — provides the most current physical-world benchmark. Your 85% digital v8 result should be contextualized against AdvReal's 70% physical on YOLOv12.
- Direct relevance to YOLO11: Comparison point.
- Direct relevance to YOLO26: Indirect — YOLOv12 is more recent than v26, so AdvReal's numbers frame where the field is.
- What I can cite: **Most recent physical benchmark paper (2025).** Use this as your "current state of physical attacks" citation. The 70% physical ASR is the number to reference when discussing physical deployment feasibility.

## Open Questions

- Does this transfer across YOLO versions? Paper focuses on YOLOv12 primarily.
- Is the patch digital only? **No — physical test is the main contribution.**
- Is the code available? Check arXiv supplemental / journal appendix.
- How does AdvReal's framework differ from your approach at the code level?

## TODO

- [ ] Read Section 3 for the physical-aware loss formulation
- [ ] Extract the comparison table (T-SEA vs AdvTexture vs AdvReal) for the capstone write-up
- [ ] Check if the physical testing protocol (distance, angle, lighting) could be replicated
- [ ] Use 70% physical figure as the current state-of-art benchmark in capstone context section
