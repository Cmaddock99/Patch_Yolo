# Research Working Packet Audit

Generated: 2026-04-15  
Scope: current-state audit after promoting newly local-PDF-backed blocker notes, the first eight local-PDF queue papers, and the multi-model transfer paper

## Corpus Inventory

| Item | Count | Notes |
|---|---:|---|
| Note files in `docs/notes/` | 56 | Includes page-cited notes, partial notes, and remaining blockers |
| Local PDFs in `docs/papers/` | 57 | Raw file count |
| Known duplicate pairs | 2 | Guesmi 2024 and Zolfi 2021 |
| Effective canonical local-PDF count | 55 | 57 local PDFs minus 2 duplicate copies |
| Notes marked `page_cited` | 24 | Current citation-grade local note count |
| Notes marked `pdf_verified` | 1 | Current non-page-cited but PDF-backed promoted note count |
| Remaining `blocked_access` notes | 3 | Wang 2026, Li 2025 ElevPatch, Zimon 2025 |
| Remaining `note_only_flagged` notes | 0 | Gala has been promoted in this pass |

## Newly Promoted In This Pass

These notes were previously treated as blocked or note-only in the working packet and are now promoted from local PDFs.

| Slug | Local source | New evidence state | Primary repo question | Why it matters |
|---|---|---|---|---|
| `liao2021_anchor_free` | `docs/papers/transferable_anchor_free_2106.01618.pdf` | `page_cited` | `yolo26_architecture_mismatch` | Verifies the anchor-free output-mismatch explanation with local PDF evidence |
| `gala2025_yolo` | `docs/papers/gala2025_adversarial_patch_yolo_edge_s10207.pdf` | `page_cited` | `yolo11_coverage` | Provides the strongest direct modern Ultralytics YOLO benchmark in the local corpus |
| `lin2024_nutnet` | `docs/papers/realtime_defense_diverse_patches_2406.10285.pdf` | `page_cited` | `physical_robustness` | Strongest repo-local online defense baseline spanning HA, AA, and physical evaluation |
| `advtexture2022` | `docs/papers/advtexture_person_detectors_2203.03373.pdf` | `page_cited` | `physical_robustness` | High-value physical clothing benchmark for multi-angle person evasion |
| `liang2021_catch_you` | `docs/papers/we_can_always_catch_you_2106.05261.pdf` | `page_cited` | `physical_robustness` | Strong YOLOv8-era defense paper with both fast and signature-independent detectors |
| `nazeri2024_detr_robustness` | `docs/papers/detection_transformers_robustness_2412.18718.pdf` | `page_cited` | `yolo26_architecture_mismatch` | Useful DETR-family robustness and transfer reference for YOLO26-style interpretation |
| `dimitriu2024_multi_model_transferability` | `docs/papers/dimitriu2024_multi_model_transferability_app142311423.pdf` | `page_cited` | `cross_yolo_transfer` | Strongest newly localized method paper for mixed-surrogate transfer improvement |
| `gu2025_SAR` | `docs/papers/gu2025_SAR_segment_recover_jimaging316.pdf` | `page_cited` | `physical_robustness` | Strongest local segment-and-inpaint defense with direct YOLO11 evaluation |
| `tereshonok2025_anomaly` | `docs/papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf` | `page_cited` | `physical_robustness` | Clean-data-only anomaly-localization defense for physical pedestrian patch attacks |
| `xu2020_adversarial_tshirt` | `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf` | `page_cited` | `physical_robustness` | Foundational TPS-based physical wearable benchmark for person evasion |
| `ji2021_adversarial_yolo_defense` | `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf` | `page_cited` | `physical_robustness` | Strongest direct YOLO-side patch-class defense baseline in the local corpus |

## Current Working-Packet Evidence Overlay

| Slug | Evidence state | Primary repo question | Current role |
|---|---|---|---|
| `bayer2024_network_transferability` | `page_cited` | `cross_yolo_transfer` | `benchmark` |
| `huang2025_advreal` | `page_cited` | `physical_robustness` | `benchmark` |
| `huang2022_tsea_transfer` | `page_cited` | `cross_yolo_transfer` | `method_to_borrow` |
| `dimitriu2024_multi_model_transferability` | `page_cited` | `cross_yolo_transfer` | `method_to_borrow` |
| `tan2024_DOEPatch` | `pdf_verified` | `cross_yolo_transfer` | `method_to_borrow` |
| `lovisotto2022_attention_patch` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `alam2023_attention_deficit` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `liao2021_anchor_free` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `gala2025_yolo` | `page_cited` | `yolo11_coverage` | `benchmark` |
| `wei2024_CAP` | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `schack2024_real_world` | `page_cited` | `physical_robustness` | `physical_caveat` |
| `cheng2024_depatch` | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `lin2024_nutnet` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `advtexture2022` | `page_cited` | `physical_robustness` | `benchmark` |
| `liang2021_catch_you` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `nazeri2024_detr_robustness` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `gu2025_SAR` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `tereshonok2025_anomaly` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `xu2020_adversarial_tshirt` | `page_cited` | `physical_robustness` | `benchmark` |
| `ji2021_adversarial_yolo_defense` | `page_cited` | `physical_robustness` | `defense_baseline` |
| `wang2026_chosen_object` | `blocked_access` | `yolo26_architecture_mismatch` | blocker |
| `li2025_elevpatch` | `blocked_access` | `yolo11_coverage` | blocker |
| `zimon2025_GAN_YOLO` | `blocked_access` | `cross_yolo_transfer` | blocker |

## Remaining Blockers

These are the only blocker notes still needed for the current working packet.

| Slug | Repo currently relies on this for | Exact missing detail preventing promotion | Blocker type |
|---|---|---|---|
| `wang2026_chosen_object` | Hungarian-matching framing for YOLO26 loss mismatch | Exact loss, datasets, ablations, and benchmark tables | architectural |
| `li2025_elevpatch` | Existence of a YOLO11-specific comparison paper | YOLO11 suppression numbers, dataset, and digital-vs-physical setup | quantitative |
| `zimon2025_GAN_YOLO` | Near-scope predecessor covering v3/v5/v8/v11 | Per-version benchmark tables, transfer matrix, and defense claims | quantitative |

## Local-PDF Upgrade Queue

These notes already have local PDFs but are not yet promoted to `page_cited` or `pdf_verified`.

| Priority band | Note | Local PDF | Why it is next |
|---|---|---|---|
| Highest | `patchzero2022_detect_zero_defense.md` | `docs/papers/patchzero2022_detect_zero_defense_2207.01795.pdf` | Strong detector-agnostic defense note still needs promotion-grade synthesis |
| Highest | `wu2020_invisibility_cloak.md` | `docs/papers/wu2020_invisibility_cloak_1910.14667.pdf` | Physical transfer benchmark still under-promoted |
| Highest | `zhou2023_mvpatch.md` | `docs/papers/zhou2023_mvpatch_2312.17431.pdf` | Multi-model camouflage benchmark still under-promoted |
| Highest | `li2025_uvattack_nerf_person.md` | `docs/papers/li2025_uvattack_nerf_person_2501.05783.pdf` | View-consistent physical attack method worth tightening |
| Medium | `lu2022_fran_frequency_attention.md` | `docs/papers/lu2022_fran_frequency_attention_2205.04638.pdf` | Frequency-domain defense idea is useful but still only partial |
| Medium | `diffnat2026_AAAI.md` | `docs/papers/diffnat2026_AAAI.pdf` | Useful naturalistic/diffusion reference but not yet promotion-grade |
| Medium | `zhou2025_sequence_level_clothing.md` | `docs/papers/zhou2025_sequence_level_clothing_2505.15848.pdf` | Sequence-level wearable robustness note could sharpen the video/temporal lane |
| Medium | `bagley2025_dynamically_optimized_clusters.md` | `docs/papers/bagley2025_dynamically_optimized_clusters_2511.18656.pdf` | Small-patch physical robustness result on modern YOLO remains under-integrated |

## Local PDFs Not Yet Wired Into A Strong Note Path

| PDF | Current state |
|---|---|
| `docs/papers/advlogo_diffusion_patch_2409.07002.pdf` | No dedicated note yet |
| `docs/papers/yolo11_architecture_overview_2410.17725.pdf` | Architecture context PDF present; no dedicated note yet |

## Working Conclusions

- The repo no longer needs a broad ingest rerun to make immediate progress.
- The highest-value next work is promotion and cleanup of the remaining local-PDF-backed defense and physical benchmark notes, not another broad ingest pass.
- `YOLO11` is still thinly covered in literature terms even after promoting Gala: the repo now has better modern Ultralytics evidence, but still lacks a dedicated local-PDF YOLO11 attack benchmark.
- `YOLO26` remains literature-thin and still depends on mechanism papers plus the repo's first-party results, though the new DETR robustness note improves the architecture-context layer.
- The current blocker set is now small enough that manual promotion work is clearly higher-return than discovery work.
