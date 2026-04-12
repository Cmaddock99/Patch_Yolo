# Rejected Candidates — Sessions 2 & 3 (2026-04-11)

**Source:** `research/data/ranked/ranked_reading_list.md` — ingest runs 2 and 3 (updated queries)
**Reason for rejection:** Wrong domain, wrong modality (infrared/thermal only), or spurious keyword match.

Note: Updated queries dramatically reduced noise — top 5 positions are now legitimately in-scope.
These rejects appear at positions 6–38+ and represent residual noise the domain penalties didn't eliminate.

---

## Wrong Domain: Autonomous Driving / Traffic / Vehicle

### Fooling the Eyes of Autonomous Vehicles: Robust Physical Adversarial Examples Against Traffic Sign Recognition Systems
- Score: 20.108 | Year: 2022 | Citations: 46
- DOI: 10.14722/ndss.2022.24130
- Venue: NDSS 2022
- Why rejected: Traffic sign recognition for autonomous vehicles — also in session 1 rejects

### FCA: Learning a 3D Full-Coverage Vehicle Camouflage for Multi-View Physical Adversarial Attack
- Score: 19.106 | Year: 2022 | Citations: 100
- DOI: 10.1609/aaai.v36i2.20141
- Venue: AAAI 2022
- PDF: https://ojs.aaai.org/index.php/AAAI/article/download/20141/19900
- Why rejected: 3D vehicle camouflage — also in session 1 rejects

### MagShadow: Physical Adversarial Example Attacks via Electromagnetic Injection
- Score: 17.598 | Year: 2025 | Citations: 4
- DOI: 10.1109/TDSC.2025.3529197
- Venue: IEEE Transactions on Dependable and Secure Computing
- Why rejected: EM signal injection into CCD sensors — hardware attack vector, not patch-based

---

## Wrong Domain: Remote Sensing / UAV / Aerial

### Adversarial Patch Attack on Multi-Scale Object Detection for Remote Sensing Image (preprint)
- Score: 18.983 | Year: 2022 | Citations: 17
- DOI: 10.20944/preprints202210.0131.v1
- Why rejected: Remote sensing — also in session 1 rejects

### Rust-Style Patch: A Physical and Naturalistic Camouflage Attacks on Object Detector for Remote Sensing Images
- Score: 17.872 | Year: 2023 | Citations: 25
- DOI: 10.3390/rs15040885
- Venue: Remote Sensing (MDPI)
- Why rejected: Remote sensing domain — also in session 1 rejects

### Adversarial Patch Attack on Multi-Scale Object Detection for UAV Remote Sensing Images
- Score: 16.635 | Year: 2022 | Citations: 48
- DOI: 10.3390/rs14215298
- Venue: Remote Sensing (MDPI)
- Why rejected: UAV remote sensing — also in session 1 rejects

---

## Wrong Domain: Semantic Segmentation

### Evaluating the Robustness of Semantic Segmentation for Autonomous Driving against Real-World Adversarial Patch Attacks
- Score: 16.994 | Year: 2021 | Citations: 106
- DOI: 10.1109/WACV51458.2022.00288
- Venue: IEEE WACV 2022
- arXiv: 2108.06179
- Why rejected: Semantic segmentation, not object detection — also in session 1 rejects

---

## Wrong Modality: Infrared / Thermal Only

These papers target thermal infrared detectors, not visible-light RGB cameras.
They are not directly comparable to RGB patch attacks on YOLO. Good for a 1-sentence
"orthogonal attack modality" mention but do not warrant full notes.

### Fooling Thermal Infrared Pedestrian Detectors in Real World Using Small Bulbs
- Score: 18.763 | Year: 2021 | Citations: 74
- DOI: 10.1609/aaai.v35i4.16477
- Venue: AAAI 2021
- PDF: https://ojs.aaai.org/index.php/AAAI/article/download/16477/16284
- Why rejected: Thermal IR attack using physical heating elements, not RGB patch

### HOTCOLD Block: Fooling Thermal Infrared Detectors with a Novel Wearable Design
- Score: 18.12 | Year: 2023 | Citations: 37
- DOI: 10.1609/aaai.v37i12.26777
- Venue: AAAI 2023
- PDF: https://ojs.aaai.org/index.php/AAAI/article/download/26777/26549
- Why rejected: Wearable thermal attack (Warming/Cooling Paste), not RGB patch

### Physical Adversarial Examples for Person Detectors in Thermal Images Based on 3D Modeling
- Score: 18.002 | Year: 2025 | Citations: 1
- DOI: 10.1109/TPAMI.2025.3582334
- Venue: IEEE TPAMI 2025
- Why rejected: Infrared aerogel clothing — thermal domain

### Reflective Adversarial Attacks against Pedestrian Detection Systems for Vehicles at Night
- Score: 17.948 | Year: 2024 | Citations: 4
- DOI: 10.3390/sym16101262
- Venue: Symmetry (MDPI)
- PDF: https://www.mdpi.com/2073-8994/16/10/1262/pdf?version=1727331252
- Why rejected: Reflective optical material attack (retro-reflection), not printed RGB patch

### Physically structured adversarial patch inspired by natural leaves multiply angles deceives infrared detectors
- Score: 16.948 | Year: 2024 | Citations: 4
- DOI: 10.1016/j.jksuci.2024.102122
- Venue: Journal of King Saud University
- Why rejected: Infrared vehicle detection, wrong modality and domain

### CDUPatch: Color-Driven Universal Adversarial Patch Attack for Dual-Modal Visible-Infrared Detectors
- Score: 17.217 | Year: 2025 | Citations: 5
- DOI: 10.1145/3746027.3755188
- Venue: ACM Multimedia 2025
- arXiv: 2504.10888
- Why rejected: Dual-modal attack optimized for infrared; requires infrared camera; not standard RGB YOLO setting

---

## Spurious Keyword Match

### Diabetic Foot Ulcer Detection: Combining Deep Learning Models for Improved Localization
- Score: 16.85 | Year: 2024 | Citations: 42
- DOI: 10.1007/s12559-024-10267-3
- Venue: Cognitive Computation (Springer)
- Why rejected: Medical imaging (DFU detection) — false positive matching on 'nms', 'yolov8', 'person' in a completely unrelated context
- Pipeline note: Add "diabetic", "medical", "clinical", "ulcer" to soft_penalties if this keeps appearing

---

## Wrong Target: Face Detection (not full-person)

### Got My "Invisibility" Patch: Towards Physical Evasion Attacks on Black-Box Face Detection Systems
- Score: 16.55 | Year: 2025 | Citations: 0
- DOI: 10.1109/TDSC.2025.3582290
- Venue: IEEE Transactions on Dependable and Secure Computing
- Why rejected: Face detection evasion, not full-body person detection; different threat model and dataset

---

## Potential Future Use

- **HOTCOLD Block** (AAAI 2023) and **IR bulbs** (AAAI 2021) — if the capstone includes an IR or multi-modal evasion chapter
- **CDUPatch** (ACM MM 2025) — if extending to multi-modal visible+infrared surveillance cameras
- **Semantic segmentation WACV** (arXiv 2108.06179, 106 citations) — if the project extends to segmentation-based threat models
