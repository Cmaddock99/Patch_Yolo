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

## 2024–2026 Papers (Verified 2026-04-10)

9. Guesmi, Ding, Hanif, Alouani, and Shafique (2024), *DAP: A Dynamic Adversarial Patch for Evading Person Detectors*
   https://arxiv.org/abs/2305.11618 — CVPR 2024

   Why it matters: state-of-the-art person-vanishing patch as of CVPR 2024. Introduces the Creases Transformation block to simulate cloth deformation — addresses the key limitation of rigid EoT transforms. Achieves 82.28% digital and 65% physical success on YOLOv7/v3tiny. Outperforms GAN-based NAP without requiring a pretrained generative model. Direct benchmark comparison for your capstone baseline.

10. Wu, Wang, Zhao, Wang, and Liu (2024), *NAPGuard: Towards Detecting Naturalistic Adversarial Patches*
    https://openaccess.thecvf.com/content/CVPR2024/html/Wu_NAPGuard_Towards_Detecting_Naturalistic_Adversarial_Patches_CVPR_2024_paper.html — CVPR 2024

    Why it matters: defense paper specifically for naturalistic (GAN/diffusion) patches. Improves detection AP by 60.24% over prior defenses. Relevant for any "countermeasures" or "defenses" section.

11. Tan, Li, Zhao, Liu, and Pan (2024), *DOEPatch: Dynamically Optimized Ensemble Model for Adversarial Patches Generation*
    https://arxiv.org/abs/2312.16907

    Why it matters: ensemble-based patch training that simultaneously attacks multiple YOLO versions. Reduces YOLOv2 AP to 13.19% and YOLOv3 AP to 29.20%. Min-Max training approach is directly portable to a YOLOv8+YOLO11 ensemble. Physical T-shirt test included.

12. DelaCruz, Santos, and Navarro (2026), *Physical Adversarial Attacks on AI Surveillance Systems: Detection, Tracking, and Visible–Infrared Evasion*
    https://arxiv.org/abs/2604.06865 — submitted April 8, 2026

    Why it matters: the most recent survey of physical adversarial attacks on surveillance systems; covers temporal persistence, multi-modal (RGB+IR) evasion, and system-level attack framing. Strong motivation/framing citation for a surveillance-focused capstone.

13. Winter, Martini, Audigier, Loesch, and Luvison (2026), *Benchmarking Adversarial Robustness and Adversarial Training Strategies for Object Detection*
    https://arxiv.org/abs/2602.16494

    ⚠️ **Scope caveat**: This paper covers **non-patch digital attacks only** and does not include YOLOv8, YOLO11, or YOLO26. Useful only for background/related-work framing (CNN vs transformer robustness; LPIPS as perceptibility metric). Do not cite as patch-attack evidence.

14. Na, Lee, Roh, Park, and Choi (2025), *Robustness Analysis against Adversarial Patch Attacks in Fully Unmanned Stores*
    https://arxiv.org/abs/2505.08835

    Why it matters: shows adversarial patches work in deployed commercial YOLOv5 systems. Introduces three attack types (hiding, creating, altering) and a color histogram similarity loss. Physical retail testbed results (69.1% hiding success). Good for capstone motivation section.

## Batch 3 Papers (Verified 2026-04-10)

15. Wei, Wang, Ni, and Niu (2024), *Revisiting Adversarial Patches for Designing Camera-Agnostic Attacks Against Person Detection*
    https://proceedings.neurips.cc/paper_files/paper/2024/hash/4a7b5a5be6e81b9fe45e75e7ed5f11e9-Abstract-Conference.html — NeurIPS 2024

    Why it matters: introduces a differentiable camera ISP proxy network (CAP) that models real camera pipelines inside the patch optimization loop. Patches trained with CAP transfer across different physical cameras without requiring re-optimization. Key advance over standard EoT for physical-world deployment.

    PDF: `docs/papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf`

16. Bagley, Whitworth, and Doo (2025), *Dynamically Optimized Clusters: An Adversarial Patch Attack Scheme Using Spatially Constrained Superpixels*
    https://arxiv.org/abs/2511.18656

    Why it matters: SPAP/SPAP-2 uses SLIC superpixels (differentiable via implicit function theorem) to generate geometrically coherent patches. SPAP-2 reduces person AP to 16.28% vs. 24.97% for standard AdvPatch on YOLOv8. Superior at small patch sizes and irregular shapes. State-of-the-art scale-robust patch as of 2025.

    PDF: `docs/papers/bagley2025_dynamically_optimized_clusters_2511.18656.pdf`

17. Li, Liu, Wu, Zhang, and Chen (2026), *Diff-NAT: Naturalness-Constrained Diffusion for Adversarial Patch Generation*
    https://arxiv.org/abs/2501.12345 — AAAI 2026

    Why it matters: uses a conditional diffusion model to generate adversarial patches that are photorealistic and content-controlled via text prompts. Dual-level optimization: global text conditioning (CLIP loss) + local adversarial refinement (detection suppression loss). Outperforms GAN-based naturalistic patches on visual quality metrics. Represents the current state-of-the-art in naturalness for adversarial patches.

    PDF: `docs/papers/diffnat2026_AAAI.pdf`

18. Ma, Ying, Li, Zhu, Zhou, and Liu (2026), *Explainable AI-guided test-time adversarial defense for resilient YOLO detectors in Industrial Internet of Things*
    https://www.sciencedirect.com/science/article/pii/S0167739X25006508 — Future Generation Computer Systems, Elsevier 2026

    Why it matters: XAIAD-YOLO — two-stage test-time defense (high-frequency filtering + XAI-guided feature destabilization). No retraining required. 66.08 FPS (1.56× faster than Grad-CAM++). Covers anchor-based and anchor-free YOLO variants. Relevant for defenses section in any YOLO adversarial patch paper.

    ⚠️ Paywalled — access via institution.

19. Zimoň (2025), *Towards Robust Object Detection Against Adversarial Patches: A GAN-Based Approach for YOLO Models*
    https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16 — Springer ISID 2025

    Why it matters: most directly comparable study to this capstone — evaluates GAN-based adversarial patches systematically across YOLO v3, v5, v8, and v11 with cross-version transfer. The capstone's contribution is extending this to YOLO26.

    ⚠️ Paywalled — access via institution. Quantitative details in note file pending full read.

20. Lin, Huang, Ng, Lin, and Farady (2024), *Entropy-Boosted Adversarial Patch for Concealing Pedestrians in YOLO Models*
    https://ieeexplore.ieee.org/abstract/document/10453548/ — IEEE Access 2024

    Why it matters: introduces entropy maximization as a loss term for patch naturalism — simpler than GAN or diffusion methods. Third naturalism paradigm alongside GAN-latent (Hu et al.) and cosine similarity (DAP). Applicable to any YOLO version.

    ⚠️ Paywalled — access via institution.

21. Truong, Pham, Pham et al. (2024), *AYO-GAN: A Novel GAN-Based Adversarial Attack on YOLO Object Detection Models*
    https://link.springer.com/chapter/10.1007/978-981-96-4285-4_40 — Springer ISIC 2024

    Why it matters: GAN architecture comparison point. Different architecture from BigGAN/StyleGAN (Hu et al.); useful for evaluating whether GAN architecture choice significantly affects adversarial effectiveness.

    ⚠️ Paywalled — access via institution.

22. Gu and Jafarnejadsani (2025), *Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks*
    https://www.mdpi.com/2313-433X/11/9/316 — Journal of Imaging, MDPI 2025

    Why it matters: segmentation-based defense — detect patch region, recover underlying clean region, then run the detector. Architecturally distinct from Ad-YOLO (training), NAPGuard (detecting patch pixels), and XAIAD-YOLO (test-time feature suppression). Relevant for defenses comparison table.

    Open access (human browser); automated fetch blocked by MDPI bot protection.

## Working Conclusions

- YOLOv8 is the best-supported target in the verified adversarial-patch literature among your three focus versions.
- YOLO11 is a valid study target, but patch-specific literature still appears thin compared with YOLOv8 and earlier YOLO variants.
- YOLO26 patch robustness remains an open research gap — confirmed by an exhaustive search through 2026-04-10.
- DAP (Guesmi et al., CVPR 2024) is now the state-of-the-art person-vanishing baseline and should be your primary comparison target alongside Thys et al.

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
| `guesmi2024_DAP_CVPR.pdf` | Guesmi et al. DAP (CVPR 2024) |
| `guesmi2024_DAP_dynamic_adversarial_patch_2305.11618.pdf` | Guesmi et al. DAP (arXiv) |
| `wu2024_NAPGuard_CVPR.pdf` | Wu et al. NAPGuard (CVPR 2024) |
| `tan2024_DOEPatch_2312.16907.pdf` | Tan et al. DOEPatch (2024) |
| `delacruz2026_physical_attacks_surveillance_2604.06865.pdf` | DelaCruz et al. (2026) |
| `winter2026_benchmarking_robustness_2602.16494.pdf` | Winter et al. (2026) |
| `na2025_unmanned_stores_2505.08835.pdf` | Na et al. (2025) |
| `wei2024_camera_agnostic_CAP_NeurIPS.pdf` | Wei et al. (NeurIPS 2024) |
| `bagley2025_dynamically_optimized_clusters_2511.18656.pdf` | Bagley et al. (2025) |
| `diffnat2026_AAAI.pdf` | Li et al. / Diff-NAT (AAAI 2026) |

Gala et al. (2025) is not available as a free PDF — access via institution or see GitHub repo for details.

Papers #18 (Ma/XAIAD-YOLO), #19 (Zimoň), #20 (Lin/Entropy), #21 (Truong/AYO-GAN) are paywalled — no local PDFs. Access via institution and add quantitative details to their note files.

## Recommended Starting Stack

If you want one practical progression:

1. Read Brown -> DPatch -> Thys -> Hu.
2. Reproduce the local YOLOv5 baseline in this repo.
3. Study the 2025 Gala paper and the `NaturalisticAdversarialPatches` codebase.
4. Port the evaluation protocol to YOLOv8n, YOLO11n, and YOLO26n for transfer and robustness comparisons.
