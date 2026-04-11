# Wang et al. (2026) — The Chosen-Object Attack

## Citation

- Title: *The Chosen-Object Attack: Exploiting the Hungarian Matching Loss in Detection Transformers for Fun and Profit*
- Authors: Wang, Wang, Wen, Deng, Shu, Cheng, Chen
- Venue / Year: IEEE Transactions on Information Forensics and Security, Vol.21, pp. 2177–2190 (2026)
- URL: https://ieeexplore.ieee.org/document/10879485/
- Access: IEEE Xplore via CSUSM

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
