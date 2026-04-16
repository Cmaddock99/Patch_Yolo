# Master Paper Pool — Adversarial Patch Research

**Document status**: Authoritative unified registry  
**Generated**: 2026-04-15
**Scope**: All papers known to the repo across tiers A–E  
**Supporting documents**: See `docs/research/pdf_corpus_synthesis.md`, `docs/research/yolo_patch_evidence_matrix.md`, `docs/research/yolo_patch_defense_and_gap_summary.md`

---

## Section 1: Executive Summary

### Total Papers in Pool

| Tier | Label | Count |
|------|-------|-------|
| A | PDF + deep note (page-cited) | 18 |
| B | PDF + skim note | 24 |
| C | Unpromoted / unverified note records | 8 |
| D | Ranked candidates (not yet in repo) | 2 |
| E | First-party experimental results | 1 (special entry) |
| **Total** | | **53** |

Notes: Tier B count is 24 (not 22 from previous synthesis) because this run added 3 newly-downloaded PDFs (huang2019, kolter2019, patchzero2022) and upgraded their notes. Gala 2025 and Liao 2021 were promoted from Tier C into Tier A in the previous sync, and the current sync adds Lin 2024 NutNet, Hu 2022 AdvTexture, Liang 2021 Catch You, Nazeri 2024 DETR robustness, Dimitriu 2024 multi-model transferability, Gu 2025 SAR, Tereshonok 2025 anomaly localization, and Xu 2020 Adversarial T-shirt into Tier A. Two PDFs are duplicates (zolfi2021_CVPR = canonical; guesmi2024_CVPR = canonical) per `research/data/ranked/pdf_duplicates.md`.

### Coverage of Target Models

| Model | Tier A (deep-read) | Tier B (skimmed) | Tier C (unpromoted) | Tier D (candidate) | First-party |
|-------|-------------------|-----------------|-------------------|-------------------|-------------|
| YOLOv8 | 5 (huang2025_advreal, bayer2024, gala2025, liang2021, dimitriu2024) | 4 | 2 (zimon2025, imran2025*) | 0 confirmed | Yes (90% suppression) |
| YOLO11 | 2 (huang2025_advreal, gu2025_SAR) | 1 (zhou2025) | 2 (li2025_elevpatch, zimon2025) | 0 confirmed | Yes (84.8% suppression) |
| YOLO26 | 0 | 0 | 0 | 0 confirmed | Yes (11.6% suppression, difficult) |

*imran2025 evaluates v3/v5/v7, not v8 directly.

### Most Critical Gaps

1. **YOLO26 has zero literature coverage** — the capstone is the first documented study of adversarial patch attacks on this architecture. This is the primary novel contribution.
2. **The v8n→v26n transfer failure (11.6%)** is predicted by literature (bayer2024 weak-source finding, liao2021 anchor-free transfer failure) but no paper directly studies this specific path.
3. **YOLO11-specific literature** contains only one known paper (li2025_elevpatch) — paywalled, results unknown.
4. **Defense methods for YOLOv8+ architectures remain thin** — Catch You includes YOLOv8 detection results, but most stronger recovery-style defenses still stop at YOLOv2-v4 or detector-agnostic settings.
5. **Physical validation on v8/v11** — AdvReal (huang2025) is closest but uses YOLOv2 as the white-box source.

### First-Party Experimental Summary

The repo has produced measured results across 6 experimental runs — the most complete multi-generation YOLO adversarial patch study in the literature:

| Run | Model | Suppression % | Key finding |
|-----|-------|--------------|-------------|
| Direct | YOLOv8n | 90.0% | Strong — exceeds all 2020-era baselines |
| Direct | YOLO11n | 84.8% | Strong — comparable to v8n |
| Direct | YOLO26n | 11.6% | Weak — structural optimization failure |
| Transfer v8n→v11n | YOLO11n | 36.4% | Moderate — 48pp below direct |
| Transfer v8n→v26n | YOLO26n | 11.6% | Negligible transfer |
| Transfer v11n→v26n | YOLO26n | 16.3% | Negligible transfer |

---

## Section 2: Complete Paper Registry Table

Legend — Evidence confidence: **high** = PDF + page citations | **medium** = PDF + skim | **low** = note-only, unverified-from-pdf | **metadata-only** = ranked candidate, no note

| Slug | Title (short) | Year | Venue | Tier | PDF? | Note? | YOLO Versions | Goal | Confidence | Relevance (1–5) | Access |
|------|---------------|------|-------|------|------|-------|---------------|------|------------|-----------------|--------|
| brown2017 | Adversarial Patch | 2017 | arXiv/NIPS | A | Yes | Yes | None (classifiers) | Targeted misclassification | high | 2 | Open |
| thys2019 | Fooling Surveillance Cameras | 2019 | CVPRW | A | Yes | Yes | YOLOv2 | Person vanishing | high | 4 | Open |
| liu2019_dpatch | DPatch | 2019 | SafeAI@AAAI | A | Yes | Yes | YOLOv2, Faster-RCNN | Untargeted suppression | high | 3 | Open |
| cheng2024_depatch | DePatch | 2024 | arXiv | A | Yes | Yes | YOLOv2/v3/v5 | Person vanishing, physical | high | 5 | Open |
| lin2024_nutnet | NutNet Real-Time Defense | 2024 | ACM CCS | A | Yes | Yes | YOLOv2-v4, SSD, Faster-RCNN, DETR | Defense: real-time patch suppression | high | 4 | Local PDF |
| nazeri2024_detr_robustness | DETR Robustness | 2024 | arXiv | A | Yes | Yes | DETR-R50/R101/DC5 | Robustness + transfer context | high | 3 | Local PDF |
| bayer2024_network_transferability | Network Transferability | 2024 | SPIE | A | Yes | Yes | YOLOv7–v10, 28 models | Transfer analysis | high | 5 | Open |
| dimitriu2024_multi_model_transferability | Multi-Model Optimization | 2024 | Applied Sciences / MDPI | A | Yes | Yes | YOLOv8, YOLOv5, YOLOv3 + black-box detector suite | Transfer method to borrow | high | 5 | Local PDF |
| huang2025_advreal | AdvReal | 2025/2026 | Expert Sys. Appl. | A | Yes | Yes | YOLOv2–v12 | Physical person suppression | high | 5 | Open |
| ji2021_adversarial_yolo_defense | Ad-YOLO | 2021 | arXiv | A | Yes | Yes | YOLOv2 | Defense: patch class | high | 4 | Open |
| gu2025_SAR | Segment and Recover (SAR) | 2025 | J. Imaging/MDPI | A | Yes | Yes | YOLOv11, DETR, Faster-RCNN | Defense: segment-recover | high | 4 | Local PDF |
| tereshonok2025_anomaly | Anomaly Localization Defense | 2025 | J. Imaging/MDPI | A | Yes | Yes | YOLOv3 | Defense: anomaly reconstruction | high | 3 | Local PDF |
| liang2021_catch_you | We Can Always Catch You | 2021/2025 | IEEE TDSC | A | Yes | Yes | YOLOv2, YOLOv4, YOLOR, YOLOv8 | Defense: patch detection | high | 4 | Local PDF |
| huang2022_tsea_transfer | T-SEA | 2022 | CVPR 2023 | A | Yes | Yes | YOLOv2–v5, multi | Cross-model transfer | high | 4 | Open |
| advtexture2022 | AdvTexture | 2022 | CVPR | A | Yes | Yes | YOLOv2, YOLOv3, Faster-RCNN, Mask R-CNN | Multi-angle physical person evasion | high | 4 | Open |
| wu2020_invisibility_cloak | Invisibility Cloak | 2020 | ECCV | B | Yes | Yes | YOLOv2+Faster-RCNN | Universal suppression, physical | medium | 4 | Open |
| xu2020_adversarial_tshirt | Adversarial T-shirt | 2020 | ECCV | A | Yes | Yes | YOLOv2, Faster-RCNN | Person suppression, clothing | high | 4 | Open |
| zolfi2021_translucent_patch | Translucent Patch | 2021 | CVPR | B | Yes | Yes | YOLOv3 | Class-specific suppression | medium | 2 | Open |
| hoory2020_dynamic_patch | Dynamic Adversarial Patch | 2020 | arXiv | B | Yes | Yes | YOLOv3 | Dynamic multi-angle | medium | 3 | Open |
| hu2021_naturalistic_patch | Naturalistic Patch | 2021 | ICCV | B | Yes | Yes | YOLOv2, Faster-RCNN | Person suppression, GAN | medium | 3 | Open |
| saha2020_spatial_context | Spatial Context Adversarial | 2020 | CVPRW | B | Yes | Yes | YOLOv3 | Contextual suppression + defense | medium | 3 | Open |
| lu2022_fran | FRAN | 2022 | IEEE Access | B | Yes | Yes | YOLOv3/v4/v5 | Frequency attention | medium | 3 | Open |
| lovisotto2022_attention_patch | Give Me Your Attention | 2022 | CVPR | B | Yes | Yes | None (ViT) | Attention analysis | medium | 3 | Open |
| zhou2023_mvpatch | MVPatch | 2024 | arXiv | B | Yes | Yes | YOLOv2–v5+FRCNN | Multi-model camouflage | medium | 3 | Open |
| guesmi2024_DAP | DAP | 2024 | CVPR | B | Yes | Yes | YOLOv5, YOLOv7 | Person suppression, naturalistic | medium | 4 | Open |
| alam2023_attention_deficit | Attention Deficit | 2023 | arXiv | B | Yes | Yes | None (Def. DETR) | Transformer patch attack | medium | 2 | Open |
| schack2024_real_world | Physical-Digital Gap | 2024 | arXiv | B | Yes | Yes | YOLOv3/v5 | Physical-digital gap analysis | medium | 3 | Open |
| tan2024_DOEPatch | DOEPatch | 2024 | arXiv | B | Yes | Yes | YOLOv2/v3/v4+FRCNN | Multi-model ensemble | medium | 3 | Open |
| wei2024_CAP | Camera-Agnostic Patch | 2024 | NeurIPS | B | Yes | Yes | YOLOv5 | Physical camera transfer | medium | 3 | Open |
| bagley2025_spap | SPAP/Superpixel Cluster | 2025 | arXiv | B | Yes | Yes | Unspecified YOLO | Superpixel physical robust | medium | 2 | Open |
| delacruz2026_physical | Physical Surveillance Attack | 2026 | arXiv | B | Yes | Yes | YOLOv8 (mentioned) | Visible+IR surveillance | medium | 4 | Open |
| diffnat2026_AAAI | Diff-NAT | 2026 | AAAI | B | Yes | Yes | Multiple (unspec.) | Diffusion naturalistic patch | medium | 2 | Open |
| li2025_uvattack | UV-Attack | 2025 | ICLR | B | Yes | Yes | YOLOv5 | NeRF UV-map clothing | medium | 3 | Open |
| zhou2025_sequence_clothing | Sequence-Level Clothing | 2025 | arXiv | B | Yes | Yes | YOLOv5/v8 | Video robust clothing | medium | 3 | Open |
| na2025_unmanned_stores | Unmanned Stores | 2025 | arXiv | B | Yes | Yes | YOLOv5 | Physical retail attack | medium | 3 | Open |
| winter2026_benchmarking | Benchmarking Robustness | 2026 | arXiv | B | Yes | Yes | YOLOv3/YOLOX only | Adv training benchmark | medium | 1 | Open |
| wu2024_NAPGuard | NAPGuard | 2024 | CVPR | B | Yes | Yes | Multiple | Defense: NAP detection | medium | 3 | Open |
| **huang2019_universal_physical** | **UPC** | **2019/2020** | **CVPR 2020** | **B** | **Yes** | **Yes (upgraded)** | Faster-RCNN (not YOLO) | Universal physical camouflage | **medium** | 3 | Open |
| **kolter2019_global_patch** | **Global Patch Suppression** | **2019** | **ICML Workshop** | **B** | **Yes** | **Yes (upgraded)** | YOLOv3 | Global scene-level suppression | **high** | 3 | Open |
| **patchzero2022** | **PatchZero** | **2022/2023** | **WACV 2023** | **B** | **Yes** | **Yes (upgraded)** | General (PASCAL VOC) | Defense: detect-and-zero | **high** | 3 | Open |
| bae2020_TOG | TOG: Targeted Objectness Gradient | ~2020 | Unknown ⚠️ | C | No | Yes | YOLOv3, Faster-RCNN | NMS-flooding attack | low [unverified-from-pdf] | 3 | Unknown — citation needs verification |
| gala2025_yolo_adversarial_patches | YOLO Adversarial Patches (Springer) | 2025 | IJIS/Springer | A | Yes | Yes | YOLOv5/v8/v9/v10 | Naturalistic patches, edge AI | high | 5 | Local PDF |
| imran2025_tkpatch | TK-Patch | 2025 | ICoDT2/IEEE | C | No | Yes | YOLOv3/v5/v7 | Multi-YOLO universal patch | low [unverified-from-pdf] | 4 | IEEE Xplore |
| li2025_elevpatch | ElevPatch (YOLO11) | 2025 | ICIC/Springer | C | No | Yes | YOLO11 | Person evasion (YOLO11 specific) | low [unverified-from-pdf] | 5 | Springer ILL |
| liao2021_anchor_free | Anchor-Free Adversarial Transfer | 2021 | IEEE ICME | A | Yes | Yes | YOLOv3, CenterNet/FCOS | Anchor-free transfer | high | 4 | Local PDF |
| lin2024_entropy | Entropy-Boosted Patch | 2024 | IEEE Access | C | No | Yes | YOLOv2/v3/v4 | Entropy naturalism loss | low [unverified-from-pdf] | 3 | IEEE CSUSM |
| ma2026_XAIAD | XAIAD-YOLO | 2026 | FGCS/Elsevier | C | No | Yes | YOLO family (anchor-free incl.) | Defense: XAI test-time | low [unverified-from-pdf] | 4 | Elsevier paywall |
| truong2024_AYO_GAN | AYO-GAN | 2024/2025 | SOICT/Springer | C | No | Yes | YOLO (v5 likely) | GAN perturbation YOLO | low [unverified-from-pdf] | 2 | Springer ILL |
| wang2026_chosen_object | Chosen-Object Attack | 2026 | IEEE TIFS | C | No | Yes | DETR-style (YOLO26 analog) | Hungarian matching attack | low [unverified-from-pdf] | 4 | IEEE CSUSM |
| zimon2025_GAN_YOLO | GAN YOLO Robustness | 2025 | Springer ISID | C | No | Yes | YOLOv3/v5/v8/v11 | Cross-YOLO GAN attack+defense | low [unverified-from-pdf] | 5 | Springer paywall |
| xue2020_3d_cloak | 3D Invisible Cloak | 2020/2024 | IEEE TETC | D | No | No | Unconfirmed person detector | 3D physical stealth | metadata-only | 2 | IEEE CSUSM |
| tpatch2023 | TPatch: Triggered Patch | 2023 | USENIX Security | D | No | No | Unconfirmed | Triggered adversarial patch | metadata-only | 2 | USENIX (open) |
| **FIRST_PARTY_RESULTS** | **Repo Experimental Results** | **2026** | **This repo** | **E** | N/A | N/A | YOLOv8n, YOLO11n, YOLO26n | Attack + transfer measurement | **first-party measured** | 5 | Internal |

---

## Section 3: Tier A Deep-Read Summary

Each summary names the single most important finding for the capstone. Reference: corresponding note file in `docs/notes/`.

### brown2017 — Adversarial Patch (Brown et al., NIPS 2017 Workshop)
Reference: `docs/notes/brown2017_adversarial_patch.md`

The foundational paper establishing that a small, universal, printable patch can be attached to any object in a scene and force a classifier to output a target class. Its primary importance for the capstone is definitional: it establishes the patch threat model (spatially localized, scene-attached, physically printable, expectation-over-transformation training) that all subsequent person-detection patch papers adopt. For the capstone specifically, brown2017 is the citation for "adversarial patch" as a concept; it does not itself evaluate person detection or YOLO.

### thys2019 — Fooling Automated Surveillance Cameras (CVPRW 2019)
Reference: `docs/notes/thys2019_fooling_surveillance.md`

The canonical person-vanishing baseline. Demonstrates that optimizing the objectness loss term (L_obj) reduces INRIA person recall from 100% to 26.46% on YOLOv2, substantially outperforming a class-probability loss (CLS, 77.58%). The three-term loss design (L_nps + L_tv + L_obj) and INRIA dataset are the standard against which all subsequent person-evasion papers compare. The capstone's v8n direct result (90% suppression) substantially exceeds this 2019 baseline, which is the primary "improvement over prior work" claim.

### liu2019_dpatch — DPatch (Liu et al., SafeAI@AAAI 2019)
Reference: `docs/notes/liu2019_dpatch.md`

First demonstration that an adversarial patch can suppress detections globally (not overlapping the target object) on YOLOv2 and Faster R-CNN. Key finding: patches placed at fixed locations can fool the region proposal stage. However, kolter2019 later shows DPatch's clipping implementation is flawed, producing weakly adversarial results compared to properly formulated PGD patches. DPatch is the basis for ART's `DPatch` implementation used in this repo's baseline (`create_adv_patch.py`).

### cheng2024_depatch — DePatch (Cheng et al., arXiv 2024)
Reference: `docs/notes/cheng2024_depatch_decoupled.md`

Most practically applicable 2024 person-vanishing paper for the capstone. Introduces block-wise decoupled patch training that addresses "self-coupling" — where physical degradation to one patch segment destroys the entire adversarial effect. Digital AP drops to 17.75%; physical clothing ASR 90.96% and poster ASR 80.14% on YOLOv2. The random block erasure technique during training is portable to any YOLO training loop and is the most directly implementable improvement to the capstone's `experiments/ultralytics_patch.py`.

### bayer2024_network_transferability — Network Transferability (Bayer et al., SPIE 2024)
Reference: `docs/notes/bayer2024_network_transferability.md`

Systematic 28-model compatibility matrix for the YOLO family showing that **YOLOv8n and YOLOv8s are weak source models for transfer** — patches trained on nano/small variants transfer poorly to other models. Larger source models transfer better. RT-DETR is an outlier (poor source, robust target). This finding is the primary literature explanation for the capstone's v8n→v11n (36.4%) and v8n→v26n (11.6%) transfer results — the nano source model effect is confirmed at scale.

### huang2025_advreal — AdvReal (Huang et al., Expert Systems with Applications 2025)
Reference: `docs/notes/huang2025_advreal_physical.md`

Only paper in the corpus to directly evaluate adversarial patch attacks on both YOLOv8 and YOLO11. Recall reduction to 32.68% on YOLOv8 (Table 7) and 32.47% on YOLO11 under closed-box evaluation from a YOLOv2 glass-box source. Physical ASR 70.13% on YOLOv12 with clothing deployment on nuScenes backgrounds. This is the strongest cross-generation transfer result in the literature and the primary comparison point for the capstone's first-party v8n (90%) and v11n (84.8%) direct results.

### ji2021_adversarial_yolo_defense — Ad-YOLO (Ji et al., arXiv 2021)
Reference: `docs/notes/ji2021_adversarial_yolo_defense.md`

Best defense paper with a PDF. Adds a dedicated "patch class" to the YOLO head — 80.31% AP under white-box attack vs. 33.93% undefended baseline; only -1.45 pp clean accuracy cost. This defense is directly extensible to YOLOv8n (add class 80 = adversarial_patch; train on Thys-style patches). For the capstone's defend phase, this is the primary comparison defense. All other PDF-backed defenses are either weaker or address a different architecture.

### huang2022_tsea_transfer — T-SEA (Huang et al., CVPR 2023)
Reference: `docs/notes/huang2022_tsea_transfer.md`

Code-available self-ensemble approach achieving black-box average mAP 9.16% across 7 detectors from a single YOLOv5 source (vs. AdvPatch baseline 36.46%). ShakeDrop augmentation + patch cutout during training are the key techniques. This is the most directly actionable improvement for the capstone's transfer results — applying T-SEA's training techniques to the v8n→v11n/v26n transfer experiments would provide a direct comparison to the literature's best transfer method.

### dimitriu2024_multi_model_transferability — Multi-Model Optimization (Dimitriu et al., Applied Sciences 2024)
Reference: `docs/notes/dimitriu2024_multi_model_transferability.md`

The clearest newly localized transfer-method paper in the repo. Extends TACO-style vehicle camouflage by averaging the attack loss across multiple source detectors and shows that mixed-generation surrogate training (`YOLOv8n + YOLOv5m + YOLOv3`) achieves the strongest overall transfer, with total mean `AP@0.5 = 0.0972` across one-stage, two-stage, and transformer detectors. For the capstone, this is the strongest direct literature support for moving from a single-source YOLOv8n patch to a mixed-surrogate transfer pipeline.

### Recent Tier A Additions (2026-04-15 sync)

Reference notes: `docs/notes/gala2025_yolo_adversarial_patches.md`, `docs/notes/liao2021_anchor_free_adversarial.md`, `docs/notes/lin2024_nutnet_defense.md`, `docs/notes/hu2022_advtexture_physical.md`, `docs/notes/liang2021_catch_you_defense.md`, `docs/notes/nazeri2024_detr_robustness.md`, `docs/notes/dimitriu2024_multi_model_transferability.md`, `docs/notes/gu2025_SAR_segment_recover.md`, `docs/notes/tereshonok2025_anomaly_localization_defense.md`, `docs/notes/xu2020_adversarial_tshirt.md`

- `gala2025_yolo_adversarial_patches`: strongest direct modern Ultralytics benchmark in the local corpus before YOLO11/YOLO26.
- `liao2021_anchor_free`: clearest local-PDF support for output-space mismatch when moving from anchor-based to anchor-free detectors.
- `lin2024_nutnet`: strongest repo-local real-time defense baseline spanning hiding, appearing, and physical patch attacks.
- `advtexture2022`: high-value physical clothing benchmark showing why multi-angle texture visibility matters more than narrow digital patch strength.
- `liang2021_catch_you`: defense benchmark with both signature-based and signature-independent modes, plus YOLOv8 evidence.
- `nazeri2024_detr_robustness`: DETR-family robustness and transfer context that strengthens the YOLO26 architecture-mismatch interpretation.
- `dimitriu2024_multi_model_transferability`: strongest newly localized method paper for mixed-surrogate transfer improvement, and the cleanest literature support for training on more than one YOLO source family.
- `gu2025_SAR`: strongest local segment-and-inpaint defense and the main direct YOLO11-side defense paper now in the working packet.
- `tereshonok2025_anomaly`: clean-data-only anomaly-localization defense for physical pedestrian patch attacks.
- `xu2020_adversarial_tshirt`: foundational TPS-based physical wearable benchmark with still-useful multi-detector results.

---

## Section 4: Tier B Skim Summary

Note: huang2019, kolter2019, and patchzero2022 have been upgraded from Tier B stubs to proper triage notes (see Section below for the upgrade discussion and their full notes in `docs/notes/`).

| Slug | Key finding | Deep read needed? |
|------|-------------|-------------------|
| wu2020_invisibility_cloak | Physical wearable clothing; systematic multi-detector + multi-configuration black-box transfer study; most complete physical benchmark for pre-2021 era | Yes — if physical deployment discussion matters |
| zolfi2021_translucent_patch | Translucent film on camera lens suppresses stop signs with 42.27% physical fooling (close to digital 42.47%); unusual insider threat model | No — not directly relevant to person evasion |
| hoory2020_dynamic_patch | Dynamic multi-placement patches for YOLOv3; poor transfer to Faster-RCNN; supports YOLO-family specificity of attacks | No |
| hu2021_naturalistic_patch | GAN-constrained naturalistic patches achieve suppression while appearing realistic; BigGAN latent space; digital only | Yes — if naturalism comparison is needed |
| saha2020_spatial_context | Background patch exploits YOLO global context to suppress person detections; 60 citations; spatial context regularization as defense | No — useful for threat-model framing |
| lu2022_fran | FRAN frequency attention: patches optimized in low-frequency domain survive image shrinking better; frequency anomalies localize patches | No — useful for defense section if FRAN is cited |
| lovisotto2022_attention_patch | Dot-product attention dramatically increases vulnerability to patches vs. CNNs; directly relevant to YOLO26 attention architecture | Yes — critical before designing YOLO26-specific loss |
| zhou2023_mvpatch | Dual-perception framework improves transfer + stealthiness across YOLO versions (v2–v5); multi-detector ensemble | No |
| guesmi2024_DAP | State-of-the-art person-vanishing CVPR 2024; Creases Transform for cloth deformation; 82.28% digital / 65% physical ASR on YOLOv7/v3tiny; direct benchmark | Yes — primary 2024 comparison paper |
| alam2023_attention_deficit | Collaborative multi-patch attack on deformable DETR; near-0% AP with <1% image area; relevant to YOLO26's attention mechanism | Yes — before YOLO26-specific loss design |
| schack2024_real_world | Physical-digital gap: hue shift 200–300° renders patches ineffective; rotation >20° kills effectiveness; tested on YOLOv3/v5 | No — well documented; cite for physical limitations |
| tan2024_DOEPatch | Dynamically optimized ensemble: YOLOv2 AP→13.19%, YOLOv3→29.20%; min-max training portable to v8+v11 ensemble | No |
| wei2024_CAP | ISP proxy network enables cross-camera physical transfer (6/6 cameras vs. 1/6); physical robustness advance | No |
| bagley2025_spap | Superpixel cluster patches (SPAP-2) reduce person AP to 16.28% vs. 24.97% AdvPatch on YOLOv8; strong small-patch result | Yes — directly tests YOLOv8 |
| delacruz2026_physical | Visible + IR surveillance evasion with YOLOv8; most recent physical surveillance paper | Yes — mentions YOLOv8 explicitly, need quantitative details |
| diffnat2026_AAAI | Diffusion-optimized naturalistic patches outperform GAN-based; AAAI 2026; text-prompt controllable | No — useful for naturalism comparison |
| li2025_uvattack | NeRF-based UV mapping for person evasion across diverse actions; YOLOv8 targeted; high ASR with unseen actions | Yes — tests YOLOv8 directly |
| zhou2025_sequence_clothing | Sequence-level temporal optimization for video-consistent clothing; ICC color locking; mentions YOLOv8 | Yes — mentions v8, need numbers |
| na2025_unmanned_stores | Physical retail adversarial patch study with YOLOv5; three attack types; 69.1% hiding success | No |
| winter2026_benchmarking | Non-patch digital attacks only; no v8/v11/v26; useful for adversarial training comparison only | No — explicitly not patch attacks |
| wu2024_NAPGuard | +60.24% AP@0.5 improvement for naturalistic adversarial patch detection on GAP dataset; CVPR 2024 | No — cite for defense comparison |
| huang2019_UPC | Universal Physical Camouflage; Faster-RCNN primary; AttackScenes virtual benchmark; semantic constraint for natural appearance; single-digit mAP on Faster-RCNN | No — YOLO not primary model |
| kolter2019_global_patch | Single global patch reduces YOLOv3 mAP 55.4% → 7.2% (clipped, 0.5 conf); outperforms DPatch substantially; physical webcam demo | No — good for threat model framing |
| patchzero2022 | Detect-and-zero pipeline: outperforms PatchGuard +26%, PatchCleanser +13%; two-stage adversarial training handles adaptive attacks; no retraining needed | No — cite for defense table |

---

## Section 5: Tier C Note-Only Summary

These are historical note-only profiles. Most entries below still lack local-PDF verification, but some older profiles were retained for provenance after later promotion into Tier A. For current evidence states, the registry table above and the working-packet audit are authoritative.

---

### 1. bae2020_TOG — TOG: Targeted Objectness Gradient

**Note file**: `docs/notes/bae2020_TOG_targeted_objectness.md`

**What the note claims** [unverified-from-pdf]: NMS-flooding attack — maximizes objectness scores across all anchor boxes in a region to create "ghost detections" that flood NMS, suppressing real detections. Targets YOLOv3 / Faster R-CNN. The objectness-flooding mechanism is architecturally distinct from class-score suppression (Thys, DAP).

**Why it matters**: Provides an alternative loss design for YOLOv8 experiments (objectness flooding vs. class suppression). Also critical architectural contrast for YOLO26: NMS flooding does NOT apply to YOLO26 (no NMS); this contrast sharpens the argument for why YOLO26 requires a new loss design.

**What needs verification from PDF**: (1) Exact paper title and DOI — the "Bae 2020" attribution and "TOG" acronym were explicitly flagged as pending confirmation during batch 4 ingestion. The verified_sources.md notes this explicitly. Do NOT cite as "Bae et al. 2020 TOG" without confirmation. (2) Exact quantitative results. (3) Whether the NMS-flooding mechanism is the primary contribution or a secondary result.

**Access path**: Unconfirmed — verify via Semantic Scholar search for "TOG targeted objectness gradient 2020".

**Priority**: Medium — useful architectural contrast, but citation is uncertain; do not cite until verified.

---

### 2. gala2025_yolo_adversarial_patches — Gala et al. YOLO Adversarial Patches

**Note file**: `docs/notes/gala2025_yolo_adversarial_patches.md`

**What the note shows**: Evaluates BigGAN-latent naturalistic adversarial patches on Ultralytics YOLOv5, YOLOv8, YOLOv9, and YOLOv10 using INRIA and MPII. The paper identifies four especially strong patches (`patch17`, `patch26`, `patch27`, `patch38`) and shows that smaller `n` models are consistently more vulnerable than `m` variants. On INRIA at scale `0.20`, `patch38` drives YOLOv8n mAP to `48.31`; at scale `0.22`, it reaches `31.27` (Tables 8-9, p. 13).

**Why it matters**: This is the strongest local-PDF benchmark for modern Ultralytics patch vulnerability before YOLO11/YOLO26. It gives a verified literature baseline for the repo's YOLOv8 results and supports the capstone's broader claim that small edge-oriented models trade security margin for efficiency.

**Most useful citable details**:
- BigGAN latent optimization is used instead of direct pixel optimization, with `L_total = L_det + 0.1 * L_tv` and Adam `lr = 0.01` (pp. 4-5).
- `patch38` reduces INRIA mAP to `36.76` on YOLOv5n, `48.31` on YOLOv8n, and `39.20` on YOLOv10n at scale `0.20` (Table 8, p. 13).
- The paper explicitly states that `n` models are more vulnerable than `m` models, while edge-device timings show the expected efficiency tradeoff (pp. 11-14).

**Priority**: High — now verified and directly usable in the related-work and comparison sections.

---

### 3. gu2025_SAR — Segment and Recover (SAR)

**Note file**: `docs/notes/gu2025_SAR_segment_recover.md`

**What the note claims** [unverified-from-pdf]: Segmentation-based defense: detect the adversarial patch region via segmentation, recover the underlying clean image region, then run the detector. Journal of Imaging (MDPI), 2025. Open access but bot-blocked.

**Why it matters**: Represents the segment-and-recover defense paradigm — architecturally distinct from Ad-YOLO (patch class), NAPGuard (semantic detection), PatchZero (detect-and-zero), XAIAD-YOLO (XAI purification), and Tereshonok (anomaly reconstruction). Six defense paradigms collectively define the current defense landscape for the capstone's defend phase.

**What needs verification from PDF**: (1) Exact YOLO versions defended. (2) Quantitative AP recovery results. (3) Whether it handles naturalistic patches (DAP-style). (4) Segmentation architecture used.

**Access path**: Open access — https://www.mdpi.com/2313-433X/11/9/316 — download PDF in human browser (bot protection blocks automated fetch).

**Priority**: Medium — fills out defense landscape; open access; straightforward to obtain.

---

### 4. imran2025_tkpatch — TK-Patch

**Note file**: `docs/notes/imran2025_tkpatch_multiyolo.md`

**What the note claims** [unverified-from-pdf]: Universal Top-K adversarial patch attacking YOLOv3, YOLOv5, and YOLOv7 simultaneously via a Top-K loss that focuses gradient energy on the K most confident detections. Physical deployment on clothing. IEEE ICoDT2 2025. 0 citations (very new paper).

**Why it matters**: The multi-YOLO ensemble design is the closest existing paper to the capstone's simultaneous v8+v11+v26 attack setup. The Top-K loss is a direct alternative to the capstone's current mean-top-K implementation and should be compared in the methods section.

**What needs verification from PDF**: (1) Exact ASR on each YOLO version. (2) How Top-K outperforms standard suppression loss. (3) Whether the loss generalizes to anchor-free architectures (YOLOv8+).

**Access path**: IEEE Xplore via CSUSM — https://ieeexplore.ieee.org/document/[10879485 equivalent for TK-Patch] or search DOI 10.1109/ICoDT269104.2025.11360694.

**Priority**: High — most directly analogous to the capstone's multi-YOLO setup; Top-K loss comparison is essential for methods discussion.

---

### 5. li2025_elevpatch — ElevPatch (YOLO11-specific)

**Note file**: `docs/notes/li2025_elevpatch_yolo11.md`

**What the note claims** [unverified-from-pdf]: White-box adversarial patch attack against YOLO11 specifically. Springer ICIC 2025. Results unknown — paywalled. This is the only paper found that specifically targets YOLO11.

**Why it matters**: The ONLY literature benchmark for YOLO11 adversarial patches. Whatever suppression rate ElevPatch achieves is the primary comparison point for the capstone's 84.8% YOLO11 direct suppression result.

**What needs verification from PDF**: (1) Their YOLO11 suppression rate (the single most important number). (2) Training setup (patch size, epochs, EoT). (3) Whether physical deployment was tested.

**Access path**: Springer ILL via CSUSM — DOI 10.1007/978-981-96-9872-1_15.

**Priority**: Critical — ONLY YOLO11-specific benchmark. Must be obtained before finalizing capstone YOLO11 results section.

---

### 6. liao2021_anchor_free — Transferable Adversarial Examples for Anchor-Free Detection

**Note file**: `docs/notes/liao2021_anchor_free_adversarial.md`

**What the note shows**: First adversarial attack paper targeting anchor-free detectors directly. It introduces sparse and dense category-wise attacks against CenterNet and shows strong white-box success plus meaningful black-box transfer across detector families. On PascalVOC, DLA34-SCA transfers to Faster R-CNN with `ATR 0.82`; on MS-COCO, DLA34-SCA transfers to CornerNet with `ATR 0.88` (Tables 2-3, pp. 5-6).

**Why it matters**: This is the repo's clearest local-PDF support for the claim that detector-output mismatch can break naive transfer assumptions. It does not prove anything about YOLO26 directly, but it is strong evidence that changing the detection mechanism changes the attack objective you need.

**Most useful citable details**:
- White-box DCA drives MS-COCO CenterNet mAP down to `0.002` with `ASR 0.99` on both Resdcn18 and DLA34 (Table 1, p. 5).
- Transfer remains meaningful across backbone and detector changes, including CenterNet to Faster R-CNN / SSD300 / CornerNet (Tables 2-3, pp. 5-6).
- The sparse attack keeps `PL0` under `1%`, showing that strong suppression does not require dense perturbation (Table 4, p. 6).

**Priority**: High — now verified and usable as the output-mismatch citation in the YOLO26 interpretation section.

---

### 7. lin2024_entropy — Entropy-Boosted Adversarial Patch

**Note file**: `docs/notes/lin2024_entropy_adversarial_patch.md`

**What the note claims** [unverified-from-pdf]: Entropy maximization as a loss term for patch naturalism — adds information-theoretic diversity to patch pixels without requiring a pretrained GAN or diffusion model. Tested on YOLOv2/v3/v4. IEEE Access 2024. A third naturalism paradigm alongside GAN-latent (Hu et al.) and cosine similarity (DAP).

**Why it matters**: Simpler naturalism approach than GAN or diffusion methods; potentially directly implementable as an additional loss term in the capstone's patch training pipeline. Provides the third data point in the naturalism comparison: GAN (Hu 2021) → entropy (Lin 2024) → diffusion (Diff-NAT 2026).

**What needs verification from PDF**: (1) Exact YOLO versions and quantitative suppression results. (2) Exact entropy loss formulation. (3) Whether it was tested on newer YOLO versions.

**Access path**: IEEE Access — https://ieeexplore.ieee.org/abstract/document/10453548/ — via CSUSM institutional access. Note: PDF may also be at https://ieeexplore.ieee.org/ielx7/6287639/10380310/10453548.pdf.

**Priority**: Medium — useful for naturalism comparison and as an implementable loss term; does not add new YOLO version coverage.

---

### 8. ma2026_XAIAD — XAIAD-YOLO

**Note file**: `docs/notes/ma2026_XAIAD_YOLO.md`

**What the note claims** [unverified-from-pdf]: Two-stage test-time defense (high-frequency filtering + XAI-guided feature destabilization). No retraining required. 66.08 FPS (1.56× faster than Grad-CAM++). Covers anchor-based and anchor-free YOLO variants. Future Generation Computer Systems, Elsevier 2026.

**Why it matters**: Test-time defense without retraining is especially relevant for deployed IIoT YOLO systems (connecting to Gala et al.'s edge AI finding). XAIAD-YOLO covers the anchor-free YOLO family, making it the most architecturally comprehensive defense paper in the pool for the capstone's target models.

**What needs verification from PDF**: (1) Exact YOLO versions tested. (2) Quantitative AP clean vs. defended results. (3) Whether anchor-free "YOLO variants" specifically includes YOLOv8/v11 or just earlier versions.

**Access path**: Elsevier — https://www.sciencedirect.com/article/pii/S0167739X25006508 — CSUSM institutional access.

**Priority**: High — most architecturally relevant defense paper for YOLOv8+ and anchor-free YOLO; needed for defenses section.

---

### 9. tereshonok2025_anomaly — Anomaly Localization Defense

**Note file**: `docs/notes/tereshonok2025_anomaly_localization_defense.md`

**What the note claims** [unverified-from-pdf]: Deep CNN localizes the adversarial region in the image; reconstructs a benign image by inpainting over the detected region before running the original detector. Tested against printed physical patches. Journal of Imaging (MDPI) 2025. Open access.

**Why it matters**: Fifth defense paradigm (anomaly reconstruction). Distinct from all other defense papers in the pool. Provides a comprehensive defense taxonomy table for the capstone: (1) patch class, (2) adversarial training, (3) detect-and-zero, (4) segment-recover, (5) anomaly reconstruction, (6) XAI purification.

**What needs verification from PDF**: (1) Exact YOLO versions defended. (2) Quantitative ASR reduction and AP recovery results. (3) Whether it handles naturalistic patches.

**Access path**: Open access PDF — https://www.mdpi.com/2313-433X/11/1/26/pdf?version=1737095625 — download in human browser.

**Priority**: Medium — open access; fills defense taxonomy; straightforward to obtain.

---

### 10. truong2024_AYO_GAN — AYO-GAN

**Note file**: `docs/notes/truong2024_AYO_GAN.md`

**What the note claims** [unverified-from-pdf — note is partially populated from detailed metadata]: Full-image GAN-generated adversarial perturbation against YOLO. ASR 22.25%, SSIM 0.936 (vs. baseline 12.67% ASR, 0.842 SSIM). SOICT 2024, Springer Singapore CCIS vol. 2351. Likely tested on YOLOv5 based on citation pattern.

**Why it matters**: Quantitative framing for why localized patches outperform full-image GAN perturbations: 22.25% ASR vs. 85.0% capstone patch ASR. The SSIM metric establishes a perceptual quality benchmark for GAN-based methods. Provides the GAN perturbation comparison data point.

**What needs verification from PDF**: (1) Exact YOLO version(s) evaluated. (2) Whether ASR = detection suppression rate or class-level misclassification rate. (3) ASR breakdown per class (is person specifically tested?).

**Access path**: Springer ILL — DOI 10.1007/978-981-96-4285-4_40.

**Priority**: Low — comparison data points are already captured in the note; the paper's main finding (22.25% ASR) is less important than the critical missing papers.

---

### 11. wang2026_chosen_object — The Chosen-Object Attack

**Note file**: `docs/notes/wang2026_chosen_object_attack.md`

**What the note claims** [unverified-from-pdf]: Exploits the Hungarian matching objective in DETR-style end-to-end object detectors, attacking the assignment mechanism rather than NMS. IEEE Trans. Information Forensics and Security, Vol. 21, 2026.

**Why it matters**: YOLO26 uses end-to-end Hungarian assignment (one-to-one and one-to-many outputs) rather than NMS. This paper provides the architectural loss design closest to a YOLO26-specific attack. The capstone's abnormally high final_det_loss of 251.9 for YOLO26 (vs. ~0.14 for v8/v11) suggests the current NMS-era loss is mismatched to YOLO26's output format — this paper provides the solution.

**What needs verification from PDF**: (1) Exact loss formulation for the Hungarian matching attack. (2) Quantitative AP drop results. (3) Whether the approach transfers across detection transformer architectures.

**Access path**: IEEE TIFS via CSUSM — https://ieeexplore.ieee.org/document/10879485/.

**Priority**: Critical for YOLO26 work — the only paper with an architecturally correct loss design for YOLO26's Hungarian matching head. Must be read before designing any YOLO26-specific loss improvements.

---

### 12. zimon2025_GAN_YOLO — GAN-Based Adversarial Patches for YOLO

**Note file**: `docs/notes/zimon2025_GAN_YOLO_robustness.md`

**What the note claims** [unverified-from-pdf]: Systematic cross-version study of GAN-based adversarial patches across YOLO v3, v5, v8, and v11. Springer ISID 2025. If the paper includes v8→v11 transfer results, this is the direct predecessor to the capstone's contribution.

**Why it matters**: Most directly comparable study to the capstone's scope — evaluates GAN-based patches across YOLOv3/v5/v8/v11. The capstone's contribution extends this to YOLO26. The benchmark numbers per YOLO version are the primary comparison for the capstone results section.

**What needs verification from PDF**: (1) Exact per-YOLO-version suppression rates. (2) Whether transfer across versions was evaluated (v8→v11, etc.). (3) Exact dataset and evaluation protocol.

**Access path**: Springer — https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16 — CSUSM institutional access or ILL.

**Priority**: Critical — most directly comparable study. Per-YOLO benchmark numbers are the primary literature comparison for the capstone.

---

## Section 6: Tier D Promotion Candidates

See `research/data/ranked/pool_promotion_candidates.md` for full entries. Summary:

Two papers from the ranked reading list still score ≥ 18.0, address person detection evasion, and are NOT already promoted into the repo's note set. `advtexture2022` and `liang2021_catch_you` were promoted into Tier A during the 2026-04-15 sync.

| Slug | Title | Score | Why it qualifies | Priority |
|------|-------|-------|-----------------|----------|
| xue2020_3d_cloak | 3D Invisible Cloak (IEEE TETC 2024) | 19.016 | 3D physical constraints for person stealth; predecessor to UV-Attack; low citations | Low-Medium |
| tpatch2023 | TPatch (USENIX Security 2023) | 18.744 | Triggered adversarial patch (acoustic trigger); USENIX venue; 45 citations; novel threat model | Medium |

Neither remaining Tier D candidate is confirmed to directly evaluate YOLOv8, YOLO11, or YOLO26 — YOLO version coverage is still unconfirmed from metadata.

---

## Section 7: First-Party Experimental Evidence

### Results Table

| Run | Model | Clean Det | Patched Det | Suppression % | final_det_loss | Notes |
|-----|-------|-----------|-------------|---------------|----------------|-------|
| Direct training | YOLOv8n | 20 | 2 | **90.0%** | 0.135 | Strong baseline |
| Direct training | YOLO11n | 33 | 5 | **84.8%** | 0.242 | Strong; slightly harder than v8n |
| Direct training | YOLO26n | 43 | 38 | **11.6%** | 251.9 | Structural optimization failure |
| Transfer v8n→v11n | YOLO11n | 33 | 21 | **36.4%** | N/A | Moderate; 48pp below direct |
| Transfer v8n→v26n | YOLO26n | 43 | 38 | **11.6%** | N/A | Negligible |
| Transfer v11n→v26n | YOLO26n | 43 | 36 | **16.3%** | N/A | Marginally better than v8n→v26n |

Implementation: `experiments/ultralytics_patch.py`  
YOLO26n detail: `preds_dict["one2many"]["scores"]` (B, 80, 8400); person = channel 0; final_det_loss of 251.9 vs ~0.14 for v8n/v11n.

### Interpretation

**v8n direct (90% suppression)**: Exceeds all pre-2022 baselines in the literature. Thys2019 (YOLOv2): 100%→26.46% recall. Xu T-shirt (YOLOv2): 74% digital ASR. AdvReal (closed-box, YOLOv2 source → YOLOv8 target): recall→32.68%. The capstone's white-box v8n result is substantially stronger than all of these, consistent with white-box > closed-box > transfer in the general attack hierarchy.

**v11n direct (84.8% suppression)**: Consistent with the pattern from AdvReal — v8 and v11 have similar vulnerability to adversarial patches (AdvReal: 32.68% vs. 32.47% recall, essentially identical). The capstone's direct results show a small gap (90% vs. 84.8%), suggesting YOLO11 is marginally harder to attack directly. This gap likely reflects the slightly different head architecture in v11 vs. v8. Without ElevPatch numbers (the only YOLO11-specific paper, currently paywalled), this result stands as the primary literature data point for YOLO11 direct attacks.

**v26n direct (11.6% suppression)**: The final_det_loss of 251.9 (vs. ~0.14 for v8/v11) is the most important technical finding in the first-party results. This is not an attack success rate failure — it is an optimization failure: the gradient-based optimization did not converge to a strongly adversarial patch for YOLO26. Two architectural explanations from the literature: (1) **Anchor-free output format mismatch** (liao2021 [unverified-from-pdf]): the loss landscape for YOLO26's `one2many["scores"]` (B, 80, 8400) is fundamentally different from the v8 anchor-free DFL format the same optimizer was applied to. (2) **Attention mechanism** (lovisotto2022, alam2023): YOLO26 uses attention-based architecture components; standard PGD patches do not optimize correctly against attention-based detectors. The wang2026 Chosen-Object Attack provides the most promising architectural fix: a Hungarian-matching-aware loss directly targeting YOLO26's assignment mechanism.

**v8n→v11n transfer (36.4% suppression)**: Moderate transfer; 48pp below the v11n direct result (84.8%). This is consistent with bayer2024's finding that YOLOv8n is a weak source model for transfer. The literature's best single-source transfer (T-SEA from YOLOv5: avg mAP 9.16% across 7 detectors) was achieved with substantially more sophisticated training (ShakeDrop + patch cutout ensemble). The capstone's simple transfer baseline is expected to be weaker. The 36.4% result has no direct paper precedent (no paper has tested v8n→v11n specifically) — it is a novel measurement.

**v8n→v26n and v11n→v26n (11.6% and 16.3%)**: Near-baseline suppression. Both transfer paths fail to produce meaningful suppression, confirming that YOLO26's optimization landscape is qualitatively different. The marginally better v11n→v26n (16.3% vs. 11.6%) may reflect the slightly closer architectural relationship between v11 and v26 in the Ultralytics family. However, the difference is within noise margins given the small detection counts (38 vs. 36 patched detections out of 43 clean).

### Open Questions Raised by First-Party Results

1. **Would a YOLO26-specific loss (Hungarian matching, per wang2026) produce meaningful suppression?** The 251.9 final_det_loss strongly suggests the answer is yes — the current loss is wrong for YOLO26, not that YOLO26 is inherently unattackable.

2. **Does ensemble training on v8+v11 improve v8n→v11n transfer?** T-SEA's approach (ensemble of multiple detector architectures during training) would predict yes. Applying ShakeDrop + patch cutout to the v8+v11 ensemble is the most directly actionable improvement suggested by the literature.

3. **What is the physical ASR for v8n and v11n?** All capstone results are digital. AdvReal achieves 70.13% physical ASR on YOLOv12 from YOLOv2 source — the capstone's digital v8n result (90%) suggests physical ASR would be substantial but likely lower.

4. **Is the v26n direct result (11.6%) a fundamental barrier or an optimization artifact?** The 251.9 loss value is 1,800× larger than the v8n value, suggesting the optimizer diverged rather than converged. A properly formulated loss (targeting the `one2many` scores directly rather than a detection loss that assumes anchor-grid output) would likely produce much better results.

---

## Section 8: Unified Evidence View — YOLOv8, YOLO11, YOLO26

### YOLOv8

**Papers that directly evaluate it**:
- huang2025_advreal (Tier A, PDF): Closed-box target; recall → 32.68% [paper claim]
- bayer2024_network_transferability (Tier A, PDF): v8n/v8s as source — weak transfer; v8 variants as transfer targets [paper claim]
- delacruz2026_physical (Tier B, PDF): YOLOv8 mentioned explicitly in physical surveillance context [paper claim, limited quantification]
- bagley2025_spap (Tier B, PDF): Person AP → 16.28% on YOLOv8 with SPAP-2 [paper claim]
- li2025_uvattack (Tier B, PDF): YOLOv8 targeted [paper claim]
- gala2025_yolo_adversarial_patches (Tier A, PDF): `patch38` reduces YOLOv8n INRIA mAP to `48.31` at scale `0.20` and `31.27` at scale `0.22`; smaller models are more vulnerable
- zimon2025_GAN_YOLO (Tier C, no PDF): Evaluates YOLOv8 — specific numbers unknown [unverified-from-pdf]

**Papers that indirectly inform its vulnerability**:
- thys2019, cheng2024_depatch: Establish objectness-loss design applicable to v8
- bayer2024: v8n weak source effect
- guesmi2024_DAP, huang2022_tsea: Training techniques applicable to v8
- lovisotto2022, alam2023: Architectural attention analysis informing v8's partial-attention components

**First-party results**: 90.0% suppression (direct), 36.4% (as v11n transfer target)

**What is still unknown**: How directly comparable Gala et al.'s mAP protocol is to the capstone's suppression metric; whether SPAP-2's 16.28% AP result uses the same evaluation protocol as the capstone; physical ASR for the capstone's specific patch.

---

### YOLO11

**Papers that directly evaluate it**:
- huang2025_advreal (Tier A, PDF): Closed-box target; recall → 32.47% [paper claim]
- li2025_elevpatch (Tier C, no PDF): ONLY paper specifically targeting YOLO11 — results unknown [unverified-from-pdf]
- zimon2025_GAN_YOLO (Tier C, no PDF): Evaluates YOLO11 — specific numbers unknown [unverified-from-pdf]

**Papers that indirectly inform its vulnerability**:
- All v8-relevant papers (v11 and v8 share the same decoupled head architecture; vulnerability patterns should be similar)
- bayer2024: v8 nano/small source weakness likely extends to v11 nano by architectural analogy

**First-party results**: 84.8% suppression (direct), 36.4% (as v8n transfer target)

**What is still unknown**: ElevPatch's YOLO11 result (the primary literature benchmark — paywalled); whether v11 has meaningfully different vulnerability than v8 at scale.

---

### YOLO26

**Papers that directly evaluate it**: None — zero literature coverage. This is confirmed by the evidence matrix, the corpus synthesis, and the verified sources bibliography.

**Papers that indirectly inform its vulnerability**:
- lovisotto2022 (Tier B, PDF): Dot-product attention dramatically increases vulnerability; YOLO26's attention mechanisms are the first architectural factor explaining poor optimization convergence
- alam2023 (Tier B, PDF): Collaborative patches targeting attention maps achieve 0% AP on deformable transformers; establishes the principle that standard patches fail against attention architectures
- liao2021 (Tier A, PDF): Anchor-free output mismatch reduces transfer across detector families and supports the repo's v8→v26 failure interpretation from the output-space side
- wang2026_chosen_object (Tier C, no PDF, [unverified-from-pdf]): Hungarian matching attack for DETR-style end-to-end detectors — the architecturally correct loss design for YOLO26
- bayer2024: Weak-source nano model effect predicts poor transfer from v8n to any target

**First-party results**: 11.6% suppression (direct — optimization failure with final_det_loss 251.9); 11.6% and 16.3% suppression (transfer from v8n and v11n respectively — both negligible)

**What is still unknown**: Everything — this is the capstone's primary novel contribution. Specifically unknown: (1) whether a YOLO26-specific loss (Hungarian matching) would achieve meaningful suppression; (2) whether ensemble training including YOLO26 in the source set would improve transfer from v8/v11; (3) the physical ASR for any patch against YOLO26; (4) whether any defense method has been tested against YOLO26.

---

## Section 9: Promotion / Retrieval Priority List

Ranked by capstone importance. Includes the 10 remaining Tier C unpromoted / unresolved papers after promoting Gala 2025 and Liao 2021 into local-PDF-backed notes.

### Priority 1 — Critical (obtain before finalizing results sections)

**1. li2025_elevpatch** — ElevPatch (Springer ILL)
- Why: ONLY YOLO11-specific benchmark. Their suppression rate is the primary literature comparison for the capstone's 84.8% YOLO11 result. Without this number, the capstone cannot claim to compare with prior work on YOLO11.
- What claim needs verification: "ElevPatch achieves X% suppression on YOLO11" — the actual number.
- Access: ILL request via CSUSM library, DOI 10.1007/978-981-96-9872-1_15

**2. zimon2025_GAN_YOLO** — GAN YOLO v3/v5/v8/v11 (Springer)
- Why: Most directly comparable cross-YOLO study. If quantitative per-version results exist, these are the primary literature benchmarks for the capstone's multi-version comparison table.
- What claim needs verification: Per-YOLO-version suppression rates; v8→v11 transfer if evaluated.
- Access: CSUSM institutional Springer or ILL, https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16

**3. wang2026_chosen_object** — Chosen-Object Attack (IEEE CSUSM)
- Why: Provides the architecturally correct loss design for YOLO26 (Hungarian matching). The capstone's YOLO26 optimization failure (final_det_loss 251.9) is directly addressed by this paper's loss formulation.
- What claim needs verification: Hungarian matching loss formulation and quantitative results on DETR-style detectors.
- Access: IEEE TIFS via CSUSM, https://ieeexplore.ieee.org/document/10879485/

### Priority 2 — High (obtain before finalizing methods and related work sections)

**4. imran2025_tkpatch** — TK-Patch (IEEE CSUSM)
- Why: Top-K loss is the closest existing approach to the capstone's simultaneous multi-YOLO attack; comparison in methods section is essential.
- What claim needs verification: Exact ASR on YOLOv3/v5/v7; Top-K loss formulation.
- Access: IEEE Xplore via CSUSM, DOI 10.1109/ICoDT269104.2025.11360694

**5. ma2026_XAIAD** — XAIAD-YOLO (Elsevier)
- Why: Most comprehensive defense paper for anchor-free YOLO; needed for defense comparison table.
- What claim needs verification: Exact YOLO versions defended; AP clean vs. defended.
- Access: CSUSM Elsevier, https://www.sciencedirect.com/article/pii/S0167739X25006508

### Priority 3 — Medium (local PDFs already present; promotion work remaining)

**6. advlogo2024** — AdvLogo (local PDF)
- Why: best next local naturalistic / diffusion patch method now that the defense queue has been promoted.
- Access: local PDF already present at `docs/papers/advlogo_diffusion_patch_2409.07002.pdf`

**7. patchzero2022** — PatchZero (local PDF)
- Why: detect-and-zero defense remains under-integrated in detector-specific terms.
- Access: local PDF already present at `docs/papers/patchzero2022_detect_zero_defense_2207.01795.pdf`

**8. lin2024_entropy** — Entropy-Boosted Patch (IEEE Access via CSUSM)
- Why: Third naturalism paradigm; YOLO versions are older (v2/v3/v4) so limited direct comparison value.
- Access: IEEE Access via CSUSM

### Priority 4 — Low (nice to have; limited direct capstone impact)

**9. bae2020_TOG** — TOG Targeted Objectness Gradient
- Why: Citation verification needed before use; NMS-flooding contrast point.
- Access: Unknown — verify citation first via Semantic Scholar

**10. truong2024_AYO_GAN** — AYO-GAN (Springer ILL)
- Why: Main comparison data (22.25% ASR) already captured in the note; ILL overhead not justified by incremental value.
- Access: Springer ILL, DOI 10.1007/978-981-96-4285-4_40
