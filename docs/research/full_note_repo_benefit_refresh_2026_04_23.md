# Full-Note Repo Benefit Refresh — 2026-04-23

## 1. Supersession & Scope

**This document supersedes** `docs/research/repo_benefit_spec.md` (2026-04-16) and `docs/research/presentation_repo_survey_2026_04_16.md` (2026-04-16) as the current source of truth for repo-benefit extraction from the full-note corpus. Both predecessors remain in-tree as historical context but should not be cited against current repo state.

**Corpus freeze date**: 2026-04-23. **Input set**: 78 `page_cited` notes in `docs/notes/`. **Excluded from evidence**: 10 `blocked_access` notes and 1 template/unclassified note. This corrects the stale `8 blocked_access` count still present in the 2026-04-16 syntheses.

**Repo-question lanes**:
- `cross_yolo_transfer` (13 page_cited notes)
- `physical_robustness` (37 notes)
- `yolo26_architecture_mismatch` (13 notes)
- `yolo11_coverage` (2 notes)
- `general_experiment_design` — catch-all; `generic_context` notes (13) appear here **only** where they reinforce a lane-tagged finding

**Current repo state** this doc is additive against (from `README.md`, `experiments/ultralytics_patch.py`, live artifacts):

- Direct suppression: v8n **90.0%**, v11n **72.7%**, v26n **16.3%** (loss converges to 0.108 — diagnosed head paradox)
- Cross-YOLO transfer: v8n→v11n 33.3%, v11n→v8n 55.0%, v8n→v26n 14.0%, v11n→v26n 9.3%, v26n→v8n 45.0%, v26n→v11n 24.2%
- Joint: v8n+v11n→v11n 66.7%; v8n+v26n→v26n 18.6% (negligible lift). Warm-start: v26n-warmstart→v8n 95.0% (v26n optimizer falls into the same local minimum regardless of init)
- Training loop already implements: `block_erase` (DePatch), `patch_cutout` (T-SEA), `apply_self_ensemble` (`--self-ensemble-mode shakedrop`), `rotate_patch_eot` (EoT), `apply_cloth_eot` (`--cloth-eot tps`), `nps_loss`, `tv_loss`, `--loss-source auto|one2many|one2one`, `--v26-loss-mode topk|logsumexp|hybrid`, `--multi-placement`, `--placement-regime`, and `--co-model` with `--co-weight-mode static|adaptive`
- Evaluation tooling now includes `experiments/failure_grid.py` (digital nuisance grid), `experiments/physical_benchmark.py` with sector markdown summaries, and placement-aware `experiments/defense_eval.py`
- `experiments/defense_eval.py` covers `jpeg`, `blur`, `crop_resize` only

---

## 2. Top Takeaways

1. **The v26n head paradox is an architecture-class problem, not a tuning problem.** YOLOv10-family detectors train with a `one2many` head and infer with a `one2one` head; Co-DETR shows the same design needs coordinated auxiliary supervision, not one-or-the-other. Warm-start→v26n 14.0% confirms the optimizer repeatedly converges to an inference-irrelevant minimum. [`yolo26_architecture_mismatch`; evidence: `docs/notes/wang2024_yolov10_end_to_end.md`, `docs/notes/zong2022_codetr_hybrid_assignments.md`, `docs/notes/zhou2021_nms_free_object_detection.md`, `docs/notes/cai2023_align_detr.md`]
2. **Source-model size is a stronger transfer predictor than loss design.** Bayer (2024) shows `YOLOv8n/s` are the weakest transfer sources in a 28-model matrix; larger sources (v9/v10) transfer best. Our nano-only matrix is upper-bounded by this. [`cross_yolo_transfer`; evidence: `docs/notes/bayer2024_network_transferability.md`, `docs/notes/dimitriu2024_multi_model_transferability.md`]
3. **Self-ensemble during training (ShakeDrop-style) is the cheapest transfer improvement we have implemented but not yet promoted with a clean ablation.** T-SEA drops 7-detector black-box mAP from 36.46% to 9.16% on a v5 source using patch cutout + ShakeDrop + constrained augmentation; the repo now has the code path, but not the validating artifact set. [`cross_yolo_transfer`; evidence: `docs/notes/huang2022_tsea_transfer.md`, `docs/notes/cheng2024_depatch_decoupled.md`]
4. **Digital suppression ≠ physical suppression; Schack's 64% brightness gap is the ceiling we should plan around.** Our 90%/72.7% direct numbers are digital only; published physical losses are 15–20 pp (Xu 2020: 74% digital → 57% physical) and brightness/rotation/hue can each wipe out the attack. [`physical_robustness`; evidence: `docs/notes/schack2024_real_world_challenges.md`, `docs/notes/xu2020_adversarial_tshirt.md`, `docs/notes/huang2025_advreal_physical.md`]
5. **Non-rigid cloth deformation (3D mesh or TPS) is the single largest physical augmentation win reported, and the repo now has the code path but not the promoted artifact.** AdvReal attributes +4.11% ASR to non-rigid deformation alone; DAP's Creases Transformation hits 92.01% physical TPR on T-shirts vs 57.22% for NAP. [`physical_robustness`; evidence: `docs/notes/huang2025_advreal_physical.md`, `docs/notes/guesmi2024_DAP_dynamic_adversarial_patch.md`, `docs/notes/xu2020_adversarial_tshirt.md`]
6. **Superpixel-constrained patches improve scale resilience without a new optimizer.** SPAP-2 drops person AP on YOLOv8 to 16.28% vs 24.97% for standard AdvPatch; the differentiable SLIC step is a drop-in regularization. [`physical_robustness`; evidence: `docs/notes/bagley2025_dynamically_optimized_clusters.md`]
7. **Naturalistic (GAN/diffusion) patches trade most of their attack strength for appearance, and NAPGuard now detects them.** AdvCaT's 0.87% ASR under AdvReal's physical protocol and NAPGuard's 91% AP on naturalistic-patch detection mean naturalism is a weak direction for our threat model. [`general_experiment_design`; evidence: `docs/notes/huang2025_advreal_physical.md`, `docs/notes/wu2024_NAPGuard.md`, `docs/notes/hu2021_naturalistic_patch.md`, `docs/notes/diffnat2026_AAAI.md`]
8. **Evaluation must separate localization failure from score collapse, and name the placement regime.** DPatch (off-object) and Thys (objectness) are different threat models; current repo summaries conflate torso-centered and off-object suppression into one number. [`general_experiment_design`; evidence: `docs/notes/liu2019_dpatch.md`, `docs/notes/saha2020_spatial_context_yolo.md`, `docs/notes/thys2019_fooling_surveillance.md`]
9. **YOLO11 verified literature remains a two-note lane, with one additional blocked comparator.** The only YOLO11-tagged `page_cited` notes are `docs/notes/gala2025_yolo_adversarial_patches.md` (BigGAN naturalistic, no transfer matrix) and `docs/notes/yolo11_architecture_overview.md` (architecture only); the one extra YOLO11-specific comparator remains blocked in § 7. Our v11n numbers are currently the strongest repo-owned datapoint. [`yolo11_coverage`; evidence: `docs/notes/gala2025_yolo_adversarial_patches.md`, `docs/notes/yolo11_architecture_overview.md`]
10. **Defense work belongs in `YOLO-Bad-Triangle`, but our preprocessing baseline is already behind the literature floor.** SAR (inpaint-recovery, certified recall 0.72–0.88 on YOLOv11), NutNet (physical ASR 83% → 0.7%), and Ji's patch-class retraining (80.31% AP under attack) all beat jpeg/blur/crop-resize, and APDE (Shen 2025) shows naturalistic patches still bypass most of them. [`general_experiment_design`; evidence: `docs/notes/gu2025_SAR_segment_recover.md`, `docs/notes/lin2024_nutnet_defense.md`, `docs/notes/ji2021_adversarial_yolo_defense.md`, `docs/notes/shen2025_revisiting_patch_defenses_detectors.md`]
11. **Attention-aware optimization is the next YOLO26-class question if the selected-query objective stalls.** Alam (Deformable DETR → 0% AP with <1% pixels) and Lovisotto (ViT/DETR → 0 mAP with 0.5% patch) show that dot-product/deformable attention needs attention-aware loss, not dense score suppression. [`yolo26_architecture_mismatch`; evidence: `docs/notes/alam2023_attention_deficit_deformable.md`, `docs/notes/lovisotto2022_attention_patch_robustness.md`]
12. **Sector-based physical reporting is cheap, eliminates over-claiming, and matches the structure every strong physical paper already uses.** Xu, Hoory, AdvReal, Schack, and DelaCruz all report by distance/yaw/lighting sector; pooling into one number hides the modes where the patch fails. [`physical_robustness`; evidence: `docs/notes/xu2020_adversarial_tshirt.md`, `docs/notes/hoory2020_dynamic_patch.md`, `docs/notes/huang2025_advreal_physical.md`, `docs/notes/schack2024_real_world_challenges.md`, `docs/notes/delacruz2026_physical_attacks_surveillance.md`]

---

## 3. Borrow Now

Candidate shortlist ranked by priority. Not every entry lands in § 6 Queue — some are parked until pre-reqs finish.

### B1 — Self-ensemble / ShakeDrop-style transfer regularization
- `priority`: **P0**
- `lane`: `cross_yolo_transfer`
- `recommendation`: Add a self-ensemble training path that combines existing `patch_cutout` with stochastic-depth-style dropout over backbone blocks; run an ablation isolating cutout-only vs. self-ensemble-only vs. combined against the current v8n→v11n 33.3% / v8n→v26n 14.0% baseline.
- `why_it_should_help`: T-SEA's self-ensemble is the best-documented transfer win in the corpus on a comparable architecture class, and we already implement one of its three components. Closes the most obvious mechanism gap without replacing the optimizer.
- `evidence_notes`: `docs/notes/huang2022_tsea_transfer.md`, `docs/notes/cheng2024_depatch_decoupled.md`
- `expected_upside`: Plausible +10–20 pp on v8n→v11n; lower confidence on v8n→v26n because the head paradox is orthogonal.
- `risk`: ShakeDrop is tuned to ResNet blocks; adaptation to Ultralytics C2f / C3k2 is approximate, not a literal port.

### B2 — Larger-source compatibility matrix (v8m / v8l source)
- `priority`: **P0**
- `lane`: `cross_yolo_transfer`
- `recommendation`: Train at least one patch against `yolov8m` (or `yolov8l`) and evaluate on the current v11n/v26n targets. Report source-size-vs-transfer cells alongside the existing nano matrix.
- `why_it_should_help`: Bayer's 28-model study identifies v8n/s as the weakest transfer sources; our current ceiling may be a source-size artifact rather than a loss-design problem. Must be answered before more nano-only tuning has diagnostic value.
- `evidence_notes`: `docs/notes/bayer2024_network_transferability.md`, `docs/notes/gala2025_yolo_adversarial_patches.md`
- `expected_upside`: Even a negative result is load-bearing: it either unlocks 15–30 pp transfer headroom or rules out source-size as the bottleneck.
- `risk`: Higher compute cost per run; GPU budget must accommodate.

### B3 — Non-rigid cloth deformation EoT (TPS or 3D-mesh approximation)
- `priority`: **P1**
- `lane`: `physical_robustness`
- `recommendation`: Add a differentiable TPS-warp (Xu 2020 recipe) or simplified stress-point mesh deform (AdvReal recipe) to the EoT stack, gated behind a flag so the rigid-only pipeline remains reproducible.
- `why_it_should_help`: AdvReal ablates +4.11% ASR from non-rigid deformation alone; DAP's Creases Transformation is the cleanest cheap version. This is the single most validated physical-robustness augmentation the repo does not yet have.
- `evidence_notes`: `docs/notes/huang2025_advreal_physical.md`, `docs/notes/guesmi2024_DAP_dynamic_adversarial_patch.md`, `docs/notes/xu2020_adversarial_tshirt.md`, `docs/notes/cheng2024_depatch_decoupled.md`
- `expected_upside`: 5–10 pp physical ASR retention under realistic cloth deformation; qualitative improvement at yaw > 20°.
- `risk`: Engineering cost is non-trivial (differentiable warping with gradient flow); fragile if re-implemented naively.

### B4 — Selected-query / dual-head objective pack for v26n
- `priority`: **P1**
- `lane`: `yolo26_architecture_mismatch`
- `recommendation`: Add a loss path that mirrors Co-DETR's hybrid supervision: compute gradient from both `one2many` (dense auxiliary) and `one2one` (selected-query) heads with scheduled weighting, reporting against current `topk`/`logsumexp` baselines.
- `why_it_should_help`: Wang (YOLOv10), Zong (Co-DETR), and Zhou (PSS) all identify coordinated dual-head supervision as the correct response to the head paradox the repo has already diagnosed. Warm-start→v26n 14.0% confirms no amount of init tuning fixes this.
- `evidence_notes`: `docs/notes/wang2024_yolov10_end_to_end.md`, `docs/notes/zong2022_codetr_hybrid_assignments.md`, `docs/notes/zhou2021_nms_free_object_detection.md`, `docs/notes/cai2023_align_detr.md`
- `expected_upside`: First honest shot at breaking the 16.3% ceiling; target is ≥ 40% v26n direct suppression.
- `risk`: Loss-schedule space is large; easy to silently overfit the auxiliary head.

### B5 — Superpixel (SLIC + IFT) spatial constraint
- `priority`: **P1**
- `lane`: `physical_robustness`
- `recommendation`: Add a superpixel-boundary spatial regularizer as a drop-in alongside TV. Train one v8n patch under the constraint and compare scale-degradation curves.
- `why_it_should_help`: SPAP-2 reaches person AP 16.28% on YOLOv8 vs 24.97% for standard AdvPatch at small scales — the only YOLOv8-direct result of this kind.
- `evidence_notes`: `docs/notes/bagley2025_dynamically_optimized_clusters.md`
- `expected_upside`: Better small-scale robustness; plausible retention at print sizes below 8".
- `risk`: Scale resilience helps only if printed artifacts are actually small; low-priority if the threat model assumes 8–12" patches.

### B6 — Attention-aware loss experiment for v26n (contingent on B4)
- `priority`: **P2**
- `lane`: `yolo26_architecture_mismatch`
- `recommendation`: After B4 results are known, add an attention-aware diagnostic path that penalizes or amplifies attention-map similarity alongside score suppression.
- `why_it_should_help`: Alam and Lovisotto show dot-product / deformable attention breaks standard dense-score gradients. If B4 plateaus, attention is the next structural suspect.
- `evidence_notes`: `docs/notes/alam2023_attention_deficit_deformable.md`, `docs/notes/lovisotto2022_attention_patch_robustness.md`
- `expected_upside`: Diagnostic (was the attention pathway the bottleneck?) rather than guaranteed attack lift.
- `risk`: Only single-paper evidence per finding for YOLO26-like detectors; speculative mechanism.

### B7 — Dynamic-weight mixed-surrogate training
- `priority`: **P2**
- `lane`: `cross_yolo_transfer`
- `recommendation`: Replace fixed co-model weights in `--co-model` joint training with a dynamic schedule (e.g. DOEPatch's Min-Max alternation) to prevent collapse onto one surrogate's gradient landscape.
- `why_it_should_help`: DOEPatch and DOEPatch-style weighting consistently outperform fixed-weight ensembles in the transfer corpus; Dimitriu confirms the approach for YOLOv8-family sources.
- `evidence_notes`: `docs/notes/tan2024_DOEPatch.md`, `docs/notes/dimitriu2024_multi_model_transferability.md`, `docs/notes/zhou2023_mvpatch.md`
- `expected_upside`: Modest (5–10 pp) over fixed-weight v8n+v11n and v8n+v26n joints.
- `risk`: Search space expands fast; needs strict experiment discipline to avoid combinatorial sprawl.

### B8 — Off-object placement evaluation lane
- `priority`: **P2**
- `lane`: `general_experiment_design`
- `recommendation`: Add an evaluation mode that places the patch off-object (beside or above the person) and reports suppression separately from torso-overlap suppression.
- `why_it_should_help`: DPatch, Kolter's global patch, and Saha's spatial-context patch all reach non-trivial suppression without target overlap. Our current numbers cannot distinguish "detector disruption" from "person-vanishing."
- `evidence_notes`: `docs/notes/liu2019_dpatch.md`, `docs/notes/kolter2019_global_patch_suppression.md`, `docs/notes/saha2020_spatial_context_yolo.md`
- `expected_upside`: Cleaner threat-model claims; likely lower headline numbers but more credible.
- `risk`: Headline suppression drops; needs reframing in the README and deck.

---

## 4. Repo Support Findings

Non-attack findings that strengthen evaluation, bound claims, or scope the later handoff.

### 4.1 Transfer diagnostics
- **Source size > loss design for transfer** (Bayer 2024): current nano-only matrix systematically under-represents achievable transfer. Pair with B2.
- **Naturalistic transfer is weaker than non-naturalistic** (Hu 2021, Diff-NAT 2026, Huang 2025): naturalistic patches consistently lag in cross-detector suppression, independent of digital numbers.
- **Anchor-free output format breaks older-transfer assumptions** (Liao 2021): CenterNet-trained patches transfer weakly to Faster R-CNN; by analogy v26n's end-to-end format may penalize v8n-sourced patches further than standard.

### 4.2 Physical failure modes
- **>20° rotation kills effectiveness** (Schack 2024, Xu 2020). Our current EoT rotation bound should be reported alongside suppression numbers.
- **Outdoor penalty ≈ 15–20 pp vs indoor** (Xu 2020: 64% indoor / 47% outdoor; Hoory 2020: 80% indoor / 15–23% outdoor with glare).
- **Brightness shift is the single worst digital→physical failure** (Schack 2024: up to 64% gap).
- **Coverage area is first-order** (Hu 2022: skirt 0.287 mASR vs dress 0.893 mASR). Our 8" × 8" patch size should be cited as a floor, not a ceiling.
- **Wearable transfer is weaker than poster transfer** (Wu 2020, AdvTexture 2022): planar-poster results over-predict body-worn performance.

### 4.3 YOLO26 / end-to-end implications
- **The head paradox is documented at architecture-class scale**: Wang (YOLOv10), Zong (Co-DETR), Zhou (PSS), Cai (Align-DETR), Zhao (RT-DETR) collectively describe the `one2many`-train / `one2one`-infer split and the optimization conflicts it creates.
- **Hungarian matching introduces a selected-query decision process that dense objectness loss does not target** (Cai 2023, Wang 2024). Current `topk` / `logsumexp` both remain score-field operations.
- **Attention-route suppression is a separate bottleneck from score suppression** (Alam 2023, Lovisotto 2022). Not actionable until B4 completes.

### 4.4 Evaluation protocol upgrades
- **Sector-based physical reporting** (see Top Takeaway #12): every strong physical paper separates by distance/yaw/lighting. Adding this is low-cost, high-clarity.
- **Per-size / per-scale reporting** (Bagley 2025, Hu 2022): headline suppression is size-dependent; report at least two print sizes.
- **Adaptive-attack acknowledgment** (Shen 2025, PatchZero 2022): adaptive (BPDA-style) evaluations should bound any defense-benchmark claim.
- **Schack-style digital failure grid**: hue / size / brightness / rotation grid as a digital pre-step before physical capture. Low implementation cost.
- **Sequence / temporal metrics when video is involved** (Zhou 2025 sequence-level clothing, Zimmermann 2026 KGFP): frame-averaged suppression hides per-frame failures.

### 4.5 Defense baselines to hand off (not this repo)
Earmarked for `YOLO-Bad-Triangle`; listed here only to prevent duplicate work on the attack side.

- **Patch-class retraining** (Ji 2021): 80.31% AP under white-box attack vs 33.93% baseline on YOLOv2; simplest retraining baseline.
- **Segment-and-recover** (Gu 2025 SAR): certified recall 0.72–0.88 on YOLOv11 under 20–40% adaptive patches; first modern-YOLO-direct defense.
- **NutNet autoencoder** (Lin 2024): physical ASR 83% → 0.7% on YOLOv2; lightest-weight recovery baseline in the corpus.
- **Anomaly localization** (Tereshonok 2025): clean-only training; mAP 46.79 → 80.97 on INRIA.
- **Patch-detection frontend** (NAPGuard 2024, PatchZero 2022): complement rather than replace recovery; NAPGuard targets naturalistic patches specifically.

---

## 5. Do Not Chase

Approaches the corpus suggests are weak fits for this repo, with the contradictions explicit.

### 5.1 Naturalistic / GAN / diffusion patches as a robustness play
- **Contradiction**: strong digital numbers (Diff-NAT YOLOv2 AP 4.37), collapse physically (AdvCaT 0.87% ASR under AdvReal), and now detectable by NAPGuard at 91% AP. Naturalism and attack strength trade off on every axis the repo cares about.
- `evidence`: `diffnat2026_AAAI.md`, `hu2021_naturalistic_patch.md`, `huang2025_advreal_physical.md`, `wu2024_NAPGuard.md`, `advlogo2024_diffusion_patch.md`

### 5.2 More nano-only v8n → v26n tuning without a larger-source baseline
- **Contradiction**: Bayer identifies v8n/s as weak transfer sources. Warm-start→v26n 14.0% shows the v26n basin is init-independent. Further nano-only tuning cannot separate source-size effects from loss-design effects.
- `evidence`: `bayer2024_network_transferability.md`, repo warm-start result (README.md)

### 5.3 Screen-based / active / dynamic patches as the physical story
- **Contradiction**: Hoory's screens drop to 15–23% outdoors; Zhu's t-patch needs an acoustic trigger; Chahe's work is car-mounted screens. Our threat model is passive printed patches; these threat models are not additive.
- `evidence`: `hoory2020_dynamic_patch.md`, `zhu2023_tpatch_triggered_physical_patch.md`, `chahe2024_dynamic_attacks_autonomous_driving.md`

### 5.4 Vehicle / infrared / stop-sign methods as person-suppression upgrades
- **Contradiction**: Wang (FCA), He (RAUCA), Zhu (IR stickers), Tang (HotCold), Zolfi (translucent stop-sign), Pavlitska (stoplight), Chahe (sign) operate on domains where coverage, background, and class semantics are fundamentally different from person detection. Mechanism reuse is limited.
- `evidence`: `wang2022_fca_vehicle_camouflage.md`, `he2024_rauca_vehicle_camouflage.md`, `zhu2024_infrared_car_stickers.md`, `tang2023_hotcold_block_infrared.md`, `zolfi2021_translucent_patch.md`, `pavlitska2025_fool_stoplight.md`

### 5.5 UV-Attack / NeRF pipelines as near-term augmentation
- **Contradiction**: Li 2025 UV-Attack achieves 92.75% on Faster R-CNN and 49.5–58.6% black-box on YOLOv8 — but only via dynamic NeRF rendering of clothing. Heavy compute, YOLOv5-trained; directionally confirms non-rigid modeling but not implementable as a drop-in.
- `evidence`: `li2025_uvattack_nerf_person.md`
- Prefer the cheaper TPS / AdvReal approximations captured in B3.

### 5.6 Claiming "physical robustness" from digital numbers
- **Contradiction**: every strong physical paper (Schack, Xu, Hoory, AdvReal, DAP) reports a substantial digital-physical gap. Our `v8n 90%` and `v11n 72.7%` are digital-only and should not be reported as physical performance.
- `evidence`: `schack2024_real_world_challenges.md`, `xu2020_adversarial_tshirt.md`, `hoory2020_dynamic_patch.md`, `huang2025_advreal_physical.md`, `guesmi2024_DAP_dynamic_adversarial_patch.md`

### 5.7 Aggressive LLM-agent orchestration (MAGIC)
- **Contradiction**: Xing 2024 MAGIC reaches 80–91% digital on YOLOv5/RT-DETR/YOLOv10 via LLM agents, but diffusion-based generation cost is high and reproducibility is questionable at research-compute budgets.
- `evidence`: `xing2024_magic_contextual_patch_agents.md`
- Parked as context, not as a near-term recommendation.

---

## 6. Next Experiment Queue

Sequenced, actionable repo tasks. `scope` marks `this_repo` vs `handoff` to `YOLO-Bad-Triangle`. Each has a measurable acceptance signal.

| rank | lane | scope | task | acceptance_signal | dependencies | evidence |
|---|---|---|---|---|---|---|
| 1 | `yolo11_coverage` | `this_repo` | Train one v8m-source (or v8l-source) patch and evaluate on current v11n and v26n targets; add source-size row to transfer matrix in README. | v8m→v11n transfer reported alongside current v8n→v11n 33.3%; direction (improvement vs no effect) is unambiguous on the same manifest. | GPU budget for a larger-source run. | bayer2024, gala2025 |
| 2 | `cross_yolo_transfer` | `this_repo` | Run the self-ensemble ablation that the codebase now supports: baseline / cutout-only / self-ensemble-only / combined. | v8n→v11n transfer improves by ≥ 5 pp over current 33.3% under at least one ablation cell; isolates cutout contribution. | Colab/GPU queue capacity. | huang2022_tsea, cheng2024 |
| 3 | `general_experiment_design` | `this_repo` | Backfill `failure_grid.py` outputs for the canonical patch artifacts and wire them into artifact gating. | Every canonical patch artifact has a saved four-axis grid with per-cell suppression numbers and best/worst-cell summary. | none | schack2024, bagley2025, hoory2020 |
| 4 | `physical_robustness` | `this_repo` | Backfill sector-based physical benchmark summaries for the canonical patch artifacts; retire pooled one-number summaries in downstream docs. | New physical benchmark runs write per-sector markdown tables; README and downstream docs cite per-sector ranges, not a single number. | Operator time for physical capture. | xu2020, hoory2020, huang2025_advreal, schack2024, delacruz2026 |
| 5 | `yolo26_architecture_mismatch` | `this_repo` | Promote the existing `--v26-loss-mode hybrid` path with a clean canonical run and compare it against current v2 / logsumexp baselines. | v26n direct suppression rises to ≥ 40% on the current manifest, OR the experiment definitively isolates the selected-query path as not-the-bottleneck and surfaces the next suspect (e.g. attention routing). | Colab/GPU queue capacity. | wang2024_yolov10, zong2022_codetr, zhou2021_nms_free, cai2023_align_detr |
| 6 | `physical_robustness` | `this_repo` | Promote the existing TPS cloth-EoT path with at least one canonical artifact and physical run. | With cloth EoT enabled, v8n direct suppression ≥ 80% (graceful degradation from 90%) AND at least one physical benchmark run shows retained suppression at yaw > 20°. | Rank 5 or another promoted source artifact. | huang2025_advreal, xu2020, guesmi2024, cheng2024 |
| 7 | `general_experiment_design` | `this_repo` | Use the new placement-aware eval tooling to report torso-centered vs off-object suppression separately in the README / matrix outputs. | New column in the transfer matrix (or side table) reports off-object suppression for at least v8n / v11n; gap between regimes is explicit. | none | liu2019_dpatch, kolter2019, saha2020 |
| 8 | `general_experiment_design` | `handoff` | Stand up segment-and-recover defense (SAR-style) as the first modern-YOLO defense baseline in `YOLO-Bad-Triangle`, using our frozen patches as input. | SAR-style pipeline produces clean-cost and attacked-AP recovery numbers comparable to Gu 2025 ranges on YOLOv11 (certified recall ≥ 0.60 on 20% patch occupancy, non-trivial clean cost). | Coordination with `YOLO-Bad-Triangle` maintainer. | gu2025_SAR, lin2024_nutnet, patchzero2022 |
| 9 | `general_experiment_design` | `handoff` | Stand up patch-class retraining baseline (Ji 2021-style) against our v8n 90% patch. | Retrained detector recovers attacked AP to within 10 pp of clean AP while keeping clean cost < 5 pp. | Handoff repo readiness. | ji2021_adversarial_yolo_defense, lin2024_nutnet |
| 10 | `cross_yolo_transfer` | `this_repo` | Run and compare the new adaptive joint-weighting path against fixed-weight `--co-model` baselines. | On the current v8n+v11n or v8n+v26n joint runs, adaptive weighting beats fixed weighting by ≥ 3 pp on the weaker target. | B7 flagged as optional after ranks 1–6. | tan2024_DOEPatch, dimitriu2024, zhou2023_mvpatch |

Notes on ranking: 1 and 2 are load-bearing for the transfer story — their outcomes decide whether we keep investing in nano-source tuning at all. 3 and 4 are cheap evaluation upgrades that improve every downstream claim. 5 is the only honest next step for the YOLO26 story. 6 is the highest-leverage physical augmentation but most expensive. 7 clarifies the threat model. 8 and 9 are the first two handoffs to `YOLO-Bad-Triangle`. 10 is optional transfer polish once the larger-source question is answered.

No standalone second `yolo11_coverage` queue row is split out because the verified lane remains thin: two `page_cited` notes (`docs/notes/gala2025_yolo_adversarial_patches.md`, `docs/notes/yolo11_architecture_overview.md`) plus one blocked comparator listed in § 7. Rank 1 is the practical v11-facing expansion task for this pass.

---

## 7. Watchlist (Blocked / Unverified)

These 10 `blocked_access` notes are **not** used as evidence for any claim in sections 2–6. Listed here because they would materially change a recommendation if verified later. There are no separate unverified research notes beyond this blocked set and the template/unclassified file noted in § 1.

| note | lane | if unblocked, would change | current status |
|---|---|---|---|
| `docs/notes/wang2026_chosen_object_attack.md` | `yolo26_architecture_mismatch` | Could replace the current hybrid-surrogate guesswork in B4 / rank 5 with a directly matched Hungarian-matching attack objective. | CSUSM IEEE access; no local PDF |
| `docs/notes/li2025_elevpatch_yolo11.md` | `yolo11_coverage` | Could anchor the only YOLO11-specific benchmark comparator in the corpus. | Springer chapter; ILL needed |
| `docs/notes/zimon2025_GAN_YOLO_robustness.md` | `cross_yolo_transfer` | Could supply the closest near-scope v3/v5/v8/v11 transfer matrix against our current nano-family results. | Springer paywall |
| `docs/notes/imran2025_tkpatch_multiyolo.md` | `cross_yolo_transfer` | Could sharpen the Top-K multi-YOLO objective comparison against our current `topk` path. | No local PDF |
| `docs/notes/bae2020_TOG_targeted_objectness.md` | `yolo26_architecture_mismatch` | Could add a clean NMS-era contrast objective for v8/v11, clarifying what should *not* transfer to v26n. | Citation unverified |
| `docs/notes/lin2024_entropy_adversarial_patch.md` | `physical_robustness` | Could add the cheapest naturalism regularizer if it proves less self-defeating than GAN/diffusion methods. | IEEE Access paywall |
| `docs/notes/truong2024_AYO_GAN.md` | `physical_robustness` | Could add a second GAN-based appearance-vs-strength comparator for the naturalism lane. | Springer paywall |
| `docs/notes/wen2025_ipattack_imperceptible.md` | `general_experiment_design` | Could materially change the stealth-patch framing if detector-side imperceptibility works without fully naturalistic textures. | Springer full text blocked |
| `docs/notes/kim2025_odshield_autoencoder_defense.md` | `general_experiment_design` | Could reorder the defense handoff priority if its claimed COCO gains hold up under full-text review. | IEEE Access full text blocked |
| `docs/notes/ma2026_XAIAD_YOLO.md` | `general_experiment_design` | Could reprioritize the defense handoff toward test-time purification if the blocked detector list includes modern YOLO variants. | Elsevier paywall |

---

## 8. Evidence Appendix

Classification uses each note's `Disposition` and `Primary repo question` metadata. Claim support uses body sections (`Method`, `Results`, `Direct Relevance`, `Limitations`). The appendix is evidence-only: it lists the 78 `page_cited` notes exactly once each. Blocked notes stay in § 7 and do not appear below.

### Map of notes by where they appear in this doc

| note file | disposition | lane | supports (sections) |
|---|---|---|---|
| `docs/notes/advlogo2024_diffusion_patch.md` | method_to_borrow | physical_robustness | §5.1 |
| `docs/notes/alam2023_attention_deficit_deformable.md` | architecture_explanation | yolo26_architecture_mismatch | §2(#11), §3(B6), §4.3 |
| `docs/notes/bagley2025_dynamically_optimized_clusters.md` | benchmark | physical_robustness | §2(#6), §3(B5), §4.4, §6(rank 3) |
| `docs/notes/bayer2024_network_transferability.md` | benchmark | cross_yolo_transfer | §2(#2), §3(B2), §4.1, §5.2, §6(rank 1) |
| `docs/notes/bhattad2021_bio_inspired_moving_attack.md` | threat_model_contrast | physical_robustness | (context only; not cited in §§2–6) |
| `docs/notes/brown2017_adversarial_patch.md` | foundational | generic_context | (context only; not cited in §§2–6) |
| `docs/notes/cai2023_align_detr.md` | architecture_explanation | yolo26_architecture_mismatch | §2(#1), §3(B4), §4.3, §6(rank 5) |
| `docs/notes/chahe2024_dynamic_attacks_autonomous_driving.md` | method_to_borrow | physical_robustness | §5.3 |
| `docs/notes/cheng2024_depatch_decoupled.md` | method_to_borrow | physical_robustness | §2(#3), §3(B1), §3(B3), §6(rank 2) |
| `docs/notes/chua2022_duet_patch_localizer.md` | defense_baseline | physical_robustness | §4.5 |
| `docs/notes/delacruz2026_physical_attacks_surveillance.md` | survey_frame | generic_context | §2(#12), §4.4 |
| `docs/notes/diffnat2026_AAAI.md` | method_to_borrow | physical_robustness | §2(#7), §5.1 |
| `docs/notes/dimitriu2024_multi_model_transferability.md` | method_to_borrow | cross_yolo_transfer | §2(#2), §3(B7), §6(rank 10) |
| `docs/notes/dutta2025_iap_invisible_patch.md` | method_to_borrow | generic_context | (context only; stealth-first framing, not cited in §§2–6) |
| `docs/notes/gala2025_yolo_adversarial_patches.md` | benchmark | yolo11_coverage | §2(#9), §3(B2), §6(rank 1) |
| `docs/notes/gastaldi2017_shake_shake.md` | background_method | generic_context | (context only; cited via T-SEA's ShakeDrop lineage in B1) |
| `docs/notes/goodfellow2015_fgsm.md` | foundational | generic_context | (context only; not cited in §§2–6) |
| `docs/notes/gu2025_SAR_segment_recover.md` | defense_baseline | physical_robustness | §2(#10), §4.5, §6(rank 8) |
| `docs/notes/guesmi2024_DAP_dynamic_adversarial_patch.md` | benchmark | physical_robustness | §2(#5), §3(B3), §5.6, §6(rank 6) |
| `docs/notes/he2024_rauca_vehicle_camouflage.md` | benchmark | physical_robustness | §5.4 |
| `docs/notes/hoory2020_dynamic_patch.md` | method_to_borrow | physical_robustness | §2(#12), §4.2, §5.3, §6(rank 3), §6(rank 4) |
| `docs/notes/hu2021_naturalistic_patch.md` | benchmark | physical_robustness | §2(#7), §4.1, §5.1 |
| `docs/notes/hu2022_advtexture_physical.md` | benchmark | physical_robustness | §4.2 |
| `docs/notes/huang2019_universal_physical_camouflage.md` | benchmark | physical_robustness | (context only; confirms cloth deformation lineage) |
| `docs/notes/huang2022_tsea_transfer.md` | method_to_borrow | cross_yolo_transfer | §2(#3), §3(B1), §6(rank 2) |
| `docs/notes/huang2025_advreal_physical.md` | benchmark | physical_robustness | §2(#4), §2(#5), §2(#7), §2(#12), §3(B3), §4.2, §5.1, §5.6, §6(rank 4), §6(rank 6) |
| `docs/notes/ji2021_adversarial_yolo_defense.md` | defense_baseline | physical_robustness | §2(#10), §4.5, §6(rank 9) |
| `docs/notes/jia2022_fooling_the_eyes_autonomous_vehicles.md` | method_to_borrow | cross_yolo_transfer | (context only; TSR, not cited in §§2–6) |
| `docs/notes/kolter2019_global_patch_suppression.md` | threat_model_contrast | generic_context | §3(B8), §6(rank 7) |
| `docs/notes/kurakin2017_physical_adversarial_examples.md` | foundational | generic_context | (context only; not cited in §§2–6) |
| `docs/notes/li2025_uvattack_nerf_person.md` | method_to_borrow | physical_robustness | §5.5 |
| `docs/notes/liang2021_catch_you_defense.md` | defense_baseline | physical_robustness | §4.5 |
| `docs/notes/liang2021_parallel_rectangle_flip_attack.md` | benchmark | cross_yolo_transfer | (context only; not cited in §§2–6) |
| `docs/notes/liang2024_open_environment_detectors.md` | survey_frame | yolo26_architecture_mismatch | (context only; framing, not cited in §§2–6) |
| `docs/notes/liao2021_anchor_free_adversarial.md` | architecture_explanation | yolo26_architecture_mismatch | §4.1 |
| `docs/notes/lin2024_nutnet_defense.md` | defense_baseline | physical_robustness | §2(#10), §4.5, §6(rank 8), §6(rank 9) |
| `docs/notes/liu2019_dpatch.md` | foundational | cross_yolo_transfer | §2(#8), §3(B8), §6(rank 7) |
| `docs/notes/liu2025_dome_detr.md` | architecture_explanation | yolo26_architecture_mismatch | (context only; framing, not cited in §§2–6) |
| `docs/notes/liu2025_gan_traffic_sign_patch_defense.md` | benchmark | generic_context | §5.4 |
| `docs/notes/lovisotto2022_attention_patch_robustness.md` | architecture_explanation | yolo26_architecture_mismatch | §2(#11), §3(B6), §4.3 |
| `docs/notes/lu2022_fran_frequency_attention.md` | method_to_borrow | physical_robustness | (context only; frequency-domain framing) |
| `docs/notes/lv2025_rt_datr_domain_adaptation.md` | architecture_explanation | cross_yolo_transfer | (context only; not cited in §§2–6) |
| `docs/notes/ma2025_cdupatch_dual_modal.md` | method_to_borrow | cross_yolo_transfer | §5.4 |
| `docs/notes/na2025_unmanned_stores.md` | deployment_motivation | generic_context | (context only; deployment framing) |
| `docs/notes/nazeri2024_detr_robustness.md` | architecture_explanation | yolo26_architecture_mismatch | §4.3 |
| `docs/notes/patchzero2022_detect_zero_defense.md` | defense_baseline | physical_robustness | §4.4, §4.5, §6(rank 8) |
| `docs/notes/pathak2024_model_agnostic_uav_defense.md` | defense_baseline | physical_robustness | §4.5 |
| `docs/notes/pavlitska2025_fool_stoplight.md` | benchmark | physical_robustness | §5.4 |
| `docs/notes/redmon2016_yolo.md` | architecture_explanation | generic_context | (context only; not cited in §§2–6) |
| `docs/notes/saha2020_spatial_context_yolo.md` | architecture_explanation | generic_context | §2(#8), §3(B8), §6(rank 7) |
| `docs/notes/schack2024_real_world_challenges.md` | physical_caveat | physical_robustness | §2(#4), §2(#12), §4.2, §4.4, §5.6, §6(rank 3), §6(rank 4) |
| `docs/notes/shen2025_revisiting_patch_defenses_detectors.md` | defense_baseline | cross_yolo_transfer | §2(#10), §4.4 |
| `docs/notes/szegedy2014_intriguing_properties.md` | foundational | generic_context | (context only; not cited in §§2–6) |
| `docs/notes/tan2024_DOEPatch.md` | method_to_borrow | cross_yolo_transfer | §3(B7), §6(rank 10) |
| `docs/notes/tang2023_hotcold_block_infrared.md` | benchmark | physical_robustness | §5.4 |
| `docs/notes/tereshonok2025_anomaly_localization_defense.md` | defense_baseline | physical_robustness | §4.5 |
| `docs/notes/thys2019_fooling_surveillance.md` | foundational | physical_robustness | §2(#8) |
| `docs/notes/tian2020_fcos_anchor_free_detector.md` | architecture_explanation | yolo26_architecture_mismatch | (context only; not cited in §§2–6) |
| `docs/notes/wang2022_fca_vehicle_camouflage.md` | method_to_borrow | cross_yolo_transfer | §5.4 |
| `docs/notes/wang2024_yolov10_end_to_end.md` | architecture_explanation | yolo26_architecture_mismatch | §2(#1), §3(B4), §4.3, §6(rank 5) |
| `docs/notes/wei2024_camera_agnostic_CAP.md` | method_to_borrow | physical_robustness | §4.2 (via outdoor penalty); §5.5 adjacent |
| `docs/notes/winter2026_benchmarking_robustness.md` | architecture_explanation | yolo26_architecture_mismatch | (context only; non-patch benchmark) |
| `docs/notes/wu2020_invisibility_cloak.md` | benchmark | physical_robustness | §4.2 |
| `docs/notes/wu2024_NAPGuard.md` | defense_baseline | physical_robustness | §2(#7), §2(#10), §4.5, §5.1 |
| `docs/notes/xing2024_magic_contextual_patch_agents.md` | method_to_borrow | physical_robustness | §5.7 |
| `docs/notes/xu2020_adversarial_tshirt.md` | benchmark | physical_robustness | §2(#4), §2(#5), §2(#12), §3(B3), §4.2, §5.6, §6(rank 4), §6(rank 6) |
| `docs/notes/xue2020_3d_invisible_cloak.md` | benchmark | physical_robustness | §4.2 |
| `docs/notes/yolo11_architecture_overview.md` | architecture_explanation | yolo11_coverage | §2(#9) |
| `docs/notes/zhao2023_rtdetr_realtime_end_to_end.md` | architecture_explanation | yolo26_architecture_mismatch | §4.3 |
| `docs/notes/zhou2021_nms_free_object_detection.md` | method_to_borrow | yolo26_architecture_mismatch | §2(#1), §3(B4), §4.3, §6(rank 5) |
| `docs/notes/zhou2023_mvpatch.md` | method_to_borrow | cross_yolo_transfer | §3(B7), §6(rank 10) |
| `docs/notes/zhou2025_sequence_level_clothing.md` | benchmark | physical_robustness | §4.4 |
| `docs/notes/zhu2023_tpatch_triggered_physical_patch.md` | threat_model_contrast | physical_robustness | §5.3 |
| `docs/notes/zhu2024_infrared_car_stickers.md` | benchmark | cross_yolo_transfer | §5.4 |
| `docs/notes/zimmermann2026_kgfp_failure_prediction.md` | runtime_monitoring | physical_robustness | §4.4 |
| `docs/notes/zimon2022_adversarial_patches_challenge.md` | lightweight_reference | generic_context | (context only; not cited in §§2–6) |
| `docs/notes/zolfi2021_translucent_patch.md` | benchmark | physical_robustness | §5.4 |
| `docs/notes/zong2022_codetr_hybrid_assignments.md` | method_to_borrow | yolo26_architecture_mismatch | §2(#1), §3(B4), §4.3, §6(rank 5) |

### Single-paper-exception flags

The following recommendations cite only one full note because the corpus has only one direct paper for that topic. This is permitted by the plan's rules and called out here explicitly.

- **B5 (Superpixel / SLIC + IFT)** — only `docs/notes/bagley2025_dynamically_optimized_clusters.md` addresses this mechanism directly with a YOLOv8-direct number. `priority: P1` rather than P0 in part because of this single-paper evidence.
- **Top Takeaway #9 (YOLO11 thin coverage)** — this is a corpus-level observation rather than a supported recommendation; the thinness is itself the finding.

---

## Coverage & integrity notes

- 78 `page_cited` notes appear in the Evidence Appendix exactly once each.
- 10 `blocked_access` notes appear only in § 7 and zero appear in the Evidence Appendix.
- Four repo-question lanes covered in § 2: `cross_yolo_transfer` (#2, #3), `physical_robustness` (#4, #5, #6, #12), `yolo26_architecture_mismatch` (#1, #11), `yolo11_coverage` (#9). `yolo11_coverage` remains thin by design (2 `page_cited` notes plus 1 blocked comparator).
- All § 6 Queue items cite ≥ 1 full note; ranks 1–3 each cite ≥ 2.
- Current repo capabilities (existing `patch_cutout`, `apply_self_ensemble`, `apply_cloth_eot`, adaptive `--co-weight-mode`, `--co-model`, `--multi-placement`, `--placement-regime`, `--loss-source`, `--v26-loss-mode hybrid`, `block_erase`, `nps_loss`, `tv_loss`, `failure_grid.py`, `physical_benchmark.py`) are called out as baseline in § 1 and § 4.5 so no queue item duplicates them as net-new code.
