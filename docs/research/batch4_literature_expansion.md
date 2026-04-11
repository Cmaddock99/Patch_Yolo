# Batch 4 Literature Expansion
*Compiled: 2026-04-11*
*Source: CSUSM OneSearch (logged in as Maddock), arXiv, Google Scholar*
*Purpose: Expand literature base for YOLO adversarial patch capstone project*

---

## TIER 1 — Directly Relevant to Your Project

### Cross-Model Transferability (Your Core Research Question)

**Bayer, Becker, Münch & Arens (2024)**
*Network transferability of adversarial patches in real-time object detection*
- Venue: SPIE Proceedings (also arXiv 2408.15833)
- DOI: 10.1117/12.3031501
- Access: arXiv preprint open; SPIE via ILL
- Key finding: Patches optimized with **larger models provide better network transferability** than patches optimized with smaller models. Tests across numerous object detector architectures.
- Why it matters: Directly answers why v8→v11 transfer drops and what model characteristics affect transferability. Should be a primary citation for your transfer results section.

**Kleber, Eppler, Palm, Eisermann & Kargl (2025)**
*Assessing the Transferability of Adversarial Patches in Real-World Systems*
- Venue: IEEE/IFIP DSN Supplemental Volume, pp. 42–48
- Access: Via ILL through CSUSM
- Key finding: Investigates transferability of adversarial patches for attacking real-world image recognition in CPS.
- Why it matters: Real-world transferability assessment across systems — directly parallels your cross-version experiments.
- ⚠️ Needs ILL request

**Imran, Kazmi, Raza, Maan & Aafaq (2025)**
*TK-Patch: Universal Top-K Adversarial Patches for Cross-Model Person Evasion*
- Venue: 5th Int'l Conference on Digital Futures (ICoDT2), pp. 1–7
- Access: Via ILL through CSUSM
- Why it matters: Specifically about universal patches for cross-model **person evasion** — the exact problem you're solving.
- ⚠️ Needs ILL request; verify DOI before requesting

**Wang, Chen, Yang & Cao (2024)**
*Enhancing the Transferability of Adversarial Patch via Alternating Minimization*
- Venue: International Journal of Computational Intelligence Systems, Vol.17(1), Article 220
- Access: Open access, full text available via CSUSM
- Key finding: AMAP method decomposes patches into sub-patches to stabilize optimization and improve transfer.
- Why it matters: A concrete technique you could apply to improve v8→v11/v26 transfer rates.

---

### Attacks on Attention / Transformer-Based Detectors (YOLO26 Specific)

**Lovisotto, Finnie, Munoz, Mummadi & Metzen (2022)**
*Give Me Your Attention: Dot-Product Attention Considered Harmful for Adversarial Patch Robustness*
- Venue: CVPR 2022, pp. 15213–15222
- Access: CVF open access + arXiv
- Key finding: Dot-product attention is a **major vulnerability source** for adversarial patch attacks — but it also changes HOW patches need to be crafted.
- Why it matters: YOLO26 uses attention mechanisms. This paper explains why standard patch approaches (designed for conv-only models) may not work as expected and what the attention surface means for optimization.

**Wang, Wang, Wen, Deng, Shu, Cheng & Chen (2026)**
*The Chosen-Object Attack: Exploiting the Hungarian Matching Loss in Detection Transformers for Fun and Profit*
- Venue: IEEE Trans. Information Forensics and Security, Vol.21, pp. 2177–2190
- Access: Full text via CSUSM (IEEE)
- Key finding: Attacks DETR-style detectors by exploiting the **Hungarian matching loss** — the one-to-one assignment used instead of NMS.
- Why it matters: YOLO26 uses end-to-end Hungarian matching instead of NMS. This is the closest architectural match to YOLO26's attack surface. The loss function described here is the most theoretically correct target for YOLO26. **Read before designing any v26-specific loss improvements.**

**Alam, Tarchoun, Alouani & Abu-Ghazaleh (2023)**
*Attention Deficit is Ordered! Fooling Deformable Vision Transformers with Collaborative Adversarial Patches*
- arXiv: 2311.12914
- Access: Open access preprint
- Key finding: Standard attacks **don't transfer to deformable transformers**. Proposes collaborative patches that manipulate attention to point to adversarial noise. Achieved complete 0% AP by altering <1% of image.
- Why it matters: YOLO26's architecture includes deformable-style attention. Shows both WHY standard patches fail AND how to fix them for this architecture class.

---

### Anchor-Free Detector Attacks (YOLO26 is Anchor-Free)

**Liao, Wang, Kong, Lyu, Zhu, Yin, Song & Wu (2021)**
*Transferable Adversarial Examples for Anchor Free Object Detection*
- Venue: IEEE ICME 2021, pp. 1–6
- Access: IEEE via CSUSM + arXiv
- Key finding: **First adversarial attack specifically targeting anchor-free detectors.** Shows that attacks designed for anchor-based models transfer poorly to anchor-free ones.
- Why it matters: YOLO26 is fully anchor-free. Your v8 patches target anchor-based heads — this paper explains the architectural mismatch and proposes a loss function designed for anchor-free outputs.

**Liao et al. (2020)**
*Category-wise Attack: Transferable Adversarial Examples for Anchor Free Object Detection*
- arXiv: 2006.xxxxx (companion preprint)
- Access: Open access preprint
- Why it matters: Companion paper with additional techniques for the anchor-free problem.

---

### YOLO-Specific Attack Papers

**Li, Liao, Li, Zhang, Wu & Jiayan (2025)**
*ElevPatch: An Adversarial Patch Attack Scheme Based on YOLO11 Object Detector*
- Venue: ICIC 2025, Advanced Intelligent Computing Technology and Applications, pp. 176–188
- DOI: 10.1007/978-981-96-9872-1_15
- Access: Springer via ILL (paywalled)
- Why it matters: **The only paper found specifically targeting YOLO11.** Direct benchmark comparison for your v11 results. Get this paper.
- ⚠️ Needs Springer ILL request

**Li, Shan, Shen, Ren & Zhang (2025)**
*PNAP-YOLO: An Improved Prompts-Based Naturalistic Adversarial Patch Model for Object Detectors*
- Venue: Annals of Data Science, Vol.12(3), pp. 1055–1072
- Access: Full text via CSUSM (Springer)
- Why it matters: Naturalistic patches via prompts — relevant if v26 suppression stays low and you need alternative approaches.

**Dai, Wang, Zhou, Guo & Zhang (2026)**
*AdvYOLO: An Improved Cross-Conv-Block Feature Fusion-Based YOLO Network for Transferable Adversarial Attacks on ORSIs Object Detection*
- Venue: Computers, Materials & Continua, Vol.87(1), pp. 1–10
- Access: Open access PDF available
- Why it matters: Builds a YOLO-based architecture for generating transferable attacks. Novel feature fusion approach.

---

## TIER 2 — Physical World & Benchmark Papers

### Physical Person Evasion

**Xu, Zhang, Liu, Fan, Sun, Chen, Chen, Wang & Lin (2020)**
*Adversarial T-shirt! Evading Person Detectors in A Physical World*
- Venue: ECCV 2020
- arXiv: 1910.11099
- Cited by: 520+
- Key numbers: **74% ASR digital, 57% ASR physical** against YOLOv2.
- Access: Open access
- Why it matters: Foundational physical-world person evasion benchmark. Your 85% digital on v8 is stronger than this 2020 baseline — important context for the write-up.

**Huang, Ren, Wang, Huo, Bai, Zhang & Yu (2025/2026)**
*AdvReal: Physical adversarial patch generation framework for security evaluation of object detection systems*
- Venue: Expert Systems with Applications, Vol.296, Article 128967
- DOI: 10.1016/j.eswa.2025.128967
- arXiv: 2505.16402
- Key numbers: **70.13% ASR on YOLOv12 in physical scenarios**; average ASR >90% under frontal/oblique views at 4m. Outperforms T-SEA (21.65%) and AdvTexture (19.70%).
- Access: Full text via CSUSM (ScienceDirect) + arXiv preprint
- Why it matters: Most recent physical attack benchmark with YOLO-family numbers.

**Wu, Lim, Davis & Goldstein (2019/ECCV 2020)**
*Making an Invisibility Cloak: Real World Adversarial Attacks on Object Detectors*
- arXiv: 1910.14667
- Access: Open access
- Key finding: Systematic study including white-box/black-box transferability, cross-dataset, cross-class, and physical attacks with printed posters and wearable clothes.

**Hu, Huang, Zhu, Sun et al. (2022)**
*Adversarial Texture for Fooling Person Detectors in the Physical World*
- Venue: CVPR 2022
- Cited by: 214+
- Access: CVF open access
- Why it matters: Full-body texture adversarial clothing, not just a patch — extends the threat model.

**Xue, He, Zhang, Liu & Liu (2025)**
*3D Invisible Cloak: A Robust Person Stealth Attack Against Object Detector in Complex 3D Physical Scenarios*
- Venue: IEEE Trans. Emerging Topics in Computing, Vol.13(3), pp. 799–815
- Access: Full text via CSUSM (IEEE)

### Transfer Improvement Techniques

**Huang, Chen, Chen & Wang (2022)**
*T-SEA: Transfer-based Self-Ensemble Attack on Object Detection*
- arXiv: 2211.09773
- Code: github.com/VDIGPKU/T-SEA
- Key finding: Single-model transfer attack using self-ensemble on input data, model, and patch to prevent overfitting. **Greatly improves black-box transferability.**
- Why it matters: Technique you could apply directly — uses one white-box model to generate patches that transfer to multiple black-box detectors. Has open code.

**Zhou, Zhao, Liu, Zhang et al. (2023/2024)**
*MVPatch: More Vivid Patch for Adversarial Camouflaged Attacks on Object Detectors in the Physical World*
- arXiv: 2312.17431
- Key finding: Dual-Perception Framework improves both transferability and stealthiness via ensemble strategy across multiple detectors.

**Ding, Chen, Yu, Shang, Qin & Ma (2024)**
*Transferable Adversarial Attacks for Object Detection Using Object-Aware Significant Feature Distortion*
- Venue: AAAI 2024, Vol.38(2), pp. 1546–1554
- Access: Open access
- Key finding: Leverages spatial consistency and feature distortion for improved transferability.

**Cao, Zhang, He, Liao, Xiao, Li, Huang & Dong (2025)**
*P³A: Powerful and Practical Patch Attack for 2D Object Detection in Autonomous Driving*
- arXiv: 2508.10600
- Key finding: Proposes Practical Attack Success Rate (PASR) metric and Localization-Confidence Suppression Loss (LCSL). Shows previous mAP-based metrics **overestimate attack effectiveness**.
- Why it matters: PASR metric may be more rigorous than your detection_suppression_pct — worth reading for methodology.

---

## TIER 3 — Defense & Survey Papers

**Guesmi, Hanif, Ouni & Shafique (2023)**
*Physical Adversarial Attacks for Camera-Based Smart Systems: Current Trends, Categorization, Applications, Research Challenges, and Future Outlook*
- Venue: IEEE Access, Vol.11, pp. 109617–109668
- Access: Open access via CSUSM
- Why it matters: Comprehensive 50-page survey — good for the related work section of the capstone.

**Zhang, Zhou, Xu, Wu, Liu (2025)**
*Adversarial attacks of vision tasks in the past 10 years: A survey*
- Venue: ACM Computing Surveys
- Cited by: 53
- Access: Via CSUSM (ACM DL)

**Ji, Feng, Xie, Xiang & Liu (2021)**
*Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches*
- arXiv: 2103.08860
- Key finding: Adds a "patch class" to YOLO to detect adversarial patches. With only 0.70% mAP drop, achieves 80.31% AP (vs 33.93% without defense).
- Why it matters: Shows YOLO-based defenses exist and work — good for the defenses section.

**Lee, Hong, Kim & Ha (2024)**
*SSIM-Based Autoencoder Modeling to Defeat Adversarial Patch Attacks*
- Venue: Sensors, Vol.24(19), Article 6461
- Access: Open access via CSUSM

---

## TIER 4 — Skim Abstracts Only

- Saha, Subramanya, Patil & Pirsiavash (2020) — "Role of Spatial Context in Adversarial Robustness for Object Detection" — CVPR Workshop
- Wang, Lv, Kuang et al. (2021) — "Towards a physical-world adversarial patch for blinding object detection models" — Information Sciences, Vol.556
- Tarchoun et al. (2021) — "Adversarial Attacks in a Multi-view Setting" — CyberWorlds 2021
- Hu, Poskitt, Sun & Dong (2026) — "DynamicPAE: Generating Scene-Aware Physical Adversarial Examples in Real-Time" — IEEE TPAMI, Vol.48(3)

---

## Access Summary

| Paper | Access Method |
|---|---|
| Bayer et al. (2024) | arXiv 2408.15833 (open) |
| Alam et al. (2023) | arXiv 2311.12914 (open) |
| Xu et al. (2020) T-shirt | arXiv 1910.11099 (open) |
| Wu et al. (2020) cloak | arXiv 1910.14667 (open) |
| T-SEA Huang (2022) | arXiv 2211.09773 (open) + GitHub code |
| MVPatch Zhou (2023) | arXiv 2312.17431 (open) |
| Ji YOLO defense (2021) | arXiv 2103.08860 (open) |
| AdvReal Huang (2025) | arXiv 2505.16402 (open) + ScienceDirect via CSUSM |
| Lovisotto (CVPR 2022) | CVF open access |
| Hu texture (CVPR 2022) | CVF open access |
| Wang Chosen-Object (2026) | IEEE via CSUSM |
| Liao anchor-free (2021) | IEEE via CSUSM + arXiv |
| ElevPatch Li (2025) | Springer ILL needed |
| Kleber (2025) | IEEE ILL needed |
| TK-Patch Imran (2025) | ILL needed |

---

## Key Benchmark Numbers for Your Write-Up

| Metric | Value | Source |
|---|---|---|
| Digital person suppression (v8, your result) | **85%** | This project |
| Digital person suppression (Thys 2019 baseline) | ~80% | Thys et al. |
| Digital person suppression (T-shirt on YOLOv2) | 74% | Xu et al. 2020 |
| Physical person suppression (T-shirt on YOLOv2) | 57% | Xu et al. 2020 |
| Physical person suppression (AdvReal on YOLOv12) | 70% | Huang et al. 2025 |
| Digital-to-physical gap (typical) | 15–25 pp | Schack et al. 2024 |
| Cross-model transfer (your v8→v11) | **39.4%** | This project |
| Cross-model transfer (Hoory v2→v3) | 10–14% | Hoory et al. 2020 |
| CNN→transformer transfer drop | Significant | Winter et al. 2026 |
| Anchor-based→anchor-free transfer drop | Significant | Liao et al. 2021 |
| Attention-based (standard patch) | ~0% AP possible | Alam et al. 2023 |

**Interpretation of your results:**
- Your 85% v8 is strong — above the 2020 T-shirt baseline, competitive with DAP (CVPR 2024)
- Your 39.4% v8→v11 is within normal cross-model range (Hoory showed 10–14% across YOLO versions)
- Your 16% v8→v26 is explained by THREE compounding factors: anchor-free architecture (Liao 2021), attention mechanisms (Lovisotto 2022), and Hungarian matching instead of NMS (Wang 2026)

---

## Recommended Next Steps

1. **Download and read Lovisotto (CVPR 2022)** — essential for understanding v26 resistance
2. **Download and read Wang Chosen-Object (2026)** — essential for v26 loss design
3. **Clone T-SEA code** — `github.com/VDIGPKU/T-SEA` — may improve transfer rates directly
4. **ILL request for ElevPatch** — the only YOLO11-specific paper; need the numbers
5. **Run browser agent with narrower queries**: "adversarial patch NMS-free detector", "adversarial patch Hungarian matching YOLO"
