# Research Working Packet Audit

Generated: 2026-04-14  
Scope: repo-first audit and note normalization pass for the capstone literature workspace

## Corpus Inventory

| Item | Count | Notes |
|---|---:|---|
| Note files in `docs/notes/` | 46 | Includes fully processed, partial, and blocker records |
| Local PDFs in `docs/papers/` | 48 | Raw file count |
| Known duplicate pairs | 2 | Zolfi 2021 and Guesmi 2024 |
| Effective canonical local-PDF count | 46 | 48 local PDFs minus 2 duplicate copies |
| First-pass deep-read papers | 9 | Exact local-PDF set for this pass |
| First-pass blocker papers | 5 | Note-only or access-limited records |

## Duplicate Handling

Pointer-only duplicates remain recorded in [pdf_duplicates.md](/Users/lurch/Desktop/Adversarial_Patch/research/data/ranked/pdf_duplicates.md).

| Canonical slug | Canonical PDF | Duplicate PDF | Status |
|---|---|---|---|
| `zolfi2021_translucent_patch` | `docs/papers/zolfi2021_translucent_patch_CVPR.pdf` | `docs/papers/zolfi2021_translucent_patch_2012.12528.pdf` | Keep one canonical record only |
| `guesmi2024_DAP` | `docs/papers/guesmi2024_DAP_CVPR.pdf` | `docs/papers/guesmi2024_DAP_dynamic_adversarial_patch_2305.11618.pdf` | Keep one canonical record only |

## Coverage Status by Paper

This table is the working registry for the first-pass scope. Evidence state uses only the working-packet values: `page_cited`, `pdf_verified`, `note_only_flagged`, and `blocked_access`.

| Slug | Local source | Evidence state | Primary repo question | Current role |
|---|---|---|---|---|
| `bayer2024_network_transferability` | local PDF | `page_cited` | `cross_yolo_transfer` | `benchmark` |
| `huang2025_advreal` | local PDF | `page_cited` | `physical_robustness` | `benchmark` |
| `huang2022_tsea_transfer` | local PDF | `page_cited` | `cross_yolo_transfer` | `method_to_borrow` |
| `tan2024_DOEPatch` | local PDF | `pdf_verified` | `cross_yolo_transfer` | `method_to_borrow` |
| `lovisotto2022_attention_patch` | local PDF | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `alam2023_attention_deficit` | local PDF | `page_cited` | `yolo26_architecture_mismatch` | `architecture_explanation` |
| `wei2024_CAP` | local PDF | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `schack2024_real_world` | local PDF | `page_cited` | `physical_robustness` | `physical_caveat` |
| `cheng2024_depatch` | local PDF | `page_cited` | `physical_robustness` | `method_to_borrow` |
| `wang2026_chosen_object` | no local PDF | `blocked_access` | `yolo26_architecture_mismatch` | blocker |
| `liao2021_anchor_free` | no local PDF | `blocked_access` | `yolo26_architecture_mismatch` | blocker |
| `li2025_elevpatch` | no local PDF | `blocked_access` | `yolo11_coverage` | blocker |
| `zimon2025_GAN_YOLO` | no local PDF | `blocked_access` | `cross_yolo_transfer` | blocker |
| `gala2025_yolo` | no local PDF | `note_only_flagged` | `yolo11_coverage` | blocker |

## Contradiction Log

1. Resolved in this pass: the first-pass notes no longer carry stub-level status for Bayer, T-SEA, Lovisotto, Alam, AdvReal, CAP, Schack, or DePatch.
2. Resolved in this pass: the repo now records Huang 2019 as a local PDF-backed paper rather than an undownloaded placeholder.
3. Resolved in this pass: the priority queue now maps each queued paper to one primary repo question and one expected output.
4. Remaining after this pass: first-pass blocker notes are now explicit blocker records, but broader synthesis prose outside the working-packet overlay can still contain legacy unverified wording for papers outside the 14-paper scope.

## Blocker Log

These papers stay unpromoted in repo-first mode.

| Slug | Repo currently relies on this for | Exact missing detail preventing promotion | Repo question affected | Blocker type | Evidence state |
|---|---|---|---|---|---|
| `wang2026_chosen_object` | Hungarian-matching framing for YOLO26 loss mismatch | Exact loss, datasets, ablations, benchmark tables | `yolo26_architecture_mismatch` | architectural | `blocked_access` |
| `liao2021_anchor_free` | Anchor-free output mismatch as a secondary explanation for v8→v26 failure | Exact models, attack loss, and quantitative transfer results | `yolo26_architecture_mismatch` | architectural | `blocked_access` |
| `li2025_elevpatch` | Existence of a YOLO11-specific comparison paper | YOLO11 suppression numbers, dataset, and whether evaluation is digital or physical | `yolo11_coverage` | quantitative | `blocked_access` |
| `zimon2025_GAN_YOLO` | Near-scope predecessor covering v3/v5/v8/v11 | Per-version benchmark tables, transfer matrix, and defense claims | `cross_yolo_transfer` | quantitative | `blocked_access` |
| `gala2025_yolo` | Modern Ultralytics v5-v10 patch benchmark and model-size robustness direction | Per-model tables, transfer details, and full method statement | `yolo11_coverage` | access | `note_only_flagged` |

## Exact First-Pass Reading Queue

YOLO11 coverage remains in the blocker track because no local PDF exists for the only two near-scope YOLO11 papers in the repo.

| Priority | Slug | Primary repo question | Why it is in the first pass | Expected output |
|---|---|---|---|---|
| 1 | `bayer2024_network_transferability` | `cross_yolo_transfer` | Best literature explanation for why nano-source patches under-transfer | Transfer benchmark note plus source-model-size takeaway |
| 2 | `huang2022_tsea_transfer` | `cross_yolo_transfer` | Strongest single-model transfer-improvement recipe with code | Transfer-method note and implementation candidate |
| 3 | `tan2024_DOEPatch` | `cross_yolo_transfer` | Joint-patch training design for multi-detector attacks | Ensemble-training method note |
| 4 | `lovisotto2022_attention_patch` | `yolo26_architecture_mismatch` | Dot-product attention vulnerability framing for attention-based detectors | Attention-loss mechanism note |
| 5 | `alam2023_attention_deficit` | `yolo26_architecture_mismatch` | Sparse/deformable attention attack design closest to YOLO26-style reasoning | Pointer-loss mechanism note |
| 6 | `huang2025_advreal` | `physical_robustness` | Best modern cross-generation physical benchmark with YOLOv8 and YOLOv11 numbers | Physical benchmark note |
| 7 | `cheng2024_depatch` | `physical_robustness` | Most portable physical-robustness training trick in the local corpus | Decoupling-method note |
| 8 | `wei2024_CAP` | `physical_robustness` | Camera ISP is a first-order physical failure source missing from most patch work | Camera-agnostic method note |
| 9 | `schack2024_real_world` | `physical_robustness` | Best cautionary paper for the digital-to-physical gap | Physical-caveat note and evaluation checklist |

## Working Conclusions

- The first pass no longer needs a brute-force reread of the PDF corpus. The highest-value repo-local work is now the 9-paper deep-read set plus the 5 blocker records.
- YOLO26 still depends on mechanism papers rather than direct literature. The only synthesis-safe explanations are the local-PDF attention papers plus guarded blocker references.
- YOLO11 remains the thinnest part of the literature layer. In repo-first mode, it is represented by one direct benchmark paper (`li2025_elevpatch`) and one near-scope multi-YOLO paper (`zimon2025_GAN_YOLO`), both blocked.
- Physical claims should cite both an enabling method (`cheng2024_depatch`, `wei2024_CAP`, `huang2025_advreal`) and a limiting study (`schack2024_real_world`) in the same argument.
