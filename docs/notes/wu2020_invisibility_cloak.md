# Wu et al. (2020) — Making an Invisibility Cloak

## Citation

- Title: *Making an Invisibility Cloak: Real World Adversarial Attacks on Object Detectors*
- Authors: Wu, Lim, Davis, Goldstein
- Venue / Year: ECCV 2020
- URL: https://arxiv.org/abs/1910.14667
- PDF: `docs/papers/wu2020_invisibility_cloak_1910.14667.pdf`

## Problem

- What threat model is assumed? White-box and black-box adversarial patch attacks on object detectors, including physical deployment.
- What detector or classifier is attacked? YOLOv2, YOLOv3, and Faster R-CNN family detectors.
- What is the attack goal? Hide objects from detectors and study how well attacks transfer across models, classes, datasets, and physical settings.

## Method

- Patch type: Localized adversarial patch for posters and wearable clothing
- Optimization method: Detector-specific gradient optimization with single-model and ensemble variants
- Loss terms: Detection-suppression objective
- Transformations / EoT details: Includes simulation-to-physical transfer analysis and experiments with physical deformations
- Physical-world considerations: Printed poster and wearable-clothing tests are a central part of the paper

## Experimental Setup

- Dataset: COCO, INRIA, Pascal VOC-style transfer settings
- Target classes: Person and other detector classes
- Model versions: YOLOv2, YOLOv3, Faster R-CNN variants
- Metrics: AP and physical success rates

## Results

- Main quantitative result: In digital simulation, adversarially learned patches reduce detector AP by at least 29%, dropping as low as 7.5% AP on retrained YOLOv2.
- What worked best: YOLO-trained patches and ensemble variants; posters are easier than wearable attacks
- What failed or stayed weak: Faster R-CNN patches transfer poorly to YOLO, and wearable attacks transfer much worse than printed-poster attacks

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — useful historical baseline for cross-model transfer and physical deployment
- Direct relevance to YOLO11: Moderate
- Direct relevance to YOLO26: Moderate — physical and transfer framing matters, but the architectures are older
- What I can reproduce: Poster-vs-wearable evaluation framing and cross-detector transfer comparisons
- What I can cite: Strong background citation for the physical transfer problem and the digital-to-physical gap

## Open Questions

- Does this transfer across YOLO versions? Yes, but mostly within older YOLO families
- Is the patch digital only, or physically tested? Both
- Is the code available? TODO
- What is missing for my project? Modern Ultralytics and YOLO26-era comparisons

## TODO

- [ ] Extract the poster and wearable success-rate tables for the write-up
- [ ] Pull the best black-box transfer numbers into the transfer section
- [ ] Compare their digital-to-physical gap against Schack 2024
