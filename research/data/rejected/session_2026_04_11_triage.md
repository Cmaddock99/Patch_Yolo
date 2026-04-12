# Phase 1 Triage Session — Reject / Tier 3 Log

Date: 2026-04-11
Session: PDF corpus deep triage (all 32 PDFs reviewed)

## No Full Rejects from PDF Corpus

After reviewing all 32 PDFs, **no paper was classified as Reject (off-topic)**. All papers in docs/papers/ are relevant to at least one aspect of adversarial patch attacks or defenses against object detectors. The following papers were classified as Tier 3 (skim-only) due to limited direct relevance to the capstone, but are retained:

| Paper | Reason for Tier 3 (not Reject) |
|---|---|
| alam2023_attention_deficit | Targets deformable ViT, not YOLO; but attention vulnerability findings are relevant if YOLO26 uses attention |
| lovisotto2022_attention_CVPR | Same — architecture-agnostic attention analysis; partial relevance |
| zolfi2021_translucent | Camera-lens attack; stop signs only; physically interesting but very different threat model |
| winter2026_benchmarking | Explicitly excludes patch attacks; tests no v8/v11/v26; but adversarial training strategy benchmarks are useful |
| diffnat2026_AAAI | Diffusion-based naturalistic patches; not YOLO-specific; partial value for naturalistic patch comparison |
| bagley2025_spap | Superpixel cluster patches; not person-specific; some value for physical robustness techniques |

## Duplicates (marked, not rejected from triage)

Two pairs identified as duplicates (arXiv preprints superseded by CVPR versions):
- `zolfi2021_translucent_patch_2012.12528.pdf` — duplicate of CVPR version
- `guesmi2024_DAP_dynamic_adversarial_patch_2305.11618.pdf` — duplicate of CVPR version

See: `research/data/ranked/pdf_duplicates.md` for full justification.

## Note on Papers in docs/notes/ Without PDFs

15 papers have notes but no PDF in docs/papers/. These were not triaged from PDF (impossible without file). They are documented in pdf_inventory.md. Candidates for PDF acquisition include:
- imran2025_tkpatch_multiyolo — directly relevant (multi-YOLO person evasion)
- li2025_elevpatch_yolo11 — directly relevant (YOLO11-specific)
- zimon2025_GAN_YOLO_robustness — directly relevant (v3/v5/v8/v11)
- lin2024_entropy_adversarial_patch — relevant (YOLO person concealment)
- gu2025_SAR_segment_recover — relevant (defense: segment and recover)
