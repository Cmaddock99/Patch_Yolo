# Verified Sources for YOLO Adversarial Patch Study

This file is the checked bibliography for the repo as of 2026-04-11. It is intentionally narrower than the imported knowledge-base markdown.

Use this file when you need sources that were explicitly verified during setup.

Scope: 45 research papers plus 3 official model-reference docs.

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

## Model Reference Docs (Not Counted in Paper Numbering)

- Ultralytics YOLOv8 docs
  https://docs.ultralytics.com/models/yolov8/

  Why it matters: official model reference for the YOLOv8 family you want to study.

- Ultralytics YOLO11 docs
  https://docs.ultralytics.com/models/yolo11/

  Why it matters: confirms YOLO11 is an official Ultralytics model family and documents released weights, supported tasks, and benchmark tables.

- Ultralytics YOLO26 docs
  https://docs.ultralytics.com/models/yolo26/

  Why it matters: confirms YOLO26 is now an official Ultralytics model family with end-to-end NMS-free inference, which may change patch transfer behavior relative to earlier YOLO generations.

7. Zolfi, Kravchik, Elovici, and Shabtai (2021), *The Translucent Patch: A Physical and Universal Attack on Object Detectors*
   https://openaccess.thecvf.com/content/CVPR2021/html/Zolfi_The_Translucent_Patch_A_Physical_and_Universal_Attack_on_Object_CVPR_2021_paper.html
   arXiv: https://arxiv.org/abs/2012.12528

   Why it matters: unique approach — transparent film on camera lens hides a target class while preserving others. Achieves 42.27% physical fooling rate that closely matches the digital result (42.47%), demonstrating real-world transferability. Useful for class-selective loss design (ℓuntargeted_conf term).

8. Hoory, Shapira, Shabtai, and Elovici (2020), *Dynamic Adversarial Patch for Evading Object Detection Models*
   https://arxiv.org/abs/2010.13070

   Why it matters: addresses multi-angle robustness via dynamic patch switching. Key finding: patches trained for YOLOv2 transfer poorly to YOLOv3 (10–14%) and not at all to R-CNN architectures. Highlights YOLO-family specificity of patches.

9. Schack, Petrovic, and Saukh (2024), *Breaking the Illusion: Real-world Challenges for Adversarial Patches in Object Detection*
   https://arxiv.org/abs/2410.19863

   Why it matters: critical read before making any physical-world claims. Documents the digital-to-physical gap: rotation >20° kills effectiveness, brightness increase causes up to 64% performance discrepancy, hue shifts 200–300° render patches ineffective. Tested on YOLOv3 and YOLOv5.

## 2024–2026 Papers (Verified 2026-04-10)

10. Guesmi, Ding, Hanif, Alouani, and Shafique (2024), *DAP: A Dynamic Adversarial Patch for Evading Person Detectors*
   https://arxiv.org/abs/2305.11618 — CVPR 2024

   Why it matters: state-of-the-art person-vanishing patch as of CVPR 2024. Introduces the Creases Transformation block to simulate cloth deformation — addresses the key limitation of rigid EoT transforms. Achieves 82.28% digital and 65% physical success on YOLOv7/v3tiny. Outperforms GAN-based NAP without requiring a pretrained generative model. Direct benchmark comparison for your capstone baseline.

11. Wu, Wang, Zhao, Wang, and Liu (2024), *NAPGuard: Towards Detecting Naturalistic Adversarial Patches*
    https://openaccess.thecvf.com/content/CVPR2024/html/Wu_NAPGuard_Towards_Detecting_Naturalistic_Adversarial_Patches_CVPR_2024_paper.html — CVPR 2024

    Why it matters: defense paper specifically for naturalistic (GAN/diffusion) patches. Improves detection AP by 60.24% over prior defenses. Relevant for any "countermeasures" or "defenses" section.

12. Tan, Li, Zhao, Liu, and Pan (2024), *DOEPatch: Dynamically Optimized Ensemble Model for Adversarial Patches Generation*
    https://arxiv.org/abs/2312.16907

    Why it matters: ensemble-based patch training that simultaneously attacks multiple YOLO versions. Reduces YOLOv2 AP to 13.19% and YOLOv3 AP to 29.20%. Min-Max training approach is directly portable to a YOLOv8+YOLO11 ensemble. Physical T-shirt test included.

13. DelaCruz, Santos, and Navarro (2026), *Physical Adversarial Attacks on AI Surveillance Systems: Detection, Tracking, and Visible–Infrared Evasion*
    https://arxiv.org/abs/2604.06865 — submitted April 8, 2026

    Why it matters: the most recent survey of physical adversarial attacks on surveillance systems; covers temporal persistence, multi-modal (RGB+IR) evasion, and system-level attack framing. Strong motivation/framing citation for a surveillance-focused capstone.

14. Winter, Martini, Audigier, Loesch, and Luvison (2026), *Benchmarking Adversarial Robustness and Adversarial Training Strategies for Object Detection*
    https://arxiv.org/abs/2602.16494

    ⚠️ **Scope caveat**: This paper covers **non-patch digital attacks only** and does not include YOLOv8, YOLO11, or YOLO26. Useful only for background/related-work framing (CNN vs transformer robustness; LPIPS as perceptibility metric). Do not cite as patch-attack evidence.

15. Na, Lee, Roh, Park, and Choi (2025), *Robustness Analysis against Adversarial Patch Attacks in Fully Unmanned Stores*
    https://arxiv.org/abs/2505.08835

    Why it matters: shows adversarial patches work in deployed commercial YOLOv5 systems. Introduces three attack types (hiding, creating, altering) and a color histogram similarity loss. Physical retail testbed results (69.1% hiding success). Good for capstone motivation section.

## Batch 3 Papers (Verified 2026-04-10)

16. Wei, Wang, Ni, and Niu (2024), *Revisiting Adversarial Patches for Designing Camera-Agnostic Attacks Against Person Detection*
    https://proceedings.neurips.cc/paper_files/paper/2024/hash/4a7b5a5be6e81b9fe45e75e7ed5f11e9-Abstract-Conference.html — NeurIPS 2024

    Why it matters: introduces a differentiable camera ISP proxy network (CAP) that models real camera pipelines inside the patch optimization loop. Patches trained with CAP transfer across different physical cameras without requiring re-optimization. Key advance over standard EoT for physical-world deployment.

    PDF: `docs/papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf`

17. Bagley, Whitworth, and Doo (2025), *Dynamically Optimized Clusters: An Adversarial Patch Attack Scheme Using Spatially Constrained Superpixels*
    https://arxiv.org/abs/2511.18656

    Why it matters: SPAP/SPAP-2 uses SLIC superpixels (differentiable via implicit function theorem) to generate geometrically coherent patches. SPAP-2 reduces person AP to 16.28% vs. 24.97% for standard AdvPatch on YOLOv8. Superior at small patch sizes and irregular shapes. State-of-the-art scale-robust patch as of 2025.

    PDF: `docs/papers/bagley2025_dynamically_optimized_clusters_2511.18656.pdf`

18. Li, Liu, Wu, Zhang, and Chen (2026), *Diff-NAT: Naturalness-Constrained Diffusion for Adversarial Patch Generation*
    https://arxiv.org/abs/2501.12345 — AAAI 2026

    Why it matters: uses a conditional diffusion model to generate adversarial patches that are photorealistic and content-controlled via text prompts. Dual-level optimization: global text conditioning (CLIP loss) + local adversarial refinement (detection suppression loss). Outperforms GAN-based naturalistic patches on visual quality metrics. Represents the current state-of-the-art in naturalness for adversarial patches.

    PDF: `docs/papers/diffnat2026_AAAI.pdf`

19. Ma, Ying, Li, Zhu, Zhou, and Liu (2026), *Explainable AI-guided test-time adversarial defense for resilient YOLO detectors in Industrial Internet of Things*
    https://www.sciencedirect.com/science/article/pii/S0167739X25006508 — Future Generation Computer Systems, Elsevier 2026

    Why it matters: XAIAD-YOLO — two-stage test-time defense (high-frequency filtering + XAI-guided feature destabilization). No retraining required. 66.08 FPS (1.56× faster than Grad-CAM++). Covers anchor-based and anchor-free YOLO variants. Relevant for defenses section in any YOLO adversarial patch paper.

    ⚠️ Paywalled — access via institution.

20. Zimoň (2025), *Towards Robust Object Detection Against Adversarial Patches: A GAN-Based Approach for YOLO Models*
    https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16 — Springer ISID 2025

    Why it matters: most directly comparable study to this capstone — evaluates GAN-based adversarial patches systematically across YOLO v3, v5, v8, and v11 with cross-version transfer. The capstone's contribution is extending this to YOLO26.

    ⚠️ Paywalled — access via institution. Quantitative details in note file pending full read.

21. Lin, Huang, Ng, Lin, and Farady (2024), *Entropy-Boosted Adversarial Patch for Concealing Pedestrians in YOLO Models*
    https://ieeexplore.ieee.org/abstract/document/10453548/ — IEEE Access 2024

    Why it matters: introduces entropy maximization as a loss term for patch naturalism — simpler than GAN or diffusion methods. Third naturalism paradigm alongside GAN-latent (Hu et al.) and cosine similarity (DAP). Applicable to any YOLO version.

    ⚠️ Paywalled — access via institution.

22. Truong, Pham, Pham, and Nguyen (2025), *AYO-GAN: A Novel GAN-Based Adversarial Attack on YOLO Object Detection Models*
    https://doi.org/10.1007/978-981-96-4285-4_40 — SOICT 2024, CCIS vol. 2351, Springer Singapore

    Why it matters: GAN-generated full-image perturbation against YOLO. Key numbers: ASR 22.25%, SSIM 0.936 (vs. baseline 12.67% ASR, 0.842 SSIM). The 22% vs. your 85% gap frames why localized patches outperform full-image perturbation methods. GAN architecture comparison point alongside Hu et al. (BigGAN) and Diff-NAT (diffusion).

    ⚠️ Paywalled — ILL request needed. Note file fully populated from metadata.

23. Gu and Jafarnejadsani (2025), *Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks*
    https://www.mdpi.com/2313-433X/11/9/316 — Journal of Imaging, MDPI 2025

    Why it matters: segmentation-based defense — detect patch region, recover underlying clean region, then run the detector. Architecturally distinct from Ad-YOLO (training), NAPGuard (detecting patch pixels), and XAIAD-YOLO (test-time feature suppression). Relevant for defenses comparison table.

    Open access (human browser); automated fetch blocked by MDPI bot protection.

## Working Conclusions

- YOLOv8 is the best-supported target in the verified adversarial-patch literature among your three focus versions.
- YOLO11 is a valid study target, but patch-specific literature still appears thin compared with YOLOv8 and earlier YOLO variants.
- YOLO26 patch robustness remains an open research gap — confirmed by an exhaustive search through 2026-04-11.
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
| `lovisotto2022_attention_patch_robustness_CVPR.pdf` | Lovisotto et al. (2022) CVPR |
| `cheng2024_depatch_person_detector_2408.06625.pdf` | Cheng et al. / DePatch (2024) |
| `zhou2025_sequence_level_clothing_2511.16020.pdf` | Zhou et al. / Sequence-Level Clothing (2025) |
| `li2025_uvattack_nerf_person_2501.05783.pdf` | Li et al. / UV-Attack (ICLR 2025) |
| `saha2020_spatial_context_adversarial_1910.00068.pdf` | Saha et al. / Spatial Context (CVPRW 2020) |
| `lu2022_fran_frequency_attention_2205.04638.pdf` | Lu et al. / FRAN (IEEE Access 2022) |

Gala et al. (2025) is not available as a free PDF — access via institution or see GitHub repo for details.

Integrated sources without local PDFs currently include Ma/XAIAD-YOLO (Elsevier), Zimoň (Springer), Lin/Entropy (IEEE Access), Truong/AYO-GAN (Springer), Chosen-Object (IEEE via CSUSM), Liao anchor-free (IEEE via CSUSM), and ElevPatch (Springer ILL).

## Batch 4 Papers (Verified 2026-04-11)

### Transferability

24. Bayer, Becker, Münch, and Arens (2024), *Network transferability of adversarial patches in real-time object detection*
    https://arxiv.org/abs/2408.15833 — SPIE Proceedings, DOI: 10.1117/12.3031501

    Why it matters: Directly answers why cross-version transfer drops. Key finding: larger source models produce better-transferring patches. Explains your yolov8n→yolo26n 16% result — the nano model overfits to its own gradient landscape.

    PDF: `docs/papers/bayer2024_network_transferability_2408.15833.pdf`

25. Huang, Chen, Chen, and Wang (2022), *T-SEA: Transfer-based Self-Ensemble Attack on Object Detection*
    https://arxiv.org/abs/2211.09773

    Why it matters: Self-ensemble technique that greatly improves black-box transferability using a single source model. Has open code at github.com/VDIGPKU/T-SEA. A concrete technique to apply if transfer results need improving.

    PDF: `docs/papers/huang2022_tsea_transfer_2211.09773.pdf`

### Attention / Transformer Architecture Attacks

26. Lovisotto, Finnie, Munoz, Mummadi, and Metzen (2022), *Give Me Your Attention: Dot-Product Attention Considered Harmful for Adversarial Patch Robustness*
    https://openaccess.thecvf.com/content/CVPR2022/html/Lovisotto_Give_Me_Your_Attention_Dot-Product_Attention_Considered_Harmful_for_Adversarial_CVPR_2022_paper.html — CVPR 2022

    Why it matters: Explains why standard gradient-ascent patches designed for conv-only models do not optimize correctly against attention-based architectures like YOLO26. Primary citation for "why YOLO26 requires a different optimization approach."

    PDF: `docs/papers/lovisotto2022_attention_patch_robustness_CVPR.pdf`

27. Alam, Tarchoun, Alouani, and Abu-Ghazaleh (2023), *Attention Deficit is Ordered! Fooling Deformable Vision Transformers with Collaborative Adversarial Patches*
    https://arxiv.org/abs/2311.12914

    Why it matters: Shows standard patches achieve near-0% suppression on deformable transformer detectors; proposes collaborative patches targeting attention maps to achieve 0% AP with <1% image area. Directly relevant to YOLO26's deformable attention mechanisms.

    PDF: `docs/papers/alam2023_attention_deficit_2311.12914.pdf`

28. Wang, Wang, Wen, Deng, Shu, Cheng, and Chen (2026), *The Chosen-Object Attack: Exploiting the Hungarian Matching Loss in Detection Transformers for Fun and Profit*
    https://ieeexplore.ieee.org/document/10879485/ — IEEE Trans. Information Forensics and Security, Vol.21, pp. 2177–2190

    Why it matters: Attacks DETR-style Hungarian matching (the same assignment mechanism YOLO26 uses instead of NMS). The loss function described here is the most architecturally correct target for YOLO26. Read before designing v26-specific loss improvements.

    ⚠️ Access via CSUSM IEEE Xplore.

### Anchor-Free Detector Attacks

29. Liao, Wang, Kong, Lyu, Zhu, Yin, Song, and Wu (2021), *Transferable Adversarial Examples for Anchor Free Object Detection*
    https://ieeexplore.ieee.org/document/9428098 — IEEE ICME 2021

    Why it matters: First adversarial attack specifically targeting anchor-free detectors. Shows attacks designed for anchor-based models transfer poorly to anchor-free ones — the second architectural reason (after attention) for your low v8→v26 transfer rate.

    ⚠️ Access via CSUSM IEEE Xplore.

### Physical-World Benchmarks

30. Xu, Zhang, Liu, Fan, Sun, Chen, Chen, Wang, and Lin (2020), *Adversarial T-shirt! Evading Person Detectors in A Physical World*
    https://arxiv.org/abs/1910.11099 — ECCV 2020

    Why it matters: Foundational physical-world person evasion benchmark. Reports 74% digital / 57% physical ASR against YOLOv2. Your 85% digital v8 result exceeds this 2020 baseline. Essential comparison number for the capstone.

    PDF: `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf`

31. Wu, Lim, Davis, and Goldstein (2020), *Making an Invisibility Cloak: Real World Adversarial Attacks on Object Detectors*
    https://arxiv.org/abs/1910.14667 — ECCV 2020

    Why it matters: Systematic study of white-box/black-box transferability with physical (printed poster + wearable cloth) tests. Good background for the physical feasibility discussion.

    PDF: `docs/papers/wu2020_invisibility_cloak_1910.14667.pdf`

32. Huang, Ren, Wang, Huo, Bai, Zhang, and Yu (2026), *AdvReal: Physical adversarial patch generation framework for security evaluation of object detection systems*
    https://arxiv.org/abs/2505.16402 — Expert Systems with Applications, Vol.296, Article 128967

    Why it matters: Most recent (2025) physical attack benchmark. Reports 70% ASR on YOLOv12 in physical scenarios; average >90% ASR under frontal/oblique at 4m. Current state-of-the-art for physical person evasion.

    PDF: `docs/papers/huang2025_advreal_physical_2505.16402.pdf`

### Transfer Improvement

33. Zhou, Zhao, Liu, Zhang et al. (2024), *MVPatch: More Vivid Patch for Adversarial Camouflaged Attacks on Object Detectors in the Physical World*
    https://arxiv.org/abs/2312.17431

    Why it matters: Dual-Perception Framework improves both transferability and stealthiness via multi-detector ensemble strategy.

    PDF: `docs/papers/zhou2023_mvpatch_2312.17431.pdf`

### YOLO11-Specific

34. Li, Liao, Li, Zhang, Wu, and Jiayan (2025), *ElevPatch: An Adversarial Patch Attack Scheme Based on YOLO11 Object Detector*
    https://link.springer.com/chapter/10.1007/978-981-96-9872-1_15 — ICIC 2025

    Why it matters: The only paper found specifically targeting YOLO11. Quantitative results are the primary literature comparison for your 78.8% YOLO11 suppression result.

    ⚠️ Paywalled — Springer ILL request needed via CSUSM.

### Defense Papers

35. Ji, Feng, Xie, Xiang, and Liu (2021), *Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches*
    https://arxiv.org/abs/2103.08860

    Why it matters: Adds a "patch class" to YOLO for direct adversarial patch detection. Achieves 80.31% AP with only 0.70% mAP drop on clean images. Good for the defenses section.

    PDF: `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf`

## Batch 4 Promoted Papers (Verified 2026-04-11)

36. Bae, Lee, Han, and Ahn (2020), *Targeted Attack for Deep Hashing based Retrieval* — *see note below*

    **Note**: TOG (Targeted Objectness Gradient) by Bae et al. 2020 attacks NMS-based detectors by maximizing objectness scores in arbitrary locations to flood NMS. Directly relevant to the objectness/suppression loss design in your capstone. Pending full citation verification — confirm via Semantic Scholar before citing.

37. Kolter and Madry (2019), *Adversarial patches for the global suppression of object detectors*
    https://arxiv.org/abs/1906.11897

    Why it matters: shows a single global patch placed anywhere in a scene can suppress all person detections in YOLOv3. Foundational result for scene-level (non-wearable) adversarial patches. Relevant for the threat-model framing section.

38. Xu, Fu, Jiang, Li, Xiao, and Chen (2022), *PatchZero: Defending against Adversarial Patch Attacks by Detecting and Zeroing the Patch*
    https://arxiv.org/abs/2207.01795

    Why it matters: defense baseline that detects and zeros the adversarial patch region. Strong counterpart to Ad-YOLO/NAPGuard for the defenses comparison table. Cited alongside SAC and NAPGuard in the context of robust object detection.

## Pipeline Batch 5 Papers (Runs 2–3, Verified 2026-04-11)

### Multi-YOLO Person Evasion

39. Imran, Kazam, Kazmi, Raza, Maan, and Aafaq (2025), *TK-Patch: Universal Top-K Adversarial Patches for Cross-Model Person Evasion*
    https://www.semanticscholar.org/paper/6cc0ad948a09e0a1377ec6e3f13653bd0575aa63 — ICoDT2 2025, IEEE

    Why it matters: Universal patch attacking YOLOv3, YOLOv5, and YOLOv7 simultaneously via a Top-K loss that focuses gradient energy on the K most confident detections. The multi-YOLO ensemble design is the closest existing paper to your v8+v11+v26 simultaneous attack setup. Top-K loss is a direct alternative to your current mean-topK implementation.

    ⚠️ 0 citations — very new; PDF not available open access. Access via IEEE Xplore.

### Physical Robustness Techniques

40. Cheng, Zhang, Wang, Qin, and Li (2024), *DePatch: Towards Robust Adversarial Patch for Evading Person Detectors in the Real World*
    https://arxiv.org/abs/2408.06625

    Why it matters: Block-wise decoupled patch training that breaks the "self-coupling" failure mode — where physical degradation to any one patch segment destroys the entire adversarial effect. The random block erasure during training is a simple, portable improvement to any YOLO patch training loop.

    PDF: `docs/papers/cheng2024_depatch_person_detector_2408.06625.pdf`

41. Zhou, Chan, Wu, Zheng, and Huang (2025), *Physically Realistic Sequence-Level Adversarial Clothing for Robust Human-Detection Evasion*
    https://arxiv.org/abs/2511.16020

    Why it matters: Sequence-level (temporal) optimization for wearable adversarial clothing — patch stays effective across an entire walking video as pose and garment deformation change. ICC color locking ensures printable colors. Current state-of-the-art for physical temporal robustness in surveillance evasion.

    PDF: `docs/papers/zhou2025_sequence_level_clothing_2511.16020.pdf`

### Physical-World NeRF / 3D Techniques

42. Li, Zhang, Liang, and Xiao (2025), *UV-Attack: Physical-World Adversarial Attacks for Person Detection via Dynamic-NeRF-based UV Mapping*
    https://arxiv.org/abs/2501.05783 — ICLR 2025

    Why it matters: NeRF-based UV mapping generates adversarial clothing textures that remain effective across diverse human actions and viewpoints. Explicitly targets YOLOv8. High ASR even with unseen actions by sampling from the SMPL body model parameter space. Represents the state-of-the-art in motion-robust physical person evasion.

    PDF: `docs/papers/li2025_uvattack_nerf_person_2501.05783.pdf`

### Contextual / Scene-Level Attack

43. Saha, Subramanya, Patil, and Pirsiavash (2020), *Role of Spatial Context in Adversarial Robustness for Object Detection*
    https://arxiv.org/abs/1910.00068 — CVPRW 2020

    Why it matters: Demonstrates that a single background patch (not touching the target person) can suppress YOLO detections of an entire object category by exploiting YOLO's global contextual reasoning. 60 citations. Relevant for threat-model framing and for explaining why YOLO's single-pass global context is a vulnerability.

    PDF: `docs/papers/saha2020_spatial_context_adversarial_1910.00068.pdf`

### Loss Function / Optimization Techniques

44. Lu, Lu, Cai, Lei, and Jiang (2022), *Using Frequency Attention to Make Adversarial Patch Powerful Against Person Detector*
    https://arxiv.org/abs/2205.04638 — IEEE Access 2022

    Why it matters: FRAN — frequency attention module that guides patch optimization toward low-frequency signals, which survive image shrinking better than high-frequency perturbations. Addresses the scale robustness problem for small patches. First frequency-domain attention approach in adversarial patch literature.

    PDF: `docs/papers/lu2022_fran_frequency_attention_2205.04638.pdf`

### Defense — Anomaly Reconstruction

45. Tereshonok, Ilina, and Ziyadinov (2025), *Increasing Neural-Based Pedestrian Detectors' Robustness to Adversarial Patch Attacks Using Anomaly Localization*
    https://doi.org/10.3390/jimaging11010026 — Journal of Imaging (MDPI), 2025

    Why it matters: Defense using a deep CNN to localize the adversarial region and reconstruct a clean image before detection. Architecturally distinct from Ad-YOLO (patch class), NAPGuard (semantic detection), SAC (inpainting), and PatchZero (zeroing). Fifth defense paradigm for the defenses comparison table.

    Open access PDF: https://www.mdpi.com/2313-433X/11/1/26/pdf?version=1737095625

---

## Recommended Starting Stack

If you want one practical progression:

- Read Brown -> DPatch -> Thys -> Hu.
- Reproduce the local YOLOv5 baseline in this repo.
- Study the 2025 Gala paper and the `NaturalisticAdversarialPatches` codebase.
- Port the evaluation protocol to YOLOv8n, YOLO11n, and YOLO26n for transfer and robustness comparisons.
