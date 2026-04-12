# Paper Review: Tereshonok et al. — Anomaly Localization Defense for Pedestrian Detectors

## Citation

- Title: Increasing Neural-Based Pedestrian Detectors' Robustness to Adversarial Patch Attacks Using Anomaly Localization
- Authors: Maxim Tereshonok, O. Ilina, V. Ziyadinov
- Venue / Year: Journal of Imaging (MDPI), 2025
- DOI: 10.3390/jimaging11010026
- URL: https://doi.org/10.3390/jimaging11010026
- PDF: https://www.mdpi.com/2313-433X/11/1/26/pdf?version=1737095625

## Problem

- What threat model is assumed? Adversary places a patch that causes pedestrian detectors to miss persons
- What detector is defended? Neural-network pedestrian detectors (YOLO family)
- What is the defense goal? Reconstruct a clean image from an adversarial input using anomaly localization, then run the original detector on the clean image

## Method

- Approach: Two-stage defense — (1) Deep CNN to localize the anomalous (adversarial) region in the image, (2) Reconstruct a benign image by inpainting over the detected region
- Architecture: Similar paradigm to SAC (Segment-and-Complete), but using anomaly detection rather than explicit segmentation
- Physical-world considerations: Tested against printed physical patches

## Experimental Setup

- Dataset: Pedestrian detection datasets
- Target classes: Pedestrian / person
- Model versions: YOLO-family detectors
- Metrics: Detection AP before/after defense; ASR reduction

## Results

- Main quantitative result: TODO — need full paper read; 2 citations, recent
- Defense approach: "Reconstruction from adversarial" — architecturally between NAPGuard (detect pixels) and SAC (segment+complete)

## Relevance to My Capstone

- Direct relevance to YOLOv8: Relevant for defenses section
- Direct relevance to YOLO11: Applicable
- Direct relevance to YOLO26: Applicable
- What I can cite: Defense paradigm 5 (anomaly reconstruction) as distinct from Ad-YOLO (patch class), NAPGuard (semantic detection), SAC (inpainting), PatchZero (zeroing)
- Open access PDF available

## Open Questions

- What are the quantitative ASR reduction numbers?
- How does it compare to SAC and NAPGuard?
- Is code available?
- TODO: download PDF and read for numbers
