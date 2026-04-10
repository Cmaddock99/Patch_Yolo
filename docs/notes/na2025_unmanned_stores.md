# Paper Review: Na et al. (2025) — Adversarial Patches in Unmanned Stores

## Citation

- Title: Robustness Analysis against Adversarial Patch Attacks in Fully Unmanned Stores
- Authors: Hyunsik Na, Wonho Lee, Seungdeok Roh, Sohee Park, Daeseon Choi
- Venue / Year: arXiv:2505.08835, 2025
- URL: https://arxiv.org/abs/2505.08835
- PDF: ../papers/na2025_unmanned_stores_2505.08835.pdf

## Problem

- What threat model is assumed? White-box and black-box (shadow attack); physically realizable; deployed retail environment.
- What detector or classifier is attacked? YOLOv5l6 (primary), YOLOv5x6 (shadow/black-box).
- What is the attack goal? Exploit adversarial patches in autonomous checkout systems. Three attack types studied:
  1. **Hiding** — conceal items to enable theft / misidentification
  2. **Creating** — fabricate false detections (inventory errors, fake promotions)
  3. **Altering** — misclassify items to wrong class (wrong pricing, brand confusion)

## Method

- Novel contribution: **Color Histogram Similarity Loss** — Chi-square distance between HSV-space color histograms of the target object and the patch. Found "Chi-S-based similarity in HSV space showed the highest positive correlation (0.284)" between color similarity and attack success. Helps generated patches match victim object colors, improving hiding effectiveness.
- Optimization: Standard patch optimization with the new color loss term added.
- Physical-world considerations: Tested in a real retail testbed (actual unmanned store environment). Both digital and physical evaluations reported.

## Experimental Setup

- Datasets:
  - **Snack dataset**: 21 categories (1,676 train / 479 val / 239 test)
  - **Fruit dataset**: 10 categories (1,550 train / 430 val / 237 test)
  - Images resized to 1088×1088
- Target classes: Snack and fruit product categories
- Model versions: YOLOv5l6 (white-box), YOLOv5x6 (black-box shadow)
- Metrics: Confusion Metric, mAP, Complete IoU

## Results

**Digital:**
| Attack | Dataset | Key Metric |
|---|---|---|
| Hiding | Snack | Confusion: 0.911; mAP: 0.079 (from 0.996) |
| Creating | Fruit | Confusion: 0.479; Complete IoU: 0.127 |
| Altering | Snack | Confusion: 0.176; mAP: 0.349 (from 0.996) |

**Physical (actual retail testbed, YOLOv5):**
| Attack | Snacks | Fruits |
|---|---|---|
| Hiding | 69.1% success | 77.6% success |
| Creating | 24.0% success | 44.6% success |
| Altering | 10.1% success | 10.2% success |

**Black-box (shadow attack):** Up to 0.717 confusion metric for Hiding attacks — significantly stronger than model-transfer attacks.

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: Low for the core person-vanishing goal, but useful for the "broader attack surface" framing. This paper shows adversarial patches matter in deployed commercial systems, not just academic surveillance benchmarks.
- What I can cite: As an example of real-world adversarial patch deployment in a commercial system (motivation for why this research matters). For the three-attack taxonomy (hiding/creating/altering) as a way to categorize capstone attack types.
- What is missing for my project: Uses YOLOv5 only; person class not the target; focuses on retail rather than surveillance.
