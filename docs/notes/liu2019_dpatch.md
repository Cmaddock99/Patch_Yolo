# Paper Review: Liu et al. (2019) — DPatch

## Citation

- Title: DPatch: An Adversarial Patch Attack on Object Detectors
- Authors: Xin Liu, Huanrui Yang, Ziwei Liu, Linghao Song, Hai Li, Yiran Chen
- Venue / Year: AAAI Workshop on Artificial Intelligence Safety (SafeAI 2019); arXiv submitted June 2018
- URL: https://arxiv.org/abs/1806.02299
- PDF: ../papers/liu2019_dpatch_1806.02299.pdf

## Problem

- What threat model is assumed? White-box (gradients used for optimization); patch is position-independent (can be placed anywhere in the scene).
- What detector or classifier is attacked? Faster R-CNN (VGG16 and ResNet101) and YOLO, both trained on PASCAL VOC / COCO.
- What is the attack goal? Disable object detection entirely — suppress all detections across the scene regardless of patch location. Simultaneously attacks bounding box regression and classification.

## Method

- Patch type: Small square patch (default 40×40 pixels; also tested at 20×20 and 80×80). Position-agnostic — trained to work at arbitrary locations.
- Optimization method: Iterative gradient-based optimization. Untargeted: maximize detector loss. Targeted: minimize loss toward a fake target label and bbox.
  - Untargeted: `P̂_u = argmax_P E_{x,s}[L(A(x,s,P); ŷ, B̂)]`
  - Targeted: `P̂_t = argmin_P E_{x,s}[L(A(x,s,P); y_t, B_t)]`
- Loss terms: Combined classification loss + bounding box regression loss. Ground truth annotations for targeted attack set to `[DPatch_x, DPatch_y, DPatch_w, DPatch_h, target_label]`.
- Transformations / EoT details: Random transformations applied at training time for robustness (exact ranges not specified in abstract; position shift s is randomized).
- Physical-world considerations: Primarily a digital attack; physical robustness not the paper's focus.

## Experimental Setup

- Dataset: PASCAL VOC 2007 (primary), MS COCO (transferability)
- Target classes: Multiple VOC classes; person and vehicle classes highlighted
- Model versions: YOLO (modified 10×10 grid), Faster R-CNN with VGG16 and ResNet101
- Metrics: mAP (mean Average Precision)

## Results

- Main quantitative results:
  - YOLO baseline mAP: 65.7% → **below 1%** with untargeted DPatch
  - Faster R-CNN (ResNet101) baseline: 75.10% → **0.30%** with untargeted DPatch
  - Faster R-CNN (VGG16): 70.01% → near zero
  - Targeted attack (cow class): mAP dropped from 75.10% to 0.38%
  - Cross-dataset transfer (COCO-trained patch → VOC): Faster R-CNN mAP 75.10% → 28.00%; YOLO 65.70% → 24.34%
  - Cross-detector transfer: YOLO-trained patch on Faster R-CNN: considerable mAP decrease, slightly less severe than same-architecture attacks
- Patch size impact (cow-targeted, Faster R-CNN): 20×20 → 0.02%; 40×40 → 0.00%; 80×80 → 0.00%
- Training convergence: Largest drops in first 40,000 iterations; saturation around 180,000–200,000 iterations.
- Attack mechanism confirmed: RoIs concentrate exclusively on patch location rather than distributing across image.
- What worked best: Untargeted attack was most aggressive; position-independence is the key practical advantage.
- What failed or stayed weak: Some targeted attacks (bike, boat classes) left mAP above 25% with random placement.

## Relevance to My Capstone

- Direct relevance to YOLOv8: High. DPatch is the direct ancestor of ART's `DPatch` implementation used in `create_adv_patch.py`. The same loss structure (maximize detection loss) applies.
- Direct relevance to YOLO11: Same loss framework applies; architecture differences may affect RoI concentration behavior.
- Direct relevance to YOLO26: YOLO26's NMS-free end-to-end detection may change how RoIs concentrate — interesting research angle.
- What I can reproduce: The mAP-drop baseline is a standard benchmark. Can reproduce with ART's DPatch on YOLOv5 and extend to v8/v11/v26.
- What I can cite: For the loss design and position-independence property; for the cross-detector transfer finding.

## Open Questions

- Does this transfer across YOLO versions? Demonstrated transfer between YOLO and Faster R-CNN. Transfer across YOLOv5→v8→v11→v26 is the open question for my capstone.
- Is the patch digital only, or physically tested? Primarily digital. No physical robustness evaluation in this paper.
- Is the code available? Reference implementation: https://github.com/veralauee/DPatch
- What is missing for my project? No physical robustness transforms (rotation, brightness, etc.); no evaluation on Ultralytics YOLO models.
