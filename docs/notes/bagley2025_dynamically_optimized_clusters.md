# Paper Review: Bagley et al. (2025) — Superpixel Adversarial Patches (SPAP)

## Citation

- Title: Robust Physical Adversarial Patches Using Dynamically Optimized Clusters
- Authors: Harrison Bagley, Will Meakin, Simon Lucey, Yee Wei Law, Tat-Jun Chin
- Venue / Year: arXiv:2511.18656, submitted November 23, 2025
- URL: https://arxiv.org/abs/2511.18656
- PDF: ../papers/bagley2025_dynamically_optimized_clusters_2511.18656.pdf

## Problem

- What threat model is assumed? White-box (YOLOv2 gradients); physically realizable; specifically addresses scale variability — patches lose effectiveness when distance to camera changes due to interpolation-induced color mixing during rescaling.
- What detector or classifier is attacked? YOLOv2 (white-box training); YOLOv5 variants (nano, small, medium, large, x-large), Faster R-CNN, DETR (black-box evaluation).
- What is the attack goal? Create adversarial patches whose structure is robust to rescaling — prior patches use pixel-level noise patterns that are smoothed away by bilinear interpolation when printed or viewed at different distances.

## Method

- Patch type: **Superpixel Adversarial Patches (SPAPs)** — patches constrained to coarse-grained superpixel regions with hard color boundaries rather than fine pixel-level patterns.
- Core innovation: **Differentiable SLIC superpixel clustering via Implicit Function Theorem (IFT)**. SLIC is traditionally non-differentiable; the authors derive gradients through it using IFT to enable end-to-end backpropagation.
  - SLIC objective: `O(X, M) = Σ_i Σ_j a_ij ||ω ⊙ (x_i - μ_j)||²₂` (pixel-to-centroid assignment in 5D color+spatial space)
  - IFT gradient: `∂M/∂X = -[∂F/∂M]⁻¹ [∂F/∂X]`, where F(X*, M*)=0 is the SLIC optimality condition
  - Final color gradient: `∂Ĉ_d/∂C_d = A Γ Aᵀ` (A = assignment matrix, Γ = cardinality normalization)
- Optimization method: AMSGrad variant of Adam, LR=0.03 with ReduceLROnPlateau scheduler (patience=50).
- Loss terms:
  - `L = α·L_TV + L_obj`
  - **L_obj**: max objectness score across anchor points in YOLOv2: `L_obj = max(p_{obj,1}, ..., p_{obj,n})`
  - **L_TV**: total variation smoothness (α=2.5)
  - NPS omitted (patches displayed on screens rather than printed)
- Transformations / EoT: Random rotation, scaling, brightness/contrast, noise.
- Physical-world considerations: **Novel evaluation protocol** — life-sized cardboard cut-outs of celebrities (Pitbull, John Cena, Danny DeVito, Taylor Swift, etc.) with screens displaying patches. Systematic variation of distance (2m–9m), horizontal angle (±45°), vertical angle (±20°).

## Experimental Setup

- Dataset: INRIA Person (training); evaluated digitally on INRIA test set + physically on cardboard cut-outs
- Target classes: Person
- Model versions: YOLOv2 (white-box), YOLOv5n/s/m/l/xl + Faster R-CNN + DETR (black-box)
- Patch parameters: K=4000 superpixels (SPAP-1), K=3600 (SPAP-2); ω=0.1
- Metrics: Average Precision (AP) — lower = stronger attack; objectness score in physical tests

## Results

**Digital (white-box, INRIA test set):**

| Patch | AP |
|---|---|
| Clean baseline | 100% |
| Random patch | 92.23% |
| AdvPatch (with NPS) | 24.97% |
| AdvPatch2 (no NPS) | 44.60% |
| Post-clustering | 30.64% |
| **SPAP-1 (K=4000)** | **22.23%** |
| **SPAP-2 (K=3600)** | **16.28%** |

SPAP-2 achieves 35% improvement over AdvPatch baseline.

**Black-box transferability (AP):**

| Patch | YOLOv2 | YOLOv5n | YOLOv5s | Faster R-CNN | DETR |
|---|---|---|---|---|---|
| AdvPatch | 24.97 | 34.55 | 33.25 | 72.55 | 51.22 |
| SPAP-1 | 22.23 | 27.47 | 37.73 | 68.86 | 48.89 |
| SPAP-2 | 16.28 | 33.91 | 44.20 | 71.11 | 50.61 |

SPAPs outperform AdvPatch on YOLOv5n; performance slightly worse on larger YOLOv5 variants and Faster R-CNN.

**Physical evaluation:** SPAPs maintained effectiveness across 2m–9m distances and ±45° viewing angles. Scale degradation was notably more gradual than pixel-level AdvPatch baselines.

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: High for physical-world evaluation. Schack et al. (2024) identified scale/distance as a key failure mode with no solution — SPAP is exactly that solution. If my capstone includes any physical distance variation, this is the citation.
- What I can reproduce: INRIA + YOLOv2 baseline is straightforward. SLIC gradient derivation is the main implementation effort but the paper provides full derivations.
- What I can cite: For the scale-robustness problem framing; for the IFT-SLIC approach; for the physical evaluation protocol (cardboard cut-outs at varied distances/angles); as a complement to Schack et al.

## Open Questions

- Does this transfer to YOLOv8/YOLO11/YOLO26? Black-box test only goes up to YOLOv5 — extension to Ultralytics v8+ is untested.
- Is the code available? Check arXiv supplementary; not confirmed from abstract.
