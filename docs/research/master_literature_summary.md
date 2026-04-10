# Master Literature Summary: Adversarial Patches Against YOLO
*Running document — last updated 2026-04-10 (batch 2)*
*Sources: Original papers, arXiv full text, CVPR/ICCV open access pages, GitHub repos*

---

## How to Use This Document

This is the living synthesis document for the capstone. Every paper processed gets a row in the table and a dedicated note file under `docs/notes/`. When new papers are read, add them here.

- For full method details, loss terms, and numbers: see the individual note files.
- For source verification: see `verified_sources.md`.
- For original PDFs: see `docs/papers/`.

---

## Paper Coverage Map

| Paper | Year | Note File | PDF | Status |
|---|---|---|---|---|
| Brown et al. — Adversarial Patch | 2017 | `notes/brown2017_adversarial_patch.md` | `papers/brown2017_adversarial_patch_1712.09665.pdf` | Fully processed |
| Liu et al. — DPatch | 2019 | `notes/liu2019_dpatch.md` | `papers/liu2019_dpatch_1806.02299.pdf` | Fully processed |
| Thys et al. — Fooling Surveillance Cameras | 2019 | `notes/thys2019_fooling_surveillance.md` | `papers/thys2019_fooling_surveillance_1904.08653.pdf` | Fully processed |
| Hoory et al. — Dynamic Adversarial Patch | 2020 | `notes/hoory2020_dynamic_patch.md` | `papers/hoory2020_dynamic_patch_2010.13070.pdf` | Fully processed |
| Hu et al. — Naturalistic Physical Patch | 2021 | `notes/hu2021_naturalistic_patch.md` | `papers/hu2021_naturalistic_patch_ICCV.pdf` | Processed (abstract+method; full numbers in PDF) |
| Zolfi et al. — Translucent Patch | 2021 | `notes/zolfi2021_translucent_patch.md` | `papers/zolfi2021_translucent_patch_2012.12528.pdf` | Fully processed |
| Schack et al. — Real-world Challenges | 2024 | `notes/schack2024_real_world_challenges.md` | `papers/schack2024_real_world_challenges_2410.19863.pdf` | Fully processed |
| Gala et al. — YOLO Models IJIS 2025 | 2025 | `notes/gala2025_yolo_adversarial_patches.md` | Not available (Springer paywall) | Processed via GitHub README |
| Guesmi et al. — DAP | 2024 | `notes/guesmi2024_DAP_dynamic_adversarial_patch.md` | `papers/guesmi2024_DAP_CVPR.pdf` | Fully processed |
| Wu et al. — NAPGuard | 2024 | `notes/wu2024_NAPGuard.md` | `papers/wu2024_NAPGuard_CVPR.pdf` | Processed (abstract+method) |
| Tan et al. — DOEPatch | 2024 | `notes/tan2024_DOEPatch.md` | `papers/tan2024_DOEPatch_2312.16907.pdf` | Fully processed |
| DelaCruz et al. — Surveillance Survey | 2026 | `notes/delacruz2026_physical_attacks_surveillance.md` | `papers/delacruz2026_physical_attacks_surveillance_2604.06865.pdf` | Processed (abstract; check PDF for full survey) |
| Winter et al. — Benchmarking Robustness | 2026 | `notes/winter2026_benchmarking_robustness.md` | `papers/winter2026_benchmarking_robustness_2602.16494.pdf` | Processed ⚠️ non-patch only |
| Na et al. — Unmanned Stores | 2025 | `notes/na2025_unmanned_stores.md` | `papers/na2025_unmanned_stores_2505.08835.pdf` | Fully processed |

**External summary (ChatGPT-generated, imported):** `docs/research/executive_summary_chatgpt.md`
**Unverified/hallucinated paper claims:** `docs/research/unverified_paper_claims.md`

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

| Paper | Attack | Target | Clean Baseline | After Patch |
|---|---|---|---|---|
| DPatch (YOLO) | Untargeted | All classes | 65.7% mAP | <1% mAP |
| DPatch (Faster R-CNN ResNet101) | Untargeted | All classes | 75.10% mAP | 0.30% mAP |
| Thys (OBJ loss) | Person vanishing | Person | 100% recall | **26.46% recall** |
| Thys (CLS loss) | Person vanishing | Person | 100% recall | 77.58% recall |
| Thys (random noise) | Baseline | Person | 100% recall | 87.14% recall |
| Zolfi (digital, 8 shapes, α=0.4) | Stop sign | Stop sign | 95.17% AP | 52.7% AP |
| Zolfi (physical) | Stop sign | Stop sign | — | 42.27% fooling rate |
| Hoory (2 screens, wide angle) | Car hiding | Car | — | 74–80% success |
| Gala et al. | Person/vehicle | Person | — | High evasion (see PDF) |

---

## Open Research Gaps (as of 2026-04-10)

1. **YOLO26 adversarial patch robustness** — no dedicated paper exists. Its NMS-free end-to-end design may respond differently to objectness suppression.
2. **Cross-generation transfer (v8→v11→v26)** — the systematic patch transfer study across these three models has not been published.
3. **YOLO11 dedicated study** — only one paper (ElevPatch, 2025) specifically addresses YOLO11.
4. **Physical robustness of Ultralytics models** — Schack et al. tested only YOLOv3/v5; the physical-world gap for v8/v11/v26 is unmeasured.
5. **Model size × robustness interaction on v11/v26** — Gala et al. showed this for v5–v10; extending it is straightforward and publishable.

---

## Recommended Reading Order for Capstone

1. Brown et al. (2017) — understand universal patches and EoT
2. Liu et al. / DPatch (2019) — understand detector-specific losses
3. Thys et al. (2019) — canonical person-vanishing method; learn the loss design
4. Hu et al. (2021) — GAN-based naturalism (needed to understand Gala)
5. Gala et al. (2025) — your direct benchmark for YOLOv8+
6. Schack et al. (2024) — read before making any physical-world claims
7. Zolfi et al. (2021) — read if extending to class-selective suppression
8. Hoory et al. (2020) — read if extending to multi-angle/physical car testing

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

### ⚠️ Citation Integrity Warning

6 papers from the same external AI recommendation batch (Wei NeurIPS 2024, Zimoň 2025, Lin IEEE Access 2024, AYO-GAN, Ma Elsevier 2025, Gu & Jafarnejadsani 2025) **could not be verified** on arXiv, CVPR, NeurIPS, or via targeted searches. They may be hallucinated citations. Details in `docs/research/unverified_paper_claims.md`.

**Rule going forward**: every paper must have a confirmed arXiv ID, DOI, or open-access URL before being added to `verified_sources.md`.

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
