# Ilina, Tereshonok, and Ziyadinov (2025) - Anomaly Localization Defense

## Citation

- Title: *Increasing Neural-Based Pedestrian Detectors' Robustness to Adversarial Patch Attacks Using Anomaly Localization*
- Authors: Olga Ilina, Maxim Tereshonok, Vadim Ziyadinov
- Venue / Year: Journal of Imaging 2025
- DOI: 10.3390/jimaging11010026
- URL: https://doi.org/10.3390/jimaging11010026
- PDF: `docs/papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf`

## Problem

- What threat model is assumed? Printed adversarial patches that hide pedestrians from a YOLO-based detector in the physical world (pp. 1-2).
- What detector family is studied? YOLOv3 pedestrian detection (pp. 1, 12).
- What is the defense goal? Restore robust pedestrian detection by reconstructing the benign image structure and localizing anomalous patch regions without needing prior patch templates (pp. 1-2, 12).

## Method

- Core idea: the method reconstructs a clean-looking image with an unsupervised DCNN, computes an error map between the input and reconstruction, then localizes anomalous fragments and suppresses them before detection (pp. 1, 4-10).
- Main components:
  - a fully convolutional DCNN trained only on clean person images to reconstruct benign inputs (pp. 6-7)
  - histogram-based fragment analysis over the reconstruction-error map (pp. 7-8)
  - Isolation Forest to mark anomalous fragments (pp. 8-9)
  - DBSCAN clustering plus histogram correlation checks to refine anomaly regions (pp. 9-10).
- Final defense step: the anomaly map is applied to the source image to hide the anomalous area and reduce its effect on the detector (p. 10).

## Experimental Setup

- Detector: YOLOv3 pretrained on MS COCO 2017 (p. 12).
- Clean reconstruction training data: `64,115` images from the `MS COCO Person` subset (p. 12).
- Evaluation data: INRIA Person test split with `288` images and `597` pedestrian instances (p. 12).
- Compared defenses: SAC and PAD (p. 12).
- Metrics:
  - clean and adversarial `mAP`
  - attack success rate (`ASR`) (p. 12).

## Results

### Table 1 - Defense comparison on INRIA Person (p. 12)

- Undefended YOLOv3:
  - clean `93.35`
  - adversarial `46.79`
  - `ASR = 19.42`
- SAC:
  - clean `93.35`
  - adversarial `53.72`
  - `ASR = 10.61`
- PAD:
  - clean `92.73`
  - adversarial `76.94`
  - `ASR = 11.76`
- Proposed method:
  - clean `93.55`
  - adversarial `80.97`
  - `ASR = 8.40`

Interpretation: the proposed anomaly-localization defense has the best adversarial mAP and the lowest ASR while preserving clean performance.

### Qualitative behavior (pp. 13-14)

- Figure 9 shows that the method restores pedestrian detections that disappear under the adversarial patch attack.
- The paper attributes the gain to localizing the patch region and mitigating its negative effect on YOLOv3's objectness scores.

## Key Claims

1. **Reconstruction-driven anomaly localization can defend against printed patch attacks without prior patch knowledge.** Supported by the method description and Table 1 (pp. 1, 12).
2. **The proposed defense clearly outperforms SAC and PAD on the tested pedestrian benchmark.** Supported by Table 1 (p. 12).
3. **Training only on clean images is enough to identify anomalous patch regions later at inference time.** Supported by the clean-only DCNN training description and the reported gains (pp. 6-7, 12).

## Threat Model

- Attack type: physical adversarial patch attacks against pedestrian detection.
- Defender position: preprocessing before the YOLOv3 detector.
- Training assumption: the reconstruction network is trained on clean pedestrian images only; the method does not require a library of known adversarial patches (pp. 6-7, 14).

## Limitations and Failure Modes

- The paper says the method increases computational complexity because of histogram-based anomaly detection and clustering, which may hurt real-time high-resolution deployment (p. 15).
- Performance depends on manually chosen thresholds and clustering parameters, which may not generalize perfectly across datasets or tasks (p. 15).
- The evaluation is only on pedestrian detection with YOLOv3, so generalization to other domains and detectors is still unverified (p. 15).
- The authors explicitly note possible weakness against natural perturbations such as severe brightness / contrast changes, blur, large blind spots, and strong compression artifacts (p. 15).

## Defensive Takeaways

- This is a useful clean-data-only defense reference in the repo.
- The strongest reusable idea is using reconstruction error as a detector-agnostic anomaly signal, then refining it with fragment-level statistical tests.
- It is a good contrast point to SAR: SAR uses explicit segmentation plus inpainting, while this paper uses anomaly localization plus anomaly-map suppression.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: Indirect only. No direct test.
- **YOLO11**: Indirect only.
- **YOLO26**: Indirect only.
- Capstone relevance: `3/5`. Useful defense baseline, but only validated on YOLOv3 pedestrian detection.

## Reproducibility Signals

- The local PDF gives the DCNN training data, optimizer settings, fragment size, and clustering parameters.
- Clean training data and test data are public.
- I did not find a code release claim in the paper. `unverified-from-pdf`

## Open Questions

- Does the method still work against naturalistic or low-contrast patches rather than the printed Thys-style attack?
- How much of the gain comes from the reconstruction network versus the Isolation Forest / DBSCAN refinement pipeline?
- Can this defense scale to YOLOv8 or YOLO11 without prohibitive latency?
- Would the anomaly-localization logic survive more complex physical corruptions in videos?

## Normalized Extraction

- Canonical slug: `tereshonok2025_anomaly`
- Canonical source record: `docs/papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf`
- Evidence state: `page_cited`
- Threat model: physical adversarial patch attacks against pedestrian detection.
- Detector family and exact version: YOLOv3.
- Attack or defense goal: reconstruct benign structure, localize anomalous patch regions, and preserve detection quality.
- Loss or objective: clean-image reconstruction with MSE, followed by fragment-level anomaly detection via Isolation Forest and DBSCAN post-processing.
- Transforms / EoT: evaluated against the real-world adversarial patch attack from Thys et al. rather than a digital-only benchmark.
- Dataset: MS COCO Person for clean reconstruction training; INRIA Person for evaluation.
- Metrics: clean `mAP`, adversarial `mAP`, `ASR`.
- Strongest quantitative result: adversarial `mAP` rises from `46.79` undefended to `80.97` with the proposed defense, while `ASR` falls to `8.40` (Table 1, p. 12).
- Transfer findings: none reported across detector families.
- Physical findings: the evaluation is tied to a printed physical patch attack scenario (pp. 1-2, 12).
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: indirect defense baseline only.
- Reproducible technique to borrow: clean-only reconstruction plus fragment-level anomaly localization.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `defense_baseline`
