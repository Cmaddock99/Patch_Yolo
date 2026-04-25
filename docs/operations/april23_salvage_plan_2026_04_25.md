# April 23 Salvage Plan — 2026-04-25

## Purpose

Turn the unfinished 2026-04-23 `Adversarial_Patch` work into mergeable source units, preserve all unrelated local work without loss, and close the execution seam with `YOLO-Bad-Triangle`.

## Safety Snapshot

Local parking branches preserve the full pre-cleanup trees:

- `Adversarial_Patch`: `codex/april23-parking-20260425`
- `YOLO-Bad-Triangle`: `codex/ybt-april23-parking-20260425`

These branches intentionally include unrelated notes, deck work, generated outputs, and temporary files so the cleanup branch can stay narrow.

## Active Source Branches

- `Adversarial_Patch`: `codex/april23-salvage`
- `YOLO-Bad-Triangle`: `codex/blind-patch-recover-imported-reporting`

Current `YOLO-Bad-Triangle` baseline state:

- `main` already includes the earlier imported-patch handoff unit: `feat: yolo11n patch-eval profile, oracle_patch_recover defense, and patch artifact provenance (#101)`
- the active local branch is a narrower follow-on reporting / defense adapter layer on top of that merged base

Current validation state:

- `Adversarial_Patch`: `./.venv/bin/pytest -q tests/test_patch_experiments.py tests/test_colab_runs.py tests/test_nuc_handoff.py` → `13 passed`
- `YOLO-Bad-Triangle`: `./.venv/bin/pytest -q tests/test_framework_defense_plugins.py tests/test_pipeline_profiles.py tests/test_plugin_inventory.py tests/test_plugin_loader_routing.py tests/test_run_unified.py` → `57 passed`

## Scope To Keep In `Adversarial_Patch`

Experiment and evaluation source:

- `README.md`
- `experiments/ultralytics_patch.py`
- `experiments/defense_eval.py`
- `experiments/live_demo.py`
- `experiments/physical_benchmark.py`
- `experiments/failure_grid.py`
- `tests/test_patch_experiments.py`

Research and handoff docs:

- `docs/research/full_note_repo_benefit_refresh_2026_04_23.md`
- `docs/research/repo_benefit_spec.md`
- `docs/research/presentation_repo_survey_2026_04_16.md`
- `docs/operations/colab_runs.md`
- `docs/operations/nuc_handoff.md`

Colab / NUC orchestration:

- `configs/colab_runs.json`
- `configs/nuc_handoff.json`
- `scripts/build_colab_runs.py`
- `scripts/colab_queue.py`
- `scripts/run_colab_patch_job.py`
- `scripts/run_nuc_handoff.py`
- `scripts/start_colab_runs.sh`
- `scripts/start_nuc_handoff.sh`
- `tests/test_colab_runs.py`
- `tests/test_nuc_handoff.py`

## Scope To Park Out Of The Salvage Unit

- `docs/notes/*`
- `docs/papers/*`
- `docs/research/master_literature_summary.md`
- `docs/research/yolo_patch_evidence_matrix.md`
- `docs/research/pdf_corpus_synthesis.md`
- `docs/deck-spec.md`
- `presentation.html`
- `scripts/html_to_pptx.py`
- `build_deck.py`
- `deck.pptx`
- `overview_deck*`
- `plain_language_explainer*`
- `presentation_script*`
- `research/data/ranked/*`
- `experiments/yolov8_patch_minimal.py`
- generated output trees and `tmp/`

## Workstreams

### 1. `Adversarial_Patch` Source Salvage

Split into two mergeable units:

1. Experiment / eval infrastructure
   - trainer updates
   - placement-aware eval
   - failure grid
   - sector-based physical reporting
   - README
   - experiment tests
2. Colab / NUC orchestration
   - queue configs
   - bundle builders
   - handoff launcher
   - ops docs
   - orchestration tests

Acceptance:

- source-only tree is clean
- generated outputs are ignored
- focused test suite passes
- research refresh doc does not contradict the code

### 2. `YOLO-Bad-Triangle` Imported-Patch Handoff

Use `main` as the stable imported-patch baseline and `codex/blind-patch-recover-imported-reporting` as the optional follow-on branch:

- keep the already-merged profile / provenance / `oracle_patch_recover` base on `main`
- keep the follow-on branch limited to imported-patch reporting and the blind-patch-recover adapter layer
- do not reintroduce manual smoke outputs or human-only walkthrough artifacts into the merge unit
- keep imported-patch evaluation centered on `patch-matrix`, `pretrained_patch`, `blind_patch_recover`, and `oracle_patch_recover`

Acceptance:

- branch stays source-clean
- imported-patch test slice stays green
- PR scope is code/config/reporting only

### 3. Execution Lane

Run the prepared queue from `Adversarial_Patch` after the source branches are stabilized:

- `v8m_source_transfer_v1`
- `v8n_transfer_baseline_v1`
- `v8n_transfer_cutout_only_v1`
- `v8n_transfer_self_ensemble_only_v1`
- `v8n_transfer_cutout_self_ensemble_v1`
- `yolo26n_hybrid_loss_v1`

Then copy returned run directories into `outputs/`, rerun local-ready digital tasks, and evaluate imported artifacts in `YOLO-Bad-Triangle`.

Acceptance:

- returned artifact has `patch.png`
- returned artifact has `patch_artifact.json`
- failure-grid output exists
- physical benchmark summary exists
- `YOLO-Bad-Triangle` patch-matrix results exist for the artifact

## Immediate Next Actions

1. Commit the `Adversarial_Patch` salvage branch as a source-only unit.
2. Review whether the orchestration layer should be one commit or two.
3. Leave parking branches untouched until both repos are merged cleanly.
4. After merge, regenerate bundles from the clean source branch instead of from parking snapshots.

## Definition Of Done

This April 23 work is only finished when all of the following are true:

1. `Adversarial_Patch` has a clean merged unit for the experiment/eval and handoff sources.
2. `YOLO-Bad-Triangle` has the imported-patch baseline on `main`, and any follow-on imported reporting / blind-recover branch is either merged or cleanly PR-ready.
3. At least one returned Colab artifact has passed the full promotion gate:
   - `patch.png`
   - `patch_artifact.json`
   - digital failure-grid output
   - physical sector summary
   - imported-patch `patch-matrix` results in `YOLO-Bad-Triangle`
