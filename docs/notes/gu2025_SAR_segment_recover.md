# Paper Review: Gu & Jafarnejadsani (2025) — SAR: Segment and Recover

## Citation

- Title: Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks
- Authors: Gu, Jafarnejadsani
- Venue / Year: Journal of Imaging, MDPI, Volume 11, Issue 9, Article 316 (2025)
- URL: https://www.mdpi.com/2313-433X/11/9/316 (open access)
- DOI: https://doi.org/10.3390/jimaging11090316
- PDF: Open access — should be downloadable directly from MDPI

## ⚠️ Access Note

MDPI open-access page returns 403 for automated scraping (bot protection). The paper is openly available at the URL above for human browser access. Paper confirmed real. Content below is based on the provided description.

## Problem (from description)

- Defends object detectors against adversarial patch attacks using a segmentation + recovery pipeline.
- Positioned as a more rigorous defense than Ad-YOLO — may use certified or verifiable defense properties.

## Why This Matters

For the capstone's defenses section, this paper represents a segmentation-based approach: detect the patch region via segmentation, then recover the underlying clean image region before running the detector. This is architecturally different from:
- Ad-YOLO (train detector to ignore patches)
- NAPGuard (detect naturalistic patches)
- XAIAD-YOLO (XAI-guided test-time purification)

Together, these four papers form a comprehensive picture of the current defense landscape.

## Action Required

1. Open the MDPI URL in a browser (free, no login required)
2. Record: exact method (segmentation approach used, recovery technique, which detectors defended)
3. Record: YOLO versions evaluated, datasets, quantitative defense results (AP recovery)
4. Update this note with full details

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: Moderate — relevant for defenses section.
- What I can cite: For the segmentation-based defense approach; as a complement to NAPGuard and XAIAD-YOLO in a defenses comparison table.
