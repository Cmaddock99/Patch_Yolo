# Shared And Patch Scripts

This directory is reserved for shared repo utilities and adversarial patch
pipeline orchestration.

- Shared setup: `bootstrap.sh`, `verify_setup.py`
- Patch orchestration: `build_colab_runs.py`, `colab_queue.py`,
  `run_colab_patch_job.py`, `import_colab_return.py`, `run_nuc_handoff.py`,
  and the corresponding `start_*.sh` wrappers

Research-loop automation is intentionally kept out of this directory. Use
`research/scripts/` for literature ingestion, citation expansion, and draft
generation.
