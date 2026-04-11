# Truong et al. (2025) — AYO-GAN

## Citation

- Title: *AYO-GAN: A Novel GAN-Based Adversarial Attack on YOLO Object Detection Models*
- Authors: Phi Ho Truong, Ngoc Minh Pham, Duy Trung Pham, Nhat Hai Nguyen
- Affiliations: Academy of Cryptography Techniques, Hanoi; Hanoi University of Science and Technology
- Venue / Year: SOICT 2024 (International Symposium on Information and Communication Technology), published April 26, 2025
- Book Series: Communications in Computer and Information Science (CCIS), vol. 2351
- Publisher: Springer, Singapore
- DOI: 10.1007/978-981-96-4285-4_40
- Print ISBN: 978-981-96-4284-7 / Online ISBN: 978-981-96-4285-4
- URL: https://doi.org/10.1007/978-981-96-4285-4_40
- Citations: 2 (as of April 2026)
- Funding: VINIF Master/PhD Scholarship VINIF.2024.TS.071
- PDF: Not freely available — ILL request needed via CSUSM

## Problem

- What threat model is assumed? White-box adversarial perturbation (not a localized patch — full-image GAN-generated perturbation) targeting YOLO object detectors.
- What detector or classifier is attacked? YOLO family (YOLOv5 cited via Jocher et al. 2022; YOLOv8 referenced via Sohan et al. 2024)
- What is the attack goal? Generate adversarial perturbations that cause misclassification/missed detections while remaining perceptually similar to the clean image (high SSIM).

## Method

- Patch type: Full-image GAN-generated adversarial perturbation (not a localized printed patch)
- Optimization method: Generative Adversarial Network — generator produces perturbations, discriminator enforces perceptual quality
- Loss terms: Adversarial attack loss (ASR-maximizing) + perceptual quality loss (SSIM-preserving)
- Key GAN design: Distinct from BigGAN/StyleGAN (Hu et al.) — AYO-GAN generates perturbations rather than naturalistic patch textures
- Transformations / EoT details: Not described in available metadata
- Physical-world considerations: Not tested physically — digital-only evaluation
- Dataset: COCO (Microsoft COCO: Common Objects in Context, Lin et al. 2014)
- Comparison baseline: Xiao et al.'s adversarial perturbation method (Inf. Sci. 2020 and Pattern Recogn. 2021)

## Experimental Setup

- Dataset: COCO
- Target classes: Multiple COCO classes (object detection, not person-specific)
- Model versions: YOLO (specific version not confirmed from metadata — likely YOLOv5 based on citations)
- Metrics: SSIM (Structural Similarity Index), ASR (Attack Success Rate)

## Results

- **SSIM: 0.936** (higher = more perceptually similar to clean image; their baseline Xiao et al. achieved 0.842)
- **ASR: 22.25%** (their baseline Xiao et al. achieved 12.67%)
- What worked best: GAN-generated perturbations maintain high perceptual quality while achieving better attack rates than prior gradient-search methods.
- What failed or stayed weak: 22.25% ASR is modest compared to patch-based methods (your v8 project achieves 85%) — GAN perturbation approach trades attack strength for perceptual quality.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Low-moderate. Tests YOLO but likely YOLOv5; full-image perturbation not comparable to your localized patch approach.
- Direct relevance to YOLO11: Low.
- Direct relevance to YOLO26: Low.
- What I can cite: GAN architecture comparison data point. AYO-GAN's 22.25% ASR confirms that GAN perturbation methods significantly underperform localized patch methods (your 85%). Useful for the methods comparison table in the capstone.
- What I can cite for perceptual quality: SSIM 0.936 establishes a GAN-based perceptual quality benchmark — relevant if discussing patch naturalism via GAN vs. diffusion (Diff-NAT) vs. entropy (Lin et al.).

## Key Numbers for Write-Up

| Method | ASR | SSIM | Notes |
|---|---|---|---|
| Xiao et al. (2020/2021) baseline | 12.67% | 0.842 | Gradient-search perturbation |
| **AYO-GAN (Truong 2025)** | **22.25%** | **0.936** | GAN perturbation, COCO |
| Your project — v8n direct | 85.0% | N/A | Localized patch, person class |
| Your project — v11n direct | 78.8% | N/A | Localized patch, person class |

The gap between 22% and 85% reflects full-image perturbation vs. localized high-intensity patch — not a fair comparison, but useful framing.

## GAN Architecture Context

AYO-GAN fits into the GAN-based adversarial attack landscape as follows:

- **Hu et al. ICCV 2021 (Naturalistic Patch)** — GAN constrains patch pixels to the natural image manifold; patches look like real images
- **Truong 2025 (AYO-GAN)** — GAN generates full-image perturbations; perturbed image looks similar to original (high SSIM)
- **Diff-NAT AAAI 2026** — diffusion model generates photorealistic patch textures via text prompts; strongest naturalism
- **Lin et al. IEEE Access 2024 (Entropy)** — no GAN; entropy maximization for naturalism; simpler approach

AYO-GAN is architecturally distinct from all three — it is a perturbation model rather than a patch model.

## Reference List (Full — From Paper)

1. Ai et al. (2021) — adversarial perturbation in remote sensing — Appl. Soft Comput. 105, 107252
2. Athira et al. (2021) — underwater object detection YOLOv3 — ICACCS 2021
3. Chen & Hsieh (2022) — *Adversarial Robustness for Machine Learning* — Academic Press
4. Chow et al. (2020) — understanding object detection through adversarial lens — ESORICS 2020, LNCS vol. 12309 pp. 460–481
5. Goodfellow, Shlens & Szegedy (2014) — explaining and harnessing adversarial examples — arXiv:1412.6572
6. He, Zhang, Ren & Sun (2016) — deep residual learning — CVPR 2016 pp. 770–778
7. Hossain et al. (2024) — review on attacks against AI — Control Syst. Optim. Lett. 2(1) pp. 52–59
8. Hu et al. (2020) — FairNN-conjoint learning — DS 2020 pp. 581–595
9. Im Choi & Tian (2022) — adversarial attack and defense of YOLO in autonomous driving — IEEE IV 2022 pp. 1011–1017
10. Irfan et al. (2021) — review on adversarial attacks — ICAI 2021 pp. 91–96
11. Jocher et al. (2022) — ultralytics/yolov5: v7.0 — Zenodo
12. Keleş et al. (2021) — PSNR computation — PCS 2021 pp. 1–5
13. Kurakin et al. (2018) — adversarial examples in the physical world — AI Safety and Security pp. 99–112
14. Liang (2022) — confusion matrix — POGIL Activity Clearinghouse 3(4)
15. Lin et al. (2014) — Microsoft COCO — ECCV 2014 pp. 740–755
16. Liu et al. (2016) — SSD: single shot multibox detector — ECCV 2016 pp. 21–37
17. Lorenz et al. (2021) — RobustBench/AutoAttack benchmark — arXiv:2112.01601
18. Miller et al. (2020) — adversarial learning targeting DNNs — Proc. IEEE 108(3) pp. 402–433
19. Mirsky (2023) — iPatch: remote adversarial patch — Cybersecurity 6(1):18
20. Mukherjee et al. (2019) — fingertip detection — Expert Syst. Appl. 136 pp. 217–229
21. Nilsson & Akenine-Möller (2020) — understanding SSIM — arXiv:2006.13846
22. Redmon (2016) — YOLO unified real-time object detection — CVPR 2016
23. Ren et al. (2016) — Faster R-CNN — IEEE TPAMI 39(6) pp. 1137–1149
24. Sohan et al. (2024) — review on YOLOv8 and advancements — ICDCI 2024 pp. 529–545
25. Wang et al. (2020) — side-aware boundary localization — ECCV 2020 pp. 403–419
26. **Xiao, Pun & Liu (2020)** — adversarial example generation with adaptive gradient search — *Inf. Sci.* 528 pp. 147–167 ← primary baseline
27. **Xiao, Pun & Liu (2021)** — fooling DNNs with adaptive object-oriented adversarial perturbation — *Pattern Recogn.* 115, 107903 ← primary baseline
28. Zhang & Ma (2022) — misleading attention and classification — Comput. Secur. 122, 102876

## Open Questions

- What YOLO version exactly? Metadata cites YOLOv5 (Jocher 2022) and YOLOv8 (Sohan 2024) — unclear which was attacked.
- Is detection suppression % reported, or only ASR? The 22.25% ASR may be class-level misclassification rate, not detection count suppression.
- Is the perturbation truly imperceptible (SSIM 0.936 is high but not perfect)?
- How does ASR change per class — is "person" tested specifically?

## TODO

- [ ] Submit ILL request for full paper — DOI: 10.1007/978-981-96-4285-4_40
- [ ] Confirm which YOLO version was the primary attack target
- [ ] Get ASR breakdown by class if available
- [ ] Clarify whether ASR = detection suppression % or classification error rate
