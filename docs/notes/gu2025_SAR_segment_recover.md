# Gu and Jafarnejadsani (2025) - SAR Segment-and-Recover Defense

## Citation

- Title: *Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks*
- Authors: Haotian Gu, Hamidreza Jafarnejadsani
- Venue / Year: Journal of Imaging 2025
- DOI: 10.3390/jimaging11090316
- URL: https://doi.org/10.3390/jimaging11090316
- PDF: `docs/papers/gu2025_SAR_segment_recover_jimaging316.pdf`
- Code: https://github.com/robotics-star/SAR

## Problem

- What threat model is assumed? Patch-hiding attacks against object detectors where the adversarial patch is localized, visible, and can vary in scale, shape, and position (pp. 1-2, 9).
- What detector family is studied? DETR, YOLOv11, and Faster R-CNN as defended base detectors (pp. 2, 9-10).
- What is the defense goal? Patch-agnostic preprocessing that localizes the patch and restores the corrupted pixels without retraining the detector (pp. 1-2, 5).

## Method

- Core idea: SAR is a "detect-and-inpaint" defense that first localizes the patch region, then restores the damaged pixels before sending the image to the base detector (pp. 5-6).
- Frontend:
  - FastSAM provides zero-shot segmentation proposals.
  - A JPEG/DCT-based adversary predictor identifies high-frequency suspicious regions and prompts the segmentation step to isolate the patch mask (pp. 5-7).
- Backend:
  - The detected patch region is repaired with large-mask inpainting rather than simply blacking out the region.
  - The paper argues this avoids the object loss introduced by older "detect-and-remove" defenses such as PAD and PatchZero (pp. 5, 13).
- Design intent: patch-agnostic defense against diverse visible patch types rather than a defense trained on one patch family (pp. 1-2, 9).

## Experimental Setup

- Base detectors: DETR, YOLOv11, Faster R-CNN, all pretrained on MS COCO (pp. 9-10).
- Attacks:
  - EAVISE printable patches with `OBJ-CLS`, `OBJ`, and `CLS` objectives
  - DPatch localized-noise patches at `40 x 40`, `75 x 75`, and `100 x 100`
  - Ad-YOLO adaptive patches covering `20%`, `30%`, and `40%` of the target bounding box (p. 9).
- Data:
  - 400 patch-attacked images created from VisDrone
  - clean AP / PR evaluation on PASCAL VOC (pp. 9-10).
- Baselines: LGS, Jedi, RLID, Jujutsu (p. 9).
- Metrics:
  - FAR for false cautions
  - patch localization recall (PLR)
  - certified recall at `0.5` (`CR@0.5`) for robust detection under patch attacks (p. 9).

## Results

### Table 3 - Clean compatibility and hostile-patch certified recall (p. 10)

- SAR preserves clean performance well:
  - DETR clean `0.70` with `FAR = 0.002`
  - YOLOv11 clean `0.74` with `FAR = 0.003`
  - Faster R-CNN clean `0.65` with `FAR = 0.006`
- Printable patch robustness:
  - DETR `OBJ-CLS / OBJ / CLS = 0.82 / 0.86 / 0.70`
  - YOLOv11 `0.75 / 0.66 / 0.61`
  - Faster R-CNN `0.65 / 0.69 / 0.75`
- Localized-noise robustness:
  - YOLOv11 improves from undefended `0.35 / 0.51 / 0.49` to `0.55 / 0.71 / 0.74`
  - Faster R-CNN improves from `0.30 / 0.53 / 0.36` to `0.71 / 0.62 / 0.55`
- Adaptive-patch robustness:
  - YOLOv11 reaches `0.72 / 0.76 / 0.70`
  - Faster R-CNN reaches `0.82 / 0.86 / 0.88`
  - DETR reaches `0.66 / 0.62 / 0.75`

### Table 4 - Patch localization recall (p. 11)

- SAR gives the strongest localization frontend among compared preprocessing defenses:
  - LaVAN: `87.2`
  - DPatch: `91.47`
  - EAVISE: `74.20`
  - Ad-YOLO patch: `93.29`

### Table 5 - Runtime (p. 13)

- The paper reports that SAR adds roughly a `2x` slowdown compared to the undefended detector while remaining lightweight enough for the authors' tracking pipeline.
- Reported per-example SAR times are approximately `55-57 ms` in the YOLOv11 runtime table.

## Key Claims

1. **SAR is patch-agnostic and handles printable, localized-noise, and adaptive patches across multiple detector families.** Supported by Table 3 and the attack setup in Section 5.2 (pp. 9-12).
2. **Inpainting is materially better than simple black masking when the patch overlaps the object.** Supported by the Figure 4 / Table 1 discussion and the backend ablation summary (p. 13).
3. **The defense is especially strong as a localization frontend.** Supported by Table 4 (p. 11).
4. **The method is detector-compatible, including with YOLOv11 and DETR.** Supported by the clean rows and PR discussion around Table 3 (p. 10).

## Threat Model

- Attack type: localized and visible patch-hiding attacks.
- Patch placement: can appear anywhere on the object, including salient object regions (p. 12).
- Defender position: image-preprocessing stage before the detector.
- Training assumption: no detector retraining is required; the method is designed as a patch-agnostic preprocessing defense (pp. 1-2, 5).

## Limitations and Failure Modes

- The defense is explicitly aimed at localized and visible patches; the paper says translucent patches can bypass the method in its current form (pp. 13-14).
- The results are defense-side only; the paper does not evaluate YOLOv8 or YOLO26 (pp. 9-10).
- SAR still adds noticeable latency, with the paper describing an approximately `2x` slowdown versus the undefended detector (p. 13).
- My inference: because the frontend depends on frequency and visibility cues, naturalistic or low-contrast patches may be a harder case than the benchmarked visible patches.

## Defensive Takeaways

- This is one of the strongest repo-local patch-agnostic detector-side defenses now available.
- The most reusable design idea is the split between localization and restoration: detect the patch mask first, then repair pixels instead of zeroing them.
- SAR is especially useful in this repo because it brings direct YOLOv11 defense evidence into the local corpus.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: Indirect. The paper does not test YOLOv8 directly, but the preprocessing design should transfer conceptually.
- **YOLO11**: Direct defense relevance. YOLOv11 is one of the paper's defended base detectors, and SAR reaches strong `CR@0.5` values under multiple patch families (p. 10).
- **YOLO26**: Indirect only. DETR results are useful architecture context, but YOLO26 itself is not tested.
- Capstone relevance: `4/5`. Strong defense baseline with direct YOLO11-side evidence.

## Reproducibility Signals

- Local PDF includes algorithm pseudocode, attack setup, detector list, and runtime discussion.
- Code URL is provided in the paper (p. 16).
- The defense is presented as detector-agnostic preprocessing rather than a fragile model-specific retraining recipe.

## Open Questions

- How well does SAR handle naturalistic diffusion-era patches such as AdvLogo?
- Would SAR retain its gains on modern Ultralytics YOLOv8 heads?
- Does the JPEG/FastSAM frontend degrade if the patch is low-contrast rather than visibly high-frequency?
- How much of the gain comes from the localization frontend versus the inpainting backend?

## Normalized Extraction

- Canonical slug: `gu2025_SAR`
- Canonical source record: `docs/papers/gu2025_SAR_segment_recover_jimaging316.pdf`
- Evidence state: `page_cited`
- Threat model: patch-agnostic defense against localized and visible patch-hiding attacks.
- Detector family and exact version: DETR, YOLOv11, Faster R-CNN.
- Attack or defense goal: localize adversarial patches, restore corrupted pixels, and preserve detection.
- Loss or objective: JPEG/DCT-frequency-guided patch prompting plus FastSAM localization and inpainting-based restoration.
- Transforms / EoT: evaluated against printable, localized-noise, and adaptive patches of varying scales.
- Dataset: VisDrone patch-attacked subset, PASCAL VOC clean evaluation.
- Metrics: `CR@0.5`, FAR, PLR, AP / PR.
- Strongest quantitative result: Faster R-CNN with SAR reaches `0.82 / 0.86 / 0.88` certified recall under `20% / 30% / 40%` adaptive patch coverage, versus undefended `0.53 / 0.57 / 0.61` (Table 3, p. 10).
- Transfer findings: evaluated across one-stage, two-stage, and transformer detectors as defended backends.
- Physical findings: printable EAVISE patches are included directly in the benchmark (pp. 9-10).
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: direct for YOLO11 defense-side evidence; indirect otherwise.
- Reproducible technique to borrow: patch localization plus restoration is stronger than simple detect-and-remove masking.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `defense_baseline`
