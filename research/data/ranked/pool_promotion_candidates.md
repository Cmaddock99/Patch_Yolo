# Pool Promotion Candidates

Generated: 2026-04-11
Source: research/data/ranked/ranked_reading_list.md, top 40 entries (score ≥ 18.0)
Criteria: Score ≥ 18.0 AND (directly evaluates YOLOv8/YOLO11/YOLO26 OR directly addresses person-detection evasion transfer across YOLO generations) AND not already present in docs/notes/.

All papers already in docs/notes/ are excluded (they are Tier A, B, or C in the master pool).

---

## Candidate 1: AdvTexture — Adversarial Texture for Fooling Person Detectors

- **Score**: 19.377
- **Full title**: *Adversarial Texture for Fooling Person Detectors in the Physical World*
- **Authors**: Bo Zhang, Fuchun Sun, Siyuan Huang, Xiaolin Hu, Xiaopei Zhu (Tsinghua University)
- **Year**: 2022
- **Venue**: CVPR 2022
- **Citations**: 152
- **arXiv**: 2203.03373
- **PDF**: http://arxiv.org/pdf/2203.03373 (open access)

**Why it qualifies**: Score 19.377 (above 18.0 threshold). Directly addresses person-detection evasion with a method (AdvTexture) designed for multi-angle robustness — patches that cover clothing with arbitrary shapes so persons can hide from person detectors from different viewing angles. 152 citations makes this a high-impact benchmark paper. The CVPR 2022 venue and citation count suggest this is a canonical multi-angle person evasion paper that fills a gap between the 2019-era papers (Thys, Xu T-shirt) and 2024-era papers (DePatch, AdvReal).

**What it would add**: A multi-angle person evasion benchmark at the 2022 state-of-the-art. The paper proposes a generative approach for full-body clothing textures that remain effective across different camera angles — directly relevant to the physical-world evaluation discussion in the capstone. The 2022 benchmark numbers would provide a middle data point in the timeline: Thys 2019 (26.46% recall) → AdvTexture 2022 → DePatch 2024 → AdvReal 2025 → this capstone.

**Specific YOLO version evaluated**: Not confirmed from abstract; likely YOLOv2/v3 or YOLOv5 (2022 publication window). Needs PDF read to confirm. Person class is primary target.

**Access status**: Open access PDF at arXiv (2203.03373). No institutional access required.

**Priority**: High — open access, high citations, fills 2022 multi-angle benchmark gap.

---

## Candidate 2: "We Can Always Catch You" — Detecting Adversarial Patched Objects

- **Score**: 19.756
- **Full title**: *We Can Always Catch You: Detecting Adversarial Patched Objects WITH or WITHOUT Signature*
- **Authors**: Binxiu Liang, Jiachun Li, Jianan Feng, Jianjun Huang
- **Year**: 2021 (published 2025 in IEEE Trans. Dependable and Secure Computing)
- **Venue**: IEEE Transactions on Dependable and Secure Computing (2025)
- **DOI**: 10.1109/TDSC.2025.3596709
- **arXiv**: 2106.05261
- **Citations**: 15
- **PDF**: not available open access

**Why it qualifies**: Score 19.756, directly addresses adversarial patch detection against YOLO-based systems. The abstract explicitly mentions YOLO as the target detector and surveillance camera escaping as the threat context — directly aligned with the capstone's surveillance framing. Two proposed detection methods: (1) signature-based (fast, uses known patch visual signatures) and (2) signature-independent (uses visual anomaly without prior knowledge of attack appearance). The signature-independent method is particularly relevant for detecting the capstone's patches without knowing their appearance.

**What it would add**: A sixth defense paradigm for the defenses comparison table: signature-based + signature-independent patch detection. Distinct from Ad-YOLO (patch class), NAPGuard (semantic detection), PatchZero (detect-and-zero), SAC/SAR (segment-recover), XAIAD-YOLO (XAI purification), and Tereshonok (anomaly reconstruction). The signature-independent method most closely competes with NAPGuard but from a different theoretical foundation.

**Specific YOLO version evaluated**: Not confirmed; abstract mentions "YOLO" but version not specified in the Semantic Scholar snippet. Needs full read. 2021/2025 publication window suggests YOLOv3/v5.

**Access status**: IEEE Xplore via CSUSM institutional access. arXiv 2106.05261 may have a preprint.

**Priority**: Medium — useful for defenses comparison table; the defense paradigm is distinct but the YOLO version coverage is uncertain.

---

## Candidate 3: 3D Invisible Cloak — 3D Physical Person Stealth Attack

- **Score**: 19.016
- **Full title**: *3D Invisible Cloak: A Robust Person Stealth Attack Against Object Detector in Complex 3D Physical Scenarios*
- **Authors**: Mingfu Xue, Can He, Zhiyu Wu, Jian Wang, Zhe Liu
- **Year**: 2020 (published 2024 in IEEE Transactions on Emerging Topics in Computing)
- **DOI**: 10.1109/TETC.2024.3513392
- **arXiv**: 2011.13705
- **Citations**: 2
- **PDF**: not available open access

**Why it qualifies**: Score 19.016. Person stealth attack with explicit 3D physical modeling (radian, wrinkle, occlusion, angle) for wearable clothing. First paper to address complex 3D physical constraints for person stealth in adversarial patches — directly extends the 2D flat-patch approach (Thys, DePatch) to 3D deformable clothing. The abstract confirms: "We launch the person stealth attacks in 3D physical space instead of 2D plane by printing the adversarial patches on real clothes. Anyone wearing the cloak can evade the detection of person detectors and achieve stealth under challenging and complex 3D physical scenarios."

**What it would add**: The 3D physical constraint modeling approach as a conceptual predecessor to DePatch (block-wise decoupling) and UV-Attack (NeRF-based UV mapping). Would place the capstone's physical discussion in a richer timeline. Low citations (2) means this is less benchmarked but technically relevant.

**Specific YOLO version evaluated**: Not confirmed from abstract; person detector is the target. Given the 2020 original date, likely YOLOv3 or earlier. Needs full read.

**Access status**: IEEE Xplore via CSUSM. arXiv 2011.13705 may have an open preprint.

**Priority**: Low-Medium — low citations, YOLO version uncertain, 3D modeling approach largely superseded by UV-Attack (which has a PDF in the repo). Would add historical depth rather than direct benchmark comparison.

---

## Candidate 4: TPatch — Triggered Physical Adversarial Patch

- **Score**: 18.744
- **Full title**: *TPatch: A Triggered Physical Adversarial Patch*
- **Authors**: Shibo Zhang, Wenjun Zhu, Wenyuan Xu, Xiaoyu Ji, Yushi Cheng
- **Year**: 2023
- **Venue**: USENIX Security Symposium 2023
- **arXiv**: 2401.00148
- **Citations**: 45
- **PDF**: not available open access (USENIX; check direct conference page)

**Why it qualifies**: Score 18.744, person detection evasion. USENIX Security placement (high-impact security venue). 45 citations. Introduces a **triggered** adversarial patch — benign under normal circumstances, becomes adversarial when triggered by an injected acoustic signal. This is a qualitatively different threat model from static patches and may be relevant to the capstone's threat-model taxonomy (static vs. triggered vs. dynamic patches).

**What it would add**: A new threat model category (triggered/acoustic adversarial patch) that contrasts with static patches. The 45 citations at a security-focused venue suggests this has influenced the security community's thinking about physical adversarial attacks. For the capstone's threat-model section, it demonstrates that the patch attack landscape extends beyond static visual perturbations.

**Specific YOLO version evaluated**: Not confirmed from abstract; "autonomous vehicles" and "object detectors" are mentioned. Likely YOLOv5 or later given the 2023 venue. The abstract mentions "hiding, creating or altering attack" types — same taxonomy as Na et al. (2025)'s retail attack paper which is already in the repo.

**Access status**: USENIX Security papers are typically freely available at the conference proceedings page. Check usenix.org/conference/usenixsecurity23.

**Priority**: Medium — unique triggered threat model; USENIX venue credibility; YOLO version uncertain; less directly relevant to person-vanishing person evasion than the other candidates.

---

## Summary

| Candidate | Score | Access | YOLO Version | Priority |
|-----------|-------|--------|--------------|----------|
| AdvTexture (Zhang 2022, CVPR) | 19.377 | Open (arXiv) | Unconfirmed (~v3/v5) | **High** |
| "We Can Always Catch You" (Liang 2021/2025) | 19.756 | IEEE CSUSM | Unconfirmed | Medium |
| 3D Invisible Cloak (Xue 2020/2024) | 19.016 | IEEE CSUSM | Unconfirmed | Low-Medium |
| TPatch (Zhang 2023, USENIX) | 18.744 | USENIX open | Unconfirmed | Medium |

**Recommendation**: Promote AdvTexture (Candidate 1) first — open access PDF, 152 citations, high capstone relevance as a 2022 multi-angle person evasion benchmark filling the gap between 2019 and 2024 papers. If the PDF confirms YOLOv8 or YOLOv11 evaluation, elevate to Tier B immediately.
