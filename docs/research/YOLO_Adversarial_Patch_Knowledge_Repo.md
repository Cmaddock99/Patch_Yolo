> Working draft imported into this repository on 2026-04-10.
>
> Use `docs/research/verified_sources.md` as the checked bibliography before citing claims from this document in a paper or presentation.

# Adversarial Patch Attacks on YOLO — Capstone Knowledge Repository
### Cal State San Marcos — Cybersecurity BS Capstone
*Compiled: April 2026 | Sources: Google Scholar, arXiv, GitHub, SSRN, EmergentMind*

---

## 1. Foundational Concepts

### What is YOLO and Why is It Vulnerable?
YOLO (You Only Look Once) is a family of one-stage, real-time object detection models that jointly predict bounding boxes, objectness scores, and class probabilities in a single forward pass through a convolutional neural network. Unlike two-stage detectors (e.g., Faster R-CNN), YOLO performs detection in one shot using a grid-based regression/classification head — which is both its speed advantage and its security weakness.

The vulnerability stems from YOLO's joint regression-classification structure: a small, localized input perturbation can simultaneously disrupt objectness confidence, bounding box localization, and class prediction — three attack surfaces in one.

**YOLO version landscape (relevant to your project):**
- YOLOv2/v3: oldest, most studied in adversarial literature
- YOLOv4/v5: widely deployed, well-documented attack/defense
- YOLOv8/v9/v10: modern Ultralytics framework versions, recently attacked for the first time in Gala et al. (2025)
- YOLO11: brand new, only one dedicated adversarial patch paper exists (ElevPatch, 2025)
- YOLO26: newest NMS-free end-to-end architecture (Chakrabarty, 2026) — adversarial research essentially nonexistent

### What is an Adversarial Patch?
An adversarial patch is a small, physically-printable image region that, when placed in a scene, causes a trained neural network to produce wrong outputs. Unlike pixel-level adversarial examples (which are imperceptible), patches are concentrated, visible, and designed to work in the physical world — printed on clothing, stickers on cars, screens in environments, etc.

**Key properties:**
- **Universal**: one patch fools the model across many different images/scenes
- **Physically realizable**: can be printed and still work under real-world lighting/angle changes
- **Localized**: only occupies a small spatial region of the input
- **Transferable**: a patch trained against one model can sometimes fool other models (black-box transfer)

---

## 2. Attack Taxonomy

| Attack Type | Placement | Goal |
|---|---|---|
| Global/Universal suppression | Anywhere in image | Minimize overall mAP, suppress all classes |
| Local/object-specific vanishing | Overlapping the target | Remove one object from detection |
| Label-switch targeted | On/near target | Force misclassification to a specific wrong class |
| Dynamic (viewpoint-adaptive) | Multiple switched patches | Maintain evasion across angles/poses |
| Stealthy/naturalistic | Designed to look like real images | Evade both human inspection and model-based detection |
| Triggered (TPatch) | Benign normally, adversarial on trigger | Activates only under specified conditions |
| Remote patch | Outside target bounding box | Fool detection without overlapping the target |

**For a capstone project**, the most achievable and academically meaningful choice is a **local person-vanishing attack** (making YOLO ignore a person wearing a printed patch), using a **universal patch** so one design works across images.

---

## 3. The Math Behind Patch Generation

The core idea is gradient-based optimization. You optimize the patch pixels P by maximizing the YOLO detection loss over a dataset:

```
P* = argmax_{P} E_{x~D, t~T} [ L_YOLO(f(A(P, x, t))) ]
```

Where:
- `x` = input image from dataset D
- `t` = a random transformation (rotation, scale, translation) sampled from distribution T
- `A(P, x, t)` = the patch P applied to image x with transform t
- `f(·)` = the YOLO model's forward pass
- `L_YOLO` = the YOLO detection loss (objectness + classification + localization)

**The Expectation over Transformations (EoT) pipeline** is critical: by sampling random transforms during training, you make the patch robust to real-world positional/scale variation. Without EoT, a patch that works digitally often fails in the physical world.

**Additional loss terms used in advanced patches:**
- **Total Variation (TV) loss**: penalizes sharp, noisy patterns — promotes smoothness for faithful printing
- **Non-Printability Score (NPS)**: penalizes colors that standard printers can't reproduce accurately
- **Naturalness / GAN latent space loss**: used in naturalistic patches to constrain to realistic-looking images

---

## 4. Naturalistic Patches (State-of-the-Art)

The Gala, Molleda & Usamentiaga paper (IJIS 2025) uses a significantly more sophisticated approach:

**Key innovation:** Instead of directly optimizing raw pixel values, they optimize in the **latent space of a pre-trained BigGAN**. The generator G maps a latent vector z to an image: `P = G(z)`. They then optimize z using gradient descent through the GAN generator into YOLO.

**Why this matters:**
1. The patch is constrained to the manifold of realistic-looking images (looks like a peacock, dog, etc.)
2. Makes it harder for human observers and automated patch-detection defenses to flag it
3. Achieves higher real-world success rates because it's visually coherent

**Results:** Their best patches (patch27, patch38) achieved significant mAP drops across YOLOv5, v8, v9, v10 at patch_scale=0.20. Smaller models (n/s variants) were more vulnerable than larger ones (m variant).

---

## 5. Naturalistic Patch Generation Paradigms (2025 Taxonomy)

From Diff-NAT (Yan et al., AAAI 2026), there are now three recognized paradigms:

1. **GAN latent space optimization** — optimize z in BigGAN latent space (Gala et al., original NaturalisticAdversarialPatch repo)
2. **Diffusion model generation** — use a diffusion model to generate realistic patches (AdvLogo, Diff-NAT, Oonishi et al.)
3. **Prompt-based naturalistic patches** — condition generation on text/image prompts (PNAP-YOLO, MAGIC with LLM agents)

---

## 6. Datasets Used

**INRIA Person Dataset**: The standard benchmark for person detection adversarial patch research. ~2,000 labeled images of pedestrians in various outdoor settings. Publicly available, free for academic use.

**MPII Human Pose Dataset**: Also used for evaluation. Contains images with diverse person poses.

**COCO (MS COCO)**: Used for multi-class attack evaluation.

**nuImage**: Used in MAGIC (2024) for physical-world driving scene experiments.

---

## 7. Step-by-Step: Building Your Adversarial Patch

### Official Repository
**GitHub:** https://github.com/Bimo99B9/NaturalisticAdversarialPatches
(Gala, Molleda, Usamentiaga — International Journal of Information Security, 2025)

### Step 1: Environment Setup
```bash
git clone https://github.com/Bimo99B9/NaturalisticAdversarialPatches
cd NaturalisticAdversarialPatches
# Prerequisites: NVIDIA GPU, Docker, NVIDIA Container Toolkit
docker build -t naturalistic-adversarial-patch .
```

### Step 2: Download Data and Weights
```bash
bash setup_dataset.sh          # Downloads INRIA Person dataset
bash ./GANLatentDiscovery/download_weights.sh  # Downloads BigGAN weights
# YOLO weights download automatically on first run via ultralytics
```

### Step 3: Train a Patch
```bash
docker run --gpus all --shm-size=4g \
  -v "$(pwd)/dataset:/usr/src/app/dataset" \
  -v "$(pwd)/exp:/usr/src/app/exp" \
  -it naturalistic-adversarial-patch \
  python ensemble.py \
    --model yolov8n \          # Start with smallest/most vulnerable model
    --classBiggan 84 \         # ImageNet class 84 = Peacock
    --epochs 1000 \
    --weight_loss_tv 0.1 \
    --learning_rate 0.01
```

Monitor with TensorBoard: `tensorboard --logdir=./exp`

### Key Training Arguments
| Argument | Description |
|---|---|
| --model | YOLO detector: yolov5n, yolov5m, yolov8n, yolov9t, yolo11n |
| --classBiggan | ImageNet class ID for GAN (84=Peacock, 259=Pomeranian dog) |
| --epochs | Number of training epochs (1000 recommended) |
| --weight_loss_tv | Total variation loss weight (0.1 recommended) |
| --learning_rate | Optimizer learning rate (0.01 recommended) |

### Step 4: Evaluate Your Patch
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements_eval.txt
./run_eval_patch.sh exp_your_patch_name
```

**Evaluation parameters to vary for capstone experiments:**
- `patch_scale`: 0.10, 0.15, 0.20, 0.25 — measure mAP vs. visibility tradeoff
- `patch_mode`: 0=adversarial, 1=white, 2=gray, 3=random — compare vs. naive baselines
- `--model`: vary from yolo11n through yolo11m to demonstrate size/robustness tradeoff

### Step 5: Live Demo
```bash
xhost +local:docker
docker run --gpus all --rm -it \
  --env="DISPLAY" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  naturalistic-adversarial-patch \
  python camera_test.py
```

---

## 8. Physical-World Considerations

- **Scale**: A patch covering ~20% of the target bounding box area (scale=0.20) is standard. In practice ~30cm×30cm on a T-shirt at typical surveillance distances.
- **Print quality**: Use NPS loss during optimization to keep patch colors within CMYK printable gamut.
- **Lighting sensitivity**: Patches can lose effectiveness under overexposure or certain LED hue spectra. Test under multiple lighting conditions. Shack et al. found up to 64% digital-to-physical performance discrepancy.
- **Rotation robustness**: Efficacy typically degrades above ~20° out-of-plane rotation. EoT pipeline helps by training with simulated rotations.
- **Material effects**: Cloth wrinkles affect the patch pattern. DAP uses a "creases transformation" during training to simulate this.
- **Remote patches**: Can be placed outside the target's bounding box entirely (Oonishi et al., 2022) — significant real-world threat surface.

---

## 9. Defenses You Should Know About

| Defense | Method | Recovery Rate | Overhead |
|---|---|---|---|
| Ad-YOLO (Ji et al., 2021) | Adds patch-detection class head to YOLO | 33.93% → 80.31% AP | Negligible |
| Grad-CAM filtering (Liang et al., 2021) | Mask high-activation regions for target class | 92% attack TPR | 85ms/frame |
| Semantic consistency (Liang et al., 2021) | Region-growing: detects disappearance when patch included | 95% detection | 1.5s/frame |
| Adversarial training + EoT | Include patches in training data | Improves robustness generally | Training cost |
| IPG (Lee et al., 2025) | Incremental patch generation for defense knowledge | Up to 11.1x more efficient training | — |
| Patch detection backbone (Gu et al., 2025) | Five YOLO backbone variants + patch detection layer | Most stable config identified | — |

---

## 10. YOLO11 Specific Research

### ElevPatch (Li, Liao, Li, Zhang, Wu, Jiayan — Springer ICAICS 2025)
**The first dedicated adversarial patch attack paper targeting YOLO11.** Generates adversarial patches from visible-light images and analyzes their impact specifically against YOLO11.
- Citation: X Li, H Liao, H Li, J Zhang, X Wu, E Jiayan — International Conference on Advanced Intelligent Computing and Applications, 2025, Springer

### Apostolidis & Papakostas (2025) — Electronics, MDPI (Open Access)
"Delving into YOLO Object Detection Models: Insights into Adversarial Robustness"
Comprehensive survey testing adversarial attacks including patch-based ones against YOLOv7, YOLOR-CSP, and **all sizes of YOLO11**. Introduces "eigenpatches" — PCA-derived patches that efficiently fool models. 17 citations already.
- URL: https://www.mdpi.com/2079-9292/14/3/563

### Adapting the NaturalisticAdversarialPatches Repo for YOLO11
The Gala et al. repo supports Ultralytics models. YOLO11 is part of the Ultralytics framework, so you can likely target it by passing `--model yolo11n` (or `yolo11s`, `yolo11m`). This would be an original contribution of your capstone.

---

## 11. 2024–2025 New Papers Summary

### arXiv Papers (Free, Open Access)

| Paper | arXiv ID | Key Contribution |
|---|---|---|
| Breaking the Illusion (Shack et al., 2024) | 2410.19863 | Physical-world YOLO patch study; 64% digital-physical gap |
| MAGIC (Xing et al., 2024) | 2412.08014 | LLM agents generate context-aware physical adversarial patches |
| IPG (Lee et al., 2025) | 2508.10946 | 11.1x more efficient patch generation |
| TPatch (Zhu et al., 2024) | 2401.00148 | Acoustic-triggered adversarial patch; USENIX Security 2023 |
| Adversarial T-shirt (Xu et al., 2020) | 1910.11099 | Non-rigid deformation modeling for cloth patches |
| DPatch (Liu et al., 2018/2019) | 1806.02299 | Original black-box patch attack on YOLO/Faster R-CNN |
| RPAttack (Huang et al., 2021) | 2103.12469 | Refined minimal-pixel patch; 100% miss rate modifying only 0.32% pixels |

### Journal/Conference Papers (2024–2025)

| Paper | Venue | Key Contribution |
|---|---|---|
| ElevPatch (Li et al., 2025) | Springer ICAICS | First adversarial patch attack on YOLO11 |
| Apostolidis & Papakostas (2025) | Electronics/MDPI | Adversarial robustness survey across all YOLO11 sizes |
| PNAP-YOLO (Li et al., 2025) | Annals of Data Science | Prompt-based naturalistic adversarial patches |
| From Vulnerability to Robustness (Liu & Xu, 2025) | Electronics/MDPI | Comprehensive survey of 2018–2025 patch attacks & defenses |
| Revisiting Patch Defenses (Zheng et al., 2025) | CVPR 2025 | 94-patch-type dataset; unified defense evaluation |
| Diff-NAT (Yan et al., 2026) | AAAI 2026 | First taxonomy of naturalistic patch paradigms; diffusion-based |
| Adversarial Patch vs UAV Detection (Quaranta, 2025) | Polito Thesis | Patches against YOLO for drone detection |
| GAN-Based Attack & Defense for YOLO (Aljaberi, 2025) | Staffordshire Thesis | Full attack+defense pipeline for video surveillance YOLO |
| Transferable Adversarial Patches (Labarbarie, 2024) | HAL Science Thesis | Wasserstein-distance approach for cross-architecture transfer |
| TOG Attacks Transferability in Maritime (Manasut et al., 2025) | IEEE | YOLO transfer attack study in maritime domain |

---

## 12. Recommended Reading Order

1. **DPatch (arXiv:1806.02299)** — Start here. The foundational paper. Understand the original attack.
2. **Adversarial T-shirt (arXiv:1910.11099)** — Physical-world realization, non-rigid deformation.
3. **Gala et al. (IJIS 2025)** — Your primary reference. Naturalistic GAN-based patches on YOLOv5-v10.
4. **Breaking the Illusion (arXiv:2410.19863)** — Essential for understanding physical-world limitations.
5. **ElevPatch (Springer, 2025)** — The YOLO11 specific attack paper.
6. **Apostolidis & Papakostas (Electronics, 2025)** — YOLO11 robustness survey.
7. **From Vulnerability to Robustness (Electronics, 2025)** — Full landscape survey for your lit review.
8. **CVPR 2025 Defense Paper (Zheng et al.)** — For your defense section.
9. **MAGIC (arXiv:2412.08014)** — For your "future directions" section.
10. **Diff-NAT (AAAI 2026)** — Cutting edge; naturalistic patch paradigm taxonomy.

---

## 13. Capstone Project Structure

### Suggested Research Question
"How effective are naturalistic GAN-based adversarial patches at evading modern YOLO object detectors (YOLOv8/YOLO11), and what factors (model size, patch scale, model architecture) determine the degree of vulnerability?"

### Suggested Sections
1. **Background**: YOLO architecture evolution, adversarial ML threat model, YOLO11 specifics
2. **Related Work**: DPatch → adversarial-yolo → naturalistic patches → YOLO11 (ElevPatch) progression
3. **Methodology**: EoT pipeline, GAN latent optimization, experimental setup (INRIA dataset)
4. **Experiments**: mAP comparison across models/scales, vs. random/white/gray baselines
5. **Results & Analysis**: Model size vs. robustness, patch scale vs. effectiveness
6. **Physical Demo** (optional but strong): Print and test patch on T-shirt
7. **Defenses**: Discuss Ad-YOLO, Grad-CAM, adversarial training approaches
8. **Future Work**: YOLO11 deeper analysis, YOLO26/NMS-free architectures as open gap

### Original Contribution Options
- Extend the Gala et al. repo to officially support YOLO11 (likely just adding the model flag)
- Compare ElevPatch vs. naturalistic GAN patch on YOLO11 — no paper does this yet
- Test whether patches trained on YOLOv8 transfer to YOLO11 (cross-version transferability)
- Benchmark attack effectiveness vs. model size on YOLO11n/s/m/l

---

## 14. Key Papers to Cite (BibTeX format)

```bibtex
@article{Gala2025,
  author = {Gala, D. L. and Molleda, J. and Usamentiaga, R.},
  title = {Evaluating the Impact of Adversarial Patch Attacks on YOLO Models and the Implications for Edge AI Security},
  journal = {International Journal of Information Security},
  year = {2025},
  volume = {24},
  number = {3},
  pages = {154},
  doi = {10.1007/s10207-025-01067-3}
}

@article{apostolidis2025,
  author = {Apostolidis, K. D. and Papakostas, G. A.},
  title = {Delving into YOLO Object Detection Models: Insights into Adversarial Robustness},
  journal = {Electronics},
  year = {2025},
  publisher = {MDPI},
  note = {Open Access}
}

@inproceedings{li2025elevpatch,
  author = {Li, X. and Liao, H. and Li, H. and Zhang, J. and Wu, X. and Jiayan, E.},
  title = {ElevPatch: An Adversarial Patch Attack Scheme Based on YOLO11 Object Detector},
  booktitle = {International Conference on Advanced Intelligent Computing and Applications},
  year = {2025},
  publisher = {Springer}
}

@article{liu2019dpatch,
  author = {Liu, X. and Yang, H. and Liu, Z. and Song, L. and Li, H. and Chen, Y.},
  title = {DPatch: An Adversarial Patch Attack on Object Detectors},
  journal = {arXiv preprint arXiv:1806.02299},
  year = {2019}
}

@article{shack2024breaking,
  author = {Shack, J. and Petrovic, K. and Saukh, O.},
  title = {Breaking the Illusion: Real-world Challenges for Adversarial Patches in Object Detection},
  journal = {arXiv preprint arXiv:2410.19863},
  year = {2024}
}

@inproceedings{xing2024magic,
  author = {Xing, Y. and Chung, N. and Zhang, J. and Cao, Y. and Tsang, I. and Liu, Y. and Ma, L. and Guo, Q.},
  title = {MAGIC: Mastering Physical Adversarial Generation in Context through Collaborative LLM Agents},
  journal = {arXiv preprint arXiv:2412.08014},
  year = {2024}
}

@misc{lee2025ipg,
  author = {Lee, W. and Na, H. and Lee, J. and Choi, D.},
  title = {IPG: Incremental Patch Generation for Generalized Adversarial Patch Training},
  journal = {arXiv preprint arXiv:2508.10946},
  year = {2025}
}

@inproceedings{ji2021adversarialyolo,
  author = {Ji, N. and Feng, Y. and Xie, H. and Xiang, X. and Liu, N.},
  title = {Adversarial YOLO: Defense Human Detection Patch Attacks via Detecting Adversarial Patches},
  journal = {arXiv preprint arXiv:2103.08860},
  year = {2021}
}

@article{xu2020adversarial_tshirt,
  author = {Xu, K. and Zhang, G. and Liu, S. and Fan, Q. and Sun, M. and Chen, H. and Chen, P.Y. and Wang, Y. and Lin, X.},
  title = {Adversarial T-shirt! Evading Person Detectors in A Physical World},
  journal = {arXiv preprint arXiv:1910.11099},
  year = {2020}
}
```

---

## 15. GitHub Repositories

| Repo | Description |
|---|---|
| https://github.com/Bimo99B9/NaturalisticAdversarialPatches | Main repo — GAN-based naturalistic patches for YOLOv5-v10 |
| https://github.com/VDIGPKU/RPAttack | RPAttack — Refined minimal-pixel patch attacks |
| https://github.com/Wu-Shudeng/DPAttack | DPAttack — Diffused patch attacks |

---

*End of Knowledge Repository — Cal State San Marcos Cybersecurity Capstone*
*Total sources reviewed: 30+ papers across Google Scholar, arXiv, GitHub, SSRN, EmergentMind*
