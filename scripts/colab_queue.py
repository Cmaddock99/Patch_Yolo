from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
COLAB_BUNDLE_ROOT = "adversarial_patch_colab_bundle"
COLAB_INCLUDE_PATHS = [
    "README.md",
    "requirements.txt",
    "experiments",
    "scripts/run_colab_patch_job.py",
    "scripts/verify_setup.py",
    "data/manifests",
    "data/custom_images",
]
BUNDLE_IGNORED_PARTS = {"__pycache__", ".ipynb_checkpoints"}
BUNDLE_IGNORED_NAMES = {".DS_Store"}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_path(anchor: Path, raw: str | Path) -> Path:
    candidate = Path(str(raw)).expanduser()
    if candidate.is_absolute():
        return candidate
    return (anchor / candidate).resolve()


def load_json_mapping(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping config at {path}")
    return payload


def should_bundle_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name in BUNDLE_IGNORED_NAMES:
        return False
    return not any(part in BUNDLE_IGNORED_PARTS for part in path.parts)


def build_patch_job_specs(config: dict[str, Any], attack_repo_root: Path) -> list[dict[str, Any]]:
    attack_defaults = dict(config.get("attack_defaults") or {})
    colab_cfg = dict(config.get("colab") or {})
    jobs_payload = colab_cfg.get("jobs")
    if jobs_payload is None:
        jobs_payload = config.get("jobs") or []
    specs: list[dict[str, Any]] = []
    for raw_job in jobs_payload:
        if not isinstance(raw_job, dict):
            raise ValueError("Each jobs entry must be a mapping.")
        if raw_job.get("enabled", True) is False:
            continue
        job_id = str(raw_job.get("job_id") or "").strip()
        if not job_id:
            raise ValueError("Each jobs entry requires job_id.")
        train = dict(attack_defaults)
        train.update(dict(raw_job.get("train") or {}))
        train.setdefault("run_name", job_id)
        train.setdefault("output_dir", "outputs")
        checkpoint_root = str(
            raw_job.get("checkpoint_root")
            or colab_cfg.get("checkpoint_root")
            or config.get("checkpoint_root")
            or ""
        ).rstrip("/")
        if checkpoint_root and "checkpoint_dir" not in train:
            train["checkpoint_dir"] = f"{checkpoint_root}/{train['run_name']}"
        drive_export_root = (
            raw_job.get("drive_export_root")
            or colab_cfg.get("drive_export_root")
            or config.get("drive_export_root")
        )
        run_dir = resolve_path(attack_repo_root, str(train["output_dir"])) / str(train["run_name"])
        patch_path = run_dir / "patches" / "patch.png"
        specs.append(
            {
                "job_id": job_id,
                "description": str(raw_job.get("description") or "").strip(),
                "train": train,
                "eval_targets": list(raw_job.get("eval_targets") or []),
                "drive_export_root": drive_export_root,
                "expected_run_dir": str(run_dir),
                "expected_patch_path": str(patch_path),
            }
        )
    return specs


def select_job_specs(job_specs: list[dict[str, Any]], requested_ids: list[str]) -> list[dict[str, Any]]:
    if not requested_ids:
        return list(job_specs)
    normalized = [str(item).strip() for item in requested_ids if str(item).strip()]
    by_id = {str(spec["job_id"]): spec for spec in job_specs}
    missing = [job_id for job_id in normalized if job_id not in by_id]
    if missing:
        raise ValueError(f"Unknown job id(s): {', '.join(missing)}")
    return [by_id[job_id] for job_id in normalized]


def render_colab_job_index(job_specs: list[dict[str, Any]]) -> str:
    lines = [
        "# Colab Job Index",
        "",
        f"- Generated at: `{utc_iso()}`",
        f"- Job count: `{len(job_specs)}`",
        "",
    ]
    if not job_specs:
        lines.append("No jobs selected.")
        lines.append("")
        return "\n".join(lines)

    lines.extend([
        "| job_id | source_model | run_name | eval_targets |",
        "|---|---|---|---|",
    ])
    for spec in job_specs:
        train = dict(spec.get("train") or {})
        targets = ", ".join(
            str(target.get("model"))
            for target in spec.get("eval_targets", [])
            if isinstance(target, dict)
        )
        lines.append(
            f"| `{spec['job_id']}` | `{train.get('model')}` | "
            f"`{train.get('run_name')}` | `{targets}` |"
        )
    lines.extend(["", "## Job Notes", ""])
    for spec in job_specs:
        description = str(spec.get("description") or "No description provided.")
        train = dict(spec.get("train") or {})
        lines.append(f"### `{spec['job_id']}`")
        lines.append("")
        lines.append(f"- Source model: `{train.get('model')}`")
        lines.append(f"- Run name: `{train.get('run_name')}`")
        lines.append(f"- Description: {description}")
        lines.append(
            "- Eval targets: "
            + ", ".join(
                f"`{target.get('model')}`"
                for target in spec.get("eval_targets", [])
                if isinstance(target, dict)
            )
        )
        lines.append("")
    return "\n".join(lines)
