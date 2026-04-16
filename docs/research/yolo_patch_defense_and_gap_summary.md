# YOLO Adversarial Patch — Defense Themes and Evidence Gaps

Generated: 2026-04-11
Scope: 30 unique PDFs in docs/papers/; additional note-only papers in docs/notes/

---

## Part 1: Recurring Defense Themes

### Theme 1: Patch Class Detection (Ad-YOLO Approach)

**Papers:** ji2021_adversarial_yolo_defense, na2025_unmanned_stores (partial), wu2024_NAPGuard (detection focus)

**Description:** Add a dedicated "adversarial_patch" detection class to the YOLO head. The model is co-trained to simultaneously detect persons and localize adversarial patches. At inference, a patch detection flags potential attack.

**Evidence strength:** Supported (ji2021 Table 4: 80.31% AP under white-box attack vs. 33.93% baseline; −1.45 pp clean cost)

**Capstone applicability:** High. Ji 2021 demonstrates this on YOLOv2; directly extensible to YOLOv8n (add class 80 = "adversarial_patch"; use Thys-style patches as training examples).

**Limitations:**
- Requires training-time access to representative patch appearances
- May fail against naturalistic patches (DAP, NatPatch) whose visual signature differs from aggressive psychedelic patches
- Placement assumption (chest) — back/floor patches may evade detection

---

### Theme 2: Adversarial Training on Patched Images

**Papers:** winter2026_benchmarking, ji2021, na2025

**Description:** Fine-tune detector on images with adversarial patches applied, so the model learns to produce correct predictions despite patch presence. Standard adversarial training loop.

**Evidence strength:** Mixed. Ji 2021 shows adversarial training (without patch class) achieves only 61.65% vs. Ad-YOLO's 80.31%. Winter 2026 shows mixed-attack adversarial training for digital (non-patch) attacks outperforms single-attack training. Extrapolation to patch domain: **Speculative**.

**Capstone applicability:** Medium. Winter 2026 recommends mixed-perturbation training (complementary objectives + high perturbation). This principle likely extends to patches.

**Key limitation:** Adversarial training often hurts clean accuracy more than the patch-class approach. Effectiveness against unseen patches (black-box attacker) is limited.

---

### Theme 3: Frequency Domain Detection (FRAN / Lovisotto)

**Papers:** lu2022_fran_frequency_attention, lovisotto2022_attention_patch_robustness

**Description:** Adversarial patches exhibit anomalous high-frequency or low-frequency signatures that differ from natural image content. Detection methods leverage this to localize patches before inference.

**Evidence strength:** Supported for the anomaly itself (lu2022 demonstrates frequency attention boosts attack and can identify patch regions; lovisotto2022 shows dot-product attention amplifies patch signals). Defense application: **Speculative** (not a deployed defense in these papers).

**Capstone applicability:** Medium. Frequency anomaly signatures could be used in the fortify phase as a pre-processing filter. However, naturalistic patches (DAP, Diff-NAT) specifically optimize to avoid high-frequency artifacts.

---

### Theme 4: Naturalistic Adversarial Patch Detection (NAPGuard)

**Papers:** wu2024_NAPGuard, hu2021_naturalistic_patch (attack side)

**Description:** NAPGuard specifically addresses the challenge that naturalistic adversarial patches (NAPs) are difficult to detect because they do not have the high-frequency psychedelic signature of standard patches. Uses aggressive feature-aligned learning (aligning with high-frequency components of adversarial patches) and natural feature suppressed inference (feature shield module to suppress NAP-associated frequencies at inference).

**Evidence strength:** Supported (wu2024 reports +60.24% AP@0.5 improvement on GAP dataset over prior NAP detection methods)

**Capstone applicability:** Medium-High. If the defend phase faces naturalistic patches (DAP-style), NAPGuard-style detection is the most appropriate response. For aggressive (non-naturalistic) patches, simpler methods suffice.

---

### Theme 5: Spatial Context Regularization

**Papers:** saha2020_spatial_context_yolo

**Description:** Standard YOLO loss only considers regions inside bounding boxes. Adding a spatial context loss that regularizes predictions outside the bounding box region forces the model to consider surrounding scene context, making it more robust to patches placed in background regions.

**Evidence strength:** Supported for the specific YOLOv3 evaluation in saha2020. Generalizability: **Speculative** (only YOLOv3).

**Capstone applicability:** Low-Medium. The insight is architecturally applicable to YOLOv8 but has not been validated on modern YOLO versions.

---

### Theme 6: Camera ISP as Natural Defense

**Papers:** wei2024_CAP_NeurIPS, schack2024_real_world_challenges

**Description:** The camera's Image Signal Processing (ISP) pipeline — demosaicing, denoising, white balancing, tone mapping — inherently attenuates adversarial perturbations. Physical attacks must account for this transformation; patches optimized only in digital domain often fail after camera capture.

**Evidence strength:** Supported. Wei 2024 demonstrates existing patches achieve 1/6 camera success rate due to ISP attenuation; their ISP-aware CAP achieves 6/6. Schack 2024 quantifies the hue transformation gap between physical and digital domains.

**Capstone applicability:** High for understanding. The ISP natural attenuation is a defense the fortify phase can exploit: deploying cameras that apply specific color/contrast transforms at the hardware level.

---

### Theme 7: Segment-and-Recover Approaches

**Papers:** gu2025_SAR_segment_recover, patchzero2022_detect_zero_defense

**Description:** Detect patch region, suppress or mask it, repair the image region, then re-run the detector on the recovered image. SAR uses FastSAM-guided segmentation plus inpainting and evaluates directly on YOLOv11, DETR, and Faster R-CNN. PatchZero uses a detect-and-zero pipeline with adaptive evaluation across patch attacks.

**Evidence strength:** Supported. SAR reports strong recovery against printable and adaptive patches while keeping false alarm rates near zero on clean data; PatchZero reports gains over PatchGuard and PatchCleanser under both standard and adaptive attacks.

**Capstone applicability:** High. This is now the clearest literature-backed fortify baseline for the project, but it still needs direct evaluation on YOLOv8 and YOLO26.

---

## Part 2: Evidence Gaps Relevant to the Capstone

### Gap 1: No Paper Evaluates Adversarial Patches on YOLO26 (NMS-free)

**What is missing:** Zero papers in this corpus evaluate adversarial patch attacks or defenses on YOLO26 or any NMS-free YOLO variant (RT-DETR, DINO-YOLO). Bayer 2024 includes RT-DETR which uses similar attention-based token representations, and finds it is substantially more robust to transfer attacks than CNN-based YOLO.

**Why it matters:** YOLO26's NMS-free design changes the detection pipeline fundamentally — there is no objectness score to minimize, and bounding box predictions are produced differently. Attack losses that target objectness (L_obj in Thys 2019) may not translate directly.

**What the capstone should measure:** Transfer from YOLOv8n-trained patch to YOLO26n; whether objectness-targeting losses need to be replaced with class-confidence-targeting losses for NMS-free detectors.

---

### Gap 2: No Systematic Cross-Generation Transfer Study (v8 → v11 → v26)

**What is missing:** Bayer 2024 covers v7–v10 (28 models); AdvReal 2025 covers v2, v3, v5, v8, v11, v12. But no paper systematically evaluates v8 → v11 → v26 as a three-step ladder with the same patch and metric. This is the specific transfer ladder the capstone needs.

**Closest evidence:**
- AdvReal (huang2025): v2→v8 recall=32.68%, v2→v11 recall=32.47% (similar between v8 and v11, consistent with shared Ultralytics architecture)
- Bayer 2024: v8n and v8s are weak source models; larger v8 variants transfer better

**What the capstone should measure:** Patch trained on v8n → evaluate on v8n (white-box), v11n (black-box), v26n (black-box). Report AP or recall at IoU=0.5.

---

### Gap 3: Physical Plausibility Under Real-World Conditions for v8/v11/v26

**What is missing:** Physical evaluation for modern Ultralytics YOLO models is almost entirely absent. Huang 2025 (AdvReal) evaluates physical performance but on YOLOv12, not v8/v11/v26 specifically. The digital-physical gap documented by Schack 2024 (YOLOv3/v5) has not been measured for v8/v11/v26.

**Why it matters:** If the capstone patch achieves 85% digital ASR on v8n but only 30% after printing (extrapolating from Schack 2024's documented gaps), the physical plausibility claim requires empirical grounding.

**What the capstone should measure:** At minimum, document the EoT augmentation parameters used during digital training and compare to known physical degradation conditions (brightness, rotation, size reduction per Schack 2024).

---

### Gap 4: Defense Evaluation on YOLOv8/v11/v26

**What is missing:** All defense papers (Ji 2021 Ad-YOLO, NAPGuard, Saha 2020) evaluate on YOLOv2 or YOLOv3. The defend phase will target YOLOv8n but has no direct literature precedent.

**What the capstone should do:** Apply Ad-YOLO (patch class addition) to YOLOv8n. The expected clean cost (~1-2 pp mAP) and robustness improvement (~46% AP recovery) from Ji 2021 provide literature-backed expectations.

---

### Gap 5: Naturalistic Patches vs. Aggressive Patches — Physical Robustness Comparison

**What is missing:** AdvReal 2025 Table 3 shows that NatPatch achieves 4.11% ASR and AdvCaT 0.87% on YOLOv12 (vs. AdvReal's 70.13%) — naturalistic patches fail physically. But the literature lacks a controlled comparison of:
(a) aggressive patch (psychedelic) vs. naturalistic patch (GAN/diffusion-generated) under identical physical conditions
(b) which is detectable by human observers vs. camera-based detection systems

**Why it matters:** The capstone's "physically plausible" constraint could mean either "naturalistic appearance" or "respects physical printing/lighting constraints." These are different constraints. AdvReal's result suggests aggressive patches win on effectiveness while naturalistic patches fail. The correct balance is unclear.

**What the capstone should document:** Explicit definition of "physical plausibility" — printable colors (NPS constraint) + viewing angle robustness (EoT) — but NOT necessarily naturalistic GAN appearance.

---

### Gap 6: Fortification (Recovery After Attack) — Sparse Direct Evidence for YOLO8+

**What is missing:** The fortify phase (recover detection quality after an adversarial patch is in the scene) now has two usable literature anchors, gu2025_SAR and patchzero2022, but coverage is still sparse for modern Ultralytics YOLO. SAR evaluates YOLOv11 directly, while PatchZero is detector-agnostic and does not target the current v8/v11/v26 ladder. Neither paper evaluates YOLOv8 or YOLO26.

**What the capstone should measure:** Test segment-and-recover pipeline on YOLOv8n: detect patch region, inpaint, re-run detector. Measure recovery rate.

---

## Part 3: Contradictions Worth Flagging

### Contradiction 1: Naturalistic Patches — Stealth vs. Effectiveness

- Hu 2021 (NatPatch, ICCV): naturalistic patches can achieve effective suppression while appearing visually unobtrusive
- AdvReal 2025 (Huang): NatPatch achieves only 4.11% ASR on YOLOv12 in realistic conditions; AdvCaT 0.87%
- DAP 2024 (Guesmi): dynamic naturalistic patches with physical robustness achieve good results in controlled tests

**Assessment:** The contradiction likely resolves by experimental conditions. AdvReal uses realistic outdoor backgrounds and 7 black-box detectors including newer YOLO generations — a harder test. Papers reporting naturalistic patch success tend to use controlled single-detector settings. **Conclusion:** Naturalistic appearance significantly trades away effectiveness in realistic cross-detector settings. The capstone should not pursue naturalistic patches if effectiveness is the priority.

### Contradiction 2: Model Size and Robustness Direction

- Bayer 2024: YOLOv8n/s are weak source models for transfer (patches transfer poorly from them to targets)
- Bayer 2024: YOLOv9/v10 are most resistant to incoming transfer attacks (good target robustness)
- AdvReal 2025: AdvReal (trained on YOLOv2) still achieves 32.68% recall reduction on YOLOv8 as black-box target

**Assessment:** These are consistent, not contradictory. Small source models produce weak-transferring patches. Large models are more robust targets. But AdvReal shows that with a sophisticated training framework (3D non-rigid + ShakeDrop), even a YOLOv2-trained patch can achieve meaningful v8 transfer. **Conclusion:** Source model size matters less when training methodology is sophisticated.

### Contradiction 3: Physical Transfer — Camera ISP as Attack vs. Defense

- Wei 2024 (CAP): Camera ISP significantly weakens adversarial patches — treat ISP as a defense layer to model
- Schack 2024: Physical-digital gap is primarily due to color/lighting transformations that the ISP applies
- AdvReal 2025: Uses relighting-matching and 3D rendering to overcome ISP gap; achieves 70%+ physical ASR

**Assessment:** Consistent. ISP is a real degradation. Sophisticated attackers (AdvReal, Wei CAP) account for it. For the capstone's digital-phase-only work, the ISP gap is a known limitation to document rather than overcome. Wei 2024's ISP proxy network is the appropriate defense-side response.
