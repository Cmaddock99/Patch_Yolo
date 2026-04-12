# Paper Review: Adversarial Patches for Global Suppression of Object Detectors

## Citation

- Title: Adversarial patches for the global suppression of object detectors
- Authors: Kolter, Madry et al.
- Venue / Year: arXiv preprint, 2019
- URL: https://arxiv.org/abs/1906.11897

## Problem

- What threat model is assumed? Scene-level adversary who places a single static patch anywhere in the scene (not on a person's body)
- What detector is attacked? YOLOv3
- What is the attack goal? Suppress all person detections across the entire frame with a single globally-placed patch

## Method

- Patch type: Printed patch placed in the environment (on a wall, floor, or background object)
- Optimization method: Gradient-based patch optimization against YOLO detection loss
- Loss terms: Detection suppression loss over all bounding boxes in scene
- Physical-world considerations: Patch is scene-placed, not wearable

## Experimental Setup

- Dataset: Persons in indoor/outdoor scenes
- Target classes: Person (COCO class 0)
- Model versions: YOLOv3
- Metrics: ASR (fraction of scenes with zero person detections)

## Results

- Main quantitative result: A single patch placed anywhere in scene suppresses all person detections in YOLOv3
- What worked best: Global placement (not on body) — demonstrates the attack extends beyond wearable threat models
- What failed or stayed weak: TODO — read full paper for failure cases

## Relevance to My Capstone

- Direct relevance to YOLOv8: Conceptual — establishes scene-level patch threat model; your work is wearable but this is cited for framing
- Direct relevance to YOLO11: Low — not tested
- Direct relevance to YOLO26: Low — not tested; attention architecture likely resists the optimization
- What I can cite: Scene-level framing, global patch threat model as contrast to wearable patches
- What I can reproduce: N/A — not the target threat model

## Open Questions

- Does this transfer to YOLOv8/YOLO11/YOLO26?
- Is code available?
- TODO: read full paper for quantitative ASR numbers
