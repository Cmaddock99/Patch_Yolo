# Recent PDF Priority Queue

Generated: 2026-04-11

**Definition of "recent":** Added in any of the 5 most recent git commits touching `docs/papers/` (commits: 5cac3e3, ca5ead1, 4e56cb0, b36e7b6, e8ef6d7). Excludes the foundational bulk-add commit 7aba5cc.

**Total recent PDFs:** 22 (of 32 total; 20 unique + 2 duplicates handled separately)

Priority order reflects capstone alignment: person suppression > YOLOv8/v11/v26 evaluation > transfer > physical plausibility > defense/fortify. Papers already having substantive notes are deprioritized unless the note is thin.

---

## Priority Queue (Deep Read Order)

### Tier 1 — Must Deep-Read

| Priority | Filename | Short Citation | Commit | Justification |
|---|---|---|---|---|
| 1 | `cheng2024_depatch_person_detector_2408.06625.pdf` | Cheng 2024 DePatch | 5cac3e3 | Person suppression with YOLO family; decoupled block-wise training directly improves physical robustness of any YOLO patch; existing note is thin (stub-level) |
| 2 | `huang2025_advreal_physical_2505.16402.pdf` | Huang 2025 AdvReal | 4e56cb0 | Physical adversarial framework for pedestrian detectors on YOLOv12; 2D+3D joint training; ASR 73% on YOLOv12 physical; directly evaluates person detection |
| 3 | `bayer2024_network_transferability_2408.15833.pdf` | Bayer 2024 Transferability | 4e56cb0 | Directly studies transfer across YOLO versions; existing note identifies it as the primary citation for capstone transfer findings |
| 4 | `tan2024_DOEPatch_2312.16907.pdf` | Tan 2024 DOEPatch | e8ef6d7 | Multi-model ensemble patch; tests YOLOv2+v3+v4 and Faster R-CNN; person class target; directly relevant to transfer-across-generations question |
| 5 | `na2025_unmanned_stores_2505.08835.pdf` | Na 2025 Unmanned Stores | e8ef6d7 | Physical evaluation with YOLOv5 victim model and RGB cameras; tests 3 attack types (Hide/Create/Alter); real store scenario; defense discussion |
| 6 | `ji2021_adversarial_yolo_defense_2103.08860.pdf` | Ji 2021 Ad-YOLO | 4e56cb0 | First YOLO-native defense (YOLOv2); adds "patch" category to YOLO head; critical defensive baseline; person detection focus |

### Tier 2 — Should Deep-Read

| Priority | Filename | Short Citation | Commit | Justification |
|---|---|---|---|---|
| 7 | `saha2020_spatial_context_adversarial_1910.00068.pdf` | Saha 2020 Spatial Context | 5cac3e3 | YOLO-specific spatial context defense; defends by regularizing outside bounding box; relevant to defend/fortify phase |
| 8 | `lu2022_fran_frequency_attention_2205.04638.pdf` | Lu 2022 FRAN | 5cac3e3 | Frequency attention module specifically designed for person detectors; YOLO-targeted; frequency domain insights for defense |
| 9 | `huang2022_tsea_transfer_2211.09773.pdf` | Huang 2022 T-SEA | 4e56cb0 | Single-model black-box transfer method; tests YOLO v2/v3/v3tiny/v4/v4tiny + Faster R-CNN; directly quantifies cross-YOLO transfer |
| 10 | `wu2020_invisibility_cloak_1910.14667.pdf` | Wu 2020 Invisibility Cloak | 4e56cb0 | Systematic transferability study across multiple detectors + physical world; wearable adversarial clothing tested |
| 11 | `alam2023_attention_deficit_2311.12914.pdf` | Alam 2023 Attention Deficit | 4e56cb0 | Collaborative patches for deformable vision transformers; partial relevance if YOLO26 uses transformer components |
| 12 | `lovisotto2022_attention_patch_robustness_CVPR.pdf` | Lovisotto 2022 Attention CVPR | ca5ead1 | CVPR 2022; dot-product attention as vulnerability; relevant if YOLO11/v26 use attention; defense angle |
| 13 | `wei2024_camera_agnostic_CAP_NeurIPS.pdf` | Wei 2024 CAP NeurIPS | b36e7b6 | Camera-agnostic attack via differentiable ISP proxy; NeurIPS 2024; critical for physical plausibility across camera hardware |
| 14 | `zhou2025_sequence_level_clothing_2511.16020.pdf` | Zhou 2025 Sequence Clothing | 5cac3e3 | Sequence-level clothing for human detection evasion; physical robustness via video-frame continuity |
| 15 | `delacruz2026_physical_attacks_surveillance_2604.06865.pdf` | DelaCruz 2026 Surveillance | e8ef6d7 | 2026 arXiv; visible+infrared evasion; AI surveillance systems; direct physical-world focus |

### Tier 3 — Skim Only

| Priority | Filename | Short Citation | Commit | Justification |
|---|---|---|---|---|
| 16 | `bagley2025_dynamically_optimized_clusters_2511.18656.pdf` | Bagley 2025 SPAP | b36e7b6 | Superpixel cluster patches; not person-specific; relevant only as physical robustness technique |
| 17 | `xu2020_adversarial_tshirt_1910.11099.pdf` | Xu 2020 Adv T-Shirt | 4e56cb0 | Already well-covered in existing note; TPS deformation for clothing; foundational physical work |
| 18 | `li2025_uvattack_nerf_person_2501.05783.pdf` | Li 2025 UV-Attack NeRF | 5cac3e3 | NeRF-based 3D UV mapping; innovative but NeRF not in capstone scope; note exists |
| 19 | `zhou2023_mvpatch_2312.17431.pdf` | Zhou 2023 MVPatch | 4e56cb0 | Multi-vivid patch; note exists; good transfer + stealth coverage |
| 20 | `diffnat2026_AAAI.pdf` | Yan 2026 Diff-NAT | b36e7b6 | Diffusion-based naturalistic attack; not YOLO-specific; low direct utility |
| 21 | `wu2024_NAPGuard_CVPR.pdf` | Wu 2024 NAPGuard | e8ef6d7 | Defense: detect NAPs; relevant for fortify phase; note exists |
| 22 | `schack2024_real_world_challenges_2410.19863.pdf` | Schack 2024 Real-World | e8ef6d7 | Already well-covered in note; evaluation framework; YOLOv3+v5 only |

---

## Notes on Duplicate Papers in Recent Additions

- `guesmi2024_DAP_CVPR.pdf` (e8ef6d7) — CANONICAL, note exists at `docs/notes/guesmi2024_DAP_dynamic_adversarial_patch.md`
- `guesmi2024_DAP_dynamic_adversarial_patch_2305.11618.pdf` (e8ef6d7) — DUPLICATE, skip
