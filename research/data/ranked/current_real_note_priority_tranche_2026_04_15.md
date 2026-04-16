# Current Real-Note Priority Tranche

Generated: 2026-04-15
Source inputs:
- `research/data/ranked/top50_fulltext_queue_2026_04_15.md`
- `research/data/ranked/top200_screening_packet_2026_04_15.jsonl`
- local PDF inventory in `docs/papers/`

Purpose: define the next papers that should become real repo notes, or the next blocked / note-only records that should be upgraded into citation-grade notes, using the current capstone questions rather than raw rank alone.

## Summary

- Tranche size: 9 papers
- Local PDF ready now: 9
- Manual retrieval still needed: 0
- Primary emphasis:
  - `physical_robustness`: 8
  - `cross_yolo_transfer`: 1

## Read Order

### 1. AdvLogo: Adversarial Patch Attack against Object Detectors based on Diffusion Models

- Repo question: `physical_robustness`
- Why now: the repo has the local PDF but no note yet, and it is the cleanest next naturalistic-versus-effective patch paper after the recent defense-heavy pass.
- Expected note outcome: method note on diffusion-based patch generation with better visual quality and how that compares to GAN-based naturalistic patches.
- Local PDF: `docs/papers/advlogo_diffusion_patch_2409.07002.pdf`

### 2. PatchZero: Defending against Adversarial Patch Attacks by Detecting and Zeroing the Patch

- Repo question: `physical_robustness`
- Why now: the repo already has a useful detector-agnostic defense note and local PDF, but promoting it into a tighter detector-focused synthesis would improve the defense-side comparison set for all YOLO generations.
- Expected note outcome: consolidated defense note for detect-and-zero preprocessing, with detector-task implications made explicit.
- Local PDF: `docs/papers/patchzero2022_detect_zero_defense_2207.01795.pdf`

### 3. Invisible Cloak: Real Physical Adversarial Attack on Object Detectors

- Repo question: `physical_robustness`
- Why now: older but still important physical transfer benchmark covering multiple detector families; worth tightening now that the defense side has been strengthened.
- Expected note outcome: upgraded benchmark note for multi-detector physical transfer and wearable evaluation.
- Local PDF: `docs/papers/wu2020_invisibility_cloak_1910.14667.pdf`

### 4. MVPatch: A Multi-Model Versatile Adversarial Patch for Object Detection

- Repo question: `cross_yolo_transfer`
- Why now: the cleanest remaining local multi-model camouflage paper for transfer discussion after the DETR and physical benchmark passes.
- Expected note outcome: transfer-oriented method note for simultaneous multi-model optimization and camouflage tradeoffs.
- Local PDF: `docs/papers/zhou2023_mvpatch_2312.17431.pdf`

### 5. UV-Attack: Physical-World Person Evasion with NeRF-Based UV Mapping

- Repo question: `physical_robustness`
- Why now: view-consistent person attack method with a local PDF already present, making it a useful bridge from older cloth attacks to newer rendering-heavy approaches.
- Expected note outcome: promoted note on NeRF / UV-map physical robustness and how much it adds beyond classic TPS-style methods.
- Local PDF: `docs/papers/li2025_uvattack_nerf_person_2501.05783.pdf`

### 6. FRAN: Frequency Attention for Adversarial Patch Robustness

- Repo question: `physical_robustness`
- Why now: the paper is still only partially integrated, but it is one of the clearest frequency-domain defense / localization references in the local corpus.
- Expected note outcome: tighter method note on frequency anomalies as a defense or diagnostic signal.
- Local PDF: `docs/papers/lu2022_fran_frequency_attention_2205.04638.pdf`

### 7. Diff-NAT: Diffusion-Based Naturalistic Patches

- Repo question: `physical_robustness`
- Why now: best local candidate for the current naturalistic / diffusion branch once AdvLogo is promoted.
- Expected note outcome: a cleaner naturalistic-patch comparison note against GAN and pixel-space methods.
- Local PDF: `docs/papers/diffnat2026_AAAI.pdf`

### 8. Sequence-Level Clothing Optimization

- Repo question: `physical_robustness`
- Why now: sequence-level clothing optimization is the clearest local next step for temporal / video robustness after the wearable benchmarks.
- Expected note outcome: promoted note on sequence-consistent physical attacks and video stability.
- Local PDF: `docs/papers/zhou2025_sequence_level_clothing_2505.15848.pdf`

### 9. SPAP-2 / Dynamically Optimized Clusters

- Repo question: `physical_robustness`
- Why now: one of the few local modern-YOLO small-patch physical robustness papers that still is not integrated into the working packet.
- Expected note outcome: promoted note on small-patch physical robustness and modern YOLOv8-side benchmarking.
- Local PDF: `docs/papers/bagley2025_dynamically_optimized_clusters_2511.18656.pdf`

## What This Means for Note Writing

- The transfer-method retrieval blocker has now been cleared and localized as `docs/papers/dimitriu2024_multi_model_transferability_app142311423.pdf`, with a citation-grade note in `docs/notes/dimitriu2024_multi_model_transferability.md`.
- Items 1 through 9 are now the practical local-PDF queue after promoting SAR, anomaly localization, Xu, Ji, and Dimitriu 2024.
- The next batch should rebalance toward naturalistic patches, detector-agnostic defenses, and the remaining physical-transfer / video-robustness benchmarks.
- Do not spend the next pass on the eight papers already completed in the last two promotion rounds, on already-covered YOLOv10 / Co-DETR / RT-DETR / FCOS / NMS-free bridge papers, or on the newly promoted Liao / Gala notes.
