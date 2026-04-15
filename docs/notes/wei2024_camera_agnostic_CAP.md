# Paper Review: Wei et al. (2024) — CAP (Camera-Agnostic Patch)

## Citation

- Title: Revisiting Adversarial Patches for Designing Camera-Agnostic Attacks against Person Detection
- Authors: Hui Wei, Zhixiang Wang, Kewei Zhang, Jiaqi Hou, Yuanwei Liu, Hao Tang, Zheng Wang
- Venue / Year: NeurIPS 2024 (Advances in Neural Information Processing Systems 37), Main Conference Track
- URL: https://proceedings.neurips.cc/paper_files/paper/2024/hash/0f5cb62a8e3331b253c232e229cd551e-Abstract-Conference.html
- PDF: ../papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf

## Problem

- What threat model is assumed? White-box; physically realizable; targets real-world deployment where the same patch must work across different cameras (smartphones, webcams, surveillance cameras).
- What detector or classifier is attacked? Person detection systems.
- What is the attack goal? Create adversarial patches that remain effective across multiple different cameras and imaging devices, not just the single device used for patch training. Prior work trains on a fixed camera pipeline; CAP generalizes across cameras by modeling camera Image Signal Processing (ISP) explicitly.

## Method

- Patch type: Adversarial patch trained with a differentiable camera ISP proxy network — physically realizable.
- Key innovation: **Differentiable ISP proxy network** that models the physical-to-digital conversion process (demosaicing, color correction, tone mapping). Bridges the gap between the printed patch in the physical world and its digital representation after camera processing.
- Optimization method: Adversarial game between:
  - **Attack module**: optimizes patch pixels to suppress person detections
  - **Defense module**: competes to maintain detections, strengthening the attack's generalization
- The ISP proxy enables gradients to flow through the camera model during training, making the patch robust to different ISP pipelines.
- Transformations / EoT details: Standard augmentations + ISP variation simulation via the proxy network.
- Physical-world considerations: Cross-camera stability demonstrated across multiple imaging devices.

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: High if extending to physical-world evaluation with actual cameras. The camera-agnostic property is important for any physical test where patch photos are taken with different devices.
- What I can cite: For the camera-ISP physical-world gap argument; as the NeurIPS 2024 state-of-the-art for camera-robust person-vanishing patches.
- What is missing for my project: Specific YOLO versions tested not confirmed from abstract alone — check the paper PDF for per-model numbers.

## Notes

Full quantitative results available in the downloaded PDF (see `docs/papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf`). The abstract confirms NeurIPS 2024 main track publication; content above is from the official NeurIPS proceedings page.

## Results

- Digital-space evaluation uses YOLOv5 fine-tuned on INRIA Person with AP and ASR under multiple ISP settings.
- CAP outperforms the comparison attacks across randomized ISP settings and avoids the multi-box failure mode that hurts T-SEA in ASR despite large AP drops (Table 2, pp. 6-7).
- Real-world cross-camera evaluation covers six devices: Sony, Canon, iPhone, Redmi, Huawei, and Samsung.
- The paper’s headline qualitative result is a shift from **1/6 successful cameras for AdvPatch** to **6/6 successful cameras for CAP** in the same scene setup (Figure 1, p. 1).
- In physical tests, CAP achieves **more than 90% ASR on all six cameras** and reaches **100% ASR on iPhone and Huawei** (Section 4.3, p. 7).

## Limitations and Failure Modes

- Evaluated on YOLOv5 only; no direct YOLOv8, YOLO11, or YOLO26 numbers in the local PDF.
- The method depends on a trained differentiable ISP proxy and additional real-camera calibration data.
- Strong physical results come from a camera-agnostic setup, not a general transfer study across detector architectures.

## Normalized Extraction

- Canonical slug: `wei2024_CAP`
- Canonical source record: `docs/papers/wei2024_camera_agnostic_CAP_NeurIPS.pdf`
- Evidence state: `page_cited`
- Threat model: White-box patch optimization against a person detector with black-box physical evaluation across unseen camera pipelines.
- Detector family and exact version: YOLOv5 fine-tuned for person detection.
- Attack or defense goal: Preserve physical attack effectiveness across heterogeneous cameras by modeling the physical-to-digital ISP transition.
- Loss or objective: Adversarial optimization game between the patch and a differentiable ISP proxy network that acts as a defender.
- Transforms / EoT: Standard digital-to-physical augmentations plus learned ISP simulation across parameterized camera pipelines.
- Dataset: INRIA Person for digital-space attack; six-camera physical capture setup for real-world evaluation.
- Metrics: AP and ASR in digital space; ASR in physical space.
- Strongest quantitative result: CAP reaches 6/6 successful cameras in the headline scene comparison and exceeds 90% ASR on every evaluated camera in physical tests (Figure 1, p. 1; Section 4.3, p. 7).
- Transfer findings: The key transfer axis is cross-camera rather than cross-detector; CAP is designed for camera-agnostic physical transfer.
- Physical findings: Camera ISP is a first-order source of physical attack failure; explicitly modeling it turns a highly unstable patch into a stable one.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: Relevant to any future physical evaluation regardless of detector generation; detector-side architecture is secondary to camera variability here.
- Reproducible technique to borrow: Treat camera ISP as an adversarially optimized differentiable preprocessing module during patch training.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `physical_robustness`
- Disposition: `method_to_borrow`
