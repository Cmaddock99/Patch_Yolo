# Paper Review: Schack et al. (2024) — Breaking the Illusion

## Citation

- Title: Breaking the Illusion: Real-world Challenges for Adversarial Patches in Object Detection
- Authors: Jakob Schack, Katarina Petrovic, Olga Saukh (Graz University of Technology; Complexity Science Hub Vienna)
- Venue / Year: EMERGE 2024 Workshop (Enabling Machine Learning Operations for next-Gen Embedded Wireless Networked Devices); arXiv:2410.19863
- URL: https://arxiv.org/html/2410.19863v2
- PDF: ../papers/schack2024_real_world_challenges_2410.19863.pdf

## Problem

- What threat model is assumed? Evaluation study (not a new attack) — pre-trained adversarial patches are tested under varying real-world conditions.
- What detector or classifier is attacked? YOLOv3 (global patches), YOLOv5 (local patches).
- What is the attack goal? Understand the discrepancy between digital patch performance and physical-world effectiveness. Why do digitally-effective patches often fail when printed and deployed?

## Method

- Patch type: Two patch types tested: (1) **global patches** (suppress all detections across a scene), (2) **local patches** (suppress detection of a specific object).
- Optimization method: Patches from Lee & Kolter (2019) and Shrestha et al. (2023) — not new patch training, but systematic physical testing of existing patches.
- Loss terms: N/A (evaluation study).
- Transformations / EoT details (physical conditions tested):
  - Geometric: patch size (10–30% of image width for global; 4–16cm for local), rotation (±90° around X/Y/Z axes), position/distance variation
  - Color/lighting: brightness (4–61 lux), hue changes (0–360°)
  - Information reduction: low-pass filtering, color palette reduction
- Physical-world considerations: Controlled indoor lab environment. Two cameras: Microsoft LifeCam HD-3000 (720p) and Ausdom AF640 (1080p). Objects tested: bottle, cup, plant, tennis racket, spoon, person image.

## Experimental Setup

- Dataset: Controlled lab scenes
- Target classes: Multiple (bottle, cup, plant, tennis racket, spoon, person)
- Model versions: YOLOv3 (global), YOLOv5 (local)
- Metrics: mAP (global patches), detection confidence (local patches)

## Results

**Global Patch (YOLOv3):**
- Rotation > 20° (Z-axis) causes significant effectiveness drop
- Larger patches (30% of image) substantially outperform smaller ones (12%)
- Brightness increase: up to 64% performance discrepancy between physical and digital domain
- Hue transformation 200–300°: renders patches ineffective in physical world

**Local Patch (YOLOv5):**
- Effective within ±30° rotation across all axes
- Detection confidence reduced to near 0 for several objects at standard brightness
- Size dependency mirrors global patch behavior

**Key Finding:** Substantial gaps exist between physical and digital patch performance despite using neural network-based parameter matching. The digital-to-physical gap is the main reliability concern.

## Relevance to My Capstone

- Direct relevance to YOLOv8: High — if extending to physical-world evaluation, these findings set realistic expectations for what will work.
- Direct relevance to YOLO11: Same — use these findings to bound claims about physical robustness.
- Direct relevance to YOLO26: Same — particularly relevant since YOLO26's NMS-free detection is newer and may behave differently under physical degradation.
- What I can reproduce: The systematic variation of patch size, rotation, and lighting conditions is a clean evaluation framework I can apply to my own patches.
- What I can cite: For the physical-digital performance gap argument; for the rotation/size sensitivity findings.

## Open Questions

- Does this transfer across YOLO versions? Study only tests YOLOv3 and v5. Whether the same degradation patterns apply to v8/v11/v26 is an open question.
- Is the patch digital only, or physically tested? Physically tested in a controlled lab environment.
- Is the code available? Not released (evaluation study).
- What is missing for my project? Focuses on pre-trained patches — does not evaluate how incorporating physical augmentations during training changes robustness. Person-vanishing attack not the focus.
