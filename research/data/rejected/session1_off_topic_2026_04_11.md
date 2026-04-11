# Rejected Candidates — Session 1 (2026-04-11)

**Source:** `research/data/ranked/ranked_reading_list.md` — ingest run 2026-04-11
**Reason for rejection:** Wrong domain — not person/pedestrian evasion against YOLO surveillance models.
These papers may be useful for future projects in autonomous driving, remote sensing, UAV detection, or semantic segmentation adversarial robustness.

---

## Wrong Domain: Autonomous Driving / Traffic / Vehicle

### Fooling the Eyes of Autonomous Vehicles: Robust Physical Adversarial Examples Against Traffic Sign Recognition Systems
- Score: 22.608 | Year: 2022 | Citations: 46
- DOI: 10.14722/ndss.2022.24130
- Venue: NDSS 2022
- Authors: Gang Qu, Haichun Zhang, Jie Wang, Wei Jia, Zhaojun Lu
- Domain: Traffic sign recognition for autonomous vehicles
- Why rejected: Traffic signs, not person detection

### Adversarial Examples for Vehicle Detection With Projection Transformation
- Score: 22.383 | Year: 2024 | Citations: 20
- DOI: 10.1109/tgrs.2024.3428360
- Venue: IEEE Transactions on Geoscience and Remote Sensing
- Authors: Jiahao Cui, Wang Guo, Haikuo Huang, Xun Lv, Hang Cao
- Domain: UAV vehicle detection
- Why rejected: Vehicle detection in aerial imagery

### FCA: Learning a 3D Full-Coverage Vehicle Camouflage for Multi-View Physical Adversarial Attack
- Score: 19.106 | Year: 2022 | Citations: 100
- DOI: 10.1609/aaai.v36i2.20141
- Venue: AAAI 2022
- Authors: Donghua Wang, Jialiang Sun, Tingsong Jiang, Weien Zhou, Wen Yao
- PDF: https://ojs.aaai.org/index.php/AAAI/article/download/20141/19900
- Domain: 3D vehicle camouflage
- Why rejected: Vehicle 3D surface attack, not person patch

### TPatch: A Triggered Physical Adversarial Patch
- Score: 17.653 | Year: 2023 | Citations: 3
- arXiv: 2401.00148
- Authors: Wenjun Zhu, Xiaoyu Ji, Yushi Cheng, Shibo Zhang, Wenyuan Xu
- Domain: Acoustic-triggered patches for autonomous vehicles
- Why rejected: Autonomous vehicle trigger attack, wrong threat model

### Physically Realizable Adversarial Creating Attack Against Vision-Based BEV Space 3D Object Detection
- Score: 16.969 | Year: 2025 | Citations: 40
- DOI: 10.1109/tip.2025.3526056
- Venue: IEEE Transactions on Image Processing
- Domain: 3D BEV autonomous driving detection
- Why rejected: 3D detection for autonomous driving

### A Unified Framework for Adversarial Patch Attacks Against Visual 3D Object Detection in Autonomous Driving
- Score: 16.558 | Year: 2025 | Citations: 46
- DOI: 10.1109/tcsvt.2025.3525725
- Venue: IEEE TCSVT
- Domain: 3D object detection autonomous driving
- Why rejected: Autonomous driving 3D detection

### Cost-effective and robust adversarial patch attacks in real-world scenarios
- Score: 16.002 | Year: 2025 | Citations: 1
- DOI: 10.1117/1.JEI.34.3.033003
- Venue: J. Electronic Imaging (SPIE)
- Authors: Kalibinuer Tiliwalidi et al.
- Domain: Camera patch attacks on self-driving cars
- Why rejected: Self-driving context, camera lens attack

### MagShadow: Physical Adversarial Example Attacks via Electromagnetic Injection
- Score: 17.318 | Year: 2025 | Citations: 6
- DOI: 10.1109/tdsc.2025.3529197
- Venue: IEEE Transactions on Dependable and Secure Computing
- Domain: EM signal injection into CCD sensors
- Why rejected: Hardware attack vector, not patch-based

---

## Wrong Domain: Remote Sensing / UAV / Aerial

### Adversarial Patch Attack on Multi-Scale Object Detection for UAV Remote Sensing Images
- Score: 22.135 | Year: 2022 | Citations: 48
- DOI: 10.3390/rs14215298
- Venue: Remote Sensing (MDPI)
- PDF: https://www.mdpi.com/2072-4292/14/21/5298/pdf?version=1666681250
- Domain: UAV remote sensing
- Why rejected: Aerial imagery, not ground-level person detection

### Adversarial Patch Attack on Multi-Scale Object Detection for Remote Sensing Image (preprint)
- Score: 21.483 | Year: 2022 | Citations: 17
- DOI: 10.20944/preprints202210.0131.v1
- Domain: Remote sensing preprint (likely same as above)
- Why rejected: Duplicate domain

### CBA: Contextual Background Attack Against Optical Aerial Detection in the Physical World
- Score: 20.758 | Year: 2023 | Citations: 46
- DOI: 10.1109/tgrs.2023.3264839
- Venue: IEEE TGRS
- Domain: Aerial detection
- Why rejected: Aerial / aircraft domain

### Rust-Style Patch: A Physical and Naturalistic Camouflage Attacks on Object Detector for Remote Sensing Images
- Score: 20.372 | Year: 2023 | Citations: 25
- DOI: 10.3390/rs15040885
- Venue: Remote Sensing (MDPI)
- PDF: https://www.mdpi.com/2072-4292/15/4/885/pdf?version=1676607668
- Domain: Remote sensing naturalistic patches
- Why rejected: Remote sensing domain

### Scale-Adaptive Adversarial Patch Attack for Remote Sensing Image Aircraft Detection
- Score: 16.485 | Year: 2021 | Citations: 48
- DOI: 10.3390/rs13204078
- Venue: Remote Sensing (MDPI)
- PDF: https://www.mdpi.com/2072-4292/13/20/4078/pdf?version=1634093571
- Domain: Aircraft detection in remote sensing
- Why rejected: Aerial / aircraft domain

### Towards a Robust Adversarial Patch Attack Against Unmanned Aerial Vehicles Object Detection
- Score: 16.32 | Year: 2023 | Citations: 23
- DOI: 10.1109/iros55552.2023.10342460
- Venue: IROS 2023
- Domain: UAV object detection
- Why rejected: UAV-specific setting

---

## Wrong Domain: Semantic Segmentation

### Evaluating the Robustness of Semantic Segmentation for Autonomous Driving against Real-World Adversarial Patch Attacks (×2 duplicate entries)
- Score: 21.994 / 21.517 | Year: 2021/2022 | Citations: 106/87
- arXiv: 2108.06179 | DOI: 10.1109/wacv51458.2022.00288
- Venue: IEEE WACV 2022
- Domain: Semantic segmentation robustness
- Why rejected: Segmentation, not object detection

---

## Borderline / Low Priority (Defense Branch, Low Citations)

### Information Distribution Based Defense Against Physical Attacks on Object Detection
- Score: 17.231 | Year: 2020 | Citations: 8
- DOI: 10.1109/icmew46912.2020.9105983
- Venue: IEEE ICMEW 2020
- Why rejected: Low citations, defense-only, older method superseded by NAPGuard/SAC/PatchZero

### Localization and Elimination: Object Detection Physical Patch Defense (LAE)
- Score: 16.05 | Year: 2025 | Citations: 0
- DOI: 10.1109/IJCNN64981.2025.11227215
- Why rejected: 0 citations, very new, not yet established

### Signals Are All You Need: Detecting and Mitigating Digital and Real-World Adversarial Patches Using Signal-Based Features
- Score: 16.255 | Year: 2024 | Citations: 7
- DOI: 10.1145/3665451.3665530
- Venue: SecTL@AsiaCCS 2024
- Why rejected: Very low citations, defense-only, no PDF

---

## Multi-View Transfer (Tier 4 in existing bibliography)

### Adversarial Attacks in a Multi-view Setting: An Empirical Study of the Adversarial Patches Inter-view Transferability
- Score: 22.305 | Year: 2021 | Citations: 7
- arXiv: 2110.04887
- PDF: https://arxiv.org/pdf/2110.04887
- Authors: Bilel Tarchoun, Ihsen Alouani, Anouar Ben Khalifa, Mohamed Ali Mahjoub
- Status: Already in Tier 4 of batch4_literature_expansion.md — parked, not promoted

---

## Potential Future Use

The following are off-topic for this capstone but may be useful for future work:
- **FCA** (3D vehicle camouflage, AAAI 2022, 100 citations) — if extending to vehicle detection
- **APRICOT** (physical patch dataset) — if building a benchmark dataset of your own
- **Kolter & Lee (1906.11897)** — ✅ PROMOTED to verified bibliography (global patch suppression on YOLOv3, person-relevant)
- **SAC Segment-and-Complete** (CVPR 2022, 98 citations) — strong defense; if doing defenses chapter
