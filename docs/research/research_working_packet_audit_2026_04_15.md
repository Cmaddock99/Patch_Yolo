# Research Working Packet Audit

Generated: 2026-04-15  
Scope: current-state audit after promoting newly local-PDF-backed blocker notes

## Corpus Inventory

| Item | Count | Notes |
|---|---:|---|
| Note files in `docs/notes/` | 51 | Includes page-cited notes, partial notes, and remaining blockers |
| Local PDFs in `docs/papers/` | 56 | Raw file count |
| Known duplicate pairs | 2 | Guesmi 2024 and Zolfi 2021 |
| Effective canonical local-PDF count | 54 | 56 local PDFs minus 2 duplicate copies |
| Notes marked `page_cited` | 15 | Current citation-grade local note count |
| Notes marked `pdf_verified` | 1 | Current non-page-cited but PDF-backed promoted note count |
| Remaining `blocked_access` notes | 3 | Wang 2026, Li 2025 ElevPatch, Zimon 2025 |
| Remaining `note_only_flagged` notes | 0 | Gala has been promoted in this pass |

## Newly Promoted In This Pass

These notes were previously treated as blocked or note-only in the working packet and are now promoted from local PDFs.

| Slug | Local source | New evidence state | Primary repo question | Why it matters |
|---|---|---|---|---|
| `liao2021_anchor_free` | `docs/papers/transferable_anchor_free_2106.01618.pdf` | `page_cited` | `yolo26_architecture_mismatch` | Verifies the anchor-free output-mismatch explanation with local PDF evidence |
| `gala2025_yolo` | `docs/papers/gala2025_adversarial_patch_yolo_edge_s10207.pdf` | `page_cited` | `yolo11_coverage` | Provides the strongest direct modern Ultralytics YOLO benchmark in the local corpus |

## Current Working-Packet Evidence Overlay

| Slug | Evidence state | Primary repo question | Current role |
|---|---|---|---|
| `bayer2024_network_transferability` | `page_cited` | `cross_yolo_transfer` | `benchmark` |
| `huang2025_advreal` | `page_cited` | `physical_robustness` | `benchmark` |
| `huang2022_tsea_transfer` | `page_cited` | `cross_yolo_transfer` | `method_to_borrow` |
| `tan2024_DOEPatch` | `pdf_verified` | `cross_yolo_transfer` | `method_to_borrow` |
| `lovisotto2022_attention_patch` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `alam2023_attention_deficit` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `liao2021_anchor_free` | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `gala2025_yolo` | `page_cited` | `yolo11_coverage` | `benchmark` |
| `wei2024_CAP` | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `schack2024_real_world` | `page_cited` | `physical_robustness` | `physical_caveat` |
| `cheng2024_depatch` | `page_cited` | `physical_robustness` | `method_to_borrow` |
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
| Highest | `xu2020_adversarial_tshirt.md` | `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf` | Primary physical benchmark still sitting at note level |
| Highest | `ji2021_adversarial_yolo_defense.md` | `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf` | Strongest direct detector-side defense benchmark for YOLO |
| Highest | `gu2025_SAR_segment_recover.md` | `docs/papers/gu2025_SAR_segment_recover_jimaging316.pdf` | Segmentation-and-recovery defense is now locally readable but the note is still access-era placeholder text |
| Highest | `tereshonok2025_anomaly_localization_defense.md` | `docs/papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf` | Anomaly-localization defense note still lacks a promoted PDF-backed synthesis |
| Medium | `lu2022_fran_frequency_attention.md` | `docs/papers/lu2022_fran_frequency_attention_2205.04638.pdf` | Frequency-domain defense idea is useful but still only partial |
| Medium | `wu2020_invisibility_cloak.md` | `docs/papers/wu2020_invisibility_cloak_1910.14667.pdf` | Physical transfer benchmark still under-promoted |
| Medium | `zhou2023_mvpatch.md` | `docs/papers/zhou2023_mvpatch_2312.17431.pdf` | Multi-model camouflage benchmark still under-promoted |
| Medium | `li2025_uvattack_nerf_person.md` | `docs/papers/li2025_uvattack_nerf_person_2501.05783.pdf` | View-consistent physical attack method worth tightening |
| Medium | `diffnat2026_AAAI.md` | `docs/papers/diffnat2026_AAAI.pdf` | Useful naturalistic/diffusion reference but not yet promotion-grade |

## Local PDFs Not Yet Wired Into A Strong Note Path

| PDF | Current state |
|---|---|
| `docs/papers/advlogo_diffusion_patch_2409.07002.pdf` | No dedicated note yet |
| `docs/papers/yolo11_architecture_overview_2410.17725.pdf` | Architecture context PDF present; no dedicated note yet |

## Working Conclusions

- The repo no longer needs a broad ingest rerun to make immediate progress.
- The highest-value next work is promotion and cleanup of local-PDF-backed defense and physical benchmark notes.
- `YOLO11` is still thinly covered in literature terms even after promoting Gala: the repo now has better modern Ultralytics evidence, but still lacks a dedicated local-PDF YOLO11 attack benchmark.
- `YOLO26` remains literature-thin and still depends on mechanism papers plus the repo's first-party results.
- The current blocker set is now small enough that manual promotion work is clearly higher-return than discovery work.
