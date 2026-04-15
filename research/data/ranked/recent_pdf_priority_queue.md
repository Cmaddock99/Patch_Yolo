# First-Pass PDF Priority Queue

Generated: 2026-04-14
Scope: exact local-PDF queue for the working-packet pass

This queue is no longer a generic “recent PDF” list. It is the first-pass reading order keyed to the repo’s four open questions:

- `cross_yolo_transfer`
- `yolo26_architecture_mismatch`
- `physical_robustness`
- `yolo11_coverage`

`yolo11_coverage` is intentionally absent from the PDF queue because the near-scope YOLO11 papers in this repo do not have local PDFs and stay in the blocker track.

## Exact First-Pass Queue

| Priority | Slug | Local PDF | Primary repo question | Why this paper is queued now | Expected output | Target evidence state | Target disposition |
|---|---|---|---|---|---|---|---|
| 1 | `bayer2024_network_transferability` | `docs/papers/bayer2024_network_transferability_2408.15833.pdf` | `cross_yolo_transfer` | Best explanation for weak transfer from small YOLO source models | Transfer benchmark note with source-model-size takeaway | `page_cited` | `benchmark` |
| 2 | `huang2022_tsea_transfer` | `docs/papers/huang2022_tsea_transfer_2211.09773.pdf` | `cross_yolo_transfer` | Strongest single-model transfer-improvement recipe with public code | Transfer-method note and implementation candidate | `page_cited` | `method_to_borrow` |
| 3 | `tan2024_DOEPatch` | `docs/papers/tan2024_DOEPatch_2312.16907.pdf` | `cross_yolo_transfer` | Joint patch training template for multi-detector attacks | Ensemble-training method note | `pdf_verified` | `method_to_borrow` |
| 4 | `lovisotto2022_attention_patch` | `docs/papers/lovisotto2022_attention_patch_robustness_CVPR.pdf` | `yolo26_architecture_mismatch` | Dot-product attention vulnerability framing for transformer detectors | Attention-loss mechanism note | `page_cited` | `architecture_explanation` |
| 5 | `alam2023_attention_deficit` | `docs/papers/alam2023_attention_deficit_2311.12914.pdf` | `yolo26_architecture_mismatch` | Sparse/deformable attention attack closest to YOLO26-style reasoning | Pointer-loss mechanism note | `page_cited` | `architecture_explanation` |
| 6 | `huang2025_advreal` | `docs/papers/huang2025_advreal_physical_2505.16402.pdf` | `physical_robustness` | Best modern physical benchmark with direct YOLOv8 and YOLOv11 transfer numbers | Physical benchmark note | `page_cited` | `benchmark` |
| 7 | `cheng2024_depatch` | `docs/papers/cheng2024_depatch_person_detector_2408.06625.pdf` | `physical_robustness` | Most portable real-world robustness technique in the local corpus | Decoupling-method note | `page_cited` | `method_to_borrow` |
| 8 | `wei2024_CAP` | `docs/papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf` | `physical_robustness` | Camera ISP is a missing physical variable in most patch pipelines | Camera-agnostic method note | `page_cited` | `method_to_borrow` |
| 9 | `schack2024_real_world` | `docs/papers/schack2024_real_world_challenges_2410.19863.pdf` | `physical_robustness` | Best cautionary paper for the digital-to-physical gap | Physical-caveat note and evaluation checklist | `page_cited` | `physical_caveat` |

## Out of Scope for This Pass

- `na2025_unmanned_stores` and `ji2021_adversarial_yolo_defense` remain useful, but they are not required to answer the four first-pass repo questions.
- `saha2020_spatial_context`, `lu2022_fran`, and `wu2024_NAPGuard` belong to a later defense-focused pass.
- `bagley2025_spap`, `li2025_uvattack`, `zhou2025_sequence_clothing`, and `delacruz2026_physical` remain secondary until the core transfer and physical questions are stabilized.

## Duplicate Reminder

- Canonical `guesmi2024_DAP_CVPR.pdf`; treat `guesmi2024_DAP_dynamic_adversarial_patch_2305.11618.pdf` as a duplicate.
- Canonical `zolfi2021_translucent_patch_CVPR.pdf`; treat `zolfi2021_translucent_patch_2012.12528.pdf` as a duplicate.
