# YOLO Adversarial Patch Evidence Matrix

Generated: 2026-04-15
Source corpus: 56 local PDFs in `docs/papers/` with 54 effective canonical PDFs after duplicate handling, plus remaining blocker records

Legend:
- Digital / Physical: D = digital only, P = physical tested, D+P = both
- Transfer evaluated: Y = yes, N = no, partial = cross-class or cross-dataset only
- Relevance to repo: 1–5 (5 = directly evaluates person suppression on YOLOv8/v11/v26)
- Working-packet evidence states: `page_cited`, `pdf_verified`, `note_only_flagged`, `blocked_access`

---

## Working-Packet Evidence Overlay

This overlay supersedes older “stub” interpretations for the first-pass papers and identifies which notes are still blockers.

| Slug | Evidence state | Primary repo question | Working-packet role |
|---|---|---|---|
| `bayer2024_network_transferability` | `page_cited` | `cross_yolo_transfer` | `benchmark` |
| `huang2025_advreal` | `page_cited` | `physical_robustness` | `benchmark` |
| `huang2022_tsea_transfer` | `page_cited` | `cross_yolo_transfer` | `method_to_borrow` |
| `tan2024_DOEPatch` | `pdf_verified` | `cross_yolo_transfer` | `method_to_borrow` |
| `lovisotto2022_attention_patch` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `alam2023_attention_deficit` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `wei2024_CAP` | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `schack2024_real_world` | `page_cited` | `physical_robustness` | `physical_caveat` |
| `cheng2024_depatch` | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `lin2024_nutnet` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `advtexture2022` | `page_cited` | `physical_robustness` | `benchmark` |
| `liang2021_catch_you` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `liao2021_anchor_free` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `nazeri2024_detr_robustness` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `gala2025_yolo` | `page_cited` | `yolo11_coverage` | `benchmark` |
| `wang2026_chosen_object` | `blocked_access` | `yolo26_architecture_mismatch` | blocker |
| `li2025_elevpatch` | `blocked_access` | `yolo11_coverage` | blocker |
| `zimon2025_GAN_YOLO` | `blocked_access` | `cross_yolo_transfer` | blocker |

---

| Paper (slug) | Detector Family | Exact YOLO Version(s) | Goal | D/P | Transfer Evaluated | Defense Relevance | Strongest Reported Outcome | Known Limitations | Code Available | Relevance to Repo |
|---|---|---|---|---|---|---|---|---|---|---|
| brown2017 | Classifiers only | None | Targeted misclassification | D+P | N | None | Printed patch forces target class in physical scenes | Classifiers only; no detection pipeline | Yes (CleverHans) | 2 |
| liu2019_dpatch | YOLO, Faster-RCNN | YOLOv2, Faster-RCNN | Untargeted suppression (global) | D | partial (2 detectors) | None | Suppresses detections anywhere in image without overlapping objects | Tested only 2 detectors; no physical; large patch | Yes (GitHub) | 3 |
| thys2019 | YOLO | YOLOv2 | Person vanishing (suppression) | D+P | N | None | OBJ loss reduces recall from 100% → 26.46% on INRIA; physically demonstrated | YOLOv2 only; no mAP metric; no newer YOLO | Yes (GitLab EAVISE) | 4 |
| wu2020_invisibility_cloak | Multi-detector | YOLOv2 + Faster-RCNN + SSD | Universal suppression (objectness) | D+P | Y (white-box + black-box, multi-detector) | None | Physical wearable clothing patches; systematic black-box transfer quantification | Focuses on YOLOv2; older architectures | Unclear | 4 |
| xu2020_adversarial_tshirt | YOLO, Faster-RCNN | YOLOv2, Faster-RCNN | Person suppression via clothing | D+P | Y (ensemble: YOLOv2 + Faster-RCNN) | None | 74% digital / 57% physical ASR on YOLOv2 with TPS deformation | YOLOv2/Faster-RCNN only; rigid background required | Yes (GitHub) | 4 |
| zolfi2021_translucent_patch | YOLO, Faster-RCNN | YOLOv3 (eval) | Class-specific suppression (stop signs) | D+P | Y (surrogate model → YOLOv3) | None | 42.27% stop sign detection prevention physically; 80% non-target preserved | Camera lens access required; stop signs only | Unclear | 2 |
| hoory2020_dynamic_patch | YOLO, Faster-RCNN | YOLOv3 | Dynamic scene object suppression | D+P | partial | None | Dynamic patches on moving objects/vehicles outperform static patches | Non-planar surfaces; specific placement constraints | Unclear | 3 |
| hu2021_naturalistic_patch | Multi-detector | YOLOv2, Faster-RCNN | Person suppression with naturalistic appearance | D | N | Indirect (stealth detection) | Naturalistic GAN-based patch achieves suppression while appearing realistic | Digital only; GAN instability; naturalistic patches weaker than non-naturalistic | Unclear | 3 |
| saha2020_spatial_context | YOLO | YOLOv3 (primary) | Spatial context-aware suppression + defense | D | partial | Yes (spatial context regularization as defense) | Context-aware loss improves transfer across YOLO versions | YOLOv3-centric; digital only | Unclear | 3 |
| ji2021_adversarial_yolo_defense | YOLO | YOLOv2 | Defense: patch class detection | D+P | N | Yes — primary defense contribution | 80.31% AP under white-box attack vs. 33.93% baseline; only −1.45 pp clean cost | YOLOv2 only; chest placement assumption | No (not released) | 4 |
| liang2021_catch_you | YOLO, YOLOR, Faster-RCNN | YOLOv2, YOLOv4, YOLOR, YOLOv8 | Defense: patch detection with and without signature | D+P | partial | Yes — primary defense contribution | Region-entropy and semantic-consistency defenses reach total F1 up to `0.926`, with strong physical performance on AdvTshirt and MyAdvTshirt | Detection-oriented rather than recovery-oriented; runtime is slower in the signature-independent mode | Unclear | 4 |
| lovisotto2022_attention_patch | Transformers + CNNs | Multiple (no specific YOLO version) | Robustness analysis: attention mechanism vulnerability | D | Y (across attention architectures) | Yes — attention as attack/defense surface | Dot-product attention dramatically increases vulnerability to patches | No YOLO versions tested directly | Unclear | 3 |
| huang2022_tsea_transfer | YOLO, Faster-RCNN, SSD | YOLOv2/v3/v3tiny/v4/v4tiny/v5, Faster-RCNN, SSD | Cross-model black-box transfer | D+P (1 qualitative demo) | Y — primary contribution (8 detectors) | Indirect (ShakeDrop as training technique) | Black-box avg mAP 9.16% vs. AdvPatch 36.46% on 7 detectors from YOLOv5 source | YOLOv8/v11/v26 not evaluated; physical only qualitative | Yes (GitHub VDIGPKU/T-SEA) | 4 |
| advtexture2022 | YOLO, Faster-RCNN, Mask R-CNN | YOLOv2, YOLOv3, Faster R-CNN, Mask R-CNN | Multi-angle physical person evasion with adversarial texture clothing | D+P | Y (cross-detector physical transfer) | None | TC-EGA keeps physical YOLOv2 AP at `0.359` while baseline clothing attacks stay near `0.952-1.000`; cross-detector physical mASR reaches `0.930` on Faster R-CNN | Only older detectors; no YOLOv8/v11/v26 coverage | Unclear | 4 |
| lu2022_fran | YOLO | YOLOv3/v4/v5 (frequency attention specific) | Person suppression via frequency domain | D | partial | Yes (FRAN module identifies patch regions via frequency anomaly) | Frequency attention boosts attack; also enables frequency-domain patch detection | Digital only; limited physical validation | Unclear | 3 |
| zhou2023_mvpatch | Multi-detector | YOLOv2/v3/v4/v5 + Faster-RCNN, YOLOv4-tiny | Universal camouflaged patch across multiple detectors | D+P | Y (multi-detector simultaneous) | Indirect | State-of-art camouflage + transferability simultaneously; 2023 benchmark | Focuses on older YOLO family; no v8/v11/v26 | Unclear | 3 |
| guesmi2024_DAP | YOLO | YOLOv5 (primary) | Person suppression with naturalistic + physical robustness | D+P | partial (YOLOv5 → Faster-RCNN) | Indirect | Naturalistic dynamic patches with Creases Transform for physical robustness | YOLOv5 primary; YOLOv8/v11/v26 not directly evaluated | Yes (CVPR Open Access) | 4 |
| alam2023_attention_deficit | Deformable ViT | None (Deformable DETR only) | Collaborative patches for deformable transformers | D | partial | Indirect | Multi-patch collaboration exploits attention across image regions | Not YOLO; attention-specific; deformable ViT only | Unclear | 2 |
| bayer2024_network_transferability | Multi-YOLO | YOLOv7–v10, YOLO-NAS, RT-DETR (28 models) | Cross-architecture patch transfer analysis | D | Y — primary contribution (28-model matrix) | Indirect (identifies most/least vulnerable architectures) | YOLOv8n/s are weak source models; larger models transfer better | YOLOv11/v26 absent; digital only; no physical | No (Fraunhofer) | 5 |
| cheng2024_depatch | YOLO | YOLOv2 (primary); YOLOv3, YOLOv5 (transfer) | Person suppression with physical robustness | D+P | partial (v2→v3, v2→v5) | Indirect | Digital AP 17.75% / physical clothing ASR 90.96% on YOLOv2 | YOLOv8/v11/v26 not evaluated | Not confirmed | 5 |
| lin2024_nutnet | YOLO, SSD, Faster-RCNN, DETR | YOLOv2, YOLOv3, YOLOv4, SSD, Faster R-CNN, DETR | Real-time defense against hiding and appearing patch attacks | D+P | Y (cross-detector evaluation) | Yes — primary defense contribution | Physical YOLOv2 attack success drops from `83.0%`, `74.9%`, `96.3%`, and `98.7%` to `0.7%`, `0.3%`, `0.0%`, and `5.6%` respectively | No YOLOv8/v11/v26 evaluation; physical tests are only on YOLOv2 | Unclear | 4 |
| nazeri2024_detr_robustness | DETR | DETR-R50, DETR-R50-DC5, DETR-R101, DETR-R101-DC5 | Pixel-space robustness and transfer analysis for detection transformers | D | Y (within DETR family and to Faster R-CNN) | Indirect | DETR-R50 mAP falls from `0.420` clean to `0.084` under the paper's attack, with transfer to Faster R-CNN still achieving `43.5%` relative degradation | Not an adversarial-patch paper; no YOLO models tested directly | Unclear | 3 |
| schack2024_real_world | YOLO | YOLOv3 (global), YOLOv5 (local) | Physical-digital gap analysis | P | N | Indirect (documents failure modes for defense planning) | Quantified digital-physical gap: hue change renders patch ineffective; size/rotation sensitivity | No new attack; evaluation only; older YOLO | No | 3 |
| tan2024_DOEPatch | Multi-detector | YOLOv2/v3/v4, Faster-RCNN (ensemble) | Multi-model ensemble adversarial patch | D | Y (multi-detector ensemble training) | Indirect | Dynamically optimized ensemble outperforms single-model patches on all target detectors | Focuses on pre-YOLOv8 family; no physical | Unclear | 3 |
| wei2024_CAP | YOLO + multi-camera | YOLOv5 (person detector) | Camera-agnostic physical attack | D+P | Y (6 cameras: Sony, Canon, iPhone, Redmi, Huawei, Samsung) | Yes (ISP proxy network is inherently defensive against patches) | 6/6 cameras succeeded vs. 1/6 for baseline | YOLOv5 only; no v8/v11/v26 | Yes (camera-agnostic.github.io) | 3 |
| bagley2025_spap | Multiple | Multiple (unspecified) | Superpixel cluster patches for physical robustness | D+P | partial | None | Superpixel clusters maintain color semantics; physically more robust | Not person-specific; YOLO versions unspecified | Unclear | 2 |
| delacruz2026_physical | YOLOv8 + tracking + IR | YOLOv8 (mentioned explicitly) | Physical attacks on AI surveillance (visible + IR) | P | partial | Indirect | Visible+IR evasion of surveillance AI; physical outdoor testing | 2026 arXiv; preprint quality; limited quantitative detail | No | 4 |
| diffnat2026_AAAI | Multi-detector | Multiple (unspecified) | Naturalistic adversarial patches via diffusion | D | partial | Indirect | Diffusion-optimized naturalistic patches more aggressive than GAN-based | Not YOLO-specific; naturalness vs. effectiveness trade-off | Unclear | 2 |
| huang2025_advreal | Multi-YOLO + transformers | YOLOv2/v3/v5/v8/v11/v12, Faster-RCNN, D-DETR | Physical person suppression across SOTA detectors | D+P | Y — critical (7 detectors, v8/v11/v12 explicitly) | Indirect (naturalistic patches fail; 3D rendering improves robustness) | YOLOv8 recall→32.68%, YOLOv11 recall→32.47%; physical ASR 70.13% on YOLOv12 | No YOLO26; glass-box is old YOLOv2 | Not confirmed | 5 |
| li2025_uvattack | YOLO + 3D | YOLOv5 (person detector) | Person suppression via NeRF-based UV mapping | D+P | partial | None | Dynamic NeRF rendering produces physically stable adversarial clothing | Complex NeRF pipeline; YOLOv5 only; high compute | Unclear | 3 |
| na2025_unmanned_stores | YOLO | YOLOv5 | Physical patch attack evaluation in retail surveillance | P | partial | Yes (attack categories + defense discussion) | Three attack types (Hide/Create/Alter) evaluated in real retail environment | YOLOv5 only; specific scenario (retail) | No | 3 |
| winter2026_benchmarking | Multi-detector (no YOLO8+) | YOLOv3, YOLOX (no v8/v11/v26) | Benchmark: digital non-patch attacks + adversarial training | D | Y (cross-architecture) | Yes — adversarial training strategies benchmarked | Mixed-attack adversarial training outperforms single-attack; transformer robustness | Patch attacks explicitly excluded; no YOLOv8/v11/v26 | Unclear | 1 |
| wu2024_NAPGuard | Multi-detector | Multiple (unspecified) | Defense: detect naturalistic adversarial patches | D | Y (across NAP types) | Yes — primary defense contribution | 60.24% AP@0.5 improvement over prior detection methods on GAP dataset | Focused on detection, not recovery; no physical | Yes (GitHub wusiyuang/NAPGuard) | 3 |
| zhou2025_sequence_clothing | YOLO | YOLOv5/v8 (mentioned) | Sequence-level clothing patches for video robustness | D+P | partial | None | Video-consistent adversarial clothing robust across pose changes; sequence-level optimization | Limited quantitative detail in pages read | Unclear | 3 |
| lovisotto2022_CVPR | Transformers | No YOLO | Robustness analysis: dot-product attention vulnerability | D | Y | Yes — attention is both vulnerability and defense angle | Attention-based models more vulnerable to patches than CNNs | No YOLO; theoretical focus | Unclear | 2 |

---

## Rows Added in Post-Previous-Review Update (2026-04-11)

### Special Row: Repo First-Party Results

| Paper (slug) | Detector Family | Exact YOLO Version(s) | Goal | D/P | Transfer Evaluated | Defense Relevance | Strongest Reported Outcome | Known Limitations | Code Available | Relevance to Repo |
|---|---|---|---|---|---|---|---|---|---|---|
| **REPO_FIRST_PARTY** | **Ultralytics YOLO** | **YOLOv8n, YOLO11n, YOLO26n** | **Person suppression + cross-generation transfer** | **D** | **Y (v8n→v11n, v8n→v26n, v11n→v26n)** | **No (attack-side only)** | **YOLOv8n 90% suppression; YOLO11n 84.8%; YOLO26n 11.6% direct (optimization failure; final_det_loss 251.9 vs ~0.14 for v8/v11); all transfer to v26n negligible** | **Digital only; small test set (20–43 clean detections); no physical evaluation; YOLO26n loss landscape mismatch** | **Yes (experiments/ultralytics_patch.py)** | **5** |

### New PDF: huang2019_universal_physical_camouflage

| Paper (slug) | Detector Family | Exact YOLO Version(s) | Goal | D/P | Transfer Evaluated | Defense Relevance | Strongest Reported Outcome | Known Limitations | Code Available | Relevance to Repo |
|---|---|---|---|---|---|---|---|---|---|---|
| huang2019_UPC | Faster R-CNN (primary) | None (Faster R-CNN VGG16/ResNet) | Universal physical camouflage — hide all instances of target class | D+P | partial (VGG16→ResNet across Faster-RCNN variants) | Indirect (semantic constraint produces natural-looking patches — stealth) | Faster R-CNN mAP drops to single digits on attacked instances; AttackScenes virtual benchmark introduced for reproducible physical evaluation | YOLO not directly evaluated; physical evaluation mostly virtual/simulated; semantic constraint may not generalize to non-naturalistic patches | Yes (mesunhlf.github.io) | 3 |

### New PDF: kolter2019_global_patch_suppression

| Paper (slug) | Detector Family | Exact YOLO Version(s) | Goal | D/P | Transfer Evaluated | Defense Relevance | Strongest Reported Outcome | Known Limitations | Code Available | Relevance to Repo |
|---|---|---|---|---|---|---|---|---|---|---|
| kolter2019_global_patch | YOLO | YOLOv3 | Global scene-level patch suppression (patch not on person) | D+P (webcam demo) | N | None | Clipped patch reduces YOLOv3 mAP 55.4% → 7.2% (0.5 conf); outperforms DPatch (26.8%); location-invariant; physically demonstrated via webcam | YOLOv3 only; no newer YOLO; physical demo is qualitative only; global placement requires environmental access | No (webcam demo only) | 3 |

### New PDF: patchzero2022_detect_zero_defense

| Paper (slug) | Detector Family | Exact YOLO Version(s) | Goal | D/P | Transfer Evaluated | Defense Relevance | Strongest Reported Outcome | Known Limitations | Code Available | Relevance to Repo |
|---|---|---|---|---|---|---|---|---|---|---|
| patchzero2022 | General (classifier + YOLO/detector) | PASCAL VOC detector (version unspecified) | Defense: pixel-wise patch detection and zeroing — no retraining needed | D | Y (across patch types and sizes) | Yes — primary defense contribution | Outperforms PatchGuard +26%, PatchCleanser +13% on MPGD/MAPGD; two-stage adversarial training handles adaptive (BPDA) attacks; 81.47% accuracy on ImageNet under attack (vs. 14.35% undefended) | Performance drops under stronger BPDA adaptive attacks (PZ-BPDA vs PZ-DO); false positive rate on highly textured natural regions not fully characterized | Yes (via ART codebase) | 3 |

### Tier C Unpromoted / Unverified Papers (10 papers — all claims unverified-from-pdf)

| Paper (slug) | Detector Family | Exact YOLO Version(s) | Goal | D/P | Transfer Evaluated | Defense Relevance | Strongest Reported Outcome | Known Limitations | Code Available | Relevance to Repo |
|---|---|---|---|---|---|---|---|---|---|---|
| bae2020_TOG ⚠️ | YOLO, Faster-RCNN | YOLOv3 [unverified-from-pdf] | NMS-flooding attack via objectness maximization [unverified-from-pdf] | D [unverified-from-pdf] | N [unverified-from-pdf] | Indirect (NMS attack contrast to non-NMS YOLO26) | NMS flooded with ghost detections suppressing real ones [unverified-from-pdf] | Citation needs verification — paper title, authors, DOI all pending confirmation | Unknown | 3 |
| gu2025_SAR | YOLO family [unverified-from-pdf] | Unspecified [unverified-from-pdf] | Defense: segment adversarial patch region; recover clean image; then detect | D+P [unverified-from-pdf] | N [unverified-from-pdf] | Yes — segmentation-based defense | Architecturally distinct defense paradigm (segment + recover) [unverified-from-pdf] | MDPI bot-blocked; exact numbers unknown | Unknown | 3 |
| imran2025_tkpatch | YOLO | YOLOv3, YOLOv5, YOLOv7 [unverified-from-pdf] | Universal Top-K multi-YOLO person evasion | D+P [unverified-from-pdf] | Y (3 models simultaneously) [unverified-from-pdf] | None | Single patch effective across YOLOv3/v5/v7 via Top-K loss [unverified-from-pdf] | v8/v11/v26 not tested; 0 citations; very new | Unknown | 4 |
| li2025_elevpatch | YOLO11 | YOLO11 [unverified-from-pdf] | Person detection evasion — YOLO11 specific | Unknown [unverified-from-pdf] | N [unverified-from-pdf] | None | YOLO11 suppression rate UNKNOWN — primary literature benchmark | Paywalled; all details unknown | Unknown | 5 |
| lin2024_entropy | YOLO | YOLOv2, YOLOv3, YOLOv4 [unverified-from-pdf] | Entropy-boosted naturalistic patches for person concealment | D [unverified-from-pdf] | N [unverified-from-pdf] | Indirect (naturalism via entropy = simpler than GAN) | Third naturalism paradigm (entropy loss); simpler than GAN/diffusion [unverified-from-pdf] | Only older YOLO versions; no v8/v11/v26 | Unknown | 3 |
| ma2026_XAIAD | YOLO family (anchor-based + anchor-free) | Unspecified YOLO family including anchor-free [unverified-from-pdf] | Defense: test-time XAI-guided purification — no retraining | D [unverified-from-pdf] | Y (white-box + black-box evaluated) [unverified-from-pdf] | Yes — XAI purification defense | 66.08 FPS (1.56× faster than Grad-CAM++); significant robustness improvement [unverified-from-pdf] | Paywalled; exact YOLO versions unknown | Unknown (anonymous repo) | 4 |
| tereshonok2025_anomaly | YOLO family [unverified-from-pdf] | Unspecified YOLO [unverified-from-pdf] | Defense: CNN anomaly localization + reconstruction before detection | D+P [unverified-from-pdf] | N [unverified-from-pdf] | Yes — anomaly reconstruction defense | Fifth distinct defense paradigm; open access available [unverified-from-pdf] | Exact numbers unknown; bot-blocked MDPI | Unknown | 3 |
| truong2024_AYO_GAN | YOLO | YOLOv5 (likely) [unverified-from-pdf] | GAN-generated full-image adversarial perturbation against YOLO | D [unverified-from-pdf] | N [unverified-from-pdf] | None | ASR 22.25%, SSIM 0.936 [partially verified from detailed metadata] | Digital only; full-image perturbation not comparable to localized patches; ASR much lower than patch-based methods | Unknown | 2 |
| wang2026_chosen_object | DETR-style (YOLO26 analog) | DETR-family [unverified-from-pdf] | Hungarian matching attack for end-to-end detection transformers | D [unverified-from-pdf] | partial [unverified-from-pdf] | Indirect (correct loss design for YOLO26) | Hungarian-matching-aware attack succeeds where NMS-era attacks fail [unverified-from-pdf] | Requires IEEE CSUSM access; exact loss formulation and numbers unknown | Unknown | 4 |
| zimon2025_GAN_YOLO | YOLO | YOLOv3, YOLOv5, YOLOv8, YOLOv11 [unverified-from-pdf] | Systematic cross-YOLO GAN-based patch attack and defense study | D [unverified-from-pdf] | Y (cross-version implied) [unverified-from-pdf] | Yes (defense also discussed) [unverified-from-pdf] | Systematic per-version evaluation across v3/v5/v8/v11 — benchmark numbers unknown [unverified-from-pdf] | Paywalled; exact numbers unknown; no YOLO26 | Unknown | 5 |

---

## Updated Summary Statistics

- First-pass normalized notes: 20 total (`19 page_cited`, `1 pdf_verified`)
- First-pass blockers: 3 total (`3 blocked_access`)

- Papers with direct YOLOv8 evaluation: 5 confirmed (huang2025_advreal, delacruz2026_physical, bagley2025_spap, li2025_uvattack, gala2025) + 1 note-only [unverified-from-pdf] (zimon2025)
- Papers with direct YOLOv11 evaluation: 1 confirmed (huang2025_advreal) + 2 note-only [unverified-from-pdf] (li2025_elevpatch, zimon2025)
- Papers with YOLO26 evaluation: 0 (literature) + 1 first-party (this repo — limited by optimization failure)
- Papers with physical evaluation: 20 (confirmed from PDFs)
- Papers with cross-version or cross-detector transfer evaluation: at least 14 (confirmed from PDFs)
- Papers with defense contributions: 9 confirmed PDFs (ji2021, liang2021, lin2024, saha2020, lovisotto2022, patchzero2022, wu2024_NAPGuard, na2025, winter2026) + 4 Tier C unverified records (gu2025, ma2026, tereshonok2025, zimon2025)
- Papers with open-source code: 8 (brown2017, liu2019, thys2019, xu2020, huang2022_tsea, wei2024_CAP, wu2024_NAPGuard, huang2019_UPC) + gala2025 via GitHub [unverified-from-pdf]
- Total papers in matrix: 30 original + 1 first-party + 3 new PDFs + 2 promoted blocker papers + 4 top-pass promoted notes + 10 remaining Tier C unverified records = 50 entries
