# Paper Review: Zolfi et al. (2021) — The Translucent Patch

## Citation

- Title: The Translucent Patch: A Physical and Universal Attack on Object Detectors
- Authors: Alon Zolfi, Moshe Kravchik, Yuval Elovici, Asaf Shabtai
- Venue / Year: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021, pp. 15232–15241; arXiv:2012.12528
- URL: https://openaccess.thecvf.com/content/CVPR2021/html/Zolfi_The_Translucent_Patch_A_Physical_and_Universal_Attack_on_Object_CVPR_2021_paper.html
- PDF: ../papers/zolfi2021_translucent_patch_2012.12528.pdf

## Problem

- What threat model is assumed? White-box (YOLOv5 gradients used for optimization); physically realizable (transparent paper printed and affixed to camera lens). No direct contact with the target object required.
- What detector or classifier is attacked? YOLOv5 (white-box); YOLOv2 and Faster R-CNN (black-box transfer).
- What is the attack goal? Hide all instances of a specific class (stop signs) from detection while preserving detection of all other classes. A single lens patch works across many scenes simultaneously — truly universal and contactless.

## Method

- Patch type: Semi-transparent printed patch placed on the camera lens. Physically: printed on transparent paper, affixed to a Logitech C930 webcam. Digitally modeled using alpha blending: `perturbed(i,j) = original(i,j)·(1-α(i,j)) + γ(i,j)·α(i,j)`.
- Patch parameterization: n blurry oval shapes, each defined by:
  - Center (xc, yc) ∈ [-1,1], radius r ∈ [rmin, rmax], shear (shx, shy) ∈ [-1,1], RGB color γ, opacity α ∈ [0,1].
  - Opacity formula: `α(i,j) = amax · (-s·d(i,j)^β + 1)` — smooth falloff from center.
  - Parameters used: s=0.9, β=2.5, rmax=0.25, rmin=0.03, patch size: 0.6×0.33 inches on lens.
- Optimization method: Gradient descent on shape parameters (position, color, opacity).
- Loss terms (four components, weights from grid search: w1=0.74, w2=0.15, w3=0.1, w4=0.01):
  - **ℓtarget_conf** (w=0.74): Minimize `Pr(objectness)·Pr(target class)` — suppresses stop sign detection.
  - **ℓIoU** (w=0.15): Minimize `IoU(predicted bbox, ground truth)` — degrades localization accuracy.
  - **ℓuntargeted_conf** (w=0.1): `(1/M)·Σ|conf(cls, clean) - conf(cls, patch)|` — preserves other class detections.
  - **ℓnps** (w=0.01): Non-printability score — constrains colors to printer-reproducible palette.
- Transformations / EoT details: Implicit robustness from operating at the lens level (single patch affects all images uniformly).
- Physical-world considerations: Printed on transparent paper (Xerox 6605DN laser printer). Tested against a 21-inch projector screen showing driving videos. Digital simulation closely matched physical results.

## Experimental Setup

- Dataset: Combined ~1,750 stop sign images from LISA (~500), Mapillary MTSD (~750), Berkeley BDD (~500). Train/val: 90/10 from BDD+MTSD; test: LISA only.
- Target classes: Stop sign (suppressed); person, bicycle, car, bus, truck, traffic light, fire hydrant (preserved)
- Model versions: YOLOv5 (white-box); YOLOv2, Faster R-CNN (black-box)
- Metrics: Average Precision (AP), Fooling Rate = #fooled_objects / #total_objects. Confidence threshold: 0.4.

## Results

**Digital (white-box, YOLOv5):**
- Stop sign AP: 95.17% (clean) → 52.7% (patched) — **42.47% reduction**
- Other classes AP: 100% (clean) → 82.69% (patched) — minimal collateral damage

**Opacity sensitivity (αmax):**
| αmax | Stop Sign AP | Other Classes AP |
|---|---|---|
| 0.1 | 93.85% | 98.26% |
| 0.3 | 70.13% | 88.25% |
| 0.5 | 51.75% | 81.93% |
| 0.9 | 36.55% | 70.45% |

**Shape count sensitivity:**
| Shapes | Stop Sign AP | Other Classes AP |
|---|---|---|
| 3 | 91.15% | 95.44% |
| 5 | 77.45% | 91.72% |
| 7 | 65.01% | 83.23% |
| 10 | 53.11% | 77.65% |

**Black-box transfer (patch trained on YOLOv5):**
| Model | Stop Sign (clean→patch) | Others (clean→patch) |
|---|---|---|
| YOLOv2 | 81.54% → 57.36% | 59.13% → 54.92% |
| Faster R-CNN | 94.31% → 54.53% | 78.31% → 70.36% |

**Physical attack:**
- Optimized patch: 42.27% stop sign fooling rate (vs. 20.57% random) — **near-identical to digital result (42.47%)**.
- Other classes: 21.54% affected (acceptable collateral, close to random patch's 19.27%).
- Colored patches (red/cyan) fooled 93–99% of stop signs but also destroyed other-class detection — the optimized patch is uniquely class-specific.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate. The class-selective suppression approach (suppress one class, preserve others) is a more sophisticated attack goal than pure suppression. The ℓuntargeted_conf loss term is a useful design pattern if my capstone extends to targeted suppression.
- Direct relevance to YOLO11: Same.
- Direct relevance to YOLO26: Same — YOLO26's NMS-free detection might respond differently to IoU-based loss components.
- What I can reproduce: The multi-component loss design (especially ℓuntargeted_conf) can be incorporated into a custom training loop.
- What I can cite: For the lens-patch concept; for the digital-to-physical near-perfect match result; for the class-selective loss formulation; for the opacity/shape sensitivity analysis.

## Open Questions

- Does this transfer across YOLO versions? Transfers to YOLOv2 and Faster R-CNN in black-box mode. Performance on YOLOv8/v11/v26 untested.
- Is the patch digital only, or physically tested? Both — physical test matches digital result closely.
- Is the code available? Not released per the executive summary; arXiv preprint available.
- What is missing for my project? Stop-sign focused (not person class); requires a physical camera to deploy as intended; YOLOv8/v11/v26 not tested.
