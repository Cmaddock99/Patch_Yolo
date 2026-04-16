# Gala et al. (2025) — Evaluating the Impact of Adversarial Patch Attacks on YOLO Models

## Citation

- Title: *Evaluating the Impact of Adversarial Patch Attacks on YOLO Models and the Implications for Edge AI Security*
- Authors: D. L. Gala, J. Molleda, R. Usamentiaga
- Venue / Year: *International Journal of Information Security*, 2025
- DOI: 10.1007/s10207-025-01067-3
- URL: https://link.springer.com/article/10.1007/s10207-025-01067-3
- PDF: `docs/papers/gala2025_adversarial_patch_yolo_edge_s10207.pdf`
- Code: https://github.com/Bimo99B9/NaturalisticAdversarialPatches

## Problem

- What problem is the paper solving? Extend naturalistic adversarial patch generation from older YOLO models into the Ultralytics YOLO family and evaluate the security tradeoff between small edge-friendly models and larger variants.
- What model family is studied? Ultralytics YOLOv5, YOLOv8, YOLOv9, and YOLOv10.
- Why this matters to the repo: This is the closest direct literature benchmark for modern Ultralytics YOLO patch vulnerability in the local corpus.

## Method

- Core approach: adapt a YOLOv4-era naturalistic patch method to the Ultralytics framework so YOLO models can participate directly in backpropagation during patch training (pp. 1-2, 14).
- Patch parameterization: optimize the latent vector of a **BigGAN** generator pretrained on ImageNet instead of optimizing pixels directly (pp. 4-5).
- Objective:
  - `L_total = L_det + λ_tv L_tv`
  - the paper sets `λ_tv = 0.1` (p. 4)
- Optimization settings (Table 1, p. 5):
  - Adam
  - learning rate `0.01`
  - `β1 = 0.5`, `β2 = 0.999`
  - batch size `8-32`
  - `400-1000` epochs depending on experiment
  - latent dimension `120`
  - generator resolution `128 × 128`
- Datasets:
  - INRIA person dataset
  - MPII human pose dataset (pp. 4-6, 14)

## Results

- The paper identifies four especially strong patches on INRIA at scale `0.20`: `patch17`, `patch26`, `patch27`, and `patch38`, with average mAP across all evaluated models of `55.72%`, `55.09%`, `51.43%`, and `51.47%`, respectively (p. 11).
- Table 8 shows those patches consistently beat the baselines on INRIA at scale `0.20` (p. 13):
  - YOLOv5n:
    - random patch `76.44`
    - advyolo baseline `58.42`
    - `patch38 = 36.76`
  - YOLOv8n:
    - random patch `77.43`
    - advyolo baseline `52.59`
    - `patch38 = 48.31`
  - YOLOv10n:
    - random patch `81.53`
    - faster R-CNN baseline `49.15`
    - `patch38 = 39.20`
  - YOLOv10s:
    - advyolo baseline `51.73`
    - `patch27 = 38.23`
- At scale `0.22`, the attack stays strong and often strengthens further (Table 9, p. 13):
  - YOLOv5n `patch38 = 19.90`
  - YOLOv8n `patch38 = 31.27`
  - YOLOv10n `patch38 = 24.51`
  - YOLOv10s `patch27 = 24.66`
- On MPII at scale `0.20`, Table 10 shows the same patches generalize across dataset context (p. 13):
  - YOLOv5n `patch38 = 16.77`
  - YOLOv8n `patch38 = 19.52`
  - YOLOv10n `patch38 = 14.83`
- The paper explicitly states that smaller models are consistently more vulnerable than medium variants, especially the `n` models versus the `m` models (pp. 11-12).
- Edge-device inference numbers reinforce the edge-security tradeoff (Table 12, p. 14):
  - YOLOv8n: `162.60 ms`, `38.51 MB` on the edge device
  - YOLOv10n: `172.64 ms`, `35.65 MB`
  - YOLOv8m: `798.94 ms`, `164.92 MB`
  - YOLOv10m: `728.63 ms`, `125.98 MB`

## Relevance to My Capstone

- Direct relevance to YOLOv8: High. This is one of the most directly comparable local-PDF papers for modern Ultralytics patch attacks.
- Direct relevance to YOLO11: Low to medium. The paper stops at YOLOv10, so it is architectural and benchmarking context, not direct YOLO11 evidence.
- Direct relevance to YOLO26: Low directly, but useful as the best pre-YOLO26 Ultralytics baseline in the repo.
- What I can cite safely:
  - naturalistic GAN-based patches remain effective on YOLOv5/v8/v9/v10
  - small edge-oriented models are generally more vulnerable than medium models
  - the Ultralytics framework can be adapted to support adversarial patch training directly.

## Open Questions

- Why does YOLOv10 sometimes look more vulnerable than YOLOv8/v9 despite being newer?
- Does the same small-model vulnerability trend hold for YOLO11 and YOLO26?
- How much of the repo's own transfer behavior is due to model size versus architectural changes between YOLO generations?

## Normalized Extraction

- Canonical slug: `gala2025_yolo`
- Canonical source record: `docs/papers/gala2025_adversarial_patch_yolo_edge_s10207.pdf`
- Evidence state: `page_cited`
- Threat model: White-box digital naturalistic adversarial patch generation with cross-model evaluation across Ultralytics YOLO families.
- Detector family and exact version: YOLOv5, YOLOv8, YOLOv9, YOLOv10.
- Attack or defense goal: Measure the effectiveness of naturalistic patches on recent Ultralytics YOLO models and relate vulnerability to edge deployment constraints.
- Loss or objective: BigGAN latent optimization with detection loss plus total variation regularization.
- Transforms / EoT: Naturalistic patch generation through latent optimization; the exact transform stack is inherited from the underlying method family but the core promoted detail here is the Ultralytics adaptation plus latent-space training.
- Dataset: INRIA person dataset, MPII human pose dataset.
- Metrics: mAP on patched datasets, cross-model patch evaluation, edge-device inference time and memory.
- Strongest quantitative result: `patch38` reduces INRIA mAP at scale `0.20` to `36.76` on YOLOv5n and `39.20` on YOLOv10n; at scale `0.22` it reduces YOLOv5n / YOLOv8n / YOLOv10n to `19.90 / 31.27 / 24.51` (Tables 8-9, p. 13).
- Transfer findings: Table 7 shows strong cross-model effectiveness of representative patches across YOLOv5 / YOLOv8 / YOLOv9 / YOLOv10 families (pp. 11-12).
- Physical findings: None; the edge-device experiments are deployment-oriented but not physical-world patch tests.
- Direct relevance to YOLOv8 / YOLO11 / YOLO26: High for YOLOv8-era benchmarking, indirect for YOLO11, and baseline-only for YOLO26.
- Reproducible technique to borrow: Ultralytics-compatible detector backpropagation for naturalistic patch training plus the small-model-versus-medium-model comparison framing.
- Citation strength: `page_cited`

## Working Packet Status

- Primary repo question: `yolo11_coverage`
- Disposition: `benchmark`
