"""
html_to_pptx.py - Export the current 10-slide presentation deck to PowerPoint.

Usage:
    python scripts/html_to_pptx.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


BG = RGBColor(0x0A, 0x0A, 0x0F)
WHITE = RGBColor(0xE8, 0xE8, 0xF0)
DIM = RGBColor(0x88, 0x88, 0x88)
DIMMER = RGBColor(0x44, 0x44, 0x44)
GREEN = RGBColor(0x3E, 0xFF, 0xA0)
YELLOW = RGBColor(0xFF, 0xE0, 0x66)
RED = RGBColor(0xFF, 0x60, 0x60)
BLUE = RGBColor(0x60, 0xB8, 0xFF)
CARD_BG = RGBColor(0x12, 0x12, 0x1A)
CARD_HL = RGBColor(0x0D, 0x1A, 0x12)
CARD_WN = RGBColor(0x1A, 0x0D, 0x0D)
CARD_INF = RGBColor(0x0D, 0x12, 0x20)
CARD_GOLD = RGBColor(0x1A, 0x18, 0x0D)
ROW_ALT = RGBColor(0x12, 0x12, 0x1A)

W = Inches(13.333)
H = Inches(7.5)


def new_prs() -> Presentation:
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    return prs


def blank_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG
    return slide


def rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
    return shape


def textbox(
    slide,
    text,
    left,
    top,
    width,
    height,
    *,
    size=18,
    bold=False,
    color=WHITE,
    align=PP_ALIGN.LEFT,
    italic=False,
):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def rich_textbox(slide, lines, left, top, width, height):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for spec in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = spec.get("align", PP_ALIGN.LEFT)
        run = p.add_run()
        run.text = spec["text"]
        run.font.size = Pt(spec.get("size", 18))
        run.font.bold = spec.get("bold", False)
        run.font.italic = spec.get("italic", False)
        run.font.color.rgb = spec.get("color", WHITE)
    return txb


def rule(slide, left, top, width, color=RGBColor(0x1E, 0x1E, 0x28)):
    rect(slide, left, top, width, Inches(0.02), color)


def tag(slide, text, left=Inches(0.9), top=Inches(0.45)):
    textbox(slide, text, left, top, Inches(4.0), Inches(0.28), size=9, bold=True, color=BLUE)


def title_block(slide, lines, top=Inches(0.85), left=Inches(0.9)):
    rich_textbox(slide, lines, left, top, Inches(11.2), Inches(1.6))


def card_title(slide, text, left, top, width):
    textbox(slide, text, left, top, width, Inches(0.22), size=9, bold=True, color=BLUE)


def bullet_lines(items, color=WHITE, size=12):
    return [{"text": f"- {item}", "size": size, "color": color} for item in items]


def slide1_title(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "CAPSTONE RESEARCH", top=Inches(0.7))
    title_block(
        slide,
        [
            {"text": "Adversarial Robustness", "size": 42, "bold": True, "color": WHITE},
            {"text": "Framework", "size": 42, "bold": True, "color": GREEN},
        ],
        top=Inches(1.2),
    )
    textbox(
        slide,
        "Two complementary tracks for attack analysis and defense-cycle evaluation across YOLO generations",
        Inches(0.9),
        Inches(3.05),
        Inches(9.6),
        Inches(0.8),
        size=16,
        color=DIM,
    )
    rule(slide, Inches(0.9), Inches(4.0), Inches(1.2), RGBColor(0x3E, 0xFF, 0xA0))
    textbox(slide, "April 2026", Inches(0.9), Inches(4.25), Inches(3.0), Inches(0.4), size=13, color=DIMMER)


def slide2_pipeline(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "FRAMEWORK OVERVIEW")
    title_block(
        slide,
        [
            {"text": "Two Complementary", "size": 38, "bold": True, "color": WHITE},
            {"text": "Tracks", "size": 38, "bold": True, "color": BLUE},
        ],
    )

    left = Inches(0.9)
    top = Inches(2.0)
    width = Inches(5.7)
    gap = Inches(0.45)
    right = left + width + gap

    rect(slide, left, top, width, Inches(3.1), CARD_INF)
    card_title(slide, "ATTACK TRACK    Adversarial_Patch", left + Inches(0.2), top + Inches(0.16), width)
    rule(slide, left + Inches(0.2), top + Inches(0.48), width - Inches(0.4))
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Gradient-based patch training against any Ultralytics YOLO model",
                "Multi-model and joint ensemble attack modes",
                "Cross-model transfer evaluation across YOLO generations",
                "Defense robustness benchmarking (JPEG, blur, crop-resize)",
                "Live demo plus 300 DPI physical print export",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
        ),
        left + Inches(0.2),
        top + Inches(0.62),
        width - Inches(0.35),
        Inches(2.3),
    )

    rect(slide, right, top, width, Inches(3.1), CARD_HL)
    card_title(slide, "DEFENSE TRACK    YOLO-Bad-Triangle", right + Inches(0.2), top + Inches(0.16), width)
    rule(slide, right + Inches(0.2), top + Inches(0.48), width - Inches(0.4))
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Plugin-based attack and defense registry",
                "22 recorded automated cycles in the defense repo",
                "DPC-UNet checkpoint finetuning with clean A/B deployment gate",
                "Schema-enforced artifact contracts and provenance tracking",
                "Automated reporting pipeline",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
        ),
        right + Inches(0.2),
        top + Inches(0.62),
        width - Inches(0.35),
        Inches(2.3),
    )

    textbox(
        slide,
        "These are complementary sibling repos, not one shared-image runtime loop: the attack track uses a 48-image common manifest, while the defense track runs automated cycles on a COCO subset and writes its own reports.",
        Inches(0.9),
        Inches(5.45),
        Inches(11.4),
        Inches(0.8),
        size=12,
        color=DIM,
    )


def slide3_results(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "ATTACK TRACK - FINDINGS")
    title_block(
        slide,
        [
            {"text": "Detection", "size": 38, "bold": True, "color": WHITE},
            {"text": "Suppression", "size": 38, "bold": True, "color": GREEN},
        ],
    )

    card_w = Inches(3.6)
    card_h = Inches(3.2)
    y = Inches(2.25)
    gap = Inches(0.4)
    x1 = Inches(0.9)
    x2 = x1 + card_w + gap
    x3 = x2 + card_w + gap

    rect(slide, x1, y, card_w, card_h, CARD_HL)
    textbox(slide, "90%", x1, y + Inches(0.28), card_w, Inches(0.9), size=54, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    textbox(slide, "YOLOv8n", x1, y + Inches(1.22), card_w, Inches(0.35), size=16, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, "20 -> 2 detections", x1, y + Inches(1.62), card_w, Inches(0.28), size=13, color=DIM, align=PP_ALIGN.CENTER)
    textbox(slide, "1000 epochs - loss 0.543", x1, y + Inches(2.02), card_w, Inches(0.25), size=10, color=DIM, align=PP_ALIGN.CENTER)

    rect(slide, x2, y, card_w, card_h, CARD_GOLD)
    textbox(slide, "72.7%", x2, y + Inches(0.28), card_w, Inches(0.9), size=54, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
    textbox(slide, "YOLO11n", x2, y + Inches(1.22), card_w, Inches(0.35), size=16, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, "33 -> 9 detections", x2, y + Inches(1.62), card_w, Inches(0.28), size=13, color=DIM, align=PP_ALIGN.CENTER)
    textbox(slide, "1000 epochs - loss 0.597", x2, y + Inches(2.02), card_w, Inches(0.25), size=10, color=DIM, align=PP_ALIGN.CENTER)

    rect(slide, x3, y, card_w, card_h, CARD_WN)
    textbox(slide, "16.3%", x3, y + Inches(0.28), card_w, Inches(0.9), size=54, bold=True, color=RED, align=PP_ALIGN.CENTER)
    textbox(slide, "YOLO26n", x3, y + Inches(1.22), card_w, Inches(0.35), size=16, bold=True, align=PP_ALIGN.CENTER)
    textbox(slide, "43 -> 36 detections", x3, y + Inches(1.62), card_w, Inches(0.28), size=13, color=DIM, align=PP_ALIGN.CENTER)
    textbox(slide, "1000 epochs - loss 0.108", x3, y + Inches(2.02), card_w, Inches(0.25), size=10, color=DIM, align=PP_ALIGN.CENTER)

    textbox(
        slide,
        "Patch size: 100 x 100 px  |  Image size: 640 x 640  |  2.4% of total pixels",
        Inches(0.9),
        Inches(5.72),
        Inches(11.4),
        Inches(0.3),
        size=13,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )
    textbox(
        slide,
        "Within v26n runs, better objective convergence did not yield better suppression - see The v26n Paradox",
        Inches(0.9),
        Inches(6.02),
        Inches(11.4),
        Inches(0.3),
        size=10,
        color=DIMMER,
    )


def slide4_bad_triangle(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "ATTACK TRACK - TRANSFER ANALYSIS")
    title_block(
        slide,
        [
            {"text": "The", "size": 36, "bold": True, "color": WHITE},
            {"text": "Bad Triangle", "size": 36, "bold": True, "color": BLUE},
        ],
    )

    lx = Inches(0.9)
    rx = Inches(8.15)
    top = Inches(2.0)

    textbox(
        slide,
        "Cross-model suppression matrix  |  row = patch trained on  |  column = model tested against",
        lx,
        top,
        Inches(6.9),
        Inches(0.3),
        size=9,
        bold=True,
        color=BLUE,
    )

    headers = ["Patch source", "-> v8n", "-> v11n", "-> v26n"]
    rows = [
        ["v8n", "90% *", "33.3%", "14.0%"],
        ["v11n", "50.0%", "72.7% *", "9.3%"],
        ["v26n", "45.0%", "24.2%", "16.3% *"],
    ]
    colors = [
        [DIM, GREEN, YELLOW, RED],
        [DIM, YELLOW, GREEN, RED],
        [DIM, YELLOW, YELLOW, RED],
    ]

    col_w = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6)]
    x = [lx, lx + col_w[0], lx + col_w[0] + col_w[1], lx + col_w[0] + col_w[1] + col_w[2]]
    y = top + Inches(0.42)
    row_h = Inches(0.52)
    for i, header in enumerate(headers):
        textbox(slide, header, x[i], y, col_w[i], Inches(0.24), size=9, color=DIM)
    for r, row in enumerate(rows):
        ry = y + Inches(0.34) + r * row_h
        rect(slide, lx - Inches(0.08), ry - Inches(0.04), Inches(6.65), Inches(0.42), ROW_ALT if r % 2 == 0 else BG)
        for c, value in enumerate(row):
            textbox(
                slide,
                value,
                x[c],
                ry,
                col_w[c],
                Inches(0.24),
                size=12,
                bold=c > 0,
                color=colors[r][c],
            )

    textbox(
        slide,
        "* = white-box  |  off-diagonal = black-box transfer",
        lx,
        Inches(4.05),
        Inches(6.9),
        Inches(0.3),
        size=10,
        color=DIM,
    )

    rect(slide, lx, Inches(4.45), Inches(6.9), Inches(1.15), CARD_INF)
    card_title(slide, "JOINT PATCHES", lx + Inches(0.2), Inches(4.6), Inches(6.5))
    textbox(
        slide,
        "v8n+v11n -> v8n  85%   |   v8n+v11n -> v11n  66.7%   |   v8n+v26n -> v26n  18.6% (best v26n result)",
        lx + Inches(0.2),
        Inches(4.95),
        Inches(6.45),
        Inches(0.45),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rect(slide, rx, top + Inches(0.35), Inches(4.25), Inches(1.45), CARD_GOLD)
    card_title(slide, "ASYMMETRY", rx + Inches(0.2), top + Inches(0.5), Inches(3.9))
    textbox(
        slide,
        "v11n -> v8n = 50.0%  >  v8n -> v11n = 33.3%\nThe asymmetry remains in the current v2 artifacts: newer-generation patches still reach backward better than older patches reach forward.",
        rx + Inches(0.2),
        top + Inches(0.82),
        Inches(3.85),
        Inches(1.0),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rect(slide, rx, top + Inches(2.0), Inches(4.25), Inches(2.05), CARD_WN)
    card_title(slide, "THE v26n FIREWALL", rx + Inches(0.2), top + Inches(2.15), Inches(3.9))
    textbox(
        slide,
        "v26n remains the hardest target in this study. Nothing in the direct matrix exceeds 16.3% against it, and even the best joint patch only reaches 18.6%.\nYet the v26n patch still transfers out at 45.0% and 24.2%.",
        rx + Inches(0.2),
        top + Inches(2.47),
        Inches(3.85),
        Inches(1.45),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )


def slide5_preprocessing(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "ATTACK TRACK - DEFENSE BENCHMARK")
    title_block(
        slide,
        [
            {"text": "Preprocessing", "size": 36, "bold": True, "color": WHITE},
            {"text": "Makes It Worse", "size": 36, "bold": True, "color": RED},
        ],
    )

    left = Inches(0.9)
    top = Inches(2.0)
    width = Inches(5.8)
    gap = Inches(0.45)
    right = left + width + gap

    rect(slide, left, top, width, Inches(3.25), CARD_BG)
    card_title(slide, "JPEG COMPRESSION   YOLOv8n patch - 48 images", left + Inches(0.2), top + Inches(0.16), width)
    rich_textbox(
        slide,
        [
            {"text": "Quality        Suppression      vs. undefended", "size": 10, "color": DIM},
            {"text": "none           85%              baseline", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
            {"text": "95             95%              +10 pp", "size": 12, "color": RED},
            {"text": "85             90%              +5 pp", "size": 12, "color": RED},
            {"text": "75             90%              +5 pp", "size": 12, "color": RED},
            {"text": "50             80%              -5 pp (clean -29 pp)", "size": 12, "color": DIM},
        ],
        left + Inches(0.2),
        top + Inches(0.48),
        width - Inches(0.35),
        Inches(1.85),
    )
    rect(slide, left, Inches(5.45), width, Inches(0.9), CARD_BG)
    card_title(slide, "CROP-RESIZE", left + Inches(0.2), Inches(5.58), width)
    textbox(
        slide,
        "High variance across seeds. At 95% and 90% retention there is no reliable benefit. Some 85% retention and isolated 90% retention seeds reduce suppression, but the effect is unstable and often trades off against clean detections.",
        left + Inches(0.2),
        Inches(5.82),
        width - Inches(0.35),
        Inches(0.6),
        size=10,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rect(slide, right, top, width, Inches(3.25), CARD_BG)
    card_title(slide, "GAUSSIAN BLUR", right + Inches(0.2), top + Inches(0.16), width)
    rich_textbox(
        slide,
        [
            {"text": "Sigma          Suppression      vs. undefended", "size": 10, "color": DIM},
            {"text": "none           85%              baseline", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
            {"text": "1.0            90%              +5 pp", "size": 12, "color": RED},
            {"text": "2.0            100%             +15 pp", "size": 12, "color": RED},
            {"text": "3.0            95%              +10 pp", "size": 12, "color": RED},
        ],
        right + Inches(0.2),
        top + Inches(0.48),
        width - Inches(0.35),
        Inches(1.5),
    )
    rect(slide, right, Inches(5.0), width, Inches(1.35), CARD_HL)
    card_title(slide, "WHY", right + Inches(0.2), Inches(5.15), width)
    textbox(
        slide,
        "Adversarial patches concentrate signal in a dense region. Blur and compression suppress helpful clean texture while leaving the patch's dominant structure intact.",
        right + Inches(0.2),
        Inches(5.4),
        width - Inches(0.35),
        Inches(0.7),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )


def slide6_paradox(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "ATTACK TRACK - ARCHITECTURAL FINDING")
    title_block(
        slide,
        [
            {"text": "The", "size": 36, "bold": True, "color": WHITE},
            {"text": "v26n Paradox", "size": 36, "bold": True, "color": RED},
        ],
    )

    lx = Inches(0.9)
    rx = Inches(7.0)
    top = Inches(2.0)
    width = Inches(5.7)

    rect(slide, lx, top, width, Inches(1.55), CARD_WN)
    card_title(slide, "WHAT HAPPENED", lx + Inches(0.2), top + Inches(0.15), width)
    rich_textbox(
        slide,
        [
            {"text": "The optimized objective converged on the scored head.", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
            {"text": "final_det_loss = 0.108 on the one2many path.", "size": 12, "color": RED},
            {"text": "Suppression: only 16.3%.", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
        ],
        lx + Inches(0.2),
        top + Inches(0.48),
        width - Inches(0.35),
        Inches(0.9),
    )

    rect(slide, lx, Inches(3.65), width, Inches(2.35), CARD_INF)
    card_title(slide, "ROOT CAUSE", lx + Inches(0.2), Inches(3.8), width)
    textbox(
        slide,
        "YOLO26n uses end-to-end Hungarian matching (head_end2end: true).",
        lx + Inches(0.2),
        Inches(4.08),
        width - Inches(0.35),
        Inches(0.35),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Training optimizes the one2many auxiliary head",
                "Inference uses the one2one head for final detections",
                "These heads are architecturally separate",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
        ),
        lx + Inches(0.2),
        Inches(4.55),
        width - Inches(0.35),
        Inches(1.0),
    )

    rect(slide, rx, top, width, Inches(2.05), CARD_BG)
    card_title(slide, "THREE EXPERIMENTS - SAME ANSWER", rx + Inches(0.2), top + Inches(0.15), width)
    rich_textbox(
        slide,
        [
            {"text": "Experiment                            Loss      Suppression", "size": 10, "color": DIM},
            {"text": "Cold start - one2many loss           0.108     16.3%", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
            {"text": "Warm start from v8n 90% patch        0.103     14.0%", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
            {"text": "Cold start - one2one loss            0.094     11.6%", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
        ],
        rx + Inches(0.2),
        top + Inches(0.5),
        width - Inches(0.35),
        Inches(1.2),
    )
    textbox(
        slide,
        "Better objective convergence -> less suppression. The relationship is inverted.",
        rx + Inches(0.2),
        top + Inches(1.72),
        width - Inches(0.35),
        Inches(0.25),
        size=10,
        color=DIM,
    )

    rect(slide, rx, Inches(4.2), width, Inches(1.8), CARD_HL)
    card_title(slide, "CONCLUSION", rx + Inches(0.2), Inches(4.35), width)
    textbox(
        slide,
        "YOLO26n shows strong resistance to this attack class in the current setup. The matching architecture decouples the optimized objective from the inference path, so targeting either head in isolation did not break through.",
        rx + Inches(0.2),
        Inches(4.68),
        width - Inches(0.35),
        Inches(1.0),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )


def slide7_arms_race(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "DEFENSE TRACK - FINDINGS")
    title_block(
        slide,
        [
            {"text": "Automated", "size": 38, "bold": True, "color": WHITE},
            {"text": "Arms Race", "size": 38, "bold": True, "color": BLUE},
        ],
    )

    left = Inches(0.9)
    right = Inches(7.15)

    textbox(
        slide,
        "This slide uses the latest canonical cycle from YOLO-Bad-Triangle. The repo records 22 cycles overall, but this snapshot is cycle 22 from the current attack_then_defense series. Latest validated attacks: DeepFool, dispersion reduction, and square. Active defenses: JPEG, median filter, bit-depth reduction, and c_dog.",
        left,
        Inches(2.0),
        Inches(5.8),
        Inches(1.15),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rect(slide, left, Inches(3.1), Inches(5.8), Inches(1.7), CARD_BG)
    rich_textbox(
        slide,
        [
            {"text": "Config                                   mAP50      vs clean", "size": 10, "color": DIM},
            {"text": "Clean baseline                           0.600      -", "size": 12, "color": GREEN},
            {"text": "Worst latest-cycle attack   dispersion_reduction    0.238   -60%", "size": 11, "color": RED},
            {"text": "Best latest-cycle defended config  square + c_dog  0.394   -34%", "size": 11, "color": YELLOW},
        ],
        left + Inches(0.2),
        Inches(3.38),
        Inches(5.4),
        Inches(1.0),
    )

    rect(slide, right, Inches(2.0), Inches(5.25), Inches(2.35), CARD_INF)
    card_title(slide, "ADVERSARIAL FINETUNING", right + Inches(0.2), Inches(2.15), Inches(4.8))
    textbox(
        slide,
        "DPC-UNet denoiser checkpoint finetuned on adversarial image pairs (square x5 oversample + DeepFool + blur + square pairs). Candidate deployed only after clean A/B comparison against the current c_dog checkpoint.",
        right + Inches(0.2),
        Inches(2.48),
        Inches(4.9),
        Inches(1.0),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Clean performance: +0.0025 mAP50 versus previous checkpoint - no regression",
                "Attack resistance: delta within noise - no measurable gain yet",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
            11,
        ),
        right + Inches(0.2),
        Inches(3.5),
        Inches(4.9),
        Inches(0.65),
    )

    rect(slide, right, Inches(4.55), Inches(5.25), Inches(1.45), CARD_HL)
    card_title(slide, "STATE OF PLAY", right + Inches(0.2), Inches(4.6), Inches(4.8))
    textbox(
        slide,
        "No universal defense has emerged. In the current canonical series, c_dog is strongest on square, while median preprocessing is stronger on deepfool. Finetuning is clean-safe but has not yet produced a measurable robustness gain.",
        right + Inches(0.2),
        Inches(4.9),
        Inches(4.9),
        Inches(0.9),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )


def slide8_engineering(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "DEFENSE TRACK - METHODOLOGY")
    title_block(
        slide,
        [
            {"text": "Arms Race", "size": 38, "bold": True, "color": WHITE},
            {"text": "Engineering", "size": 38, "bold": True, "color": BLUE},
        ],
    )

    left = Inches(0.9)
    right = Inches(7.15)

    rect(slide, left, Inches(2.0), Inches(5.8), Inches(4.2), CARD_INF)
    card_title(slide, "4-PHASE AUTOMATION PIPELINE", left + Inches(0.2), Inches(2.15), Inches(5.4))
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Phase 1 - Characterize: smoke-rank candidate attacks",
                "Phase 2 - Matrix: smoke-rank candidate defenses against top attacks",
                "Phase 3 - Tune: coordinate-descent best attack and defense params",
                "Phase 4 - Validate + report: full-dataset mAP50 validation and artifact/report generation",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
            11,
        ),
        left + Inches(0.2),
        Inches(2.55),
        Inches(5.4),
        Inches(2.05),
    )
    textbox(
        slide,
        "Checkpoint promotion is a separate clean A/B step for the c_dog denoiser: deploy only if the candidate does not regress versus the current checkpoint.",
        left + Inches(0.2),
        Inches(4.62),
        Inches(5.4),
        Inches(0.55),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )
    textbox(slide, "22", left + Inches(0.4), Inches(5.35), Inches(1.0), Inches(0.4), size=24, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    textbox(slide, "4", left + Inches(2.15), Inches(5.35), Inches(1.0), Inches(0.4), size=24, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    textbox(slide, "5", left + Inches(3.85), Inches(5.35), Inches(1.0), Inches(0.4), size=24, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
    textbox(slide, "recorded cycles", left + Inches(0.2), Inches(5.73), Inches(1.4), Inches(0.2), size=9, color=DIM, align=PP_ALIGN.CENTER)
    textbox(slide, "active defenses", left + Inches(1.8), Inches(5.73), Inches(1.7), Inches(0.2), size=9, color=DIM, align=PP_ALIGN.CENTER)
    textbox(slide, "canonical post-switch cycles", left + Inches(3.2), Inches(5.73), Inches(2.3), Inches(0.2), size=8, color=DIM, align=PP_ALIGN.CENTER)

    rect(slide, right, Inches(2.0), Inches(5.25), Inches(1.95), CARD_HL)
    card_title(slide, "c_dog - STRONGEST SQUARE DEFENSE IN CYCLE 22", right + Inches(0.2), Inches(2.15), Inches(4.8))
    textbox(
        slide,
        "A DPC-UNet denoiser that preprocesses inputs before YOLO inference. In cycle 22, square + c_dog improves mAP50 from 0.363 to 0.394. It is not the strongest defense on every attack.",
        right + Inches(0.2),
        Inches(2.48),
        Inches(4.9),
        Inches(1.05),
        size=11,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )
    textbox(
        slide,
        "Current snapshot: square attack 0.363 -> square + c_dog 0.394",
        right + Inches(0.2),
        Inches(3.62),
        Inches(4.9),
        Inches(0.3),
        size=11,
        color=YELLOW,
    )

    rect(slide, right, Inches(4.18), Inches(5.25), Inches(2.0), CARD_BG)
    card_title(slide, "ADVERSARIAL FINETUNING", right + Inches(0.2), Inches(4.25), Inches(4.8))
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Architecture: DPC-UNet denoiser checkpoint",
                "Mix: square x5 oversample + DeepFool + blur + square pairs",
                "Gate: deploy only if clean A/B does not regress vs current checkpoint",
                "Result: +0.0025 clean mAP50 vs previous checkpoint - gate passed",
                "Attack resistance: delta within noise - open problem",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
            10,
        ),
        right + Inches(0.2),
        Inches(4.58),
        Inches(4.9),
        Inches(1.45),
    )


def slide9_demo(prs: Presentation, patch_path: Path):
    slide = blank_slide(prs)
    tag(slide, "LIVE DEMONSTRATION")

    left = Inches(0.9)
    right = Inches(8.55)

    textbox(slide, "Live Demo", left, Inches(1.25), Inches(5.5), Inches(0.8), size=40, bold=True, color=GREEN)
    textbox(
        slide,
        "Split-screen: clean YOLO detections on the left, patch digitally overlaid on the right.",
        left,
        Inches(2.2),
        Inches(6.2),
        Inches(0.55),
        size=14,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )
    rule(slide, left, Inches(2.9), Inches(4.2))
    rich_textbox(
        slide,
        bullet_lines(
            [
                "Patch: 100 x 100 px, YOLOv8n",
                "Placed on the torso of the largest detected person",
                "Rolling 30-frame suppression average",
            ],
            RGBColor(0xCC, 0xCC, 0xCC),
            13,
        ),
        left,
        Inches(3.1),
        Inches(6.2),
        Inches(0.95),
    )
    rule(slide, left, Inches(4.18), Inches(4.2))

    rect(slide, left, Inches(4.45), Inches(6.4), Inches(1.6), CARD_WN)
    card_title(slide, "PHYSICAL PRINT", left + Inches(0.2), Inches(4.58), Inches(6.0))
    rich_textbox(
        slide,
        [
            {"text": "Patch exported at 300 DPI, 8 x 8 inches.", "size": 12, "color": YELLOW},
            {"text": "Physical demos underperform digital because printer color shift, lighting, and view angle perturb the patch.", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
            {"text": "NPS loss during training partially compensates.", "size": 12, "color": RGBColor(0xCC, 0xCC, 0xCC)},
        ],
        left + Inches(0.2),
        Inches(4.88),
        Inches(6.0),
        Inches(0.9),
    )

    if patch_path.exists():
        slide.shapes.add_picture(str(patch_path), right, Inches(1.6), Inches(3.0), Inches(3.0))
    rect(slide, right + Inches(0.05), Inches(4.85), Inches(2.9), Inches(0.7), CARD_BG)
    textbox(
        slide,
        "YOLOv8n patch - 90% suppression\n100 x 100 px - shown 2x",
        right + Inches(0.15),
        Inches(5.0),
        Inches(2.7),
        Inches(0.4),
        size=10,
        color=DIM,
        align=PP_ALIGN.CENTER,
    )


def slide10_conclusions(prs: Presentation):
    slide = blank_slide(prs)
    tag(slide, "CONCLUSIONS")
    title_block(
        slide,
        [
            {"text": "What We", "size": 38, "bold": True, "color": WHITE},
            {"text": "Learned", "size": 38, "bold": True, "color": GREEN},
        ],
    )

    card_w = Inches(3.6)
    card_h = Inches(2.7)
    y = Inches(2.35)
    gap = Inches(0.4)
    x1 = Inches(0.9)
    x2 = x1 + card_w + gap
    x3 = x2 + card_w + gap

    rect(slide, x1, y, card_w, card_h, CARD_HL)
    card_title(slide, "FRAMEWORK CONTRIBUTION", x1 + Inches(0.2), y + Inches(0.18), card_w)
    textbox(
        slide,
        "Two complementary repos, not one merged pipeline: Adversarial_Patch reports cross-generation patch training and transfer on YOLOv8n, YOLO11n, and YOLO26n; YOLO-Bad-Triangle reports 22 recorded defense-cycle artifacts, with current canonical trends taken from the post-switch series.",
        x1 + Inches(0.2),
        y + Inches(0.55),
        card_w - Inches(0.3),
        Inches(1.9),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rect(slide, x2, y, card_w, card_h, CARD_INF)
    card_title(slide, "ARCHITECTURE MATTERS", x2 + Inches(0.2), y + Inches(0.18), card_w)
    textbox(
        slide,
        "YOLO26n's end-to-end matching breaks the usual assumption that optimizing the attack objective will directly reduce detections.",
        x2 + Inches(0.2),
        y + Inches(0.55),
        card_w - Inches(0.3),
        Inches(1.9),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rect(slide, x3, y, card_w, card_h, CARD_GOLD)
    card_title(slide, "OPEN QUESTIONS", x3 + Inches(0.2), y + Inches(0.18), card_w)
    textbox(
        slide,
        "Does the NMS-free shift require a new attack class, or can DETR-style matching-aware attacks port into YOLO26n? Physical robustness at scale remains open.",
        x3 + Inches(0.2),
        y + Inches(0.55),
        card_w - Inches(0.3),
        Inches(1.9),
        size=12,
        color=RGBColor(0xCC, 0xCC, 0xCC),
    )

    rule(slide, Inches(0.9), Inches(5.65), Inches(11.5))
    textbox(
        slide,
        "Attack repo -> github.com/Cmaddock99/Patch_Yolo\nDefense repo -> github.com/Cmaddock99/YOLO-Bad-Triangle",
        Inches(0.9),
        Inches(5.95),
        Inches(11.5),
        Inches(0.6),
        size=11,
        color=BLUE,
    )


def main():
    root = Path(__file__).parent.parent
    patch_path = root / "outputs" / "yolov8n_patch_v2" / "patches" / "patch.png"
    out_path = root / "presentation.pptx"

    prs = new_prs()
    slide1_title(prs)
    slide2_pipeline(prs)
    slide3_results(prs)
    slide4_bad_triangle(prs)
    slide5_preprocessing(prs)
    slide6_paradox(prs)
    slide7_arms_race(prs)
    slide8_engineering(prs)
    slide9_demo(prs, patch_path)
    slide10_conclusions(prs)
    prs.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
