from __future__ import annotations

import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts import run_colab_patch_job, run_nuc_handoff


class NucHandoffHelpersTest(unittest.TestCase):
    def test_mapping_to_cli_args_handles_bool_and_repeatable_flags(self) -> None:
        args = run_colab_patch_job.mapping_to_cli_args(
            {
                "model": "yolov8n",
                "eval_only": True,
                "co_models": ["yolo11n", "yolo26n"],
                "co_weights": [0.2, 0.3],
                "resume": False,
            }
        )

        self.assertIn("--model", args)
        self.assertIn("yolov8n", args)
        self.assertIn("--eval-only", args)
        self.assertEqual(args.count("--co-model"), 2)
        self.assertEqual(args.count("--co-weight"), 2)
        self.assertNotIn("--resume", args)

    def test_build_patch_job_specs_applies_defaults(self) -> None:
        config = {
            "attack_defaults": {
                "manifest": "data/manifests/common_all_models.txt",
                "output_dir": "outputs",
                "epochs": 1000,
            },
            "colab": {
                "checkpoint_root": "/content/drive/MyDrive/checkpoints",
                "drive_export_root": "/content/drive/MyDrive/exports",
                "jobs": [
                    {
                        "job_id": "demo_job",
                        "train": {
                            "model": "yolov8n",
                            "run_name": "demo_job",
                        },
                        "eval_targets": [{"model": "yolo11n"}],
                    }
                ],
            },
        }

        specs = run_nuc_handoff.build_patch_job_specs(config, REPO_ROOT)

        self.assertEqual(len(specs), 1)
        spec = specs[0]
        self.assertEqual(spec["job_id"], "demo_job")
        self.assertEqual(spec["train"]["manifest"], "data/manifests/common_all_models.txt")
        self.assertEqual(
            spec["train"]["checkpoint_dir"],
            "/content/drive/MyDrive/checkpoints/demo_job",
        )
        self.assertTrue(str(spec["expected_patch_path"]).endswith("outputs/demo_job/patches/patch.png"))
        self.assertEqual(spec["drive_export_root"], "/content/drive/MyDrive/exports")

    def test_build_patch_matrix_payload_keeps_modes_and_defense_params(self) -> None:
        payload = run_nuc_handoff.build_patch_matrix_payload(
            artifact_name="demo_patch",
            artifact_path=Path("/tmp/demo_patch.png"),
            ybt_output_root="outputs/patch_matrix/nuc",
            source_dir="coco/val2017_subset500/images",
            max_images=64,
            seed=42,
            defenses=["none", "oracle_patch_recover"],
            defense_params={"oracle_patch_recover": {"dilate_px": 8}},
            placement_modes=["largest_person_torso", "off_object_fixed"],
            profile="yolo11n_patch_eval_v1",
        )

        self.assertEqual(payload["profile"], "yolo11n_patch_eval_v1")
        self.assertEqual(payload["artifacts"][0]["placement_modes"], ["largest_person_torso", "off_object_fixed"])
        self.assertEqual(payload["defense_params"]["oracle_patch_recover"]["dilate_px"], 8)
        self.assertIn("runner.max_images=64", payload["overrides"])

    def test_collect_artifact_status_detects_promotion_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            patch_path = root / "outputs" / "demo_patch" / "patches" / "patch.png"
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_bytes(b"png")
            sidecar = patch_path.with_name("patch_artifact.json")
            sidecar.write_text(json.dumps({"model": "yolov8n"}), encoding="utf-8")
            (patch_path.parent.parent / "results.json").write_text(
                json.dumps({"detection_suppression_pct": 90.0}),
                encoding="utf-8",
            )

            failure_dir = root / "outputs" / "failure_grid" / "demo_patch_on_yolov8n"
            failure_dir.mkdir(parents=True, exist_ok=True)
            (failure_dir / "failure_grid_results.json").write_text("{}", encoding="utf-8")

            physical_dir = root / "outputs" / "physical_benchmark"
            physical_dir.mkdir(parents=True, exist_ok=True)
            (physical_dir / "summary_demo_patch.json").write_text("{}", encoding="utf-8")

            matrix_dir = root / "ybt" / "outputs" / "patch_matrix" / "nuc" / "patchmatrix__demo_patch__largest_person_torso__none"
            matrix_dir.mkdir(parents=True, exist_ok=True)
            (matrix_dir / "run_summary.json").write_text("{}", encoding="utf-8")

            status = run_nuc_handoff.collect_artifact_status(
                {
                    "artifact_id": "demo_patch",
                    "artifact_name": "demo_patch",
                    "patch_path": str(patch_path),
                    "source_model": "yolov8n",
                    "failure_grid_models": ["yolov8n"],
                    "enable_patch_matrix": True,
                    "enable_physical": True,
                    "from_job": False,
                },
                attack_repo_root=root,
                ybt_repo_root=root / "ybt",
                local_defaults={
                    "failure_grid_output_dir": "outputs/failure_grid",
                    "physical_output_dir": "outputs/physical_benchmark",
                    "ybt_output_root": "outputs/patch_matrix/nuc",
                    "ybt_placement_modes": ["largest_person_torso"],
                    "ybt_defenses": ["none"],
                },
            )

            self.assertTrue(status["patch_exists"])
            self.assertTrue(status["results_exists"])
            self.assertTrue(status["sidecar_exists"])
            self.assertTrue(status["failure_reports_complete"])
            self.assertTrue(status["patch_matrix_complete"])
            self.assertTrue(status["digital_gate_ready"])
            self.assertTrue(status["physical_summary_exists"])
            self.assertTrue(status["promotion_gate_ready"])

    def test_collect_artifact_status_requires_patch_matrix_for_digital_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ybt_root = root / "ybt"
            patch_path = root / "outputs" / "demo_patch" / "patches" / "patch.png"
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_bytes(b"png")
            patch_path.with_name("patch_artifact.json").write_text(json.dumps({"model": "yolov8n"}), encoding="utf-8")
            (patch_path.parent.parent / "results.json").write_text(json.dumps({"detection_suppression_pct": 50.0}), encoding="utf-8")

            failure_dir = root / "outputs" / "failure_grid" / "demo_patch_on_yolov8n"
            failure_dir.mkdir(parents=True, exist_ok=True)
            (failure_dir / "failure_grid_results.json").write_text("{}", encoding="utf-8")

            status = run_nuc_handoff.collect_artifact_status(
                {
                    "artifact_id": "demo_patch",
                    "artifact_name": "demo_patch",
                    "patch_path": str(patch_path),
                    "source_model": "yolov8n",
                    "failure_grid_models": ["yolov8n"],
                    "enable_patch_matrix": True,
                    "enable_physical": True,
                    "from_job": True,
                },
                attack_repo_root=root,
                ybt_repo_root=ybt_root,
                local_defaults={
                    "failure_grid_output_dir": "outputs/failure_grid",
                    "physical_output_dir": "outputs/physical_benchmark",
                    "ybt_output_root": "outputs/patch_matrix/nuc",
                    "ybt_placement_modes": ["largest_person_torso"],
                    "ybt_defenses": ["none"],
                },
            )

            self.assertFalse(status["patch_matrix_complete"])
            self.assertFalse(status["digital_gate_ready"])
            self.assertFalse(status["promotion_gate_ready"])

    def test_build_sequential_status_selects_next_job_and_winners(self) -> None:
        config = {
            "sequential_plan": {
                "queue_order": [
                    "v8m_source_transfer_v1",
                    "v8n_transfer_baseline_v1",
                    "v8n_transfer_cutout_only_v1",
                    "v8n_transfer_self_ensemble_only_v1",
                    "v8n_transfer_cutout_self_ensemble_v1",
                    "yolo26n_hybrid_loss_v1",
                    "yolo26n_hybrid_loss_tps_v1",
                ],
                "baselines": {
                    "v8_transfer": {
                        "yolo11n": 33.3,
                        "yolo26n": 14.0,
                    }
                },
                "gates": {
                    "gate_a": {
                        "job_id": "v8m_source_transfer_v1",
                        "deltas": {
                            "yolo11n": 5.0,
                            "yolo26n": 3.0,
                        },
                    },
                    "gate_b": {
                        "job_ids": [
                            "v8n_transfer_baseline_v1",
                            "v8n_transfer_cutout_only_v1",
                            "v8n_transfer_self_ensemble_only_v1",
                            "v8n_transfer_cutout_self_ensemble_v1",
                        ],
                        "deltas": {
                            "yolo11n": 5.0,
                            "yolo26n": 3.0,
                        },
                    },
                    "gate_c": {
                        "job_id": "yolo26n_hybrid_loss_v1",
                        "follow_on_job_id": "yolo26n_hybrid_loss_tps_v1",
                        "min_direct_suppression": 25.0,
                    },
                },
            }
        }
        job_statuses = [
            {
                "job_id": "v8m_source_transfer_v1",
                "artifact_name": "v8m_source_transfer_v1",
                "transfer_metrics": {"yolo11n": 40.0, "yolo26n": 18.0},
                "train_suppression_pct": 91.0,
                "colab_return_complete": True,
                "digital_gate_ready": True,
                "sidecar_exists": True,
                "train_results_exists": True,
                "failure_reports_complete": True,
                "patch_matrix_complete": True,
                "physical_summary_exists": False,
            },
            {
                "job_id": "v8n_transfer_baseline_v1",
                "artifact_name": "v8n_transfer_baseline_v1",
                "transfer_metrics": {"yolo11n": 33.3, "yolo26n": 14.0},
                "train_suppression_pct": 90.0,
                "colab_return_complete": True,
                "digital_gate_ready": True,
                "sidecar_exists": True,
                "train_results_exists": True,
                "failure_reports_complete": True,
                "patch_matrix_complete": True,
                "physical_summary_exists": False,
            },
            {
                "job_id": "v8n_transfer_cutout_only_v1",
                "artifact_name": "v8n_transfer_cutout_only_v1",
                "transfer_metrics": {"yolo11n": 35.0, "yolo26n": 14.5},
                "train_suppression_pct": 89.0,
                "colab_return_complete": True,
                "digital_gate_ready": True,
                "sidecar_exists": True,
                "train_results_exists": True,
                "failure_reports_complete": True,
                "patch_matrix_complete": True,
                "physical_summary_exists": False,
            },
            {
                "job_id": "v8n_transfer_self_ensemble_only_v1",
                "artifact_name": "v8n_transfer_self_ensemble_only_v1",
                "transfer_metrics": {"yolo11n": 39.0, "yolo26n": 17.5},
                "train_suppression_pct": 88.0,
                "colab_return_complete": True,
                "digital_gate_ready": True,
                "sidecar_exists": True,
                "train_results_exists": True,
                "failure_reports_complete": True,
                "patch_matrix_complete": True,
                "physical_summary_exists": False,
            },
            {
                "job_id": "v8n_transfer_cutout_self_ensemble_v1",
                "artifact_name": "v8n_transfer_cutout_self_ensemble_v1",
                "transfer_metrics": {"yolo11n": 36.0, "yolo26n": 16.0},
                "train_suppression_pct": 87.0,
                "colab_return_complete": True,
                "digital_gate_ready": True,
                "sidecar_exists": True,
                "train_results_exists": True,
                "failure_reports_complete": True,
                "patch_matrix_complete": True,
                "physical_summary_exists": False,
            },
            {
                "job_id": "yolo26n_hybrid_loss_v1",
                "artifact_name": "yolo26n_hybrid_loss_v1",
                "transfer_metrics": {"yolo11n": 28.0},
                "train_suppression_pct": 27.0,
                "colab_return_complete": True,
                "digital_gate_ready": True,
                "sidecar_exists": True,
                "train_results_exists": True,
                "failure_reports_complete": True,
                "patch_matrix_complete": True,
                "physical_summary_exists": False,
            },
        ]

        status = run_nuc_handoff.build_sequential_status(
            config=config,
            job_statuses=job_statuses,
            enabled_job_ids={
                "v8m_source_transfer_v1",
                "v8n_transfer_baseline_v1",
                "v8n_transfer_cutout_only_v1",
                "v8n_transfer_self_ensemble_only_v1",
                "v8n_transfer_cutout_self_ensemble_v1",
                "yolo26n_hybrid_loss_v1",
            },
        )

        self.assertEqual(status["gate_statuses"]["gate_a"]["state"], "pass")
        self.assertEqual(status["gate_statuses"]["gate_b"]["state"], "pass")
        self.assertEqual(status["gate_statuses"]["gate_b"]["winner_job_id"], "v8n_transfer_self_ensemble_only_v1")
        self.assertEqual(status["gate_statuses"]["gate_c"]["state"], "ready_to_enable_follow_on")
        self.assertEqual(status["promoted_artifacts"]["transfer_winner"]["job_id"], "v8m_source_transfer_v1")
        self.assertEqual(status["promoted_artifacts"]["yolo26_winner"]["job_id"], "yolo26n_hybrid_loss_v1")
        self.assertEqual(status["next_step"]["kind"], "config_edit")

    def test_main_refreshes_manifest_after_local_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            attack_root = root / "attack"
            ybt_root = root / "ybt"
            (attack_root / ".venv" / "bin").mkdir(parents=True, exist_ok=True)
            (ybt_root / ".venv" / "bin").mkdir(parents=True, exist_ok=True)
            (attack_root / ".venv" / "bin" / "python").write_text("", encoding="utf-8")
            (ybt_root / ".venv" / "bin" / "python").write_text("", encoding="utf-8")

            patch_path = attack_root / "outputs" / "demo_patch" / "patches" / "patch.png"
            patch_path.parent.mkdir(parents=True, exist_ok=True)
            patch_path.write_bytes(b"png")
            patch_path.with_name("patch_artifact.json").write_text(
                json.dumps({"model": "yolov8n"}),
                encoding="utf-8",
            )
            (patch_path.parent.parent / "results.json").write_text(
                json.dumps({"detection_suppression_pct": 50.0}),
                encoding="utf-8",
            )
            failure_dir = attack_root / "outputs" / "failure_grid" / "demo_patch_on_yolov8n"
            failure_dir.mkdir(parents=True, exist_ok=True)
            (failure_dir / "failure_grid_results.json").write_text("{}", encoding="utf-8")

            config_path = root / "nuc_handoff_test.json"
            config_path.write_text(
                json.dumps(
                    {
                        "repo_roots": {
                            "attack_repo": str(attack_root),
                            "ybt_repo": str(ybt_root),
                        },
                        "local_defaults": {
                            "failure_grid_output_dir": "outputs/failure_grid",
                            "failure_grid_manifest": "data/manifests/common_all_models.txt",
                            "physical_output_dir": "outputs/physical_benchmark",
                            "run_failure_grid": True,
                            "run_patch_matrix": True,
                            "ybt_output_root": "outputs/patch_matrix/nuc",
                            "ybt_source_dir": "coco/val2017_subset500/images",
                            "ybt_max_images": 64,
                            "ybt_seed": 42,
                            "ybt_defenses": ["none"],
                            "ybt_defense_params": {},
                            "ybt_placement_modes": ["largest_person_torso"],
                            "ybt_profile": "yolo11n_patch_eval_v1",
                        },
                        "colab": {
                            "bundle_output_root": "outputs/nuc_handoff",
                            "jobs": [],
                        },
                        "sequential_plan": {
                            "gates": {
                                "gate_b": {
                                    "job_ids": ["demo_job"],
                                }
                            }
                        },
                        "existing_artifacts": [
                            {
                                "artifact_id": "demo_patch",
                                "patch_path": str(patch_path),
                                "source_model": "yolov8n",
                                "failure_grid_models": ["yolov8n"],
                                "enable_patch_matrix": True,
                                "enable_physical": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            def fake_run_command(*, label: str, cwd: Path, command: list[str], dry_run: bool) -> run_nuc_handoff.CommandResult:
                if label == "local-ready:run_unified.py":
                    matrix_index = command.index("--matrix-config")
                    matrix_payload = json.loads(Path(command[matrix_index + 1]).read_text(encoding="utf-8"))
                    artifact_name = matrix_payload["artifacts"][0]["name"]
                    placement_mode = matrix_payload["artifacts"][0]["placement_modes"][0]
                    defense_name = matrix_payload["defenses"][0]
                    run_dir = (
                        ybt_root
                        / "outputs"
                        / "patch_matrix"
                        / "nuc"
                        / f"patchmatrix__{artifact_name}__{placement_mode}__{defense_name}"
                    )
                    run_dir.mkdir(parents=True, exist_ok=True)
                    (run_dir / "run_summary.json").write_text("{}", encoding="utf-8")
                return run_nuc_handoff.CommandResult(label=label, cwd=cwd, command=command, exit_code=0)

            def fake_add_colab_bundle(*, attack_repo_root: Path, bundle_dir: Path, handoff_dir: Path, extra_paths: list[Path]) -> Path:
                tar_path = bundle_dir / f"{run_nuc_handoff.COLAB_BUNDLE_ROOT}.tar.gz"
                tar_path.write_bytes(b"bundle")
                return tar_path

            with mock.patch.object(run_nuc_handoff, "run_command", side_effect=fake_run_command), mock.patch.object(
                run_nuc_handoff, "add_colab_bundle", side_effect=fake_add_colab_bundle
            ):
                exit_code = run_nuc_handoff.main(
                    [
                        "--config",
                        str(config_path),
                        "--skip-preflight",
                        "--run-local-ready",
                    ]
                )

            self.assertEqual(exit_code, 0)
            manifest_path = next((attack_root / "outputs" / "nuc_handoff").glob("*/handoff_manifest.json"))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            artifact_status = manifest["artifact_statuses"][0]
            self.assertTrue(artifact_status["patch_matrix_complete"])
            self.assertTrue(artifact_status["failure_reports_complete"])
            self.assertTrue(
                any(
                    row["label"] == "local-ready:run_unified.py" and row["exit_code"] == 0
                    for row in manifest["command_results"]
                )
            )


if __name__ == "__main__":
    unittest.main()
