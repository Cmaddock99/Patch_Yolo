# Master Literature Summary: Adversarial Patches Against YOLO
*Running document — last updated 2026-04-15 (working-packet sync)*
*Sources: Original papers, arXiv full text, CVPR/ICCV open access pages, GitHub repos, CSUSM library*

---

## How to Use This Document

This is the living synthesis document for the capstone. Every paper processed gets a row in the table and a dedicated note file under `docs/notes/`. When new papers are read, add them here.

- For full method details, loss terms, and numbers: see the individual note files.
- For source verification: see `verified_sources.md`.
- For original PDFs: see `docs/papers/`.
- Working-packet sync for this pass: 25 promoted notes (`24 page_cited`, `1 pdf_verified`) and 3 blockers explicitly bounded (`3 blocked_access`).

## Working-Packet Sync

- The first-pass notes for Bayer, AdvReal, T-SEA, DOEPatch, Lovisotto, Alam, CAP, Schack, and DePatch are no longer stub-level working notes.
- Newly promoted local-PDF notes in this pass: Gala 2025, Liao 2021, Lin 2024 NutNet, Hu 2022 AdvTexture, Liang 2021 Catch You, Nazeri 2024 DETR robustness, Dimitriu 2024 multi-model transferability, Gu 2025 SAR, Tereshonok 2025 anomaly localization, Xu 2020 Adversarial T-shirt, and Ji 2021 Ad-YOLO.
- The blocker notes for Chosen-Object, ElevPatch, and Zimon should not be treated as promoted benchmark evidence in repo-first mode.
- Where this document still uses older labels such as `Fully processed` or `Stub`, defer to the note-level evidence state and the working packet audit.

---

## Paper Coverage Map

| Paper | Year | Note File | PDF | Status |
|---|---|---|---|---|
| Brown et al. — Adversarial Patch | 2017 | `notes/brown2017_adversarial_patch.md` | `papers/brown2017_adversarial_patch_1712.09665.pdf` | Fully processed |
| Liu et al. — DPatch | 2019 | `notes/liu2019_dpatch.md` | `papers/liu2019_dpatch_1806.02299.pdf` | Fully processed |
| Thys et al. — Fooling Surveillance Cameras | 2019 | `notes/thys2019_fooling_surveillance.md` | `papers/thys2019_fooling_surveillance_1904.08653.pdf` | Fully processed |
| Huang et al. — Universal Physical Camouflage | 2019 | `notes/huang2019_universal_physical_camouflage.md` | `papers/huang2019_universal_physical_camouflage_1909.04326.pdf` | Processed baseline |
| Hoory et al. — Dynamic Adversarial Patch | 2020 | `notes/hoory2020_dynamic_patch.md` | `papers/hoory2020_dynamic_patch_2010.13070.pdf` | Fully processed |
| Hu et al. — Naturalistic Physical Patch | 2021 | `notes/hu2021_naturalistic_patch.md` | `papers/hu2021_naturalistic_patch_ICCV.pdf` | Processed (abstract+method; full numbers in PDF) |
| Zolfi et al. — Translucent Patch | 2021 | `notes/zolfi2021_translucent_patch.md` | `papers/zolfi2021_translucent_patch_2012.12528.pdf` | Fully processed |
| Hu et al. — AdvTexture | 2022 | `notes/hu2022_advtexture_physical.md` | `papers/advtexture_person_detectors_2203.03373.pdf` | `page_cited` — multi-angle physical benchmark |
| Liang et al. — Catch You Defense | 2021/2025 | `notes/liang2021_catch_you_defense.md` | `papers/we_can_always_catch_you_2106.05261.pdf` | `page_cited` — defense benchmark |
| Schack et al. — Real-world Challenges | 2024 | `notes/schack2024_real_world_challenges.md` | `papers/schack2024_real_world_challenges_2410.19863.pdf` | Fully processed |
| Gala et al. — YOLO Models IJIS 2025 | 2025 | `notes/gala2025_yolo_adversarial_patches.md` | `papers/gala2025_adversarial_patch_yolo_edge_s10207.pdf` | `page_cited` — modern Ultralytics benchmark |
| Guesmi et al. — DAP | 2024 | `notes/guesmi2024_DAP_dynamic_adversarial_patch.md` | `papers/guesmi2024_DAP_CVPR.pdf` | Fully processed |
| Wu et al. — NAPGuard | 2024 | `notes/wu2024_NAPGuard.md` | `papers/wu2024_NAPGuard_CVPR.pdf` | Processed (abstract+method) |
| Tan et al. — DOEPatch | 2024 | `notes/tan2024_DOEPatch.md` | `papers/tan2024_DOEPatch_2312.16907.pdf` | Fully processed |
| Lin et al. — NutNet | 2024 | `notes/lin2024_nutnet_defense.md` | `papers/realtime_defense_diverse_patches_2406.10285.pdf` | `page_cited` — real-time defense baseline |
| Nazeri et al. — DETR Robustness | 2024 | `notes/nazeri2024_detr_robustness.md` | `papers/detection_transformers_robustness_2412.18718.pdf` | `page_cited` — DETR robustness / transfer context |
| DelaCruz et al. — Surveillance Survey | 2026 | `notes/delacruz2026_physical_attacks_surveillance.md` | `papers/delacruz2026_physical_attacks_surveillance_2604.06865.pdf` | Processed (abstract; check PDF for full survey) |
| Winter et al. — Benchmarking Robustness | 2026 | `notes/winter2026_benchmarking_robustness.md` | `papers/winter2026_benchmarking_robustness_2602.16494.pdf` | Processed ⚠️ non-patch only |
| Na et al. — Unmanned Stores | 2025 | `notes/na2025_unmanned_stores.md` | `papers/na2025_unmanned_stores_2505.08835.pdf` | Fully processed |
| Wei et al. — Camera-Agnostic Patches (CAP) | 2024 | `notes/wei2024_camera_agnostic_CAP.md` | `papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf` | Fully processed |
| Bagley et al. — SPAP/SPAP-2 | 2025 | `notes/bagley2025_dynamically_optimized_clusters.md` | `papers/bagley2025_dynamically_optimized_clusters_2511.18656.pdf` | Fully processed |
| Li et al. — Diff-NAT | 2026 | `notes/diffnat2026_AAAI.md` | `papers/diffnat2026_AAAI.pdf` | Fully processed |
| Ma et al. — XAIAD-YOLO | 2026 | `notes/ma2026_XAIAD_YOLO.md` | No PDF (Elsevier paywall) | Processed (abstract+method; numbers need institutional access) |
| Zimoň — GAN YOLO v3/v5/v8/v11 | 2025 | `notes/zimon2025_GAN_YOLO_robustness.md` | No PDF (Springer paywall) | `blocked_access` — near-scope predecessor, numbers unavailable |
| Lin et al. — Entropy Patch | 2024 | `notes/lin2024_entropy_adversarial_patch.md` | No PDF (IEEE Access paywall) | Access-limited — quantitative details pending |
| Truong et al. — AYO-GAN | 2024 | `notes/truong2024_AYO_GAN.md` | No PDF (Springer paywall) | Access-limited — quantitative details pending |
| Gu & Jafarnejadsani — SAR | 2025 | `notes/gu2025_SAR_segment_recover.md` | `papers/gu2025_SAR_segment_recover_jimaging316.pdf` | `page_cited` — detector-agnostic defense baseline |
| Ilina et al. — Anomaly Localization | 2025 | `notes/tereshonok2025_anomaly_localization_defense.md` | `papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf` | `page_cited` — clean-data-only defense baseline |
| Bayer et al. — Network Transferability | 2024 | `notes/bayer2024_network_transferability.md` | `papers/bayer2024_network_transferability_2408.15833.pdf` | `page_cited` — transfer benchmark |
| Dimitriu et al. — Multi-Model Optimization | 2024 | `notes/dimitriu2024_multi_model_transferability.md` | `papers/dimitriu2024_multi_model_transferability_app142311423.pdf` | `page_cited` — transfer method to borrow |
| Huang et al. — T-SEA | 2022 | `notes/huang2022_tsea_transfer.md` | `papers/huang2022_tsea_transfer_2211.09773.pdf` | `page_cited` — transfer method |
| Lovisotto et al. — Attention Patch Robustness | 2022 | `notes/lovisotto2022_attention_patch_robustness.md` | `papers/lovisotto2022_attention_patch_robustness_CVPR.pdf` | `page_cited` — attention mechanism |
| Alam et al. — Attention Deficit | 2023 | `notes/alam2023_attention_deficit_deformable.md` | `papers/alam2023_attention_deficit_2311.12914.pdf` | `page_cited` — deformable-attention mechanism |
| Wang et al. — Chosen-Object Attack | 2026 | `notes/wang2026_chosen_object_attack.md` | CSUSM IEEE access (no local PDF) | `blocked_access` — Hungarian-matching blocker |
| Liao et al. — Anchor-Free Adversarial | 2021 | `notes/liao2021_anchor_free_adversarial.md` | `papers/transferable_anchor_free_2106.01618.pdf` | `page_cited` — anchor-free mismatch reference |
| Xu et al. — Adversarial T-shirt | 2020 | `notes/xu2020_adversarial_tshirt.md` | `papers/xu2020_adversarial_tshirt_1910.11099.pdf` | `page_cited` — primary physical benchmark |
| Huang et al. — AdvReal | 2025 | `notes/huang2025_advreal_physical.md` | `papers/huang2025_advreal_physical_2505.16402.pdf` | `page_cited` — physical benchmark |
| Li et al. — ElevPatch YOLO11 | 2025 | `notes/li2025_elevpatch_yolo11.md` | ILL needed | `blocked_access` — only YOLO11-specific paper |
| Ji et al. — Adversarial YOLO defense | 2021 | `notes/ji2021_adversarial_yolo_defense.md` | `papers/ji2021_adversarial_yolo_defense_2103.08860.pdf` | `page_cited` — direct YOLO defense benchmark |
| Wu et al. — Invisibility Cloak | 2020 | `notes/wu2020_invisibility_cloak.md` | `papers/wu2020_invisibility_cloak_1910.14667.pdf` | Stub — physical transfer study |
| Zhou et al. — MVPatch | 2023 | `notes/zhou2023_mvpatch.md` | `papers/zhou2023_mvpatch_2312.17431.pdf` | Stub — transfer + stealth benchmark |

**External summary (ChatGPT-generated, imported):** `docs/research/executive_summary_chatgpt.md`
**Full batch 4 compilation:** `docs/research/batch4_literature_expansion.md`
**Verification error correction log:** `docs/research/unverified_paper_claims.md`

---

## Synthesis: What the Literature Tells Us

### 1. The Canonical Attack Pipeline (all papers agree on this)

1. Start with a pretrained YOLO detector (weights frozen).
2. Initialize a patch (random noise, or a GAN-sampled latent vector for naturalistic patches).
3. In each batch: apply random differentiable transforms to the patch (rotate ±20°, scale ±20%, gaussian noise, brightness/contrast jitter), overlay it at a target location on each image.
4. Forward pass through YOLO; compute a detection-suppression loss.
5. Backpropagate gradients to the patch only; update with Adam (LR ~0.01–5.0).
6. Repeat for 500–5000 iterations.

### 2. Loss Function Evolution

| Paper | Loss Design | Key Insight |
|---|---|---|
| Brown et al. (2017) | Cross-entropy to target class | EoT (random transforms) makes patches physically robust |
| Liu et al. / DPatch (2019) | Maximize classification + bbox regression loss jointly | Position-independence; attacks both localization and classification |
| Thys et al. (2019) | L_obj + L_tv + L_nps | **Objectness loss alone > class probability loss**; printability and smoothness constraints matter |
| Zolfi et al. (2021) | ℓtarget_conf + ℓIoU + ℓuntargeted_conf + ℓnps | Class-selective: suppress one class, preserve all others |
| Hu et al. (2021) | Objectness loss + GAN latent prior | Latent space optimization makes patches look natural |
| Gala et al. (2025) | Follows Hu et al., adapted for Ultralytics | Extends to YOLOv5/v8/v9/v10 |

**Key finding from Thys et al.**: Minimizing objectness score directly is more effective than minimizing class probability (26.46% recall vs. 77.58% for CLS-only). This is the recommended loss for a person-vanishing attack.

### 3. Datasets

| Dataset | Used By | What For |
|---|---|---|
| INRIA Persons | Thys, Hu, Gala | Person detection training and evaluation |
| MS COCO | DPatch, Hoory, Hu, Gala | Multi-class detection benchmarking |
| Pascal VOC | DPatch | mAP measurement baseline |
| MPII Human Pose | Gala | Person evaluation |
| LISA / MTSD / BDD | Zolfi | Stop sign detection (driving) |
| KITTI | Zolfi (mentioned) | Autonomous driving scenes |

**For my capstone**: INRIA Persons is the standard dataset for person-vanishing attacks and is used by both Thys et al. and Gala et al. — the two most directly relevant papers.

### 4. Metrics Used

| Metric | Meaning | Used By |
|---|---|---|
| AP (Average Precision) | Area under precision-recall curve for one class | Thys, Zolfi, Gala |
| mAP | Mean AP across all classes | DPatch, Schack, Gala |
| Recall | Fraction of true detections found | Thys |
| Fooling Rate | % of target objects no longer detected (IoU>0.5) | Zolfi, Hoory |
| Detection Confidence | Raw YOLO confidence score | Schack (local patches) |

**Recommended metric set for my capstone**: AP and Recall for the person class (clean vs. patched), plus fooling rate. mAP across all classes if using a multi-class dataset.

### 5. Physical-World Findings

| Paper | Physical Setup | Key Physical Finding |
|---|---|---|
| Brown et al. | Printed patch, photographed | Works when printed and photographed |
| Thys et al. | Printed ~40cm×40cm cardboard held by person | Filmed in real scenarios; OBJ patch was effective |
| Hoory et al. | 32"/28" screens on car, filmed in parking lot | 80% success indoors; drops to 15–23% outdoors (glare) |
| Zolfi et al. | Transparent film on webcam lens | 42.27% fooling rate (matches digital 42.47%) |
| Schack et al. | Controlled indoor lab | **Large digital-to-physical gap**; >20° rotation kills effectiveness; brightness increase causes up to 64% performance gap |

**Critical physical-world insight from Schack et al.**: Patches optimized purely digitally degrade significantly under real-world conditions. For a physically-tested capstone, rotation tolerance (±30° is safe), patch size (bigger is better), and consistent lighting are the key variables to control.

### 6. Cross-Version Transfer

| Patch Trained On | Tested On | Transfer Result |
|---|---|---|
| YOLO (DPatch) | Faster R-CNN | Moderate transfer |
| Faster R-CNN (DPatch) | YOLO | Moderate transfer |
| YOLOv5 (Zolfi) | YOLOv2, Faster R-CNN | 57% and 54% stop sign AP (from 81% and 94% clean) |
| YOLOv2 (Hoory) | YOLOv3 | 10–14% success (poor) |
| YOLOv2 (Hoory) | Fast R-CNN, Mask R-CNN | No meaningful transfer |

**Key gap**: No paper has tested patch transfer across YOLOv8 → YOLO11 → YOLO26. This is my capstone's primary research contribution.

### 7. Model Size and Robustness

From Gala et al. (2025): **Larger models are more robust to adversarial patches than smaller models.** This has direct implications for Edge AI, where small (n/s) models are preferred for speed but are the most vulnerable. My capstone should test this across yolov8n/s/m and yolo11n/s/m comparisons.

---

## Key Numbers Quick Reference

| Paper | Setting | Key result | Why it matters |
|---|---|---|---|
| This project (YOLOv8) | Digital person suppression | **90.0%** suppression | Already stronger than the classic Xu 2020 physical benchmark on YOLOv2 |
| This project (YOLOv8 -> YOLOv11) | Cross-generation transfer | **36.4%** suppression | Confirms partial within-family transfer without retraining on YOLO11 |
| This project (YOLOv8 -> YOLO26) | Cross-generation transfer | **11.6%** suppression | The core result Batch 4 now helps explain |
| DPatch (YOLO) | Untargeted detector attack | 65.7% mAP -> <1% mAP | Canonical detector-specific patch baseline |
| Thys et al. (OBJ loss) | Person vanishing | 100% recall -> **26.46% recall** | Core objectness-loss benchmark for hiding persons |
| Xu et al. (2020) | Physical T-shirt on YOLOv2 | **74% digital ASR; 57% physical ASR** | Foundational physical benchmark for person evasion |
| Wu et al. (2020) | Cross-model / physical patch study | Digital AP drops by at least 29%, down to 7.5% AP on retrained YOLOv2 | Strong evidence that digital success, transfer, and physical success are different problems |
| Bayer et al. (2024) | Cross-model transfer across real-time detectors | Larger source models transfer best; YOLOv8n / YOLOv8s source patches are among the weakest transfer sources | Best integrated explanation for why v8n-trained patches under-transfer |
| Lovisotto et al. (2022) | Attention-Fool on transformers | 0.5% patch can drive ViT robust accuracy to 0% and DETR mAP below 3% | Shows attention changes both vulnerability and the correct optimization target |
| Alam et al. (2023) | Collaborative patches on deformable transformers | 0% AP with <1% of the image perturbed | Closest attention-specific benchmark to the YOLO26 problem |
| AdvReal (2025) | Physical benchmark on YOLO-family detector | **70.13% ASR** on YOLOv12; >90% ASR at 4m frontal / oblique | Current physical benchmark to cite against modern YOLO-family systems |

---

## Open Research Gaps (as of 2026-04-15)

1. **YOLO26 still lacks a dedicated adversarial-patch paper** — Batch 4 now covers attention, anchor-free outputs, and Hungarian matching separately, but not as one YOLO26-targeted study.
2. **Cross-generation transfer (v8->v11->v26)** — no paper yet measures transfer across these three Ultralytics generations with one common dataset and metric stack.
3. **YOLO11 remains thinly covered** — ElevPatch is still the only dedicated YOLO11 paper in the current repo literature.
4. **Physical robustness of Ultralytics models is still open** — Xu, Wu, Schack, and AdvReal provide physical baselines, but the physical gap for v8/v11/v26 remains unmeasured.
5. **Model-size and architecture effects are only partially explained** — Bayer explains source-model size, Lovisotto / Alam explain attention, and Liao / Chosen-Object explain anchor-free and matching effects, but nobody has tested those factors together on YOLO26.

---

## Next Note Pass (after 2026-04-15 local-queue completion)

1. AdvLogo (2024) — local PDF exists but no dedicated note yet; best next naturalistic / diffusion attack method.
2. PatchZero (2022) — local defense PDF already present and worth tightening into detector-focused evidence.
3. Wu et al. / Invisibility Cloak (2020) — older but still useful physical transfer anchor.
4. Zhou et al. / MVPatch (2023) — strongest remaining local multi-model transfer benchmark.
5. Li et al. / UV-Attack (2025) — strongest local NeRF / UV-map physical benchmark still below promotion-grade status.
6. Lu et al. / FRAN (2022) — frequency-domain defense and localization angle worth tightening.
7. Diff-NAT (2026) — naturalistic diffusion baseline once AdvLogo is promoted.

---

## Recommended Reading Order for Capstone

1. Brown et al. (2017) — understand universal patches and EoT
2. Liu et al. / DPatch (2019) — understand detector-specific losses
3. Thys et al. (2019) — canonical person-vanishing method; learn the loss design
4. Guesmi et al. / DAP (2024) — strongest person-vanishing baseline before your own runs
5. Lovisotto et al. (2022) — attention-specific vulnerability framing
6. Alam et al. (2023) — deformable-transformer patch mechanics
7. Liao et al. (2021) — anchor-free transfer mismatch
8. Bayer et al. (2024) — why v8n-trained patches under-transfer
9. Huang et al. / T-SEA (2022) — what to try if transfer needs to improve
10. Xu et al. (2020) — physical person benchmark
11. Huang et al. / AdvReal (2025) — current physical benchmark
12. Gala et al. (2025) — direct modern Ultralytics benchmark
13. Schack et al. (2024) — read before making any physical-world claim

---

## Batch 2 Additions (2026-04-10) — New Verified Papers

### DAP — New State-of-the-Art Baseline (Guesmi et al., CVPR 2024)

DAP is now the strongest verified person-vanishing result. Key advantages over Thys et al.:
- **Creases Transformation (CT)**: directly simulates cloth wrinkles — more realistic than rigid EoT rotation/scale
- **No GAN required**: uses a cosine similarity loss (L_sim) to maintain naturalism
- **Better digital numbers**: 93.46% success on YOLOv3tiny vs Thys' 73.54% (recall reduction)
- **Physical T-shirt test**: 65% success rate with printed patch on clothing

Loss: `L_total = L_det + 4·L_sim + 0.5·L_tv` (objectness×class probability + similarity to benign image + smoothness)

**Your capstone should compare against DAP as the 2024 baseline, not just Thys (2019).**

### DOEPatch — Ensemble Approach for Multi-Model Attacks (Tan et al., 2024)

If extending your capstone to train a single patch that fools YOLOv8 + YOLO11 simultaneously, DOEPatch provides the exact framework. The Min-Max alternating optimization with dynamic weight adjustment prevents collapse to a single model. Tested on YOLOv2–v4 + Faster R-CNN; the same approach is portable to v8/v11.

### NAPGuard — Defense Reference (Wu et al., CVPR 2024)

For any "countermeasures" section: NAPGuard improves detection of naturalistic patches (GAN/diffusion-generated) by 60.24% AP@0.5 over prior defenses. The existence of NAPGuard is relevant to discussing why naturalistic patches (like Gala et al.) are still a research priority — defenses exist but are not deployed by default.

### DelaCruz et al. (2026) — Surveillance System Framing

The most recent survey of physical attacks on surveillance systems. Four-dimension framework (temporal persistence, modality, carrier realism, system-level) provides a structured way to frame your capstone's contribution beyond per-frame mAP numbers.

### ⚠️ Correction: Previously Flagged Papers Are Real

The 6 papers flagged in a prior version of this document as "likely hallucinated" (Wei NeurIPS 2024, Zimoň 2025, Lin IEEE Access 2024, AYO-GAN, Ma Elsevier 2025, Gu & Jafarnejadsani 2025) are **confirmed real papers**, but not all are local-PDF-verified yet. The earlier flag was a methodology error — arXiv was searched as if it were a comprehensive academic archive. It is not; Springer, IEEE Access, MDPI, and Elsevier regularly publish papers without arXiv preprints. All 6 have been confirmed at their publisher URLs, processed into note files, and added to `verified_sources.md`; their note-level evidence states still depend on local PDF access and verification. See `docs/research/unverified_paper_claims.md` for the full correction record.

**Rule going forward**: verify by DOI, publisher URL, or Google Scholar — not arXiv alone.

### Updated Recommended Reading Order

1. Brown et al. (2017) — universal patches + EoT
2. Liu et al. / DPatch (2019) — detector-specific losses
3. Thys et al. (2019) — canonical person-vanishing; objectness loss
4. **Guesmi et al. / DAP (CVPR 2024)** — current SOTA person-vanishing; Creases Transformation
5. Hu et al. (2021) — GAN latent naturalism (prerequisite for Gala)
6. Gala et al. (2025) — Ultralytics YOLOv5–v10 benchmark
7. Schack et al. (2024) — physical-world gap; read before any physical claims
8. Tan et al. / DOEPatch (2024) — if planning multi-model ensemble training
9. DelaCruz et al. (2026) — if framing capstone as a surveillance systems paper
10. Wu et al. / NAPGuard (2024) — if writing a defenses section

---

## Batch 3 Additions (2026-04-10) — Attack Methods

### CAP — Camera-Agnostic Patches via ISP Proxy (Wei et al., NeurIPS 2024)

The camera ISP proxy network (CAP) is the current state-of-the-art for physical-world patch transfer across different camera hardware. Standard EoT (rotation, scale, brightness) treats the camera as a black box. CAP instead builds a differentiable model of the full camera pipeline (lens distortion → sensor noise → ISP color processing) and incorporates it directly into the patch optimization loop.

- **Why it matters for your capstone**: if you physically print and photograph a patch, the camera itself is a variable. CAP addresses this systematically rather than hoping EoT is enough.
- **Practical implication**: for purely digital experiments, CAP is not needed. For physical-world claim, it is the benchmark to compare against.

### SPAP/SPAP-2 — Superpixel Adversarial Patches (Bagley et al., 2025)

SLIC superpixels are computed on the target region and differentiated via the implicit function theorem (IFT), making the segmentation boundary itself part of the optimization. The patch is constrained to superpixel boundaries → visually coherent, geometrically irregular patches that are harder to detect and more robust at small sizes.

- **Key number**: SPAP-2 reduces person AP to **16.28%** on YOLOv8 vs. 24.97% for standard AdvPatch — strongest result in the scale-robustness regime.
- **Why it matters**: directly tested on YOLOv8; provides a state-of-the-art 2025 attack baseline beyond DAP.

### Diff-NAT — Diffusion-Based Naturalistic Patches (Li et al., AAAI 2026)

Dual-level optimization using a conditional diffusion model:
1. **Global level**: CLIP-guided text conditioning to make the patch look like a specific semantic category (e.g., "a flower")
2. **Local level**: standard detection suppression loss via backpropagation through denoising steps

Diff-NAT closes the gap between naturalism (human-perceptible realism) and adversarial effectiveness that GAN-based methods (Hu et al.) leave open. Outperforms BigGAN-based NAP on both SSIM (visual quality) and AP suppression.

- **Three naturalism paradigms now on record**:
  1. GAN-latent optimization: Hu et al. (2021), AYO-GAN (2024), Gala et al. (2025)
  2. Cosine similarity to benign image: DAP/Guesmi (2024)
  3. Entropy maximization: Lin et al. (2024)
  4. **Diffusion model with text+latent optimization**: Diff-NAT (AAAI 2026) ← current state-of-the-art

### Zimoň (2025) — The Closest Prior Work to This Capstone

This is the single most directly relevant predecessor paper. It evaluates GAN-based patches across **YOLO v3, v5, v8, and v11** — exactly the model family this capstone covers, minus YOLO26. Key questions to answer by reading the full paper (institutional access required):

1. What are the per-version AP numbers under attack?
2. Do patches trained on v8 transfer to v11? What's the transfer rate?
3. What dataset(s) are used?

These numbers are the benchmark your capstone's YOLO26 results extend. **Read this paper before writing your capstone related-work section.**

### Lin et al. (2024) — Entropy Loss: The Simplest Naturalism Approach

Entropy maximization adds a single information-theoretic loss term (maximize Shannon entropy of the patch pixel distribution) without any pretrained generative model. This makes it the cheapest naturalism approach to implement. May be worth a brief ablation comparing entropy vs. TV vs. cosine similarity.

### AYO-GAN (Truong et al., 2024)

A second GAN architecture for adversarial patch generation applied to YOLO. Distinct from BigGAN (Hu et al.) — provides a data point for whether GAN architecture choice significantly affects attack strength. Full comparison requires institutional access.

---

## Batch 3 Additions (2026-04-10) — Defense Methods

Four defense papers are now in the literature base. They cover four distinct defense paradigms:

| Defense | Paper | Paradigm | Requires Retraining? |
|---|---|---|---|
| Ad-YOLO | (background context) | Train detector to ignore patches | Yes |
| NAPGuard | Wu et al. CVPR 2024 | Detect naturalistic patch pixels | Yes (classifier) |
| XAIAD-YOLO | Ma et al. Elsevier 2026 | Test-time XAI-guided purification | No |
| SAR | Gu & Jafarnejadsani MDPI 2025 | Segment patch region → recover → redetect | No |

**For the capstone defenses section**: if you are framing this as "attack + defense evaluation," these four papers provide a complete comparison table. XAIAD-YOLO and SAR are the most relevant because they require no retraining and could be applied to any YOLO version — including YOLO26.

---

## Updated Open Research Gaps (2026-04-10, after 22 papers)

1. **YOLO26 adversarial patch robustness** — still zero dedicated papers. NMS-free end-to-end design may respond differently to objectness suppression attacks.
2. **Cross-generation transfer (v8→v11→v26)** — Zimoň covers v3/v5/v8/v11; extension to v26 is the capstone's primary contribution.
3. **Physical robustness of Ultralytics v8/v11/v26** — Schack et al. tested only YOLOv3/v5; CAP and Diff-NAT are digital. The physical gap for the Ultralytics generation is unmeasured.
4. **Model size × robustness interaction on v11/v26** — Gala et al. showed this for v5–v10; extending it to v11/v26 is straight-forward and publishable.
5. **Defense evaluation on YOLO26** — none of the four defense papers tested against YOLO26; NMS-free detection may change defense effectiveness.

### Final Recommended Reading Order (22 papers)

**Core pipeline** (must-read):
1. Brown (2017) → DPatch (2019) → Thys (2019) → DAP/Guesmi (2024)

**Modern Ultralytics benchmark** (must-read):
5. Gala et al. (2025) → Zimoň (2025)

**Physical world** (read before any physical claims):
7. Schack (2024) → Wei/CAP (2024)

**Advanced attack methods** (for methods section):
9. Hu (2021) → Bagley/SPAP (2025) → Diff-NAT (2026) → Lin/entropy (2024) → DOEPatch (2024)

**Defenses** (for defenses/countermeasures section):
14. NAPGuard (2024) → XAIAD-YOLO (2026) → SAR (2025)

**Context and framing**:
17. Zolfi (2021) → Hoory (2020) → DelaCruz (2026) → Na (2025)
