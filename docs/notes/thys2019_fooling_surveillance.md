# Paper Review: Thys et al. (2019) — Fooling Automated Surveillance Cameras

## Citation

- Title: Fooling Automated Surveillance Cameras: Adversarial Patches to Attack Person Detection
- Authors: Simen Thys, Wiebe Van Ranst, Toon Goedemé
- Venue / Year: CVPR Workshop: CV-COPS 2019; arXiv:1904.08653
- URL: https://arxiv.org/abs/1904.08653
- PDF: ../papers/thys2019_fooling_surveillance_1904.08653.pdf
- Code: https://gitlab.com/EAVISE/adversarial-yolo

## Problem

- What threat model is assumed? White-box (gradients of YOLOv2 used during training); physically realizable (patch printed and held by person).
- What detector or classifier is attacked? YOLOv2 trained on COCO (person class).
- What is the attack goal? Hide a person from a YOLOv2 surveillance camera detector by holding a printed adversarial patch (~40cm × 40cm cardboard). The patch must work across diverse person appearances (high intra-class variation).

## Method

- Patch type: Universal, printable ~40cm × 40cm patch. Optimized to suppress YOLOv2's detection of a person across many images and real-world conditions.
- Optimization method: Gradient descent on patch pixel values (network weights frozen). Adam optimizer.
- Loss terms: Three-component loss:
  - `L = α·L_nps + β·L_tv + L_obj`
  - **L_nps** (Non-Printability Score): Penalizes colors that cannot be reproduced by a standard printer.
  - **L_tv** (Total Variation): Enforces smooth color transitions — prevents noisy, unnatural textures.
  - **L_obj** (Detection Loss): Minimizes YOLOv2's objectness or classification score for the person class.
  - Three variants tested: OBJ-CLS (product of objectness and class probability), OBJ (objectness alone), CLS (class probability alone).
- Transformations / EoT details: Random transforms applied each iteration to build robustness:
  - Rotation: ±20 degrees
  - Scaling: random scale changes
  - Noise: random perturbations
  - Brightness/Contrast: random adjustments
  - All transforms are differentiable to allow backpropagation through to the patch.
- Physical-world considerations: Patch physically printed and held in front of person in real filmed scenarios.

## Experimental Setup

- Dataset: INRIA Person dataset (full-body pedestrians, train split)
- Target classes: Person (COCO class)
- Model versions: YOLOv2 trained on COCO
- Metrics: Person detection AP, precision/recall curves (threshold derived from clean baseline PR curve at 0.4 confidence)

## Results

Main quantitative results (recall at 0.4 confidence threshold):

| Approach | Recall (%) |
|---|---|
| Clean baseline | 100% |
| Random noise patch | 87.14% |
| OBJ-CLS patch | 39.31% |
| **OBJ patch (best)** | **26.46%** |
| CLS patch | 77.58% |

- **Best result: OBJ loss reduced detection recall from 100% to 26.46%** — meaning the patch suppressed ~74% of person detections.
- Objectness minimization outperformed class probability minimization by a large margin.
- Paper also demonstrated real-world effectiveness: patch printed and held by a person was filmed and shown to fool the detector.
- What worked best: OBJ loss + L_nps + L_tv combination. Minimizing objectness directly is more effective than minimizing class confidence.
- What failed: CLS-only loss barely improved over random noise.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Very high. This paper's method (objectness minimization, EoT transforms, INRIA dataset) is the canonical baseline for person-vanishing attacks. YOLOv8 uses a similar objectness-class joint head.
- Direct relevance to YOLO11: Same — both use Ultralytics C3/C2f architecture with shared detection head design.
- Direct relevance to YOLO26: High interest — YOLO26's NMS-free design may respond differently to objectness suppression since it uses a different detection formulation.
- What I can reproduce: The full training loop is reproducible with INRIA dataset + YOLOv2/v5 weights. The `create_adv_patch.py` baseline in this repo uses the same DPatch framework adapted for YOLOv5.
- What I can cite: For loss design (L_nps + L_tv + L_obj), EoT transforms, INRIA dataset setup, and the key finding that objectness loss outperforms class probability loss.

## Open Questions

- Does this transfer across YOLO versions? Not tested in this paper. Transfer from YOLOv2 to YOLOv5/v8/v11/v26 is the central open question for my capstone.
- Is the patch digital only, or physically tested? Both — digital evaluation on INRIA + real filmed test with printed patch.
- Is the code available? Yes: https://gitlab.com/EAVISE/adversarial-yolo
- What is missing for my project? Only tested on YOLOv2; no evaluation on Ultralytics models; no mAP reported (only recall/AP curves).
