# Paper Review: Wu et al. (2024) — NAPGuard

## Citation

- Title: NAPGuard: Towards Detecting Naturalistic Adversarial Patches
- Authors: Siyang Wu, Jiakai Wang, Jiejie Zhao, Yazhe Wang, Xianglong Liu
- Venue / Year: CVPR 2024, pp. 24367–24376
- URL: https://openaccess.thecvf.com/content/CVPR2024/html/Wu_NAPGuard_Towards_Detecting_Naturalistic_Adversarial_Patches_CVPR_2024_paper.html
- PDF: ../papers/wu2024_NAPGuard_CVPR.pdf

## Problem

- What threat model is assumed? Defense paper — detects naturalistic adversarial patches (NAPs) that are designed to look realistic (GAN or diffusion-generated). Prior patch detectors focused on noisy, obviously artificial patches and fail on NAPs.
- What detector or classifier is attacked/defended? General object detectors. Benchmarks against Ad-YOLO, APE, SAC, PatchZero as baseline defenses.
- What is the attack goal (from attacker side)? NAPs evade both detectors and patch-detection systems by appearing visually natural while suppressing object detections.

## Method (Defense)

- NAPGuard uses a **critical feature modulation** framework with two components:
  1. **Aggressive Feature Aligned Learning**: During training, a pattern alignment loss captures accurate "aggressive" (adversarial) feature patterns by aligning features from patched and clean images. Improves detection precision.
  2. **Natural Feature Suppressed Inference**: A feature shield module universally mitigates disturbances from diverse NAP visual representations during inference. Enhances generalization across unseen patch styles.
- Core insight: NAPs are simultaneously "aggressive" (disrupt detections) and "natural" (look realistic). Prior methods fail by treating these as conflicting signals; NAPGuard separates them.

## Experimental Setup

- Dataset: Naturalistic adversarial patches from multiple generation methods (GAN-based, diffusion-based)
- Baselines compared: Ad-YOLO, APE, SAC, PatchZero
- Metrics: AP@0.5 for patch detection

## Results

- NAPGuard **improves average AP@0.5 by 60.24%** over state-of-the-art methods for detecting naturalistic patches.
- Demonstrates strong generalization: the Natural Feature Suppressed Inference module handles diverse NAP appearances unseen during training.

## Relevance to My Capstone

- Direct relevance to YOLOv8: Moderate — relevant if the capstone includes a defenses section or discusses how the adversarial patches could be detected.
- Direct relevance to YOLO11/YOLO26: Same as above.
- What I can reproduce: CVPR 2024 open access code likely available.
- What I can cite: For the defenses/countermeasures section of the capstone. Establishes that GAN/diffusion patches (like those in Gala et al. / Hu et al.) can be detected with a dedicated defense. If your capstone asks "how could this be stopped?", this is the citation.

## Open Questions

- Does NAPGuard work against patches on Ultralytics YOLO models specifically? Unknown from the abstract.
- What YOLO versions are targeted? Not specified from available content.
- Is the code available? Yes — CVPR 2024 open access.
- What is missing for my project? This is a defense paper. Only relevant for the "defenses" or "countermeasures" section.
