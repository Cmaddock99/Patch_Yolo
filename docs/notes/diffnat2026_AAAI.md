# Paper Review: Yan et al. (2026) — Diff-NAT

## Citation

- Title: Diff-NAT: Better Naturalistic and Aggressive Adversarial Attacks via Class-Optimized Diffusion for Object Detection
- Authors: Qinglong Yan, Tong Zou, Xunpeng Yi, Xinyu Xiang, Xuying Wu, Hao Zhang, Jiayi Ma (Wuhan University)
- Venue / Year: AAAI Conference on Artificial Intelligence, Vol. 40 No. 14 (AAAI-26), published March 14, 2026
- URL: https://ojs.aaai.org/index.php/AAAI/article/view/38137
- PDF: ../papers/diffnat2026_AAAI.pdf

## Problem

- What threat model is assumed? White-box; physically realizable; naturalistic appearance required.
- What detector or classifier is attacked? Object detectors (specific YOLO versions not confirmed from abstract; check PDF).
- What is the attack goal? Generate adversarial patches that are simultaneously naturalistic (visually realistic) and aggressively effective. Existing GAN-latent approaches (Hu et al.) constrain optimization to a learned manifold that limits adversarial effectiveness; diffusion priors are broader and more flexible.

## Method

- Patch type: Diffusion-model-generated naturalistic adversarial patches.
- Key innovation over Hu et al. (GAN): Uses pretrained diffusion models as "powerful natural image priors" instead of GANs. Diffusion models offer a richer, more diverse image manifold.
- Optimization method: **Dual-level optimization**:
  1. **Semantic-level**: text prompt refinement — guides the diffusion model toward adversarial class semantics via text conditioning
  2. **Instance-level**: latent code adjustment — fine-grained pixel-level control within the semantic class
  - Together these enable "progressive navigation toward adversarial distributions embedded within the natural semantic manifold"
- Loss terms: Not specified in available abstract — check PDF.
- Physical-world considerations: Both digital and physical evaluations reported.

## Results

- Claims state-of-the-art in both visual realism and adversarial aggressiveness vs. prior SOTA.
- Full quantitative numbers (AP drop, mAP, fooling rate per model) not available from abstract — see downloaded PDF.

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: High — diffusion-based naturalistic patches are the next step beyond GAN-based (Hu 2021, Gala 2025). If YOLO26 is targeted, this method applies.
- What I can cite: As the AAAI-26 state-of-the-art for naturalistic adversarial patches using diffusion models; as the evolution from GAN-latent → diffusion-latent optimization.
- What is missing: Specific YOLO version results require reading the PDF.

## Notes

Full results in downloaded PDF: `docs/papers/diffnat2026_AAAI.pdf`. This paper was previously listed in the knowledge repo without a verified URL — confirmed at AAAI 2026 proceedings.
