#!/usr/bin/env python3
"""Import a finished Colab job return into the local outputs tree."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.colab_queue import build_patch_job_specs, load_json_mapping, resolve_path, select_job_specs

DEFAULT_CONFIG = REPO_ROOT / "configs" / "nuc_handoff.json"


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import a returned Colab job into local outputs.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to the NUC handoff config.")
    parser.add_argument("--job-id", required=True, help="Queued job id to import.")
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the exported job folder or its parent export root.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace any existing destination directories/files.")
    parser.add_argument("--rerun-handoff", action="store_true", help="Run scripts/start_nuc_handoff.sh after import.")
    parser.add_argument(
        "--handoff-skip-preflight",
        action="store_true",
        help="Pass --skip-preflight when rerunning the handoff coordinator.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the planned copies without writing files.")
    return parser.parse_args(argv)


def load_job_spec(*, config_path: Path, job_id: str) -> tuple[dict[str, Any], Path]:
    config = load_json_mapping(resolve_path(REPO_ROOT, config_path))
    repo_roots = dict(config.get("repo_roots") or {})
    attack_repo_root = resolve_path(REPO_ROOT, str(repo_roots.get("attack_repo") or "."))
    job_specs = build_patch_job_specs(config, attack_repo_root)
    selected = select_job_specs(job_specs, [job_id])
    if not selected:
        raise ValueError(f"No enabled job spec found for {job_id}.")
    return selected[0], attack_repo_root


def resolve_source_job_dir(source: Path, *, job_id: str) -> Path:
    expanded = source.expanduser().resolve()
    if not expanded.exists():
        raise FileNotFoundError(f"Import source does not exist: {expanded}")
    if (expanded / job_id).is_dir():
        return (expanded / job_id).resolve()
    return expanded


def expected_eval_run_names(job_spec: dict[str, Any]) -> list[str]:
    run_names: list[str] = []
    for index, target in enumerate(job_spec.get("eval_targets") or []):
        if not isinstance(target, dict):
            raise ValueError("Each eval_targets entry must be a mapping.")
        model_name = str(target.get("model") or f"eval{index}").strip()
        run_names.append(str(target.get("run_name") or f"{job_spec['job_id']}__transfer__{model_name}"))
    return run_names


def planned_imports(*, job_spec: dict[str, Any], attack_repo_root: Path, source_job_dir: Path) -> dict[str, Any]:
    train = dict(job_spec.get("train") or {})
    output_root = resolve_path(attack_repo_root, str(train.get("output_dir") or "outputs"))
    run_name = str(train.get("run_name") or job_spec["job_id"])
    run_names = [run_name, *expected_eval_run_names(job_spec)]
    run_dir_plans = []
    for name in run_names:
        run_dir_plans.append(
            {
                "name": name,
                "source": source_job_dir / name,
                "destination": output_root / name,
            }
        )
    summary_source = source_job_dir / f"{job_spec['job_id']}.json"
    summary_destination = attack_repo_root / "outputs" / "colab_job_summaries" / f"{job_spec['job_id']}.json"
    return {
        "run_dirs": run_dir_plans,
        "summary_source": summary_source,
        "summary_destination": summary_destination,
    }


def validate_sources(plan: dict[str, Any]) -> None:
    missing = [str(item["source"]) for item in plan["run_dirs"] if not Path(item["source"]).is_dir()]
    summary_source = Path(plan["summary_source"])
    if not summary_source.is_file():
        missing.append(str(summary_source))
    if missing:
        raise FileNotFoundError("Missing expected Colab return paths:\n- " + "\n- ".join(missing))


def copy_tree(*, source: Path, destination: Path, overwrite: bool, dry_run: bool) -> None:
    if destination.exists():
        if not overwrite:
            raise FileExistsError(f"Destination already exists: {destination}")
        if not dry_run:
            shutil.rmtree(destination)
    if not dry_run:
        shutil.copytree(source, destination)


def copy_file(*, source: Path, destination: Path, overwrite: bool, dry_run: bool) -> None:
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination already exists: {destination}")
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def write_receipt(
    *,
    attack_repo_root: Path,
    job_id: str,
    source_job_dir: Path,
    imported_paths: list[str],
    dry_run: bool,
) -> Path:
    receipt_root = attack_repo_root / "outputs" / "colab_job_summaries" / "import_receipts"
    receipt_path = receipt_root / f"{job_id}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    payload = {
        "job_id": job_id,
        "source_job_dir": str(source_job_dir),
        "imported_at_utc": utc_iso(),
        "imported_paths": imported_paths,
    }
    if not dry_run:
        receipt_root.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return receipt_path


def rerun_handoff(*, attack_repo_root: Path, skip_preflight: bool, dry_run: bool) -> int:
    command = ["./scripts/start_nuc_handoff.sh"]
    if skip_preflight:
        command.append("--skip-preflight")
    print(f"{utc_iso()} [import-colab-return] $ {' '.join(command)}")
    if dry_run:
        return 0
    return subprocess.call(command, cwd=attack_repo_root)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    job_spec, attack_repo_root = load_job_spec(config_path=args.config, job_id=str(args.job_id).strip())
    source_job_dir = resolve_source_job_dir(args.source, job_id=str(job_spec["job_id"]))
    plan = planned_imports(job_spec=job_spec, attack_repo_root=attack_repo_root, source_job_dir=source_job_dir)
    validate_sources(plan)

    imported_paths: list[str] = []
    for item in plan["run_dirs"]:
        source = Path(item["source"])
        destination = Path(item["destination"])
        print(f"{utc_iso()} [import-colab-return] copytree {source} -> {destination}")
        copy_tree(source=source, destination=destination, overwrite=bool(args.overwrite), dry_run=bool(args.dry_run))
        imported_paths.append(str(destination))

    summary_source = Path(plan["summary_source"])
    summary_destination = Path(plan["summary_destination"])
    print(f"{utc_iso()} [import-colab-return] copy {summary_source} -> {summary_destination}")
    copy_file(
        source=summary_source,
        destination=summary_destination,
        overwrite=bool(args.overwrite),
        dry_run=bool(args.dry_run),
    )
    imported_paths.append(str(summary_destination))

    receipt_path = write_receipt(
        attack_repo_root=attack_repo_root,
        job_id=str(job_spec["job_id"]),
        source_job_dir=source_job_dir,
        imported_paths=imported_paths,
        dry_run=bool(args.dry_run),
    )
    print(f"{utc_iso()} [import-colab-return] receipt -> {receipt_path}")

    if args.rerun_handoff:
        return rerun_handoff(
            attack_repo_root=attack_repo_root,
            skip_preflight=bool(args.handoff_skip_preflight),
            dry_run=bool(args.dry_run),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
