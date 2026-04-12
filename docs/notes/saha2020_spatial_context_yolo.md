# Paper Review: Saha et al. — Role of Spatial Context in Adversarial Robustness for Object Detection

## Citation

- Title: Role of Spatial Context in Adversarial Robustness for Object Detection
- Authors: Aniruddha Saha, Akshayvarun Subramanya, Koninika Patil, Hamed Pirsiavash
- Venue / Year: CVPR Workshop (CVPRW) 2020
- DOI: 10.1109/CVPRW50498.2020.00400
- arXiv: 1910.00068
- URL: https://arxiv.org/abs/1910.00068
- PDF: `docs/papers/saha2020_spatial_context_adversarial_1910.00068.pdf`
- Citations: ~60

## Problem

- What threat model is assumed? Adversary places a patch anywhere in a scene (does NOT need to overlap the target person); exploits contextual reasoning of single-pass detectors
- What detector is attacked? YOLO (primary), exploiting contextual single-pass inference
- What is the attack goal? Make YOLO "blind" to a chosen object category using a patch placed anywhere in the image (not on the target)

## Method

- Patch type: Context-aware adversarial patch (placed in background/environment, not on the target object)
- Key insight: Single-pass detectors like YOLO use contextual information from the entire image for predictions. A patch in one part of the image can suppress detections in a completely different part.
- Optimization method: Category-specific patch that exploits the spatial context used by YOLO's global receptive field
- Defense improvement: Shows that reducing contextual reasoning during training improves robustness to context-based patches

## Experimental Setup

- Dataset: PASCAL VOC / COCO
- Target classes: Any category (shown for persons, cars)
- Model versions: YOLO (original paper focus)
- Metrics: AP drop with context patch; defense: AP recovery

## Results

- Main quantitative result: A single background patch can suppress a full category in YOLO; limiting context during training partially mitigates this
- 60 citations — well-established result
- Key finding: YOLO's global context, which makes it fast, also makes it vulnerable to scene-level patches

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — YOLOv8 still has a global receptive field; this vulnerability likely persists
- Direct relevance to YOLO11: Moderate
- Direct relevance to YOLO26: Lower — YOLO26's transformer architecture processes global context differently; the contextual exploit may be weaker or differently structured
- What I can cite: Scene-level contextual attack as an alternative to wearable patches; threat model framing section
- What I can reproduce: Could test a context patch (placed on wall/floor in your test images) — quick ablation experiment

## Open Questions

- Does contextual vulnerability persist in YOLOv8/11/26?
- Is code available?
- How does it compare to DPatch/Thys for magnitude of AP drop?
