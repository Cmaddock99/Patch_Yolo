# Paper Review: Zimoň (2025) — GAN-Based Adversarial Patches for YOLO v3/v5/v8/v11

## Citation

- Title: Towards Robust Object Detection Against Adversarial Patches: A GAN-Based Approach for YOLO Models
- Authors: Zimoň (first name not confirmed from available sources)
- Venue / Year: Springer ISID 2025 (Intelligent Systems and Image Data, or similar)
- URL: https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16
- PDF: Not freely available (Springer paywall; access via institution)

## ⚠️ Access Note

The Springer URL provided leads to a paywalled chapter. This file remains a blocker record, not a synthesis-grade review, until a local full text is available.

## Problem (from description)

- What is the attack/defense goal? Studies GAN-based adversarial patch attacks across YOLO v3, v5, v8, and v11. Discusses cross-version robustness and defenses.
- This is the **closest paper to this capstone's exact scope** — a systematic cross-version study across the YOLO generations most relevant to this project.

## Why This Matters

If the paper includes systematic results comparing patch effectiveness and transfer across YOLOv3 → v5 → v8 → v11, this is a direct predecessor to the capstone's contribution. The key difference from the capstone scope is the absence of YOLO26.

## Action Required

1. Access via institution (Springer link above)
2. Record: exact quantitative results per YOLO version (AP/mAP drop, fooling rate)
3. Record: whether patches trained on v8 were tested on v11 (transfer results)
4. Record: exact dataset(s) used
5. Update this note with full method details

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11: **Extremely high** — this paper likely contains the benchmark numbers my capstone extends to YOLO26.
- Direct relevance to YOLO26: Not included — this is the gap my capstone fills.
- What I can cite: As the most direct predecessor to my capstone's cross-YOLO-version evaluation.

## Normalized Extraction

- Canonical slug: `zimon2025_GAN_YOLO`
- Canonical source record: `Springer chapter entry only; no local PDF in repo`
- Evidence state: `blocked_access`
- Threat model: GAN-based adversarial patch attack across multiple YOLO generations, currently inferred from title and note history.
- Detector family and exact version: YOLOv3, YOLOv5, YOLOv8, YOLOv11, pending full-text confirmation.
- Attack or defense goal: Systematic cross-YOLO comparison of GAN-based patch attacks and possibly defenses.
- Loss or objective: Unknown until full text is available.
- Transforms / EoT: Unknown until full text is available.
- Dataset: Unknown until full text is available.
- Metrics: Unknown until full text is available.
- Strongest quantitative result: Unknown; repo-first mode only confirms scope, not numbers.
- Transfer findings: Likely central to the paper, but all transfer claims are blocked.
- Physical findings: Unknown.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: High for YOLOv8 and YOLO11, gap-framing only for YOLO26.
- Reproducible technique to borrow: None can be promoted until the chapter is available locally.
- Citation strength: `blocked_access`

## Working Packet Status

- Primary repo question: `cross_yolo_transfer`
- Repo currently relies on this for: The claim that a near-scope cross-YOLO predecessor exists for v3/v5/v8/v11.
- Exact missing detail preventing promotion: Per-version benchmark numbers, transfer matrix details, datasets, and defense conclusions.
- Blocker type: `quantitative`
- Promotion rule: Treat as a scope placeholder only until a local PDF is added.
