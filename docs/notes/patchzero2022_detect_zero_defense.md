# Paper Review: PatchZero — Defending against Adversarial Patch Attacks

## Citation

- Title: PatchZero: Defending against Adversarial Patch Attacks by Detecting and Zeroing the Patch
- Authors: Xu, Fu, Jiang, Li, Xiao, and Chen
- Venue / Year: arXiv, 2022
- URL: https://arxiv.org/abs/2207.01795

## Problem

- What threat model is assumed? White-box adversary that plants a visible adversarial patch in the input image
- What detector is attacked? General object detector (defense paper)
- What is the attack goal? Defense — detect and neutralize the patch before the detector sees it

## Method

- Approach: Two-stage pipeline — (1) detect the adversarial patch region, (2) zero out (fill with neutral values) the patch pixels before inference
- Patch type: Any visible patch (digital or physical)
- Physical-world considerations: Tested against printed patches

## Experimental Setup

- Dataset: COCO + adversarial patch test sets
- Target classes: General object detection
- Model versions: Standard YOLO family
- Metrics: Clean AP (no patch), defended AP (patch zeroed), attack success rate reduction

## Results

- Main quantitative result: TODO — read full paper for precise numbers
- What worked best: Zeroing approach is detector-agnostic; no retraining needed for the underlying detector
- Compared to: Ad-YOLO (Ji 2021), SAC, NAPGuard — all require either retraining or a segmentation model

## Relevance to My Capstone

- Direct relevance to YOLOv8: Defense comparison table — "what stops your patch"
- Direct relevance to YOLO11: Likely applicable (detector-agnostic approach)
- Direct relevance to YOLO26: Likely applicable
- What I can cite: Defense paradigm #4 (detect-and-zero) as counterpart to Ad-YOLO (patch class), NAPGuard (semantic detection), SAC (inpainting)
- What I can reproduce: Could apply PatchZero preprocessing to your test images and measure effectiveness

## Open Questions

- Is code publicly available?
- What is the detection accuracy on naturalistic (GAN/diffusion) patches vs. raw gradient patches?
- How does false positive rate affect clean AP?
- TODO: read full paper for quantitative defense numbers
