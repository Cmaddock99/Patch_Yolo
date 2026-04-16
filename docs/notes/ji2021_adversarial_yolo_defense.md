# Ji et al. (2021) - Ad-YOLO Patch-Class Defense

## Citation

- Title: *Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches*
- Authors: Ning Ji, Yinan Feng, Haojie Xie, Xueshuang Xiang, Ning Liu
- Venue / Year: arXiv 2021
- arXiv: 2103.08860
- URL: https://arxiv.org/abs/2103.08860
- PDF: `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf`

## Problem

- What threat model is assumed? White-box and physical adversarial patch attacks against human detection, especially chest-mounted printed patches (pp. 1-2, 6-7).
- What detector family is studied? YOLOv2 human detection (pp. 1-4).
- What is the defense goal? Detect the person and the adversarial patch at the same time by adding a patch category directly into the detector head (pp. 1-4).

## Method

- Core idea: extend YOLOv2 with one extra `patch` class so the network learns to localize adversarial patches and preserve the person detection simultaneously (pp. 1-4).
- Architectural change:
  - retain all YOLOv2 layers except the last layer
  - increase each anchor output from `(5 + n)` to `(5 + n + 1)` by adding the patch class probability (p. 4).
- Dataset construction:
  - build `Inria-Patch`, a 200-patch dataset generated through iterative adversarial training over models `M0-M3`
  - use 160 patches for training (`P0`) and 40 for testing (`P1`) (pp. 4-5).
- Training data: Pascal VOC, INRIA, and Inria-Patch are combined to train Ad-YOLO (pp. 1, 4-5).

## Experimental Setup

- Base detector: YOLOv2 trained on Pascal VOC 2007+2012 (pp. 4-6).
- Human-detection benchmark: INRIA Person splits `I0` / `I1` and patch splits `P0` / `P1` (pp. 4-6).
- Main evaluations:
  - clean object detection on VOC 2007
  - generalization across seen / unseen people and patches
  - white-box attacks
  - qualitative physical-world attacks with printed patches (pp. 5-7).

## Results

### Table 2 - VOC 2007 clean object detection (p. 6)

- YOLOv2 `mAP = 73.05%`
- Ad-YOLO `mAP = 72.35%`

Clean object-detection cost is only `0.70` points.

### Table 3 - Generalization on INRIA Person (p. 6)

- `I0-P0`: `79.70%`
- `I1-P0`: `78.70%`
- `I0-P1`: `78.63%`
- `I1-P1`: `77.82%`

Interpretation: Ad-YOLO generalizes well to unseen persons and unseen adversarial patches.

### White-box attack comparison (pp. 6-7, Table 4 on p. 7)

- YOLOv2 person AP falls from `88.03%` clean to `33.93%` under white-box attack.
- Ad-YOLO retains `80.31%` person AP under white-box attack with `86.58%` clean AP.
- Adversarial-training baselines are much weaker under attack:
  - `Model1 = 58.62%`
  - `Model2 = 56.38%`
  - `Model3 = 61.65%`

### Physical-world behavior (p. 7)

- Figure 7 shows that printed patches can fool the original YOLOv2 detector but fail to fool Ad-YOLO in the demonstrated physical scenes.
- The defense also detects the patch itself rather than only restoring the person detection.

## Key Claims

1. **Adding a patch class works far better than adversarial training alone for this threat model.** Supported by Table 4 (p. 7).
2. **The defense has low clean-cost.** Supported by Table 2 and the INRIA clean comparison discussion (pp. 5-6).
3. **Patch diversity during training materially improves generalization to unseen attacks.** Supported by the Inria-Patch construction and Table 3 (pp. 4-6).
4. **The method transfers to physical printed attacks qualitatively.** Supported by Figure 7 (p. 7).

## Threat Model

- Attack type: printed adversarial patch attacks against person detection.
- Patch placement: patches are designed to be placed on the chest in the paper's physical setup (pp. 3, 7).
- Defender position: retrained detector with an extra adversarial-patch class.
- Knowledge assumption: the defender can generate representative training patches and retrain the detector.

## Limitations and Failure Modes

- The paper only evaluates YOLOv2, so it does not prove the same effect on YOLOv8, YOLO11, or YOLO26.
- The defense assumes retraining and access to a diverse patch dataset; that is stronger defender knowledge than a patch-agnostic preprocessing method.
- Physical evidence is qualitative rather than a reported physical AP table (p. 7).
- My inference: patch placements far from the torso or strongly non-Thys-style naturalistic patches may be harder for the learned patch class than the paper's training distribution.

## Defensive Takeaways

- This is still the cleanest direct YOLO-side defense baseline in the repo.
- The most portable idea is not the exact YOLOv2 implementation but the training recipe: add an explicit patch class and train on diverse generated patches.
- It is a useful complement to NutNet, SAR, and anomaly localization because it is detector-integrated rather than preprocessing-based.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: High as a defense idea. The patch-class concept should transfer more easily than many older YOLOv2-specific tricks.
- **YOLO11**: Moderate-to-high as a defense idea, though the paper does not test it directly.
- **YOLO26**: Lower confidence. A patch class may still help, but the end-to-end detection design changes how the extra class would integrate.
- Capstone relevance: `4/5`. Strong direct defense baseline even though it is old.

## Reproducibility Signals

- The local PDF includes the dataset construction loop, the output-head modification, and the main evaluation tables.
- Training details such as optimizers and patch-dataset construction are described in the paper.
- I did not verify a code release from the PDF. `unverified-from-pdf`

## Open Questions

- How well would a patch-class defense generalize to naturalistic or diffusion-based patches?
- Would the same idea retain low clean-cost on modern Ultralytics models?
- How much patch diversity is enough before returns diminish?
- Does explicit patch detection remain stable when the patch is not chest-mounted?

## Normalized Extraction

- Canonical slug: `ji2021_adversarial_yolo_defense`
- Canonical source record: `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf`
- Evidence state: `page_cited`
- Threat model: white-box and physical adversarial patch attacks against human detection.
- Detector family and exact version: YOLOv2.
- Attack or defense goal: defend by adding a dedicated patch class to the detector.
- Loss or objective: YOLOv2 loss with an additional conditional patch-class term plus training on the Inria-Patch dataset.
- Transforms / EoT: patch generation follows the Thys-style attack pipeline; diverse generated patches are used in training.
- Dataset: Pascal VOC 2007+2012, INRIA Person, Inria-Patch.
- Metrics: VOC `mAP`, person `AP`, white-box attack `AP`.
- Strongest quantitative result: Ad-YOLO preserves `80.31%` person AP under white-box attack versus `33.93%` for YOLOv2 and `61.65%` for the best adversarial-training baseline (Table 4, p. 7).
- Transfer findings: generalization to unseen persons and unseen patches remains `77.82-78.70%` AP (Table 3, p. 6).
- Physical findings: qualitative physical defense examples show person and patch both detected where YOLOv2 fails (Figure 7, p. 7).
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: strong defense idea, but no direct modern-model evaluation.
- Reproducible technique to borrow: add an adversarial-patch class and train on diverse generated patches.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `defense_baseline`
