# Huang et al. (2019) — Universal Physical Camouflage Attacks

## Citation

- Title: *Universal Physical Camouflage Attacks on Object Detectors*
- Authors: Huang et al.
- Venue / Year: arXiv 1909.04326 (2019)
- URL: https://arxiv.org/abs/1909.04326
- Access: Open access preprint

## Problem

- What threat model is assumed? Physical-world adversarial camouflage attack with a universal pattern that should remain effective across scenes.
- What detector or classifier is attacked? Object detectors, including YOLO-style pipelines.
- What is the attack goal? Suppress detections in realistic physical settings using a detector-aware camouflage pattern instead of a purely digital perturbation.

## Method

- Patch type: Universal physical camouflage / printable patch
- Optimization method: Detector-specific gradient optimization
- Loss terms: Object-detector-oriented suppression loss with physical robustness terms
- Transformations / EoT details: Includes deformation-aware and physical-world transformations
- Physical-world considerations: Designed specifically for real, printed deployment rather than simulation only

## Experimental Setup

- Dataset: TODO — extract from full paper
- Target classes: TODO — extract from full paper
- Model versions: Object detectors including YOLO-style models
- Metrics: Detection suppression / AP-style metrics

## Results

- Main quantitative result: TODO — pull the exact AP / success-rate numbers from the paper
- What worked best: Detector-aware physical camouflage with deformation robustness
- What failed or stayed weak: TODO — confirm failure modes from the full text

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — useful historical baseline for physically robust detector attacks
- Direct relevance to YOLO11: Moderate — same physical-world threat model applies
- Direct relevance to YOLO26: Moderate — helpful for physical framing, but not architecture-specific
- What I can reproduce: The physical-world transformation setup and detector-specific optimization framing
- What I can cite: Early physical detector-attack baseline with deformation-aware camouflage design

## Open Questions

- Does this transfer across YOLO versions? TODO — verify from full paper
- Is the patch digital only, or physically tested? Physical-world framing is central
- Is the code available? TODO
- What is missing for my project? Exact benchmark numbers and detector list

## TODO

- [ ] Read the full preprint and extract the detector list
- [ ] Add quantitative AP / success-rate numbers
- [ ] Compare its physical-world setup against Xu 2020 and AdvReal 2025
