#!/usr/bin/env python3
"""One-command NUC orchestration for Adversarial_Patch + YOLO-Bad-Triangle."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.colab_queue import (
    COLAB_BUNDLE_ROOT,
    COLAB_INCLUDE_PATHS,
    build_patch_job_specs,
    load_json_mapping,
    resolve_path,
    should_bundle_file,
    utc_iso,
    utc_stamp,
)

DEFAULT_CONFIG = REPO_ROOT / "configs" / "nuc_handoff.json"


@dataclass
class CommandResult:
    label: str
    cwd: Path
    command: list[str]
    exit_code: int

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


def resolve_repo_root(
    *,
    anchor: Path,
    raw: str | Path,
    fallbacks: list[Path] | None = None,
) -> Path:
    primary = resolve_path(anchor, raw)
    if primary.is_dir():
        return primary
    for fallback in fallbacks or []:
        if fallback.is_dir():
            log(f"repo root fallback selected: configured={primary} fallback={fallback}")
            return fallback.resolve()
    return primary


def log(message: str) -> None:
    print(f"{utc_iso()} [nuc-handoff] {message}")


def shell_quote(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def run_command(
    *,
    label: str,
    cwd: Path,
    command: list[str],
    dry_run: bool,
) -> CommandResult:
    log(f"{label}: {shell_quote(command)}")
    if dry_run:
        return CommandResult(label=label, cwd=cwd, command=command, exit_code=0)
    exit_code = subprocess.call(command, cwd=cwd)
    return CommandResult(label=label, cwd=cwd, command=command, exit_code=exit_code)


def ensure_venv(
    *,
    repo_root: Path,
    bootstrap_python: str,
    requirements_file: str,
    dry_run: bool,
) -> Path:
    venv_python = repo_root / ".venv" / "bin" / "python"
    if venv_python.is_file():
        return venv_python

    create_cmd = [bootstrap_python, "-m", "venv", str(repo_root / ".venv")]
    result = run_command(label=f"bootstrap:{repo_root.name}:venv", cwd=repo_root, command=create_cmd, dry_run=dry_run)
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to create venv for {repo_root} with {bootstrap_python}")

    pip_upgrade = [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"]
    result = run_command(label=f"bootstrap:{repo_root.name}:pip", cwd=repo_root, command=pip_upgrade, dry_run=dry_run)
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to upgrade pip in {repo_root}")

    install_cmd = [str(venv_python), "-m", "pip", "install", "-r", str(repo_root / requirements_file)]
    result = run_command(label=f"bootstrap:{repo_root.name}:requirements", cwd=repo_root, command=install_cmd, dry_run=dry_run)
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to install requirements for {repo_root}")
    return venv_python


def build_patch_matrix_payload(
    *,
    artifact_name: str,
    artifact_path: Path,
    ybt_output_root: str,
    source_dir: str,
    max_images: int,
    seed: int,
    defenses: list[str],
    defense_params: dict[str, Any],
    placement_modes: list[str],
    profile: str,
) -> dict[str, Any]:
    return {
        "profile": profile,
        "overrides": [
            f"data.source_dir={source_dir}",
            f"runner.output_root={ybt_output_root}",
            f"runner.max_images={max_images}",
            f"runner.seed={seed}",
        ],
        "artifacts": [
            {
                "name": artifact_name,
                "artifact_path": str(artifact_path),
                "placement_modes": placement_modes,
                "attack_params": {
                    "clean_detect_conf": 0.5,
                    "clean_detect_iou": 0.7,
                },
            }
        ],
        "defenses": defenses,
        "defense_params": defense_params,
    }


def patch_artifact_sidecar(patch_path: Path) -> Path:
    return patch_path.with_name("patch_artifact.json")


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def derive_artifact_entries(
    *,
    config: dict[str, Any],
    attack_repo_root: Path,
    job_specs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    existing = config.get("existing_artifacts") or []
    for raw in existing:
        if not isinstance(raw, dict):
            raise ValueError("existing_artifacts entries must be mappings.")
        patch_path = resolve_path(attack_repo_root, str(raw.get("patch_path") or ""))
        artifact_id = str(raw.get("artifact_id") or patch_path.parent.parent.name or patch_path.stem).strip()
        artifacts.append(
            {
                "artifact_id": artifact_id,
                "artifact_name": artifact_id,
                "patch_path": str(patch_path),
                "source_model": raw.get("source_model"),
                "failure_grid_models": list(raw.get("failure_grid_models") or []),
                "enable_patch_matrix": bool(raw.get("enable_patch_matrix", True)),
                "enable_physical": bool(raw.get("enable_physical", True)),
                "from_job": False,
            }
        )
    for spec in job_specs:
        local_eval = dict(spec.get("local_eval") or {})
        train = dict(spec.get("train") or {})
        artifact_id = str(spec["job_id"])
        source_model = train.get("model")
        artifacts.append(
            {
                "artifact_id": artifact_id,
                "artifact_name": str(train.get("run_name") or artifact_id),
                "patch_path": str(resolve_path(attack_repo_root, str(spec["expected_patch_path"]))),
                "source_model": source_model,
                "failure_grid_models": list(local_eval.get("failure_grid_models") or ([source_model] if source_model else [])),
                "enable_patch_matrix": bool(local_eval.get("enable_patch_matrix", True)),
                "enable_physical": bool(local_eval.get("enable_physical", True)),
                "from_job": True,
            }
        )
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for artifact in artifacts:
        key = str(artifact["artifact_id"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(artifact)
    return deduped


def collect_artifact_status(
    artifact: dict[str, Any],
    *,
    attack_repo_root: Path,
    local_defaults: dict[str, Any],
) -> dict[str, Any]:
    patch_path = resolve_path(attack_repo_root, str(artifact["patch_path"]))
    sidecar = patch_artifact_sidecar(patch_path)
    sidecar_payload = load_json_if_exists(sidecar)
    artifact_name = patch_path.parent.parent.name if patch_path.name == "patch.png" and patch_path.parent.name == "patches" else str(artifact["artifact_name"])
    failure_grid_models = list(artifact.get("failure_grid_models") or [])
    if not failure_grid_models and sidecar_payload.get("model"):
        failure_grid_models = [str(sidecar_payload["model"])]
    failure_grid_dir = resolve_path(attack_repo_root, str(local_defaults["failure_grid_output_dir"]))
    failure_reports = [
        failure_grid_dir / f"{artifact_name}_on_{model}" / "failure_grid_results.json"
        for model in failure_grid_models
    ]
    physical_dir = resolve_path(attack_repo_root, str(local_defaults["physical_output_dir"]))
    physical_summary = physical_dir / f"summary_{artifact_name}.json"
    return {
        "artifact_id": artifact["artifact_id"],
        "artifact_name": artifact_name,
        "patch_path": str(patch_path),
        "patch_exists": patch_path.is_file(),
        "sidecar_path": str(sidecar),
        "sidecar_exists": sidecar.is_file(),
        "sidecar_payload": sidecar_payload,
        "failure_grid_models": failure_grid_models,
        "failure_reports": [str(path) for path in failure_reports],
        "failure_reports_complete": all(path.is_file() for path in failure_reports) if failure_reports else False,
        "physical_summary": str(physical_summary),
        "physical_summary_exists": physical_summary.is_file(),
        "source_model": artifact.get("source_model") or sidecar_payload.get("model"),
        "enable_patch_matrix": bool(artifact.get("enable_patch_matrix", True)),
        "enable_physical": bool(artifact.get("enable_physical", True)),
        "from_job": bool(artifact.get("from_job")),
        "promotion_gate_ready": (
            patch_path.is_file()
            and sidecar.is_file()
            and (all(path.is_file() for path in failure_reports) if failure_reports else False)
            and physical_summary.is_file()
        ),
    }


def render_handoff_spec(
    *,
    bundle_dir: Path,
    attack_repo_root: Path,
    ybt_repo_root: Path,
    local_ready_script: Path,
    physical_queue_script: Path,
    colab_bundle_path: Path,
    job_specs: list[dict[str, Any]],
    artifact_statuses: list[dict[str, Any]],
) -> str:
    lines = [
        "# NUC Handoff Spec",
        "",
        f"- Generated at: `{utc_iso()}`",
        f"- Bundle directory: `{bundle_dir}`",
        f"- Attack repo: `{attack_repo_root}`",
        f"- YOLO-Bad-Triangle repo: `{ybt_repo_root}`",
        f"- Local rerun script: `{local_ready_script}`",
        f"- Physical queue script: `{physical_queue_script}`",
        f"- Colab bundle: `{colab_bundle_path}`",
        "",
        "## Local vs Colab Split",
        "",
        "- Colab: adversarial patch training, checkpointed runs, and transfer eval-only sweeps.",
        "- NUC: environment bootstrap, imported-patch defense matrices, digital failure grids, physical benchmark queueing, and final artifact gating.",
        "",
        "## Colab Queue",
        "",
    ]
    if not job_specs:
        lines.extend(["No Colab jobs configured.", ""])
    else:
        lines.extend([
            "| job_id | source_model | run_name | eval_targets |",
            "|---|---|---|---|",
        ])
        for spec in job_specs:
            train = dict(spec["train"])
            targets = ", ".join(str(target.get("model")) for target in spec.get("eval_targets", []) if isinstance(target, dict))
            lines.append(
                f"| `{spec['job_id']}` | `{train.get('model')}` | `{train.get('run_name')}` | `{targets}` |"
            )
        lines.append("")
    lines.extend([
        "## Artifact Intake Status",
        "",
        "| artifact | patch | sidecar | failure grid | physical | ready_for_promotion_gate |",
        "|---|---|---|---|---|---|",
    ])
    for status in artifact_statuses:
        lines.append(
            f"| `{status['artifact_name']}` | "
            f"{'yes' if status['patch_exists'] else 'no'} | "
            f"{'yes' if status['sidecar_exists'] else 'no'} | "
            f"{'yes' if status['failure_reports_complete'] else 'no'} | "
            f"{'yes' if status['physical_summary_exists'] else 'no'} | "
            f"{'yes' if status['promotion_gate_ready'] else 'no'} |"
        )
    lines.extend([
        "",
        "## Acceptance Gates",
        "",
        "- Every promoted patch artifact needs `patch_artifact.json`, digital failure-grid output, and a physical sector summary.",
        "- `v8m_source_transfer_v1` decides whether source-model size is a real transfer bottleneck.",
        "- The four `v8n_transfer_*` jobs decide whether self-ensemble earns promotion over the baseline.",
        "- `yolo26n_hybrid_loss_v1` must beat the current non-hybrid path before any cloth-EoT follow-on is promoted.",
        "- `oracle_patch_recover` stays an upper bound until imported-patch results show it materially beats the preprocess baselines.",
        "",
        "## Operator Notes",
        "",
        "- Re-run `./scripts/start_nuc_handoff.sh` after new Colab run directories are copied back into `outputs/`.",
        "- The generated Colab bundle is built from the current local repo state, not from GitHub. Use that bundle if local changes are ahead of remote.",
        "- The physical benchmark remains manual by design. The queue script only stages the commands.",
        "",
    ])
    return "\n".join(lines)


def write_shell_script(path: Path, commands: list[list[str]], *, cwd_comment: str) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"# {cwd_comment}",
    ]
    for command in commands:
        lines.append(shell_quote(command))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o755)


def add_colab_bundle(
    *,
    attack_repo_root: Path,
    bundle_dir: Path,
    job_specs_dir: Path,
    spec_sheet_path: Path,
) -> Path:
    tar_path = bundle_dir / f"{COLAB_BUNDLE_ROOT}.tar.gz"
    quickstart = bundle_dir / "COLAB_QUICKSTART.md"
    first_job = sorted(job_specs_dir.glob("*.json"))[0].name if job_specs_dir.exists() and any(job_specs_dir.glob("*.json")) else "<job>.json"
    quickstart.write_text(
        "\n".join(
            [
                "# Colab Quickstart",
                "",
                "1. Upload the generated tarball to Google Drive or the Colab runtime.",
                "2. In Colab, enable a GPU runtime.",
                "3. Run:",
                "",
                "```python",
                "from pathlib import Path",
                "import tarfile",
                "",
                "bundle = Path('/content/drive/MyDrive/adversarial_patch_colab_bundle.tar.gz')",
                "workdir = Path('/content/adversarial_patch_bundle')",
                "workdir.mkdir(parents=True, exist_ok=True)",
                "with tarfile.open(bundle, 'r:gz') as handle:",
                "    handle.extractall(workdir)",
                "```",
                "",
                "```bash",
                f"cd /content/adversarial_patch_bundle/{COLAB_BUNDLE_ROOT}",
                "python -m pip install -r requirements.txt",
                f"python scripts/run_colab_patch_job.py --job-spec handoff/colab_jobs/{first_job}",
                "```",
                "",
                "4. Copy the finished run directory back into `Adversarial_Patch/outputs/` on the NUC and rerun `./scripts/start_nuc_handoff.sh`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    with tarfile.open(tar_path, "w:gz") as handle:
        for relative in COLAB_INCLUDE_PATHS:
            source = attack_repo_root / relative
            if source.is_dir():
                for child in source.rglob("*"):
                    if not should_bundle_file(child):
                        continue
                    arcname = Path(COLAB_BUNDLE_ROOT) / relative / child.relative_to(source)
                    handle.add(child, arcname=str(arcname))
            elif source.is_file():
                arcname = Path(COLAB_BUNDLE_ROOT) / relative
                handle.add(source, arcname=str(arcname))
        for child in job_specs_dir.rglob("*"):
            if should_bundle_file(child):
                arcname = Path(COLAB_BUNDLE_ROOT) / "handoff" / "colab_jobs" / child.relative_to(job_specs_dir)
                handle.add(child, arcname=str(arcname))
        handle.add(quickstart, arcname=str(Path(COLAB_BUNDLE_ROOT) / "handoff" / "COLAB_QUICKSTART.md"))
        handle.add(spec_sheet_path, arcname=str(Path(COLAB_BUNDLE_ROOT) / "handoff" / "nuc_spec_sheet.md"))
    return tar_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and run the NUC handoff workflow.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to the JSON handoff config.")
    parser.add_argument("--bootstrap", action="store_true", help="Create repo venvs and install requirements if needed.")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip verify/check-environment commands.")
    parser.add_argument("--run-local-ready", action="store_true", help="Execute local-ready failure grids and patch matrices.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = load_json_mapping(resolve_path(REPO_ROOT, args.config))

    repo_roots = dict(config.get("repo_roots") or {})
    attack_repo_root = resolve_repo_root(anchor=REPO_ROOT, raw=str(repo_roots.get("attack_repo") or "."), fallbacks=[])
    ybt_repo_root = resolve_repo_root(
        anchor=REPO_ROOT,
        raw=str(repo_roots.get("ybt_repo") or "../YOLO-Bad-Triangle"),
        fallbacks=[
            attack_repo_root.parent / "YOLO-Bad-Triangle",
            attack_repo_root.parent.parent / "YOLO-Bad-Triangle",
            Path.home() / "ml-labs" / "YOLO-Bad-Triangle",
        ],
    )
    if not attack_repo_root.is_dir():
        raise FileNotFoundError(f"Attack repo root not found: {attack_repo_root}")
    if not ybt_repo_root.is_dir():
        raise FileNotFoundError(
            f"YOLO-Bad-Triangle repo root not found: {ybt_repo_root}. "
            "Update configs/nuc_handoff.json for the target NUC checkout."
        )
    bootstrap_cfg = dict(config.get("bootstrap") or {})
    local_defaults = dict(config.get("local_defaults") or {})
    colab_cfg = dict(config.get("colab") or {})

    bundle_root = resolve_path(attack_repo_root, str(colab_cfg.get("bundle_output_root") or "outputs/nuc_handoff"))
    bundle_dir = bundle_root / f"{str(colab_cfg.get('bundle_name_prefix') or 'nuc_handoff')}_{utc_stamp()}"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    job_specs_dir = bundle_dir / "colab_jobs"
    job_specs_dir.mkdir(parents=True, exist_ok=True)

    attack_python = attack_repo_root / ".venv" / "bin" / "python"
    ybt_python = ybt_repo_root / ".venv" / "bin" / "python"
    if args.bootstrap:
        attack_python = ensure_venv(
            repo_root=attack_repo_root,
            bootstrap_python=str(bootstrap_cfg.get("attack_python") or "python3"),
            requirements_file="requirements.txt",
            dry_run=bool(args.dry_run),
        )
        ybt_python = ensure_venv(
            repo_root=ybt_repo_root,
            bootstrap_python=str(bootstrap_cfg.get("ybt_python") or "python3.11"),
            requirements_file="requirements.txt",
            dry_run=bool(args.dry_run),
        )
    elif not attack_python.is_file() or not ybt_python.is_file():
        raise FileNotFoundError(
            "Missing repo venv(s). Re-run with --bootstrap or provision both repos first."
        )

    command_results: list[CommandResult] = []
    if not args.skip_preflight:
        command_results.append(
            run_command(
                label="attack-preflight",
                cwd=attack_repo_root,
                command=[str(attack_python), "scripts/verify_setup.py"],
                dry_run=bool(args.dry_run),
            )
        )
        command_results.append(
            run_command(
                label="ybt-preflight",
                cwd=ybt_repo_root,
                command=[str(ybt_python), "scripts/check_environment.py"],
                dry_run=bool(args.dry_run),
            )
        )

    job_specs = build_patch_job_specs(config, attack_repo_root)
    for spec in job_specs:
        job_spec_path = job_specs_dir / f"{spec['job_id']}.json"
        job_spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")

    artifact_entries = derive_artifact_entries(config=config, attack_repo_root=attack_repo_root, job_specs=job_specs)
    artifact_statuses = [
        collect_artifact_status(artifact, attack_repo_root=attack_repo_root, local_defaults=local_defaults)
        for artifact in artifact_entries
    ]

    local_ready_commands: list[list[str]] = []
    physical_queue_commands: list[list[str]] = []
    for status in artifact_statuses:
        if not status["patch_exists"]:
            continue
        patch_path = Path(status["patch_path"])
        source_model = str(status["source_model"] or "yolov8n")
        if bool(local_defaults.get("run_failure_grid", True)):
            for model_name in status["failure_grid_models"]:
                local_ready_commands.append(
                    [
                        str(attack_python),
                        str(attack_repo_root / "experiments" / "failure_grid.py"),
                        "--patch",
                        str(patch_path),
                        "--model",
                        str(model_name),
                        "--manifest",
                        str(resolve_path(attack_repo_root, str(local_defaults["failure_grid_manifest"]))),
                        "--output-dir",
                        str(resolve_path(attack_repo_root, str(local_defaults["failure_grid_output_dir"]))),
                    ]
                )
        if bool(local_defaults.get("run_patch_matrix", True)) and status["enable_patch_matrix"]:
            matrix_payload = build_patch_matrix_payload(
                artifact_name=str(status["artifact_name"]),
                artifact_path=patch_path,
                ybt_output_root=str(local_defaults["ybt_output_root"]),
                source_dir=str(local_defaults["ybt_source_dir"]),
                max_images=int(local_defaults["ybt_max_images"]),
                seed=int(local_defaults["ybt_seed"]),
                defenses=list(local_defaults["ybt_defenses"]),
                defense_params=dict(local_defaults["ybt_defense_params"]),
                placement_modes=list(local_defaults["ybt_placement_modes"]),
                profile=str(local_defaults["ybt_profile"]),
            )
            matrix_path = bundle_dir / f"patch_matrix_{status['artifact_id']}.yaml"
            matrix_path.write_text(json.dumps(matrix_payload, indent=2), encoding="utf-8")
            local_ready_commands.append(
                [
                    str(ybt_python),
                    str(ybt_repo_root / "scripts" / "run_unified.py"),
                    "patch-matrix",
                    "--matrix-config",
                    str(matrix_path),
                ]
            )
        if bool(local_defaults.get("prepare_physical_queue", True)) and status["enable_physical"]:
            physical_queue_commands.append(
                [
                    str(attack_python),
                    str(attack_repo_root / "experiments" / "physical_benchmark.py"),
                    "--patch",
                    str(patch_path),
                    "--artifact-name",
                    str(status["artifact_name"]),
                    "--model",
                    source_model,
                    "--output-dir",
                    str(resolve_path(attack_repo_root, str(local_defaults["physical_output_dir"]))),
                ]
            )
            if bool(local_defaults.get("run_physical_dry_run", False)):
                local_ready_commands.append(
                    [
                        str(attack_python),
                        str(attack_repo_root / "experiments" / "physical_benchmark.py"),
                        "--patch",
                        str(patch_path),
                        "--artifact-name",
                        str(status["artifact_name"]),
                        "--model",
                        source_model,
                        "--output-dir",
                        str(resolve_path(attack_repo_root, str(local_defaults["physical_output_dir"]))),
                        "--dry-run",
                    ]
                )

    local_ready_script = bundle_dir / "run_local_ready.sh"
    write_shell_script(local_ready_script, local_ready_commands or [["echo", "No local-ready commands generated."]], cwd_comment="Commands use absolute paths and can be run from any working directory.")
    physical_queue_script = bundle_dir / "run_physical_queue.sh"
    write_shell_script(physical_queue_script, physical_queue_commands or [["echo", "No physical benchmark queue generated."]], cwd_comment="Commands use absolute paths. These are manual-camera steps.")

    spec_sheet_path = bundle_dir / "nuc_spec_sheet.md"
    spec_sheet_path.write_text(
        render_handoff_spec(
            bundle_dir=bundle_dir,
            attack_repo_root=attack_repo_root,
            ybt_repo_root=ybt_repo_root,
            local_ready_script=local_ready_script,
            physical_queue_script=physical_queue_script,
            colab_bundle_path=bundle_dir / f"{COLAB_BUNDLE_ROOT}.tar.gz",
            job_specs=job_specs,
            artifact_statuses=artifact_statuses,
        ),
        encoding="utf-8",
    )
    colab_bundle_path = add_colab_bundle(
        attack_repo_root=attack_repo_root,
        bundle_dir=bundle_dir,
        job_specs_dir=job_specs_dir,
        spec_sheet_path=spec_sheet_path,
    )

    if args.run_local_ready:
        for command in local_ready_commands:
            cwd = attack_repo_root if str(attack_repo_root) in command[1] else ybt_repo_root
            command_results.append(
                run_command(
                    label=f"local-ready:{Path(command[1]).name}",
                    cwd=cwd,
                    command=command,
                    dry_run=bool(args.dry_run),
                )
            )

    manifest = {
        "generated_at_utc": utc_iso(),
        "bundle_dir": str(bundle_dir),
        "colab_bundle": str(colab_bundle_path),
        "job_specs": [str(path) for path in sorted(job_specs_dir.glob("*.json"))],
        "artifact_statuses": artifact_statuses,
        "command_results": [
            {
                "label": result.label,
                "cwd": str(result.cwd),
                "command": result.command,
                "exit_code": result.exit_code,
            }
            for result in command_results
        ],
    }
    manifest_path = bundle_dir / "handoff_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    failures = [result for result in command_results if not result.ok]
    log(f"Bundle directory: {bundle_dir}")
    log(f"Spec sheet: {spec_sheet_path}")
    log(f"Colab bundle: {colab_bundle_path}")
    log(f"Manifest: {manifest_path}")
    if failures:
        for failure in failures:
            log(f"FAILED {failure.label} (exit={failure.exit_code})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
