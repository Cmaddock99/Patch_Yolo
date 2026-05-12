# Patch Pipeline Configs

This directory is for adversarial patch execution and orchestration configs.

- `colab_runs.json` defines queued patch-training and transfer-eval jobs.
- `nuc_handoff.json` defines the local-to-Colab handoff flow and evidence gates.

Research-loop config does not live here. Literature ingestion and ranking
config stays under `research/config/`.
