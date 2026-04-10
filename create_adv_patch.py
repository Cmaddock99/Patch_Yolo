#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import cv2
import matplotlib
import numpy as np
import torch
import yolov5
from PIL import Image
from art.attacks.evasion import DPatch
from art.estimators.object_detection.pytorch_yolo import PyTorchYolo
from yolov5.utils.loss import ComputeLoss

matplotlib.use("Agg")

COCO_LABELS = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".webp"}


@dataclass(frozen=True)
class AttackConfig:
    threshold: float
    target_class: str
    victim_class: str
    batch_size: int
    iou_threshold: float
    max_iter: int
    target_location: tuple[int, int]
    target_shape: tuple[int, int, int]
    images_to_display: int
    folder_name: str

    @classmethod
    def from_file(cls, path: Path) -> "AttackConfig":
        raw = json.loads(path.read_text(encoding="utf-8"))

        target_location = tuple(int(value) for value in raw["TARGET_LOCATION"])
        if len(target_location) != 2:
            raise ValueError("TARGET_LOCATION must contain exactly two integers: [top, left].")

        target_shape = normalize_patch_shape(tuple(int(value) for value in raw["TARGET_SHAPE"]))

        return cls(
            threshold=float(raw["THRESHOLD"]),
            target_class=str(raw.get("TARGET_CLASS", "")).strip(),
            victim_class=str(raw["VICTIM_CLASS"]).strip(),
            batch_size=max(1, int(raw["BATCH_SIZE"])),
            iou_threshold=float(raw["IOU_THRESHOLD"]),
            max_iter=max(1, int(raw["MAX_ITER"])),
            target_location=target_location,
            target_shape=target_shape,
            images_to_display=max(1, int(raw["IMAGES_TO_DISPLAY"])),
            folder_name=str(raw["FOLDER_NAME"]).strip() or "adv_patch_run",
        )


def normalize_patch_shape(shape: Sequence[int]) -> tuple[int, int, int]:
    if len(shape) != 3:
        raise ValueError("TARGET_SHAPE must contain exactly three integers.")

    if shape[0] in (1, 3, 4):
        return int(shape[0]), int(shape[1]), int(shape[2])

    if shape[2] in (1, 3, 4):
        return int(shape[2]), int(shape[0]), int(shape[1])

    raise ValueError("TARGET_SHAPE must be CHW or HWC with 1, 3, or 4 channels.")


def resolve_class_id(class_name: str) -> int | None:
    normalized = class_name.strip().lower()
    if not normalized:
        return None

    lookup = {label.lower(): index for index, label in enumerate(COCO_LABELS)}
    try:
        return lookup[normalized]
    except KeyError as exc:
        raise ValueError(
            f"Unknown COCO class '{class_name}'. Use one of: {', '.join(COCO_LABELS)}"
        ) from exc


class YoloV5ARTWrapper(torch.nn.Module):
    def __init__(self, model: torch.nn.Module):
        super().__init__()
        self.model = model

        try:
            self.loss_model = self.model.model.model
        except AttributeError as exc:
            raise ValueError(
                "Unsupported yolov5 model layout. This script expects the `yolov5` pip package "
                "used in ART's official examples."
            ) from exc

        hyp = {
            "box": 0.05,
            "obj": 1.0,
            "cls": 0.5,
            "anchor_t": 4.0,
            "cls_pw": 1.0,
            "obj_pw": 1.0,
            "fl_gamma": 0.0,
        }
        self.model.hyp = hyp
        self.loss_model.hyp = hyp
        self.compute_loss = ComputeLoss(self.loss_model)

    def forward(self, x: torch.Tensor, targets: torch.Tensor | None = None):
        if self.training:
            outputs = self.loss_model(x)
            loss, _ = self.compute_loss(outputs, targets)
            return {"loss_total": loss}

        return self.model(x)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and apply an adversarial patch against YOLOv5 with ART.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("data/configs/adv_patch_default_config.json"),
        help="Path to the JSON configuration file.",
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=Path("data/custom_images"),
        help="Folder containing unlabeled training images.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Root folder for generated patches and visualizations.",
    )
    parser.add_argument(
        "--weights",
        default="yolov5s.pt",
        help="YOLOv5 weights to load through the `yolov5` package.",
    )
    parser.add_argument(
        "--image-size",
        type=int,
        default=640,
        help="Square size used to resize every input image.",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=5.0,
        help="Learning rate passed to ART's DPatch attack.",
    )
    return parser.parse_args()


def load_images(images_dir: Path, image_size: int) -> tuple[np.ndarray, list[Path]]:
    image_paths = sorted(
        path for path in images_dir.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not image_paths:
        raise ValueError(f"No images found in {images_dir}. Add JPG or PNG files and try again.")

    images = []
    for image_path in image_paths:
        image = Image.open(image_path).convert("RGB").resize((image_size, image_size))
        images.append(np.asarray(image, dtype=np.float32))

    return np.stack(images, axis=0), image_paths


def build_detector(config: AttackConfig, weights: str, image_size: int) -> PyTorchYolo:
    raw_model = load_yolov5_model(weights)
    if hasattr(raw_model, "conf"):
        raw_model.conf = config.threshold
    if hasattr(raw_model, "iou"):
        raw_model.iou = config.iou_threshold

    model = YoloV5ARTWrapper(raw_model)
    return PyTorchYolo(
        model=model,
        device_type="cpu",
        input_shape=(3, image_size, image_size),
        clip_values=(0, 255),
        attack_losses=("loss_total",),
    )


def load_yolov5_model(weights: str) -> torch.nn.Module:
    original_torch_load = torch.load

    def compatible_torch_load(*args, **kwargs):
        kwargs.setdefault("weights_only", False)
        return original_torch_load(*args, **kwargs)

    # The current yolov5 wheel still expects the pre-PyTorch-2.6 torch.load default.
    torch.load = compatible_torch_load
    try:
        return yolov5.load(weights)
    finally:
        torch.load = original_torch_load


def predict_images(detector: PyTorchYolo, images_chw: np.ndarray, batch_size: int) -> list[dict[str, np.ndarray]]:
    predictions: list[dict[str, np.ndarray]] = []
    for start in range(0, images_chw.shape[0], batch_size):
        batch = images_chw[start : start + batch_size]
        try:
            batch_predictions = detector.predict(x=batch, standardise_output=True)
        except TypeError:
            batch_predictions = detector.predict(x=batch)
        predictions.extend(batch_predictions)
    return predictions


def filter_prediction(prediction: dict[str, np.ndarray], score_threshold: float) -> dict[str, np.ndarray]:
    boxes = np.asarray(prediction["boxes"], dtype=np.float32)
    labels = np.asarray(prediction["labels"], dtype=np.int64)
    scores = np.asarray(prediction["scores"], dtype=np.float32)
    keep = scores >= score_threshold
    return {
        "boxes": boxes[keep],
        "labels": labels[keep],
        "scores": scores[keep],
    }


def select_training_subset(
    images_nhwc: np.ndarray,
    image_paths: list[Path],
    predictions: list[dict[str, np.ndarray]],
    victim_class_id: int,
    score_threshold: float,
) -> tuple[np.ndarray, list[Path], list[dict[str, np.ndarray]]]:
    selected_indices = []
    selected_predictions = []

    for index, prediction in enumerate(predictions):
        filtered = filter_prediction(prediction, score_threshold)
        if np.any(filtered["labels"] == victim_class_id):
            selected_indices.append(index)
            selected_predictions.append(filtered)

    if not selected_indices:
        victim_name = COCO_LABELS[victim_class_id]
        raise ValueError(
            f"No images in the dataset produced a '{victim_name}' detection above the {score_threshold:.2f} threshold."
        )

    selected_images = images_nhwc[selected_indices]
    selected_paths = [image_paths[index] for index in selected_indices]
    return selected_images, selected_paths, selected_predictions


def build_location_mask(
    image_height: int,
    image_width: int,
    patch_shape: tuple[int, int, int],
    target_location: tuple[int, int],
) -> np.ndarray:
    patch_height = patch_shape[1]
    patch_width = patch_shape[2]
    top = int(target_location[0])
    left = int(target_location[1])

    if top < 0 or left < 0:
        raise ValueError("TARGET_LOCATION must be non-negative.")
    if top + patch_height > image_height or left + patch_width > image_width:
        raise ValueError("Patch would fall outside the resized image. Adjust TARGET_LOCATION or TARGET_SHAPE.")

    center_row = top + patch_height // 2
    center_col = left + patch_width // 2

    mask = np.zeros((1, image_height, image_width), dtype=bool)
    mask[0, center_row, center_col] = True
    return mask


def draw_prediction_boxes(
    image_nhwc: np.ndarray,
    prediction: dict[str, np.ndarray],
    score_threshold: float,
) -> np.ndarray:
    canvas = np.clip(image_nhwc.copy(), 0, 255).astype(np.uint8)
    filtered = filter_prediction(prediction, score_threshold)

    for box, label, score in zip(filtered["boxes"], filtered["labels"], filtered["scores"]):
        x1, y1, x2, y2 = (int(round(value)) for value in box)
        cv2.rectangle(canvas, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

        label_index = int(label)
        label_name = COCO_LABELS[label_index] if 0 <= label_index < len(COCO_LABELS) else str(label_index)
        text = f"{label_name}: {score:.2f}"
        text_origin = (x1, max(18, y1 - 6))
        cv2.putText(canvas, text, text_origin, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    return canvas


def save_rgb_image(image_hwc: np.ndarray, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(image_hwc, 0, 255).astype(np.uint8)).save(destination)


def save_patch_image(patch: np.ndarray, destination: Path) -> None:
    if patch.ndim != 3:
        raise ValueError("Patch array must be 3-dimensional.")

    if patch.shape[0] in (1, 3, 4):
        patch_hwc = np.transpose(patch, (1, 2, 0))
    else:
        patch_hwc = patch

    save_rgb_image(patch_hwc, destination)


def save_prediction_samples(
    images_nhwc: np.ndarray,
    image_paths: list[Path],
    predictions: list[dict[str, np.ndarray]],
    output_dir: Path,
    score_threshold: float,
    limit: int,
    prefix: str,
) -> None:
    for index, (image, image_path, prediction) in enumerate(zip(images_nhwc[:limit], image_paths[:limit], predictions[:limit])):
        rendered = draw_prediction_boxes(image, prediction, score_threshold)
        destination = output_dir / f"{prefix}_{index:02d}_{image_path.stem}.png"
        save_rgb_image(rendered, destination)


def to_chw(images_nhwc: np.ndarray) -> np.ndarray:
    return np.transpose(images_nhwc, (0, 3, 1, 2)).astype(np.float32)


def main() -> None:
    args = parse_args()
    config = AttackConfig.from_file(args.config)

    victim_class_id = resolve_class_id(config.victim_class)
    if victim_class_id is None:
        raise ValueError("VICTIM_CLASS must be a valid COCO class name.")

    target_class_id = resolve_class_id(config.target_class)

    run_dir = args.output_dir / config.folder_name
    original_dir = run_dir / "original"
    patched_dir = run_dir / "patched"
    patch_dir = run_dir / "patches"
    for directory in (original_dir, patched_dir, patch_dir):
        directory.mkdir(parents=True, exist_ok=True)

    images_nhwc, image_paths = load_images(args.images_dir, args.image_size)
    detector = build_detector(config, args.weights, args.image_size)

    original_predictions = predict_images(detector, to_chw(images_nhwc), batch_size=config.batch_size)
    training_images, training_paths, training_predictions = select_training_subset(
        images_nhwc=images_nhwc,
        image_paths=image_paths,
        predictions=original_predictions,
        victim_class_id=victim_class_id,
        score_threshold=config.threshold,
    )
    training_images_chw = to_chw(training_images)

    save_prediction_samples(
        images_nhwc=training_images,
        image_paths=training_paths,
        predictions=training_predictions,
        output_dir=original_dir,
        score_threshold=config.threshold,
        limit=min(config.images_to_display, len(training_images)),
        prefix=f"detection_{config.folder_name}",
    )

    mask = build_location_mask(
        image_height=training_images.shape[1],
        image_width=training_images.shape[2],
        patch_shape=config.target_shape,
        target_location=config.target_location,
    )

    attack = DPatch(
        estimator=detector,
        patch_shape=config.target_shape,
        learning_rate=float(args.learning_rate),
        max_iter=config.max_iter,
        batch_size=min(config.batch_size, len(training_images)),
        verbose=True,
    )

    if target_class_id is None:
        patch = attack.generate(x=training_images_chw, y=training_predictions, mask=mask)
    else:
        patch = attack.generate(x=training_images_chw, y=None, target_label=target_class_id, mask=mask)

    patch_path = patch_dir / "patch.png"
    save_patch_image(patch, patch_path)

    adversarial_images_chw = attack.apply_patch(
        x=training_images_chw,
        patch_external=patch,
        random_location=True,
        mask=mask,
    )
    adversarial_images = np.transpose(adversarial_images_chw, (0, 2, 3, 1))
    attack_predictions = predict_images(
        detector,
        adversarial_images_chw,
        batch_size=min(config.batch_size, len(training_images)),
    )

    save_prediction_samples(
        images_nhwc=adversarial_images,
        image_paths=training_paths,
        predictions=attack_predictions,
        output_dir=patched_dir,
        score_threshold=config.threshold,
        limit=min(config.images_to_display, len(adversarial_images)),
        prefix="patched",
    )

    target_mode = "untargeted" if target_class_id is None else f"targeted ({config.target_class})"
    print(f"Loaded {len(images_nhwc)} image(s) from {args.images_dir}.")
    print(
        f"Selected {len(training_images)} image(s) containing '{config.victim_class}' above "
        f"the {config.threshold:.2f} threshold."
    )
    print(f"Patch training mode: {target_mode}.")
    print(f"Saved patch to: {patch_path}")
    print(f"Saved clean detections to: {original_dir}")
    print(f"Saved patched detections to: {patched_dir}")


if __name__ == "__main__":
    main()
