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

### 1. Improving Transferability of Physical Adversarial Attacks on Object Detectors Through Multi-Model Optimization

- Repo question: `cross_yolo_transfer`
- Why now: most direct candidate for improving black-box transfer without training on every target model separately, and now the main remaining retrieval blocker in the tranche.
- Expected note outcome: method note for multi-model patch training and transfer improvement.
- Local PDF: not localized yet; MDPI direct PDF returned access-gated HTML during earlier fetch.
- Retrieval status: manual browser fetch or alternate open-access mirror needed before a full note can be written.

### 2. Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks

- Repo question: `physical_robustness`
- Why now: the repo now has the local PDF, but the note is still an access-era placeholder. This is the cleanest segment-and-recover defense in the local corpus.
- Expected note outcome: promoted defense note for the fortify / recovery phase instead of continuing to treat SAR as a note-only concept.
- Local PDF: `docs/papers/gu2025_SAR_segment_recover_jimaging316.pdf`

### 3. Increasing Neural-Based Pedestrian Detectors' Robustness to Adversarial Patch Attacks Using Anomaly Localization

- Repo question: `physical_robustness`
- Why now: the note exists, the local PDF exists, and it fills the anomaly-localization defense slot that is still underrepresented in the promoted literature layer.
- Expected note outcome: promoted defense note for anomaly localization plus reconstruction as a distinct mitigation path.
- Local PDF: `docs/papers/tereshonok2025_pedestrian_robustness_jimaging026.pdf`

### 4. Adversarial T-shirt! Evading Person Detectors in A Physical World

- Why now: still the cleanest older physical benchmark for deformable wearable attacks, and a good anchor point for comparing newer physical patch methods against the repo's digital-first results.
- Expected note outcome: upgraded benchmark note with verified digital / physical numbers and the exact TPS-based deformation idea to borrow.
- Local PDF: `docs/papers/xu2020_adversarial_tshirt_1910.11099.pdf`

### 5. Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches

- Repo question: `physical_robustness`
- Why now: strongest direct YOLO-side defense benchmark still sitting below citation-grade status in the repo, and a useful counterpart to the new NutNet / Catch-You notes.
- Expected note outcome: promoted YOLO defense baseline note that can anchor defense-side comparisons more directly than detector-agnostic methods.
- Local PDF: `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf`

### 6. AdvLogo: Adversarial Patch Attack against Object Detectors based on Diffusion Models

- Repo question: `physical_robustness`
- Why now: the repo has the local PDF but no note yet, and it is a strong recent candidate for the naturalistic-versus-effective patch tradeoff discussion.
- Expected note outcome: method note on diffusion-based patch generation with better visual quality and how that compares to GAN-based naturalistic patches.
- Local PDF: `docs/papers/advlogo_diffusion_patch_2409.07002.pdf`

### 7. PatchZero: Defending against Adversarial Patch Attacks by Detecting and Zeroing the Patch

- Repo question: `physical_robustness`
- Why now: the repo already has a useful detector-agnostic defense note and local PDF, but promoting it into a tighter detector-focused synthesis would improve the defense-side comparison set for all YOLO generations.
- Expected note outcome: consolidated defense note for detect-and-zero preprocessing, with detector-task implications made explicit.
- Local PDF: `docs/papers/patchzero2022_detect_zero_defense_2207.01795.pdf`

### 8. Invisible Cloak: Real Physical Adversarial Attack on Object Detectors

- Repo question: `physical_robustness`
- Why now: older but still important physical transfer benchmark covering multiple detector families; worth tightening now that the defense side has been strengthened.
- Expected note outcome: upgraded benchmark note for multi-detector physical transfer and wearable evaluation.
- Local PDF: `docs/papers/wu2020_invisibility_cloak_1910.14667.pdf`

### 9. MVPatch: A Multi-Model Versatile Adversarial Patch for Object Detection

- Repo question: `cross_yolo_transfer`
- Why now: the cleanest remaining local multi-model camouflage paper for transfer discussion after the DETR and physical benchmark passes.
- Expected note outcome: transfer-oriented method note for simultaneous multi-model optimization and camouflage tradeoffs.
- Local PDF: `docs/papers/zhou2023_mvpatch_2312.17431.pdf`

### 10. UV-Attack: Physical-World Person Evasion with NeRF-Based UV Mapping

- Repo question: `physical_robustness`
- Why now: view-consistent person attack method with a local PDF already present, making it a useful bridge from older cloth attacks to newer rendering-heavy approaches.
- Expected note outcome: promoted note on NeRF / UV-map physical robustness and how much it adds beyond classic TPS-style methods.
- Local PDF: `docs/papers/li2025_uvattack_nerf_person_2501.05783.pdf`

## What This Means for Note Writing

- The immediate next move is item 1 if you want to chase the only remaining transfer-method retrieval blocker; otherwise start with items 2 through 5 for fully local work.
- Items 2 through 10 are now the practical local-PDF queue: they either convert access-era placeholders into real notes or tighten partial notes into citation-grade evidence.
- The defense side is now substantially stronger after the first four notes, so the next batch should rebalance toward SAR, anomaly localization, Ji 2021, and one more physical benchmark.
- Do not spend the next pass on the four papers completed in this pass, on already-covered YOLOv10 / Co-DETR / RT-DETR / FCOS / NMS-free bridge papers, or on the newly promoted Liao / Gala notes.
