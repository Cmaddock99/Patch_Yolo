#!/usr/bin/env python3
"""Run a generated adversarial-patch training job inside Colab or another GPU runtime."""
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
SUMMARY_ROOT = REPO_ROOT / "outputs" / "colab_job_summaries"
REPEATED_FLAGS = {
    "co_models": "--co-model",
    "co_weights": "--co-weight",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_repo_path(raw: str | Path) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_absolute():
        return candidate
    return (REPO_ROOT / candidate).resolve()


def render_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def mapping_to_cli_args(payload: dict[str, Any]) -> list[str]:
    args: list[str] = []
    for key, value in payload.items():
        if value is None or value is False:
            continue
        flag = REPEATED_FLAGS.get(key, f"--{key.replace('_', '-')}")
        if isinstance(value, bool):
            args.append(flag)
            continue
        if isinstance(value, list):
            for item in value:
                args.extend([flag, render_scalar(item)])
            continue
        args.extend([flag, render_scalar(value)])
    return args


def build_train_payload(job_payload: dict[str, Any], *, force_resume: bool = False) -> dict[str, Any]:
    train_payload = dict(job_payload.get("train") or {})
    if force_resume:
        train_payload["resume"] = True
    return train_payload


def build_train_command(job_payload: dict[str, Any], *, force_resume: bool = False) -> list[str]:
    train_payload = build_train_payload(job_payload, force_resume=force_resume)
    return [
        sys.executable,
        str(REPO_ROOT / "experiments" / "ultralytics_patch.py"),
        *mapping_to_cli_args(train_payload),
    ]


def build_eval_payload(
    job_payload: dict[str, Any],
    target: dict[str, Any],
    *,
    patch_path: Path,
    index: int,
) -> dict[str, Any]:
    train_payload = build_train_payload(job_payload, force_resume=False)
    eval_payload = dict(target)
    model_name = str(eval_payload.get("model") or f"eval{index}").strip()
    eval_payload["eval_only"] = True
    eval_payload["load_patch"] = str(patch_path)
    eval_payload.setdefault("manifest", train_payload.get("manifest"))
    eval_payload.setdefault("output_dir", train_payload.get("output_dir", "outputs"))
    eval_payload.setdefault("run_name", f"{job_payload['job_id']}__transfer__{model_name}")
    return eval_payload


def build_eval_command(job_payload: dict[str, Any], target: dict[str, Any], *, patch_path: Path, index: int) -> list[str]:
    eval_payload = build_eval_payload(job_payload, target, patch_path=patch_path, index=index)
    return [
        sys.executable,
        str(REPO_ROOT / "experiments" / "ultralytics_patch.py"),
        *mapping_to_cli_args(eval_payload),
    ]


def run_command(command: list[str], *, dry_run: bool) -> int:
    rendered = " ".join(command)
    print(f"{utc_now_iso()} [colab-job] $ {rendered}")
    if dry_run:
        return 0
    return subprocess.call(command, cwd=REPO_ROOT)


def expected_run_dir(job_payload: dict[str, Any]) -> Path:
    train = dict(job_payload.get("train") or {})
    output_dir = resolve_repo_path(str(train.get("output_dir") or "outputs"))
    run_name = str(train.get("run_name") or job_payload.get("job_id") or "").strip()
    if not run_name:
        raise ValueError("Job spec is missing train.run_name/job_id.")
    return output_dir / run_name


def expected_patch_path(job_payload: dict[str, Any]) -> Path:
    raw = str(job_payload.get("expected_patch_path") or "").strip()
    if raw:
        return resolve_repo_path(raw)
    return expected_run_dir(job_payload) / "patches" / "patch.png"


def copy_run_exports(
    *,
    export_root_raw: str | None,
    job_id: str,
    run_dirs: list[Path],
    summary_path: Path,
    dry_run: bool,
) -> list[str]:
    if not export_root_raw:
        return []
    export_root = Path(export_root_raw).expanduser()
    if not export_root.is_absolute():
        export_root = resolve_repo_path(export_root)
    job_export_root = export_root / job_id
    copied: list[str] = []
    if dry_run:
        copied.append(str(job_export_root))
        return copied
    job_export_root.mkdir(parents=True, exist_ok=True)
    for run_dir in run_dirs:
        if not run_dir.is_dir():
            continue
        target = job_export_root / run_dir.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(run_dir, target)
        copied.append(str(target))
    shutil.copy2(summary_path, job_export_root / summary_path.name)
    return copied


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a generated Colab patch-job spec.")
    parser.add_argument("--job-spec", type=Path, required=True, help="Path to a JSON job spec.")
    parser.add_argument("--skip-train", action="store_true", help="Skip the training command.")
    parser.add_argument("--skip-eval", action="store_true", help="Skip eval-only transfer runs.")
    parser.add_argument("--resume", action="store_true", help="Force --resume on the training step.")
    parser.add_argument("--export-root", default=None, help="Override the export root from the job spec.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = json.loads(args.job_spec.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid job spec payload: {args.job_spec}")

    job_id = str(payload.get("job_id") or "").strip()
    if not job_id:
        raise ValueError("job_id is required in the job spec.")

    payload["job_id"] = job_id
    eval_targets = list(payload.get("eval_targets") or [])
    export_root = str(args.export_root or payload.get("drive_export_root") or "").strip() or None
    summary = {
        "job_id": job_id,
        "job_spec_path": str(args.job_spec.resolve()),
        "started_at_utc": utc_now_iso(),
        "train_command": None,
        "train_exit_code": None,
        "eval_runs": [],
        "expected_patch_path": str(expected_patch_path(payload)),
        "expected_run_dir": str(expected_run_dir(payload)),
        "export_root": export_root,
    }

    train_command = build_train_command(payload, force_resume=bool(args.resume))
    summary["train_command"] = train_command

    if not args.skip_train:
        code = run_command(train_command, dry_run=bool(args.dry_run))
        summary["train_exit_code"] = code
        if code != 0:
            summary["finished_at_utc"] = utc_now_iso()
            SUMMARY_ROOT.mkdir(parents=True, exist_ok=True)
            summary_path = SUMMARY_ROOT / f"{job_id}.json"
            summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
            return code

    patch_path = expected_patch_path(payload)
    run_dirs = [expected_run_dir(payload)]
    if not args.dry_run and not patch_path.is_file() and not args.skip_eval:
        raise FileNotFoundError(
            f"Expected trained patch missing: {patch_path}. "
            "The training step did not produce the artifact that the eval step requires."
        )

    if not args.skip_eval:
        for index, target in enumerate(eval_targets):
            if not isinstance(target, dict):
                raise ValueError("Each eval_targets entry must be a mapping.")
            eval_payload = build_eval_payload(payload, target, patch_path=patch_path, index=index)
            model_name = str(eval_payload.get("model") or f"eval{index}").strip()
            eval_command = build_eval_command(payload, target, patch_path=patch_path, index=index)
            code = run_command(eval_command, dry_run=bool(args.dry_run))
            eval_run_dir = resolve_repo_path(str(eval_payload["output_dir"])) / str(eval_payload["run_name"])
            run_dirs.append(eval_run_dir)
            summary["eval_runs"].append(
                {
                    "model": model_name,
                    "command": eval_command,
                    "exit_code": code,
                    "run_dir": str(eval_run_dir),
                }
            )
            if code != 0:
                summary["finished_at_utc"] = utc_now_iso()
                SUMMARY_ROOT.mkdir(parents=True, exist_ok=True)
                summary_path = SUMMARY_ROOT / f"{job_id}.json"
                summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
                return code

    summary["finished_at_utc"] = utc_now_iso()
    SUMMARY_ROOT.mkdir(parents=True, exist_ok=True)
    summary_path = SUMMARY_ROOT / f"{job_id}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    copied = copy_run_exports(
        export_root_raw=export_root,
        job_id=job_id,
        run_dirs=run_dirs,
        summary_path=summary_path,
        dry_run=bool(args.dry_run),
    )
    if copied:
        print("Planned export targets:" if args.dry_run else "Exported run directories:")
        for path in copied:
            print(f"  - {path}")
    print(f"Job summary → {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
