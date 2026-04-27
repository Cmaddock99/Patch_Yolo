# NUC Handoff Workflow

This repo now owns the operator entrypoint for the two-repo hardening cycle.

Run:

```bash
./scripts/start_nuc_handoff.sh
```

That command does four things:

1. Bootstraps or reuses the local `.venv` in `Adversarial_Patch`.
2. Bootstraps or reuses the local `.venv` in `YOLO-Bad-Triangle`.
3. Generates a timestamped handoff bundle under `outputs/nuc_handoff/`.
4. Runs any local-ready digital evaluation steps for artifacts already present in `outputs/`.

## What Runs Where

Local NUC responsibilities:

- attack-repo setup verification
- `YOLO-Bad-Triangle` environment validation
- digital failure-grid runs for returned patch artifacts
- `YOLO-Bad-Triangle` imported-patch defense matrices
- physical benchmark queue generation
- artifact gating and status reporting

Google Colab responsibilities:

- patch training runs that need GPU time
- checkpointed long-running attack jobs
- transfer eval-only sweeps immediately after training

The handoff flow assumes Colab is for compute-heavy attack work, while the NUC is the stable coordinator and evaluator.

## Why The Colab Bundle Exists

The older notebook path assumes GitHub clone state. That is unsafe when the local repo has unpublished changes.

`scripts/run_nuc_handoff.py` therefore packages a Colab bundle from the exact current local repo state, including:

- `experiments/ultralytics_patch.py`
- `scripts/run_colab_patch_job.py`
- `data/manifests/`
- `data/custom_images/`
- generated job specs
- a generated Colab quickstart note

Use that bundle in Colab if the NUC checkout is ahead of remote.

## Generated Outputs

Each run writes a timestamped folder like:

```text
outputs/nuc_handoff/nuc_handoff_<timestamp>/
```

Important files inside:

- `nuc_spec_sheet.md`: operator-facing spec and artifact status table
- `sequential_status.json`: machine-readable gate state, winners, and next-step recommendation
- `handoff_manifest.json`: machine-readable summary
- `handoff/colab_jobs/*.json`: one job spec per Colab run
- `handoff/run_<job>.sh`: one Colab wrapper per job
- `handoff/resume_<job>.sh`: resume wrapper per job
- `handoff/run_all_jobs.sh`: full enabled queue wrapper
- `adversarial_patch_colab_bundle.tar.gz`: upload this to Colab
- `run_local_ready.sh`: rerun local-ready digital tasks
- `run_physical_queue.sh`: manual physical benchmark queue for promoted digital winners only

## Current Colab Queue

The default config stages:

- `v8m_source_transfer_v1`
- `v8n_transfer_baseline_v1`
- `v8n_transfer_cutout_only_v1`
- `v8n_transfer_self_ensemble_only_v1`
- `v8n_transfer_cutout_self_ensemble_v1`
- `yolo26n_hybrid_loss_v1`

`yolo26n_hybrid_loss_tps_v1` is present but disabled by default until the base hybrid run earns promotion.

## Sequential Control

`./scripts/start_nuc_handoff.sh` is now the canonical coordinator for the staged run order.

What it decides automatically:

- the next recommended Colab job
- whether Gate A / B / C has passed yet
- which artifacts are digitally complete
- which artifacts, if any, are eligible for physical benchmarking

Read those decisions from:

- `nuc_spec_sheet.md`
- `sequential_status.json`

The intended operator loop is:

1. Run `./scripts/start_nuc_handoff.sh`
2. In Colab, run only the recommended `handoff/run_<job>.sh`
3. Copy the returned run directory and `outputs/colab_job_summaries/<job>.json` back into this repo
4. Rerun `./scripts/start_nuc_handoff.sh`
5. Only run `run_physical_queue.sh` when the spec sheet names promoted digital winners

## Return Contract

After a Colab job finishes, copy the produced run directory back into this repo's `outputs/` tree on the NUC. Then rerun:

```bash
./scripts/start_nuc_handoff.sh
```

The launcher detects the returned artifact, checks for `results.json` plus `patch_artifact.json`, runs any still-missing local digital evaluations, refreshes the spec sheet, and updates the gate state.

## Promotion Gate

A patch artifact is only considered ready for promotion when all of these exist:

- `patch.png`
- `results.json`
- `patch_artifact.json`
- digital failure-grid output
- imported-patch matrix output in `YOLO-Bad-Triangle`
- physical benchmark sector summary

Physical benchmarking is staged only for the promoted digital winners from the transfer lane and the YOLO26 lane. That gate is reflected in the generated `nuc_spec_sheet.md`.
