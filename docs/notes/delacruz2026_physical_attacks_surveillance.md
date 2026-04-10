# Paper Review: DelaCruz et al. (2026) — Physical Adversarial Attacks on AI Surveillance Systems

## Citation

- Title: Physical Adversarial Attacks on AI Surveillance Systems: Detection, Tracking, and Visible–Infrared Evasion
- Authors: Miguel A. DelaCruz, Patricia Mae Santos, Rafael T. Navarro
- Venue / Year: arXiv:2604.06865, submitted April 8, 2026
- URL: https://arxiv.org/abs/2604.06865
- PDF: ../papers/delacruz2026_physical_attacks_surveillance_2604.06865.pdf

## Problem

- What threat model is assumed? Survey paper — reviews physical adversarial attacks on deployed surveillance systems (not just single-frame image classifiers/detectors). Covers multi-frame video, multi-modal (RGB + thermal), and system-level attack pipelines.
- What detector or classifier is attacked? Surveyed systems include YOLO-based surveillance pipelines, multi-object trackers, and visible-infrared dual-modal sensors.
- What is the attack goal (of surveyed attacks)? Evasion of surveillance infrastructure across: (1) temporal persistence (multiple video frames), (2) multi-object tracking pipelines, (3) both visible and infrared sensing simultaneously, and (4) physically realistic wearable implementations.

## Method (Survey Dimensions)

The paper organizes physical adversarial attack research through four critical dimensions:

1. **Temporal Persistence**: Attacks that maintain evasion across video frame sequences, not just isolated frames. Notes that per-frame benchmarks are insufficient for evaluating surveillance robustness.
2. **Sensing Modality**: Addresses both RGB and thermal (infrared) imaging. Attacks that fool only one modality may be detected by the other in dual-modal systems.
3. **Carrier Realism**: Distinguishes laboratory-printed patches from practical wearable implementations (clothing, accessories). Examines how carrier material and form factor affect attack effectiveness.
4. **System-Level Objectives**: Evaluates attacks within full surveillance pipelines — including detection, tracking, and re-identification components — not just the detector in isolation.

**Key claim**: "Surveillance robustness cannot be judged reliably from isolated per-frame benchmarks alone; it has to be examined as a system problem unfolding over time, across sensors, and under realistic physical deployment constraints."

## Relevance to My Capstone

- Direct relevance to YOLOv8: High for framing — if my capstone uses YOLO as part of a person-detection pipeline (as in a surveillance scenario), this paper's system-level framing is directly applicable.
- Direct relevance to YOLO11/YOLO26: Same framing. YOLO26's NMS-free design may also change tracking pipeline integration behavior.
- What I can reproduce: Survey paper — no implementation to reproduce, but the four dimensions provide a structured evaluation framework I can apply to my experiments.
- What I can cite: For the surveillance threat model motivation (why person-vanishing patches matter beyond academic benchmarks); for positioning my capstone's physical-world evaluation within a system-level framing; for the temporal persistence angle if I test on video.

## Open Questions

- What specific YOLO versions are covered in depth? Likely YOLOv5/v7 based on the 2026 submission; check PDF for specifics.
- Does it cover YOLO11 or YOLO26? Unlikely (too new), but check the PDF.
- Is there original experimental work or is it purely a survey? Check PDF — the abstract suggests a review paper.
- What is missing for my project? This is a survey, not a new attack. Specific per-model attack numbers not available from the abstract alone.
