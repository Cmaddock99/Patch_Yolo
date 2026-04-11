# Zhou et al. (2023) — MVPatch

## Citation

- Title: *MVPatch: More Vivid Patch for Adversarial Camouflaged Attacks on Object Detectors in the Physical World*
- Authors: Zhou, Zhao, Liu, Zhang et al.
- Venue / Year: arXiv 2312.17431 (2023/2024)
- URL: https://arxiv.org/abs/2312.17431
- PDF: `docs/papers/zhou2023_mvpatch_2312.17431.pdf`

## Problem

- What threat model is assumed? Transferable and stealthy adversarial patch attack against object detectors in digital and physical settings.
- What detector or classifier is attacked? Multiple YOLO-family detectors plus transfer targets such as Faster R-CNN, SSD, and YOLOv5.
- What is the attack goal? Improve transferability, stealthiness, and practicality at the same time instead of optimizing only one of them.

## Method

- Patch type: Camouflaged adversarial patch
- Optimization method: Dual-Perception Framework
- Loss terms: Transferability-oriented ensemble objective plus stealth / naturalness regularization
- Transformations / EoT details: Uses an ensemble-based Model-Perception-Based Module (MPBM) and a Human-Perception-Based Module (HPBM); includes printer / physical robustness considerations
- Physical-world considerations: Designed explicitly for physical deployment, not just digital evaluation

## Experimental Setup

- Dataset: Multiple object-detection benchmarks
- Target classes: Multiple
- Model versions: YOLOv2, YOLOv3, YOLOv3-tiny, YOLOv4, YOLOv4-tiny; transfer targets include Faster R-CNN, SSD, and YOLOv5
- Metrics: Transferability score, naturalness score, digital and physical attack results

## Results

- Main quantitative result: MVPatch outperforms prior baselines on both transferability and naturalness in digital and physical evaluations.
- What worked best: The ensemble-based MPBM for transfer plus HPBM for visual realism
- What failed or stayed weak: Exact benchmark tables still need extraction for the capstone notes

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — transfer-improvement framing is directly relevant to v8->v11/v26 experiments
- Direct relevance to YOLO11: Moderate to high
- Direct relevance to YOLO26: Moderate — useful for transfer/stealth methodology, but not architecture-specific
- What I can reproduce: Ensemble-style transfer training ideas and physical robustness framing
- What I can cite: Transferability + stealth benchmark beyond T-SEA

## Open Questions

- Does this transfer across YOLO versions? Yes, that is one of the main claims
- Is the patch digital only, or physically tested? Both
- Is the code available? TODO
- What is missing for my project? Exact numbers for the comparison table and details on the physical protocol

## TODO

- [ ] Extract the main digital and physical benchmark table
- [ ] Compare MVPatch's ensemble strategy against T-SEA
- [ ] Record the naturalness and transferability metrics for the write-up
