# Ji et al. (2021) — Adversarial YOLO Defense (Ad-YOLO)

## Citation

- Title: *Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches*
- Authors: Ji, Feng, Xie, Xiang, Liu
- Venue / Year: arXiv 2103.08860 (2021)
- URL: https://arxiv.org/abs/2103.08860
- PDF: `docs/papers/ji2021_adversarial_yolo_defense_2103.08860.pdf`

## Problem

- What threat model is assumed? Defense against white-box and physical-world adversarial patch attacks on human (person-class) detection. Defender has access to representative adversarial patches during training.
- What detector is attacked (victim)? YOLOv2 trained on VOC/COCO
- What is the defense goal? Jointly detect persons AND adversarial patches — treating the patch as a new detection class, so the model simultaneously localizes persons and flags patch presence.

## Method

- Defense type: Adversarial training with "patch" added as a YOLO detection class
- Key insight: Instead of external patch-neutralization modules, Ad-YOLO adds a "patch" output class to the YOLO head. The model learns to detect the adversarial patch region as a distinct bounding box object.
- Training: INRIA Person + self-generated patch dataset (Patch₀, Patch₁, Patch₂, Patch₃ via Thys et al.); train/test splits I0-P0, I1-P1, I0-P1, I1-P0 for generalization testing
- Transformations / EoT details: Patch diversity via multiple independently-generated patches; EoT augmentations during training
- Physical-world considerations: Physical printed patches placed on person's chest; tested in indoor and outdoor scenes (Figure 7)

## Experimental Setup

- Dataset: Pascal VOC 2007/2012; INRIA Person (614 train / 288 test)
- Target classes: Person (primary), Patch (new class for defense)
- Model: YOLOv2 (baseline = Model₀); adversarial training baselines (Model₁, Model₂, Model₃)
- Metrics: mAP (VOC 2007), AP (INRIA person class), white-box attack AP

## Results

### Table 2 — VOC 2007 mAP (p. 6)

| Model | mAP |
|---|---|
| YOLOv2 (Model₀) | 73.05% |
| Ad-YOLO | **72.35%** |

Only −0.70 pp clean accuracy cost. **Supported**.

### Table 3 — INRIA Person Generalization AP (p. 6)

| Split | AP |
|---|---|
| I0-P0 (training patches + training persons) | 79.70% |
| I1-P1 (unseen patches + unseen persons) | 78.70% |
| I1-P0 (unseen persons, training patches) | 78.63% |
| I0-P1 (training persons, unseen patches) | 77.82% |

Generalizes well to unseen patches and unseen persons. **Supported**.

### Table 4 — White-Box Attack Robustness (p. 9)

| Model | Clean AP | White-Box Attack AP |
|---|---|---|
| Model₀ (YOLOv2) | 88.03% | 33.93% |
| Model₁ (adv. training) | 86.44% | 58.62% |
| Model₂ | 87.45% | 56.38% |
| Model₃ | 87.00% | 61.65% |
| **Ad-YOLO** | **86.58%** | **80.31%** |

Ad-YOLO: 80.31% under white-box attack vs. 33.93% baseline. ~46% improvement in robustness. Clean cost: only −1.45 pp. **Supported**.

Physical-world: Ad-YOLO detects both person and adversarial patch in physical scenarios where YOLOv2 fails (Figure 7). **Supported** (qualitative).

## Key Claims

1. **"Patch class" defense dramatically outperforms adversarial training alone** (80.31% vs. best adversarial training 61.65%). **Supported** (Table 4).
2. **Negligible clean accuracy cost** (−1.45 pp on INRIA, −0.70 pp mAP on VOC). **Supported**.
3. **Generalizes to unseen patches** — AP drops only 1 pp from trained-patch to unseen-patch evaluation. **Supported** (Table 3).
4. **Works in physical world** — patch detected and person maintained under physical attack. **Supported** (qualitative, Figure 7).

## Threat Model

- Attacker: White-box YOLOv2; patch placed on person's chest
- Defender: Has access to patch generation process; re-trains YOLO with patch class
- Physical: Printed patches on real persons; indoor + outdoor scenes

## Limitations and Failure Modes

- Only YOLOv2 evaluated — requires full re-training for YOLOv8/v11/v26. **Verified-from-pdf (absence)**.
- Assumes patch placement on person's chest area — patches at back, floor, or unexpected locations may evade the patch class detector. **Speculative from evaluation protocol**.
- Defense requires knowing approximate patch appearance at training time; may fail against significantly novel patch styles (e.g., DAP naturalistic patches). **My inference**.
- No evaluation against black-box transfer attacks where the defender doesn't know the attacker's patch. **Verified-from-pdf (absence)**.

## Defensive Takeaways

- Most computationally efficient defense in this corpus — no external inference module, no latency penalty (single YOLO forward pass detects both person and patch).
- Patch class addition is directly extensible to Ultralytics YOLOv8 by adding one class to the training configuration.
- Training patch diversity (multiple independently-generated patches) is key to generalization — do not train on a single patch style.
- **Key actionable insight for defend phase:** Add "adversarial_patch" as class 80 in YOLOv8n (COCO has 80 classes), generate Thys-style patches as training examples, co-train. Expected clean mAP cost: ~1-2 pp based on this paper.

## Direct Relevance to YOLOv8 / YOLO11 / YOLO26

- **YOLOv8**: High. Decoupled head with separate cls/obj branches makes adding a patch class straightforward. YAML config change + patch dataset. Direct adaptation.
- **YOLO11**: High. Same head architecture as YOLOv8. Same adaptation applies.
- **YOLO26**: Medium. NMS-free design (anchor-free, no objectness score) changes how the patch class integrates. Would need different handling of the patch class signal. Review architecture before implementing.
- Capstone relevance: **4/5**. Clean, low-cost, actionable defense baseline for the defend and fortify phases.

## Reproducibility Signals

- INRIA Person (public); VOC 2007 (public); Thys et al. patch generation code (public: GitLab EAVISE)
- Ad-YOLO code not explicitly released — **unverified-from-pdf**
- Training details: standard YOLOv2 training extended with patch class; splits I0/I1, P0/P1 defined in Section 4.2

## Open Questions

- Does Ad-YOLO generalize to naturalistic patches (DAP, Hu 2021 NatPatch)?
- Can the same approach be applied directly to YOLOv8n for the defend phase?
- What is the minimum patch dataset size needed for good generalization?
- How does patch class detection behave for non-chest patch placements?
