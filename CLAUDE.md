# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Research and experimentation workspace for studying adversarial patch attacks against Ultralytics YOLO models (YOLOv8, YOLO11, YOLO26).

This repo is not the canonical runtime for the broader attack-defend-fortify project.
`YOLO-Bad-Triangle` is the only canonical execution surface. Work here should be framed as:

1. Patch training and patch-demo research.
2. Patch artifact generation for later manual import into the main pipeline.
3. Literature review and experiment notes.

## Environment Setup

```bash
./scripts/bootstrap.sh          # creates .venv and installs requirements.txt
source .venv/bin/activate
python scripts/verify_setup.py  # checks imports and expected paths
```

Python 3.12, venv at `.venv/`. Always activate the venv before running scripts.

## Running the Baseline Experiment

Place unlabeled images (JPG/PNG) in `data/custom_images/`, then:

```bash
python create_adv_patch.py
```

With optional overrides:

```bash
python create_adv_patch.py \
  --config data/configs/adv_patch_default_config.json \
  --images-dir data/custom_images \
  --output-dir outputs \
  --weights yolov5s.pt \
  --image-size 640 \
  --learning-rate 5.0
```

Outputs land in `outputs/<FOLDER_NAME>/`: `original/` (clean detections), `patched/` (adversarial detections), `patches/patch.png` (the learned patch).

## Architecture of `create_adv_patch.py`

The script is a single-file pipeline with no external project modules:

- **`AttackConfig`** — frozen dataclass loaded from the JSON config; normalizes `TARGET_SHAPE` from CHW or HWC automatically.
- **`YoloV5ARTWrapper`** — thin `torch.nn.Module` that bridges the `yolov5` pip package to ART's `PyTorchYolo` interface. In training mode it returns `{"loss_total": loss}`; in eval mode it returns raw YOLO output.
- **`build_detector`** — wraps the model in `PyTorchYolo` for CPU-only inference (portability).
- **`select_training_subset`** — filters images down to those where the detector already sees the `VICTIM_CLASS` above the confidence threshold; these are the only images used for patch training.
- **`build_location_mask`** — produces a boolean mask array that pins the patch to `TARGET_LOCATION` (top, left in resized image space).
- **`main`** — orchestrates: load images → build detector → get initial predictions → filter training set → save clean samples → build mask → run `DPatch.generate()` → apply patch → save adversarial samples.

ART's `DPatch` performs gradient ascent on the patch pixels to maximize the YOLO detection loss. For an untargeted attack `y=training_predictions` is passed; for a targeted attack `target_label=target_class_id` is used instead.

## Config Reference (`data/configs/adv_patch_default_config.json`)

| Key | Meaning |
|---|---|
| `TARGET_SHAPE` | Patch dimensions as CHW, e.g. `[3, 100, 100]` = 100×100 RGB |
| `TARGET_LOCATION` | `[top, left]` pixel offset in resized image space |
| `TARGET_CLASS` | COCO label to force misclassification to (empty = untargeted) |
| `VICTIM_CLASS` | COCO label whose detections are suppressed |
| `THRESHOLD` | Confidence threshold for keeping a detection |
| `MAX_ITER` | Number of gradient-ascent steps |
| `FOLDER_NAME` | Subdirectory name under `outputs/` |

## Key Scope Constraint

`create_adv_patch.py` targets **YOLOv5 only** because ART's `PyTorchYolo` wrapper is built around the `yolov5` pip package internals. Extending to YOLOv8/YOLO11/YOLO26 requires a different ART estimator or a custom training loop — see `docs/research/study_roadmap.md` for the phased plan.

Do not present this repo as a second orchestrator for the main project. If patch
support is promoted later, the integration point should be a profile-aware attack
plugin inside `YOLO-Bad-Triangle`.

## Research Docs

- `docs/research/YOLO_Adversarial_Patch_Knowledge_Repo.md` — background on YOLO vulnerability and attack taxonomy
- `docs/research/verified_sources.md` — checked bibliography (use this when citing)
- `docs/research/study_roadmap.md` — four-phase plan from literature → baseline → YOLOv8/11/26 experiments → research question
- `docs/notes/paper_review_template.md` — template for per-paper notes

## Research Ingestion Pipeline (`research/`)

The `research/` directory is a machine-assisted paper discovery layer that is intentionally **separate** from `docs/`, which remains the curated, human-reviewed knowledge base. Scripts never write to `docs/`.

### Running the pipeline

```bash
# Multi-source ingest (OpenAlex, Semantic Scholar, arXiv, Crossref, Unpaywall)
python research/scripts/ingest_papers.py --config research/config/research_queries.yaml

# Depth-1 citation expansion from vetted seeds
python research/scripts/expand_citations.py \
  --config research/config/research_queries.yaml \
  --seeds research/config/seed_papers.yaml
```

Optional env vars (set before running):

```bash
export OPENALEX_API_KEY=...
export SEMANTIC_SCHOLAR_API_KEY=...
export CONTACT_EMAIL=...   # enables polite OpenAlex ID and Unpaywall lookups
```

### Pipeline output contract

- `research/data/raw/` — ignored raw source payloads
- `research/data/normalized/` — ignored JSONL candidate datasets (`papers.jsonl`, `papers_deduped.jsonl`, `citation_candidates.jsonl`); all records carry `verification_state: candidate`
- `research/data/ranked/` — reviewable ranked markdown outputs; safe to commit

### Manual promotion workflow

1. Review ranked output under `research/data/ranked/`.
2. Verify candidates against trusted sources.
3. Promote into `docs/research/verified_sources.md` and create note files under `docs/notes/` using `paper_review_template.md`.
