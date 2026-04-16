# Xu et al. (2020) - Adversarial T-shirt Physical Benchmark

## Citation

- Title: *Adversarial T-shirt! Evading Person Detectors in A Physical World*
- Authors: Kaidi Xu, Gaoyuan Zhang, Sijia Liu, Quanfu Fan, Mengshu Sun, Hongge Chen, Pin-Yu Chen, Yanzhi Wang, Xue Lin
- Venue / Year: ECCV 2020
- arXiv: 1910.11099
- URL: https://arxiv.org/abs/1910.11099
- PDF: `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf`

## Problem

- What threat model is assumed? A person wears a printed adversarial T-shirt so that a person detector misses them in the physical world while they move, deform the cloth, and change pose (pp. 1-3).
- What detector family is studied? YOLOv2 and Faster R-CNN (pp. 1, 9).
- What is the attack goal? Physical person-vanishing under non-rigid cloth deformation, not just digital suppression on static images (pp. 1-3).

## Method

- Core idea: explicitly model T-shirt deformation with thin plate spline (`TPS`) during patch optimization (pp. 3-8).
- Physical robustness components:
  - `TPS` transformation for cloth warping
  - physical color transformation from digital to printed appearance
  - standard physical transforms such as scaling, translation, rotation, brightness, and blurring (pp. 7-8).
- Multi-detector extension: the paper also proposes a min-max ensemble attack against YOLOv2 and Faster R-CNN simultaneously (p. 8).
- Main message: without TPS-based non-rigid modeling, the physical attack degrades sharply (pp. 10-12).

## Experimental Setup

- Training data: `40` videos with `2003` frames collected from four scenes for learning the perturbation (p. 9).
- Digital test set: `10` videos captured in the same scene family (p. 9).
- Physical test set: printed T-shirts evaluated in indoor, outdoor, and unseen scenes using iPhone X video at `416 x 416` resolution (pp. 9, 11-12).
- Victim detectors: YOLOv2 and Faster R-CNN, both pretrained on COCO with confidence threshold `0.7` (p. 9).
- Metric: attack success rate (`ASR`) over test frames (p. 9).

## Results

### Table 1 - Digital ASR (p. 11)

- Single-detector attacks:
  - Faster R-CNN: `61%` with TPS vs `34%` without TPS
  - YOLOv2: `74%` with TPS vs `48%` without TPS
- Single-detector transfer is weak:
  - Faster R-CNN -> YOLOv2 or vice versa only `10-13%`
- Ensemble attacks:
  - Faster R-CNN average / min-max: `32% / 47%`
  - YOLOv2 average / min-max: `60% / 53%`
- Baseline advPatch is much weaker:
  - Faster R-CNN target `22%`
  - YOLOv2 target `24%`

### Table 2 - Physical ASR (p. 12)

- Faster R-CNN with TPS:
  - indoor `50%`
  - outdoor `42%`
  - new scenes `48%`
  - average `47%`
- YOLOv2 with TPS:
  - indoor `64%`
  - outdoor `47%`
  - new scenes `59%`
  - average `57%`
- Baseline advPatch on YOLOv2 averages only `18%`, so the TPS-based wearable attack is a large physical improvement.

### Table 3 and ablation discussion (pp. 12-13)

- Pose sensitivity on YOLOv2 with TPS:
  - crouching `53%`
  - sitting `32%`
  - running `63%`
- Complex scenes remain workable:
  - office `73%`
  - parking lot `65%`
  - crossroad `54%`
- Angle and distance limits:
  - works well within about `20` degrees and `4 m`
  - drops sharply around `30` degrees and beyond `7 m` (p. 12).

## Key Claims

1. **TPS-based cloth deformation modeling is the key reason the method works physically.** Supported by Table 1 and the page-12 ablation discussion.
2. **This is the first successful adversarial wearable attack in the paper's framing.** Supported by the abstract and conclusion (pp. 1, 13).
3. **Physical transfer is possible but much weaker than direct single-detector optimization.** Supported by Tables 1-2 (pp. 11-12).
4. **Outdoor lighting, pose, angle, and occlusion remain major physical failure modes.** Supported by the physical-scene and ablation discussion (pp. 11-13).

## Threat Model

- Attack type: physical wearable patch / T-shirt attack against pedestrian detectors.
- Deployment: moving person in real scenes, not a static printed object.
- Attacker capability: print a full-shirt pattern and optimize it with deformation-aware EoT plus physical color calibration.

## Limitations and Failure Modes

- Direct transfer between the two detectors is weak in digital evaluation (`10-13%`), so cross-detector generalization is limited (p. 11).
- Performance drops outdoors and in unseen scenes compared with the best indoor case (p. 12).
- Strong camera angle changes and larger distances hurt the attack substantially; the paper explicitly flags degradation around `30` degrees and beyond `7 m` (p. 12).
- The paper only evaluates YOLOv2 and Faster R-CNN, so it does not answer how modern Ultralytics models behave.

## Offensive Takeaways

- This remains one of the most important physical person-evasion benchmark papers in the repo.
- TPS-style non-rigid modeling is the main transferable idea for any future wearable or cloth attack experiments.
- The paper is also a useful caution against over-reading digital success: physical deployment costs about a `10` point ASR drop even for the stronger method (pp. 11-12).

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: Indirect benchmark only.
- **YOLO11**: Indirect benchmark only.
- **YOLO26**: Indirect benchmark only.
- Capstone relevance: `4/5`. Foundational physical benchmark even though the detectors are old.

## Reproducibility Signals

- The local PDF includes TPS construction details, the physical transform library, the min-max ensemble objective, and the physical evaluation design.
- Appendix material includes threshold, lambda, and dataset-summary details.
- I did not verify a code release from the PDF. `unverified-from-pdf`

## Open Questions

- Would TPS plus modern Ultralytics heads produce similar physical gains, or do newer detectors break the old setup?
- How much of the result comes from TPS itself versus the physical color transformation and conventional EoT stack?
- Can the weak transfer reported here be improved by later methods such as T-SEA or multi-model optimization?
- How much of the remaining physical drop is due to occlusion versus detector robustness?

## Normalized Extraction

- Canonical slug: `xu2020_adversarial_tshirt`
- Canonical source record: `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf`
- Evidence state: `page_cited`
- Threat model: physical wearable person-evasion attack using an adversarial T-shirt.
- Detector family and exact version: YOLOv2, Faster R-CNN.
- Attack or defense goal: hide a person from detection under cloth deformation and real-world scene variation.
- Loss or objective: TPS-based deformation-aware optimization with physical color transformation and a min-max ensemble variant for multi-detector attacks.
- Transforms / EoT: TPS warping, color transformation, scaling, translation, rotation, brightness, blurring.
- Dataset: custom video collection for digital and physical evaluation.
- Metrics: `ASR`.
- Strongest quantitative result: YOLOv2 reaches `74%` digital ASR and `57%` average physical ASR with TPS, versus `24%` and `18%` for the advPatch baseline (Tables 1-2, pp. 11-12).
- Transfer findings: single-detector transfer remains weak at `10-13%` in digital evaluation (Table 1, p. 11).
- Physical findings: YOLOv2 physical ASR is `64%` indoor, `47%` outdoor, and `59%` in unseen scenes; angle and distance degrade the method beyond about `20` degrees and `4 m` (pp. 12-13).
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: no direct evaluation; foundational physical baseline only.
- Reproducible technique to borrow: TPS-based deformation modeling for cloth attacks.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `benchmark`
