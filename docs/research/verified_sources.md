# Verified Sources for YOLO Adversarial Patch Study

This file is the checked bibliography for the repo as of 2026-04-10. It is intentionally narrower than the imported knowledge-base markdown.

Use this file when you need sources that were explicitly verified during setup.

## Core Patch Papers

1. Brown et al. (2017), *Adversarial Patch*
   https://arxiv.org/abs/1712.09665

   Why it matters: the foundational universal, printable patch paper. It is classifier-focused, but it establishes the patch threat model and physical-world framing.

2. Liu et al. (2018), *DPatch: An Adversarial Patch Attack on Object Detectors*
   https://arxiv.org/abs/1806.02299

   Why it matters: one of the key detector-specific patch papers and explicitly relevant to YOLO.

   Reference implementation:
   https://github.com/veralauee/DPatch

3. Thys, Van Ranst, and Goedemé (2019), *Fooling automated surveillance cameras: adversarial patches to attack person detection*
   https://arxiv.org/abs/1904.08653

   Why it matters: directly relevant if your capstone centers on hiding people from YOLO-based surveillance pipelines.

   Codebase linked to the paper:
   https://gitlab.com/EAVISE/adversarial-yolo

4. Huang et al. (2019), *Universal Physical Camouflage Attacks on Object Detectors*
   https://arxiv.org/abs/1909.04326

   Why it matters: strong physical-world detector paper with deformation-aware transformations and object-detector-specific attack design.

5. Hu et al. (2021), *Naturalistic Physical Adversarial Patch for Object Detectors*
   https://openaccess.thecvf.com/content/ICCV2021/html/Hu_Naturalistic_Physical_Adversarial_Patch_for_Object_Detectors_ICCV_2021_paper.html

   Why it matters: important bridge from raw pixel patches to more realistic, GAN-constrained patches.

## Modern Ultralytics YOLO Sources

6. Gala, Molleda, and Usamentiaga (2025), *Evaluating the Impact of Adversarial Patch Attacks on YOLO Models and the Implications for Edge AI Security*
   https://link.springer.com/article/10.1007/s10207-025-01067-3

   Why it matters: this is the strongest directly relevant paper I verified for modern Ultralytics YOLO models. It evaluates naturalistic patches on YOLOv5, YOLOv8, YOLOv9, and YOLOv10.

   Official code:
   https://github.com/Bimo99B9/NaturalisticAdversarialPatches

7. Ultralytics YOLOv8 docs
   https://docs.ultralytics.com/models/yolov8/

   Why it matters: official model reference for the YOLOv8 family you want to study.

8. Ultralytics YOLO11 docs
   https://docs.ultralytics.com/models/yolo11/

   Why it matters: confirms YOLO11 is an official Ultralytics model family and documents released weights, supported tasks, and benchmark tables.

9. Ultralytics YOLO26 docs
   https://docs.ultralytics.com/models/yolo26/

   Why it matters: confirms YOLO26 is now an official Ultralytics model family with end-to-end NMS-free inference, which may change patch transfer behavior relative to earlier YOLO generations.

6. Zolfi, Kravchik, Elovici, and Shabtai (2021), *The Translucent Patch: A Physical and Universal Attack on Object Detectors*
   https://openaccess.thecvf.com/content/CVPR2021/html/Zolfi_The_Translucent_Patch_A_Physical_and_Universal_Attack_on_Object_CVPR_2021_paper.html
   arXiv: https://arxiv.org/abs/2012.12528

   Why it matters: unique approach — transparent film on camera lens hides a target class while preserving others. Achieves 42.27% physical fooling rate that closely matches the digital result (42.47%), demonstrating real-world transferability. Useful for class-selective loss design (ℓuntargeted_conf term).

7. Hoory, Shapira, Shabtai, and Elovici (2020), *Dynamic Adversarial Patch for Evading Object Detection Models*
   https://arxiv.org/abs/2010.13070

   Why it matters: addresses multi-angle robustness via dynamic patch switching. Key finding: patches trained for YOLOv2 transfer poorly to YOLOv3 (10–14%) and not at all to R-CNN architectures. Highlights YOLO-family specificity of patches.

8. Schack, Petrovic, and Saukh (2024), *Breaking the Illusion: Real-world Challenges for Adversarial Patches in Object Detection*
   https://arxiv.org/abs/2410.19863

   Why it matters: critical read before making any physical-world claims. Documents the digital-to-physical gap: rotation >20° kills effectiveness, brightness increase causes up to 64% performance discrepancy, hue shifts 200–300° render patches ineffective. Tested on YOLOv3 and YOLOv5.

## Working Conclusions

- YOLOv8 is the best-supported target in the verified adversarial-patch literature among your three focus versions.
- YOLO11 is a valid study target, but patch-specific literature still appears thin compared with YOLOv8 and earlier YOLO variants.
- I did not verify a strong, dedicated adversarial-patch paper for YOLO26 during setup. For now, treat YOLO26 patch robustness as an open research gap and a strong capstone angle.

## Papers with Local PDFs (docs/papers/)

| Filename | Paper |
|---|---|
| `brown2017_adversarial_patch_1712.09665.pdf` | Brown et al. (2017) |
| `liu2019_dpatch_1806.02299.pdf` | Liu et al. / DPatch (2019) |
| `thys2019_fooling_surveillance_1904.08653.pdf` | Thys et al. (2019) |
| `hoory2020_dynamic_patch_2010.13070.pdf` | Hoory et al. (2020) |
| `hu2021_naturalistic_patch_ICCV.pdf` | Hu et al. (2021) ICCV |
| `zolfi2021_translucent_patch_2012.12528.pdf` | Zolfi et al. (2021) arXiv |
| `zolfi2021_translucent_patch_CVPR.pdf` | Zolfi et al. (2021) CVPR final |
| `schack2024_real_world_challenges_2410.19863.pdf` | Schack et al. (2024) |

Gala et al. (2025) is not available as a free PDF — access via institution or see GitHub repo for details.

## Recommended Starting Stack

If you want one practical progression:

1. Read Brown -> DPatch -> Thys -> Hu.
2. Reproduce the local YOLOv5 baseline in this repo.
3. Study the 2025 Gala paper and the `NaturalisticAdversarialPatches` codebase.
4. Port the evaluation protocol to YOLOv8n, YOLO11n, and YOLO26n for transfer and robustness comparisons.
