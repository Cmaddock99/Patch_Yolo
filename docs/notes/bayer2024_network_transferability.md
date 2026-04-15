# Bayer et al. (2024) — Network Transferability of Adversarial Patches

## Citation

- Title: *Network transferability of adversarial patches in real-time object detection*
- Authors: Jens Becker, Michael Becker, Marko Münch, Michael Arens (Fraunhofer IOSB)
- Venue / Year: SPIE Proceedings 2024 (arXiv preprint August 2024)
- DOI: 10.1117/12.3031501
- arXiv: 2408.15833
- URL: https://arxiv.org/abs/2408.15833
- PDF: `docs/papers/bayer2024_network_transferability_2408.15833.pdf`

## Problem

- What threat model is assumed? Black-box transfer of adversarial patches — patch trained white-box on a source model, then evaluated on target models without gradient access.
- What detector or classifier is attacked? 28 real-time object detection networks across multiple YOLO generations (v7 through v10, including YOLO-NAS and RT-DETR)
- What is the attack goal? Systematically measure which source model properties best predict transferability to unseen target architectures, and identify which target architectures are most/least vulnerable to transfer attacks.

## Method

- Patch type: Standard localized adversarial patch (non-clothing, rectangular)
- Optimization: Gradient-based white-box training on source model; 280 patches total (10 patches × 28 source models)
- Dataset for training: INRIA Person dataset (person class target)
- Dataset for evaluation: INRIA Person test set + COCO test set
- Metric: Relative mAP drop (mAP_clean − mAP_attacked) / mAP_clean; visualized as Patch Compatibility Matrix (28×28 heatmap)
- Color similarity analysis: HSV histogram correlation and Chi-Square + KLD divergence metrics

## Key Findings from PDF

### Architecture Group Transferability (p. 6, Figure 1 + Figure 6 heatmap)

- **Best source models for transfer: larger networks within a family** — YOLOv9 and YOLOv10 architectures produce patches with highest cross-model transferability
- **Worst source models: YOLO-NAS and RT-DETR** — patches trained on these architectures transfer far less to other detectors ("dark horizontal line" in compatibility matrix)
- **YOLOv8-n and YOLOv8-s transfer poorly** — small nano/small models of YOLOv8 produce patches with weaker transfer than YOLOv8-m, -l, -x
- **YOLOv9 and YOLOv10 are most resistant to incoming transfer attacks** — other models' patches cause smallest mAP drops on them
- "The YOLOv7 networks are much more sensitive to the patches compared to the results achieved with the INRIA Person test set" (p. 7)

### Patch Color Analysis (p. 5-6, Figure 5)

- Patch color distributions differ by source architecture — patches trained on YOLOv8-s and YOLOv8-n converge to different HSV profiles than larger YOLOv8 variants
- Color histogram correlation (R_C) and attack success rate (R_S) are inversely proportional — higher visual similarity to surroundings correlates with lower success rate (Table II, unverified-from-pdf for exact numbers beyond Figure 5)

### COCO vs. INRIA

- "The impact on the INRIA Person dataset is by far less low than on the COCO dataset" (p. 7) — patches transfer more reliably on complex multi-class scenes
- Grayscale patches (value 0.5) affect all 28 networks — hypothesized as artifact of mosaic training which uses 0.5-value padding (p. 7)

### Summary Statement (p. 7, Section 6)

"The results indicate that patches that are optimized with larger models have a higher transferability between different models than patches that are optimized with smaller models." — **Supported** (paper's own conclusion, corroborated by heatmap visualization)

## Key Claims

1. **Larger source models → better transfer** across all architecture families tested. **Supported** (compatibility matrix, Figures 1 and 6).

2. **YOLO-NAS and RT-DETR are robustness outliers** — both resistant to attacks from all sources, and produce poorly-transferring patches. **Supported** (heatmap shows dark rows/columns for these groups).

3. **YOLOv8-n and YOLOv8-s produce worse-than-average patches** for transfer purposes. **Supported** (p. 6: "Only the YOLOv8-n and YOLOv8-s networks perform similarly. This block belongs to the YOLO-NAS and RT-DETR architecture groups.").

4. **Cross-architecture transfer generally fails when going from CNN to attention-based (DETR-style) detectors** — consistent with Winter 2026 benchmarking findings. **Supported (Mixed)** — this is for non-patch attacks in Winter; for patches Bayer shows RT-DETR is also an outlier.

5. **Color similarity to reference image is a negative predictor of attack success** — counter-intuitive (naturalistic patches are weaker, not stronger). **Weak** — only shown via correlation analysis, not controlled experiment.

## Threat Model

- White-box training on source detector; black-box transfer to target
- Person class; INRIA Person dataset for training
- Digital evaluation only (no physical testing)
- 28 networks: YOLOv7 (x, w6, e6, d6, e6e), YOLOv8 (n, s, m, l, x), GELAN (c, e), YOLOv9 (c, e), YOLOv10 (n, s, m, b, l, x), YOLO-NAS (s, m, l), RT-DETR (r18, r34, r50, r101)
- Note: YOLOv11 and YOLO26 are NOT in this paper's model set. **Verified-from-pdf (absence).**

## Experimental Setup

- 280 patches (10 per source model × 28 source models)
- INRIA Person (training + primary eval); COCO test set (secondary eval)
- All models use official pretrained COCO weights
- Fraunhofer IOSB affiliation; SPIE 2024 proceedings

## Results

Patch Compatibility Matrix (Figure 6) — key structural findings:
- Bright (high mAP drop) columns = good source models for transfer (YOLOv9, YOLOv10)
- Dark (low mAP drop) rows = robust target models (YOLO-NAS, RT-DETR, YOLOv9/v10)
- YOLOv8-n, YOLOv8-s: darker column than larger YOLOv8 variants — **Supported**
- YOLOv7 models: most sensitive to incoming transfer attacks — **Supported**

Specific numeric mAP drops: available in heatmap but not extracted as discrete table values in pages reviewed — **unverified-from-pdf for exact numbers**.

## Limitations and Failure Modes

- YOLO11 and YOLO26 are absent from the model set (paper published August 2024; YOLO11 released October 2024). Cannot directly cite for v11/v26 behavior. **My inference.**
- Digital-only evaluation — no physical testing or clothing deformation.
- 10 patches per source model may be insufficient for variance-robust conclusions about color analysis (p. 6 acknowledges this implicitly).
- The "YOLOv8-n behaves like RT-DETR group" finding needs validation — it may reflect a quirk of INRIA training rather than a fundamental architectural property. **Speculative.**

## Defensive Takeaways

- If the defend phase uses YOLOv8n as the evaluation model, patches trained on larger YOLOv8 variants will transfer to it more reliably than patches trained on nano models — this is relevant for selecting surrogate models in adversarial training.
- YOLO-NAS architecture appears naturally more robust to transfer attacks — worth investigating whether YOLO11/v26 share any YOLO-NAS-like design features.
- Mixed-architecture adversarial training (using patches from multiple source models) should outperform single-source adversarial training for robustness.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: **Critical**. Paper explicitly evaluates YOLOv8n/s/m/l/x. YOLOv8n (capstone anchor) is identified as one of the weaker source models for transfer. This directly predicts why a patch trained on YOLOv8n will transfer poorly to YOLO11n and especially YOLO26n.
- **YOLO11**: Not in model set, but the paper's finding that newer/larger architectures in the same family are more robust gives a directional prediction. **My inference** — needs verification.
- **YOLO26**: Not in model set. YOLO26's NMS-free design is closer to RT-DETR than to conventional YOLO. If so, it may exhibit RT-DETR-like robustness to transfer attacks (i.e., patches trained on YOLOv8n will transfer very poorly). **Speculative** — needs empirical verification.
- Capstone relevance: **5/5**. This is the primary literature source explaining the cross-version transfer challenge central to the capstone.

## Reproducibility Signals

- 280 patches, 28 models, INRIA Person training dataset — reproducible in principle
- SPIE proceedings format; Fraunhofer IOSB institutional code likely not public
- arXiv preprint available: 2408.15833
- No explicit code release mentioned in pages reviewed — **unverified-from-pdf**

## Open Questions

- What are exact numeric mAP drops for YOLOv8n as source model vs. YOLOv8x?
- How does YOLOv11 fit into this compatibility matrix?
- Does YOLO26's NMS-free design make it analogous to RT-DETR in terms of transfer resistance?
- Would training on YOLOv8l or YOLOv8x (instead of n) significantly improve v8→v11 and v8→v26 transfer rates?

## Normalized Extraction

- Canonical slug: `bayer2024_network_transferability`
- Canonical source record: `docs/papers/bayer2024_network_transferability_2408.15833.pdf`
- Evidence state: `page_cited`
- Threat model: White-box patch training on one source detector with black-box transfer evaluation across 28 target detectors in digital space.
- Detector family and exact version: YOLOv7, YOLOv8, GELAN, YOLOv9, YOLOv10, YOLO-NAS, RT-DETR.
- Attack or defense goal: Quantify cross-model adversarial-patch transferability and identify which source and target architectures dominate the transfer matrix.
- Loss or objective: Standard detector-specific patch optimization on each source model; paper evaluates relative mAP drop rather than proposing a new loss.
- Transforms / EoT: Digital patch placement and detector evaluation on INRIA Person and COCO; physical augmentation is not part of the paper’s core method in the pages reviewed.
- Dataset: INRIA Person train/test and COCO test.
- Metrics: Relative mAP drop; patch compatibility matrix; histogram-based color analyses.
- Strongest quantitative result: Larger YOLOv9 and YOLOv10 source models yield the strongest transfer, while YOLOv8-n and YOLOv8-s cluster with the weakest-transfer groups such as YOLO-NAS and RT-DETR (Figure 6 and Section 5, pp. 6-7).
- Transfer findings: Transfer quality is strongly source-model-size dependent; RT-DETR and YOLO-NAS are robust targets and poor source models; YOLOv8-n and YOLOv8-s are weak transfer sources.
- Physical findings: None. This is a digital-only transfer study.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Direct for YOLOv8; indirect for YOLO11; architectural analogy only for YOLO26 via RT-DETR-like robustness.
- Reproducible technique to borrow: Re-run transfer studies with larger source models rather than only nano variants; use a compatibility-matrix view instead of single transfer pairs.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `cross_yolo_transfer`
- Disposition: `benchmark`
