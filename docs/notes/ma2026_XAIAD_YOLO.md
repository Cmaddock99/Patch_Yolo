# Paper Review: Ma et al. (2026) — XAIAD-YOLO

## Citation

- Title: Explainable AI-guided test-time adversarial defense for resilient YOLO detectors in Industrial Internet of Things
- Authors: Ruinan Ma, Zuobin Ying, Wenjuan Li, Dehua Zhu, Wanlei Zhou, Hongyi Liu
- Venue / Year: Future Generation Computer Systems, Volume 179, June 2026 (Elsevier)
- URL: https://www.sciencedirect.com/science/article/pii/S0167739X25006508
- PDF: Not freely available (Elsevier paywall)

## Problem

- What threat model is assumed? Both white-box and black-box adversarial attacks on deployed YOLO in IIoT systems.
- What detector or classifier is defended? YOLO variants — specifically covers anchor-based, anchor-free, lightweight, and non-lightweight YOLO architectures. (This implies coverage of YOLOv5 through at least YOLOv8/v11.)
- What is the defense goal? Enable test-time adversarial defense without retraining — critical for deployed IIoT systems where model retraining is impractical. Use XAI saliency maps to locate and neutralize adversarial artifacts.

## Method

- Defense type: **Two-stage test-time purification framework (XAIAD-YOLO)**:
  1. **Stage 1 — High-frequency filtering**: Signal processing applied to remove high-frequency adversarial noise components.
  2. **Stage 2 — XAI-guided feature destabilization**: Uses saliency maps based on "differential feature stability" to locate adversarial artifacts in feature space, then applies targeted perturbation to neutralize them.
- XAI component: Achieves **66.08 FPS** (1.56× faster than Grad-CAM++) — designed to be runtime-efficient.
- No retraining required — operates at inference time only.
- Applicable to: anchor-based, anchor-free, lightweight, and non-lightweight YOLO variants.

## Results

- Significantly improves adversarial robustness under both white-box and black-box attack scenarios.
- 66.08 FPS inference speed (1.56× faster than Grad-CAM++).
- Full quantitative breakdown (AP/mAP clean vs. defended) in the Elsevier paper.

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: High for a defenses section. XAIAD-YOLO is explicitly designed for deployed YOLO systems and covers the relevant model families.
- What I can cite: For test-time defense without retraining; for XAI-guided adversarial purification; for the IIoT deployment context (edge devices with small YOLO models — directly connects to Gala et al.'s model-size/robustness finding).
- What is missing: Full quantitative results require institutional Elsevier access. Code available via anonymous repository (mentioned in the paper).
