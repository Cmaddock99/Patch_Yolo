# Defense Evaluation Report

Model: `yolov8n` | Manifest: `data/manifests/common_all_models.txt` | Images: 48

Pass criteria: attack_reduction > 0.0 pp  AND  clean_cost < 5.0 pp

### yolov8n_patch_v2

| defense | setting | suppression_undefended | suppression_defended | attack_reduction_pp | clean_cost_pp | PASS |
|---------|---------|------------------------|----------------------|--------------------|--------------:|------|
| jpeg | quality=95 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| jpeg | quality=85 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| jpeg | quality=75 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| jpeg | quality=50 | 85.0% | 80.0% | +5.0 pp | +0.0 pp | ✓ |
| blur | sigma=1.0 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| blur | sigma=2.0 | 85.0% | 100.0% | -15.0 pp | +0.0 pp | ✗ |
| blur | sigma=3.0 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=0 | 85.0% | 85.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=1 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=2 | 85.0% | 85.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=3 | 85.0% | 100.0% | -15.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=4 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=5 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=6 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=7 | 85.0% | 100.0% | -15.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=8 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=9 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=0 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=1 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=2 | 85.0% | 85.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=3 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=4 | 85.0% | 80.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.9  seed=5 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=6 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=7 | 85.0% | 100.0% | -15.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=8 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=9 | 85.0% | 85.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=0 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=1 | 85.0% | 85.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=2 | 85.0% | 75.0% | +10.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=3 | 85.0% | 80.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=4 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=5 | 85.0% | 95.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=6 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=7 | 85.0% | 85.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=8 | 85.0% | 80.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=9 | 85.0% | 90.0% | -5.0 pp | +0.0 pp | ✗ |

### yolov8n+yolo11n_joint_patch_v2

| defense | setting | suppression_undefended | suppression_defended | attack_reduction_pp | clean_cost_pp | PASS |
|---------|---------|------------------------|----------------------|--------------------|--------------:|------|
| jpeg | quality=95 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| jpeg | quality=85 | 75.0% | 85.0% | -10.0 pp | +0.0 pp | ✗ |
| jpeg | quality=75 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| jpeg | quality=50 | 75.0% | 95.0% | -20.0 pp | +0.0 pp | ✗ |
| blur | sigma=1.0 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| blur | sigma=2.0 | 75.0% | 90.0% | -15.0 pp | +0.0 pp | ✗ |
| blur | sigma=3.0 | 75.0% | 90.0% | -15.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=0 | 75.0% | 70.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.95  seed=1 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=2 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=3 | 75.0% | 85.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=4 | 75.0% | 85.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=5 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=6 | 75.0% | 65.0% | +10.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.95  seed=7 | 75.0% | 70.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.95  seed=8 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.95  seed=9 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=0 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=1 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=2 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=3 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=4 | 75.0% | 65.0% | +10.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.9  seed=5 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=6 | 75.0% | 70.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.9  seed=7 | 75.0% | 85.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.9  seed=8 | 75.0% | 55.0% | +20.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.9  seed=9 | 75.0% | 65.0% | +10.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=0 | 75.0% | 85.0% | -10.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=1 | 75.0% | 45.0% | +30.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=2 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=3 | 75.0% | 55.0% | +20.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=4 | 75.0% | 65.0% | +10.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=5 | 75.0% | 75.0% | +0.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=6 | 75.0% | 80.0% | -5.0 pp | +0.0 pp | ✗ |
| crop_resize | retain_frac=0.85  seed=7 | 75.0% | 65.0% | +10.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=8 | 75.0% | 70.0% | +5.0 pp | +0.0 pp | ✓ |
| crop_resize | retain_frac=0.85  seed=9 | 75.0% | 65.0% | +10.0 pp | +0.0 pp | ✓ |
