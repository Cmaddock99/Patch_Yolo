# YOLO Adversarial Patch Study Workspace

This repository is set up as a combined research and experiment workspace for studying adversarial patches against Ultralytics YOLO models, with emphasis on YOLOv8, YOLO11, and YOLO26.

It currently includes two tracks:

- A local, runnable baseline attack example using ART + YOLOv5 in `create_adv_patch.py`
- A research workspace under `docs/` for literature review, source tracking, and experiment planning for YOLOv8/YOLO11/YOLO26
- A machine-generated research ingestion workspace under `research/` for candidate discovery, dedupe, enrichment, and ranking

## Quick Start

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
python scripts/verify_setup.py
```

## What Is In This Repo

- `docs/research/YOLO_Adversarial_Patch_Knowledge_Repo.md`
  Imported from your base markdown so it now lives inside the repo.
- `docs/research/verified_sources.md`
  A tighter bibliography of sources that were checked during setup.
- `docs/research/study_roadmap.md`
  A practical roadmap for moving from literature review to experiments.
- `docs/notes/paper_review_template.md`
  A lightweight template for paper notes and capstone writeups.
- `create_adv_patch.py`
  A self-contained baseline patch trainer against a pretrained YOLOv5 detector using ART's `DPatch`.
- `research/`
  Scripts, config, and machine-generated outputs for API-based paper discovery. This workspace never auto-edits `docs/`.

## Baseline Experiment

Put unlabeled training images in `data/custom_images/`, then run:

```bash
python create_adv_patch.py
```

Optional flags:

```bash
python create_adv_patch.py \
  --config data/configs/adv_patch_default_config.json \
  --images-dir data/custom_images \
  --output-dir outputs \
  --weights yolov5s.pt \
  --image-size 640 \
  --learning-rate 5.0
```

## Important Scope Note

The local script is a YOLOv5 baseline because ART provides a usable YOLO wrapper there. It is useful for learning the patch-generation workflow, but it is not yet a native YOLOv8/YOLO11/YOLO26 training pipeline.

For the newer Ultralytics models, start with the verified research/code links in `docs/research/verified_sources.md` and use the roadmap in `docs/research/study_roadmap.md`.

## Research Ingestion

Bootstrap installs the lightweight crawler dependencies used by the `research/` workspace. The workflow is API-first and intentionally keeps `docs/` manual and curated.

Run the main ingest pass:

```bash
python research/scripts/ingest_papers.py --config research/config/research_queries.yaml
```

Run depth-1 citation expansion from vetted seeds:

```bash
python research/scripts/expand_citations.py \
  --config research/config/research_queries.yaml \
  --seeds research/config/seed_papers.yaml
```

Supported environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `CONTACT_EMAIL`

Outputs:

- `research/data/raw/`
  Ignored raw source payloads from OpenAlex, Semantic Scholar, arXiv, Crossref, and Unpaywall.
- `research/data/normalized/`
  Ignored JSONL candidate datasets such as `papers.jsonl`, `papers_deduped.jsonl`, and `citation_candidates.jsonl`.
- `research/data/ranked/`
  Reviewable ranked markdown outputs that can be committed.

Promotion into `docs/research/verified_sources.md` and `docs/notes/` remains manual. The ingestion scripts do not download PDFs, scrape websites, or write into `docs/`.

## Config Notes

- `TARGET_SHAPE` is interpreted as `CHW`. The example value `[3, 100, 100]` means a 100x100 RGB patch.
- `TARGET_LOCATION` is interpreted as `[top, left]` in the resized image space. With the default `640x640` resize, `[200, 200]` places the patch's upper-left corner at row 200, column 200.
- Leave `TARGET_CLASS` empty for an untargeted patch.
- Set `TARGET_CLASS` to a COCO class name such as `person`, `bus`, or `truck` for a targeted patch.
- `VICTIM_CLASS` filters the image set down to samples where the detector already sees the victim object above the configured threshold.

## Outputs

Each run writes to `outputs/<FOLDER_NAME>/`:

- `original/`: clean images with YOLO predictions overlaid
- `patched/`: patched images with YOLO predictions overlaid
- `patches/patch.png`: the learned adversarial patch

## Practical Limits

- The script resizes every image to a square input size.
- It uses pseudo-labels from the detector itself for untargeted patch training, so ground-truth annotations are not required for the baseline.
- The detector is configured for CPU execution to keep the example portable.
- Only use trusted weights such as the official `yolov5s.pt`.
