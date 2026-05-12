# Test Split

The test tree mirrors the repo split.

- `patch_tests/` covers adversarial patch training, evaluation, and
  orchestration.
- `research_tests/` covers the literature ingestion and note-generation loop.

Run both with `./.venv/bin/pytest -q tests`, or target one track at a time with
`./.venv/bin/pytest -q tests/patch_tests` or
`./.venv/bin/pytest -q tests/research_tests`.
