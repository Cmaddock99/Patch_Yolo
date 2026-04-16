# Hu et al. (2022) — AdvTexture for Multi-Angle Physical Person Evasion

## Citation

- Title: *Adversarial Texture for Fooling Person Detectors in the Physical World*
- Authors: Zhanhao Hu, Siyuan Huang, Xiaopei Zhu, Fuchun Sun, Bo Zhang, Xiaolin Hu
- Venue / Year: CVPR 2022
- DOI: 10.1109/CVPR52688.2022.01295
- arXiv: 2203.03373
- URL: https://arxiv.org/abs/2203.03373
- PDF: `docs/papers/advtexture_person_detectors_2203.03373.pdf`

## Problem

- What threat model is assumed? Physical person-evasion attacks where clothing must remain effective across multiple viewing angles instead of only when a single adversarial patch directly faces the camera (pp. 1-2).
- What detector family is studied? Primarily YOLOv2, with additional evaluation on YOLOv3, Faster R-CNN, and Mask R-CNN (pp. 6-8).
- What is the attack goal? Person vanishing from detection in the physical world by covering clothing with an expandable adversarial texture rather than a single patch (pp. 1-2).

## Method

- Core idea: replace a single fixed patch with an **adversarial texture** that can cover arbitrarily sized clothing so any local crop still has adversarial effect (pp. 2, 4-5).
- Main method: **Toroidal-Cropping-based Expandable Generative Attack (TC-EGA)**.
  - Stage 1 trains a fully convolutional generator to produce adversarial local patterns.
  - Stage 2 optimizes a local latent pattern and tiles it through Toroidal Cropping so the final texture stays continuous and expandable (pp. 4-5).
- Physical-robustness mechanisms:
  - EoT-style random transformations
  - TPS deformation for cloth-like warping
  - randomized scales, contrast, brightness, and noise during optimization (p. 3).
- Design motivation: solve the paper's "segment-missing problem," where single patches lose effectiveness when only fragments are visible from oblique viewpoints (pp. 1-2).

## Experimental Setup

- Training and digital evaluation dataset: INRIA Person, with `614` train images and `288` test images (p. 5).
- Physical evaluation:
  - `3` human subjects
  - indoor and outdoor scenes
  - `32` frames sampled per video
  - `192` frames collected for each adversarial clothing item (pp. 5, 8).
- Target detectors: YOLOv2, YOLOv3, Faster R-CNN, Mask R-CNN (pp. 6-8).
- Metrics:
  - `AP` in digital and physical evaluations
  - `mASR` across multiple confidence thresholds for physical tests (pp. 6-8).

## Results

### Table 1 - Digital patch-based evaluation on YOLOv2 (p. 7)

- Clean baseline: `AP = 1.000`.
- Single-patch AdvPatch remains strongest in pure patch form:
  - `AdvPatch = 0.352`
- TC-EGA is nearly as strong while staying expandable:
  - `TC-EGA = 0.362`
- Other expandable or cropped variants are weaker:
  - `EGA = 0.470`
  - `TCA = 0.664`
  - `RCA2x = 0.606`
  - `RCA6x = 0.855`

Interpretation: TC-EGA is the best expandable method, even though a fixed single patch still wins slightly in the narrow digital patch setting.

### Figure 10 - Physical-world YOLOv2 evaluation (p. 8)

- TC-EGA is the only method with strong physical persistence:
  - `TC-EGA, AP = 0.359`
- Baselines largely fail once realized as clothing:
  - `AdvPatch, AP = 0.995`
  - `AdvPatchTile, AP = 0.996`
  - `AdvTshirt, AP = 1.000`
  - `AdvTshirtTile, AP = 0.952`

This is the paper's most important result: the method that is not the strongest in narrow digital patch evaluation becomes the only one that still works well in real physical deployment.

### Table 2 - Clothing-type sensitivity (p. 8)

- Physical mASR varies strongly with garment coverage:
  - random texture: `0.092`
  - T-shirt: `0.771`
  - skirt: `0.287`
  - dress: `0.893`

Larger visible textured area improves attack strength.

### Table 3 - Cross-detector physical transfer (p. 8)

- Physical adversarial clothes transfer across detector families:
  - YOLOv2: `mASR = 0.743`
  - YOLOv3: `mASR = 0.701`
  - Faster R-CNN: `mASR = 0.930`
  - Mask R-CNN: `mASR = 0.855`

This is strong evidence that the texture is not just overfit to one detector.

## Key Claims

1. **Single patches fail under viewpoint change because only fragments remain visible.** Supported by the problem framing and Figure 1 discussion (pp. 1-2).
2. **TC-EGA is the best expandable method in the digital setting while staying competitive with standard AdvPatch.** Supported by Table 1 (p. 7).
3. **TC-EGA is dramatically better than prior baselines in the physical clothing setting.** Supported by Figure 10 and the AP values on page 8.
4. **The resulting adversarial clothes transfer across detector families in the physical world.** Supported by Table 3 (p. 8).

## Threat Model

- Attack type: physical wearable person-evasion attack.
- Attacker capability: print large textures on clothing and optimize them digitally before fabrication.
- Physical variation covered: multiple viewing angles, different garments, indoor/outdoor scenes, and limited detector transfer tests.
- Goal: person vanishing, not misclassification or appearing attacks.

## Limitations and Failure Modes

- Direct detector coverage is old: YOLOv2 and YOLOv3 are the only YOLO versions actually tested. Verified from the model list and tables (pp. 6-8).
- The paper does not evaluate YOLOv8, YOLO11, or YOLO26. Verified from the PDF.
- Transfer is not universal: the conclusion explicitly says transferability to other detectors is limited even though some transfer exists (p. 8).
- Physical effectiveness depends on how much of the garment is visible; the skirt result (`0.287`) is much weaker than the dress result (`0.893`) (Table 2, p. 8).

## Defensive Takeaways

- This is one of the best repo-local physical benchmarks for why cloth deformation and multi-angle visibility matter more than raw digital patch strength.
- It is a useful bridge between older YOLOv2 patch papers and later naturalistic / 3D-aware physical methods.
- The "segment-missing" framing is a strong diagnostic lens for why some physical patches fail after deployment.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: Indirect only. No direct evaluation, but the multi-angle physical benchmark is still highly relevant to any future wearable-patch study.
- **YOLO11**: Indirect only.
- **YOLO26**: Indirect only.
- Capstone relevance: `4/5` for physical benchmarking, `2/5` for exact modern-model comparison.

## Reproducibility Signals

- The PDF gives the method structure, training stages, detector list, and physical collection setup.
- INRIA is public.
- The paper does not clearly state public code availability in the pages reviewed. `unverified-from-pdf`

## Open Questions

- Would the same texture strategy still work on modern Ultralytics heads, or would the texture overfit to older objectness-based detectors?
- How much of the physical gain comes from expandability versus TPS / EoT deformation?
- Would a multi-model objective improve modern cross-YOLO transfer better than the single-detector setup here?
- Can the segment-missing idea explain why some repo patches fail physically even when digital suppression looks strong?

## Normalized Extraction

- Canonical slug: `advtexture2022`
- Canonical source record: `docs/papers/advtexture_person_detectors_2203.03373.pdf`
- Evidence state: `page_cited`
- Threat model: physical wearable adversarial texture attack for person evasion across multiple viewpoints.
- Detector family and exact version: YOLOv2, YOLOv3, Faster R-CNN, Mask R-CNN.
- Attack or defense goal: person-vanishing physical attack that stays effective when only local parts of a garment are visible.
- Loss or objective: generator-based adversarial texture learning with adversary objective plus information objective; physical transforms and TPS are included during optimization.
- Transforms / EoT: randomized scale, contrast, brightness, noise, and TPS deformation.
- Dataset: INRIA Person plus physical recordings from 3 subjects in indoor and outdoor scenes.
- Metrics: `AP` and `mASR`.
- Strongest quantitative result: in physical evaluation, `TC-EGA` reaches `AP = 0.359` on YOLOv2 while baseline clothing realizations remain near `0.952-1.000` AP (Figure 10, p. 8).
- Transfer findings: physical adversarial clothes achieve `mASR` of `0.743`, `0.701`, `0.930`, and `0.855` on YOLOv2, YOLOv3, Faster R-CNN, and Mask R-CNN respectively (Table 3, p. 8).
- Physical findings: garment size and visible area strongly affect success, with dress `0.893` and skirt `0.287` mASR (Table 2, p. 8).
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: no direct evaluation; strong physical benchmark only.
- Reproducible technique to borrow: multi-angle physical robustness should be evaluated at the clothing-texture level, not just with fixed patches.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `benchmark`
