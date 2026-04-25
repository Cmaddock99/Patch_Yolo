#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 scripts/run_nuc_handoff.py \
  --config configs/nuc_handoff.json \
  --bootstrap \
  --run-local-ready \
  "$@"
