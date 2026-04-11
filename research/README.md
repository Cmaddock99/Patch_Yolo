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
- `data/raw/`
  Ignored raw source payloads.
- `data/normalized/`
  Ignored JSONL candidate datasets.
- `data/ranked/`
  Reviewable markdown outputs that are safe to commit.

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

## Output Contract

- Every normalized record is emitted with `verification_state: candidate`.
- The scripts never download PDFs.
- The scripts never scrape websites.
- The scripts never write to `docs/research/`, `docs/notes/`, or `docs/papers/`.

## Manual Promotion Workflow

1. Run ingest or citation expansion.
2. Review the ranked markdown output under `data/ranked/`.
3. Manually verify candidate papers against trusted sources.
4. Promote verified papers into `docs/research/verified_sources.md` and create or update note files under `docs/notes/`.

This separation is deliberate. `research/` helps discover candidates; `docs/` remains the human-reviewed literature base.
