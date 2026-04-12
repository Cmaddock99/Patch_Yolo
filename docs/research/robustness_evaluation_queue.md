# Robustness Evaluation Queue

Generated: 2026-04-11  
Scope: Safe, bounded next steps grounded in PDF corpus evidence.  
All items are framed as measurement and evaluation tasks — not as improvements to attack evasion.

---

## Framing Principles

Every item below answers three questions:
1. What to measure
2. Why the literature supports measuring it
3. What it contributes to the defend or fortify phases of the capstone

Nothing in this queue is intended to improve the patch's evasion capability beyond establishing a reproducible baseline. All items feed into understanding the threat model and evaluating defensive responses.

---

## Category 1: Cross-Version Transfer Baselines

### Item 1.1: Systematic v8n → v11n → v26n Transfer Evaluation

**What to measure:** Patch trained on YOLOv8n (white-box) evaluated on YOLOv8n (white-box baseline), YOLOv11n (black-box), and YOLO26n (black-box). Report AP@0.5 and recall at IoU=0.5 for person class on INRIA Person test set.

**Literature support:** AdvReal (huang2025) provides the best prior art — v2→v8 recall=32.68%, v2→v11 recall=32.47%. Bayer 2024 shows v8n is a weak source model. This measurement will determine if v8n→v11n/v26n transfer is meaningful and whether the capstone patch functions as a stable multi-version artifact.

**Contribution to defend/fortify:** Establishes the baseline transfer rates that defense must account for. If v8n→v26n transfer is near zero, the defend phase can prioritize v8n-targeted defenses without worrying about YOLO26 attack transferability.

**Safety note:** This is evaluation-only — measuring existing patch effectiveness against existing models. No new optimization involved.

---

### Item 1.2: Patch Compatibility Replication (Bayer 2024 Protocol, Subset)

**What to measure:** Replicate Bayer 2024's patch compatibility matrix for the subset: YOLOv8n, YOLOv8x, YOLOv11n, YOLO26n. Train one patch per source model (4 patches), evaluate each on all 4 targets (16 cells). Report relative mAP drop. Use INRIA Person as training/eval dataset.

**Literature support:** Bayer 2024 (p. 6) identifies YOLOv8n as a weak source model consistent with YOLOv8-n and YOLOv8-s cluster. Whether v8x substantially improves v8→v26 transfer is a direct empirical question this measurement can answer.

**Contribution to defend/fortify:** If v8x-trained patches transfer better to v11/v26 than v8n-trained patches, the defend phase should test against v8x patches, not just v8n. Identifies the most dangerous (highest-transfer) attack configuration.

---

### Item 1.3: Self-Ensemble Training Effect on Transfer (T-SEA Protocol)

**What to measure:** Compare transfer rates (v8n→v11n, v8n→v26n) for: (a) baseline v8n patch, (b) v8n patch trained with ShakeDrop regularization, (c) v8n patch trained with patch cutout augmentation, (d) v8n patch trained with both. All patches trained to identical digital suppression on v8n, then evaluated on v11n and v26n.

**Literature support:** T-SEA (huang2022) demonstrates ShakeDrop + patch cutout improve black-box average mAP from 36.46% → 9.16% on 7 detectors. DePatch (cheng2024) independently validates segment-erasing (patch cutout) for physical robustness. Both suggest these augmentations improve generalization of the adversarial signal beyond the source model's gradient landscape.

**Contribution to defend/fortify:** Identifies which training augmentations create the most transferable patches. This characterizes the threat the defend phase must address — if ShakeDrop-trained patches are 3x better at transfer, defenses must be evaluated against that configuration.

---

## Category 2: Physical Plausibility Measurement

### Item 2.1: Digital-Physical Gap Benchmarking (Schack 2024 Protocol)

**What to measure:** Evaluate capstone patch under controlled simulated physical conditions on YOLOv8n: (a) patch rotation ±90° in 10° increments around Z axis, (b) brightness variation 4–61 lux via gamma adjustment, (c) size reduction to 10%, 15%, 20%, 25%, 30% of image width, (d) hue shift 0–360° in 30° increments.

Report: AP@0.5 and recall vs. clean baseline at each condition.

**Literature support:** Schack 2024 (p. 4-5) systematically identifies these as the conditions causing the largest digital-physical gap. Rotation >20° Z-axis and hue shifts of 200-300° cause the most significant effectiveness loss. This measurement directly quantifies how robust the capstone patch is under known degradation modes.

**Contribution to fortify phase:** Maps the patch's robustness boundary. Any fortification strategy (EoT augmentation during training, adversarial training with perturbed images) can be evaluated against this benchmark. Post-fortification, rerun this measurement to quantify improvement.

---

### Item 2.2: EoT Transformation Coverage Audit

**What to measure:** For the EoT transformations currently used in patch training, verify that they cover the physical degradation modes documented in the literature: (a) rotation range ≥ ±20° (Schack), (b) brightness variation matching 4-61 lux range (Schack), (c) TPS or block-masking for partial occlusion (DePatch), (d) color jitter covering printable gamut (NPS loss — Thys, DePatch).

Report: Which physical degradation modes are and are not currently covered by the training augmentations.

**Literature support:** EoT (Brown 2017) is the standard framework; Thys 2019 applies it to person detection; DePatch adds block-masking; AdvReal adds relighting matching. The completeness of EoT coverage directly predicts physical-digital gap size.

**Contribution to fortify phase:** Documents which physical conditions the capstone patch is not robust to, guiding fortification priorities.

---

## Category 3: Defense Baselines

### Item 3.1: Ad-YOLO Patch Class Adaptation to YOLOv8n

**What to measure:** Add a "adversarial_patch" class (index 80) to YOLOv8n YAML configuration. Generate patch-annotated training images (apply capstone patch over INRIA Person images; annotate patch location as class 80 bounding box). Fine-tune YOLOv8n for N epochs. Measure: (a) clean person AP before/after, (b) person AP under patch attack before/after.

**Literature support:** Ji 2021 (Ad-YOLO) demonstrates 80.31% AP under white-box attack vs. 33.93% baseline on YOLOv2; −1.45 pp clean cost. This is the strongest defense result in the PDF corpus. The architecture change (adding one class to YOLO head) is minimal and directly applicable to YOLOv8n via Ultralytics YAML config.

**Contribution to defend phase:** Establishes whether the patch class approach replicates on modern YOLO. If ji2021's results hold (expected ~46% AP recovery under attack; ~1-2 pp clean cost), this becomes the primary defense baseline for the capstone.

**Safety note:** The defense makes the detector more reliable, not the attack more effective.

---

### Item 3.2: Adversarial Training Baseline (Standard)

**What to measure:** Fine-tune YOLOv8n on a mix of clean INRIA images and patched INRIA images (patch applied to 50% of training examples). Compare: (a) clean AP, (b) AP under seen patch, (c) AP under unseen patch (different patch generated independently). Compare to Ad-YOLO patch class approach.

**Literature support:** Ji 2021 Table 4 shows adversarial training (Model₁-₃) achieves 58-62% AP under white-box attack — substantially worse than Ad-YOLO (80.31%). Winter 2026 shows mixed-attack adversarial training outperforms single-attack training for digital non-patch attacks. Testing both single-patch and multi-patch adversarial training establishes which is necessary.

**Contribution to defend phase:** Establishes adversarial training as a secondary defense. Confirms or refutes Ji 2021's finding that patch-class detection outperforms adversarial training.

---

### Item 3.3: NAPGuard-Style Frequency Detection Baseline

**What to measure:** Test whether the capstone patch exhibits frequency domain anomalies detectable by a simple high-pass filter or frequency histogram comparison. Compare patch pixels' FFT spectrum to clean image spectrum. Report if frequency anomaly is detectable without a trained model.

**Literature support:** Lu 2022 (FRAN) shows adversarial patches have anomalous frequency characteristics relative to natural images. Wu 2024 (NAPGuard) builds on this for naturalistic patches. A simple frequency audit determines whether the capstone patch would be flagged by basic frequency-domain defenses.

**Contribution to fortify phase:** If the patch has large high-frequency components, simple frequency filtering partially destroys it. Alternatively, this informs whether a NAPGuard-style detector would flag the patch. Useful for characterizing what the fortify phase needs to withstand.

---

## Category 4: Benchmark Replication

### Item 4.1: INRIA Person Evaluation Protocol Standardization

**What to measure:** Establish a standard evaluation protocol for all capstone measurements using INRIA Person test set (288 images) with the following metrics: AP@IoU=0.5 (person class), Recall@0.4 confidence threshold (for comparison with Thys 2019), ASR (% images where person confidence < 0.5 after patch applied), and F1-score at IoU=0.5.

**Literature support:** INRIA Person is used as the evaluation dataset in: thys2019, wu2020, cheng2024, huang2022_tsea, bayer2024, huang2025_advreal. Using INRIA as the common benchmark enables direct numeric comparison with published results. Thys 2019 uses recall@0.4 threshold; AdvReal uses IoU@0.5 with confidence threshold; DePatch uses AP@0.5.

**Contribution to all phases:** Standardized metrics enable published result comparison. If capstone v8n achieves DePatch-level AP suppression (17.75% on INRIA), that can be directly stated with literature support.

---

### Item 4.2: Person Detection Baseline (Clean Model, Clean Data)

**What to measure:** Run YOLOv8n, YOLOv11n, and YOLO26n on clean INRIA Person test set. Record: AP@0.5, Recall@0.4, F1@0.5 for each. This establishes the clean baseline from which attack suppression is measured.

**Literature support:** All papers establish clean baselines before reporting attack results. Without this, attack effectiveness claims cannot be evaluated. AdvReal Table 3 shows white/gray/noise patches as controls; DePatch shows "Noise" patch (96.12% AP) as clean baseline.

**Contribution to all phases:** Necessary baseline for any attack or defense measurement. Simple and unambiguous.

---

## Category 5: Literature-Backed Documentation Gap

### Item 5.1: YOLO26 Architecture Analysis for Patch Attack Surface

**What to measure:** Read YOLO26 technical documentation and model architecture. Identify: (a) whether YOLO26 uses an objectness score (anchor-based) or class-confidence-only (anchor-free/NMS-free), (b) how many detection heads it has vs. v8/v11, (c) what loss components are available for adversarial patch optimization, (d) whether C2f or AIFI blocks are present.

**Literature support:** Bayer 2024 shows RT-DETR (NMS-free, attention-based) is an outlier in transfer robustness. Winter 2026 shows transformer architectures are more robust to cross-architecture transfer. AdvReal shows D-DETR (59.09% ASR) is harder to fool than YOLO-family (67-78% ASR). If YOLO26 uses DETR-like attention, the patch threat model changes.

**Contribution to attack phase:** Determines whether the capstone patch (trained with objectness-suppression loss on v8n) is theoretically applicable to v26n. If v26n has no objectness score, the loss function needs adjustment. This is architectural due diligence, not attack optimization.

---

### Item 5.2: Physical Plausibility Definition Document

**What to measure / document:** Write a one-page document defining the capstone's physical plausibility constraints: (1) NPS constraint scope (which printer color gamut?), (2) TV loss threshold (what smoothness is physically realistic?), (3) Patch size as percentage of person bounding box, (4) EoT augmentation range matched to documented physical conditions in Schack 2024, (5) What physical conditions the patch is NOT designed to withstand (and why).

**Literature support:** Schack 2024 documents the physical-digital gap systematically. DePatch provides NPS + TV loss formulation. Wei 2024 shows camera ISP as an additional physical constraint. AdvReal uses 300×300 patch on 416×416 input as the standard.

**Contribution to all phases:** Provides the explicit threat model boundary that the defend and fortify phases can use to design evaluation conditions. Prevents scope creep and ensures claims are bounded.
