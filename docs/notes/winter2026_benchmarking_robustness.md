# Paper Review: Winter et al. (2026) — Benchmarking Adversarial Robustness for Object Detection

## Citation

- Title: Benchmarking Adversarial Robustness and Adversarial Training Strategies for Object Detection
- Authors: Alexis Winter, Jean-Vincent Martini, Romaric Audigier, Angelique Loesch, Bertrand Luvison
- Venue / Year: arXiv:2602.16494, submitted February 2026
- URL: https://arxiv.org/abs/2602.16494
- PDF: ../papers/winter2026_benchmarking_robustness_2602.16494.pdf

## ⚠️ Scope Caveat

**This paper is about non-patch digital attacks only.** The authors explicitly exclude patch-based attacks from their benchmark, stating: "we exclude patch-based attacks. These attacks are perceptible by design and operate on a 'cost' model that is completely different from the perturbation measures used by imperceptible attacks." It also does not include YOLOv8, YOLO11, or YOLO26 — only YOLOv3, YOLOX, Faster R-CNN, FCOS, DETR, Mask R-CNN (Swin), and DINO. **Relevance to this capstone is limited.**

## Problem

- What threat model is assumed? Digital, non-patch-based adversarial perturbations (imperceptible). White-box and black-box settings.
- What detector or classifier is attacked? YOLOv3, YOLOX, Faster R-CNN (ResNet-50), FCOS, DETR (ResNet-50), Mask R-CNN (Swin), DINO (Swin-L).
- What is the attack goal? Establish a fair, unified benchmark for comparing digital attacks and adversarial training strategies across heterogeneous detectors.

## Method

Benchmark framework evaluating four attacks (OSFD, EBAD, CAA, PhantomSponges) with new metrics:
- **APₗₒc**: Localization-only metric (separates bbox errors from classification errors)
- **CSR**: Classification success ratio
- **LPIPS**: Perceptual distance metric (replaces L∞ as more accurate perceptibility measure)

## Key Findings

**CNN vs Transformer robustness:**
- DINO (transformer): 89.6% clean mAP, drops only 27.3% maximum under OSFD attack
- YOLOv3 (CNN): 84%+ mAP reduction under same attack
- Transformer architectures are dramatically more robust in black-box transfer scenarios

**Adversarial training:**
- Mixed-attack training (OSFD 75% + EBAD ε=50 25%) outperforms single-attack training
- Accuracy-robustness trade-off is small: 2.3 pp benign mAP cost for OSFD-trained YOLOv3

**Metric finding:** L∞ norm is inadequate for perceptibility; LPIPS is more appropriate

**Attack timings (TITAN RTX):** CAA 84s/image, OSFD 44s/image, EBAD 17s/image

| Attack | YOLOv3 mAP Drop | DINO mAP Drop |
|---|---|---|
| OSFD | 84.3% | 27.3% |
| EBAD (ε=30) | 69.3% | 4.4% |
| CAA | 83.8% | 0.7% |

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: **Low** — patch-based attacks are excluded, and Ultralytics models are not tested.
- What I can cite: For the general framing that CNN-based detectors are more vulnerable than transformer-based ones (relevant if discussing YOLO's CNN backbone as the attack surface). For the argument that evaluation metrics matter (LPIPS vs L∞).
- What is missing for my project: Everything specific to patch attacks on YOLO. Use this only in an introduction or related-work section to contrast with patch-based attacks.
