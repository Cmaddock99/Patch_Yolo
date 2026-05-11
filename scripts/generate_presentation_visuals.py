"""
Generate reusable adversarial-patch visuals for the presentation deck.

These assets are derived from committed local artifacts so the deck can use
the same imagery in both the HTML view and the PowerPoint export.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets" / "presentation"

PATCH_PATH = ROOT / "outputs" / "yolov8n_patch_v2" / "patches" / "patch.png"
PATCH_PRINT_PATH = ROOT / "outputs" / "yolov8n_patch_v2" / "patches" / "patch_print_300dpi.png"
CLEAN_PATH = ROOT / "outputs" / "yolov8n_patch_v1" / "original" / "clean_01_IMG_20260410_114610856_HDR.png"
PATCHED_PATH = ROOT / "outputs" / "yolov8n_patch_v1" / "patched" / "patched_01_IMG_20260410_114610856_HDR.png"

BG = "#0a0a0f"
CARD = "#12121a"
CARD_INFO = "#0d1220"
CARD_WARN = "#1a0d0d"
CARD_HL = "#0d1a12"
STROKE = "#232334"
WHITE = "#e8e8f0"
MUTED = "#aeb3c2"
DIM = "#6f7484"
GREEN = "#3effa0"
YELLOW = "#ffe066"
RED = "#ff6060"
BLUE = "#60b8ff"
ORANGE = "#ff9560"

TRANSFER = [
    [90.0, 33.3, 14.0],
    [55.0, 72.7, 9.3],
    [45.0, 24.2, 16.3],
]

PARADOX_ROWS = [
    ("Direct one2many", 0.108, 16.3),
    ("Warm start from v8n", 0.103, 14.0),
    ("one2one objective", 0.094, 11.6),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def canvas(width: int, height: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), BG)
    return image, ImageDraw.Draw(image)


def rounded(draw: ImageDraw.ImageDraw, box, fill, outline=STROKE, radius=28, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def fit_contain(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height))
    return copy


def paste_center(base: Image.Image, child: Image.Image, left: int, top: int, width: int, height: int):
    x = left + (width - child.width) // 2
    y = top + (height - child.height) // 2
    base.paste(child, (x, y))


def add_label(
    draw: ImageDraw.ImageDraw,
    text: str,
    left: int,
    top: int,
    *,
    text_color=WHITE,
    fill=CARD_INFO,
    size=24,
):
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font(size, bold=True))
    width = (x1 - x0) + 34
    height = (y1 - y0) + 18
    rounded(draw, (left, top, left + width, top + height), fill=fill, outline=None, radius=18, width=0)
    draw.text((left + 17, top + 8), text, font=font(size, bold=True), fill=text_color)


def heat_color(value: float) -> str:
    if value >= 70:
        return "#123625"
    if value >= 45:
        return "#2a3415"
    if value >= 25:
        return "#3b2611"
    return "#391519"


def save_transfer_heatmap():
    image, draw = canvas(1600, 900)
    draw.text((90, 70), "Cross-model transfer heatmap", font=font(54, bold=True), fill=WHITE)
    draw.text(
        (90, 145),
        "Rows = patch source | Columns = evaluation model | Diagonal = white-box",
        font=font(26),
        fill=MUTED,
    )

    grid_left = 270
    grid_top = 220
    cell = 185
    gap = 14
    models = ["YOLOv8n", "YOLO11n", "YOLO26n"]
    short = ["v8n", "v11n", "v26n"]

    for index, label in enumerate(models):
        x = grid_left + index * (cell + gap)
        draw.text((x + 28, 178), label, font=font(28, bold=True), fill=BLUE)
        draw.text((100, grid_top + index * (cell + gap) + 70), short[index], font=font(30, bold=True), fill=BLUE)

    add_label(draw, "Patch source", 90, 228, fill=CARD_INFO, size=20)
    add_label(draw, "Eval model", 625, 106, fill=CARD_INFO, size=20)

    for row_idx, row in enumerate(TRANSFER):
        for col_idx, value in enumerate(row):
            left = grid_left + col_idx * (cell + gap)
            top = grid_top + row_idx * (cell + gap)
            rounded(draw, (left, top, left + cell, top + cell), fill=heat_color(value), radius=28)
            border = GREEN if row_idx == col_idx else STROKE
            draw.rounded_rectangle((left, top, left + cell, top + cell), radius=28, outline=border, width=4)
            if row_idx == col_idx:
                add_label(draw, "white-box", left + 28, top + 22, fill=CARD_HL, text_color=GREEN, size=16)
            pct = f"{value:.1f}%"
            tx = draw.textbbox((0, 0), pct, font=font(52, bold=True))
            tw = tx[2] - tx[0]
            th = tx[3] - tx[1]
            draw.text((left + (cell - tw) / 2, top + 80 - th / 2), pct, font=font(52, bold=True), fill=WHITE)

    image.save(ASSET_DIR / "transfer_heatmap.png")


def save_method_pipeline():
    image, draw = canvas(1600, 220)

    steps = [
        ("1", "Train patch", "Optimize the 100x100 artifact."),
        ("2", "Overlay on torso", "Place the patch on the torso region."),
        ("3", "Run YOLO", "Measure clean and patched outputs."),
        ("4", "Compare outcomes", "Count person boxes and confidence."),
        ("5", "Benchmark", "Test transfer and defenses."),
    ]

    patch_thumb = fit_contain(Image.open(PATCH_PATH).convert("RGB"), 84, 84)
    start_x = 54
    top = 24
    box_w = 268
    box_h = 144
    gap = 14
    for idx, (num, title, body) in enumerate(steps):
        left = start_x + idx * (box_w + gap)
        fill = CARD_INFO if idx in {0, 2, 4} else CARD
        rounded(draw, (left, top, left + box_w, top + box_h), fill=fill, radius=24)
        add_label(draw, num, left + 18, top + 16, fill=CARD_WARN if idx == 1 else CARD_HL, text_color=WHITE, size=18)
        if idx == 0:
            image.paste(patch_thumb, (left + box_w - 108, top + 20))
        draw.text((left + 18, top + 52), title, font=font(26, bold=True), fill=WHITE)
        draw.multiline_text((left + 18, top + 100), body, font=font(15), fill=MUTED, spacing=4)
        if idx < len(steps) - 1:
            arrow_y = top + box_h // 2
            arrow_x = left + box_w + 6
            draw.line((arrow_x, arrow_y, arrow_x + gap - 12, arrow_y), fill=BLUE, width=6)
            draw.polygon(
                [(arrow_x + gap - 12, arrow_y - 11), (arrow_x + gap - 12, arrow_y + 11), (arrow_x + gap + 4, arrow_y)],
                fill=BLUE,
            )
    image.save(ASSET_DIR / "method_pipeline.png")


def save_paradox_visual():
    image, draw = canvas(1600, 900)
    draw.text((90, 70), "YOLO26n paradox", font=font(54, bold=True), fill=WHITE)
    draw.text((90, 145), "Lower final loss did not translate into stronger person suppression.", font=font(28), fill=MUTED)

    card_w = 430
    card_h = 460
    top = 250
    lefts = [90, 585, 1080]
    for idx, (name, loss, suppression) in enumerate(PARADOX_ROWS):
        fill = CARD_WARN if idx == 2 else CARD
        rounded(draw, (lefts[idx], top, lefts[idx] + card_w, top + card_h), fill=fill, radius=28)
        draw.text((lefts[idx] + 28, top + 28), name, font=font(28, bold=True), fill=BLUE if idx == 0 else WHITE)
        draw.text((lefts[idx] + 28, top + 90), "Final loss", font=font(20, bold=True), fill=MUTED)
        rounded(draw, (lefts[idx] + 28, top + 122, lefts[idx] + card_w - 28, top + 196), fill=CARD_INFO, radius=24)
        draw.text((lefts[idx] + 46, top + 141), f"{loss:.3f}", font=font(44, bold=True), fill=BLUE)
        draw.text((lefts[idx] + 220, top + 153), "lower is better", font=font(20), fill=MUTED)

        draw.text((lefts[idx] + 28, top + 238), "Suppression", font=font(20, bold=True), fill=MUTED)
        rounded(draw, (lefts[idx] + 28, top + 270, lefts[idx] + card_w - 28, top + 360), fill=CARD_HL, radius=24)
        draw.text((lefts[idx] + 46, top + 293), f"{suppression:.1f}%", font=font(48, bold=True), fill=RED if suppression < 15 else YELLOW)
        bar_left = lefts[idx] + 200
        bar_top = top + 305
        bar_w = 160
        draw.rounded_rectangle((bar_left, bar_top, bar_left + bar_w, bar_top + 26), radius=13, fill="#231a1a")
        filled = int(bar_w * (suppression / 20.0))
        draw.rounded_rectangle((bar_left, bar_top, bar_left + filled, bar_top + 26), radius=13, fill=RED if suppression < 15 else ORANGE)
        draw.text((lefts[idx] + 28, top + 392), "Attack stayed weak even as the objective improved.", font=font(18), fill=MUTED)

    rounded(draw, (90, 760, 1510, 840), fill=CARD_INFO, radius=24)
    draw.text((124, 785), "Takeaway:", font=font(24, bold=True), fill=BLUE)
    draw.text(
        (260, 785),
        "The barrier is architectural. YOLO26n likely needs a matching-aware attack formulation, not just more optimization.",
        font=font(24),
        fill=MUTED,
    )
    image.save(ASSET_DIR / "yolo26n_paradox.png")


def save_proof_pair():
    image, draw = canvas(1600, 900)
    clean = Image.open(CLEAN_PATH).convert("RGB")
    patched = Image.open(PATCHED_PATH).convert("RGB")

    draw.text((90, 60), "Proof pair: same frame, different outcome", font=font(50, bold=True), fill=WHITE)
    draw.text((90, 128), "The patch is placed on the torso; the clean person box disappears in the patched frame.", font=font(24), fill=MUTED)

    panels = [
        (90, 210, 650, 620, "Clean detections", "Baseline frame: person box still present.", GREEN, clean),
        (860, 210, 650, 620, "Patch applied", "Patched frame: same scene with the optimized torso patch.", YELLOW, patched),
    ]
    for left, top, width, height, label, caption, accent, src in panels:
        rounded(draw, (left, top, left + width, top + height), fill=CARD, radius=30)
        add_label(draw, label, left + 24, top + 22, fill=CARD_INFO, text_color=accent, size=24)
        inner = fit_contain(src, width - 50, height - 120)
        paste_center(image, inner, left + 25, top + 82, width - 50, height - 130)
        draw.text((left + 24, top + height - 36), caption, font=font(20), fill=MUTED)

    draw.line((740, 510, 840, 510), fill=BLUE, width=8)
    draw.polygon([(840, 510), (805, 490), (805, 530)], fill=BLUE)
    add_label(draw, "same person | same camera | same frame", 542, 560, fill=CARD_HL, text_color=WHITE, size=20)
    image.save(ASSET_DIR / "yolov8n_proof_pair.png")


def save_print_inset():
    source = Image.open(PATCH_PRINT_PATH).convert("RGB")
    image, draw = canvas(760, 520)
    rounded(draw, (0, 0, 759, 519), fill=CARD, radius=26)
    inner = fit_contain(source, 680, 400)
    paste_center(image, inner, 40, 40, 680, 400)
    add_label(draw, "300 DPI printable artifact", 40, 448, fill=CARD_WARN, text_color=YELLOW, size=18)
    image.save(ASSET_DIR / "patch_print_inset.png")


def main():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    save_transfer_heatmap()
    save_method_pipeline()
    save_paradox_visual()
    save_proof_pair()
    save_print_inset()
    print(f"Saved presentation assets to {ASSET_DIR}")


if __name__ == "__main__":
    main()
