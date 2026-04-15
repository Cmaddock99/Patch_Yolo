# Lovisotto et al. (2022) — Give Me Your Attention

## Citation

- Title: *Give Me Your Attention: Dot-Product Attention Considered Harmful for Adversarial Patch Robustness*
- Authors: Giulio Lovisotto, Nicole Finnie, Mauricio Munoz, Chaitanya K. Mummadi, Jan Hendrik Metzen
- Venue / Year: CVPR 2022, pp. 15213–15222
- URL: https://openaccess.thecvf.com/content/CVPR2022/html/Lovisotto_Give_Me_Your_Attention_Dot-Product_Attention_Considered_Harmful_for_Adversarial_CVPR_2022_paper.html
- PDF: `docs/papers/lovisotto2022_attention_patch_robustness_CVPR.pdf`

## Problem

- What threat model is assumed? White-box adversarial patch attack against vision transformers and hybrid CNN-transformer architectures.
- What detector or classifier is attacked? ViT, DeiT, and hybrid architectures; detection and classification.
- What is the attack goal? Understand why dot-product self-attention changes the adversarial patch vulnerability surface relative to pure CNNs.

## Method

- Patch type: Standard adversarial patch (printable, localized region)
- Optimization method: PGD-based patch optimization
- Loss terms: Classification/detection loss
- Key finding: Dot-product attention creates a fundamentally different gradient landscape — attention heads can be manipulated to spread patch influence across the entire image far more effectively than in convolutional models.
- Physical-world considerations: Not the focus; primarily a theoretical/empirical analysis of the attention vulnerability surface.

## Experimental Setup

- Dataset: ImageNet, COCO
- Target classes: Multiple
- Model versions: ViT, DeiT, hybrid CNN-ViT models
- Metrics: Attack success rate, patch influence spread

## Results

- Main quantitative result: Attention-Fool patches covering only 0.5% of the input can drive ViT robust accuracy to 0% and reduce DETR mAP to below 3%.
- What worked best: Patches that explicitly target attention weight manipulation outperform naive CNN-style patches against transformers.
- What failed or stayed weak: Directly porting CNN-optimized patches to transformer models — the gradient landscape is fundamentally different.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Low — v8 is conv-based.
- Direct relevance to YOLO11: Low — v11 is primarily conv-based.
- Direct relevance to YOLO26: **HIGH** — YOLO26 incorporates attention mechanisms. This paper explains why standard gradient-ascent patches (designed for conv outputs like (B,84,8400)) may not optimize effectively against YOLO26's attention layers. The gradient landscape through `preds["one2many"]["scores"]` in YOLO26 will be shaped by attention, not just conv filters.
- What I can cite: Explanation for why v8-trained patches transfer poorly to v26 (attention architecture difference). Motivation for why YOLO26 requires a different optimization approach.

## Open Questions

- Does this transfer across YOLO versions? This paper explains WHY it doesn't.
- Is the patch digital only, or physically tested? Digital analysis primarily.
- Is the code available? Yes — CVF supplemental.
- What is missing for my project? Needs adaptation to object detection specifically (paper focuses on classification). YOLO26-specific attention analysis not done.

## TODO

- [ ] Read Section 4 (attention vulnerability analysis) carefully
- [ ] Check if their attack formulation applies to YOLO26's one2many attention scores

## Normalized Extraction

- Canonical slug: `lovisotto2022_attention_patch`
- Canonical source record: `docs/papers/lovisotto2022_attention_patch_robustness_CVPR.pdf`
- Evidence state: `page_cited`
- Threat model: White-box localized adversarial patch attack against dot-product attention models.
- Detector family and exact version: ViT, DeiT, and DETR-family attention models.
- Attack or defense goal: Explain and exploit the vulnerability of dot-product attention to small adversarial patches.
- Loss or objective: Attention-Fool losses that optimize pre-softmax query-key dot-product similarity to redirect attention toward the patch.
- Transforms / EoT: Fixed-location patch optimization with PGD; physical robustness is not the focus.
- Dataset: ImageNet and MS COCO.
- Metrics: Robust accuracy for classification and mAP for detection.
- Strongest quantitative result: A patch covering 0.5% of the image drives ViT robust accuracy to 0% and reduces DETR mAP below 3% (abstract, p. 1).
- Transfer findings: CNN-style patch objectives underuse the attention-weight channel and are suboptimal on transformers; attention-aware objectives are required.
- Physical findings: None. The paper is a digital robustness and mechanism study.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Direct mechanism reference for YOLO26-style attention reasoning; low direct value for YOLOv8 and YOLO11.
- Reproducible technique to borrow: Optimize pre-softmax attention similarities rather than only end-task detector loss when attacking attention-based detectors.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Disposition: `architecture_explanation`
