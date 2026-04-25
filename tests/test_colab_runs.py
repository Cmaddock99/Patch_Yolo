from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts import colab_queue, run_colab_patch_job


class ColabQueueHelpersTest(unittest.TestCase):
    def test_select_job_specs_preserves_requested_order(self) -> None:
        specs = [
            {"job_id": "a"},
            {"job_id": "b"},
            {"job_id": "c"},
        ]

        selected = colab_queue.select_job_specs(specs, ["c", "a"])

        self.assertEqual([item["job_id"] for item in selected], ["c", "a"])

    def test_select_job_specs_rejects_unknown_id(self) -> None:
        with self.assertRaises(ValueError):
            colab_queue.select_job_specs([{"job_id": "known"}], ["missing"])

    def test_render_colab_job_index_includes_targets(self) -> None:
        rendered = colab_queue.render_colab_job_index(
            [
                {
                    "job_id": "demo_job",
                    "description": "demo",
                    "train": {"model": "yolov8n", "run_name": "demo_job"},
                    "eval_targets": [{"model": "yolo11n"}, {"model": "yolo26n"}],
                }
            ]
        )

        self.assertIn("demo_job", rendered)
        self.assertIn("yolo11n", rendered)
        self.assertIn("yolo26n", rendered)


class ColabJobRunnerTest(unittest.TestCase):
    def test_build_train_command_can_force_resume(self) -> None:
        job_payload = {
            "job_id": "demo_job",
            "train": {
                "model": "yolov8n",
                "run_name": "demo_job",
            },
        }

        command = run_colab_patch_job.build_train_command(job_payload, force_resume=True)

        self.assertIn("--resume", command)
        self.assertIn("--model", command)
        self.assertIn("yolov8n", command)

    def test_build_eval_payload_inherits_manifest_and_output(self) -> None:
        job_payload = {
            "job_id": "demo_job",
            "train": {
                "manifest": "data/manifests/common_all_models.txt",
                "output_dir": "outputs",
            },
        }

        payload = run_colab_patch_job.build_eval_payload(
            job_payload,
            {"model": "yolo11n"},
            patch_path=Path("/tmp/patch.png"),
            index=0,
        )

        self.assertTrue(payload["eval_only"])
        self.assertEqual(payload["manifest"], "data/manifests/common_all_models.txt")
        self.assertEqual(payload["output_dir"], "outputs")
        self.assertEqual(payload["run_name"], "demo_job__transfer__yolo11n")
        self.assertEqual(payload["load_patch"], "/tmp/patch.png")


if __name__ == "__main__":
    unittest.main()
