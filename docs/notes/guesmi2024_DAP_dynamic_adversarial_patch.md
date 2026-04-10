# Paper Review: Guesmi et al. (2024) — DAP

## Citation

- Title: DAP: A Dynamic Adversarial Patch for Evading Person Detectors
- Authors: Amira Guesmi, Ruitian Ding, Muhammad Abdullah Hanif, Ihsen Alouani, Muhammad Shafique
- Venue / Year: CVPR 2024; arXiv:2305.11618
- URL: https://arxiv.org/abs/2305.11618
- CVPR Open Access PDF: ../papers/guesmi2024_DAP_CVPR.pdf
- arXiv PDF: ../papers/guesmi2024_DAP_dynamic_adversarial_patch_2305.11618.pdf

## Problem

- What threat model is assumed? White-box (YOLO gradients used); physically realizable (printed T-shirt test); addresses non-rigid deformation from clothing movement.
- What detector or classifier is attacked? YOLOv2, YOLOv3, YOLOv3tiny, YOLOv4, YOLOv4tiny, YOLOv7, Faster R-CNN.
- What is the attack goal? Hide persons from detectors even when the patch is worn on clothing that wrinkles, folds, and deforms — a key limitation of prior work that used rigid EoT transforms but ignored cloth-specific deformation.

## Method

- Patch type: Adversarial patch optimized directly in pixel space (not GAN latent space). Maintains naturalistic appearance through a similarity loss rather than a GAN prior.
- Optimization method: Adam optimizer (lr=0.001, β₁=0.9, β₂=0.999). Direct pixel-value optimization.
- Loss terms (weighted: α=1, β=4, γ=0.5):
  ```
  L_total = α·L_det + β·L_sim + γ·L_tv
  ```
  - **L_det**: Detection loss — minimizes `(1/n)·Σ[1/#objects · Σ(D^j_obj × D^j_cls)]`; suppresses both objectness and person class probability.
  - **L_sim**: Similarity loss — maximizes cosine similarity to a benign target image: `L_sim = -(Σ P_i,j·N_i,j / √[ΣP²_i,j]·√[ΣN²_i,j])²` — squared form slows convergence, keeps patch naturalistic.
  - **L_tv**: Total variation smoothness: `L_tv = Σ√[(P_{i+1,j}-P_{i,j})² + (P_{i,j+1}-P_{i,j})²]`
- **Creases Transformation (CT) block** — the key innovation. Simulates cloth wrinkles by displacing patch pixels using a crease vector from a random origin point:
  ```
  multiplier(x,y) = 1 - [sin²θ · ((x-x₀)² + (y-y₀)²)] / [width² + height²]
  ```
  where θ is the angle between the pixel's direction from (x₀,y₀) and the crease directional vector. Emulates natural variation in crease intensity along crease length.
- Transformations / EoT details: Rotation ±20°, scale [0.25, 1.25], noise ±0.1, brightness ±0.1, contrast [0.8, 1.2], affine 0.7.
- Physical-world considerations: Printed on T-shirt (20.5cm × 21.5cm). Physical test with YOLOv3tiny on edge cameras.

## Experimental Setup

- Dataset: INRIA Person dataset (614 training, 288 test detections)
- Target classes: Person
- Model versions: YOLOv2, YOLOv3, YOLOv3tiny, YOLOv4, YOLOv4tiny, YOLOv7, Faster R-CNN
- Metrics: Attack success rate (1 - AP), mAP

## Results

**Digital (no deformation transforms):**
| Model | Clean mAP | DAP mAP | Success Rate |
|---|---|---|---|
| YOLOv3tiny | ~100% | 6.54% | **93.46%** |
| YOLOv7 | ~100% | 17.72% | **82.28%** |
| YOLOv3 | ~100% | 32.63% | 67.37% |

**With non-rigid cloth deformations:**
| Model | mAP | Success Rate |
|---|---|---|
| YOLOv3tiny | 15.44% | 84.56% |
| YOLOv3 | 37.70% | 62.30% |
| FasterRCNN | 30.60% | 69.40% |

**Transferability:** YOLOv3tiny-trained patch → YOLOv3: 64.07% success

**Physical (printed T-shirt, YOLOv3tiny):**
- True Positive Rate (concealment): 92.01%
- False Positive Rate: 8.33%
- Overall success rate: **65%**

**vs. baselines (YOLOv3tiny, digital):**
- DAP: 6.54% mAP
- NAP (GAN): 10.02% mAP
- Adversarial YOLO (Thys): 8.74% mAP
- UPC: 63.82% mAP (weaker)

DAP outperforms GAN-based NAP while requiring no pretrained generative model.

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — the Creases Transformation is applicable to any YOLO version. Cloth deformation is a real issue if testing with wearable patches.
- Direct relevance to YOLO11: Same — directly portable.
- Direct relevance to YOLO26: Same — CT block addresses physical deployment, not architecture-specific.
- What I can reproduce: Code available at CVPR open access. Requires INRIA dataset + YOLO weights. No GAN pretrain needed — lower setup cost than Hu et al.
- What I can cite: For the Creases Transformation approach to cloth deformation; for the L_sim naturalism approach; for the digital vs. non-rigid deformation performance comparison; as the CVPR 2024 state-of-the-art for person-vanishing.

## Open Questions

- Does this transfer across YOLO versions? YOLOv3tiny → YOLOv3 transfer demonstrated (64%). YOLOv7 → v8/v11/v26 untested.
- Is the patch digital only, or physically tested? Both. Physical T-shirt test included.
- Is the code available? Yes — CVPR 2024 open access.
- What is missing for my project? No evaluation on YOLOv8, v11, or v26. No comparison with ART's DPatch framework.
