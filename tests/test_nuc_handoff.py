from __future__ import annotations

import json
import sys
import tempfile
import unittest
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

            failure_dir = root / "outputs" / "failure_grid" / "demo_patch_on_yolov8n"
            failure_dir.mkdir(parents=True, exist_ok=True)
            (failure_dir / "failure_grid_results.json").write_text("{}", encoding="utf-8")

            physical_dir = root / "outputs" / "physical_benchmark"
            physical_dir.mkdir(parents=True, exist_ok=True)
            (physical_dir / "summary_demo_patch.json").write_text("{}", encoding="utf-8")

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
                local_defaults={
                    "failure_grid_output_dir": "outputs/failure_grid",
                    "physical_output_dir": "outputs/physical_benchmark",
                },
            )

            self.assertTrue(status["patch_exists"])
            self.assertTrue(status["sidecar_exists"])
            self.assertTrue(status["failure_reports_complete"])
            self.assertTrue(status["physical_summary_exists"])
            self.assertTrue(status["promotion_gate_ready"])


if __name__ == "__main__":
    unittest.main()
