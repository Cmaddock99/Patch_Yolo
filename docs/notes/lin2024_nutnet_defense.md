# Lin et al. (2024) — NutNet Real-Time Defense for Adversarial Patches

## Citation

- Title: *I Don't Know You, But I Can Catch You: Real-Time Defense against Diverse Adversarial Patches for Object Detectors*
- Authors: Zijin Lin, Yue Zhao, Kai Chen, Jinwen He
- Venue / Year: ACM CCS 2024
- DOI: 10.1145/3658644.3670317
- arXiv: 2406.10285
- URL: https://doi.org/10.1145/3658644.3670317
- PDF: `docs/papers/realtime_defense_diverse_patches_2406.10285.pdf`
- Project page: https://sites.google.com/view/nutnet

## Problem

- What threat model is assumed? Online defense against physical and digital adversarial patch attacks on object detectors, including both Hiding Attacks (HA) and Appearing Attacks (AA), with no assumption that the defender knows a specific patch family at inference time (pp. 1-2).
- What detector family is studied? YOLOv2-v4, SSD, Faster R-CNN, and DETR (pp. 1, 7-8).
- What is the defense goal? Detect and suppress adversarial patches while preserving detector accuracy and real-time throughput (pp. 1-2, 11-12).

## Method

- Core approach: NutNet is a lightweight reconstruction-based autoencoder that treats clean images as in-distribution and adversarial patches as out-of-distribution regions that reconstruct poorly (pp. 2-4).
- Main components:
  - image-splitting to amplify the difference between patched and clean regions
  - destructive training to limit the autoencoder's ability to reconstruct out-of-distribution content
  - DualMask generation combining a coarse mask and a fine mask to localize the patch while keeping false positives low (pp. 2-5).
- Efficiency claim: the paper emphasizes that NutNet adds only about `5k` parameters, explicitly contrasting it with heavier segmentation-based defenses (p. 2).
- Training philosophy: the defense is trained on clean-sample structure rather than pre-generated adversarial patches, which is the paper's main generalization argument (pp. 2-3).

## Experimental Setup

- Datasets:
  - INRIA for targeted HA evaluation (p. 8)
  - COCO2014 for untargeted HA evaluation with PAPatch (p. 9)
  - KITTI-derived cropped images for AA evaluation with stop-sign and person patches (p. 9)
  - physical video evaluations on printed patches for YOLOv2 (p. 12)
- Victim detectors: YOLOv2, YOLOv3, YOLOv4, SSD, Faster R-CNN, DETR (pp. 8-9).
- Attack families evaluated:
  - targeted HA: AdvPatch, AdvT-shirt, AdvCloak, NaturalPatch, AdvTexture
  - untargeted HA: PAPatch
  - AA: stop-sign and person patches (pp. 8-9).
- Metrics:
  - `AP0.5` for targeted HA and AA
  - `mAP0.5` for untargeted HA
  - physical attack success rate in videos
  - FPS / efficiency and qualitative generalization comparisons (pp. 8-12).

## Results

### Table 1 - Targeted hiding attacks on INRIA (p. 8)

- NutNet restores person detection strongly across older YOLO models:
  - YOLOv2 with `AdvPatch (a)`: `0.310 -> 0.780`
  - YOLOv3 with `AdvPatch`: `0.206 -> 0.837`
  - YOLOv4 with `AdvPatch`: `0.417 -> 0.829`
- On DETR, the baseline is already less degraded than old YOLO, but NutNet still improves it:
  - DETR with `AdvPatch`: `0.769 / 0.764 -> 0.824 / 0.814`
- Clean-cost is small and sometimes positive:
  - YOLOv2 clean `0.847 -> 0.868`
  - DETR clean `0.857 -> 0.924`

### Table 2 - Untargeted hiding attack on COCO (p. 9)

- Against PAPatch, NutNet gives the largest gain on YOLOv3:
  - YOLOv3 `0.299 -> 0.438`
- It also improves YOLOv2 and YOLOv4:
  - YOLOv2 `0.312 -> 0.351`
  - YOLOv4 `0.425 -> 0.440`

### Table 3 - Appearing attacks (p. 9)

- NutNet is strongest where the objective is to drive false detections nearly to zero:
  - YOLOv2 stop-sign patch: `0.900 -> 0.041`
  - YOLOv3 person patch: `0.952 -> 0.002`
  - YOLOv4 person patch: `0.885 -> 0.000`
  - SSD person patch: `0.843 -> 0.000`
  - DETR stop-sign patch: `0.709 -> 0.003`
  - DETR person patch: `0.767 -> 0.074`

### Table 7 - Physical attack success rates on YOLOv2 (p. 12)

- NutNet collapses physical attack success rates:
  - targeted HA `AdvPatch (a)`: `83.0% -> 0.7%`
  - targeted HA `NaturalPatch`: `39.0% -> 1.0%`
  - untargeted HA `PAPatch`: `74.9% -> 0.3%`
  - AA stop-sign patch: `96.3% -> 0.0%`
  - AA person patch: `98.7% -> 5.6%`

### Efficiency and comparison claims (pp. 1, 11-12)

- The paper's headline claim is that NutNet improves defense performance by over `2.4x` on HA and `4.7x` on AA with only `0.4%` clean-performance sacrifice and about `8%` inference overhead (p. 1).
- Table 6 rates NutNet as the only compared method with consistently good generalization across targeted HA, untargeted HA, and AA while still meeting real-time constraints (p. 12).

## Key Claims

1. **NutNet is the first defense in the paper's comparison set that consistently handles both HA and AA across multiple detector families.** Supported by Tables 1-3 and the summary comparison in Table 6 (pp. 8-12).
2. **Clean-sample-only reconstruction is enough to localize and suppress adversarial patches in practice.** Supported by the clean-performance rows in Tables 1-2 and the physical-world results in Table 7 (pp. 8-12).
3. **The defense remains effective in physical deployment, not just digital benchmarks.** Supported by Table 7 (p. 12).
4. **Efficiency is a major differentiator versus prior segmentation or masking defenses.** Supported by the abstract and Section 5.5 discussion (pp. 1, 11-12).

## Threat Model

- Attack types covered: targeted HA, untargeted HA, and AA.
- Deployment settings: digital images and physical printed attacks.
- Defender position: an online pre-processing or filtering stage before the detector.
- Adaptive setting: the paper explicitly evaluates adaptive attacks against NutNet and argues that stronger bypass pressure also weakens the underlying attack (p. 10, Table 5).

## Limitations and Failure Modes

- The paper does **not** evaluate YOLOv8, YOLO11, or YOLO26 directly. Its YOLO evidence stops at YOLOv4, with DETR added as a transformer-era comparator. Verified from the tested model list and tables (pp. 8-9).
- Physical-world evaluation is only reported for YOLOv2, so the paper does not prove the same real-world defense level on newer detectors. Supported by Table 7 (p. 12).
- Adaptive attacks remain a real concern even though the paper shows they lose much of their original attack power when optimized to evade NutNet (p. 10, Table 5).
- NutNet is a patch-localization and filtering defense, not a guarantee that the base detector itself becomes intrinsically robust. This is my inference from the pipeline design.

## Defensive Takeaways

- This is one of the strongest repo-local detector-side defense baselines for adversarial patches.
- The clean-only training idea is valuable because it avoids dependence on one specific patch family.
- DualMask is the paper's most portable design idea: coarse localization plus fine correction is better than either mask alone (p. 13, Table 9).
- For the sibling defense project, NutNet is a strong comparison point against simpler preprocessing defenses.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: Indirect but meaningful. The paper does not test YOLOv8, yet it is one of the best repo-local examples of a lightweight online defense that already generalizes across one-stage, two-stage, and transformer detectors.
- **YOLO11**: Indirect only. No direct evaluation.
- **YOLO26**: Indirect only. DETR results are relevant as a transformer-era defense stress test, but the paper does not study Hungarian-matching or NMS-free YOLO heads directly.
- Capstone relevance: `4/5`. High-value defense baseline, but not a modern Ultralytics benchmark.

## Reproducibility Signals

- Local PDF contains the full method, ablations, physical evaluation, and efficiency discussion.
- The project page is linked in the abstract.
- The paper gives enough architectural detail to reproduce the defense concept, though exact training implementation details for all detectors are not the main contribution.

## Open Questions

- Does NutNet retain its generalization on YOLOv8 / YOLO11 class heads without retraining changes?
- How well would the method work against naturalistic diffusion-era patches such as AdvLogo?
- Would a DETR-style or YOLO26-style decoder require a different mask or threshold schedule?
- How much of NutNet's benefit comes from reconstruction failure itself versus the specific DualMask heuristic?

## Normalized Extraction

- Canonical slug: `lin2024_nutnet`
- Canonical source record: `docs/papers/realtime_defense_diverse_patches_2406.10285.pdf`
- Evidence state: `page_cited`
- Threat model: Online defense against digital and physical adversarial patches for object detectors, covering both hiding and appearing attacks.
- Detector family and exact version: YOLOv2, YOLOv3, YOLOv4, SSD, Faster R-CNN, DETR.
- Attack or defense goal: Detect and suppress adversarial patches with minimal clean accuracy and latency cost.
- Loss or objective: Reconstruction-based out-of-distribution separation with image-splitting, destructive training, and DualMask localization.
- Transforms / EoT: Evaluated against transformed patches and physical videos; the defense itself is not an attack-training method.
- Dataset: INRIA, COCO2014, KITTI-derived AA set, physical video tests.
- Metrics: `AP0.5`, `mAP0.5`, attack success rate, and runtime.
- Strongest quantitative result: physical attack success rates drop from `83.0%`, `74.9%`, `96.3%`, and `98.7%` to `0.7%`, `0.3%`, `0.0%`, and `5.6%` respectively (Table 7, p. 12).
- Transfer findings: The defense is tested across one-stage, two-stage, and transformer detectors, but not across YOLOv8+ generations.
- Physical findings: Strong physical defense evidence is reported for YOLOv2 video tests.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: indirect defense baseline only.
- Reproducible technique to borrow: lightweight reconstruction defense plus coarse-to-fine patch masking.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `defense_baseline`
