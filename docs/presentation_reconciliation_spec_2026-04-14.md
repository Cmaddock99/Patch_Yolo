# Presentation Reconciliation Spec

Date: 2026-04-14

## Purpose

Make the presentation truthful before any polish pass.

Priority order:

1. Remove or qualify claims that are false, overstated, or scoped too broadly.
2. Sync the visible deck, PPT generator, and speaker notes so they do not drift.
3. Apply small cleanup items that reduce future confusion.

This spec is written for another agent to implement without re-running the audit.

## Source Of Truth

Use these artifacts as the factual baseline for the current workspace state.

Attack-side repo: `Adversarial_Patch`

- Direct suppression:
  - `outputs/yolov8n_patch_v2/results.json`
  - `outputs/yolo11n_patch_v2/results.json`
  - `outputs/yolo26n_patch_v2/results.json`
- Current `v2` transfer artifacts:
  - `outputs/yolo11n_from_yolov8n_patch_v2_transfer/results.json`
  - `outputs/yolo26n_from_yolov8n_patch_v2_transfer/results.json`
  - `outputs/yolov8n_from_yolo11n_patch_v2_transfer/results.json`
  - `outputs/yolo26n_from_yolo11n_patch_v2_transfer/results.json`
  - `outputs/yolov8n_from_yolo26n_patch_v2_transfer/results.json`
  - `outputs/yolo11n_from_yolo26n_patch_v2_transfer/results.json`
- Joint and warm-start artifacts:
  - `outputs/yolov8n+yolo11n_joint_patch_v2/results.json`
  - `outputs/yolov8n_from_yolov8n+yolo11n_joint_patch_v2_transfer/results.json`
  - `outputs/yolo11n_from_yolov8n+yolo11n_joint_patch_v2_transfer/results.json`
  - `outputs/yolov8n+yolo26n_joint_patch_v2/results.json`
  - `outputs/yolo26n_from_yolov8n+yolo26n_joint_patch_v2_transfer/results.json`
  - `outputs/yolo26n_patch_v2_warmstart/results.json`
  - `outputs/yolov8n_from_yolo26n_warmstart_transfer/results.json`
  - `outputs/yolo11n_from_yolo26n_warmstart_transfer/results.json`
  - `outputs/yolo26n_patch_v3_one2one/results.json`
- Defense benchmark:
  - `outputs/defense_eval/defense_report.md`
  - `outputs/defense_eval/defense_results.json`
- Demo and print support:
  - `experiments/live_demo.py`
  - `experiments/physical_benchmark.py`

Defense-side repo: `../ml-labs/YOLO-Bad-Triangle`

- Repo overview and artifact policy:
  - `README.md`
  - `docs/LOOP_DESIGN.md`
  - `docs/TEAM_MANUAL.md`
  - `docs/FRESH_CLONE_SETUP.md`
- Current attack/defense catalogue:
  - `scripts/auto_cycle.py`
- Current defense implementation identity:
  - `src/lab/defenses/preprocess_dpc_unet_adapter.py`
- Current cycle and report artifacts:
  - `outputs/cycle_history/cycle_20260407_193440.json`
  - `outputs/cycle_report.md`
  - `outputs/cycle_report.csv`
  - `outputs/eval_ab_clean.json`
- Current DPC-UNet direction status:
  - `docs/DIRECTION_A_SPEC.md`

## Files To Edit

Required presentation-source files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`

Required support-file sync:

- `README.md`

Optional only if the user later asks for it:

- `presenter_guide.txt`

Do not hand-edit `presentation.pptx`. Regenerate it from `scripts/html_to_pptx.py` after the source copy is fixed.

## Global Rules

- Treat the two repos as complementary sibling projects, not one merged runtime pipeline.
- Do not claim the two repos share one image set. They do not.
- When quoting attack-side transfer numbers, use one consistent artifact family. Use current `v2` artifacts unless the slide is explicitly labeled `v1`.
- When quoting defense-side summary numbers, scope them to the latest canonical cycle or to the canonical post-switch series. Do not present them as repo-wide all-time truth without qualification.
- Call `c_dog` and DPC-UNet a denoiser or preprocessing defense, not a detector.
- Do not claim a fixed physical suppression percentage unless a committed benchmark artifact supports it.

## Slide-By-Slide Changes

### Slide 1

Status: Recommended wording downgrade

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`

On-slide subtitle replacement:

```text
Two complementary tracks for attack analysis and defense-cycle evaluation across YOLO generations
```

Reason:

The current subtitle says "two-track pipeline," which reads as a tighter integration than the repos support.

### Slide 2

Status: Required

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`

On-slide title replacement:

```text
Two Complementary Tracks
```

Attack-track bullet replacement:

```text
Cross-model transfer evaluation across YOLO generations
```

Defense-track bullet replacements:

```text
22 recorded automated cycles in the defense repo
DPC-UNet checkpoint finetuning with clean A/B deployment gate
```

Bottom paragraph replacement:

```text
These are complementary sibling repos, not one shared-image runtime loop: the attack track uses a 48-image common manifest, while the defense track runs automated cycles on a COCO subset and writes its own reports.
```

Presenter guide slide-2 script replacement:

```text
"This project has two complementary tracks, but they are not one merged runtime pipeline. The attack repo trains and evaluates adversarial patches on a 48-image common manifest across YOLOv8n, YOLO11n, and YOLO26n. The defense repo runs automated attack-defense cycles on a COCO subset and records cycle reports, checkpoint evaluations, and provenance-tracked artifacts. I’m presenting them together as sibling results from the same research direction, not as one shared-image loop."
```

### Slide 3

Status: No factual change required

Keep the current direct suppression numbers.

### Slide 4

Status: Required

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`
- `README.md`

Use current `v2` transfer artifacts for the whole direct matrix.

Direct matrix replacement:

```text
v8n row: 90.0, 33.3, 14.0
v11n row: 50.0, 72.7, 9.3
v26n row: 45.0, 24.2, 16.3
```

Asymmetry card replacement:

```text
v11n→v8n = 50.0% > v8n→v11n = 33.3%

The asymmetry remains in the current v2 artifacts: newer-generation patches still reach backward better than older patches reach forward.
```

`v26n firewall` card replacement:

```text
v26n remains the hardest target in this study. Nothing in the direct matrix exceeds 16.3% against it, and even the best joint patch only reaches 18.6%. Yet the v26n patch still transfers out at 45.0% and 24.2%.
```

Presenter guide slide-4 script replacement:

```text
"This matrix uses the current v2 transfer artifacts. The white-box diagonal is unchanged, but two v8n-source off-diagonal values move to 33.3 percent on v11n and 14.0 percent on v26n. The asymmetry still holds because v11n to v8n is 50 percent. And v26n is still the hardest target: nothing in the direct matrix exceeds 16.3 percent against it, while the best joint patch only reaches 18.6 percent."
```

Presenter guide slide-4 explainer replacement:

```text
- `Asymmetry`: `v11n -> v8n` works better than `v8n -> v11n` even in the current `v2` artifacts.
```

README transfer matrix replacement:

```text
| v8n → v11n | 33.3% |
| v11n → v8n | 50.0% |
| v26n → v8n | 45.0% |
| v26n → v11n | 24.2% |
| v8n → v26n | 14.0% |
| v11n → v26n | 9.3% |
```

README transfer-asymmetry sentence replacement:

```text
**Transfer asymmetry:** v11n → v8n transfers better (50%) than v8n → v11n (33.3%), suggesting v11n's adversarial features are a superset. v26n patches transfer well to v8n/v11n despite low self-suppression.
```

### Slide 5

Status: Recommended cleanup

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`

Crop-resize paragraph replacement:

```text
High variance across seeds. At 95% and 90% retention there is no reliable benefit. Some 85% retention and isolated 90% retention seeds reduce suppression, but the effect is unstable and often trades off against clean detections.
```

Presenter guide slide-5 script replacement:

```text
"A natural defense idea is to blur, compress, or crop-resize the image before it reaches the detector. Here, blur and JPEG usually fail or make the patch stronger. Crop-resize occasionally helps at stronger crops, but it is too unstable to present as a reliable defense."
```

### Slide 6

Status: No required numeric change

Keep the current visible experiment table, but do not broaden the conclusion beyond "in the current setup."

### Slide 7

Status: Required

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`

Intro paragraph replacement:

```text
This slide uses the latest canonical cycle from YOLO-Bad-Triangle. The repo records 22 cycles overall, but this snapshot is cycle 22 from the current `attack_then_defense` series. Latest validated attacks: deepfool, dispersion reduction, and square. Active defenses: JPEG, median filter, bit-depth reduction, and c_dog.
```

Table row label replacements:

```text
Clean baseline
Worst latest-cycle attack    dispersion_reduction
Best latest-cycle defended config    square + c_dog
```

Adversarial finetuning card replacement:

```text
DPC-UNet denoiser checkpoint finetuned on adversarial image pairs (square ×5 oversample + DeepFool + blur + square pairs). Candidate deployed only after clean A/B comparison against the current c_dog checkpoint.
```

Adversarial finetuning bullets replacement:

```text
Clean performance: +0.0025 mAP50 versus previous checkpoint — no regression
Attack resistance: Δ within noise — no measurable gain yet
```

State-of-play card replacement:

```text
No universal defense has emerged. In the current canonical series, c_dog is strongest on square, while median preprocessing is stronger on deepfool. Finetuning is clean-safe but has not yet produced a measurable robustness gain.
```

Presenter guide slide-7 script replacement:

```text
"The defense track asks a different question: what does the latest canonical cycle show? In cycle 22, clean baseline is 0.600, dispersion reduction drops it to 0.238, and the strongest defended configuration in that same latest cycle is square plus c_dog at 0.394. That does not mean c_dog wins every matchup; in the current canonical series median preprocessing is stronger on deepfool. The honest summary is partial recovery, not a universal defense."
```

Presenter guide quick-reference label replacements:

```text
Latest-cycle worst attack mAP50 | 0.238
Latest-cycle strongest defended mAP50 | 0.394
Recorded automated cycles | 22
```

### Slide 8

Status: Required

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`

Replace the current "three-phase" framing with the real four-phase loop.

Methodology card title replacement:

```text
4-Phase Automation Pipeline
```

Methodology bullets replacement:

```text
Phase 1 — Characterize: smoke-rank candidate attacks
Phase 2 — Matrix: smoke-rank candidate defenses against top attacks
Phase 3 — Tune: coordinate-descent best attack and defense params
Phase 4 — Validate + report: full-dataset mAP50 validation and artifact/report generation
```

Methodology body replacement:

```text
Checkpoint promotion is a separate clean A/B step for the c_dog denoiser: deploy only if the candidate does not regress versus the current checkpoint.
```

Stat block replacements:

```text
22  recorded cycles
4   active defenses
5   canonical post-switch cycles
```

`c_dog` card title replacement:

```text
c_dog — strongest square defense in cycle 22
```

`c_dog` card body replacement:

```text
A DPC-UNet denoiser that preprocesses inputs before YOLO inference. In cycle 22, square + c_dog improves mAP50 from 0.363 to 0.394. It is not the strongest defense on every attack.
```

Checkpoint-finetuning bullet replacement:

```text
Architecture: DPC-UNet denoiser checkpoint
Mix: square ×5 oversample + DeepFool + blur + square pairs
Gate: deploy only if clean A/B does not regress vs current checkpoint
Result: +0.0025 clean mAP50 vs previous checkpoint — gate passed
Attack resistance: Δ within noise — open problem
```

Presenter guide slide-8 script replacement:

```text
"Mechanically, the loop is four phases, not three: characterize attacks, build a defense matrix, tune the best pair, then validate on the full dataset. The clean A/B gate is a separate checkpoint-promotion step for c_dog, not a claim that every cycle stays above the 0.600 no-defense baseline. The repo has 22 recorded cycles overall, but only the post-switch attack-then-defense series should be treated as the canonical current trend."
```

### Slide 9

Status: Required

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`
- `README.md`

Physical-print card replacement:

```text
Patch exported at 300 DPI, 8"×8".
Physical demos underperform digital because printer color shift, lighting, and view angle perturb the patch.
NPS loss during training partially compensates.
```

Presenter guide slide-9 script replacement:

```text
"In the demo, the left side shows the clean detector output and the right side shows the same feed with the patch digitally overlaid on the torso of the largest detected person. The bar at the bottom shows a rolling 30-frame suppression average so the result is readable instead of jittery. I can also show the physical version: an 8-by-8-inch print at 300 DPI. Physical performance is directionally lower than digital because printers, lighting, and viewing angles perturb the patch. The repo includes a structured physical benchmark script, but the committed presentation artifacts should not claim a fixed physical suppression percentage."
```

README physical note replacement:

```text
Physical suppression will be lower than digital because printer color shift, lighting, and viewing angle perturb the patch. The patch was trained with Non-Printability Score (NPS) loss to partially compensate. Use `experiments/physical_benchmark.py` for a structured physical benchmark instead of quoting a fixed percentage from the deck.
```

### Slide 10

Status: Required

Files:

- `presentation.html`
- `scripts/html_to_pptx.py`
- `presenter_guide.md`

Framework-contribution card replacement:

```text
Two complementary repos, not one merged pipeline: Adversarial_Patch reports cross-generation patch training and transfer on YOLOv8n, YOLO11n, and YOLO26n; YOLO-Bad-Triangle reports 22 recorded defense-cycle artifacts, with current canonical trends taken from the post-switch series.
```

Presenter guide slide-10 script replacement:

```text
"I’d close with three careful takeaways. First, the contribution is two complementary repos, not one merged pipeline: one captures patch training and cross-generation transfer, and the other captures automated defense-cycle evidence. Second, architecture still matters: YOLO26n breaks the usual assumption that optimizing the attack objective will directly reduce detections. Third, the defense repo shows partial recovery and clean-safe checkpoint updates, but not a universal defense."
```

Footer replacement:

```text
Attack repo → github.com/Cmaddock99/Patch_Yolo
Defense repo → github.com/Cmaddock99/YOLO-Bad-Triangle
```

## Non-Slide Cleanup

Status: Required

Files:

- `presentation.html`

Fix duplicate slide IDs.

Current problem:

- Defense benchmark slide uses `id="s4"`
- `v26n Paradox` slide also uses `id="s4"`

Required change:

- Rename the second one to a unique ID such as `s5`

Reason:

Arrow navigation currently survives because it iterates `.slide`, but duplicate DOM IDs make any future per-slide linking or scripting ambiguous.

## README Sync Scope

Apply the README edits only where they support the deck and remove stale or unsupported claims.

Required README updates:

- Transfer matrix numbers must match the chosen artifact family.
- Transfer asymmetry sentence must use `33.3%`, not `36.4%`, if the matrix is updated to `v2`.
- Physical note must remove the unsupported `~30–60%` claim.

No other README changes are required for this handoff.

## Implementation Notes

- `presentation.html` and `scripts/html_to_pptx.py` should end with the same visible wording.
- `presenter_guide.md` should match the final visible deck scope and terminology.
- Expect layout pressure on slides 2, 7, 8, and 10 after the copy changes. Adjust card widths, font size, or spacing as needed, but do not cut factual qualifiers to save space.
- Do not touch the untracked `presenter_guide.txt` unless the user explicitly asks for a `.txt` sync artifact.
- Be careful with the already-modified `presentation.pptx` in the worktree. Regenerate only after source copy is correct.

## Acceptance Criteria

The implementation is complete when all of the following are true.

- No slide claims that the two repos share one image set or one merged runtime loop.
- The transfer matrix uses one internally consistent artifact family.
- Slide 7 and Slide 8 clearly scope defense metrics to the latest canonical cycle or canonical post-switch series.
- `c_dog` and DPC-UNet are described as a denoiser or preprocessing defense, never as a detector.
- The deck no longer shows `0.238 -> 0.394` for `square + c_dog`.
- The deck no longer claims a fixed physical suppression range without benchmark artifacts.
- The conclusion slide cites both repos.
- `presentation.html`, `scripts/html_to_pptx.py`, `presenter_guide.md`, and `README.md` are mutually consistent.
- `presentation.pptx` is regenerated from `scripts/html_to_pptx.py`.

## Verification

After implementing the copy changes:

1. Run:

```bash
python scripts/html_to_pptx.py
```

2. Open `presentation.html` and visually confirm there is no overflow on slides 2, 4, 7, 8, 9, and 10.

3. Confirm the regenerated PPT contains the corrected visible copy.

4. Re-check these facts manually:

- Slide 4 uses `33.3` and `14.0` for the `v8n` transfer row.
- Slide 7 and Slide 8 no longer imply `c_dog` is best on every attack.
- Slide 8 no longer says the gate is `clean mAP50 >= 0.600`.
- Slide 9 no longer claims `~30–60%`.
- Slide 10 cites both repos.
