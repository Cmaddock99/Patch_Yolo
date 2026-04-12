# Paper Review: TK-Patch — Universal Top-K Adversarial Patches for Cross-Model Person Evasion

## Citation

- Title: TK-Patch: Universal Top-K Adversarial Patches for Cross-Model Person Evasion
- Authors: S. Imran, Syed M. Kazam, Abbas Kazmi, Umair Raza, Fahim Maan, Nayyer Aafaq
- Venue / Year: ICoDT2 2025 (5th International Conference on Digital Futures and Transformative Technologies), IEEE
- DOI: 10.1109/ICoDT269104.2025.11360694
- URL: https://www.semanticscholar.org/paper/6cc0ad948a09e0a1377ec6e3f13653bd0575aa63

## Problem

- What threat model is assumed? Physical adversary deploying a printed patch on clothing; attacker cannot access model internals for all targets (model-agnostic framework)
- What detector is attacked? YOLOv3, YOLOv5, YOLOv7 simultaneously
- What is the attack goal? Person vanishing — universal patch effective across multiple YOLO versions without retraining per model

## Method

- Patch type: Printed patch worn on clothing (physical)
- Optimization method: Top-K loss — suppresses the top-K highest-confidence person detections instead of all detections; focuses gradient energy on confident detections
- Key insight: Standard loss targets all detections equally; TK-Patch focuses on the K most confident predictions, which are harder to suppress but more important for evasion
- Physical-world considerations: EoT-style transforms; tested in surveillance settings

## Experimental Setup

- Dataset: Persons in surveillance-style scenarios
- Target classes: Person (COCO class 0)
- Model versions: YOLOv3, YOLOv5, YOLOv7
- Metrics: ASR across models

## Results

- Main quantitative result: TODO — 0 citations, paper is very new; need full read for numbers
- What worked best: Multi-model universality — single patch degrades all three YOLO versions
- Unique contribution: Top-K loss design vs. standard full-detection suppression loss

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — the multi-model ensemble approach is exactly what your DOEPatch-style simultaneous v8+v11+v26 attack needs
- Direct relevance to YOLO11: High — same family as v3/v5/v7 targets; Top-K loss should apply directly
- Direct relevance to YOLO26: Medium — YOLO26 has no NMS but the Top-K concept (focus on top confident preds) maps to focusing on the highest-score channels in the `one2many` head
- What I can cite: Multi-YOLO universal patch design; Top-K loss as an alternative to mean-top-K your current implementation uses
- What I can reproduce: Top-K loss is straightforward — compare against your current loss formulation

## Open Questions

- What is the actual ASR on each YOLO version?
- Does the top-K approach outperform standard suppression loss for cross-version transfer?
- Is code available?
- Does it test on YOLOv8 or later anchor-free detectors?
