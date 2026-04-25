# Presentation Repo Survey

Generated: 2026-04-16  
Repo: `Adversarial_Patch` at git `d575ca9`

## Method

This survey follows the staged design from the uploaded "Optimal Design" PDF:

1. deterministic inventory first
2. evidence-first extraction from committed artifacts
3. canonical machine record before prose synthesis
4. explicit separation between promoted evidence and upstream candidate backlog

The canonical record for this note is `research/data/ranked/presentation_repo_survey_2026_04_16.json`.

## Core Claim

This repo is presentation-ready on its core attack story, and this pass now also closes the local-PDF research layer: every PDF in `docs/papers/` is attached to a page-cited note. The larger remaining gap is the external unread research backlog: most of the 805-paper candidate universe still lives in `research/data` rather than in promoted, citation-grade notes.

## Inventory Snapshot

- Live repo counts during this survey: 1118 raw research records, 805 deduped candidates, 63 note files, 57 local PDFs, 58 draft notes.
- Freshest research audit: `docs/research/research_working_packet_audit_2026_04_15.md`
- Presentation sources present: `presentation.html`, `scripts/html_to_pptx.py`, `deck.pptx`
- Presentation support artifact still missing: `speaker-notes.md`
- Verification status:
  - `.venv/bin/python -m pytest tests/research_tests -q` passed with `17 passed in 0.57s`
  - plain `python -m pytest tests/research_tests -q` failed in the unactivated shell because `feedparser` was missing there

## Bulk Unprocessed Backlog

The first survey note underplayed the size of the machine-generated corpus. The repo is carrying a large upstream research queue that is only partially promoted into human-reviewed notes.

- Deduped candidate universe: 805 records
- Source mix in the deduped pool:
  - `openalex`: 573 records
  - `semanticscholar`: 249 records
- Open-access split:
  - `open_access = true`: 590
  - `open_access = false`: 215
- Most common years in the candidate pool:
  - 2025: 181
  - 2024: 140
  - 2023: 131
  - 2022: 102
- Most common matched themes:
  - `object detection`, `detector`, `yolo`, `robustness`, `physical`, `real-world`, `adversarial patch`, `transfer`

The top-200 screening packet makes the backlog shape clearer:

- 50 `deep_read_now`
- 48 `queue_for_full_text`
- 71 `metadata_only`
- 24 `already_covered`
- 7 `skip_offtopic`

Within that screened tranche, the dominant buckets are:

- `attack_core`: 83
- `generic_context`: 39
- `defense_core`: 36
- `architecture_context`: 35

And the dominant repo questions are:

- `cross_yolo_transfer`: 75
- `physical_robustness`: 72
- `yolo26_architecture_mismatch`: 48
- `yolo11_coverage`: 5

The practical implication is that the repo already has enough curated evidence for a talk, but the bulk of the research mass still lives upstream in candidate and queue layers rather than in promoted notes.

## What Is Solid Enough To Present

### Attack-side findings

- Direct suppression remains clear and well-supported by committed result files:
  - YOLOv8n: 90.0%
  - YOLO11n: 72.7%
  - YOLO26n: 16.3%
- The reconciled transfer matrix now uses the live v2 artifacts:
  - `v8n -> v11n`: 33.3%
  - `v11n -> v8n`: 55.0%
  - `v8n -> v26n`: 14.0%
  - `v26n -> v8n`: 45.0%
  - `v26n -> v11n`: 24.2%
  - `v11n -> v26n`: 9.3%
- The reconciled joint and warm-start highlights are:
  - `v8n + v11n -> v8n`: 90.0%
  - `v8n + v11n -> v11n`: 66.7%
  - `v8n + v26n -> v26n`: 18.6%
  - `v26n warmstart -> v8n`: 95.0%
- The strongest architectural explanation is still the YOLO26n mismatch: training optimizes the auxiliary `one2many` head, while evaluation depends on the `one2one` head.
- The defense benchmark is presentation-worthy as a negative result: the committed preprocessing report shows JPEG and blur mostly worsen outcomes or cost too much clean accuracy, and only a small subset of crop-resize settings pass the repo threshold.
- The live-demo and physical-benchmark scripts are present, so the repo can support a demo-oriented talk without claiming a fixed physical suppression number.

### Research-side findings

- The literature layer is already deep enough to support the presentation frame:
  - 57 local PDFs with page-cited coverage
  - 55 page-cited note files attached to that local corpus
  - 8 `blocked_access` external notes that now explicitly represent the unread promoted backlog
- That promoted set is still small relative to the full backlog:
  - 57 local PDFs versus 805 deduped candidates
  - 50 additional papers already sit in the immediate full-text queue
  - 48 more sit in the secondary full-text queue
- The current working packet is organized around four clear questions:
  - `cross_yolo_transfer`
  - `physical_robustness`
  - `yolo26_architecture_mismatch`
  - `yolo11_coverage`
- The 2026-04-15 working-packet audit is a safer source than the older PDF inventory when quoting corpus scope.

## Reconciled In This Pass

- `README.md` now matches the live transfer, joint-patch, and warm-start artifacts.
- `presentation.html` now matches the live transfer and joint-patch artifacts.
- `scripts/html_to_pptx.py` now matches the live transfer and joint-patch artifacts.
- `docs/deck-spec.md` now reflects the same live transfer values.
- `deck.pptx` was regenerated from the updated PPT generator.

## Remaining Drift Risks

| Surface | Live value | Current file value | Why it matters |
|---|---:|---:|---|
| presentation handoff files | `speaker-notes.md` absent | `docs/deck-spec.md` assumes a speaker-note handoff file | The source deck is reconciled, but the note handoff artifact is still missing |

## Presentation-Safe Framing

- Present this repo as a research and artifact workspace, not the canonical runtime. That framing already matches `README.md`.
- Use `outputs/*.json` as the source of truth for all percentages.
- Keep the v26n story centered on architecture mismatch, not generic "optimization failure."
- When discussing the backlog, distinguish clearly between:
  - promoted evidence in `docs/notes` and `docs/research`
  - machine-ranked but still-unprocessed candidates in `research/data`
- Use the research layer as context and support, not as a live dashboard. Prefer the refreshed `pdf_inventory.md` / `yolo_patch_evidence_matrix.md` pair over older snapshot docs when you quote corpus counts.
- Keep physical claims qualitative unless `experiments/physical_benchmark.py` has been run and summarized for the artifact you plan to show.

## Immediate Next Actions

1. Create `speaker-notes.md` so the presentation handoff matches `docs/deck-spec.md`.
2. If the talk should cover backlog scale explicitly, add one slide or appendix note summarizing the top-200 screening packet and the 50-paper immediate full-text queue.
3. Treat `research/data/ranked/presentation_repo_survey_2026_04_16.json` as the canonical record for this survey pass.
4. Keep new literature work focused on the external unread backlog rather than reworking the now-closed local PDF corpus.
