# Speaker Notes: Adversarial Robustness Framework

Revised speaker notes for the 10-slide deck. Each slide is split into:

- `Script`: what to say aloud
- `Explainer`: plain-English backup notes for Q&A or mixed audiences

## Slide 1 — Title

### Script

"Good morning. Today I’m going to show you a framework for attacking and defending AI object detectors, specifically YOLO, one of the most widely deployed real-time vision systems. The project has two parts: an attack pipeline that trains adversarial patches to suppress person detections, and a defense pipeline that runs attacks and defenses against each other in an automated loop. By the end, I want you to have a clear view of what worked, what failed, and why one newer YOLO architecture behaved very differently from the others."

### Explainer

- `YOLO`: "You Only Look Once," a fast family of object detectors used in surveillance, robotics, drones, and embedded vision.
- `Object detector`: a model that predicts boxes, labels, and confidence scores for things it sees.
- `v8n`, `v11n`, `v26n`: nano-sized versions of three YOLO generations. The `n` means the smallest and fastest model in each family.
- `Adversarial patch`: a small image optimized to interfere with the model’s decision-making when overlaid on a person.

## Slide 2 — Two Complementary Tracks

### Script

"This project has two complementary tracks, but they are not one merged runtime pipeline. The attack repo trains and evaluates adversarial patches on a 48-image common manifest across YOLOv8n, YOLO11n, and YOLO26n. The defense repo runs automated attack-defense cycles on a COCO subset and records cycle reports, checkpoint evaluations, and provenance-tracked artifacts. I’m presenting them together as sibling results from the same research direction, not as one shared-image loop."

### Explainer

- `Track`: one coordinated workflow inside the broader research direction.
- `Gradient-based patch training`: the patch pixels are updated with backpropagation so they become more effective at suppressing detections.
- `Multi-model` or `joint ensemble` training: one patch is optimized against more than one detector at the same time.
- `Transfer evaluation`: train on one model, test on another, and measure whether the attack generalizes.
- `Schema-enforced artifacts`: each run writes results in a fixed format so experiments can be compared safely.
- `Provenance tracking`: each artifact records the code, config, and data path that produced it.

## Slide 3 — Detection Suppression

### Script

"Here are the headline results. On YOLOv8n, the patch suppresses 90 percent of person detections. On YOLO11n, it still suppresses 72.7 percent. Then YOLO26n changes the picture completely: suppression falls to 16.3 percent. So the patch works very well on the older two generations and poorly on the new one. The important point is that v26n did not simply look like a broken training run. The optimization objective still converged, but that convergence did not translate into fewer detections. That mismatch becomes the main technical result of the talk."

### Explainer

- `Suppression %`: the fraction of person detections removed by the patch relative to the clean baseline.
- `90% suppression`: if the clean model would detect 20 people, the patched version detects about 2.
- `1000 epochs`: the patch was updated over 1,000 full passes through the training set.
- `100×100 px`: the patch covers only 2.4% of a `640×640` image.
- `Loss / optimized objective`: the training signal used to update the patch. The key point here is not comparing raw loss values across different architectures; it is that, within the v26n experiments, better objective convergence did not produce better suppression.

## Slide 4 — The Bad Triangle

### Script

"This matrix uses the current v2 transfer artifacts. The white-box diagonal is unchanged, but two v8n-source off-diagonal values move to 33.3 percent on v11n and 14.0 percent on v26n. The asymmetry still holds because v11n to v8n is 50 percent. And v26n is still the hardest target: nothing in the direct matrix exceeds 16.3 percent against it, while the best joint patch only reaches 18.6 percent."

### Explainer

- `White-box attack`: the attacker has full access to the model internals and gradients.
- `Black-box transfer`: the attacker trains on one model and tests on another without using that second model during training.
- `Asymmetry`: `v11n -> v8n` works better than `v8n -> v11n` even in the current `v2` artifacts.
- `Joint patch`: one patch trained against two models simultaneously. It usually trades peak single-model performance for broader coverage.
- `Best joint result on v26n`: `18.6%`, which is slightly better than the single-model v26n result but still low.

## Slide 5 — Preprocessing Makes It Worse

### Script

"A natural defense idea is to blur, compress, or crop-resize the image before it reaches the detector. Here, blur and JPEG usually fail or make the patch stronger. Crop-resize occasionally helps at stronger crops, but it is too unstable to present as a reliable defense."

### Explainer

- `JPEG compression`: removes fine image detail by quantizing high-frequency content.
- `Gaussian blur`: averages nearby pixels; larger sigma means stronger blur.
- `Crop-resize`: cuts away part of the image and scales the rest back up.
- `pp`: percentage points. `+10 pp` means 85% became 95%.
- Why it fails here: a patch is a strong localized signal. Preprocessing weakens helpful background detail while leaving the patch’s dominant structure visible.

## Slide 6 — The v26n Paradox

### Script

"So why did the v26n attacks stay weak? The short answer is architecture. YOLO26n uses end-to-end matching. During training, one internal head learns with a one-to-many objective. During inference, a different one-to-one head produces the final detections. I tested three variants: a cold start on the one-to-many path, a warm start from the v8n patch, and a direct one-to-one objective. In all three cases, the optimized objective improved while suppression stayed weak or even got worse. That is the paradox: the patch was optimizing a target, but not one that reliably controlled inference."

### Explainer

- `Hungarian matching`: an assignment method used to pair predictions with ground-truth objects in end-to-end detectors.
- `NMS`: Non-Maximum Suppression, the older post-processing step used by traditional YOLO models to remove duplicate boxes.
- `one2many head`: training-oriented path that emits many candidate predictions.
- `one2one head`: inference path that emits the final object predictions.
- Why this matters: if the attack objective is aligned with one path and the final output depends on another, optimization can look healthy while practical suppression stays low.
- The strongest evidence is internal to v26n itself: objective values improved across runs (`0.108 -> 0.103 -> 0.094`) while suppression degraded (`16.3% -> 14.0% -> 11.6%`).

## Slide 7 — Automated Arms Race

### Script

"The defense track asks a different question: what does the latest canonical cycle show? In cycle 22, clean baseline is 0.600, dispersion reduction drops it to 0.238, and the strongest defended configuration in that same latest cycle is square plus c_dog at 0.394. That does not mean c_dog wins every matchup; in the current canonical series median preprocessing is stronger on deepfool. The honest summary is partial recovery, not a universal defense."

### Explainer

- `mAP50`: standard object detection metric; higher is better.
- `Latest canonical cycle`: the repo records 22 cycles overall, but the current trend should be read from the post-switch `attack_then_defense` series.
- `c_dog`: a learned denoiser that tries to remove adversarial structure before detection; it is strongest on square in cycle 22, not on every attack.
- `Adversarial finetuning`: update the DPC-UNet denoiser checkpoint on adversarial image pairs, then compare it against the current checkpoint on clean data before promotion.
- `Clean A/B gate`: deploy only if the candidate checkpoint does not regress versus the current checkpoint on clean data.

## Slide 8 — Arms Race Engineering

### Script

"Mechanically, the loop is four phases, not three: characterize attacks, build a defense matrix, tune the best pair, then validate on the full dataset. The clean A/B gate is a separate checkpoint-promotion step for c_dog, not a claim that every cycle stays above the 0.600 no-defense baseline. The repo has 22 recorded cycles overall, but only the post-switch attack-then-defense series should be treated as the canonical current trend."

### Explainer

- `Characterize`: quick screening to identify the most damaging attacks before expensive validation.
- `Matrix`: quick screening of candidate defenses against the strongest attacks.
- `Validate + report`: full-dataset mAP50 validation plus report and artifact generation.
- `DPC-UNet`: denoiser checkpoint used as a preprocessing defense before YOLO inference.
- `5x oversample`: square-attack examples are shown more frequently during finetuning because they are currently the strongest c_dog pairing.
- `Within noise`: any change in robustness was too small to separate from run-to-run variation.

## Slide 9 — Live Demo

### Script

"In the demo, the left side shows the clean detector output and the right side shows the same feed with the patch digitally overlaid on the torso of the largest detected person. The bar at the bottom shows a rolling 30-frame suppression average so the result is readable instead of jittery. I can also show the physical version: an 8-by-8-inch print at 300 DPI. Physical performance is directionally lower than digital because printers, lighting, and viewing angles perturb the patch. The repo includes a structured physical benchmark script, but the committed presentation artifacts should not claim a fixed physical suppression percentage."

### Explainer

- `Digital mode`: perfect software overlay; pixel values are exact.
- `Physical mode`: printed patch held in front of a real camera; color drift, perspective, and lighting reduce effectiveness.
- `Torso placement`: chosen because it overlaps the central region of the detector’s person box.
- `30-frame rolling average`: smooths frame-to-frame noise over about one second of video.
- `NPS loss`: Non-Printability Score; penalizes colors that printers reproduce poorly.

## Slide 10 — Conclusions

### Script

"I’d close with three careful takeaways. First, the contribution is two complementary repos, not one merged pipeline: one captures patch training and cross-generation transfer, and the other captures automated defense-cycle evidence. Second, architecture still matters: YOLO26n breaks the usual assumption that optimizing the attack objective will directly reduce detections. Third, the defense repo shows partial recovery and clean-safe checkpoint updates, but not a universal defense."

### Explainer

- `Reproducible`: someone else should be able to rerun the experiment from code and config.
- `NMS-free shift`: moving away from NMS changes how detections are produced and therefore how attacks should target them.
- `DETR`: Detection Transformer, a major end-to-end matching-based detector family.
- `Porting from DETR literature`: the likely next step is to adapt attack objectives designed for matching-based detectors to YOLO26n.
- `Physical robustness at scale`: still an open engineering problem across cameras, lighting, printers, angles, and distance.

## Quick Reference

| Stat | Value |
| --- | --- |
| v8n suppression | 90% |
| v11n suppression | 72.7% |
| v26n suppression | 16.3% |
| Best transfer (`v11n -> v8n`) | 50% |
| Best joint result on v26n | 18.6% |
| Clean mAP50 | 0.600 |
| Latest-cycle worst attack mAP50 | 0.238 |
| Latest-cycle strongest defended mAP50 | 0.394 |
| Finetuning clean gain | +0.0025 |
| Recorded automated cycles | 22 |
| Patch size | 100×100 px |
