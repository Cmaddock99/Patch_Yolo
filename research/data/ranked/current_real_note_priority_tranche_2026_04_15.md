# Current Real-Note Priority Tranche

Generated: 2026-04-15
Source inputs:
- `research/data/ranked/top50_fulltext_queue_2026_04_15.md`
- `research/data/ranked/top200_screening_packet_2026_04_15.jsonl`
- local PDF inventory in `docs/papers/`

Purpose: define the next papers that should become real repo notes, or the next blocked / note-only records that should be upgraded into citation-grade notes, using the current capstone questions rather than raw rank alone.

## Summary

- Tranche size: 10 papers
- Local PDF ready now: 9
- Manual retrieval still needed: 1
- Primary emphasis:
  - `physical_robustness`: 8
  - `cross_yolo_transfer`: 2

## Read Order

### 1. I Don't Know You, But I Can Catch You: Real-Time Defense against Diverse Adversarial Patches for Object Detectors

- Repo question: `physical_robustness`
- Why now: strongest unread detector-side defense paper in the current queue, with both digital and physical framing and a local PDF already in the corpus.
- Expected note outcome: defense comparator for the capstone limitations and countermeasure discussion.
- Local PDF: `docs/papers/realtime_defense_diverse_patches_2406.10285.pdf`

### 2. Adversarial Texture for Fooling Person Detectors in the Physical World

- Repo question: `physical_robustness`
- Why now: high-citation physical person-evasion benchmark that fills the gap between the older YOLOv2 shirt work and newer multi-view physical attacks.
- Expected note outcome: real benchmark note for multi-angle physical clothing attacks against person detectors.
- Local PDF: `docs/papers/advtexture_person_detectors_2203.03373.pdf`

### 3. We Can Always Catch You: Detecting Adversarial Patched Objects WITH or WITHOUT Signature

- Repo question: `physical_robustness`
- Why now: distinct defense paradigm and now locally available in the repo, making it a good contrast with both preprocessing baselines and learned detector-side defenses.
- Expected note outcome: defense note comparing signature-based versus signature-independent patch detection.
- Local PDF: `docs/papers/we_can_always_catch_you_2106.05261.pdf`

### 4. Evaluating the Adversarial Robustness of Detection Transformers

- Repo question: `cross_yolo_transfer`
- Why now: directly relevant to whether transformer-style detectors behave like the repo's hardest transfer target, especially after the new YOLOv10 / RT-DETR / Co-DETR architecture notes.
- Expected note outcome: benchmark note on attack behavior against DETR-family models and what that implies for `YOLO26n`.
- Local PDF: `docs/papers/detection_transformers_robustness_2412.18718.pdf`

### 5. Improving Transferability of Physical Adversarial Attacks on Object Detectors Through Multi-Model Optimization

- Repo question: `cross_yolo_transfer`
- Why now: most direct candidate for improving black-box transfer without training on every target model separately.
- Expected note outcome: method note for multi-model patch training and transfer improvement.
- Local PDF: not localized yet; MDPI direct PDF returned access-gated HTML during earlier fetch.
- Retrieval status: manual browser fetch or alternate open-access mirror needed before a full note can be written.

### 6. Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks

- Repo question: `physical_robustness`
- Why now: the repo now has the local PDF, but the note is still an access-era placeholder. This is the cleanest segment-and-recover defense in the local corpus.
- Expected note outcome: promoted defense note for the fortify / recovery phase instead of continuing to treat SAR as a note-only concept.
- Local PDF: `docs/papers/gu2025_SAR_segment_recover_jimaging316.pdf`

### 7. Increasing Neural-Based Pedestrian Detectors' Robustness to Adversarial Patch Attacks Using Anomaly Localization

- Repo question: `physical_robustness`
- Why now: the note exists, the local PDF exists, and it fills the anomaly-localization defense slot that is still underrepresented in the promoted literature layer.
- Expected note outcome: promoted defense note for anomaly localization plus reconstruction as a distinct mitigation path.
- Local PDF: `docs/papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf`

### 8. Adversarial T-shirt! Evading Person Detectors in A Physical World

- Repo question: `physical_robustness`
- Why now: still the cleanest older physical benchmark for deformable wearable attacks, and a good anchor point for comparing newer physical patch methods against the repo's digital-first results.
- Expected note outcome: upgraded benchmark note with verified digital / physical numbers and the exact TPS-based deformation idea to borrow.
- Local PDF: `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf`

### 9. AdvLogo: Adversarial Patch Attack against Object Detectors based on Diffusion Models

- Repo question: `physical_robustness`
- Why now: the repo has the local PDF but no note yet, and it is a strong recent candidate for the naturalistic-versus-effective patch tradeoff discussion.
- Expected note outcome: method note on diffusion-based patch generation with better visual quality and how that compares to GAN-based naturalistic patches.
- Local PDF: `docs/papers/advlogo_diffusion_patch_2409.07002.pdf`

### 10. PatchZero: Defending against Adversarial Patch Attacks by Detecting and Zeroing the Patch

- Repo question: `physical_robustness`
- Why now: the repo already has a useful detector-agnostic defense note and local PDF, but promoting it into a tighter detector-focused synthesis would improve the defense-side comparison set for all YOLO generations.
- Expected note outcome: consolidated defense note for detect-and-zero preprocessing, with detector-task implications made explicit.
- Local PDF: `docs/papers/patchzero2022_detect_zero_defense_2207.01795.pdf`

## What This Means for Note Writing

- The first pass should focus on items 1 through 4 because they are new, local, and directly improve the current defense / transfer discussion.
- Item 5 is the only manual-retrieval blocker left in the tranche; everything else can be advanced from repo-local materials now.
- Items 6 through 10 are upgrade targets: they either convert access-era placeholder notes into real PDF-backed defenses or tighten partial notes into citation-grade evidence.
- Do not spend the next pass on already-covered YOLOv10 / Co-DETR / RT-DETR / FCOS / NMS-free bridge papers, or on the newly promoted Liao / Gala notes.
