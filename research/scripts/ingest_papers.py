#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.pipeline import run_ingest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest paper candidates into the research data workspace.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("research/config/research_queries.yaml"),
        help="Path to the research query config YAML.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_ingest(args.config)
    print(f"Done. Raw records: {result['raw_records']} | Deduped records: {result['deduped_records']}")
    if result.get("source_failures"):
        print(f"Completed with degraded coverage. Source failures: {result['source_failures']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
