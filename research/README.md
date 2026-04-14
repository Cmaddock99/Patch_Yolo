# Research Workspace

This directory is the machine-generated research layer for the repo. It is intentionally separate from `docs/`, which remains the curated, citation-safe knowledge base.

## What Lives Here

- `config/research_queries.yaml`
  Seed queries, ranking weights, source limits, year filters, and citation expansion caps.
- `config/seed_papers.yaml`
  Vetted seed papers used for depth-1 citation expansion.
- `schemas/paper_record.example.json`
  Example shape for normalized candidate records.
- `scripts/ingest_papers.py`
  Main multi-source ingest workflow.
- `scripts/expand_citations.py`
  One-hop citation expansion workflow based on vetted seeds.
- `scripts/auto_note.py`
  Draft-note generator that fills citation metadata, embeds abstracts, and
  extracts PDF text into `research/data/drafts/` without writing to `docs/`.
- `data/raw/`
  Ignored raw source payloads.
- `data/normalized/`
  Ignored JSONL candidate datasets.
- `data/ranked/`
  Reviewable markdown outputs that are safe to commit.
- `data/drafts/`
  Ignored machine-generated skeleton notes and `YOLO26_flagged.md`; safe to
  delete and regenerate.

## Setup

The main repo bootstrap already installs the crawler dependencies:

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
python scripts/verify_setup.py
```

Optional environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `CONTACT_EMAIL`

`CONTACT_EMAIL` is recommended. It enables polite OpenAlex identification and Unpaywall lookups.

## Commands

Run the main ingest pass:

```bash
python research/scripts/ingest_papers.py --config research/config/research_queries.yaml
```

Run citation expansion from vetted seeds:

```bash
python research/scripts/expand_citations.py \
  --config research/config/research_queries.yaml \
  --seeds research/config/seed_papers.yaml
```

Generate machine-filled note drafts from ranked candidates:

```bash
python research/scripts/auto_note.py --top-n 40
```

## Output Contract

- Every normalized record is emitted with `verification_state: candidate`.
- `ingest_papers.py` and `expand_citations.py` never download PDFs.
- `auto_note.py` may fetch open-access PDFs transiently and extract text into
  generated drafts; it does not persist raw PDFs.
- The research scripts never write to `docs/research/`, `docs/notes/`, or `docs/papers/`.

## Manual Promotion Workflow

1. Run ingest or citation expansion.
2. Review the ranked markdown output under `data/ranked/`.
3. Optionally run `auto_note.py` to create drafts under `data/drafts/`.
4. Manually verify candidate papers against trusted sources.
5. Promote verified papers into `docs/research/verified_sources.md` and create or update note files under `docs/notes/`.

This separation is deliberate. `research/` helps discover candidates; `docs/` remains the human-reviewed literature base.
