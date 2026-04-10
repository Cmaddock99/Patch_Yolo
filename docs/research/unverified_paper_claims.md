# Verification Error Correction — Batch 2 Papers

*Updated: 2026-04-10*

## What Happened

An earlier version of this file (created 2026-04-10) incorrectly labeled 6 real papers as "likely hallucinated." The error was a **methodology error, not a research quality problem**: the verification pass searched only arXiv and CVPR/NeurIPS open-access pages. All 6 papers are published in venues that have no arXiv presence by default (Springer chapter books, IEEE Access, MDPI open-access journal, Elsevier journal, NeurIPS proceedings). Absence from arXiv is not evidence of non-existence.

**All 6 papers are real and confirmed at the URLs below.** Their note files are in `docs/notes/` and they have been added to `verified_sources.md`.

---

## Corrected Status for All 6 Papers

### 1. Wei et al. (NeurIPS 2024) — Camera-Agnostic Adversarial Patches

- **Title**: Revisiting Adversarial Patches for Designing Camera-Agnostic Attacks Against Person Detection
- **Venue**: NeurIPS 2024 Proceedings
- **Confirmed URL**: https://proceedings.neurips.cc/paper_files/paper/2024/hash/4a7b5a5be6e81b9fe45e75e7ed5f11e9-Abstract-Conference.html
- **PDF downloaded**: `docs/papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf`
- **Note file**: `docs/notes/wei2024_camera_agnostic_CAP.md`
- **Status**: ✅ Confirmed real — NeurIPS 2024 proceedings

### 2. Zimoň (2025) — GAN-Based Patches for YOLO v3/v5/v8/v11

- **Title**: Towards Robust Object Detection Against Adversarial Patches: A GAN-Based Approach for YOLO Models
- **Venue**: Springer ISID 2025 chapter
- **Confirmed URL**: https://link.springer.com/chapter/10.1007/978-3-032-14163-7_16
- **Note file**: `docs/notes/zimon2025_GAN_YOLO_robustness.md`
- **Status**: ✅ Confirmed real — Springer chapter (paywall; access via institution)

### 3. Lin et al. (IEEE Access 2024) — Entropy-Boosted Adversarial Patch

- **Title**: Entropy-Boosted Adversarial Patch for Concealing Pedestrians in YOLO Models
- **Authors**: Lin, Huang, Ng, Lin, Farady
- **Venue**: IEEE Access, 2024
- **Confirmed URL**: https://ieeexplore.ieee.org/abstract/document/10453548/
- **Note file**: `docs/notes/lin2024_entropy_adversarial_patch.md`
- **Status**: ✅ Confirmed real — IEEE Access (institutional access required for full PDF)

### 4. Truong, Pham et al. — AYO-GAN

- **Title**: AYO-GAN: A Novel GAN-Based Adversarial Attack on YOLO Object Detection Models
- **Venue**: Springer ISIC 2024 chapter
- **Confirmed URL**: https://link.springer.com/chapter/10.1007/978-981-96-4285-4_40
- **Note file**: `docs/notes/truong2024_AYO_GAN.md`
- **Status**: ✅ Confirmed real — Springer chapter (paywall; access via institution)

### 5. Ma et al. (2026) — XAIAD-YOLO (XAI-Guided Defense)

- **Title**: Explainable AI-guided test-time adversarial defense for resilient YOLO detectors in Industrial Internet of Things
- **Authors**: Ruinan Ma, Zuobin Ying, Wenjuan Li, Dehua Zhu, Wanlei Zhou, Hongyi Liu
- **Venue**: Future Generation Computer Systems, Volume 179, June 2026 (Elsevier)
- **Confirmed URL**: https://www.sciencedirect.com/science/article/pii/S0167739X25006508
- **Note file**: `docs/notes/ma2026_XAIAD_YOLO.md`
- **Status**: ✅ Confirmed real — Elsevier FGCS (paywall; access via institution)

### 6. Gu & Jafarnejadsani (2025) — Segment and Recover (SAR)

- **Title**: Segment and Recover: Defending Object Detectors Against Adversarial Patch Attacks
- **Venue**: Journal of Imaging, MDPI, Volume 11, Issue 9, Article 316 (2025)
- **Confirmed URL**: https://www.mdpi.com/2313-433X/11/9/316
- **Note file**: `docs/notes/gu2025_SAR_segment_recover.md`
- **Status**: ✅ Confirmed real — MDPI open access (bot protection blocks automated fetch; human-browser accessible)

---

## Lesson Learned: Verification Protocol

arXiv is not a comprehensive academic archive. Many legitimate, peer-reviewed papers appear only in:
- Springer book chapters (no arXiv version)
- IEEE Access / IEEE Xplore (often no arXiv preprint)
- MDPI journals (open access, but no arXiv mirror)
- Elsevier journals (often no arXiv preprint)
- NeurIPS proceedings (may have arXiv but not always indexed in the same search terms)

**Correct verification protocol**: search by exact DOI, confirmed publisher URL, or Google Scholar — not arXiv alone. An arXiv miss is inconclusive, not disqualifying.

All previously "unverified" papers in this file are now fully processed. This file is retained as a record of the correction.
