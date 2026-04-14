# Presenter Guide: Adversarial Robustness Framework

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

## Slide 2 — Two-Track Pipeline

### Script

"This project has two tracks that feed into each other. The attack track trains patches against YOLO models and measures direct suppression, transfer across models, and robustness under common preprocessing defenses. The defense track runs a continuous attack-defense loop: attack the current detector, tune a defense against that attack, then only keep the defense if it still performs well on clean data. Both tracks share the same image set and both output structured artifacts, so the results are reproducible rather than one-off demos."

### Explainer

- `Pipeline`: an automated sequence of steps that turns inputs into outputs without manual intervention at every stage.
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

"This matrix is where the transfer story becomes interesting. The green diagonal is the white-box result: each patch tested on the same model it was trained on. Off the diagonal, we get transfer. A patch trained on YOLO11n fools YOLOv8n at 50 percent, but the reverse direction only reaches 36.4 percent. So newer-generation patches reach backward better than older-generation patches reach forward. And v26n is the hardest target in the matrix: nothing exceeds 18.6 percent against it. But its own patch still transfers out to v8n and v11n. In this setup, resistance as a target did not stop v26n from producing transferable adversarial structure."

### Explainer

- `White-box attack`: the attacker has full access to the model internals and gradients.
- `Black-box transfer`: the attacker trains on one model and tests on another without using that second model during training.
- `Asymmetry`: `v11n -> v8n` works better than `v8n -> v11n`, suggesting the newer model’s adversarial features generalize backward more effectively.
- `Joint patch`: one patch trained against two models simultaneously. It usually trades peak single-model performance for broader coverage.
- `Best joint result on v26n`: `18.6%`, which is slightly better than the single-model v26n result but still low.

## Slide 5 — Preprocessing Makes It Worse

### Script

"A natural defense idea is to blur or compress the image before it reaches the detector. For classic distributed adversarial noise, that sometimes helps. Here it did not. Mild JPEG compression pushed suppression from 85 percent to 95 percent. Gaussian blur at sigma 2 pushed it to 100 percent. So the simple preprocessing defenses either failed or made the attack stronger. The reason is structural: this threat is a concentrated patch, not faint noise spread across the whole image. Blur and compression damage the clean scene more than they damage the patch."

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

"The defense track asks a different question: once attacks exist, how much performance can we recover automatically? On clean data, the detector starts at mAP50 of 0.600. The best attack, dispersion reduction, drops that to 0.238, which is about a 60 percent collapse. The best defense combination, square plus the learned denoiser c_dog, recovers performance to 0.394. That is still below clean, but it is substantially better than leaving the model undefended. I also ran adversarial finetuning. It cleared the clean-data gate, but it has not yet produced measurable robustness gains."

### Explainer

- `mAP50`: standard object detection metric; higher is better.
- `0.600 -> 0.238`: the strongest attack severely degrades detector quality.
- `c_dog`: a learned denoiser that tries to remove adversarial structure before detection.
- `Adversarial finetuning`: continue training the detector on attacked examples so it learns robustness.
- `Clean gate`: only deploy a defense or finetuned model if clean performance stays at or above the required baseline.

## Slide 8 — Arms Race Engineering

### Script

"Mechanically, each automation cycle has three phases. First, attack the current model and record the performance drop. Second, tune a defense against that attack and record the recovery. Third, run the clean gate and only keep the change if clean mAP50 does not regress. Every cycle writes a schema-checked, provenance-tracked artifact. That matters because after 22 cycles, you do not want a spreadsheet of hand-edited notes; you want a reproducible experimental record."

### Explainer

- `Hyperparameters`: settings such as learning rate, patch size, augmentation strength, or defense configuration.
- `Schema-enforced JSON`: output files must match a predefined structure.
- `Provenance hash`: fingerprint of the run inputs so results can be traced and reproduced.
- `DPC-UNet`: detector architecture used in the defense track experiments.
- `5× oversample`: adversarial examples are shown more frequently during finetuning to force the model to care about them.
- `Within noise`: any change in robustness was too small to separate from run-to-run variation.

## Slide 9 — Live Demo

### Script

"In the demo, the left side shows the clean detector output and the right side shows the same feed with the patch digitally overlaid on the torso of the largest detected person. The bar at the bottom shows a rolling 30-frame suppression average so the result is readable instead of jittery. I can also show the physical version: an 8-by-8-inch print at 300 DPI. Physical performance is lower than digital because printers, lighting, and viewing angles all perturb the patch."

### Explainer

- `Digital mode`: perfect software overlay; pixel values are exact.
- `Physical mode`: printed patch held in front of a real camera; color drift, perspective, and lighting reduce effectiveness.
- `Torso placement`: chosen because it overlaps the central region of the detector’s person box.
- `30-frame rolling average`: smooths frame-to-frame noise over about one second of video.
- `NPS loss`: Non-Printability Score; penalizes colors that printers reproduce poorly.

## Slide 10 — Conclusions

### Script

"I’d close with three takeaways. First, the contribution is not just one patch result. It is a reproducible framework that produced attack, transfer, defense, and automation results across multiple YOLO generations. Second, architecture matters more than a simple leaderboard comparison suggests. In this setup, YOLO26n breaks the usual assumption that optimizing the attack objective will directly reduce detections. Third, the open research question is whether this architecture needs a different attack class entirely, possibly adapted from DETR-style matching literature. That is where the next cycle should go."

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
| Best attack mAP50 | 0.238 |
| Best defended mAP50 | 0.394 |
| Finetuning clean gain | +0.003 |
| Automated cycles | 22 |
| Patch size | 100×100 px |
