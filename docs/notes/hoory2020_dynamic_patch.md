# Paper Review: Hoory et al. (2020) — Dynamic Adversarial Patch

## Citation

- Title: Dynamic Adversarial Patch for Evading Object Detection Models
- Authors: Shahar Hoory, Tzvika Shapira, Asaf Shabtai, Yuval Elovici
- Venue / Year: arXiv:2010.13070; IEEE Robotics and Automation Letters (RA-L), 2021
- URL: https://arxiv.org/abs/2010.13070
- PDF: ../papers/hoory2020_dynamic_patch_2010.13070.pdf

## Problem

- What threat model is assumed? White-box (gradients of YOLOv2 used); physically realizable (patches displayed on screens attached to car).
- What detector or classifier is attacked? YOLOv2 (car class); also tested on YOLOv3, Fast R-CNN, Mask R-CNN.
- What is the attack goal? Hide a car from YOLOv2 detection across a wide viewing angle range (90°). Addresses the limitation of static patches that only work from a narrow angle.

## Method

- Patch type: Multiple angle-specific adversarial patches displayed on flat screens physically attached to the target car. Patches are dynamically switched based on camera position relative to the target.
- Optimization method: Gradient descent via Adam optimizer. Training data is split into angle-based subsets. The algorithm iteratively increases the number of subsets until test performance plateaus.
- Loss terms: Three variants tested:
  - **cls**: Minimizes maximum class probability for the target object across all predictions
  - **obj**: Minimizes objectness scores
  - **obj_cls**: Product of objectness and class probability (performed best in wide-angle tests)
  - Full objective: `J(p, xp) = α·TV(p) + Loss(fθ(xp))`
  - Semantic extension: `J(p, xp, C) = α·TV(p) + Σ_{yi∈C} Loss(fθ(xp), yi)` — adds semantically related classes (e.g., bus, truck) to excluded class set
- Transformations / EoT details: Random transformations for robustness; precise patch placement via perspective transformation on screen placeholder regions.
- Physical-world considerations: Patches displayed on 32" and 28" screens attached to car. Tested in underground parking (controlled lighting) and outdoor sunny conditions. Screen covers ~15% of car's rear area.

## Experimental Setup

- Dataset: ~471 frames from 20 FPS video of a Hyundai Elantra 2016 in an underground parking lot. Three car models tested: Hyundai Elantra 2016, Toyota Corolla 2006, Fiat Tipo 2018.
- Target classes: Car
- Model versions: YOLOv2 (primary); YOLOv3, Fast R-CNN, Mask R-CNN (transferability)
- Metrics: Attack success rate = % of video frames where "car" class is absent from detector output
- Camera: Samsung Galaxy Note 9 at 4m fixed distance

## Results

**Screens and patches:**
- 1 screen: 43.4% success (obj_cls)
- 2 screens: 74% success (obj_cls)

**Dynamic switching (side view):**
- 1 patch: 90% success (obj_cls)

**Wide-angle (90° coverage):**
- obj: 40% | cls: 41.3% | obj_cls: 80%

**Semantic patches (90°):**
- obj: 44.28% | cls: 35.17% | obj_cls: 72%

**Cross-model transferability:**
- Fiat Tipo (similar appearance): 71% success
- Toyota Corolla (different color): 51% success
- YOLOv3: 10.5–13.8% (poor transfer)
- Fast R-CNN, Mask R-CNN: No meaningful transfer

**Environment impact:**
- Underground parking (cloudy simulation): 80% success
- Sunny outdoor noon: 15–23.2% (large degradation due to screen glare)

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate. The multi-angle / viewpoint robustness concept is relevant if extending to physical-world evaluation; the core gradient-based approach is the same.
- Direct relevance to YOLO11: Same as YOLOv8.
- Direct relevance to YOLO26: Interesting — YOLO26's NMS-free formulation may behave differently under objectness suppression.
- What I can reproduce: The core single-screen, single-angle variant is straightforward to adapt. Dynamic switching requires screen hardware.
- What I can cite: For the multi-angle robustness motivation; for the obj_cls loss comparison; for the screen-glare / outdoor degradation finding (relevant to physical-world claims).

## Open Questions

- Does this transfer across YOLO versions? Poor transfer to YOLOv3 (10–14%); no transfer to R-CNN. Suggests YOLO-family-specific patches.
- Is the patch digital only, or physically tested? Physically tested (screens on car in parking lot).
- Is the code available? Not released.
- What is missing for my project? Focuses on car class only; no person-vanishing evaluation; screen-based physical setup is not directly reproducible in a capstone without hardware.
