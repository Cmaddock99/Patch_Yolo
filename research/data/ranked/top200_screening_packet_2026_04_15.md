# Top-200 Screening Packet

Generated: 2026-04-15
Source: `research/data/normalized/papers_deduped.jsonl`
Scope: top 200 ranked candidates cross-referenced against `docs/notes` (50 notes).

## Summary

- Screened candidates: 200
- Existing note overlap: 24
- Immediate full-text queue: 50
- Secondary full-text queue: 48
- Metadata-only rows: 71
- Off-topic skips: 7

## Method

- Match existing coverage by DOI first, then normalized title.
- Bucket candidates into `attack_core`, `defense_core`, `architecture_context`, `generic_context`, or `offtopic_domain` using repo-specific heuristics.
- Map each paper to one primary repo question: `yolo26_architecture_mismatch`, `cross_yolo_transfer`, `physical_robustness`, or `yolo11_coverage`.
- Promote only queue-eligible open-access papers into the immediate queue, deduplicate by normalized title, and park the next tranche as manual retrieval targets.

## Decision Counts

| Bucket | Count |
| --- | ---: |
| `metadata_only` | 71 |
| `deep_read_now` | 50 |
| `queue_for_full_text` | 48 |
| `already_covered` | 24 |
| `skip_offtopic` | 7 |

## Category Counts

| Bucket | Count |
| --- | ---: |
| `attack_core` | 83 |
| `generic_context` | 39 |
| `defense_core` | 36 |
| `architecture_context` | 35 |
| `offtopic_domain` | 7 |

## Primary Repo Questions

| Bucket | Count |
| --- | ---: |
| `cross_yolo_transfer` | 75 |
| `physical_robustness` | 72 |
| `yolo26_architecture_mismatch` | 48 |
| `yolo11_coverage` | 5 |

## Existing Coverage Overlap

These candidates already map to repo notes and should not be treated as unread work.

- Rank 1: *YOLOv10: Real-Time End-to-End Object Detection* -> `docs/notes/wang2024_yolov10_end_to_end.md`
- Rank 2: *The Chosen-Object Attack: Exploiting the Hungarian Matching Loss in Detection Transformers for Fun and Profit* -> `docs/notes/wang2026_chosen_object_attack.md`
- Rank 3: *DETRs with Collaborative Hybrid Assignments Training* -> `docs/notes/zong2022_codetr_hybrid_assignments.md`
- Rank 4: *DETRs Beat YOLOs on Real-time Object Detection* -> `docs/notes/zhao2023_rtdetr_realtime_end_to_end.md`
- Rank 7: *Evaluating the Impact of Adversarial Patch Attacks on YOLO Models and the Implications for Edge AI Security* -> `docs/notes/gala2025_yolo_adversarial_patches.md`
- Rank 11: *Increasing Neural-Based Pedestrian Detectors’ Robustness to Adversarial Patch Attacks Using Anomaly Localization* -> `docs/notes/tereshonok2025_anomaly_localization_defense.md`
- Rank 15: *Dynamic Adversarial Patch for Evading Object Detection Models* -> `docs/notes/hoory2020_dynamic_patch.md`
- Rank 19: *Object Detection Made Simpler by Eliminating Heuristic NMS* -> `docs/notes/zhou2021_nms_free_object_detection.md`
- Rank 21: *Breaking the Illusion: Real-world Challenges for Adversarial Patches in Object Detection* -> `docs/notes/schack2024_real_world_challenges.md`
- Rank 23: *AdvReal: Physical adversarial patch generation framework for security evaluation of object detection systems* -> `docs/notes/huang2025_advreal_physical.md`
- Rank 27: *Entropy-Boosted Adversarial Patch for Concealing Pedestrians in YOLO Models* -> `docs/notes/lin2024_entropy_adversarial_patch.md`
- Rank 31: *Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches* -> `docs/notes/ji2021_adversarial_yolo_defense.md`
- Rank 42: *DPATCH: An Adversarial Patch Attack on Object Detectors* -> `docs/notes/liu2019_dpatch.md`
- Rank 49: *Fooling Automated Surveillance Cameras: Adversarial Patches to Attack Person Detection* -> `docs/notes/thys2019_fooling_surveillance.md`
- Rank 52: *Revisiting Adversarial Patches for Designing Camera-Agnostic Attacks against Person Detection* -> `docs/notes/wei2024_camera_agnostic_CAP.md`
- Rank 57: *Role of Spatial Context in Adversarial Robustness for Object Detection* -> `docs/notes/saha2020_spatial_context_yolo.md`
- Rank 76: *DOEPatch: Dynamically Optimized Ensemble Model for Adversarial Patches Generation* -> `docs/notes/tan2024_DOEPatch.md`
- Rank 78: *FCOS: A Simple and Strong Anchor-Free Object Detector* -> `docs/notes/tian2020_fcos_anchor_free_detector.md`
- Rank 87: *Object Detection Made Simpler by Eliminating Heuristic NMS* -> `docs/notes/zhou2021_nms_free_object_detection.md`
- Rank 93: *Give Me Your Attention: Dot-Product Attention Considered Harmful for Adversarial Patch Robustness* -> `docs/notes/lovisotto2022_attention_patch_robustness.md`
- Rank 128: *Robustness Analysis against Adversarial Patch Attacks in Fully Unmanned Stores* -> `docs/notes/na2025_unmanned_stores.md`
- Rank 131: *Benchmarking Adversarial Robustness and Adversarial Training Strategies for Object Detection* -> `docs/notes/winter2026_benchmarking_robustness.md`
- Rank 134: *Adversarial T-Shirt! Evading Person Detectors in a Physical World* -> `docs/notes/xu2020_adversarial_tshirt.md`
- Rank 136: *ElevPatch: An Adversarial Patch Attack Scheme Based on YOLO11 Object Detector* -> `docs/notes/li2025_elevpatch_yolo11.md`

## Immediate Full-Text Queue

These are the highest-priority open-access candidates not already covered.

5. *HE-DMDeception: Adversarial Attack Network for 3D Object Detection Based on Human Eye and Deep Learning Model Deception* (2025) [`attack_core` | `physical_robustness` | priority 34.05]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
6. *I Don't Know You, But I Can Catch You: Real-Time Defense against Diverse Adversarial Patches for Object Detectors* (2024) [`defense_core` | `physical_robustness` | priority 30.462]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
10. *Complex Scene Occluded Object Detection with Fusion of Mixed Local Channel Attention and Multi-Detection Layer Anchor-Free Optimization* (2024) [`architecture_context` | `cross_yolo_transfer` | priority 29.4]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Architecture context rather than an attack benchmark. Open-access full text is likely available.
17. *PDGV-DETR: Object Detection for Secure On-Site Weapon and Personnel Location Based on Dynamic Convolution and Cross-Scale Semantic Fusion* (2026) [`architecture_context` | `physical_robustness` | priority 27.7]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Architecture context rather than an attack benchmark. Open-access full text is likely available.
22. *Infrared Adversarial Car Stickers* (2024) [`attack_core` | `cross_yolo_transfer` | priority 27.831]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
25. *Improving Transferability of Physical Adversarial Attacks on Object Detectors Through Multi-Model Optimization* (2024) [`attack_core` | `cross_yolo_transfer` | priority 27.616]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
26. *MAGIC: Mastering Physical Adversarial Generation in Context through Collaborative LLM Agents* (2024) [`attack_core` | `physical_robustness` | priority 27.303]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
28. *Fooling the Eyes of Autonomous Vehicles: Robust Physical Adversarial Examples Against Traffic Sign Recognition Systems* (2022) [`defense_core` | `cross_yolo_transfer` | priority 26.608]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. Open-access full text is likely available.
32. *We Can Always Catch You: Detecting Adversarial Patched Objects WITH or WITHOUT Signature* (2021) [`defense_core` | `physical_robustness` | priority 26.256]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
34. *RT-DATR: Real-time Unsupervised Domain Adaptive Detection Transformer with Adversarial Feature Alignment* (2025) [`attack_core` | `cross_yolo_transfer` | priority 26.55]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
35. *Adversarial Texture for Fooling Person Detectors in the Physical World* (2022) [`attack_core` | `physical_robustness` | priority 27.381]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available. Citation count suggests this is a field anchor.
37. *FCA: Learning a 3D Full-Coverage Vehicle Camouflage for Multi-View Physical Adversarial Attack* (2022) [`attack_core` | `cross_yolo_transfer` | priority 27.106]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available. Citation count suggests this is a field anchor.
39. *3D Invisible Cloak: A Robust Person Stealth Attack Against Object Detector in Complex 3D Physical Scenarios* (2020) [`attack_core` | `physical_robustness` | priority 16.016]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
40. *Adversarial Patch Attack on Multi-Scale Object Detection for Remote Sensing Image* (2022) [`attack_core` | `cross_yolo_transfer` | priority 15.983]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
41. *Evaluating the Adversarial Robustness of Detection Transformers* (2024) [`attack_core` | `cross_yolo_transfer` | priority 25.948]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
45. *TPatch: A Triggered Physical Adversarial Patch* (2023) [`defense_core` | `physical_robustness` | priority 25.244]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
46. *Evading Real-Time Person Detectors by Adversarial T-shirt* (2019) [`attack_core` | `cross_yolo_transfer` | priority 25.466]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
50. *HOTCOLD Block: Fooling Thermal Infrared Detectors with a Novel Wearable Design* (2022) [`attack_core` | `physical_robustness` | priority 16.267]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
54. *Reflective Adversarial Attacks against Pedestrian Detection Systems for Vehicles at Night* (2024) [`attack_core` | `physical_robustness` | priority 24.948]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
55. *Rust-Style Patch: A Physical and Naturalistic Camouflage Attacks on Object Detector for Remote Sensing Images* (2023) [`attack_core` | `cross_yolo_transfer` | priority 14.872]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
58. *CDUPatch: Color-Driven Universal Adversarial Patch Attack for Dual-Modal Visible-Infrared Detectors* (2025) [`attack_core` | `cross_yolo_transfer` | priority 14.217]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
61. *Physically structured adversarial patch inspired by natural leaves multiply angles deceives infrared detectors* (2024) [`attack_core` | `cross_yolo_transfer` | priority 23.948]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
63. *Adversarial Patch Attack on Multi-Scale Object Detection for UAV Remote Sensing Images* (2022) [`attack_core` | `cross_yolo_transfer` | priority 13.635]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
64. *Enhancing Object Detection Robustness: Detecting and Restoring Confidence in the Presence of Adversarial Patch Attacks* (2024) [`defense_core` | `physical_robustness` | priority 22.948]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
65. *Infrared Adversarial Patch Generation Based on Reinforcement Learning* (2024) [`attack_core` | `physical_robustness` | priority 23.448]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
67. *Attacking Object Detector Using A Universal Targeted Label-Switch Patch* (2022) [`attack_core` | `cross_yolo_transfer` | priority 23.271]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
68. *X-Detect: explainable adversarial patch detection for object detectors in retail* (2023) [`defense_core` | `cross_yolo_transfer` | priority 12.75]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. Open-access full text is likely available.
70. *IPG: Incremental Patch Generation for Generalized Adversarial Patch Training* (2025) [`defense_core` | `cross_yolo_transfer` | priority 22.502]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. Open-access full text is likely available.
72. *Higher-Order Adversarial Patches for Real-Time Object Detectors* (2026) [`attack_core` | `yolo26_architecture_mismatch` | priority 23.7]
   Access: `open_access_pdf`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Direct attack paper. Open-access full text is likely available.
75. *PAD: Patch-Agnostic Defense against Adversarial Patch Attacks* (2024) [`defense_core` | `physical_robustness` | priority 21.894]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
84. *UP-DETR: Unsupervised Pre-training for Object Detection with Transformers* (2020) [`architecture_context` | `yolo26_architecture_mismatch` | priority 23.019]
   Access: `open_access_pdf`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. Open-access full text is likely available.
88. *Object Detection Models Sensitivity &amp; Robustness to Satellite-based Adversarial Attacks* (2024) [`defense_core` | `yolo26_architecture_mismatch` | priority 12.4]
   Access: `open_access_pdf`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Defense-side comparator. Open-access full text is likely available.
95. *Snake-DETR: a lightweight and efficient model for fine-grained snake detection in complex natural environments* (2025) [`attack_core` | `yolo26_architecture_mismatch` | priority 12.098]
   Access: `open_access_pdf`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Direct attack paper. Open-access full text is likely available.
98. *Group DETR: Fast Training Convergence with Decoupled One-to-Many Label Assignment* (2022) [`architecture_context` | `yolo26_architecture_mismatch` | priority 22.053]
   Access: `open_access_pdf`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. Open-access full text is likely available.
102. *Camouflaged Adversarial Patch Attack on Object Detector* (2023) [`attack_core` | `physical_robustness` | priority 20.966]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
113. *Rpattack: Refined Patch Attack on General Object Detectors* (2021) [`attack_core` | `cross_yolo_transfer` | priority 20.385]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
117. *FCOS: Fully Convolutional One-Stage Object Detection* (2019) [`architecture_context` | `yolo26_architecture_mismatch` | priority 22.15]
   Access: `open_access_pdf`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. Open-access full text is likely available. Citation count suggests this is a field anchor.
120. *Thermally Activated Dual-Modal Adversarial Clothing against AI Surveillance Systems* (2025) [`attack_core` | `physical_robustness` | priority 20.002]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
124. *A Real-Time Defense Against Object Vanishing Adversarial Patch Attacks for Object Detection in Autonomous Vehicles* (2024) [`defense_core` | `physical_robustness` | priority 19.4]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
126. *InvisibiliTee: Angle-agnostic Cloaking from Person-Tracking Systems with a Tee* (2022) [`attack_core` | `physical_robustness` | priority 19.816]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
139. *SSIM-Based Autoencoder Modeling to Defeat Adversarial Patch Attacks* (2024) [`attack_core` | `physical_robustness` | priority 19.303]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
146. *Delving into YOLO Object Detection Models: Insights into Adversarial Robustness* (2025) [`attack_core` | `physical_robustness` | priority 19.112]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
147. *A Survey on Physical Adversarial Attack in Computer Vision* (2023) [`attack_core` | `physical_robustness` | priority 19.066]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
149. *Daedalus: Breaking Non-Maximum Suppression in Object Detection via Adversarial Examples* (2019) [`attack_core` | `cross_yolo_transfer` | priority 18.984]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
173. *DPAttack: Diffused Patch Attacks against Universal Object Detection* (2020) [`attack_core` | `cross_yolo_transfer` | priority 18.037]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
174. *IPatch: a remote adversarial patch* (2023) [`attack_core` | `cross_yolo_transfer` | priority 18.014]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
179. *Location-independent adversarial patch generation for object detection* (2023) [`attack_core` | `cross_yolo_transfer` | priority 17.966]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
188. *Towards Generic and Controllable Attacks Against Object Detection* (2023) [`attack_core` | `cross_yolo_transfer` | priority 17.702]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
189. *Beyond the Patch: Exploring Vulnerabilities of Visuomotor Policies via Viewpoint-Consistent 3D Adversarial Object* (2026) [`attack_core` | `cross_yolo_transfer` | priority 17.7]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.
195. *Adversarial Attention Deficit: Fooling Deformable Vision Transformers with Collaborative Adversarial Patches* (2025) [`attack_core` | `cross_yolo_transfer` | priority 17.502]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. Open-access full text is likely available.

## Secondary Full-Text Queue

These are the next candidates to fetch or read after the immediate queue.

9. *YOLO-AlignRank: Cross-Scale Deformable Head and Rank-Consistent Loss for One-Stage Object Detection* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 28.55]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
18. *Mitigating Adversarial Attacks in Object Detection using Multi-Modal Fusion in Autonomous Vehicles* (2025) [`defense_core` | `physical_robustness` | priority 26.05]
   Access: `landing_only`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. May require library or manual retrieval.
29. *Physical Adversarial Examples for Person Detectors in Thermal Images Based on 3D Modeling* (2025) [`attack_core` | `cross_yolo_transfer` | priority 25.05]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
30. *Research on YOLOv10-Mamba-Based Object Detection Algorithm* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 25.05]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
33. *MAGIC: Mastering Physical Adversarial Generation in Context Through Collaborative LLM Agents* (2026) [`attack_core` | `physical_robustness` | priority 24.7]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
38. *YOLOv8-FSRT: A Wheat Head Detection and Counting Model Based on the RT-DETR Decoder* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 24.05]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
43. *Gradient-Free Sparse Adversarial Attack on Object Detection Models* (2025) [`attack_core` | `physical_robustness` | priority 23.766]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
48. *Adversarial Lens Flares: A Threat to Camera-Based Systems in Smart Devices* (2024) [`defense_core` | `physical_robustness` | priority 22.852]
   Access: `landing_only`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. May require library or manual retrieval.
51. *HOTCOLD Block: Fooling Thermal Infrared Detectors with a Novel Wearable Design* (2023) [`attack_core` | `physical_robustness` | priority 15.12]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
59. *Improving End-to-End Object Detection by Enhanced Attention* (2024) [`attack_core` | `yolo26_architecture_mismatch` | priority 23.116]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Direct attack paper. May require library or manual retrieval.
60. *A Comparative Study of YOLOv3 and YOLOv10 for hCAPTCHA Challenge Solving* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 22.05]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
69. *Research on Improvement of Fire Hydrant Target Detection Algorithm Based on YOLOv10* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 21.05]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
71. *Physically Adversarial Infrared Patches with Learnable Shapes and Locations* (2023) [`attack_core` | `physical_robustness` | priority 20.73]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
77. *Adversarial Infrared Geometry: Using Geometry to Perform Adversarial Attack against Infrared Pedestrian Detectors* (2024) [`defense_core` | `cross_yolo_transfer` | priority 11.852]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. Open-access full text is likely available.
81. *BadPatch: Diffusion-Based Generation of Physical Adversarial Patches* (2024) [`defense_core` | `physical_robustness` | priority 11.616]
   Access: `open_access_pdf`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. Open-access full text is likely available.
83. *Localization and Elimination: Object Detection Physical Patch Defense Based on Adversarial Patch Characterization* (2025) [`defense_core` | `physical_robustness` | priority 9.55]
   Access: `landing_only`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. May require library or manual retrieval.
89. *Object Detection Models Sensitivity & Robustness to Satellite-based Adversarial Attacks* (2024) [`defense_core` | `yolo26_architecture_mismatch` | priority 10.352]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Defense-side comparator. May require library or manual retrieval.
90. *Securing Autonomous Vehicles Visual Perception: Adversarial Patch Attack and Defense Schemes With Experimental Validations* (2024) [`defense_core` | `physical_robustness` | priority 19.164]
   Access: `landing_only`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. May require library or manual retrieval.
92. *A Novel Adversarial Patch Attack on YOLOv8-based Brain Tumor Detection Model* (2025) [`defense_core` | `physical_robustness` | priority 19.05]
   Access: `landing_only`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. May require library or manual retrieval.
94. *Stealthy Adversarial Patch for Evading Object Detectors Based on Sensitivity Maps* (2024) [`attack_core` | `physical_robustness` | priority 9.352]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
96. *Diffusion to Confusion: Naturalistic Adversarial Patch Generation Based on Diffusion Model for Object Detector* (2023) [`attack_core` | `physical_robustness` | priority 11.096]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
99. *Learning from the Environment: A Novel Adversarial Patch Attack against Object Detectors Using a GAN Trained on Image Slices* (2025) [`attack_core` | `physical_robustness` | priority 19.05]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
100. *SPAttack: A Physically Feasible Adversarial Patch Attack Against SAR Target Detection* (2025) [`attack_core` | `cross_yolo_transfer` | priority 9.002]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
101. *Physically Realizable Adversarial Creating Attack Against Vision-Based BEV Space 3D Object Detection* (2025) [`defense_core` | `cross_yolo_transfer` | priority 18.469]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. May require library or manual retrieval.
103. *An Adaptive Adversarial Patch-Generating Algorithm for Defending against the Intelligent Low, Slow, and Small Target* (2023) [`defense_core` | `cross_yolo_transfer` | priority 10.421]
   Access: `open_access_pdf`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. Open-access full text is likely available.
107. *Localized Query Attack Toward Transformer-Based Visible Object Detectors* (2026) [`attack_core` | `cross_yolo_transfer` | priority 18.7]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
108. *FAB-Attack: Fabric-Aware Adversarial Attacks on Person Detectors under Motion Blur* (2025) [`attack_core` | `physical_robustness` | priority 18.55]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
109. *LADF-YOLO: A Highly Accurate Low-Light Target Detection Algorithm* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 18.55]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
110. *A Unified Framework for Adversarial Patch Attacks Against Visual 3D Object Detection in Autonomous Driving* (2025) [`defense_core` | `cross_yolo_transfer` | priority 18.015]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. May require library or manual retrieval.
111. *A Novel YOLOv5 Deep Learning Model for Handwriting Detection and Recognition* (2022) [`attack_core` | `yolo26_architecture_mismatch` | priority 19.455]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Direct attack paper. May require library or manual retrieval.
123. *Towards a Robust Adversarial Patch Attack Against Unmanned Aerial Vehicles Object Detection* (2023) [`attack_core` | `cross_yolo_transfer` | priority 7.966]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
141. *Advertising or adversarial? AdvSign: Artistic advertising sign camouflage for target physical attacking to object detector* (2025) [`attack_core` | `physical_robustness` | priority 17.266]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
142. *Implementing NMS-Free Training Using YOLOv10 on Mammographic Images to Detect Breast Cancer* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 17.266]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
148. *Universal Adversarial Perturbations for Two-Stage Black-Box Object Detectors* (2025) [`attack_core` | `cross_yolo_transfer` | priority 17.002]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
152. *Legitimate Adversarial Patches* (2021) [`attack_core` | `physical_robustness` | priority 16.869]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
154. *A Unified, Resilient, and Explainable Adversarial Patch Detector* (2025) [`defense_core` | `physical_robustness` | priority 16.266]
   Access: `landing_only`. Expected output: Defense comparator for the capstone risk discussion.
   Reason: Useful for physical robustness or deployment realism. Defense-side comparator. May require library or manual retrieval.
158. *Evaluating the Practical Effectiveness of Adversarial Patches Against YOLOv8* (2025) [`attack_core` | `cross_yolo_transfer` | priority 16.55]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
160. *Transferable Physical Adversarial Patch Attack for Remote Sensing Object Detection* (2024) [`attack_core` | `cross_yolo_transfer` | priority 6.4]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
169. *L-HAWK: A Controllable Physical Adversarial Patch Against a Long-Distance Target* (2025) [`attack_core` | `physical_robustness` | priority 16.098]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
176. *PNAP-YOLO: An Improved Prompts-Based Naturalistic Adversarial Patch Model for Object Detectors* (2025) [`attack_core` | `cross_yolo_transfer` | priority 16.002]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.
178. *An Enhanced Transferable Adversarial Attack Against Object Detection* (2023) [`defense_core` | `cross_yolo_transfer` | priority 15.466]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. May require library or manual retrieval.
183. *DynamicPAE: Generating Scene-Aware Physical Adversarial Examples in Real-Time* (2024) [`attack_core` | `physical_robustness` | priority 7.9]
   Access: `open_access_pdf`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. Open-access full text is likely available.
184. *Invisible Cloak to AI Recognition from All Horizontal Directions by Adversarial Patch* (2024) [`attack_core` | `physical_robustness` | priority 15.9]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
191. *Enhancing robustness of person detection: A universal defense filter against adversarial patch attacks* (2024) [`defense_core` | `cross_yolo_transfer` | priority 15.067]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Defense-side comparator. May require library or manual retrieval.
192. *Natural Physical Adversarial Attack Method for UAV Visual Detection System* (2025) [`attack_core` | `physical_robustness` | priority 5.55]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
193. *Physical Adversarial Patch Attack for Optical Fine-Grained Aircraft Recognition* (2025) [`attack_core` | `physical_robustness` | priority 5.55]
   Access: `landing_only`. Expected output: Physical benchmark or robustness method to borrow.
   Reason: Useful for physical robustness or deployment realism. Direct attack paper. May require library or manual retrieval.
194. *Shadow-DETR: Alleviating matching conflicts through shadow queries* (2025) [`architecture_context` | `yolo26_architecture_mismatch` | priority 15.55]
   Access: `landing_only`. Expected output: Architecture note tying detector design to patch-loss mismatch.
   Reason: Useful for the YOLO26 architecture-mismatch question. Architecture context rather than an attack benchmark. May require library or manual retrieval.
198. *MalPatch: Evading DNN-Based Malware Detection With Adversarial Patches* (2024) [`attack_core` | `cross_yolo_transfer` | priority 15.47]
   Access: `landing_only`. Expected output: Transfer benchmark or surrogate-training tactic.
   Reason: Useful for cross-YOLO transfer or multi-model patch training. Direct attack paper. May require library or manual retrieval.

## Full Screening Table

| Rank | Decision | Category | Repo question | Score | Title |
| ---: | --- | --- | --- | ---: | --- |
| 1 | `already_covered` | `architecture_context` | `yolo26_architecture_mismatch` | 34.9 | YOLOv10: Real-Time End-to-End Object Detection |
| 2 | `already_covered` | `attack_core` | `yolo26_architecture_mismatch` | 20.2 | The Chosen-Object Attack: Exploiting the Hungarian Matching Loss in Detection Transformers for Fun and Profit |
| 3 | `already_covered` | `architecture_context` | `yolo26_architecture_mismatch` | 29.6 | DETRs with Collaborative Hybrid Assignments Training |
| 4 | `already_covered` | `architecture_context` | `yolo26_architecture_mismatch` | 28.8 | DETRs Beat YOLOs on Real-time Object Detection |
| 5 | `deep_read_now` | `attack_core` | `physical_robustness` | 34.0 | HE-DMDeception: Adversarial Attack Network for 3D Object Detection Based on Human Eye and Deep Learning Model Deception |
| 6 | `deep_read_now` | `defense_core` | `physical_robustness` | 30.5 | I Don't Know You, But I Can Catch You: Real-Time Defense against Diverse Adversarial Patches for Object Detectors |
| 7 | `already_covered` | `attack_core` | `yolo26_architecture_mismatch` | 21.8 | Evaluating the Impact of Adversarial Patch Attacks on YOLO Models and the Implications for Edge AI Security |
| 8 | `metadata_only` | `generic_context` | `yolo26_architecture_mismatch` | 29.7 | YOLOv5, YOLOv8 and YOLOv10: The Go-To Detectors for Real-time Vision |
| 9 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 28.6 | YOLO-AlignRank: Cross-Scale Deformable Head and Rank-Consistent Loss for One-Stage Object Detection |
| 10 | `deep_read_now` | `architecture_context` | `cross_yolo_transfer` | 29.4 | Complex Scene Occluded Object Detection with Fusion of Mixed Local Channel Attention and Multi-Detection Layer Anchor-Free Optimization |
| 11 | `already_covered` | `defense_core` | `physical_robustness` | 19.8 | Increasing Neural-Based Pedestrian Detectors’ Robustness to Adversarial Patch Attacks Using Anomaly Localization |
| 12 | `metadata_only` | `generic_context` | `physical_robustness` | 15.2 | PDD: Post-Disaster Dataset for Human Detection and Performance Evaluation |
| 13 | `skip_offtopic` | `offtopic_domain` | `yolo26_architecture_mismatch` | 16.6 | Hybrid CNN-Transformer Model for Accurate Impacted Tooth Detection in Panoramic Radiographs |
| 14 | `metadata_only` | `generic_context` | `yolo11_coverage` | 29.0 | YOLO advances to its genesis: a decadal and comprehensive review of the You Only Look Once (YOLO) series |
| 15 | `already_covered` | `attack_core` | `cross_yolo_transfer` | 20.4 | Dynamic Adversarial Patch for Evading Object Detection Models |
| 16 | `skip_offtopic` | `offtopic_domain` | `physical_robustness` | 5.1 | RF-DETR Object Detection vs YOLOv12 : A Study of Transformer-based and CNN-based Architectures for Single-Class and Multi-Class Greenfruit Detection in Complex Orchard Environments Under Label Ambiguity |
| 17 | `deep_read_now` | `architecture_context` | `physical_robustness` | 27.7 | PDGV-DETR: Object Detection for Secure On-Site Weapon and Personnel Location Based on Dynamic Convolution and Cross-Scale Semantic Fusion |
| 18 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 26.1 | Mitigating Adversarial Attacks in Object Detection using Multi-Modal Fusion in Autonomous Vehicles |
| 19 | `already_covered` | `architecture_context` | `yolo26_architecture_mismatch` | 18.1 | Object Detection Made Simpler by Eliminating Heuristic NMS |
| 20 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 18.1 | KD-DETR: Knowledge Distillation for Detection Transformer with Consistent Distillation Points Sampling |
| 21 | `already_covered` | `defense_core` | `physical_robustness` | 17.3 | Breaking the Illusion: Real-world Challenges for Adversarial Patches in Object Detection |
| 22 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 27.8 | Infrared Adversarial Car Stickers |
| 23 | `already_covered` | `attack_core` | `cross_yolo_transfer` | 17.8 | AdvReal: Physical adversarial patch generation framework for security evaluation of object detection systems |
| 24 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 17.7 | CLoCKDistill: Consistent Location-and-Context-aware Knowledge Distillation for DETRs |
| 25 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 27.6 | Improving Transferability of Physical Adversarial Attacks on Object Detectors Through Multi-Model Optimization |
| 26 | `deep_read_now` | `attack_core` | `physical_robustness` | 27.3 | MAGIC: Mastering Physical Adversarial Generation in Context through Collaborative LLM Agents |
| 27 | `already_covered` | `attack_core` | `cross_yolo_transfer` | 17.1 | Entropy-Boosted Adversarial Patch for Concealing Pedestrians in YOLO Models |
| 28 | `deep_read_now` | `defense_core` | `cross_yolo_transfer` | 26.6 | Fooling the Eyes of Autonomous Vehicles: Robust Physical Adversarial Examples Against Traffic Sign Recognition Systems |
| 29 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 25.1 | Physical Adversarial Examples for Person Detectors in Thermal Images Based on 3D Modeling |
| 30 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 25.1 | Research on YOLOv10-Mamba-Based Object Detection Algorithm |
| 31 | `already_covered` | `defense_core` | `physical_robustness` | 16.5 | Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches |
| 32 | `deep_read_now` | `defense_core` | `physical_robustness` | 26.3 | We Can Always Catch You: Detecting Adversarial Patched Objects WITH or WITHOUT Signature |
| 33 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 24.7 | MAGIC: Mastering Physical Adversarial Generation in Context Through Collaborative LLM Agents |
| 34 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 26.6 | RT-DATR: Real-time Unsupervised Domain Adaptive Detection Transformer with Adversarial Feature Alignment |
| 35 | `deep_read_now` | `attack_core` | `physical_robustness` | 27.4 | Adversarial Texture for Fooling Person Detectors in the Physical World |
| 36 | `metadata_only` | `attack_core` | `yolo26_architecture_mismatch` | 17.2 | Adversarially Robust and Explainable Insulator Defect Detection for Smart Grid Infrastructure |
| 37 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 27.1 | FCA: Learning a 3D Full-Coverage Vehicle Camouflage for Multi-View Physical Adversarial Attack |
| 38 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 24.1 | YOLOv8-FSRT: A Wheat Head Detection and Counting Model Based on the RT-DETR Decoder |
| 39 | `deep_read_now` | `attack_core` | `physical_robustness` | 16.0 | 3D Invisible Cloak: A Robust Person Stealth Attack Against Object Detector in Complex 3D Physical Scenarios |
| 40 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 16.0 | Adversarial Patch Attack on Multi-Scale Object Detection for Remote Sensing Image |
| 41 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 25.9 | Evaluating the Adversarial Robustness of Detection Transformers |
| 42 | `already_covered` | `attack_core` | `cross_yolo_transfer` | 17.8 | DPATCH: An Adversarial Patch Attack on Object Detectors |
| 43 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 23.8 | Gradient-Free Sparse Adversarial Attack on Object Detection Models |
| 44 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 23.8 | Fooling Thermal Infrared Pedestrian Detectors in Real World Using Small Bulbs |
| 45 | `deep_read_now` | `defense_core` | `physical_robustness` | 25.2 | TPatch: A Triggered Physical Adversarial Patch |
| 46 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 25.5 | Evading Real-Time Person Detectors by Adversarial T-shirt |
| 47 | `metadata_only` | `attack_core` | `physical_robustness` | 23.4 | Full-Distance Evasion of Pedestrian Detectors in the Physical World |
| 48 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 22.9 | Adversarial Lens Flares: A Threat to Camera-Based Systems in Smart Devices |
| 49 | `already_covered` | `attack_core` | `physical_robustness` | 16.3 | Fooling Automated Surveillance Cameras: Adversarial Patches to Attack Person Detection |
| 50 | `deep_read_now` | `attack_core` | `physical_robustness` | 16.3 | HOTCOLD Block: Fooling Thermal Infrared Detectors with a Novel Wearable Design |
| 51 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 15.1 | HOTCOLD Block: Fooling Thermal Infrared Detectors with a Novel Wearable Design |
| 52 | `already_covered` | `defense_core` | `physical_robustness` | 12.6 | Revisiting Adversarial Patches for Designing Camera-Agnostic Attacks against Person Detection |
| 53 | `skip_offtopic` | `offtopic_domain` | `yolo26_architecture_mismatch` | 12.0 | Recognizing Egyptian currency for people with visual impairment using deep learning models |
| 54 | `deep_read_now` | `attack_core` | `physical_robustness` | 24.9 | Reflective Adversarial Attacks against Pedestrian Detection Systems for Vehicles at Night |
| 55 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 14.9 | Rust-Style Patch: A Physical and Naturalistic Camouflage Attacks on Object Detector for Remote Sensing Images |
| 56 | `metadata_only` | `attack_core` | `physical_robustness` | 12.6 | MagShadow: Physical Adversarial Example Attacks via Electromagnetic Injection |
| 57 | `already_covered` | `defense_core` | `physical_robustness` | 14.8 | Role of Spatial Context in Adversarial Robustness for Object Detection |
| 58 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 14.2 | CDUPatch: Color-Driven Universal Adversarial Patch Attack for Dual-Modal Visible-Infrared Detectors |
| 59 | `queue_for_full_text` | `attack_core` | `yolo26_architecture_mismatch` | 23.1 | Improving End-to-End Object Detection by Enhanced Attention |
| 60 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 22.1 | A Comparative Study of YOLOv3 and YOLOv10 for hCAPTCHA Challenge Solving |
| 61 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 23.9 | Physically structured adversarial patch inspired by natural leaves multiply angles deceives infrared detectors |
| 62 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 20.9 | Diabetic Foot Ulcer Detection: Combining Deep Learning Models for Improved Localization |
| 63 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 13.6 | Adversarial Patch Attack on Multi-Scale Object Detection for UAV Remote Sensing Images |
| 64 | `deep_read_now` | `defense_core` | `physical_robustness` | 22.9 | Enhancing Object Detection Robustness: Detecting and Restoring Confidence in the Presence of Adversarial Patch Attacks |
| 65 | `deep_read_now` | `attack_core` | `physical_robustness` | 23.4 | Infrared Adversarial Patch Generation Based on Reinforcement Learning |
| 66 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 13.3 | Transformer-based End-to-End Object Detection in Aerial Images |
| 67 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 23.3 | Attacking Object Detector Using A Universal Targeted Label-Switch Patch |
| 68 | `deep_read_now` | `defense_core` | `cross_yolo_transfer` | 12.8 | X-Detect: explainable adversarial patch detection for object detectors in retail |
| 69 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 21.1 | Research on Improvement of Fire Hydrant Target Detection Algorithm Based on YOLOv10 |
| 70 | `deep_read_now` | `defense_core` | `cross_yolo_transfer` | 22.5 | IPG: Incremental Patch Generation for Generalized Adversarial Patch Training |
| 71 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 20.7 | Physically Adversarial Infrared Patches with Learnable Shapes and Locations |
| 72 | `deep_read_now` | `attack_core` | `yolo26_architecture_mismatch` | 23.7 | Higher-Order Adversarial Patches for Real-Time Object Detectors |
| 73 | `metadata_only` | `architecture_context` | `physical_robustness` | 11.5 | LW-DETR: a lightweight transformer-based object detection algorithm for efficient railway crossing surveillance |
| 74 | `metadata_only` | `architecture_context` | `physical_robustness` | 12.5 | Enhancing UAV Aerial Image Analysis: Integrating Advanced SAHI Techniques With Real-Time Detection Models on the VisDrone Dataset |
| 75 | `deep_read_now` | `defense_core` | `physical_robustness` | 21.9 | PAD: Patch-Agnostic Defense against Adversarial Patch Attacks |
| 76 | `already_covered` | `attack_core` | `cross_yolo_transfer` | 12.4 | DOEPatch: Dynamically Optimized Ensemble Model for Adversarial Patches Generation |
| 77 | `queue_for_full_text` | `defense_core` | `cross_yolo_transfer` | 11.9 | Adversarial Infrared Geometry: Using Geometry to Perform Adversarial Attack against Infrared Pedestrian Detectors |
| 78 | `already_covered` | `architecture_context` | `yolo26_architecture_mismatch` | 14.3 | FCOS: A Simple and Strong Anchor-Free Object Detector |
| 79 | `metadata_only` | `generic_context` | `physical_robustness` | 20.2 | Exploring Deep Learning-Based Architecture, Strategies, Applications and Current Trends in Generic Object Detection: A Comprehensive Review |
| 80 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 9.1 | ESFD-YOLOv8n: Early Smoke and Fire Detection Method Based on an Improved YOLOv8n Model |
| 81 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 11.6 | BadPatch: Diffusion-Based Generation of Physical Adversarial Patches |
| 82 | `metadata_only` | `defense_core` | `physical_robustness` | 22.6 | DetectorGuard: Provably Securing Object Detectors against Localized Patch Hiding Attacks |
| 83 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 9.6 | Localization and Elimination: Object Detection Physical Patch Defense Based on Adversarial Patch Characterization |
| 84 | `deep_read_now` | `architecture_context` | `yolo26_architecture_mismatch` | 23.0 | UP-DETR: Unsupervised Pre-training for Object Detection with Transformers |
| 85 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 12.0 | CV-YOLOv10-AR-M: Foreign Object Detection in Pu-Erh Tea Based on Five-Fold Cross-Validation |
| 86 | `metadata_only` | `attack_core` | `physical_robustness` | 12.0 | Research and optimization of a multilevel fire detection framework based on deep learning and classical pattern recognition techniques |
| 87 | `already_covered` | `architecture_context` | `yolo26_architecture_mismatch` | 11.9 | Object Detection Made Simpler by Eliminating Heuristic NMS |
| 88 | `deep_read_now` | `defense_core` | `yolo26_architecture_mismatch` | 12.4 | Object Detection Models Sensitivity &amp; Robustness to Satellite-based Adversarial Attacks |
| 89 | `queue_for_full_text` | `defense_core` | `yolo26_architecture_mismatch` | 10.4 | Object Detection Models Sensitivity & Robustness to Satellite-based Adversarial Attacks |
| 90 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 19.2 | Securing Autonomous Vehicles Visual Perception: Adversarial Patch Attack and Defense Schemes With Experimental Validations |
| 91 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 11.6 | Multi‐Scale Feature Attention‐DEtection TRansformer: Multi‐Scale Feature Attention for security check object detection |
| 92 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 19.1 | A Novel Adversarial Patch Attack on YOLOv8-based Brain Tumor Detection Model |
| 93 | `already_covered` | `attack_core` | `yolo26_architecture_mismatch` | 12.4 | Give Me Your Attention: Dot-Product Attention Considered Harmful for Adversarial Patch Robustness |
| 94 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 9.4 | Stealthy Adversarial Patch for Evading Object Detectors Based on Sensitivity Maps |
| 95 | `deep_read_now` | `attack_core` | `yolo26_architecture_mismatch` | 12.1 | Snake-DETR: a lightweight and efficient model for fine-grained snake detection in complex natural environments |
| 96 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 11.1 | Diffusion to Confusion: Naturalistic Adversarial Patch Generation Based on Diffusion Model for Object Detector |
| 97 | `metadata_only` | `generic_context` | `yolo26_architecture_mismatch` | 20.1 | YOLOv1 to YOLOv10: The Fastest and Most Accurate Real-time Object Detection Systems |
| 98 | `deep_read_now` | `architecture_context` | `yolo26_architecture_mismatch` | 22.1 | Group DETR: Fast Training Convergence with Decoupled One-to-Many Label Assignment |
| 99 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 19.1 | Learning from the Environment: A Novel Adversarial Patch Attack against Object Detectors Using a GAN Trained on Image Slices |
| 100 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 9.0 | SPAttack: A Physically Feasible Adversarial Patch Attack Against SAR Target Detection |
| 101 | `queue_for_full_text` | `defense_core` | `cross_yolo_transfer` | 18.5 | Physically Realizable Adversarial Creating Attack Against Vision-Based BEV Space 3D Object Detection |
| 102 | `deep_read_now` | `attack_core` | `physical_robustness` | 21.0 | Camouflaged Adversarial Patch Attack on Object Detector |
| 103 | `queue_for_full_text` | `defense_core` | `cross_yolo_transfer` | 10.4 | An Adaptive Adversarial Patch-Generating Algorithm for Defending against the Intelligent Low, Slow, and Small Target |
| 104 | `metadata_only` | `attack_core` | `yolo26_architecture_mismatch` | 21.9 | BankTweak: Adversarial Attack against Multi-Object Trackers by Manipulating Feature Banks |
| 105 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 10.8 | A high precision YOLO model for surface defect detection based on PyConv and CISBA |
| 106 | `metadata_only` | `architecture_context` | `physical_robustness` | 19.7 | YOLO-lychee-advanced: an optimized detection model for lychee pest damage based on YOLOv11 |
| 107 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 18.7 | Localized Query Attack Toward Transformer-Based Visible Object Detectors |
| 108 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 18.6 | FAB-Attack: Fabric-Aware Adversarial Attacks on Person Detectors under Motion Blur |
| 109 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 18.6 | LADF-YOLO: A Highly Accurate Low-Light Target Detection Algorithm |
| 110 | `queue_for_full_text` | `defense_core` | `cross_yolo_transfer` | 18.0 | A Unified Framework for Adversarial Patch Attacks Against Visual 3D Object Detection in Autonomous Driving |
| 111 | `queue_for_full_text` | `attack_core` | `yolo26_architecture_mismatch` | 19.5 | A Novel YOLOv5 Deep Learning Model for Handwriting Detection and Recognition |
| 112 | `metadata_only` | `attack_core` | `cross_yolo_transfer` | 20.5 | PhysPatch: A Physically Realizable and Transferable Adversarial Patch Attack for Multimodal Large Language Models-based Autonomous Driving Systems |
| 113 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 20.4 | Rpattack: Refined Patch Attack on General Object Detectors |
| 114 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 19.3 | An Evaluation of Deep Learning Methods for Small Object Detection |
| 115 | `metadata_only` | `defense_core` | `physical_robustness` | 19.8 | UMFNet: Frequency-Guided Multi-Scale Fusion with Dynamic Noise Suppression for Robust Low-Light Object Detection |
| 116 | `metadata_only` | `architecture_context` | `yolo11_coverage` | 10.7 | Enhanced YOLO12 with spatial pyramid pooling for real-time cotton insect detection |
| 117 | `deep_read_now` | `architecture_context` | `yolo26_architecture_mismatch` | 22.1 | FCOS: Fully Convolutional One-Stage Object Detection |
| 118 | `metadata_only` | `generic_context` | `yolo11_coverage` | 18.5 | A Study on the Detection Method for Split Pin Defects in Power Transmission Lines Based on Two-Stage Detection and Mamba-YOLO-SPDC |
| 119 | `metadata_only` | `attack_core` | `cross_yolo_transfer` | 8.0 | Cost-effective and robust adversarial patch attacks in real-world scenarios |
| 120 | `deep_read_now` | `attack_core` | `physical_robustness` | 20.0 | Thermally Activated Dual-Modal Adversarial Clothing against AI Surveillance Systems |
| 121 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 19.0 | The YOLO Framework: A Comprehensive Review of Evolution, Applications, and Benchmarks in Object Detection |
| 122 | `metadata_only` | `generic_context` | `yolo26_architecture_mismatch` | 18.0 | YOLOv10 to Its Genesis: A Decadal and Comprehensive Review of The You Only Look Once Series |
| 123 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 8.0 | Towards a Robust Adversarial Patch Attack Against Unmanned Aerial Vehicles Object Detection |
| 124 | `deep_read_now` | `defense_core` | `physical_robustness` | 19.4 | A Real-Time Defense Against Object Vanishing Adversarial Patch Attacks for Object Detection in Autonomous Vehicles |
| 125 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 19.9 | Advancing precision agriculture: A comparative analysis of YOLOv8 for multi-class weed detection in cotton cultivation |
| 126 | `deep_read_now` | `attack_core` | `physical_robustness` | 19.8 | InvisibiliTee: Angle-agnostic Cloaking from Person-Tracking Systems with a Tee |
| 127 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 7.8 | Microarmature Solder Surface Detection: An Adaptive Central Region Sample Selection Anchor Free Framework |
| 128 | `already_covered` | `defense_core` | `physical_robustness` | -0.7 | Robustness Analysis against Adversarial Patch Attacks in Fully Unmanned Stores |
| 129 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 9.7 | WRRT-DETR: Weather-Robust RT-DETR for Drone-View Object Detection in Adverse Weather |
| 130 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 17.7 | An enhanced real-time human pose estimation method based on modified YOLOv8 framework |
| 131 | `already_covered` | `defense_core` | `cross_yolo_transfer` | 9.2 | Benchmarking Adversarial Robustness and Adversarial Training Strategies for Object Detection |
| 132 | `metadata_only` | `generic_context` | `physical_robustness` | 6.7 | A novel hybrid deep learning approach for super-resolution and objects detection in remote sensing |
| 133 | `metadata_only` | `generic_context` | `physical_robustness` | 16.6 | Generative Image Steganography via Encoding Pose Keypoints |
| 134 | `already_covered` | `attack_core` | `physical_robustness` | 9.6 | Adversarial T-Shirt! Evading Person Detectors in a Physical World |
| 135 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 6.6 | YOLOv8n_BT: Research on Classroom Learning Behavior Recognition Algorithm Based on Improved YOLOv8n |
| 136 | `already_covered` | `attack_core` | `yolo11_coverage` | 9.1 | ElevPatch: An Adversarial Patch Attack Scheme Based on YOLO11 Object Detector |
| 137 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 16.4 | YOLOv8-MU: An Improved YOLOv8 Underwater Detector Based on a Large Kernel Block and a Multi-Branch Reparameterization Module |
| 138 | `metadata_only` | `generic_context` | `yolo26_architecture_mismatch` | 19.4 | Object Detection Using Deep Learning, CNNs and Vision Transformers: A Review |
| 139 | `deep_read_now` | `attack_core` | `physical_robustness` | 19.3 | SSIM-Based Autoencoder Modeling to Defeat Adversarial Patch Attacks |
| 140 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 16.3 | Precise Detection for Dense PCB Components Based on Modified YOLOv8 |
| 141 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 17.3 | Advertising or adversarial? AdvSign: Artistic advertising sign camouflage for target physical attacking to object detector |
| 142 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 17.3 | Implementing NMS-Free Training Using YOLOv10 on Mammographic Images to Detect Breast Cancer |
| 143 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 19.2 | Improving YOLOv11 for marine water quality monitoring and pollution source identification |
| 144 | `metadata_only` | `attack_core` | `physical_robustness` | 19.2 | Adversarial Patch Attacks on Deep-Learning-Based Face Recognition Systems Using Generative Adversarial Networks |
| 145 | `metadata_only` | `defense_core` | `cross_yolo_transfer` | 18.7 | Turn Fake into Real: Adversarial Head Turn Attacks Against Deepfake Detection |
| 146 | `deep_read_now` | `attack_core` | `physical_robustness` | 19.1 | Delving into YOLO Object Detection Models: Insights into Adversarial Robustness |
| 147 | `deep_read_now` | `attack_core` | `physical_robustness` | 19.1 | A Survey on Physical Adversarial Attack in Computer Vision |
| 148 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 17.0 | Universal Adversarial Perturbations for Two-Stage Black-Box Object Detectors |
| 149 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 19.0 | Daedalus: Breaking Non-Maximum Suppression in Object Detection via Adversarial Examples |
| 150 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 17.9 | Democratising deep learning for microscopy with ZeroCostDL4Mic |
| 151 | `metadata_only` | `generic_context` | `physical_robustness` | 15.9 | From COCO to COCO-FP: A Deep Dive into Background False Positives for COCO Detectors |
| 152 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 16.9 | Legitimate Adversarial Patches |
| 153 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 15.8 | Dense Pedestrian Detection Based on GR-YOLO |
| 154 | `queue_for_full_text` | `defense_core` | `physical_robustness` | 16.3 | A Unified, Resilient, and Explainable Adversarial Patch Detector |
| 155 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 15.7 | Fabric Defect Detection in Real World Manufacturing Using Deep Learning |
| 156 | `metadata_only` | `attack_core` | `cross_yolo_transfer` | 18.7 | Attention-Guided Digital Adversarial Patches on Visual Detection |
| 157 | `metadata_only` | `generic_context` | `physical_robustness` | 17.6 | Multimodal biomedical AI |
| 158 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 16.6 | Evaluating the Practical Effectiveness of Adversarial Patches Against YOLOv8 |
| 159 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 6.5 | SAFF-DETR: An End-to-End Object Detection Network for Remote Sensing Images With Targets of Varying Sizes Based on Scale Adaptation and Frequency Fusion |
| 160 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 6.4 | Transferable Physical Adversarial Patch Attack for Remote Sensing Object Detection |
| 161 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 15.4 | MAS-YOLOv11: An Improved Underwater Object Detection Algorithm Based on YOLOv11 |
| 162 | `metadata_only` | `architecture_context` | `yolo26_architecture_mismatch` | 18.3 | Object Detection Based on Improved YOLOv10 for Electrical Equipment Image Classification |
| 163 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 6.3 | TPH-YOLOv5++: Boosting Object Detection on Drone-Captured Scenarios with Cross-Layer Asymmetric Transformer |
| 164 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 7.2 | YOLO-v1 to YOLO-v8, the Rise of YOLO and Its Complementary Nature toward Digital Manufacturing and Industrial Defect Detection |
| 165 | `metadata_only` | `attack_core` | `physical_robustness` | 18.2 | PapMOT: Exploring Adversarial Patch Attack Against Multiple Object Tracking |
| 166 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 16.2 | Pothole Detection Using Deep Learning: A Real‐Time and AI‐on‐the‐Edge Perspective |
| 167 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 17.1 | A Bottom-Up Clustering Approach to Unsupervised Person Re-Identification |
| 168 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 16.1 | YOLO Object Detection for Real-Time Fabric Defect Inspection in the Textile Industry: A Review of YOLOv1 to YOLOv11 |
| 169 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 16.1 | L-HAWK: A Controllable Physical Adversarial Patch Against a Long-Distance Target |
| 170 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 6.1 | TPH-YOLOv5: Improved YOLOv5 Based on Transformer Prediction Head for Object Detection on Drone-captured Scenarios |
| 171 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 16.1 | Traffic Sign Detection and Recognition Using YOLO Object Detection Algorithm: A Systematic Review |
| 172 | `metadata_only` | `attack_core` | `yolo26_architecture_mismatch` | 7.0 | Improved YOLOv10 model for detecting surface defects on solar photovoltaic panels |
| 173 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 18.0 | DPAttack: Diffused Patch Attacks against Universal Object Detection |
| 174 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 18.0 | IPatch: a remote adversarial patch |
| 175 | `metadata_only` | `generic_context` | `yolo11_coverage` | 16.5 | AGS-YOLO: An Efficient Underwater Small-Object Detection Network for Low-Resource Environments |
| 176 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 16.0 | PNAP-YOLO: An Improved Prompts-Based Naturalistic Adversarial Patch Model for Object Detectors |
| 177 | `metadata_only` | `generic_context` | `physical_robustness` | 15.0 | Enhancing Object Detection in Smart Video Surveillance: A Survey of Occlusion-Handling Approaches |
| 178 | `queue_for_full_text` | `defense_core` | `cross_yolo_transfer` | 15.5 | An Enhanced Transferable Adversarial Attack Against Object Detection |
| 179 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 18.0 | Location-independent adversarial patch generation for object detection |
| 180 | `metadata_only` | `generic_context` | `physical_robustness` | 15.0 | Computer Vision Based Areal Photographic Rocket Detection using YOLOv8 Models |
| 181 | `skip_offtopic` | `offtopic_domain` | `cross_yolo_transfer` | -5.1 | Object Detection Method for Grasping Robot Based on Improved YOLOv5 |
| 182 | `metadata_only` | `generic_context` | `physical_robustness` | 14.9 | Survey on Image-Based Vehicle Detection Methods |
| 183 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 7.9 | DynamicPAE: Generating Scene-Aware Physical Adversarial Examples in Real-Time |
| 184 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 15.9 | Invisible Cloak to AI Recognition from All Horizontal Directions by Adversarial Patch |
| 185 | `metadata_only` | `defense_core` | `physical_robustness` | 17.3 | Just Rotate it: Deploying Backdoor Attacks via Rotation Transformation |
| 186 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 15.8 | Yolo-tla: An Efficient and Lightweight Small Object Detection Model based on YOLOv5 |
| 187 | `skip_offtopic` | `offtopic_domain` | `cross_yolo_transfer` | -6.2 | YOLOv11-EMD: An Enhanced Object Detection Algorithm Assisted by Multi-Stage Transfer Learning for Industrial Steel Surface Defect Detection |
| 188 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 17.7 | Towards Generic and Controllable Attacks Against Object Detection |
| 189 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 17.7 | Beyond the Patch: Exploring Vulnerabilities of Visuomotor Policies via Viewpoint-Consistent 3D Adversarial Object |
| 190 | `metadata_only` | `defense_core` | `yolo26_architecture_mismatch` | 16.2 | An Anchor-Free Dual-Branch Approach for Real-Time Metro Passenger Detection |
| 191 | `queue_for_full_text` | `defense_core` | `cross_yolo_transfer` | 15.1 | Enhancing robustness of person detection: A universal defense filter against adversarial patch attacks |
| 192 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 5.5 | Natural Physical Adversarial Attack Method for UAV Visual Detection System |
| 193 | `queue_for_full_text` | `attack_core` | `physical_robustness` | 5.5 | Physical Adversarial Patch Attack for Optical Fine-Grained Aircraft Recognition |
| 194 | `queue_for_full_text` | `architecture_context` | `yolo26_architecture_mismatch` | 15.6 | Shadow-DETR: Alleviating matching conflicts through shadow queries |
| 195 | `deep_read_now` | `attack_core` | `cross_yolo_transfer` | 17.5 | Adversarial Attention Deficit: Fooling Deformable Vision Transformers with Collaborative Adversarial Patches |
| 196 | `metadata_only` | `generic_context` | `cross_yolo_transfer` | 15.5 | Object Detection in Autonomous Vehicles under Adverse Weather: A Review of Traditional and Deep Learning Approaches |
| 197 | `skip_offtopic` | `offtopic_domain` | `cross_yolo_transfer` | 4.5 | SenseFi: A library and benchmark on deep-learning-empowered WiFi human sensing |
| 198 | `queue_for_full_text` | `attack_core` | `cross_yolo_transfer` | 15.5 | MalPatch: Evading DNN-Based Malware Detection With Adversarial Patches |
| 199 | `skip_offtopic` | `offtopic_domain` | `cross_yolo_transfer` | 4.4 | Machine Learning and Deep Learning for Plant Disease Classification and Detection |
| 200 | `metadata_only` | `generic_context` | `physical_robustness` | 5.4 | A YOLOv6-Based Improved Fire Detection Approach for Smart City Environments |

