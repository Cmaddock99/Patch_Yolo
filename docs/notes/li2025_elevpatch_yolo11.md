# Li et al. (2025) — ElevPatch: YOLO11-Specific Adversarial Patch

## Citation

- Title: *ElevPatch: An Adversarial Patch Attack Scheme Based on YOLO11 Object Detector*
- Authors: Li, Liao, Li, Zhang, Wu, Jiayan
- Venue / Year: ICIC 2025 — Advanced Intelligent Computing Technology and Applications, pp. 176–188
- DOI: 10.1007/978-981-96-9872-1_15
- URL: https://link.springer.com/chapter/10.1007/978-981-96-9872-1_15
- Access: Springer — ILL request needed via CSUSM

## Evidence Note

This file is a blocker record, not a synthesis-grade review. There is no local PDF in the repo, so method and benchmark claims remain blocked.

## Problem

- What threat model is assumed? White-box adversarial patch attack against YOLO11 specifically.
- What detector or classifier is attacked? YOLO11 (Ultralytics)
- What is the attack goal? Person detection evasion against YOLO11.

## Method

- Patch type: Adversarial patch (localized)
- Optimization method: Gradient-based against YOLO11 inner model (likely similar approach to this project)
- Loss terms: Detection suppression — details pending full paper read
- Transformations / EoT details: Unknown — needs full read
- Physical-world considerations: Unknown — needs full read

## Experimental Setup

- Dataset: Unknown — needs full read
- Target classes: Person (assumed based on venue context)
- Model versions: YOLO11
- Metrics: Detection suppression % or mAP drop

## Results

- Main quantitative result: **UNKNOWN — needs institutional access**
- This is the only paper found targeting YOLO11 specifically. The numbers here are the primary comparison point for your 78.8% YOLO11 suppression result.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Indirect.
- Direct relevance to YOLO11: **CRITICAL** — this is the only benchmark paper specifically for YOLO11. Whatever suppression % they report is the number to beat or match in your write-up.
- Direct relevance to YOLO26: Indirect.
- What I can cite: Once obtained, this is the primary literature comparison for your YOLO11 result.

## Open Questions

- What is their YOLO11 suppression rate? This is the key question.
- Is the patch digital only, or physically tested?
- Is the code available?
- How does their training setup compare to yours (epochs, patch size, EoT)?

## TODO

- [ ] Submit ILL request via CSUSM library for this Springer chapter
- [ ] Once received: fill in Results section above
- [ ] Compare their YOLO11 result to your 78.8% suppression
- [ ] Check if their training hyperparameters match yours (patch size 100, 1000 epochs, lr 0.01)

## Normalized Extraction

- Canonical slug: `li2025_elevpatch`
- Canonical source record: `Springer chapter entry only; no local PDF in repo`
- Evidence state: `blocked_access`
- Threat model: YOLO11-targeted adversarial patch attack, inferred from the chapter title and note history.
- Detector family and exact version: YOLO11.
- Attack or defense goal: Provide the only currently known YOLO11-specific patch benchmark in the repo literature.
- Loss or objective: Unknown until full text is available.
- Transforms / EoT: Unknown until full text is available.
- Dataset: Unknown until full text is available.
- Metrics: Unknown until full text is available.
- Strongest quantitative result: Unknown; this is the main missing YOLO11 benchmark.
- Transfer findings: Unknown.
- Physical findings: Unknown.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: High only for YOLO11 benchmarking.
- Reproducible technique to borrow: None can be promoted until the chapter is available locally.
- Citation strength: `blocked_access`

## Working Packet Status

- Primary repo question: `yolo11_coverage`
- Repo currently relies on this for: The existence of a YOLO11-specific literature comparison point.
- Exact missing detail preventing promotion: YOLO11 suppression numbers, dataset, EoT details, and whether evaluation is digital or physical.
- Blocker type: `quantitative`
- Promotion rule: Do not cite this as a benchmark beyond existence until the chapter is locally available.
