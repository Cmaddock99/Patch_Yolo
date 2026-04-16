# Nazeri et al. (2024) — Adversarial Robustness of Detection Transformers

## Citation

- Title: *Evaluating the Adversarial Robustness of Detection Transformers*
- Authors: Amirhossein Nazeri, Chunheng Zhao, Pierluigi Pisu
- Venue / Year: arXiv 2024
- arXiv: 2412.18718
- DOI: 10.48550/arXiv.2412.18718
- URL: https://arxiv.org/abs/2412.18718
- PDF: `docs/papers/detection_transformers_robustness_2412.18718.pdf`

## Problem

- What threat model is assumed? White-box and black-box adversarial **pixel perturbation** attacks against DETR-family detectors, not adversarial patches (pp. 1-3).
- What detector family is studied? DETR with ResNet-50 / ResNet-101 backbones and their DC5 dilation variants, plus Faster R-CNN for transfer analysis (pp. 1-3, 5-6).
- What is the study goal? Quantify how vulnerable detection transformers are to standard adversarial attacks and how well attacks transfer within the DETR family versus to CNN-based detectors (pp. 1-2).

## Method

- Baseline attacks extended to DETR:
  - FGSM
  - PGD
  - C&W
- New contribution: a DETR-specific untargeted white-box attack that combines:
  - an initial one-step perturbation
  - a modified C&W-style optimization
  - class, box-regression, and IoU losses from both the final decoder output and intermediate decoder layers (pp. 3-4).
- Important scope note: this is an adversarial-robustness benchmark for end-to-end transformer detectors, not a physical or patch benchmark.

## Experimental Setup

- Datasets:
  - COCO 2017 validation set for general object detection
  - KITTI-derived validation split for autonomous-driving scenarios (p. 4).
- DETR variants:
  - DETR-R50
  - DETR-R50-DC5
  - DETR-R101
  - DETR-R101-DC5
- Metrics:
  - `AP` and `AR`
  - robustness score `RS = AP_adv / AP_clean`
  - transfer rate `TR` for black-box transferability (pp. 4-6).

## Results

### Table I - White-box attacks on COCO and KITTI (p. 5)

- DETR is clearly vulnerable to standard attacks.
- On COCO:
  - DETR-R50 clean `AP = 0.420`
  - PGD (`eps = 0.1`) lowers it to `0.070`
  - the paper's own attack lowers it to `0.084`
  - DETR-R50-DC5 clean `0.433 -> 0.047` under the paper's own attack
  - DETR-R101-DC5 clean `0.449 -> 0.034` under the paper's own attack
- On KITTI:
  - DETR-R50 clean `AP = 0.378`
  - PGD (`eps = 0.1`) lowers it to `0.034`
  - the paper's own attack lowers it to `0.075`
  - DETR-R101 clean `0.367 -> 0.023` under PGD and `0.061` under the paper's attack

### Table II - Intra-network and cross-network transferability (p. 6)

- Transfer within the DETR family is strong.
- Example on COCO, adversarial examples generated on DETR-R50:
  - PGD transfer rate to DETR-R50-DC5: `109.0%`
  - to DETR-R101: `106.2%`
  - to DETR-R101-DC5: `109.3%`
  - but only `54.8%` to Faster R-CNN
- The same pattern holds on KITTI:
  - strong DETR-to-DETR transfer
  - weaker transfer to Faster R-CNN than within-family transfer

### Table III - Transferability of the paper's own attack on COCO (p. 6)

- The proposed attack also transfers well inside the DETR family:
  - generated on DETR-R50, it reaches `99.5%` on DETR-R50-DC5 and `95.8%` on DETR-R101
- Cross-network transfer to Faster R-CNN is lower:
  - `43.5%`

## Key Claims

1. **Detection transformers are not inherently robust to adversarial perturbations; they are vulnerable in the same broad sense as CNN-based detectors.** Supported by Table I and the Section V discussion (pp. 5-6).
2. **PGD remains the strongest standard white-box attack in raw performance, but with larger perturbations.** Supported by Table I and the discussion below it (pp. 5-6).
3. **The paper's DETR-specific attack reaches PGD-like performance on COCO while keeping perturbations smaller.** Supported by the Table I comparisons and discussion on page 6.
4. **Transfer is strongest within the DETR family and weaker across architectural families.** Supported by Tables II and III (p. 6).

## Threat Model

- White-box access for the main attack evaluation.
- Black-box transfer setting for cross-model transfer tests.
- Digital perturbation setting only.
- No physical or patch-based evaluation.

## Limitations and Failure Modes

- This is **not** an adversarial patch paper. It studies pixel perturbations, so its results should not be treated as direct patch-transfer evidence.
- The study contains no YOLO models and no Ultralytics results. Verified from the model list.
- The most useful repo value is architectural, not direct benchmarking.
- Because Faster R-CNN is the only CNN comparison target, cross-family transfer conclusions are still somewhat limited. This is my inference from the transfer setup.

## Defensive Takeaways

- DETR-family models are not automatically protected by their transformer structure.
- However, attack effectiveness is more architecture-local than universal, which matters for interpreting weak transfer from older YOLO patch sources into DETR-like targets.
- This note is most useful as context for why a YOLO26-like detector may need detector-specific attack or defense reasoning.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: Low direct relevance. No YOLO models are tested.
- **YOLO11**: Low direct relevance.
- **YOLO26**: Medium to high indirect relevance. DETR is the closest family in the local corpus for understanding end-to-end transformer-style detector behavior under adversarial optimization, even though the attack type here is perturbation rather than patch.
- Capstone relevance: `3/5`. Architecture-context note, not a direct benchmark note.

## Reproducibility Signals

- The paper gives exact datasets, DETR variants, attack parameters, and transfer protocol.
- It states that code will be released upon publication (p. 1).
- Attack hyperparameters are explicit in Table I notes (p. 5).

## Open Questions

- Do adversarial **patches** show the same intra-family transfer pattern as the perturbation attacks here?
- Would YOLO26 behave more like DETR under detector-specific loss design than under old YOLO patch losses?
- How much of the weak cross-family transfer is due to transformer decoding versus end-to-end matching?
- Would a multi-model surrogate including DETR-like targets improve patch transfer into YOLO26-style detectors?

## Normalized Extraction

- Canonical slug: `nazeri2024_detr_robustness`
- Canonical source record: `docs/papers/detection_transformers_robustness_2412.18718.pdf`
- Evidence state: `page_cited`
- Threat model: digital white-box and black-box perturbation attacks on DETR-family detectors.
- Detector family and exact version: DETR-R50, DETR-R50-DC5, DETR-R101, DETR-R101-DC5, Faster R-CNN for transfer evaluation.
- Attack or defense goal: benchmark DETR robustness and design a DETR-specific untargeted perturbation attack.
- Loss or objective: class, box, and IoU objectives across final and intermediate decoder layers in a modified C&W-style optimization.
- Transforms / EoT: none; this is not a physical or EoT paper.
- Dataset: COCO 2017 and KITTI.
- Metrics: `AP`, `AR`, `RS`, and transfer rate `TR`.
- Strongest quantitative result: on COCO, the proposed attack drives DETR-R101-DC5 from clean `AP 0.449` to `0.034`, while PGD drives DETR-R50 from `0.420` to `0.070` and KITTI DETR-R101 from `0.367` to `0.023` (Table I, p. 5).
- Transfer findings: transfer is strong within the DETR family and notably weaker to Faster R-CNN, with the paper's own attack reaching only `43.5%` transfer to Faster R-CNN on COCO (Tables II-III, p. 6).
- Physical findings: none.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: indirect only, strongest for YOLO26-style architecture interpretation.
- Reproducible technique to borrow: treat transformer-style detectors as a separate attack family rather than assuming old CNN-era losses will transfer cleanly.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
