#!/usr/bin/env python3
"""One-command NUC orchestration for Adversarial_Patch + YOLO-Bad-Triangle."""
from __future__ import annotations

import argparse
import json
import re
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
    render_colab_job_index,
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


def results_sidecar_for_patch(patch_path: Path) -> Path | None:
    if patch_path.name != "patch.png":
        return None
    if patch_path.parent.name != "patches":
        return None
    return patch_path.parent.parent / "results.json"


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def sanitize_segment(value: object, fallback: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value or "").strip().lower()).strip("-")
    return cleaned or fallback


def read_suppression_pct(payload: dict[str, Any]) -> float | None:
    raw = payload.get("detection_suppression_pct")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def colab_job_summary_path(*, attack_repo_root: Path, job_id: str) -> Path:
    return attack_repo_root / "outputs" / "colab_job_summaries" / f"{job_id}.json"


def expected_eval_result_entries(job_spec: dict[str, Any], *, attack_repo_root: Path) -> list[dict[str, Any]]:
    train = dict(job_spec.get("train") or {})
    default_output_root = str(train.get("output_dir") or "outputs")
    entries: list[dict[str, Any]] = []
    for index, target in enumerate(job_spec.get("eval_targets") or []):
        if not isinstance(target, dict):
            raise ValueError("Each eval_targets entry must be a mapping.")
        model_name = str(target.get("model") or f"eval{index}").strip()
        output_root = resolve_path(
            attack_repo_root,
            str(target.get("output_dir") or default_output_root),
        )
        run_name = str(target.get("run_name") or f"{job_spec['job_id']}__transfer__{model_name}")
        result_path = output_root / run_name / "results.json"
        payload = load_json_if_exists(result_path)
        entries.append(
            {
                "model": model_name,
                "run_name": run_name,
                "results_path": str(result_path),
                "results_exists": result_path.is_file(),
                "results_payload": payload,
                "detection_suppression_pct": read_suppression_pct(payload),
            }
        )
    return entries


def expected_patch_matrix_run_summaries(
    *,
    artifact_name: str,
    ybt_repo_root: Path,
    local_defaults: dict[str, Any],
    enable_patch_matrix: bool,
) -> list[Path]:
    if not enable_patch_matrix:
        return []
    output_root = resolve_path(ybt_repo_root, str(local_defaults["ybt_output_root"]))
    placement_modes = list(local_defaults.get("ybt_placement_modes") or ["largest_person_torso"])
    defenses = list(local_defaults.get("ybt_defenses") or ["none"])
    run_summaries: list[Path] = []
    for placement_mode in placement_modes:
        for defense_name in defenses:
            run_name = (
                f"patchmatrix__{sanitize_segment(artifact_name, 'artifact')}"
                f"__{sanitize_segment(placement_mode, 'placement')}"
                f"__{sanitize_segment(defense_name, 'defense')}"
            )
            run_summaries.append(output_root / run_name / "run_summary.json")
    return run_summaries


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
    ybt_repo_root: Path,
    local_defaults: dict[str, Any],
) -> dict[str, Any]:
    patch_path = resolve_path(attack_repo_root, str(artifact["patch_path"]))
    sidecar = patch_artifact_sidecar(patch_path)
    sidecar_payload = load_json_if_exists(sidecar)
    results_path = results_sidecar_for_patch(patch_path)
    results_payload = load_json_if_exists(results_path) if results_path else {}
    artifact_name = patch_path.parent.parent.name if patch_path.name == "patch.png" and patch_path.parent.name == "patches" else str(artifact["artifact_name"])
    failure_grid_models = list(artifact.get("failure_grid_models") or [])
    if not failure_grid_models and sidecar_payload.get("model"):
        failure_grid_models = [str(sidecar_payload["model"])]
    failure_grid_dir = resolve_path(attack_repo_root, str(local_defaults["failure_grid_output_dir"]))
    failure_reports = [
        failure_grid_dir / f"{artifact_name}_on_{model}" / "failure_grid_results.json"
        for model in failure_grid_models
    ]
    enable_patch_matrix = bool(artifact.get("enable_patch_matrix", True))
    patch_matrix_summaries = expected_patch_matrix_run_summaries(
        artifact_name=artifact_name,
        ybt_repo_root=ybt_repo_root,
        local_defaults=local_defaults,
        enable_patch_matrix=enable_patch_matrix,
    )
    physical_dir = resolve_path(attack_repo_root, str(local_defaults["physical_output_dir"]))
    physical_summary = physical_dir / f"summary_{artifact_name}.json"
    failure_reports_complete = all(path.is_file() for path in failure_reports) if failure_reports else True
    patch_matrix_complete = all(path.is_file() for path in patch_matrix_summaries) if patch_matrix_summaries else not enable_patch_matrix
    results_exists = bool(results_path and results_path.is_file())
    digital_gate_ready = (
        patch_path.is_file()
        and sidecar.is_file()
        and results_exists
        and failure_reports_complete
        and patch_matrix_complete
    )
    return {
        "artifact_id": artifact["artifact_id"],
        "artifact_name": artifact_name,
        "patch_path": str(patch_path),
        "patch_exists": patch_path.is_file(),
        "sidecar_path": str(sidecar),
        "sidecar_exists": sidecar.is_file(),
        "sidecar_payload": sidecar_payload,
        "results_path": str(results_path) if results_path else None,
        "results_exists": results_exists,
        "results_payload": results_payload,
        "failure_grid_models": failure_grid_models,
        "failure_reports": [str(path) for path in failure_reports],
        "failure_reports_complete": failure_reports_complete,
        "patch_matrix_expected_runs": [str(path) for path in patch_matrix_summaries],
        "patch_matrix_complete": patch_matrix_complete,
        "physical_summary": str(physical_summary),
        "physical_summary_exists": physical_summary.is_file(),
        "source_model": artifact.get("source_model") or sidecar_payload.get("model") or results_payload.get("model"),
        "enable_patch_matrix": enable_patch_matrix,
        "enable_physical": bool(artifact.get("enable_physical", True)),
        "from_job": bool(artifact.get("from_job")),
        "digital_gate_ready": digital_gate_ready,
        "promotion_gate_ready": digital_gate_ready and physical_summary.is_file(),
    }


def collect_job_status(
    job_spec: dict[str, Any],
    *,
    attack_repo_root: Path,
    artifact_status_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    job_id = str(job_spec["job_id"])
    train = dict(job_spec.get("train") or {})
    expected_run_dir = resolve_path(attack_repo_root, str(job_spec["expected_run_dir"]))
    train_results_path = expected_run_dir / "results.json"
    train_results_payload = load_json_if_exists(train_results_path)
    patch_path = resolve_path(attack_repo_root, str(job_spec["expected_patch_path"]))
    sidecar_path = patch_artifact_sidecar(patch_path)
    eval_results = expected_eval_result_entries(job_spec, attack_repo_root=attack_repo_root)
    summary_path = colab_job_summary_path(attack_repo_root=attack_repo_root, job_id=job_id)
    artifact_status = artifact_status_by_id.get(job_id, {})
    transfer_metrics = {
        str(entry["model"]): entry["detection_suppression_pct"]
        for entry in eval_results
        if entry["detection_suppression_pct"] is not None
    }
    return {
        "job_id": job_id,
        "source_model": train.get("model"),
        "artifact_name": str(train.get("run_name") or job_id),
        "expected_run_dir": str(expected_run_dir),
        "train_results_path": str(train_results_path),
        "train_results_exists": train_results_path.is_file(),
        "train_results_payload": train_results_payload,
        "train_suppression_pct": read_suppression_pct(train_results_payload),
        "patch_path": str(patch_path),
        "patch_exists": patch_path.is_file(),
        "sidecar_path": str(sidecar_path),
        "sidecar_exists": sidecar_path.is_file(),
        "colab_summary_path": str(summary_path),
        "colab_summary_exists": summary_path.is_file(),
        "eval_results": eval_results,
        "transfer_metrics": transfer_metrics,
        "colab_return_complete": (
            train_results_path.is_file()
            and patch_path.is_file()
            and sidecar_path.is_file()
            and summary_path.is_file()
            and all(entry["results_exists"] for entry in eval_results)
        ),
        "digital_gate_ready": bool(artifact_status.get("digital_gate_ready")),
        "patch_matrix_complete": bool(artifact_status.get("patch_matrix_complete")),
        "failure_reports_complete": bool(artifact_status.get("failure_reports_complete")),
        "physical_summary_exists": bool(artifact_status.get("physical_summary_exists")),
        "promotion_gate_ready": bool(artifact_status.get("promotion_gate_ready")),
    }


def build_transfer_candidate(
    *,
    job_id: str,
    job_status: dict[str, Any],
    baselines: dict[str, float],
    deltas: dict[str, float],
) -> dict[str, Any] | None:
    rows: list[dict[str, Any]] = []
    normalized_scores: list[float] = []
    total_delta = 0.0
    total_suppression = 0.0
    for model_name, baseline in baselines.items():
        actual = job_status["transfer_metrics"].get(model_name)
        if actual is None:
            return None
        delta = round(float(actual) - float(baseline), 1)
        threshold = float(deltas.get(model_name, 0.0))
        norm = delta / threshold if threshold else delta
        rows.append(
            {
                "model": model_name,
                "baseline": float(baseline),
                "actual": float(actual),
                "delta_vs_baseline": delta,
                "min_delta_to_pass": threshold,
                "meets_threshold": delta >= threshold,
                "normalized_gain": round(norm, 3),
            }
        )
        normalized_scores.append(norm)
        total_delta += delta
        total_suppression += float(actual)
    return {
        "job_id": job_id,
        "artifact_name": job_status["artifact_name"],
        "metrics": rows,
        "score_max_normalized_gain": max(normalized_scores) if normalized_scores else float("-inf"),
        "score_total_delta": round(total_delta, 1),
        "score_total_suppression": round(total_suppression, 1),
        "digital_gate_ready": bool(job_status.get("digital_gate_ready")),
    }


def evaluate_transfer_gate(
    *,
    gate_id: str,
    job_id: str,
    job_status_by_id: dict[str, dict[str, Any]],
    baselines: dict[str, float],
    deltas: dict[str, float],
) -> dict[str, Any]:
    job_status = job_status_by_id.get(job_id)
    if not job_status:
        return {
            "gate_id": gate_id,
            "state": "waiting",
            "job_id": job_id,
            "summary": "Job is not present in the enabled queue.",
            "metrics": [],
        }
    candidate = build_transfer_candidate(job_id=job_id, job_status=job_status, baselines=baselines, deltas=deltas)
    if candidate is None:
        return {
            "gate_id": gate_id,
            "state": "waiting",
            "job_id": job_id,
            "summary": "Waiting for transfer eval results.",
            "metrics": [],
        }
    passes = candidate["score_max_normalized_gain"] >= 1.0
    return {
        "gate_id": gate_id,
        "state": "pass" if passes else "fail",
        "job_id": job_id,
        "summary": (
            "Larger-source training cleared the minimum transfer gain."
            if passes
            else "Larger-source training did not clear the minimum transfer gain."
        ),
        "metrics": candidate["metrics"],
        "winner_job_id": job_id,
        "winner_artifact_name": candidate["artifact_name"],
        "winner_score_max_normalized_gain": candidate["score_max_normalized_gain"],
    }


def evaluate_ablation_gate(
    *,
    gate_id: str,
    job_ids: list[str],
    job_status_by_id: dict[str, dict[str, Any]],
    baselines: dict[str, float],
    deltas: dict[str, float],
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    missing: list[str] = []
    for job_id in job_ids:
        job_status = job_status_by_id.get(job_id)
        if not job_status:
            missing.append(job_id)
            continue
        candidate = build_transfer_candidate(job_id=job_id, job_status=job_status, baselines=baselines, deltas=deltas)
        if candidate is None:
            missing.append(job_id)
            continue
        candidates.append(candidate)
    if missing:
        return {
            "gate_id": gate_id,
            "state": "waiting",
            "job_ids": job_ids,
            "summary": f"Waiting for ablation results: {', '.join(missing)}.",
            "candidates": candidates,
        }
    winner = max(
        candidates,
        key=lambda item: (
            item["score_max_normalized_gain"],
            item["score_total_delta"],
            item["score_total_suppression"],
        ),
    )
    passes = winner["score_max_normalized_gain"] >= 1.0
    return {
        "gate_id": gate_id,
        "state": "pass" if passes else "fail",
        "job_ids": job_ids,
        "summary": (
            f"Promote `{winner['job_id']}` as the best v8n transfer cell."
            if passes
            else f"No v8n ablation cell cleared the minimum transfer gain. Best observed cell: `{winner['job_id']}`."
        ),
        "candidates": candidates,
        "winner_job_id": winner["job_id"],
        "winner_artifact_name": winner["artifact_name"],
        "winner_score_max_normalized_gain": winner["score_max_normalized_gain"],
    }


def evaluate_yolo26_gate(
    *,
    gate_id: str,
    job_id: str,
    follow_on_job_id: str,
    follow_on_enabled: bool,
    job_status_by_id: dict[str, dict[str, Any]],
    min_direct_suppression: float,
) -> dict[str, Any]:
    job_status = job_status_by_id.get(job_id)
    if not job_status:
        return {
            "gate_id": gate_id,
            "state": "waiting",
            "job_id": job_id,
            "summary": "Hybrid-loss job is not present in the enabled queue.",
        }
    direct = job_status.get("train_suppression_pct")
    if direct is None:
        return {
            "gate_id": gate_id,
            "state": "waiting",
            "job_id": job_id,
            "summary": "Waiting for hybrid-loss training results.",
        }
    digital_requirements = {
        "results_exists": bool(job_status.get("train_results_exists")),
        "sidecar_exists": bool(job_status.get("sidecar_exists")),
        "failure_grid_complete": bool(job_status.get("failure_reports_complete")),
        "patch_matrix_complete": bool(job_status.get("patch_matrix_complete")),
    }
    digital_ready = all(digital_requirements.values())
    if float(direct) < float(min_direct_suppression):
        return {
            "gate_id": gate_id,
            "state": "fail",
            "job_id": job_id,
            "summary": (
                f"Hybrid-loss direct suppression {float(direct):.1f}% did not reach "
                f"the {float(min_direct_suppression):.1f}% floor."
            ),
            "direct_suppression_pct": float(direct),
            "min_direct_suppression": float(min_direct_suppression),
            "digital_requirements": digital_requirements,
            "ready_for_follow_on": False,
        }
    if not digital_ready:
        return {
            "gate_id": gate_id,
            "state": "waiting",
            "job_id": job_id,
            "summary": "Hybrid-loss suppression passed, but digital gate artifacts are still incomplete.",
            "direct_suppression_pct": float(direct),
            "min_direct_suppression": float(min_direct_suppression),
            "digital_requirements": digital_requirements,
            "ready_for_follow_on": False,
        }
    if follow_on_enabled:
        state = "pass"
        summary = f"Hybrid-loss artifact cleared Gate C. `{follow_on_job_id}` is eligible to run."
    else:
        state = "ready_to_enable_follow_on"
        summary = (
            f"Hybrid-loss artifact cleared Gate C. Enable `{follow_on_job_id}` in both queue configs "
            "before building the next bundle."
        )
    return {
        "gate_id": gate_id,
        "state": state,
        "job_id": job_id,
        "summary": summary,
        "direct_suppression_pct": float(direct),
        "min_direct_suppression": float(min_direct_suppression),
        "digital_requirements": digital_requirements,
        "ready_for_follow_on": True,
    }


def determine_transfer_winner(
    *,
    job_ids: list[str],
    job_status_by_id: dict[str, dict[str, Any]],
    baselines: dict[str, float],
    deltas: dict[str, float],
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for job_id in job_ids:
        job_status = job_status_by_id.get(job_id)
        if not job_status or not job_status.get("digital_gate_ready"):
            continue
        candidate = build_transfer_candidate(job_id=job_id, job_status=job_status, baselines=baselines, deltas=deltas)
        if candidate is not None:
            candidates.append(candidate)
    if not candidates:
        return None
    winner = max(
        candidates,
        key=lambda item: (
            item["score_max_normalized_gain"],
            item["score_total_delta"],
            item["score_total_suppression"],
        ),
    )
    return winner if winner["score_max_normalized_gain"] >= 1.0 else None


def determine_yolo26_winner(
    *,
    job_ids: list[str],
    job_status_by_id: dict[str, dict[str, Any]],
    min_direct_suppression: float,
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for job_id in job_ids:
        job_status = job_status_by_id.get(job_id)
        if not job_status or not job_status.get("digital_gate_ready"):
            continue
        direct = job_status.get("train_suppression_pct")
        if direct is None or float(direct) < float(min_direct_suppression):
            continue
        y11_transfer = job_status.get("transfer_metrics", {}).get("yolo11n")
        candidates.append(
            {
                "job_id": job_id,
                "artifact_name": job_status["artifact_name"],
                "direct_suppression_pct": float(direct),
                "yolo11n_transfer_pct": float(y11_transfer) if y11_transfer is not None else float("-inf"),
            }
        )
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item["direct_suppression_pct"], item["yolo11n_transfer_pct"]))


def determine_next_step(
    *,
    queue_order: list[str],
    job_status_by_id: dict[str, dict[str, Any]],
    gate_statuses: dict[str, dict[str, Any]],
    enabled_job_ids: set[str],
    transfer_winner: dict[str, Any] | None,
    yolo26_winner: dict[str, Any] | None,
) -> dict[str, Any]:
    gate_c = gate_statuses.get("gate_c", {})
    tps_job_id = str(gate_c.get("follow_on_job_id") or "")
    for job_id in queue_order:
        if job_id == tps_job_id:
            continue
        job_status = job_status_by_id.get(job_id)
        if not job_status or not job_status.get("colab_return_complete"):
            return {
                "kind": "colab_job",
                "job_id": job_id,
                "summary": f"Run `{job_id}` next in Colab, then copy the returned run back into `outputs/` and rerun `./scripts/start_nuc_handoff.sh`.",
            }
    if gate_c.get("state") == "ready_to_enable_follow_on":
        return {
            "kind": "config_edit",
            "job_id": tps_job_id or None,
            "summary": (
                f"Enable `{tps_job_id}` in both queue configs, rebuild the handoff bundle, and run it alone."
                if tps_job_id
                else "Enable the configured TPS follow-on job before the next bundle."
            ),
        }
    if tps_job_id and tps_job_id in enabled_job_ids:
        tps_status = job_status_by_id.get(tps_job_id)
        if not tps_status or not tps_status.get("colab_return_complete"):
            if gate_c.get("state") == "pass":
                return {
                    "kind": "colab_job",
                    "job_id": tps_job_id,
                    "summary": f"Run `{tps_job_id}` next in Colab, then copy the returned run back into `outputs/` and rerun `./scripts/start_nuc_handoff.sh`.",
                }
    physical_targets = [item["job_id"] for item in [transfer_winner, yolo26_winner] if item]
    if physical_targets:
        return {
            "kind": "physical",
            "job_ids": physical_targets,
            "summary": "Digital winners are ready for physical benchmarking. Run the generated physical queue for the promoted artifacts only.",
        }
    return {
        "kind": "done",
        "summary": "No further Colab jobs are pending. Review the spec sheet and outputs for any remaining manual follow-up.",
    }


def build_sequential_status(
    *,
    config: dict[str, Any],
    job_statuses: list[dict[str, Any]],
    enabled_job_ids: set[str],
) -> dict[str, Any]:
    sequential_cfg = dict(config.get("sequential_plan") or {})
    gate_cfg = dict(sequential_cfg.get("gates") or {})
    baselines = dict(sequential_cfg.get("baselines") or {})
    transfer_baselines = dict(baselines.get("v8_transfer") or {})
    queue_order = [str(item) for item in sequential_cfg.get("queue_order") or [status["job_id"] for status in job_statuses]]
    enabled_queue_order = [job_id for job_id in queue_order if job_id in enabled_job_ids]
    job_status_by_id = {str(status["job_id"]): status for status in job_statuses}

    gate_a_cfg = dict(gate_cfg.get("gate_a") or {})
    gate_b_cfg = dict(gate_cfg.get("gate_b") or {})
    gate_c_cfg = dict(gate_cfg.get("gate_c") or {})

    gate_a = evaluate_transfer_gate(
        gate_id="gate_a",
        job_id=str(gate_a_cfg.get("job_id") or "v8m_source_transfer_v1"),
        job_status_by_id=job_status_by_id,
        baselines={key: float(value) for key, value in transfer_baselines.items()},
        deltas={key: float(value) for key, value in dict(gate_a_cfg.get("deltas") or {}).items()},
    )
    gate_b_job_ids = [str(item) for item in gate_b_cfg.get("job_ids") or []]
    gate_b = evaluate_ablation_gate(
        gate_id="gate_b",
        job_ids=gate_b_job_ids,
        job_status_by_id=job_status_by_id,
        baselines={key: float(value) for key, value in transfer_baselines.items()},
        deltas={key: float(value) for key, value in dict(gate_b_cfg.get("deltas") or {}).items()},
    )
    follow_on_job_id = str(gate_c_cfg.get("follow_on_job_id") or "yolo26n_hybrid_loss_tps_v1")
    gate_c = evaluate_yolo26_gate(
        gate_id="gate_c",
        job_id=str(gate_c_cfg.get("job_id") or "yolo26n_hybrid_loss_v1"),
        follow_on_job_id=follow_on_job_id,
        follow_on_enabled=follow_on_job_id in enabled_job_ids,
        job_status_by_id=job_status_by_id,
        min_direct_suppression=float(gate_c_cfg.get("min_direct_suppression") or 25.0),
    )
    gate_c["follow_on_job_id"] = follow_on_job_id

    transfer_winner = determine_transfer_winner(
        job_ids=[str(gate_a_cfg.get("job_id") or "v8m_source_transfer_v1"), *gate_b_job_ids],
        job_status_by_id=job_status_by_id,
        baselines={key: float(value) for key, value in transfer_baselines.items()},
        deltas={key: float(value) for key, value in dict(gate_b_cfg.get("deltas") or {}).items()},
    )
    yolo26_winner = determine_yolo26_winner(
        job_ids=[str(gate_c_cfg.get("job_id") or "yolo26n_hybrid_loss_v1"), follow_on_job_id],
        job_status_by_id=job_status_by_id,
        min_direct_suppression=float(gate_c_cfg.get("min_direct_suppression") or 25.0),
    )
    gate_statuses = {
        "gate_a": gate_a,
        "gate_b": gate_b,
        "gate_c": gate_c,
    }
    next_step = determine_next_step(
        queue_order=enabled_queue_order,
        job_status_by_id=job_status_by_id,
        gate_statuses=gate_statuses,
        enabled_job_ids=enabled_job_ids,
        transfer_winner=transfer_winner,
        yolo26_winner=yolo26_winner,
    )
    return {
        "queue_order": enabled_queue_order,
        "job_statuses": job_statuses,
        "gate_statuses": gate_statuses,
        "promoted_artifacts": {
            "transfer_winner": transfer_winner,
            "yolo26_winner": yolo26_winner,
        },
        "next_step": next_step,
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
    sequential_status: dict[str, Any],
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
        "## Recommended Next Step",
        "",
        f"- {sequential_status.get('next_step', {}).get('summary', 'No next step available.')}",
        "",
        "## Sequential Queue Status",
        "",
        "| job_id | colab_return | digital_gate | direct_pct | y11_transfer | y26_transfer | physical |",
        "|---|---|---|---|---|---|---|",
    ]
    for job_status in sequential_status.get("job_statuses", []):
        transfer_metrics = dict(job_status.get("transfer_metrics") or {})
        direct = job_status.get("train_suppression_pct")
        lines.append(
            f"| `{job_status['job_id']}` | "
            f"{'yes' if job_status.get('colab_return_complete') else 'no'} | "
            f"{'yes' if job_status.get('digital_gate_ready') else 'no'} | "
            f"{f'{float(direct):.1f}' if direct is not None else '—'} | "
            f"{f'{float(transfer_metrics['yolo11n']):.1f}' if transfer_metrics.get('yolo11n') is not None else '—'} | "
            f"{f'{float(transfer_metrics['yolo26n']):.1f}' if transfer_metrics.get('yolo26n') is not None else '—'} | "
            f"{'yes' if job_status.get('physical_summary_exists') else 'no'} |"
        )
    lines.extend([
        "",
        "## Gate Status",
        "",
        "| gate | state | summary |",
        "|---|---|---|",
    ])
    for gate_id in ("gate_a", "gate_b", "gate_c"):
        gate = dict(sequential_status.get("gate_statuses", {}).get(gate_id) or {})
        lines.append(f"| `{gate_id}` | `{gate.get('state', 'unknown')}` | {gate.get('summary', '—')} |")
    lines.extend([
        "",
        "## Promoted Digital Winners",
        "",
    ])
    transfer_winner = dict(sequential_status.get("promoted_artifacts", {}).get("transfer_winner") or {})
    yolo26_winner = dict(sequential_status.get("promoted_artifacts", {}).get("yolo26_winner") or {})
    lines.append(
        f"- Transfer winner: `{transfer_winner.get('job_id', 'none')}`"
        if transfer_winner
        else "- Transfer winner: none yet"
    )
    lines.append(
        f"- YOLO26 winner: `{yolo26_winner.get('job_id', 'none')}`"
        if yolo26_winner
        else "- YOLO26 winner: none yet"
    )
    lines.extend([
        "",
        "## Colab Queue",
        "",
    ])
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
        "| artifact | patch | results | sidecar | failure grid | patch matrix | physical | ready_for_promotion_gate |",
        "|---|---|---|---|---|---|---|---|",
    ])
    for status in artifact_statuses:
        lines.append(
            f"| `{status['artifact_name']}` | "
            f"{'yes' if status['patch_exists'] else 'no'} | "
            f"{'yes' if status['results_exists'] else 'no'} | "
            f"{'yes' if status['sidecar_exists'] else 'no'} | "
            f"{'yes' if status['failure_reports_complete'] else 'no'} | "
            f"{'yes' if status['patch_matrix_complete'] else 'no'} | "
            f"{'yes' if status['physical_summary_exists'] else 'no'} | "
            f"{'yes' if status['promotion_gate_ready'] else 'no'} |"
        )
    lines.extend([
        "",
        "## Acceptance Gates",
        "",
        "- Every promoted patch artifact needs `patch.png`, `results.json`, `patch_artifact.json`, digital failure-grid output, imported-patch matrix output, and a physical sector summary.",
        "- `v8m_source_transfer_v1` is compared against the current repo baselines `v8n → v11n = 33.3%` and `v8n → v26n = 14.0%`.",
        "- The four `v8n_transfer_*` jobs are ranked by normalized gain over those baselines; the best passing cell is the promoted v8n candidate.",
        "- `yolo26n_hybrid_loss_v1` must reach at least `25.0%` direct suppression and clear the digital gate before the TPS follow-on is allowed.",
        "- Physical benchmarking is queued only for promoted digital winners.",
        "",
        "## Operator Notes",
        "",
        "- Re-run `./scripts/start_nuc_handoff.sh` after new Colab run directories are copied back into `outputs/`.",
        "- The generated Colab bundle is built from the current local repo state, not from GitHub. Use that bundle if local changes are ahead of remote.",
        "- The physical benchmark remains manual by design. The queue script only stages commands for promoted winners.",
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


def write_colab_handoff_assets(
    *,
    handoff_dir: Path,
    job_specs: list[dict[str, Any]],
    recommended_job_id: str | None,
) -> None:
    handoff_dir.mkdir(parents=True, exist_ok=True)
    index_path = handoff_dir / "colab_job_index.md"
    index_path.write_text(render_colab_job_index(job_specs), encoding="utf-8")

    run_all_path = handoff_dir / "run_all_jobs.sh"
    run_all_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        'ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"',
        'cd "$ROOT_DIR"',
        "",
    ]
    for spec in job_specs:
        run_all_lines.append(f"bash handoff/run_{spec['job_id']}.sh")
    run_all_lines.append("")
    run_all_path.write_text("\n".join(run_all_lines), encoding="utf-8")
    run_all_path.chmod(0o755)

    for spec in job_specs:
        job_id = str(spec["job_id"])
        write_shell_script(
            handoff_dir / f"run_{job_id}.sh",
            [["python", "scripts/run_colab_patch_job.py", "--job-spec", f"handoff/colab_jobs/{job_id}.json"]],
            cwd_comment="Run this inside the extracted Colab bundle root.",
        )
        write_shell_script(
            handoff_dir / f"resume_{job_id}.sh",
            [["python", "scripts/run_colab_patch_job.py", "--job-spec", f"handoff/colab_jobs/{job_id}.json", "--resume"]],
            cwd_comment="Resume this job inside the extracted Colab bundle root.",
        )

    first_job = recommended_job_id or (str(job_specs[0]["job_id"]) if job_specs else "<job>")
    quickstart_path = handoff_dir / "COLAB_QUICKSTART.md"
    quickstart_path.write_text(
        "\n".join(
            [
                "# Colab Quickstart",
                "",
                "1. Upload the generated tarball to Google Drive or the Colab runtime.",
                "2. In Colab, enable a GPU runtime.",
                "3. Extract the tarball, install requirements, and run the recommended wrapper:",
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
                f"bash handoff/run_{first_job}.sh",
                "```",
                "",
                "4. After the job finishes, copy the exported run directory and job summary back into `Adversarial_Patch/outputs/` on the NUC and rerun `./scripts/start_nuc_handoff.sh`.",
                "",
                "Use `bash handoff/run_all_jobs.sh` only if you intentionally want the full enabled queue without gate pauses.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def add_colab_bundle(
    *,
    attack_repo_root: Path,
    bundle_dir: Path,
    handoff_dir: Path,
    extra_paths: list[Path],
) -> Path:
    tar_path = bundle_dir / f"{COLAB_BUNDLE_ROOT}.tar.gz"
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
        for child in handoff_dir.rglob("*"):
            if should_bundle_file(child):
                arcname = Path(COLAB_BUNDLE_ROOT) / "handoff" / child.relative_to(handoff_dir)
                handle.add(child, arcname=str(arcname))
        for extra_path in extra_paths:
            if should_bundle_file(extra_path):
                handle.add(extra_path, arcname=str(Path(COLAB_BUNDLE_ROOT) / extra_path.name))
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
    raw_jobs_payload = list(colab_cfg.get("jobs") or config.get("jobs") or [])
    configured_job_ids = {
        str(raw.get("job_id") or "").strip()
        for raw in raw_jobs_payload
        if isinstance(raw, dict) and str(raw.get("job_id") or "").strip()
    }
    enabled_job_ids = {
        str(raw.get("job_id") or "").strip()
        for raw in raw_jobs_payload
        if isinstance(raw, dict)
        and str(raw.get("job_id") or "").strip()
        and raw.get("enabled", True) is not False
    }

    bundle_root = resolve_path(attack_repo_root, str(colab_cfg.get("bundle_output_root") or "outputs/nuc_handoff"))
    bundle_dir = bundle_root / f"{str(colab_cfg.get('bundle_name_prefix') or 'nuc_handoff')}_{utc_stamp()}"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    handoff_dir = bundle_dir / "handoff"
    job_specs_dir = handoff_dir / "colab_jobs"
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
        collect_artifact_status(
            artifact,
            attack_repo_root=attack_repo_root,
            ybt_repo_root=ybt_repo_root,
            local_defaults=local_defaults,
        )
        for artifact in artifact_entries
    ]
    artifact_status_by_id = {str(status["artifact_id"]): status for status in artifact_statuses}
    job_statuses = [
        collect_job_status(
            spec,
            attack_repo_root=attack_repo_root,
            artifact_status_by_id=artifact_status_by_id,
        )
        for spec in job_specs
    ]
    sequential_status = build_sequential_status(
        config=config,
        job_statuses=job_statuses,
        enabled_job_ids=enabled_job_ids,
    )

    local_ready_commands: list[list[str]] = []
    for status in artifact_statuses:
        if not status["patch_exists"]:
            continue
        patch_path = Path(status["patch_path"])
        if bool(local_defaults.get("run_failure_grid", True)) and not status["failure_reports_complete"]:
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
        if bool(local_defaults.get("run_patch_matrix", True)) and status["enable_patch_matrix"] and not status["patch_matrix_complete"]:
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

    physical_queue_commands: list[list[str]] = []
    promoted = dict(sequential_status.get("promoted_artifacts") or {})
    promoted_job_ids = [
        item["job_id"]
        for item in [promoted.get("transfer_winner"), promoted.get("yolo26_winner")]
        if isinstance(item, dict) and item.get("job_id")
    ]
    for job_id in promoted_job_ids:
        status = artifact_status_by_id.get(job_id)
        if not status or not status["patch_exists"] or not status["enable_physical"] or status["physical_summary_exists"]:
            continue
        source_model = str(status["source_model"] or "yolov8n")
        physical_queue_commands.append(
            [
                str(attack_python),
                str(attack_repo_root / "experiments" / "physical_benchmark.py"),
                "--patch",
                str(status["patch_path"]),
                "--artifact-name",
                str(status["artifact_name"]),
                "--model",
                source_model,
                "--output-dir",
                str(resolve_path(attack_repo_root, str(local_defaults["physical_output_dir"]))),
            ]
        )

    local_ready_script = bundle_dir / "run_local_ready.sh"
    write_shell_script(
        local_ready_script,
        local_ready_commands or [["echo", "No local-ready commands generated."]],
        cwd_comment="Commands use absolute paths and can be run from any working directory.",
    )
    physical_queue_script = bundle_dir / "run_physical_queue.sh"
    write_shell_script(
        physical_queue_script,
        physical_queue_commands or [["echo", "No physical benchmark queue generated."]],
        cwd_comment="Commands use absolute paths. These are manual-camera steps for promoted winners only.",
    )

    write_colab_handoff_assets(
        handoff_dir=handoff_dir,
        job_specs=job_specs,
        recommended_job_id=sequential_status.get("next_step", {}).get("job_id"),
    )

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
            sequential_status=sequential_status,
        ),
        encoding="utf-8",
    )

    sequential_status_path = bundle_dir / "sequential_status.json"
    sequential_status_path.write_text(json.dumps(sequential_status, indent=2), encoding="utf-8")

    colab_bundle_path = add_colab_bundle(
        attack_repo_root=attack_repo_root,
        bundle_dir=bundle_dir,
        handoff_dir=handoff_dir,
        extra_paths=[
            spec_sheet_path,
            sequential_status_path,
            resolve_path(attack_repo_root, "configs/nuc_handoff.json"),
        ],
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
        "job_statuses": job_statuses,
        "sequential_status": sequential_status,
        "configured_job_ids": sorted(item for item in configured_job_ids if item),
        "enabled_job_ids": sorted(item for item in enabled_job_ids if item),
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
    log(f"Sequential status: {sequential_status_path}")
    log(f"Colab bundle: {colab_bundle_path}")
    log(f"Manifest: {manifest_path}")
    if failures:
        for failure in failures:
            log(f"FAILED {failure.label} (exit={failure.exit_code})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
