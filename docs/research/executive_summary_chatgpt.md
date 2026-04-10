# Executive Summary: Adversarial Patch Attacks on YOLO
*Source: ChatGPT-generated executive summary, imported 2026-04-10*
*Note: This document was AI-generated. Cross-check all claims and citations against verified_sources.md before citing in a paper or presentation.*

---

Adversarial "patch" attacks exploit deep detectors like YOLO by training a small, visible sticker (the patch) that, when placed in a scene, causes the model to ignore or misclassify objects.

## Key Findings

- YOLOv2 and later detectors are vulnerable: a patch can hide people from a YOLOv2 person detector (Thys et al. 2019).
- Since 2017, papers have proposed improved patch-generation methods (e.g. optimizing the patch in the latent space of a GAN for natural appearance), evaluated robustness to physical transformations, and explored novel setups (e.g. a transparent patch on the camera lens that hides all stop signs).
- Early work: Brown et al. (2017) introduced universal patches for classifiers.
- DPatch (Liu et al. 2019) attacked Faster-RCNN and YOLO on VOC/COCO, dropping YOLO's mAP to ~1%.
- Thys et al. (2019): a patch held by a person can hide them from YOLOv2.
- Later works incorporate robustness (random scale/rotation/noise augmentations) and naturalism (GAN-based patches).
- Gala et al. (2025): high evasion rates on Ultralytics YOLOv5–v10 using GAN-optimized patches.

## Patch Training Workflow

```
Input: Images + Pretrained YOLO
  → Initialize patch (e.g. random noise)
  → Apply random transforms (rotate, scale, noise, brightness)
  → Overlay patch on each image at target location
  → Forward pass through YOLO detector
  → Compute loss (e.g. minimize objectness/person score)
  → Backpropagate gradients to patch pixels
  → Update patch (Adam/SGD)
  → Repeat until convergence
  → Output: Final Adversarial Patch
```

## Key Papers Table

| Paper | Year | Target Model(s) | Patch Method (Loss) | Transforms | Dataset(s) | Metrics | Code |
|---|---|---|---|---|---|---|---|
| Brown et al. "Adversarial Patch" | 2017 | Image classifiers (ImageNet) | Optimize universal patch (cross-entropy loss to target class) over diverse images | Random rotation/scale/translation | ImageNet, COCO | Top-1/Top-5 accuracy drop, target class confidence | github.com/Brown/patch |
| Liu et al. (DPatch) | 2019 | Faster R-CNN, YOLOv2 (COCO/VOC) | Iteratively optimize patch to maximize detection loss (objectness + classification) | Position-agnostic (patch placed at random locations) | Pascal VOC, MS COCO | mAP drop | None reported |
| Thys et al. | 2019 | YOLOv2 (person class) | Minimize YOLO's person confidence. Tested: class probability, objectness, or product (objectness minimization worked best) | Rotate ±20°, random scale, gaussian noise, brightness/contrast | INRIA Persons (train); YOLOv2 trained on COCO | Person detection AP, precision/recall curves | GitLab: EAVISE/adversarial-yolo |
| Zolfi et al. (Translucent Patch) | 2021 | YOLOv5 (stop-sign class) | Optimize transparent patch on camera lens to hide target class while preserving others | Fixed patch on lens (no per-frame transforms) | Autonomous-driving images (e.g. KITTI) | % of target vs other detections | Not released |
| Hoory et al. (Dynamic Patch) | 2020 | YOLOv2 (car class) | Create multiple patches for different views; dynamically switch which patch is shown as camera angle changes. Loss: YOLOv2 detection score | Multiple fixed viewpoints covered by switching patches | Custom car videos (wide angle range) | % frames fooled by patch | Not released |
| Hu et al. (Naturalistic Patch) | 2021 | YOLOv2/v3/v4 (person) | Optimize patch in latent space of pretrained GAN (BigGAN/StyleGAN) to fool detector and look realistic. Loss: minimize objectness for person + latent priors | Digital and physical; random jittering and standard augmentations | MS COCO, INRIA | mAP drop; human perceptual realism scores | GitHub: aiiu-lab/Naturalistic-Adversarial-Patch |
| Schack et al. (Real-world Eval) | 2024 | YOLOv3, YOLOv5 | Evaluation study: tests fixed (pre-trained) patches under varying real-world conditions (two patch types: global vs. local) | Vary patch size, position, rotation, brightness, hue, blur in real indoor scene vs. digital simulations | Controlled lab scenes | mAP (global patch), detection confidence (local patch) | N/A |
| Gala et al. (IJIS) | 2025 | Ultralytics YOLOv5, v8–v10 | Adapt GAN-based method to modern YOLO models. Optimize patches to evade detection of person/vehicles | Digital transforms during training (scale, rotation, blur, etc.) | INRIA Persons, MPII Humans | Detection evasion rate (e.g. drop in AP) | GitHub |

## Open-Source Implementations

- **adversarial_yolo2** (Thys 2019 code) — PyTorch, YOLOv2. Includes `train_patch.py`, uses INRIA/COCO.
- **Adversarial-Patch-Attacks-TRAINING-YOLO-SSD-Pytorch** (alex96295) — YOLOv2, v3, v4 (COCO) and SSD (VOC). Scripts: `train_patch_yolov2.py`, etc.
- **AdvLogo** (Bomingmiao et al. 2023) — Diffusion model-based patches. Supports YOLOv2–v4 and SSD. GitHub: https://github.com/Bomingmiao/Advlogo
- **NaturalisticAdversarialPatches** (Gala IJIS 2025) — Official repo for YOLOv5/v8–v10. Includes Dockerfile, scripts, pretrained GAN models. https://github.com/Bimo99B9/NaturalisticAdversarialPatches
- **Naturalistic-Adversarial-Patch** (Hu ICCV 2021) — aiiu-lab, GAN-based patches for YOLOv2–v4. BigGAN/StyleGAN required.
- **TPatch** (USENIX 2023) — Triggered physical patch for YOLOv3 and YOLOv5 / Faster R-CNN. https://github.com/usslab/tpatch

## Recommended Next Steps (from summary)

1. Clarify target YOLO version and weights.
2. Implement patch training loop with random transforms (rotation ±20°, scaling ±20%, gaussian noise, brightness/contrast jitter).
3. Use objectness minimization loss (found most effective by Thys et al.).
4. Evaluate with mAP, recall, and fooling rate (fraction of target objects no longer detected at IoU>0.5).
5. Incorporate reproducibility checklist: fixed random seeds, documented hyperparameters (Adam, LR ~1e-2, 1000–5000 iterations), saved config.
6. Experiment with GAN-based naturalistic patches (Hu et al.) as a stretch goal.

## Recommended Metrics and Datasets

- **Metrics**: mAP (mean Average Precision), detection recall/miss rate, fooling rate (% targets suppressed), precision-recall curves, confidence heatmaps (Grad-CAM style).
- **Datasets**: INRIA Persons, MS COCO, Pascal VOC, MPII Humans.

## Milestone Timeline

| Year | Milestone |
|---|---|
| 2017 | Brown et al. — Universal adversarial patch (classification) |
| 2018 | Eykholt et al. — Physical sticker on stop signs |
| 2019 | Liu et al. — DPatch (object detectors); Thys et al. — Hide person with patch |
| 2020 | Hoory et al. — Dynamic multi-patch car attack |
| 2021 | Zolfi et al. — Translucent lens patch; Hu et al. — Naturalistic GAN patch |
| 2024 | Schack et al. — Real-world patch robustness analysis |
| 2025 | Gala et al. — YOLOv5+ GAN patch attacks; Liang et al. — Adv. camouflage patch (IJCAI 2025) |

## References (from PDF)

1. Thys et al. (2019) — https://arxiv.org/abs/1904.08653
2. Brown et al. (2017) — https://arxiv.org/abs/1712.09665
3. Hu et al. (2021) — https://openaccess.thecvf.com/content/ICCV2021/papers/Hu_Naturalistic_Physical_Adversarial_Patch_for_Object_Detectors_ICCV_2021_paper.pdf
4. Schack et al. (2024) — https://arxiv.org/html/2410.19863v2
5. Zolfi et al. (2021) — https://openaccess.thecvf.com/content/CVPR2021/papers/Zolfi_The_Translucent_Patch_A_Physical_and_Universal_Attack_on_Object_CVPR_2021_paper.pdf
6. Liu et al. / DPatch (2019) — https://arxiv.org/abs/1806.02299
7. Gala et al. (2025) — https://link.springer.com/article/10.1007/s10207-025-01067-3
8. Hoory et al. (2020) — https://arxiv.org/abs/2010.13070
9. AdvLogo / Bomingmiao — https://github.com/Bomingmiao/Advlogo
10. TPatch / USSLab — https://github.com/usslab/tpatch
