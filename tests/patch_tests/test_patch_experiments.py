from __future__ import annotations

import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
import unittest

import torch

from experiments.failure_grid import summarize_failure_grid_rows
from experiments.physical_benchmark import summarize_sector_rows
from experiments.ultralytics_patch import (
    PLACEMENT_OFF_OBJECT_FIXED,
    compute_patch_placement,
    detection_loss,
    predict_with_grad,
    save_patch_outputs,
)


class PatchExperimentHelpersTest(unittest.TestCase):
    def test_predict_with_grad_handles_train_mode_score_dict(self) -> None:
        class DictScoreModel(torch.nn.Module):
            def forward(self, image_bchw: torch.Tensor) -> dict[str, object]:
                batch = image_bchw.shape[0]
                anchor_logits = image_bchw[:, :1, 0, 0].view(batch, 1, 1).expand(batch, 80, 5)
                return {
                    "boxes": torch.zeros(batch, 64, 5, device=image_bchw.device),
                    "scores": anchor_logits,
                    "feats": [],
                }

        image = torch.ones((1, 3, 8, 8), dtype=torch.float32, requires_grad=True)
        scores = predict_with_grad(DictScoreModel(), image, model_name="yolov8m")

        self.assertEqual(tuple(scores.shape), (1, 80, 5))
        self.assertTrue(scores.requires_grad)

    def test_detection_loss_uses_person_channel_zero_for_score_only_tensor(self) -> None:
        preds = torch.zeros((1, 80, 3), dtype=torch.float32)
        preds[:, 0, :] = 0.0
        preds[:, 4, :] = 10.0

        loss = detection_loss(preds, topk=3, is_v26=False)

        self.assertAlmostEqual(loss.item(), 0.5, places=5)

    def test_compute_patch_placement_supports_off_object_fixed(self) -> None:
        top, left = compute_patch_placement(
            [],
            320,
            20,
            placement_regime=PLACEMENT_OFF_OBJECT_FIXED,
            image_width=320,
            patch_width=20,
        )

        self.assertEqual(top, 16)
        self.assertEqual(left, 16)

    def test_save_patch_outputs_writes_patch_artifact_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "outputs" / "demo_run"
            patch_tensor = torch.full((3, 8, 8), 0.5, dtype=torch.float32)
            summary = {
                "run_name": "demo_run",
                "model": "yolov8n",
                "joint_models": ["yolov8n"],
                "joint_weights": [1.0],
                "manifest_path": "data/manifests/common_all_models.txt",
                "training_images": 18,
                "patch_size": 8,
                "detection_suppression_pct": 90.0,
                "loss_source": "channel4",
            }
            args = SimpleNamespace(
                placement_regime="largest_person_torso",
                block_erase_prob=0.5,
                cutout_prob=0.3,
                cutout_size=20,
                self_ensemble_mode="shakedrop",
                self_ensemble_prob=0.3,
                rot_max=15.0,
                cloth_eot="tps",
                nps_weight=0.01,
            )

            patch_png, sidecar = save_patch_outputs(
                run_dir=run_dir,
                patch_tensor=patch_tensor,
                summary=summary,
                args=args,
                repo_commit="deadbeef",
            )

            self.assertTrue(patch_png.is_file())
            self.assertTrue(sidecar.is_file())
            payload = json.loads(sidecar.read_text(encoding="utf-8"))
            self.assertEqual(payload["run_name"], "demo_run")
            self.assertEqual(payload["placement_regime"], "largest_person_torso")
            self.assertEqual(payload["self_ensemble_mode"], "shakedrop")
            self.assertEqual(payload["cloth_eot"], "tps")
            self.assertEqual(payload["repo_commit"], "deadbeef")
            self.assertTrue(payload["artifact_sha256"])

    def test_failure_grid_summary_tracks_best_and_worst_cells(self) -> None:
        summary = summarize_failure_grid_rows(
            {
                "brightness": [
                    {"axis": "brightness", "value": 0.6, "detection_suppression_pct": 60.0},
                    {"axis": "brightness", "value": 1.0, "detection_suppression_pct": 80.0},
                ],
                "rotation_degrees": [
                    {"axis": "rotation_degrees", "value": 0, "detection_suppression_pct": 90.0},
                    {"axis": "rotation_degrees", "value": 30, "detection_suppression_pct": 50.0},
                ],
            }
        )

        self.assertEqual(summary["best_cell"]["axis"], "rotation_degrees")
        self.assertEqual(summary["best_cell"]["value"], 0)
        self.assertEqual(summary["worst_cell"]["axis"], "rotation_degrees")
        self.assertEqual(summary["worst_cell"]["value"], 30)

    def test_physical_sector_summary_tracks_best_and_worst_sectors(self) -> None:
        rows = [
            {"distance_m": 0.5, "yaw_deg": 0, "lighting": "bright_300lux", "suppression_vs_clean": 90.0},
            {"distance_m": 0.5, "yaw_deg": 15, "lighting": "dim_45lux", "suppression_vs_clean": 88.0},
            {"distance_m": 2.0, "yaw_deg": 0, "lighting": "bright_300lux", "suppression_vs_clean": 20.0},
            {"distance_m": 2.0, "yaw_deg": 15, "lighting": "dim_45lux", "suppression_vs_clean": 22.0},
        ]

        summary = summarize_sector_rows(rows)

        self.assertEqual(summary["best_sector"]["axis"], "distance")
        self.assertEqual(summary["best_sector"]["value"], "0.5")
        self.assertEqual(summary["worst_sector"]["axis"], "distance")
        self.assertEqual(summary["worst_sector"]["value"], "2.0")


if __name__ == "__main__":
    unittest.main()
