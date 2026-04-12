# Paper Review: Zhou et al. — Sequence-Level Adversarial Clothing for Human Detection Evasion

## Citation

- Title: Physically Realistic Sequence-Level Adversarial Clothing for Robust Human-Detection Evasion
- Authors: Dingkun Zhou, Patrick P. K. Chan, Hengxu Wu, Shikang Zheng, Ruiqi Huang
- Venue / Year: arXiv, 2025
- arXiv: 2511.16020
- URL: https://arxiv.org/abs/2511.16020
- PDF: `docs/papers/zhou2025_sequence_level_clothing_2511.16020.pdf`
- Citations: 0 (very new)

## Problem

- What threat model is assumed? Physical adversary wearing adversarial clothing; attacker moves naturally through a surveillance environment (video sequence)
- What detector is attacked? Human detection systems (YOLO-family surveillance detectors)
- What is the attack goal? Human vanishing in video — adversarial clothing texture remains effective throughout an entire walking video, not just individual frames

## Method

- Patch type: Full clothing adversarial texture (shirt, trousers, hat) mapped to UV space
- Key insight: Existing methods optimize per-frame, causing adversarial effect to break between frames as pose/view changes. Sequence-level optimization ensures the texture is adversarial across entire walking sequences.
- Technique: UV-space parameterization with compact palette + control-point representation; ICC color locking to keep all colors printable
- Optimization method: Temporal sequence loss — evaluates adversarial effect across a sequence of frames rather than single images
- Physical-world considerations: ICC locking for print-accurate colors; tested in physical settings

## Experimental Setup

- Dataset: Video sequences of walking persons in surveillance scenarios
- Target classes: Human / person
- Model versions: YOLO-family detectors
- Metrics: ASR across full video sequences; both digital and physical

## Results

- Main quantitative result: TODO — 0 citations, very new (arXiv Nov 2025); read full paper
- Key advance: Temporal consistency — patch remains effective as person walks, turns, and deforms clothing
- Printability constraint: ICC locking ensures colors reproduce accurately on fabric

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — surveillance use case is exactly your capstone framing
- Direct relevance to YOLO11: High
- Direct relevance to YOLO26: Medium — not likely tested but the temporal framing is relevant
- What I can cite: State-of-the-art (2025) physical adversarial clothing with temporal robustness; most realistic physical threat model for surveillance
- What I can reproduce: Per-frame evaluation is easy to replicate; temporal sequence evaluation requires video — beyond current experiment scope

## Open Questions

- What is the ASR across YOLO versions?
- Is code available?
- How does temporal sequence loss compare to standard EoT + DAP Creases Transform?
- Does it work against YOLO26?
