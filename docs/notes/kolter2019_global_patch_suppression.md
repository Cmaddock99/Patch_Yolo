# Paper Review: Kolter & Lee (2019) — On Physical Adversarial Patches for Object Detection

## Citation

- Title: *On Physical Adversarial Patches for Object Detection*
- Authors: Mark Lee, J. Zico Kolter
- Venue / Year: ICML 2019 Workshop on Security and Privacy of Machine Learning
- URL: https://arxiv.org/abs/1906.11897
- Note: Commonly cited as "Kolter 2019" or "Kolter & Madry 2019" in secondary literature — the actual authors are Lee & Kolter (Madry is not an author; this is a citation error that circulates in the field).

## Triage Summary (from PDF pages 1–5)

### Problem

Demonstrates that a single adversarial patch placed **anywhere in a scene** (not overlapping the target object) can suppress all person detections by the YOLOv3 detector. This is the "global patch" threat model: the attacker does not need to wear or attach the patch to a person; they can place it on a wall, floor, or elsewhere in the environment.

### Method Overview

- Patch type: Printed patch placed in the background of the scene; not attached to the target person
- Optimization method: Projected Gradient Descent (PGD) — standard l-infinity PGD following Madry et al. (2017) with expectation over random transformations (rotation x,y,z axes, scaling, translation, brightness)
- Loss formulation: Standard untargeted maximization — maximize the detection loss J(h_θ(A(δ, x, t)), y) over the patch δ, where A is the patch application function (masking pixels at a specific location), transformations t drawn from T, and y is the original ground truth
- Two variants: **Unclipped attack** (patches not constrained to [0,1] pixel range) and **Clipped attack** (patches properly clipped to valid image range, more realistic)
- Key insight: DPatch's formulation clips patches but does so inconsistently — the clipping in the DPatch method produces patches that are weakly adversarial; Lee & Kolter argue the patch must be clipped *after* applying the transformation function A, not before
- Evaluation metric: mAP at 0.5 IoU on full COCO validation set; also evaluated at 0.1 confidence threshold

### Detector Evaluated

- **YOLOv3** pretrained on COCO 2014 (416×416 pixels); achieves 55.4% mAP-50 (0.001 conf), 40.9% at 0.5 conf baseline

### Key Results

From Tables 1 and 2 in the PDF:

**Unclipped attack** (Table 1):
| Method | Cnt | mAP (%) |
|--------|-----|---------|
| Baseline | — | 55.4 |
| DPatch | 0.001 | 9.21 |
| **Ours** | **0.001** | **0.28** |
| DPatch | 0.5 | 34.7 |
| **Ours** | **0.5** | **13.8** |

**Clipped attack** (Table 2):
| Method | Cnt | mAP (%) |
|--------|-----|---------|
| Baseline | — | 55.4 |
| DPatch | 0.001 | 39.6 |
| **Ours** | **0.001** | **19.4** |
| DPatch | 0.5 | 26.8 |
| **Ours** | **0.5** | **7.2** |

**Physical attack** (Figure 6): Printed patch (standard printer paper + normal lighting) attacking YOLOv3 via webcam in real time successfully suppresses detections even at distances. Location-invariant: patch works from multiple positions in the scene.

**Key finding**: At confidence threshold 0.001, the clipped patch achieves 19.4% mAP (vs. 55.4% baseline) — substantially outperforming DPatch (39.6%). At 0.5 threshold: 7.2% mAP (baseline 40.9%), vs. DPatch 26.8%. A single background-placed patch suppresses all persons in the scene.

### Why DPatch is Weaker

The paper identifies DPatch's core flaw: "patches never go outside the allowable image range" — but DPatch clamps before the patch application function, so the final image contains patches that are only marginally adversarial when the patch occupies boundary pixel values. Lee & Kolter's update rule clips *after* applying the patch, producing a dramatically more effective result.

### Limitations

- YOLOv3 only — not tested on YOLOv5/v8/v11/v26
- Physical demonstration is qualitative (webcam demo) — no systematic physical quantification
- Global placement means the attacker must control some part of the physical environment (wall, floor, signage)

## Relevance to Capstone

- **YOLOv8**: Conceptual — global patch threat model contrasts with your wearable patch approach; cite for threat-model framing section. The loss formulation (standard PGD with EoT) is directly applicable and likely close to your current implementation.
- **YOLO11**: Same as v8 — not tested, but the loss design is portable.
- **YOLO26**: Low — YOLOv3 NMS-based; the global placement optimization does not account for YOLO26's Hungarian matching. However, the physical demonstration of location-invariant suppression is useful framing.
- **What to cite**: As the scene-level (global) adversarial patch threat model; as a contrast to wearable (local) patches in threat-model taxonomy; for the quantitative improvement over DPatch on YOLOv3.
- **Key number for write-up**: Global patch reduces YOLOv3 mAP from 55.4% → 7.2% (clipped, 0.5 conf) — roughly equivalent in effectiveness to your v8n wearable result (90% suppression = detection count 20→2).

## Evidence Confidence

High (PDF read; quantitative tables extracted).

## Open Questions

- Is code available? The paper mentions a demo at https://youtu.be/WXnQjb2le7Y but no GitHub code repository mentioned.
- Does this transfer to YOLOv8 without modification?
- How does performance degrade at different patch sizes (the paper tests 120×120 pixels at fixed top-left)?
