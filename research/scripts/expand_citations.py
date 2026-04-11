#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.pipeline import run_citation_expansion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Expand a vetted seed list into one-hop citation candidates.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("research/config/research_queries.yaml"),
        help="Path to the research query config YAML.",
    )
    parser.add_argument(
        "--seeds",
        type=Path,
        default=Path("research/config/seed_papers.yaml"),
        help="Path to the vetted seed papers YAML.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_citation_expansion(args.config, args.seeds)
    print(f"Done. Citation candidates: {result['citation_candidates']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
