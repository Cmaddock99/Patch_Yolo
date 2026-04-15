# Wang et al. (2026) — The Chosen-Object Attack

## Citation

- Title: *The Chosen-Object Attack: Exploiting the Hungarian Matching Loss in Detection Transformers for Fun and Profit*
- Authors: Wang, Wang, Wen, Deng, Shu, Cheng, Chen
- Venue / Year: IEEE Transactions on Information Forensics and Security, Vol.21, pp. 2177–2190 (2026)
- URL: https://ieeexplore.ieee.org/document/10879485/
- Access: IEEE Xplore via CSUSM

## Evidence Note

This file is a blocker record, not a synthesis-grade review. There is no local PDF in the repo, so details remain unverified until the full text is available inside the workspace.

## Problem

- What threat model is assumed? White-box attack against detection transformers that use one-to-one assignment instead of NMS.
- What detector or classifier is attacked? DETR-style end-to-end object detectors.
- What is the attack goal? Exploit the Hungarian matching objective directly so the detector selects the wrong assignment outcomes.

## Method

- Patch type: Adversarial attack against detection-transformer assignment dynamics
- Optimization method: Loss-driven optimization targeting the Hungarian matching stage
- Loss terms: Hungarian-matching-aware objective
- Transformations / EoT details: TODO — extract exact augmentation scheme
- Physical-world considerations: Not the primary reason this paper matters for the repo

## Experimental Setup

- Dataset: TODO — extract from full paper
- Target classes: TODO — extract from full paper
- Model versions: DETR-style detectors
- Metrics: AP / attack success metrics

## Results

- Main quantitative result: TODO — extract the main AP drop / attack-success table from the full text
- What worked best: Targeting the Hungarian matching loss directly rather than using an NMS-era detector loss
- What failed or stayed weak: TODO — identify transfer limits and architecture assumptions

## Relevance to My Capstone

- Direct relevance to YOLOv8: Low — v8 still fits the older NMS/objectness-centric framing
- Direct relevance to YOLO11: Low to moderate
- Direct relevance to YOLO26: **HIGH** — this is the closest integrated paper to YOLO26's end-to-end matching behavior
- What I can reproduce: The loss-design ideas for a YOLO26-specific attack objective
- What I can cite: Architectural explanation for why YOLO26 may require a different loss than v8/v11-era patch attacks

## Open Questions

- Does this transfer across YOLO versions? Not directly; it is mainly a YOLO26-style architecture citation
- Is the patch digital only, or physically tested? TODO — confirm
- Is the code available? TODO
- What is missing for my project? Exact loss formulation and ablation numbers

## TODO

- [ ] Pull the full IEEE text and extract the Hungarian-matching loss details
- [ ] Record the main quantitative results and baseline comparisons
- [ ] Compare the loss design against YOLO26's one-to-many / one-to-one outputs

## Normalized Extraction

- Canonical slug: `wang2026_chosen_object`
- Canonical source record: `IEEE Xplore entry only; no local PDF in repo`
- Evidence state: `blocked_access`
- Threat model: White-box attack on end-to-end detection transformers that use Hungarian matching.
- Detector family and exact version: DETR-style end-to-end detectors; no verified YOLO-family evaluation in the local repo.
- Attack or defense goal: Use the matching objective itself as the attack surface instead of legacy NMS-era losses.
- Loss or objective: Hungarian-matching-aware objective, exact formulation blocked.
- Transforms / EoT: Unknown until full text is available.
- Dataset: Unknown until full text is available.
- Metrics: Unknown until full text is available.
- Strongest quantitative result: Unknown; current repo only relies on the architectural premise, not benchmark numbers.
- Transfer findings: Unknown.
- Physical findings: Unknown.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Architectural interest is high only for YOLO26-style end-to-end matching.
- Reproducible technique to borrow: None can be promoted until the exact loss and ablations are read.
- Citation strength: `blocked_access`

## Working Packet Status

- Primary repo question: `yolo26_architecture_mismatch`
- Repo currently relies on this for: Hungarian-matching attack framing for why YOLO26 may need a different loss from v8/v11.
- Exact missing detail preventing promotion: Exact loss formulation, datasets, ablations, and benchmark tables.
- Blocker type: `architectural`
- Promotion rule: Do not promote any quantitative or method-specific claim until a local full-text source is added.
