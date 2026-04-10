# Paper Review: Lin et al. (2024) — Entropy-Boosted Adversarial Patch

## Citation

- Title: Entropy-Boosted Adversarial Patch for Concealing Pedestrians in YOLO Models
- Authors: Lin, Huang, Ng, Lin, Farady
- Venue / Year: IEEE Access, 2024
- URL: https://ieeexplore.ieee.org/abstract/document/10453548/
- PDF: https://ieeexplore.ieee.org/iel7/6287639/10380310/10453548.pdf (IEEE institutional access)

## ⚠️ Access Note

IEEE Xplore blocks automated scraping (HTTP 418). Paper confirmed real at the IEEE Xplore URL above. Access via institution for full content. Content below is based on the provided description.

## Problem (from description)

- What is the attack goal? Conceal pedestrians from YOLO detectors using adversarial patches. Introduces **entropy as a loss term** to make patches look more natural while remaining adversarial — provides a third naturalism approach distinct from GAN-latent (Hu et al.) and pixel-similarity (DAP/Guesmi et al.).

## Method (from description)

- Key innovation: **Entropy maximization loss** added to the optimization objective. Higher entropy in the patch image = more varied pixel distribution = more visually natural appearance (avoids the obvious uniform or structured noise of naive patch optimization).
- Does not require a pretrained GAN or diffusion model — naturalness is achieved through a simple information-theoretic loss term.
- Loss terms: Standard detection suppression loss + entropy term (maximizes entropy of patch pixel distribution) + possibly TV/NPS.

## Why This Matters

Provides a third naturalism paradigm for the capstone's related-work section:
1. GAN-latent optimization (Hu et al. 2021, Gala et al. 2025)
2. Cosine similarity to benign image (DAP, Guesmi et al. 2024)
3. **Entropy maximization** (Lin et al. 2024)

The entropy approach is simpler to implement than GAN or diffusion methods and may be worth including in a methods comparison.

## Action Required

1. Access via IEEE institution link
2. Record: exact YOLO versions tested, datasets, quantitative AP/recall results
3. Record: exact entropy loss formulation
4. Update this note with full details

## Relevance to My Capstone

- Direct relevance to YOLOv8/YOLO11/YOLO26: Moderate — the entropy approach is applicable to any YOLO version.
- What I can cite: As a simpler alternative to GAN-based naturalism; for the three-paradigm naturalism comparison.
