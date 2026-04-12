# Paper Review: DePatch — Decoupled Adversarial Patch for Person Detectors

## Citation

- Title: DePatch: Towards Robust Adversarial Patch for Evading Person Detectors in the Real World
- Authors: Jikang Cheng, Ying Zhang, Zhongyuan Wang, Zou Qin, Chen Li
- Venue / Year: arXiv 2408.06625, 2024
- URL: https://arxiv.org/abs/2408.06625
- PDF: `docs/papers/cheng2024_depatch_person_detector_2408.06625.pdf`

## Problem

- What threat model is assumed? Physical adversary deploying a printed patch worn on clothing or as a poster held on a person's front. White-box gradient access to source detector during training.
- What detector is attacked? YOLOv2 (primary test bed); evaluated for transfer on YOLOv3 and YOLOv5.
- What is the attack goal? Person vanishing — suppress person-class detections under real-world physical transformations including distance, occlusion, lighting, and outdoor conditions.

## Method

- Patch type: Expandable block-wise segmented adversarial patch applied to clothing or poster
- Key insight: "Self-coupling issue" — standard patches fail physically because any degraded segment breaks the entire patch's adversarial signal, since all segments are jointly optimized. Block-wise decoupling makes each segment independently adversarial.
- Optimization method: Block-wise Bernoulli masking (randomly zero out n×n blocks at ratio r during each training iteration); border-shifting sliding window to prevent segment boundary over-fitting; Progressive Decoupling Strategy (PDS: gradually increase n from 2→6, r from 0.2→0.5 across 2000 epochs)
- Loss terms: L_acc (IoU-weighted accuracy score minimization — selects highest-accuracy bounding box as optimization target), L_nps (non-printability score), L_tv (total variation). Full objective: DePatch = argmin(L_acc + α·L_nps + β·L_tv), α=0.01, β=2.5
- Transformations / EoT details: Standard EoT (noise, contrast, brightness, rotation) + Toroidal Cropping (TC) for clothing expandability
- Physical-world considerations: Manufactured adversarial clothing (short-sleeve shirt, long-sleeve shirt, dress) and posters; 3 subjects varying in age and height; video evaluation at 1.5m, 3.0m, 4.5m distances; outdoor and indoor testing; full occlusion conditions

## Experimental Setup

- Dataset: Inria Person (614 train / 288 test); MS-COCO validation (2693 person images for cross-dataset)
- Target classes: Person (COCO class 0)
- Model versions: YOLOv2 (primary); transfer to YOLOv3 [ref 25], YOLOv5 [ref 16]
- Metrics: AP (digital, IoU@0.5); ASR = Attack Success Rate (% frames where detector yields incorrect detection at confidence < 0.5 or IoU < 0.5; physical world)
- Training hardware: One NVIDIA Tesla V100; 2000 epochs; Adam optimizer lr=0.03; patch initialized 300×300 Gaussian noise; 90000 pixels for fair comparison

## Results

### Table 1 — Digital Results, Inria Person test set (AP %, lower = better attack)

| Method | Original | EoT | TC Mean | Oc(0.1) | Oc(0.2) | Oc(0.3) | Overall |
|---|---|---|---|---|---|---|---|
| Noise | — | 96.23 | 96.09 | 95.71 | 96.38 | 95.91 | 95.52 | 96.12 |
| AdvPatch | 2019 | 18.55 | 32.87 | 81.89 | 51.47 | 60.16 | 74.72 | 60.42 |
| AdvTshirt | 2020 | 54.75 | 75.04 | 85.10 | 84.30 | 85.93 | 90.75 | 84.22 |
| AdvCloak | 2020 | 57.11 | 76.63 | 82.62 | 82.15 | 87.45 | 91.32 | 84.04 |
| AdvTexture | 2022 | 25.96 | 36.52 | 36.93 | 51.72 | 72.47 | 86.88 | 56.90 |
| T-SEA | 2023 | 20.21 | 27.18 | 78.78 | 36.31 | 48.43 | 70.36 | 46.71 |
| **DePatch** | **2024** | **17.75** | **20.06** | **54.45** | **22.35** | **27.74** | **45.90** | **34.10** |
| DePatch+TC | 2024 | 21.43 | 24.64 | 25.30 | 28.12 | 40.87 | 49.26 | 33.78 |

(Page 9, Table 1) — **Supported** (paper's own evaluation)

### Table 2 — Cross-Dataset, MS-COCO validation (AP %, lower = better)

| Method | Original | EoT | Oc Mean | Overall |
|---|---|---|---|---|
| Noise | 89.18 | 90.91 | 87.17 | 89.04 |
| AdvPatch | 38.15 | 53.26 | 54.33 | 53.80 |
| AdvCloak | 64.73 | 65.17 | 72.23 | 68.70 |
| **DePatch** | **30.37** | **32.16** | **38.02** | **35.09** |

(Page 11, Table 2) — **Supported**

### Tables 3+4 — Physical World ASR (higher = better attack)

**Poster-based (Table 3):**
- DePatch Overall ASR: **0.8014** vs AdvPatch 0.1253, AdvTexture 0.4694
- At 1.5m: DePatch 0.7037; at 3m: 0.8981; at 4.5m: 0.8333
- Outdoor: DePatch 0.5677

**Clothing-based (Table 4):**
- DePatch Overall ASR: **0.9096** vs AdvTexture 0.6947
- 360° rotation: DePatch 0.9629 vs AdvTexture 0.8055

(Pages 11-12, Tables 3-4) — **Supported** (physical world with real subjects)

## Key Claims

1. **Self-coupling issue is the primary reason standard patches fail physically** (p. 6): when any segment degrades, all segments lose adversarial effectiveness because of joint optimization dependencies. **Supported** (Figure 3 demonstrates AP degradation curves under increasing occlusion ratios).

2. **Block-wise decoupling makes each segment independently adversarial**, recovering effectiveness even under partial physical damage. **Supported** (Tables 1, 3, 4).

3. **DePatch achieves best digital AP suppression under occlusion conditions** on Inria. Under 30% occlusion (Oc 0.3), DePatch AP = 45.90% vs AdvTexture 86.88%, AdvPatch 74.72%. **Supported**.

4. **DePatch generalizes cross-dataset** (trained on Inria, tested on COCO) — 30.37% AP overall vs 38.15% AdvPatch. **Supported**.

5. **Physical world effectiveness far superior to baselines** — poster-based ASR 80.14%, clothing-based ASR 90.96% overall. **Supported** (physical trials with 3 real subjects, video evaluation).

## Threat Model

- Attacker capability: White-box access to source detector (gradient-based optimization)
- Deployment: Printed patch worn on clothing or as poster attached to clothing
- Scene: Surveillance-style cameras; outdoor and indoor; various viewing distances (1.5–4.5m)
- Physical degradation: Distance attenuation, partial occlusion by other objects, outdoor lighting, 360° rotation of subjects
- Transfer: Black-box transfer from YOLOv2 → YOLOv3, YOLOv5 (not quantified in main tables; mentioned but numbers not prominent in pages read)

## Method at a High Level

[restricted-summary] Block-wise segmentation of patch pixels followed by stochastic erasure of segments during gradient optimization. Segments are treated as transparent when zeroed (not black), so the model sees clean image underneath. Progressive training schedule increases segment granularity (n) and erasure ratio (r) during training. L_acc uses IoU-weighted accuracy score to select the highest-quality bounding box as the minimization target, rather than maximizing objectness or class score alone.

## Limitations and Failure Modes

- Primary test model is YOLOv2 — direct applicability to YOLOv8/v11/v26 requires re-training (not evaluated in paper). **My inference.**
- DePatch+TC performs slightly worse than DePatch alone in digital settings, suggesting the Toroidal Cropping technique slightly reduces adversarial effectiveness while improving expandability. (p. 11, Table 1) — **Paper claim (Mixed)**.
- Outdoor ASR (0.5677) is substantially lower than controlled indoor/distance tests, indicating real outdoor conditions degrade performance. **Supported** (Table 3).
- No evaluation on newer YOLO generations (v8, v11, v26). **Verified-from-pdf (absence)**.

## Defensive Takeaways

- Patches trained with block-wise decoupling are significantly harder to defend via simple patch detection because they do not rely on spatial contiguity — a defense that assumes coherent high-frequency regions may fail.
- The physical robustness demonstrated (90.96% ASR on clothing) underscores the severity of the threat; this motivates the need for adversarial training on physically augmented data, not just digital augmentations.
- Erased-region transparency (showing clean image under erased blocks) is a training trick worth noting: defenses based on reconstructing "what's under the patch" may be less effective if the patch is sparse.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: High. DePatch targets YOLOv2 but the block-wise decoupling technique is detector-agnostic and can be applied directly to YOLOv8n as a training improvement. The L_acc loss reformulation (using IoU + objectness score as optimization target) is directly applicable to YOLOv8's decoupled head.
- **YOLO11**: High. Same decoupled head architecture. Decoupling trick is plug-in compatible.
- **YOLO26**: Medium. Architecture differences (NMS-free) may change which loss component to target, but decoupling strategy is architecture-independent.
- Capstone relevance: **5/5**. This is the most directly applicable 2024 paper to the capstone's physical robustness goal. DePatch's block-wise decoupling + PDS is a concrete, implementable improvement to the current patch training loop.

## Reproducibility Signals

- Training details provided: 2000 epochs, Adam lr=0.03, 300×300 patch, 90000 pixels normalized, α=0.01, β=2.5 (p. 10)
- Dataset: Inria Person (public) + COCO validation (public)
- Code: Not explicitly mentioned in PDF pages reviewed — **unverified-from-pdf**
- Physical evaluation: 3 subjects, 36 frames/video × 3 subjects = 108 images per condition; outdoor + indoor (p. 9-10)

## Open Questions

- Does this transfer to YOLOv8/v11/v26? Not evaluated; this is the primary gap for the capstone.
- What are the exact per-model ASR numbers for YOLOv3 and YOLOv5 transfer? (mentioned but not prominent in pages reviewed)
- Is code available? Unverified — check arXiv supplemental.
- How does DePatch compare to DAP (Guesmi 2024) on physical robustness with identical evaluation conditions?
