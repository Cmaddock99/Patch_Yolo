# Dimitriu et al. (2024) - Multi-Model Optimization for Physical Transferability

## Citation

- Title: *Improving Transferability of Physical Adversarial Attacks on Object Detectors Through Multi-Model Optimization*
- Authors: Adonisz Dimitriu, Tamas Vilmos Michaletzky, Viktor Remeli
- Venue / Year: Applied Sciences 2024
- DOI: 10.3390/app142311423
- URL: https://doi.org/10.3390/app142311423
- PDF: `docs/papers/dimitriu2024_multi_model_transferability_app142311423.pdf`

## Problem

- What threat model is assumed? Physical-looking adversarial vehicle textures that should transfer across unseen object detectors, with evaluation performed in a photorealistic Unreal Engine pipeline rather than on real printed vehicles (pp. 1-5, 10-13).
- What detector family is studied? YOLOv8, YOLOv5, YOLOv3 during optimization, plus one-stage, two-stage, and transformer-based black-box detectors at evaluation time (pp. 1-2, 6, 9-11).
- What is the attack goal? Improve cross-model transferability of adversarial textures by optimizing against multiple source detectors at once instead of a single source model (pp. 1-2, 5, 8-13).

## Method

- Core idea: reuse the TACO truck-camouflage pipeline, but replace single-model optimization with the mean attack loss across multiple source detectors so the learned texture is less overfit to one architecture (pp. 3-5).
- Rendering pipeline:
  - optimize a texture on a 3D truck in an Unreal Engine 5 scene using a differentiable neural renderer trained to mimic UE5 output (pp. 3-4)
  - combine rendered truck pixels with scene backgrounds using depth maps, masks, and camera parameters from the UE5 dataset (pp. 3-4).
- Loss design:
  - class-confidence loss suppresses boxes overlapping the truck via an IoP threshold (p. 5)
  - IoU term penalizes strong overlap between predicted and ground-truth truck boxes (p. 5)
  - smoothness term keeps the texture physically realizable (p. 5)
  - total single-model loss is `Lcls + beta * LIoU + gamma * Lsmooth`, then multi-model optimization averages that attack loss across the chosen detector set (pp. 5-6).
- Main model combinations tested:
  - within YOLOv8 sizes: pairs and triples such as `YOLOv8{x,n}` and `YOLOv8{x,m,n}` (pp. 8-9)
  - across generations: `YOLOv8n`, `YOLOv5m`, and `YOLOv3` is the best-performing cross-family source combination (pp. 10-13).

## Experimental Setup

- Scene / object: 3D truck camouflage attack, not person evasion (pp. 3-5).
- Data volume:
  - 17,000 daytime truck images from 17 locations for training
  - 8,000 truck images from 8 unseen positions for evaluation (p. 5).
- Camera variation:
  - distances from 5 m to 35 m
  - azimuth from 0 to 360 degrees
  - elevation from 0 to 45 degrees (pp. 5-6).
- Optimization settings:
  - image resolution `640 x 640`
  - Adam with learning rate `0.012`, `beta1 = 0.25`, `beta2 = 0.9`
  - batch size `6`
  - `beta = 0.01`, `gamma = 0.1`
  - thresholds `tauIoP = 0.6`, `tauIoU = 0.45`
  - `6` training epochs (pp. 5-6).
- Evaluation models:
  - YOLOv8 family for within-family tests (pp. 6-8)
  - small external detectors: YOLOv5n, YOLOv10n, YOLOX-n, RetinaNet-s, RT-DETR-s (p. 9)
  - large external detectors: YOLOv5x, YOLOv10x, YOLOX-x, RetinaNet-x, RT-DETR-x (p. 9)
  - broader final comparison: one-stage, two-stage, and transformer detector groups (pp. 10-12).

## Results

### Within-Family Transfer Trend

- Single-model textures show strong source-size dependence:
  - `YOLOv8n`-optimized textures attack small targets well but weaken as target size grows
  - `YOLOv8x`-optimized textures do better against larger targets (pp. 7-8).
- Multi-model YOLOv8 training improves consistency across sizes. In Table 3, the best pure-YOLOv8 combination is `YOLOv8{x,m,n}` with mean `AP@0.5 = 0.0296`, beating weaker pairs such as `YOLOv8{x,n}` at `0.0475` and `YOLOv8{x,l}` at `0.0835` (p. 8).

### Transfer to Other Detector Families

- On small outside-family targets, `YOLOv8{x,m,n}` improves substantially over single-model baselines:
  - `YOLOv10n`: `0.0586` vs. `0.0387` for `YOLOv8n` and `0.3062` for `YOLOv8x`
  - `RT-DETR-s`: `0.2295` vs. `0.3162` for `YOLOv8n` and `0.5209` for `YOLOv8x` (p. 9).
- On large outside-family targets, `YOLOv8{x,m,n}` also wins:
  - `YOLOv5x`: `0.0293`
  - `YOLOv10x`: `0.0592`
  - `RT-DETR-x`: `0.3255`, substantially lower than `0.5032` from `YOLOv8n` and `0.4705` from `YOLOv8x` (p. 9).

### Best Cross-Family Combination

- The strongest overall source combination is `YOLOv{8n,5m,3}`:
  - total mean `AP@0.5 = 0.0972` across one-stage, two-stage, and transformer detectors
  - one-stage mean `0.0736`
  - two-stage mean `0.0760`
  - transformer mean `0.1421` (pp. 10-11).
- The alternative `YOLOv{8m,5n,3}` is close at total mean `0.0978`, but slightly worse overall (p. 11).
- Low-light evaluation preserves the same ordering: `YOLOv{8n,5m,3}` remains best with mean `AP@0.5 = 0.2636` at night (p. 10).

## Key Claims

1. Multi-model optimization improves transferability over single-model texture training. Supported by Tables 3, 5, 6, and 7 (pp. 8-11).
2. Mixing model size and generation matters: the best source set combines `YOLOv8n`, `YOLOv5m`, and `YOLOv3`, not just different sizes within one family. Supported by Table 7 and Discussion (pp. 11-13).
3. CNN-trained textures can still transfer meaningfully to transformer detectors such as RT-DETR and DINO. Supported, though transformers remain harder targets than one-stage or two-stage CNN detectors (pp. 11-13).
4. The method provides real-world transfer guidance, but not real-world physical validation. Supported as a limitation: evaluation is photorealistic/synthetic, not printed-vehicle field testing (pp. 3-6, 10-14).

## Threat Model

- White-box optimization on selected source detectors
- Black-box evaluation on other detector families
- Vehicle camouflage, not person-worn patches
- Photorealistic neural-rendered UE5 scenes rather than real captured physical deployments
- Daytime scenes for training and evaluation, plus a separate nighttime robustness check (pp. 5-6, 10-12)

## Limitations and Failure Modes

- The paper targets trucks rather than pedestrians, so its attack geometry and texture coverage differ materially from wearable person-evasion patches. This is an inference from the setup (pp. 3-5).
- Physical claims are simulation-backed, not field-tested with printed materials or real cameras (pp. 3-6, 10-14).
- The optimization set is still YOLO-only; the paper explicitly says future work should include transformer and other CNN families during training (p. 13).
- No YOLO11 or YOLO26 evaluation appears in the paper, so the repo still lacks direct literature on the v8-to-v11-to-v26 ladder (pp. 6-13).
- Data are not readily available; the dataset is only available by request, and no public code release is stated in the paper (p. 14).

## Takeaways

- This is the cleanest repo-local evidence that multi-model source training can materially improve black-box transfer in physical-style detector attacks.
- It strengthens the repo's attack-side method lane: if `YOLOv8n` alone is a weak source, then mixing it with a different generation and scale is a literature-backed next step.
- It also gives a direct bridge between Bayer's "small source models transfer poorly" result and the repo's next experimental move: broaden the surrogate set rather than only tuning losses on one nano model.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: direct. The paper optimizes and evaluates on YOLOv8 variants extensively (pp. 6-11).
- **YOLO11**: indirect. The paper does not include YOLO11, but it supports the general idea that mixing model generations can improve transfer beyond one-family training. This is my inference from the reported `YOLOv8 + YOLOv5 + YOLOv3` result.
- **YOLO26**: indirect. The paper tests RT-DETR and DINO as transformer-side targets and shows non-trivial transfer still occurs, which is relevant to the repo's YOLO26 problem. This is an inference, not a direct YOLO26 result.
- Capstone relevance: **5/5**. It is now one of the strongest method papers for improving cross-detector transfer in the repo-local corpus.

## Reproducibility Signals

- Detailed loss definitions and hyperparameters are provided (pp. 4-6).
- Training/eval image counts, angle ranges, and distance ranges are specified (pp. 5-6).
- Detector tables list the target models explicitly (pp. 6-11).
- Dataset access is by request rather than open release, which weakens practical reproducibility (p. 14).
- No public code release is stated in the paper pages reviewed.

## Open Questions

- How much of the gain comes from model diversity versus simply training on a larger single source model?
- Would replacing `YOLOv3` in the best trio with a DETR-style or anchor-free detector improve transfer to YOLO26-like targets further?
- Does the same multi-model strategy help person-worn patches as much as full-vehicle camouflage?
- How much of the nighttime robustness gap is due to missing night data versus a deeper failure of the learned texture?

## Normalized Extraction

- Canonical slug: `dimitriu2024_multi_model_transferability`
- Canonical source record: `docs/papers/dimitriu2024_multi_model_transferability_app142311423.pdf`
- Evidence state: `page_cited`
- Threat model: white-box multi-model adversarial texture optimization on source detectors with black-box transfer evaluation across detector families.
- Detector family and exact version: YOLOv8, YOLOv5, YOLOv3 during optimization; YOLOv10, YOLOX, RetinaNet, Faster R-CNN, Cascade R-CNN, Sparse R-CNN, RT-DETR, RTMDet, DINO, and DDQ at evaluation.
- Attack or defense goal: improve cross-model transferability of physical-style adversarial textures.
- Loss or objective: average the TACO attack loss across multiple source detectors, where the base loss combines class-confidence suppression, IoU penalty, and smoothness.
- Transforms / EoT: camera-angle, distance, and scene variation are built into the UE5 dataset and rendering pipeline; nighttime evaluation is reported separately.
- Dataset: 17,000 training images from 17 truck locations and 8,000 evaluation images from 8 unseen positions.
- Metrics: `AP@0.5` across source-family, outside-family, and detector-category evaluations.
- Strongest quantitative result: `YOLOv{8n,5m,3}` reaches total mean `AP@0.5 = 0.0972` across one-stage, two-stage, and transformer detectors, with `0.2636` in low-light evaluation (pp. 10-12).
- Transfer findings: multi-model optimization outperforms single-model source training both within YOLOv8 and across external detector families.
- Physical findings: physically realizable vehicle textures are optimized in photorealistic simulation, but no real printed physical deployment is reported.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: direct for YOLOv8; method-level relevance for YOLO11 and transformer-like YOLO26 transfer.
- Reproducible technique to borrow: average the attack loss across mixed-generation surrogate detectors instead of relying on one YOLO source model.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `cross_yolo_transfer`
- Disposition: `method_to_borrow`
