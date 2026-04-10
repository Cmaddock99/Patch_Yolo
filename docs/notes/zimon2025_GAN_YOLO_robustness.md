# Paper Review: Zimoň (2025) — GAN-Based Adversarial Patches for YOLO v3/v5/v8/v11

## Citation

- Title: Towards Robust Object Detection Against Adversarial Patches: A GAN-Based Approach for YOLO Models
- Authors: Zimoň (first name not confirmed from available sources)
- Venue / Year: Springer ISID 2025 (Intelligent Systems and Image Data, or similar)
- URL: https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16
- PDF: Not freely available (Springer paywall; access via institution)

## ⚠️ Access Note

The Springer URL provided leads to a paywalled chapter. The WebFetch tool cannot follow Springer's redirect chain. Paper confirmed real by user; content below is based on the provided description. **Read the full paper for authoritative details.**

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
