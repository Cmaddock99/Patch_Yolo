# PDF Corpus Synthesis — Adversarial Patch Research

---

## FINAL SUMMARY BLOCK

**Date:** 2026-04-11  
**Total PDF count:** 32 (30 unique, 2 duplicate arXiv preprints excluded from analysis)  
**Recent additions reviewed:** 22 PDFs added in the 5 most recent commits to docs/papers/  
**Duplicates found:** 2 pairs — canonical choices: `zolfi2021_translucent_patch_CVPR.pdf`, `guesmi2024_DAP_CVPR.pdf`  
**Papers deep-read (extended notes with page citations):** 8 (brown2017, thys2019, liu2019, cheng2024_depatch, bayer2024_network_transferability, huang2025_advreal, ji2021_adversarial_yolo_defense, huang2022_tsea_transfer)  
**Papers skimmed (template notes, some page references):** 22  
**Papers with note-only (no PDF in corpus):** 15 additional papers in docs/notes/ without corresponding PDFs

### Most Important YOLO-Specific Findings (with paper slugs)

1. **huang2025_advreal**: Only paper in corpus to directly evaluate on YOLOv8, YOLOv11, and YOLOv12. Trained on YOLOv2 glass-box; achieves recall reduction to 32.68% on YOLOv8 and 32.47% on YOLOv11 (closed-box). Physical ASR 70.13% on YOLOv12 with AdvReal framework. Strongest cross-generation result in corpus.

2. **bayer2024_network_transferability**: Systematic 28-model compatibility matrix showing YOLOv8n and YOLOv8s are weak source models for transfer — patches trained on nano/small variants transfer poorly. YOLOv9/v10 are most resistant targets. RT-DETR is an outlier (both poor source and robust target). Directly explains why capstone v8n→v26n transfer may be low.

3. **cheng2024_depatch**: Most practically applicable 2024 person-vanishing paper. Block-wise decoupling reduces "self-coupling" issue in physical deployment. Digital AP 17.75%, physical clothing ASR 90.96%, physical poster ASR 80.14% on YOLOv2. Best occlusion robustness in corpus.

4. **huang2022_tsea_transfer**: Code-available (GitHub). Self-ensemble approach achieves black-box average mAP 9.16% across 7 detectors from single YOLOv5 source. ShakeDrop + patch cutout = actionable improvements for capstone v2 run.

5. **ji2021_adversarial_yolo_defense**: Best defense paper with a PDF. "Patch class" in YOLO head achieves 80.31% AP under white-box attack vs. 33.93% baseline; only −1.45 pp clean cost. Directly extensible to YOLOv8n for defend phase.

6. **thys2019**: Canonical person-vanishing baseline. OBJ loss reduces recall 100%→26.46% on INRIA/YOLOv2. Loss design (L_nps + L_tv + L_obj) and INRIA dataset are the standard that all subsequent papers compare against.

### Strongest Defense/Mitigation Themes

1. **Patch class detection** (ji2021): ~46% AP improvement under attack; negligible clean cost; directly extensible to YOLOv8
2. **Frequency domain anomaly detection** (lu2022_fran): patches exhibit frequency anomalies exploitable for detection
3. **Camera ISP as natural defense** (wei2024_CAP, schack2024): ISP inherently attenuates patches; exploit at hardware level
4. **Naturalistic patch detection** (wu2024_NAPGuard): +60.24% AP@0.5 on GAP dataset for NAP detection
5. **Adversarial training** (winter2026, ji2021): works but patch-class approach is more effective; mixed-attack training improves robustness

### Biggest Remaining Evidence Gaps (Relative to Capstone Anchor)

1. **YOLO26 entirely absent** — zero papers evaluate any attack or defense on YOLO26 or equivalent NMS-free YOLO
2. **No systematic v8→v11→v26 transfer study** — AdvReal provides v2→v8/v11 data but not with YOLOv8n as source
3. **Physical evaluation for v8/v11** — AdvReal is closest (clothing + nuScenes), but uses YOLOv2 glass-box; no direct v8n white-box physical study
4. **Defense on YOLOv8+** — all defense papers use YOLOv2 or older; no adaptation to decoupled-head architectures
5. **Fortify (recovery) phase** — only note-only papers (SAR, PatchZero) address recovery; no PDF evidence for v8+

---

## Section 1: YOLO-Specific vs. Detector-Adjacent Papers

### Truly YOLO-Specific (YOLO is the central model)

| Paper | YOLO Versions | Notes |
|---|---|---|
| thys2019 | YOLOv2 | Canonical person-vanishing for YOLO; YOLOv2 is the only model |
| liu2019_dpatch | YOLOv2, Faster-RCNN | DPatch — YOLO plus Faster-RCNN; YOLO central |
| ji2021_adversarial_yolo_defense | YOLOv2 | Defense explicitly designed for YOLO architecture |
| huang2025_advreal | YOLOv2/v3/v5/v8/v11/v12 | Explicitly targets YOLO family + transformers; YOLO central |
| bayer2024_network_transferability | YOLOv7–v10 (28 models) | YOLO-family compatibility matrix as primary contribution |
| cheng2024_depatch | YOLOv2/v3/v5 | Person detection; YOLO is primary victim |
| huang2022_tsea_transfer | YOLOv2–v5, Faster-RCNN, SSD | YOLOv5 white-box; multi-YOLO black-box |
| saha2020_spatial_context | YOLOv3 | Spatial context in YOLO specifically |
| lu2022_fran | YOLOv3/v4/v5 | Frequency attention for YOLO person detectors |
| delacruz2026_physical | YOLOv8 (mentioned) | Physical surveillance; YOLO8 explicitly |

### Detector-Adjacent (YOLO is one of several models)

| Paper | Primary Model | YOLO Role |
|---|---|---|
| brown2017 | ImageNet classifiers | Not applicable |
| wu2020_invisibility_cloak | Multi-detector | YOLOv2 as one of several |
| xu2020_adversarial_tshirt | YOLOv2, Faster-RCNN | YOLOv2 as primary person detector |
| guesmi2024_DAP | YOLOv5, Faster-RCNN | YOLOv5 as one detector |
| zhou2023_mvpatch | Multi-YOLO + Faster-RCNN | Ensemble across YOLO versions |
| tan2024_DOEPatch | Multi-YOLO + Faster-RCNN | Ensemble approach |
| wei2024_CAP | YOLOv5 | Person detector |
| schack2024_real_world | YOLOv3, YOLOv5 | Two YOLO versions evaluated |
| wu2024_NAPGuard | Multiple | YOLO is one target |

### Not YOLO / YOLO-Peripheral

| Paper | Notes |
|---|---|
| alam2023_attention_deficit | Deformable DETR only; no YOLO |
| lovisotto2022_attention_CVPR | Architecture-agnostic attention analysis; no specific YOLO |
| winter2026_benchmarking | YOLOv3, YOLOX — no v8/v11/v26; patch attacks explicitly excluded |
| hoory2020_dynamic_patch | YOLOv3 as one of several; scene focus |
| bagley2025_spap | YOLO version unspecified |
| diffnat2026_AAAI | Multi-detector; naturalness focus |
| hu2021_naturalistic | YOLOv2, Faster-RCNN; naturalness focus |
| zolfi2021_translucent | YOLOv3 eval; stop signs only |

---

## Section 2: Papers Evaluating YOLOv8, YOLO11, or YOLO26 Directly

| Paper | v8 | v11 | v26 | Notes |
|---|---|---|---|---|
| huang2025_advreal | Yes (Table 7: recall→32.68%) | Yes (Table 7: recall→32.47%) | No | Only paper in corpus with direct v8 AND v11 evaluation |
| delacruz2026_physical | Mentioned (not quantified in pages read) | No | No | 2026 preprint; limited numbers |
| bayer2024_network_transferability | Yes (v8 family: n,s,m,l,x) | No (v11 released after paper) | No | Compatibility matrix includes all v8 variants as source/target |
| winter2026_benchmarking | No | No | No | Only v3, YOLOX |
| zhou2025_sequence_clothing | YOLOv8 mentioned | No | No | Limited quantitative in pages read |

**Critical finding:** Only huang2025_advreal provides direct quantitative evidence for v8 and v11 vulnerability. YOLO26 has no coverage in this corpus.

---

## Section 3: Attack Families — Digital-Only vs. Physically Evaluated

### Physically Evaluated (with specific conditions noted)

| Paper | Physical Method | Physical Condition | ASR / Result |
|---|---|---|---|
| thys2019 | Printed cardboard held by person | Surveillance camera | Recall → 26.46% |
| wu2020_invisibility_cloak | Printed poster + wearable clothing | Indoor/outdoor | Systematic distance/angle study |
| xu2020_adversarial_tshirt | Adversarial T-shirt | Corridor walking video | 57% ASR |
| guesmi2024_DAP | Wearable clothing | Multiple conditions | Physical robustness with Creases Transform |
| cheng2024_depatch | Posters attached to clothing + adversarial clothes | 1.5–4.5m, outdoor | Poster 80.14%, clothing 90.96% ASR |
| huang2025_advreal | Long-sleeve tops + trousers | nuScenes traffic backgrounds | Physical ASR 70.13% on YOLOv12 |
| zolfi2021_translucent | Translucent film on camera lens | Autonomous driving scenes | 42.27% stop sign suppression |
| schack2024_real_world | Pre-trained patches; lab conditions | 4–61 lux, rotation ±90°, 4–16cm sizes | Gap quantified: hue/brightness significant |
| wei2024_CAP | Printed clothing | 6 camera hardware variants | 6/6 cameras vs. 1/6 baseline |
| na2025_unmanned_stores | Patch stickers in retail | Real store environment | Three attack types evaluated |
| xu2020_adversarial_tshirt | T-shirt worn | Corridor | 57% physical vs. 74% digital |
| li2025_uvattack | NeRF-rendered UV mapping clothing | Multi-view | Physically stable across viewpoints |
| zhou2025_sequence_clothing | Sequence-level video adversarial clothing | Video frames | Consistent across pose changes |
| bagley2025_spap | Superpixel cluster patches | Physical surface | Maintains adversarial under physical transform |
| huang2022_tsea | iPad display | Qualitative only | Person missed by YOLOv5 + SSD |

### Digital-Only

| Paper | Note |
|---|---|
| brown2017 | Classifier-only; printed but not detector-tested |
| liu2019_dpatch | Digital only; no physical |
| hu2021_naturalistic | Digital GAN generation; no physical |
| saha2020_spatial_context | Digital only |
| alam2023_attention_deficit | Digital only; deformable ViT |
| lovisotto2022 | Digital analysis only |
| bayer2024_network_transferability | Digital transfer study only |
| tan2024_DOEPatch | Digital multi-model ensemble only |
| winter2026_benchmarking | Digital non-patch attacks only |
| wu2024_NAPGuard | Detection evaluation; digital |
| diffnat2026_AAAI | Digital generation; naturalness focus |

---

## Section 4: Results Robust Across Multiple Conditions

### Robust Findings (appear across multiple papers)

1. **Objectness loss outperforms class probability loss for person suppression** — First shown in thys2019 (OBJ recall 26.46% vs. CLS 77.58%); corroborated structurally by DePatch (IoU-weighted accuracy target) and AdvReal (detection loss with IoU threshold). **Evidence: Strong (3 independent papers, multiple detectors)**

2. **Physical patches degrade significantly with hue/color transformation** — Schack 2024 documents this as the primary physical-digital gap; Wei 2024 addresses it via ISP modeling. **Evidence: Supported (2 papers, independent methodologies)**

3. **Larger source models → better cross-model transfer** — Bayer 2024 shows this for the YOLO family specifically; Wu 2020 (Invisibility Cloak) shows ensemble of detectors during training improves transfer; AdvReal shows even YOLOv2-trained patches transfer well when training methodology is sophisticated. **Evidence: Supported (2 papers directly; consistent with AdvReal)**

4. **Self-coupling in patches causes physical failure** — DePatch (cheng2024) names and addresses this explicitly; the phenomenon is implicitly present in Schack 2024's finding that partial occlusion collapses patch effectiveness. **Evidence: Supported (1 direct paper; 1 corroborating)**

5. **NMS must be fooled at all anchor points simultaneously** — Wu 2020 articulates this as the fundamental challenge of detector attacks vs. classifier attacks. DePatch's IoU-weighted target selection addresses it. **Evidence: Supported (2 papers, consistent with detector architecture)**

6. **Transformer-based detectors (DETR, DINO) are more robust to patch transfer** — Winter 2026 (digital attacks), Bayer 2024 (RT-DETR is outlier), AdvReal (D-DETR 59.09% vs. YOLO 70-78%). **Evidence: Supported (3 papers; consistent pattern)**

### Mixed/Uncertain Findings

1. **Naturalistic patches vs. aggressive patches** — contextual (see contradictions in defense document)
2. **Physical rotation robustness** — DePatch shows good 360° robustness; Schack shows >20° rotation degrades patches. Reconciled by different patch types (clothing wraps vs. flat poster) and evaluation setups.

---

## Section 5: Claims Relying on Unusually Strong Assumptions

| Paper | Assumption | Assessment |
|---|---|---|
| thys2019 | White-box YOLOv2; patch visible on person's front facing camera | Standard for proof-of-concept; not deployable without visibility |
| zolfi2021_translucent | Attacker has supply-chain access to camera lens | Very strong assumption; limits threat model to insider attacks |
| li2025_uvattack | NeRF model of person available; multi-camera calibration needed | High compute; complex setup |
| lovisotto2022 | Patch placed in exact attention hotspot location | Placement precision requirement may not be achievable physically |
| bagley2025_spap | Superpixel boundaries align with physical object surfaces | May not generalize to arbitrary viewpoints |
| alam2023_attention_deficit | Model uses deformable attention (DETR-style) | Not applicable to CNN-based YOLO |

---

## Section 6: Defenses and Recovery Methods

### Defense Methods with Quantitative Evidence (PDF in corpus)

| Defense | Paper | Method Type | Quantitative Result |
|---|---|---|---|
| Ad-YOLO patch class | ji2021 | Detection (in-model) | 80.31% AP under white-box vs. 33.93% baseline |
| NAPGuard | wu2024_NAPGuard | Detection (separate module) | +60.24% AP@0.5 on GAP dataset |
| ISP proxy defense | wei2024_CAP | Physical-layer defense | Baseline patches: 1/6 cameras; with ISP: 6/6 |
| Adversarial training (mixed) | winter2026 | Training-time robustness | 2.3 pp clean cost; improved digital non-patch robustness |
| FRAN (frequency attention) | lu2022_fran | Detection via frequency | Frequency anomalies localize patch regions |

### Defense Methods Mentioned (note-only, no PDF)

- PatchZero (2022) — zero-shot patch detection
- SAR — Segment and Recover (gu2025)
- Kolter global patch suppression (kolter2019)

---

## Section 7: Thin or Contradictory Evidence Zones

1. **YOLO26 / NMS-free YOLO** — completely absent from attack AND defense literature in this corpus. Total gap.

2. **YOLOv8n specifically as a white-box source model for physical attacks** — Bayer shows v8n is a weak transfer source; AdvReal uses YOLOv2 as source and shows good v8 transfer as TARGET. The capstone's specific configuration (v8n as source, v11n/v26n as targets) has no direct precedent.

3. **Fortify phase (recovery after attack)** — only note-only papers; no PDF evidence.

4. **Physical validation of defense methods** — Ji 2021 provides qualitative physical demo for Ad-YOLO; no paper provides systematic physical attack + defense physical comparison in same experiment.

5. **Cross-YOLO-generation defense transfer** — if a defense is trained on patches targeting v8n, does it generalize to patches targeting v11n or v26n? No evidence in corpus.

---

## New PDFs Added (Post Previous Review)

Three PDFs were downloaded after the previous review and are now triage-read. Their full upgraded notes are at `docs/notes/huang2019_universal_physical_camouflage.md`, `docs/notes/kolter2019_global_patch_suppression.md`, and `docs/notes/patchzero2022_detect_zero_defense.md`.

### huang2019_UPC — Universal Physical Camouflage (Huang et al., CVPR 2020)

**Triage summary**: Introduces Universal Physical Camouflage (UPC) — a universal adversarial pattern that hides all instances of a target class simultaneously (universal across persons of different poses, sizes, lighting). **Primary evaluated detectors are Faster R-CNN variants (VGG16, ResNet), NOT YOLO directly** — this is the key limitation for this corpus. The attack jointly targets the RPN stage (L_rpn: reduce proposal quality) and the classification+regression stage (L_cls + L_reg: mislead class output and corrupt bounding box predictions). A semantic constraint (projection onto natural image manifold) enforces visual naturalness of the generated pattern — the camouflage appears as a realistic texture on human accessories (garments, masks). UPC achieves single-digit mAP on Faster R-CNN across multiple variants (Table 1: our method at Cnt=0.001 achieves mAP 0.28 vs. DPatch 9.21 on unclipped case). The paper introduces **AttackScenes** — the first standardized virtual benchmark database for reproducible physical-world evaluation (20 virtual scenes, 18 cameras per scene, 3 illumination levels). The physical deployment scenario is printed garment texture on human clothing.

**Capstone relevance**: Moderate. The AttackScenes benchmark is citable as the first systematic virtual physical-world evaluation standard. The semantic constraint and deformation transforms (T_r external/viewpoint, T_c internal/cloth) are portable to the capstone's EoT pipeline. The joint RPN + C&R attack design does not directly apply to YOLOv8+ (single-stage anchor-free) but the multi-head attack principle is relevant for YOLO26's one2many/one2one dual outputs.

**Evidence confidence**: Medium — PDF triage read; YOLO not directly evaluated.

### kolter2019_global_patch — On Physical Adversarial Patches for Object Detection (Lee & Kolter, ICML Workshop 2019)

**Triage summary**: Demonstrates that a single adversarial patch placed **anywhere in a scene** (not on the target person) can suppress all YOLOv3 person detections. Uses standard PGD (Madry et al. 2017) with expectation over transformations (rotation, scale, translation, brightness). Key technical contribution: identifies and corrects a clipping flaw in DPatch's implementation — DPatch's clipping produces weakly adversarial patches; properly clipped PGD patches are dramatically stronger. **Quantitative results (YOLOv3, COCO 2014)**: Clipped attack at 0.5 conf threshold — Ours: 7.2% mAP vs. DPatch: 26.8% mAP vs. Baseline: 40.9%. At 0.001 conf — Ours: 19.4% vs. DPatch: 39.6% vs. Baseline: 55.4%. Physical demonstration: printed patch on standard printer paper fooling YOLOv3 via webcam. Note: authors are Mark Lee and J. Zico Kolter (NOT Madry — the "Kolter & Madry" attribution in secondary literature is an error).

**Capstone relevance**: High for threat-model framing. The global scene-level threat model (attacker controls the environment, not the person) is a canonical contrast to wearable patches. The clipping-correction finding explains why ART's DPatch implementation in `create_adv_patch.py` may be weaker than a properly implemented PGD patch — relevant to the baseline discussion. The YOLOv3 mAP (7.2%) is directly comparable to other suppression results in the pool.

**Evidence confidence**: High — PDF triage read; exact quantitative results extracted from Tables 1 and 2.

### patchzero2022 — PatchZero (Xu, Xiao et al., WACV 2023)

**Triage summary**: General defense pipeline that detects adversarial patches at the pixel level and zeros out the patch region with mean pixel values — without retraining the downstream classifier or detector. Exploits the observation that adversarial patches are highly textured and visually different from natural image regions. Architecture: PSPNet (ResNet-50 backbone) patch detector + zeroing step. Two-stage adversarial training: Stage 1 (DO attack only) → Stage 2 (BPDA adaptive attack considering both patch detector and downstream model). **Quantitative results (ImageNet, MPGD/MAPGD attacks)**: PatchZero-DO: 75.80% / 76.80% vs. PatchGuard: 48.91% / 48.91% vs. PatchCleanser: 64.30% / 63.57% vs. Undefended: 14.35% / 9.40%. On RESISC-45: PatchZero-DO achieves 87.5% / 85.0% (MPGD/MAPGD) vs. adversarial training 71.8% / 67.2%. Detector-agnostic (no downstream model retraining); transfers to different patch shapes and attack types.

**Capstone relevance**: High for defense comparison table. PatchZero is one of six defense paradigms in the pool: (1) Ad-YOLO patch class [ji2021], (2) adversarial training, (3) frequency detection [lu2022], (4) NAPGuard semantic [wu2024], (5) detect-and-zero [patchzero2022], (6) anomaly reconstruction [tereshonok2025]. PatchZero's detector-agnostic preprocessing approach is directly applicable to any YOLOv8/v11/v26 deployment without architecture-specific adaptation. The ART codebase used for attacks in this paper is the same framework as `create_adv_patch.py`.

**Evidence confidence**: High — PDF triage read; exact quantitative comparison tables extracted.

---

## Note-Only Paper Coverage Summary

The 12 Tier C papers (notes without local PDFs) collectively add the following to the picture at metadata level. The picture changes substantially once their PDFs are obtained.

### What the 12 papers collectively add (metadata level only)

**Modern YOLO coverage (v8/v11)**: Four papers would, once verified, provide direct quantitative benchmarks for YOLOv8 and/or YOLO11 that do not exist in the PDF corpus:
- gala2025 (v5/v8/v9/v10 systematic evaluation)
- zimon2025 (v3/v5/v8/v11 systematic evaluation — most directly comparable to capstone)
- li2025_elevpatch (YOLO11 only — the sole YOLO11 benchmark)
- imran2025_tkpatch (v3/v5/v7 — informative for multi-YOLO loss design)

**YOLO26 architecture**: Two papers provide the architectural framework for attacking YOLO26 properly, which the PDF corpus entirely lacks:
- wang2026_chosen_object (Hungarian matching loss for end-to-end detectors)
- liao2021_anchor_free (anchor-free output format mismatch explains transfer failure)

**Defense landscape completion**: Four papers would complete a six-paradigm defense taxonomy:
- gu2025_SAR (segment-recover paradigm)
- ma2026_XAIAD (XAI test-time purification, anchor-free YOLO)
- tereshonok2025 (anomaly reconstruction)
- patchzero2022 (detect-and-zero — now PDF-confirmed in this update)

**Naturalism comparison**: Two papers add alternative naturalism approaches:
- lin2024_entropy (entropy maximization — simpler than GAN)
- truong2024_AYO_GAN (GAN perturbation baseline — 22.25% ASR, key comparison for localized patches)

**Citation verification**: One paper (bae2020_TOG) requires citation confirmation before use.

### What changes once PDFs are obtained

1. **YOLO11 direct benchmark**: Once li2025_elevpatch is obtained, the capstone has a literature comparison for 84.8% YOLO11 suppression. Without it, the result stands only in relation to huang2025_advreal's closed-box 32.47% recall (different threat model — not directly comparable).

2. **YOLOv8 cross-version benchmark**: Once gala2025 and zimon2025 are obtained, the capstone can place its 90% v8n result in the context of a systematic literature comparison across YOLO versions. Currently, only bayer2024 and bagley2025 provide quantitative v8 data points (neither with person-class suppression percentages in the same format).

3. **YOLO26 loss design**: Once wang2026 is obtained, the capstone has an architectural basis for a v26-specific loss redesign. This would be the most significant technical improvement to the v26 experiments.

4. **Defense taxonomy completeness**: The PDF corpus currently has 5 of 6 defense paradigms with quantitative evidence (patch class, frequency, NAPGuard, PatchZero, adversarial training). Obtaining gu2025, ma2026, and tereshonok2025 completes the taxonomy with quantitative evidence for the remaining paradigms.
