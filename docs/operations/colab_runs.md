# Colab Queue Workflow

The planned GPU-heavy runs now have a dedicated Colab path that does not depend on the NUC launcher.

For the canonical staged experiment loop, prefer `./scripts/start_nuc_handoff.sh`. The standalone Colab queue is still useful for ad hoc or source-only bundle generation, but it does not compute gate status or promoted-winner selection.

## Main Entry Point

Build the queue bundle with:

```bash
./scripts/start_colab_runs.sh
```

That command reads [configs/colab_runs.json](/Users/lurch/Desktop/Adversarial_Patch/configs/colab_runs.json) and writes a timestamped bundle under `outputs/colab_runs/`.

## What Gets Generated

Each bundle directory contains:

- `adversarial_patch_colab_bundle.tar.gz`
- `handoff/COLAB_QUICKSTART.md`
- `handoff/colab_job_index.md`
- `handoff/colab_jobs/*.json`
- `handoff/run_all_jobs.sh`
- `handoff/run_<job>.sh`
- `handoff/resume_<job>.sh`
- `colab_bundle_manifest.json`

## Queue Control

List the enabled jobs without building a bundle:

```bash
python3 scripts/build_colab_runs.py --list-jobs
```

Build only a subset:

```bash
python3 scripts/build_colab_runs.py \
  --job v8m_source_transfer_v1 \
  --job yolo26n_hybrid_loss_v1
```

## Current Queue

The default config stages:

- `v8m_source_transfer_v1`
- `v8n_transfer_baseline_v1`
- `v8n_transfer_cutout_only_v1`
- `v8n_transfer_self_ensemble_only_v1`
- `v8n_transfer_cutout_self_ensemble_v1`
- `yolo26n_hybrid_loss_v1`

`yolo26n_hybrid_loss_tps_v1` stays disabled until the base hybrid-loss run is worth extending.

## In Colab

1. Enable a GPU runtime.
2. Upload the generated tarball to Google Drive or the runtime filesystem.
3. Extract the tarball.
4. Install requirements.
5. Run one of the generated shell wrappers.

Example:

```bash
cd /content/adversarial_patch_bundle/adversarial_patch_colab_bundle
python -m pip install -r requirements.txt
bash handoff/run_v8m_source_transfer_v1.sh
```

To resume after a disconnect:

```bash
cd /content/adversarial_patch_bundle/adversarial_patch_colab_bundle
bash handoff/resume_v8m_source_transfer_v1.sh
```

You can also call the runner directly:

```bash
python scripts/run_colab_patch_job.py \
  --job-spec handoff/colab_jobs/v8m_source_transfer_v1.json \
  --resume
```

## What Colab Should Own

Use Colab for:

- patch training runs
- transfer eval-only sweeps that immediately follow those runs
- any long checkpointed runs that benefit from Drive-backed resume

Keep local-only tasks outside this queue:

- digital failure-grid analysis
- physical benchmark capture
- imported-patch defense matrices in `YOLO-Bad-Triangle`

## Existing Notebook

[experiments/colab_run.ipynb](/Users/lurch/Desktop/Adversarial_Patch/experiments/colab_run.ipynb) still works for ad hoc single runs. The queue bundle is the better path for the planned experiment roster because it removes manual parameter editing and makes resume behavior explicit.
