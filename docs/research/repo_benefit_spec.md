# Research-to-Repo Benefit Spec

Generated: 2026-04-16  
Audience: internal engineering and planning  
Scope: turn the live research-note corpus into a ranked opportunity sheet for `Adversarial_Patch` and the broader `YOLO-Bad-Triangle` project, with no code changes in this pass

## Inputs Used

- Live note corpus: `docs/notes/*.md`
- Current repo state: `README.md`, `experiments/ultralytics_patch.py`, `experiments/physical_benchmark.py`, `experiments/defense_eval.py`
- Existing planning/synthesis docs: `docs/research/robustness_evaluation_queue.md`, `docs/research/master_paper_pool.md`, `docs/research/yolo_patch_evidence_matrix.md`

## Current-State Snapshot

- Cross-model transfer is still constrained by nano-source experiments. The repo has a live transfer matrix and fixed-weight joint training, but the current results still show weak source-to-target generalization on harder model pairs.
- Physical robustness is partially modeled, not fully characterized. The training loop already includes `block_erase`, `patch_cutout`, `rotate_patch_eot`, `nps_loss`, and `TV` regularization, and the repo has `experiments/physical_benchmark.py`, but the current path does not yet cover cloth deformation, relighting, camera ISP modeling, or a Schack-style digital failure grid.
- YOLO26 objective design is still an architecture-mismatch problem. The repo already has a `one2one` hook path, `one2many` ablation path, `topk` versus `logsumexp`, and `multi-placement`, but it still lacks a decision-complete loss and metric framework for end-to-end selected-query behavior.
- Defense coverage is currently narrow. `experiments/defense_eval.py` only benchmarks preprocessing defenses (`jpeg`, `blur`, `crop_resize`); stronger literature-backed defenses still live outside the repo.

## Canonical Opportunity Schema

All ranked sections below use the same fields:

- `rank`
- `lane`
- `status`
- `boundary`
- `opportunity`
- `literature_basis`
- `current_repo_state`
- `proposed_work`
- `expected_benefit`
- `validation_plan`
- `risk_or_blocker`

Fixed labels:

- `lane`: `cross_yolo_transfer`, `physical_robustness`, `yolo26_architecture_mismatch`, `defense_eval`
- `status`: `already_present`, `partial`, `missing`
- `boundary`: `this_repo`, `handoff_to_yolo_bad_triangle`, `blocked_watchlist`

Ranking rule for this sheet:

1. current-repo implementability
2. broader-project handoff value
3. literature novelty

---

## Cross-Model Transfer

| rank | lane | status | boundary | opportunity | literature_basis | current_repo_state | proposed_work | expected_benefit | validation_plan | risk_or_blocker |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `cross_yolo_transfer` | `already_present` | `this_repo` | Fixed-weight joint multi-model training baseline | `dimitriu2024_multi_model_transferability`, `tan2024_DOEPatch` | `experiments/ultralytics_patch.py` already supports `--co-model` and `--co-weight`; `README.md` already reports joint patch results. | No new work in this pass. Treat current fixed-weight co-training as the baseline every new transfer idea must beat. | Prevents duplicate work and gives later transfer experiments a stable comparison point. | Reuse the current joint-patch result surfaces and keep future rows comparable to the existing `README.md` tables. | Already implemented; not a new recommendation. |
| 2 | `cross_yolo_transfer` | `partial` | `this_repo` | Larger-source compatibility matrix before more nano-only tuning | `bayer2024_network_transferability` | The repo reports transfer only among nano-family artifacts and does not yet expose a compatibility-matrix view across source-model sizes. | Add a work package that compares at least one larger source model against the current nano baselines and reports a source-to-target matrix rather than isolated transfer pairs. | Separates model-size effects from loss-design effects and may explain whether current weak transfer is mostly a nano-source artifact. | Compare matrix cells against the current v8n/v11n/v26n transfer table and report whether larger sources materially improve cross-model suppression. | Higher compute cost and larger-model training time. |
| 3 | `cross_yolo_transfer` | `partial` | `this_repo` | Self-ensemble transfer ablation on top of the current pipeline | `huang2022_tsea_transfer`, `cheng2024_depatch_decoupled` | `patch_cutout` is already implemented, but the repo has no ShakeDrop-style self-ensemble path and no explicit transfer ablation isolating cutout versus ensemble effects. | Extend the transfer lane with a literature-matched ablation pack: baseline, cutout-only, self-ensemble-only, and combined. | Highest-likelihood short-path improvement for black-box transfer without replacing the current optimizer. | Hold source-model direct suppression constant, then compare transfer deltas on v11n and v26n against the current baseline. | ShakeDrop is architecture-sensitive; adaptation to Ultralytics backbones may require approximation rather than a literal port. |
| 4 | `cross_yolo_transfer` | `partial` | `this_repo` | Mixed-surrogate training with dynamic weight schedules | `dimitriu2024_multi_model_transferability`, `tan2024_DOEPatch`, `zhou2023_mvpatch` | The repo can sum losses across co-models, but weighting is static and the training surfaces are still centered on a small set of paired runs. | Add a mixed-surrogate work package that trains against multiple source families with dynamic weighting rather than fixed equal or hand-picked weights. | Better cross-family transfer and less overfitting to a single source detector's gradient landscape. | Report the same direct and transfer metrics already used in the repo, plus a per-source contribution summary for each training schedule. | Search space expands quickly; needs strong experiment discipline to avoid combinatorial sprawl. |
| 5 | `cross_yolo_transfer` | `missing` | `this_repo` | Position-independent and off-object transfer framing | `liu2019_dpatch`, `saha2020_spatial_context_yolo` | Current placement logic is torso-centered by default, with optional multi-placement over detected persons; it does not separate target-overlap dependence from general detector suppression. | Add an evaluation lane for off-object and position-independent placements so transfer claims can distinguish person-vanishing from broader detector disruption. | Improves threat-model clarity and makes transfer numbers more interpretable. | Compare torso-overlap placement versus off-object placement on the same manifest and report the gap explicitly. | May lower headline suppression, but the result is scientifically cleaner. |

---

## Physical Robustness and Evaluation

| rank | lane | status | boundary | opportunity | literature_basis | current_repo_state | proposed_work | expected_benefit | validation_plan | risk_or_blocker |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `physical_robustness` | `already_present` | `this_repo` | Baseline physical pipeline and benchmark harness | `thys2019_fooling_surveillance`, `cheng2024_depatch_decoupled`, `schack2024_real_world_challenges` | The repo already has `rotate_patch_eot`, `nps_loss`, `block_erase`, `patch_cutout`, print export in `live_demo.py`, and `experiments/physical_benchmark.py` for structured live capture. | No new work in this pass. Treat the current augmentation and benchmark surfaces as the baseline that later physical methods must extend, not replace blindly. | Prevents the spec from recommending techniques that are already in the codebase. | Preserve current benchmark outputs as the control condition for any future robustness expansion. | Already implemented, but incomplete relative to the literature. |
| 2 | `physical_robustness` | `partial` | `this_repo` | EoT coverage audit plus Schack-style failure grid | `schack2024_real_world_challenges`, `bagley2025_dynamically_optimized_clusters`, `hoory2020_dynamic_patch` | The repo can run a live distance-yaw-lighting benchmark, but it does not yet expose a digital benchmark grid over hue, size, brightness, and rotation failure modes. | Expand the physical evaluation lane so the repo documents the exact robustness envelope instead of only offering a live benchmark harness. | Replaces qualitative physical caveats with a measurable boundary of what the patch can and cannot survive. | Report condition-wise performance over size, rotation, brightness, and hue, then compare those results against the current live benchmark outputs. | More evaluation complexity without immediate attack gains; still worth it because it tightens claims. |
| 3 | `physical_robustness` | `partial` | `this_repo` | Cloth deformation and non-rigid augmentation upgrade | `guesmi2024_DAP_dynamic_adversarial_patch`, `xu2020_adversarial_tshirt`, `huang2025_advreal_physical`, `cheng2024_depatch_decoupled` | Current robustness augmentations are mostly rigid or masking-oriented: rotation, cutout, block erase, and printability regularization. | Add a next-phase augmentation pack for cloth-specific distortion: creases, TPS-like deformation, non-rigid cloth warping, and relight matching. | Most direct literature-backed route from digital success toward stronger physical carryover. | Benchmark the new augmentation family against the existing physical baseline using the same printed artifact workflow and condition matrix. | Highest engineering effort in the physical lane because non-rigid augmentation needs careful differentiable integration. |
| 4 | `physical_robustness` | `missing` | `this_repo` | Camera ISP and relighting realism | `wei2024_camera_agnostic_CAP`, `huang2025_advreal_physical`, `schack2024_real_world_challenges` | The repo acknowledges printer color shift and lighting limits, but the training loop does not model camera ISP or explicit relighting beyond current augmentations. | Add a research work package for differentiable camera/lighting modeling so physical transfer is not treated as a black-box post-hoc phenomenon. | Better alignment between digitally optimized patches and real camera capture conditions. | Compare current physical benchmark results against an ISP-aware or relight-aware training variant on the same artifact and camera setup. | Likely heavy implementation cost; should follow the simpler EoT audit before deeper realism modeling. |
| 5 | `physical_robustness` | `partial` | `this_repo` | Better physical reporting: viewpoint sectors and protocolized summaries | `hoory2020_dynamic_patch`, `bagley2025_dynamically_optimized_clusters`, `delacruz2026_physical_attacks_surveillance` | The current benchmark logs condition rows, but repo-facing reporting is still mostly pooled summary language rather than sector-by-sector interpretation. | Promote sector-based reporting: best-per-range, worst-per-range, and protocolized summaries by distance, yaw, and lighting. | Makes physical results more diagnostic and easier to compare across artifacts. | Require every physical benchmark summary to include per-sector breakdowns rather than only one pooled suppression number. | More reporting overhead, but low implementation risk. |

---

## YOLO26 / End-to-End Objective Design

| rank | lane | status | boundary | opportunity | literature_basis | current_repo_state | proposed_work | expected_benefit | validation_plan | risk_or_blocker |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `yolo26_architecture_mismatch` | `already_present` | `this_repo` | One-to-one gradient hook and ablation baseline | `wang2024_yolov10_end_to_end`, `zhou2021_nms_free_object_detection` | `experiments/ultralytics_patch.py` already supports `--loss-source auto|one2many|one2one`, a live `one2one` hook path, `--v26-loss-mode topk|logsumexp`, and `--multi-placement`. | No new work in this pass. Treat the current one-to-one pipeline as the minimum baseline for all future YOLO26 work. | Prevents the spec from restating work that the repo already did correctly. | Future YOLO26 variants must report against the current `one2one` and `one2many` baselines, not against an older dense-only path. | Already implemented, but still not sufficient to close the YOLO26 gap. |
| 2 | `yolo26_architecture_mismatch` | `partial` | `this_repo` | Selected-query objective pack for end-to-end inference | `wang2024_yolov10_end_to_end`, `zhou2021_nms_free_object_detection`, `zhao2023_rtdetr_realtime_end_to_end` | The repo can optimize one-to-one scores, but it still treats them largely as a score field rather than as a selected-query decision process with explicit bookkeeping. | Formalize a chosen-query work package that targets the selected one-to-one positives rather than only top-k score aggregates. | Most plausible path to improving YOLO26-specific attack alignment without abandoning the current codebase. | Compare selected-query objectives against current `topk` and `logsumexp` v26 baselines on the same manifest and report per-head behavior. | More brittle than dense loss functions; mistakes here can silently overfit to the wrong path. |
| 3 | `yolo26_architecture_mismatch` | `partial` | `this_repo` | Dual-head and auxiliary-supervision loss schedule | `zong2022_codetr_hybrid_assignments`, `wang2024_yolov10_end_to_end`, `liao2021_anchor_free_adversarial` | The repo can switch between `one2many` and `one2one`, but it does not yet implement a coordinated objective that treats the dual-head structure as a design opportunity rather than a binary choice. | Add a work package for auxiliary supervision or positive-query surrogates that intentionally couples dense and selected outputs. | Could recover signal from the auxiliary head without ignoring the inference head that actually matters. | Require paired ablations: one-to-one only, one-to-many only, and coordinated dual-head objectives, each evaluated on the same YOLO26 artifact set. | High research risk; may improve optimization signal or simply add noise. |
| 4 | `yolo26_architecture_mismatch` | `missing` | `this_repo` | Transformer-style metric separation for YOLO26 studies | `winter2026_benchmarking_robustness`, `nazeri2024_detr_robustness` | Current repo summaries focus on suppression percentages and clean-to-patched count drops; they do not separate localization failure from confidence collapse or track perceptual distance metrics. | Extend the YOLO26 evaluation lane with separated localization/classification metrics and a perceptual-quality control metric. | Makes YOLO26 failures interpretable instead of collapsing them into one headline suppression number. | Add metric outputs that distinguish missed localization, score collapse, and perceptual distortion, then compare against current suppression summaries. | Additional metrics may complicate reporting, but they reduce ambiguity. |
| 5 | `yolo26_architecture_mismatch` | `missing` | `this_repo` | Attention-routing analysis for sparse end-to-end detectors | `alam2023_attention_deficit_deformable`, `lovisotto2022_attention_patch_robustness`, `zhao2023_rtdetr_realtime_end_to_end` | The repo currently treats YOLO26 primarily as a score-path problem; it does not yet inspect whether sparse routing and attention selection are the deeper bottlenecks. | Add a diagnostic work package that splits routing or query-selection behavior from downstream score suppression. | Would clarify whether the next YOLO26 improvement should target routing, scoring, or both. | Pair any new diagnostic with the existing one-to-one baseline and require an explanation of where the suppression attempt fails. | Highest uncertainty in the YOLO26 lane; useful only after the simpler selected-query work is exhausted. |

---

## Defense and Recovery Baselines

| rank | lane | status | boundary | opportunity | literature_basis | current_repo_state | proposed_work | expected_benefit | validation_plan | risk_or_blocker |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `defense_eval` | `already_present` | `this_repo` | Preprocessing defense sweep baseline | `schack2024_real_world_challenges`, `wei2024_camera_agnostic_CAP` | `experiments/defense_eval.py` already benchmarks `jpeg`, `blur`, and `crop_resize` and reports clean-cost versus attack-reduction tradeoffs. | No new work in this pass. Treat the current preprocessing sweep as the defense floor every stronger baseline must exceed. | Keeps future defense work honest about what simple preprocessing already achieves. | Reuse the current `defense_results.json` and `defense_report.md` surfaces as the baseline comparator. | Already implemented; not a recommendation for new work. |
| 2 | `defense_eval` | `missing` | `handoff_to_yolo_bad_triangle` | Patch-class detector baseline | `ji2021_adversarial_yolo_defense` | The current repo has no retraining-based detector defense; the canonical runtime boundary in `README.md` points future runtime defenses to `YOLO-Bad-Triangle`. | Hand off the strongest direct defense baseline: add an `adversarial_patch` class and evaluate clean-versus-attacked recovery. | Highest-confidence literature-backed defense candidate with direct YOLO relevance. | Measure clean AP cost and attacked AP recovery against the existing preprocessing baseline. | Requires model retraining and belongs in the canonical defense pipeline rather than this artifact repo. |
| 3 | `defense_eval` | `missing` | `handoff_to_yolo_bad_triangle` | Segment-and-recover defense | `gu2025_SAR_segment_recover`, `lin2024_nutnet_defense` | No patch localization, segmentation, or restoration path exists in the current repo. | Hand off a segment-mask-recover baseline that localizes the patch and repairs the region before rerunning detection. | Stronger recovery path than simple preprocessing and closer to current detector-defense literature. | Compare attacked AP before and after recovery, plus clean false-positive cost, against the preprocessing and patch-class baselines. | Depends on additional segmentation or inpainting components not present here. |
| 4 | `defense_eval` | `missing` | `handoff_to_yolo_bad_triangle` | Mask-and-zero / PatchZero-style defense | `patchzero2022_detect_zero_defense` | The repo does not currently benchmark explicit patch masking or zero-out defenses. | Hand off a masking baseline that detects candidate patch regions and measures zero-out recovery under attack. | Adds a simple but literature-backed recovery control between preprocessing and full restoration. | Evaluate clean-cost and attack-reduction metrics on the same patched inputs used by the current defense sweep. | May over-mask natural image regions; needs adaptive-attack caveats in reporting. |
| 5 | `defense_eval` | `missing` | `handoff_to_yolo_bad_triangle` | Frequency and anomaly screening baseline | `wu2024_NAPGuard`, `tereshonok2025_anomaly_localization_defense`, `lu2022_fran_frequency_attention` | The current repo does not audit patch frequency signatures or clean-data anomaly detection behavior. | Hand off a cheap detection-side baseline that measures FFT or anomaly-localization signals before deeper recovery models are added. | Low-cost filter baseline for deciding whether more complex defenses are warranted. | Benchmark false positives on clean frames and detection of patched frames before any recovery step. | Risk of weak generalization to naturalistic or low-frequency patches. |

---

## Top 5 Next Candidates

1. **Larger-source compatibility matrix**
   Landing zone: `this_repo`
   Why first: strongest short path for explaining whether current transfer weakness is mostly a source-model-size problem.

2. **Self-ensemble transfer ablation on top of the current cutout path**
   Landing zone: `this_repo`
   Why second: highest literature-backed chance of improving transfer without redesigning the whole pipeline.

3. **EoT coverage audit plus Schack-style physical failure grid**
   Landing zone: `this_repo`
   Why third: closes the biggest measurement gap in current physical claims with relatively low conceptual risk.

4. **Selected-query / dual-head YOLO26 objective pack**
   Landing zone: `this_repo`
   Why fourth: the main unresolved architecture problem is still YOLO26-specific optimization mismatch.

5. **Patch-class defense baseline**
   Landing zone: `handoff_to_yolo_bad_triangle`
   Why fifth: strongest direct defense result in the corpus, but it belongs in the canonical defense runtime rather than this repo.

## Blocked Watchlist

Only `blocked_access` note ideas appear here. None of these should enter the main ranked backlog until the missing full text or citation details are resolved.

| blocked item | lane | why blocked | if unblocked, what it could change |
|---|---|---|---|
| `wang2026_chosen_object` | `yolo26_architecture_mismatch` | No local PDF; exact Hungarian-matching loss, datasets, and ablations are still unavailable. | Could materially tighten the selected-query / YOLO26 objective lane. |
| `li2025_elevpatch` | `defense_eval` | No local PDF; the only YOLO11-specific attack comparison paper is still unread at full-text level. | Could change the benchmarking target for YOLO11-specific evaluation. |
| `zimon2025_GAN_YOLO` | `cross_yolo_transfer` | No local PDF; near-scope v3/v5/v8/v11 benchmark tables and transfer claims are blocked. | Could sharpen the transfer benchmark lane and the broader-project handoff story. |
| `imran2025_tkpatch` | `cross_yolo_transfer` | No local PDF; the exact Top-K multi-YOLO results and loss details are still blocked. | Could add a more direct alternative to current top-k transfer objectives. |
| `bae2020_TOG` | `yolo26_architecture_mismatch` | Citation identity and full text still unverified. | Could add an NMS-era contrast loss for v8/v11 ablations, not for YOLO26 directly. |
| `lin2024_entropy` | `physical_robustness` | No local PDF; entropy-naturalism method details and numbers are blocked. | Could add a lightweight naturalness regularizer to the physical lane. |
| `ma2026_XAIAD` | `defense_eval` | No local PDF; defense mechanism details are too incomplete for implementation. | Could become a stronger broader-project defense handoff candidate. |
| `truong2024_AYO_GAN` | `physical_robustness` | No local PDF; useful only at metadata level right now. | Mostly benchmarking and naturalism framing, not a near-term implementation target. |

## Defaults and Non-Goals

- This sheet is a planning document only. It does not change code, experiment outputs, or ranked data.
- Main-list candidates must stay grounded in `page_cited` notes and the current live repo state.
- `already_present` rows exist to prevent duplicate recommendations, not to expand the backlog.
- Defense work that changes runtime behavior should default to `YOLO-Bad-Triangle` unless the repo boundary changes later.
