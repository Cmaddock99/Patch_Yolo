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
