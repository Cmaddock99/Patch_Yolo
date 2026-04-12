# Paper Review: TOG — Targeted Attack for Object Detection via Objectness Gradient

## Citation

- Title: Targeted Attack for Deep Hashing based Retrieval (TOG variant — see note)
- Authors: Bae, Lee, Han, and Ahn (2020)
- Venue / Year: ~2020
- URL: TODO — pending full citation verification via Semantic Scholar

⚠️ **Verification note**: The "TOG" acronym and Bae 2020 attribution were flagged as *pending confirmation* during batch 4 ingestion. Verify the exact paper title and DOI before citing. The core concept (targeted objectness gradient attack flooding NMS) is confirmed as a known technique; the citation details need checking.

## Problem

- What threat model is assumed? White-box access to detector; attacker can place a patch on or near the target
- What detector is attacked? NMS-based detectors (YOLOv3 / Faster R-CNN)
- What is the attack goal? Flood NMS with false high-confidence detections to suppress real detections (objectness maximization attack)

## Method

- Patch type: Adversarial patch placed near target
- Optimization method: Gradient ascent on objectness scores across anchor grid
- Loss terms: Maximize objectness for all anchor boxes in a region to create "ghost detections" that flood NMS
- Key insight: NMS can be weaponized — if you create many high-score false positives they suppress real detections via IoU thresholding

## Experimental Setup

- Dataset: COCO / VOC persons
- Target classes: Person
- Model versions: YOLOv3 / Faster R-CNN
- Metrics: ASR, AP drop

## Results

- Main quantitative result: TODO — read full paper
- What worked best: The objectness-flooding approach is architecturally different from class-score suppression approaches (Thys, DAP)
- Architectural note: This NMS-flooding mechanism does NOT apply to YOLO26 which uses end-to-end Hungarian matching instead of NMS

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — YOLOv8 uses NMS; objectness-flooding is an alternative loss design
- Direct relevance to YOLO11: Moderate — same NMS pipeline as v8
- Direct relevance to YOLO26: Low / architectural mismatch — YOLO26 has no NMS to flood; cite only as contrast
- What I can cite: NMS-specific attack mechanism; contrast with your end-to-end Hungarian matching target for v26
- What I can reproduce: Could substitute TOG loss for your class-suppression loss in v8 experiments as ablation

## Open Questions

- Confirm exact citation / DOI before citing
- Is code available?
- How does objectness-flooding compare to class-score suppression quantitatively on same dataset?
