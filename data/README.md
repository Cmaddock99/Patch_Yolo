# Patch Pipeline Data

This directory belongs to the adversarial patch pipeline.

- `manifests/` contains the image lists used by training and evaluation.
- `custom_images/` contains the captured scene images referenced by those
  manifests.
- `configs/` contains the older baseline configs used by `create_adv_patch.py`.

Research-loop intermediate data lives under `research/data/`, not here.
