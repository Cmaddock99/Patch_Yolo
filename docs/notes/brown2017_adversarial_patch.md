# Paper Review: Brown et al. (2017) — Adversarial Patch

## Citation

- Title: Adversarial Patch
- Authors: Tom B. Brown, Dandelion Mané, Aurko Roy, Martín Abadi, Justin Gilmer
- Venue / Year: arXiv:1712.09665 (NIPS 2017 Workshop)
- URL: https://arxiv.org/abs/1712.09665
- PDF: ../papers/brown2017_adversarial_patch_1712.09665.pdf

## Problem

- What threat model is assumed? White-box (access to model gradients); physically realizable (patch can be printed).
- What detector or classifier is attacked? Image classifiers (ImageNet-trained models).
- What is the attack goal? Force the classifier to output a target class of the attacker's choice, regardless of the rest of the scene. One patch works universally across many scenes.

## Method

- Patch type: A small, printable image region that is universal (works across images) and targeted (forces a specific class prediction).
- Optimization method: Expectation over Transformations (EoT) — gradient descent on patch pixels, averaging over randomly sampled transformations to build robustness into the patch during training.
- Loss terms: Cross-entropy loss to maximize the probability of the target class.
- Transformations / EoT details: Random rotation, scale, and translation applied during training to ensure the patch works under real-world viewing conditions.
- Physical-world considerations: Patches were printed and photographed; demonstrated to work even when physically held in front of a scene.

## Experimental Setup

- Dataset: ImageNet, COCO
- Target classes: Various (attacker-chosen target class labels)
- Model versions: ImageNet classifiers
- Metrics: Top-1 / Top-5 accuracy drop; target class confidence

## Results

- Main quantitative result: Printed patches successfully caused classifiers to output the attacker's chosen class across a wide range of scenes and viewing conditions.
- What worked best: Combining random scale, rotation, and translation during EoT training yielded robust physical-world patches.
- What failed or stayed weak: Only attacks classifiers — no bounding box regression, no object detection pipeline.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Indirect — establishes the universal patch concept and EoT training framework that all subsequent detector attacks build on.
- Direct relevance to YOLO11: Same — foundational framing only.
- Direct relevance to YOLO26: Same — foundational framing only.
- What I can reproduce: The EoT training loop concept is directly used in Thys et al. and in our `create_adv_patch.py` baseline.
- What I can cite: As the foundational universal patch paper for any capstone introduction section.

## Open Questions

- Does this transfer across YOLO versions? Not applicable — classifier only.
- Is the patch digital only, or physically tested? Physically tested (printed and photographed).
- Is the code available? Yes — referenced in the TensorFlow/CleverHans project.
- What is missing for my project? Detector-specific loss (objectness + bbox regression) is not addressed; this paper only covers classifiers.
