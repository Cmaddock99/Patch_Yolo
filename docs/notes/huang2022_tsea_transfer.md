# Huang et al. (2022) — T-SEA: Transfer-based Self-Ensemble Attack

## Citation

- Title: *T-SEA: Transfer-based Self-Ensemble Attack on Object Detection*
- Authors: Hao Huang, Ziyan Chen, Huanran Chen, Yongtao Wang
- Venue / Year: arXiv 2022 (published in proceedings)
- arXiv: 2211.09773
- URL: https://arxiv.org/abs/2211.09773
- Code: https://github.com/VDIGPKU/T-SEA
- PDF: `docs/papers/huang2022_tsea_transfer_2211.09773.pdf`

## Problem

- What threat model is assumed? Black-box transfer of adversarial patches using only a single source model (no access to target model).
- What detector or classifier is attacked? Multiple YOLO variants and other object detectors.
- What is the attack goal? Improve transferability of adversarial patches without requiring access to an ensemble of models during training.

## Method

- Patch type: Standard adversarial patch
- Optimization method: Self-ensemble — augments the single source model's gradient by applying diverse transformations to the input, model (dropout variants), and patch itself during training.
- Loss terms: Detection suppression loss over self-ensemble of model states
- Key finding: By treating different augmented versions of a single model as an implicit ensemble, the patch avoids overfitting to the specific gradient landscape of the source model. **Greatly improves black-box transferability.**
- Transformations / EoT details: Self-ensemble across input augmentations, model augmentations (e.g., dropout), and patch augmentations simultaneously.
- Physical-world considerations: Tested on physical printed patches in some experiments.

## Experimental Setup

- Dataset: COCO
- Target classes: Person, vehicle, multiple
- Model versions: YOLOv2, v3, v4, v5 as source; multiple detectors as black-box targets
- Metrics: mAP drop, attack success rate across target models

## Results

- Main quantitative result: T-SEA achieves substantially better cross-model transfer than single-model baselines with no additional model access required.
- AdvReal benchmark showed T-SEA at 21.65% ASR physical — lower than their AdvReal framework but still competitive.
- What worked best: Combining all three self-ensemble dimensions simultaneously.
- What failed or stayed weak: Single augmentation dimension alone (input-only or model-only).

## Relevance to My Capstone

- Direct relevance to YOLOv8: **HIGH** — you could apply T-SEA's self-ensemble approach to your v8n training to improve the 39.4% v8→v11 and 16% v8→v26 transfer rates without needing access to v11/v26 during training.
- Direct relevance to YOLO11: Same — train on v11 with T-SEA to improve v11→v26 transfer.
- Direct relevance to YOLO26: Indirect — T-SEA as source model training would produce better-transferring patches targeting v26 as black-box.
- What I can reproduce: The code is open source at github.com/VDIGPKU/T-SEA. Could be a direct improvement experiment if v26 results need boosting.
- What I can cite: Technique citation for "if we applied ensemble-based training, transfer would likely improve."

## Open Questions

- Does this transfer across YOLO versions? Yes — the entire paper is about this.
- Is the patch digital only? Physical tests included.
- Is the code available? **Yes — github.com/VDIGPKU/T-SEA**
- What is missing for my project? Needs adaptation to Ultralytics API (original code likely uses older YOLO pip packages).

## TODO

- [ ] Clone T-SEA code and check if it can be adapted to Ultralytics YOLO
- [ ] Read Section 3 (self-ensemble formulation) for the specific implementation details
- [ ] Consider adding T-SEA as a v2 ablation if v26 suppression remains below 30%
