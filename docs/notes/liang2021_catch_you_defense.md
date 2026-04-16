# Li et al. (2025) — We Can Always Catch You

## Citation

- Title: *We Can Always Catch You: Detecting Adversarial Patched Objects WITH or WITHOUT Signature*
- Authors: Jiachun Li, Jianan Feng, Jianjun Huang, Bin Liang
- Venue / Year: IEEE Transactions on Dependable and Secure Computing, 2025
- arXiv: 2106.05261
- URL: https://arxiv.org/abs/2106.05261
- PDF: `docs/papers/we_can_always_catch_you_2106.05261.pdf`

## Problem

- What threat model is assumed? Defense against adversarial patch attacks on object detectors in both digital and physical settings, including attacks on YOLO-style person detection (pp. 1-2).
- What detector family is studied? YOLOv2, YOLOv4, YOLOR, YOLOv8, plus a camouflage transfer case on Faster R-CNN (pp. 6-12).
- What is the defense goal? Detect whether an object in an image is adversarially patched, either through patch signatures or through local/global semantics inconsistency, so hidden objects can be recovered at detection time (pp. 1-2).

## Method

- The paper proposes **two different defense families**:
  - a **signature-based** approach
  - a **signature-independent** approach (pp. 1-2).
- Signature-based branch:
  - **Region Entropy** identifies patch blocks with unusually high entropy, then isolates candidate regions with GrabCut and fills them with a learned benign sticker (pp. 5-6).
  - **Guided Grad-CAM** identifies pixels with abnormally high class-discriminative importance and filters the top-scoring `n%` pixels, with `n = 2%` chosen in validation (p. 6, Table 2).
- Signature-independent branch:
  - detects **content semantics inconsistency** through region growing
  - the key idea is that benign objects should remain detectable globally if they are detectable locally, while patched adversarial objects can appear locally but disappear globally (pp. 10-12).
- Tradeoff stated by the paper:
  - signature-based method is faster and more real-time friendly
  - signature-independent method is slower but more robust to unknown and defense-aware attacks (pp. 1-2, 12).

## Experimental Setup

- Digital datasets:
  - adversarial / benign pairs on COCO and VOC
  - `905` adversarial and `905` benign digital examples in total according to the setup description (p. 7).
- Physical datasets:
  - `1200` physical AdvPatch-style examples
  - `72` MyAdvTshirt adversarial examples plus `72` corresponding benign examples
  - AdvTshirt physical examples from prior work (p. 7).
- Victim models:
  - YOLOv2, YOLOv4, YOLOR, YOLOv8 for the main defense evaluation
  - Faster R-CNN for the camouflage transfer case (pp. 7, 12).
- Metrics:
  - precision, recall, and F1 for adversarial-example detection rather than raw detector AP (pp. 7, 12).

## Results

### Table 4 - Signature-based results against prior defenses (p. 7)

- **Region Entropy** is consistently the strongest signature-based variant overall:
  - YOLOv8 digital COCO: `P/R/F1 = 0.995 / 0.910 / 0.950`
  - YOLOv8 digital VOC: `0.983 / 0.931 / 0.957`
  - physical YOLOv2 MyAdvTshirt: `1.000 / 0.917 / 0.957`
  - total row: `0.964 / 0.814 / 0.876`
- **Guided Grad-CAM** is weaker overall on digital benchmarks but very strong on some physical cases:
  - physical YOLOv2 AdvTshirt: `1.000 / 1.000 / 1.000`
  - total row: `0.949 / 0.643 / 0.745`
- Compared baselines such as DetectGuard, ObjectSeeker, and UDF are consistently worse in the total row:
  - DetectGuard total F1 `0.463`
  - ObjectSeeker total F1 `0.456`
  - UDF total F1 `0.593`
  - Region Entropy total F1 `0.876`

### Table 8 - Signature-independent detection (p. 12)

- The signature-independent method is strong and more balanced across datasets:
  - YOLOv2 COCO/VOC: `F1 = 0.911 / 0.894`
  - YOLOv4 COCO/VOC: `0.935 / 0.909`
  - YOLOR COCO/VOC: `0.904 / 0.937`
  - YOLOv8 COCO/VOC: `0.931 / 0.884`
  - physical YOLOv2 indoor/outdoor: `0.934 / 0.967`
  - physical MyAdvTshirt: `0.965`
  - physical AdvTshirt: `1.000`
  - total row: `P/R/F1 = 0.951 / 0.904 / 0.926`

### Runtime and deployment claims (pp. 8, 12)

- The text explicitly states the signature-based method can reach real-time performance on several YOLO models, while the signature-independent method is slower but more general.
- The paper describes the signature-independent method as roughly `0.96s` per image on YOLOv2 and `0.53s` on YOLOv8 in its discussion section, which is acceptable for sampled or parallelized monitoring rather than strict frame-by-frame real-time defense (p. 15 in extracted discussion block).

## Key Claims

1. **Known adversarial patches expose exploitable signatures such as high entropy and high Guided Grad-CAM salience.** Supported by Sections 3.2-3.3 and Tables 1-3 (pp. 5-6).
2. **A simple signature-based defense can already outperform prior detector-patch defenses by a large margin.** Supported by Table 4 (p. 7).
3. **A signature-independent semantics-consistency method can detect unknown and defense-aware attacks better than signature-based heuristics.** Supported by the method framing and Table 8 (pp. 10-12).
4. **The defense story extends to newer detectors such as YOLOv8, not just YOLOv2-era models.** Supported by Tables 4 and 8 (pp. 7, 12).

## Threat Model

- Attacks considered: adversarial patch attacks that hide or camouflage objects.
- Deployment settings: digital images and physical examples.
- Detection target: identify adversarially patched objects rather than directly retraining the detector.
- Defense-aware setting: the paper explicitly discusses and tests this case for the signature-independent method (pp. 1-2, 14-15).

## Limitations and Failure Modes

- The signature-based methods depend on specific patch signatures and may fail on previously unseen patch styles. This is the paper's own motivation for adding the signature-independent branch (pp. 1-2).
- The signature-independent method is not real-time in the strictest sense; it is slower and better suited to sampled or parallel monitoring workflows (pp. 12, 15).
- The paper is still about **detection of patched objects**, not full restoration or model hardening.
- YOLO11 and YOLO26 are not evaluated. Verified from the tested model list.

## Defensive Takeaways

- This is one of the strongest repo-local defenses for the sibling defense project because it gives both a fast heuristic detector and a slower general detector.
- The semantics-consistency idea is especially useful because it is not tied to one patch family.
- The paper provides direct YOLOv8-era evidence, which is rare in the local corpus for defense-side work.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: High. Directly evaluated in both signature-based and signature-independent experiments.
- **YOLO11**: Medium by architectural analogy only. No direct test.
- **YOLO26**: Low to medium. The semantics-consistency idea might still transfer conceptually, but the paper does not evaluate NMS-free or Hungarian-matching detectors.
- Capstone relevance: `4/5` for defense planning, `2/5` for attack benchmarking.

## Reproducibility Signals

- The paper provides public dataset links for its detection data in the introduction block.
- Hyperparameter choices are explicit for `m` and `n` in Tables 1-3 (pp. 5-6).
- The workflow for both defenses is fully described at the algorithm level.

## Open Questions

- Does the signature-independent method remain as strong on YOLO11 and YOLO26 where head behavior differs?
- How would the method behave on diffusion-generated naturalistic patches such as AdvLogo?
- Is the semantics-consistency test robust to crowded scenes with severe occlusion?
- Could the fast signature-based detector be used as a front-end trigger for a slower recovery model?

## Normalized Extraction

- Canonical slug: `liang2021_catch_you`
- Canonical source record: `docs/papers/we_can_always_catch_you_2106.05261.pdf`
- Evidence state: `page_cited`
- Threat model: digital and physical adversarial patch detection for object detectors.
- Detector family and exact version: YOLOv2, YOLOv4, YOLOR, YOLOv8, plus Faster R-CNN in the camouflage case.
- Attack or defense goal: detect adversarially patched objects with fast signature-based and general signature-independent methods.
- Loss or objective: no attack optimization contribution; main defenses are entropy / Grad-CAM filtering and semantics-consistency region growing.
- Transforms / EoT: evaluated on digital and physical examples, including clothing-based attacks.
- Dataset: COCO, VOC, physical AdvPatch-style data, MyAdvTshirt, and AdvTshirt examples.
- Metrics: precision, recall, and F1 for adversarial-example detection.
- Strongest quantitative result: signature-independent total `F1 = 0.926`, with YOLOv8 digital `F1 = 0.931` on COCO and physical `F1 = 1.000` on AdvTshirt examples (Table 8, p. 12).
- Transfer findings: the paper is about defense generality more than attack transfer, but it demonstrates cross-model applicability up to YOLOv8 and Faster R-CNN camouflage detection.
- Physical findings: both defense families work on physical patched examples, with particularly strong physical F1 scores in Tables 4, 5, and 8.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: direct for YOLOv8 only.
- Reproducible technique to borrow: semantics-consistency detection is the most project-useful idea.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `defense_baseline`
