#!/usr/bin/env python3
"""Build a Colab-first adversarial-patch job bundle from the current local repo state."""
from __future__ import annotations

import argparse
import json
import shlex
import sys
import tarfile
from pathlib import Path

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
    select_job_specs,
    should_bundle_file,
    utc_iso,
    utc_stamp,
)

DEFAULT_CONFIG = REPO_ROOT / "configs" / "colab_runs.json"


def shell_quote(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def render_quickstart(*, first_job: str, job_count: int) -> str:
    return "\n".join(
        [
            "# Colab Queue Quickstart",
            "",
            f"- Generated at: `{utc_iso()}`",
            f"- Job count in this bundle: `{job_count}`",
            "",
            "## In Colab",
            "",
            "1. Enable a GPU runtime.",
            "2. Mount Google Drive if you want checkpoint persistence and exported results.",
            "3. Upload the generated tarball to Drive or the runtime filesystem.",
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
            "## Resume A Long Job",
            "",
            "```bash",
            f"cd /content/adversarial_patch_bundle/{COLAB_BUNDLE_ROOT}",
            f"bash handoff/resume_{first_job}.sh",
            "```",
            "",
            "## Run The Whole Queue",
            "",
            "```bash",
            f"cd /content/adversarial_patch_bundle/{COLAB_BUNDLE_ROOT}",
            "bash handoff/run_all_jobs.sh",
            "```",
            "",
            "The existing notebook remains useful for ad hoc single runs. This bundle is the queue-driven path for the planned experiments.",
            "",
        ]
    )


def write_shell_script(path: Path, command: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                'ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"',
                'cd "$ROOT_DIR"',
                shell_quote(command) + ' "$@"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    path.chmod(0o755)


def add_bundle(
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
                    if should_bundle_file(child):
                        arcname = Path(COLAB_BUNDLE_ROOT) / relative / child.relative_to(source)
                        handle.add(child, arcname=str(arcname))
            elif source.is_file():
                handle.add(source, arcname=str(Path(COLAB_BUNDLE_ROOT) / relative))
        for child in handoff_dir.rglob("*"):
            if should_bundle_file(child):
                arcname = Path(COLAB_BUNDLE_ROOT) / "handoff" / child.relative_to(handoff_dir)
                handle.add(child, arcname=str(arcname))
        for extra_path in extra_paths:
            if should_bundle_file(extra_path):
                handle.add(extra_path, arcname=str(Path(COLAB_BUNDLE_ROOT) / extra_path.name))
    return tar_path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Colab job queue bundle.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to the Colab queue config.")
    parser.add_argument("--job", dest="jobs", action="append", default=[], help="Limit output to the named job id. Repeatable.")
    parser.add_argument("--list-jobs", action="store_true", help="List enabled jobs and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned output paths without creating them.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config = load_json_mapping(resolve_path(REPO_ROOT, args.config))
    attack_repo_root = resolve_path(REPO_ROOT, str(config.get("attack_repo") or "."))
    if not attack_repo_root.is_dir():
        raise FileNotFoundError(f"Attack repo root not found: {attack_repo_root}")

    job_specs = build_patch_job_specs(config, attack_repo_root)
    selected_specs = select_job_specs(job_specs, list(args.jobs))

    if args.list_jobs:
        print(render_colab_job_index(selected_specs))
        return 0

    if not selected_specs:
        raise ValueError("No enabled jobs were selected.")

    output_root = resolve_path(attack_repo_root, str(config.get("bundle_output_root") or "outputs/colab_runs"))
    bundle_prefix = str(config.get("bundle_name_prefix") or "colab_runs")
    bundle_dir = output_root / f"{bundle_prefix}_{utc_stamp()}"
    handoff_dir = bundle_dir / "handoff"
    job_specs_dir = handoff_dir / "colab_jobs"

    if args.dry_run:
        print(f"Bundle dir: {bundle_dir}")
        print(f"Selected jobs: {', '.join(str(spec['job_id']) for spec in selected_specs)}")
        print(f"Tarball: {bundle_dir / f'{COLAB_BUNDLE_ROOT}.tar.gz'}")
        return 0

    job_specs_dir.mkdir(parents=True, exist_ok=True)
    for spec in selected_specs:
        (job_specs_dir / f"{spec['job_id']}.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")

    index_path = handoff_dir / "colab_job_index.md"
    index_path.write_text(render_colab_job_index(selected_specs), encoding="utf-8")

    first_job = str(selected_specs[0]["job_id"])
    quickstart_path = handoff_dir / "COLAB_QUICKSTART.md"
    quickstart_path.write_text(
        render_quickstart(first_job=first_job, job_count=len(selected_specs)),
        encoding="utf-8",
    )

    run_all_path = handoff_dir / "run_all_jobs.sh"
    run_all_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        'ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"',
        'cd "$ROOT_DIR"',
        "",
    ]
    for spec in selected_specs:
        run_all_lines.append(f"bash handoff/run_{spec['job_id']}.sh")
    run_all_lines.append("")
    run_all_path.write_text("\n".join(run_all_lines), encoding="utf-8")
    run_all_path.chmod(0o755)

    for spec in selected_specs:
        job_id = str(spec["job_id"])
        write_shell_script(
            handoff_dir / f"run_{job_id}.sh",
            ["python", "scripts/run_colab_patch_job.py", "--job-spec", f"handoff/colab_jobs/{job_id}.json"],
        )
        write_shell_script(
            handoff_dir / f"resume_{job_id}.sh",
            ["python", "scripts/run_colab_patch_job.py", "--job-spec", f"handoff/colab_jobs/{job_id}.json", "--resume"],
        )

    manifest = {
        "generated_at_utc": utc_iso(),
        "bundle_dir": str(bundle_dir),
        "selected_jobs": [str(spec["job_id"]) for spec in selected_specs],
        "job_spec_paths": [str(path) for path in sorted(job_specs_dir.glob("*.json"))],
    }
    manifest_path = bundle_dir / "colab_bundle_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    tar_path = add_bundle(
        attack_repo_root=attack_repo_root,
        bundle_dir=bundle_dir,
        handoff_dir=handoff_dir,
        extra_paths=[manifest_path, resolve_path(attack_repo_root, "configs/colab_runs.json"), resolve_path(attack_repo_root, "scripts/build_colab_runs.py")],
    )

    print(f"Bundle directory: {bundle_dir}")
    print(f"Tarball: {tar_path}")
    print(f"Quickstart: {quickstart_path}")
    print(f"Job index: {index_path}")
    print(f"Selected jobs: {', '.join(str(spec['job_id']) for spec in selected_specs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
