"""
html_to_pptx.py — Convert presentation.html to presentation.pptx

Usage:
    python scripts/html_to_pptx.py
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# ---------------------------------------------------------------------------
# Colour palette (matches the HTML)
# ---------------------------------------------------------------------------
BG       = RGBColor(0x0a, 0x0a, 0x0f)
WHITE    = RGBColor(0xe8, 0xe8, 0xf0)
DIM      = RGBColor(0x88, 0x88, 0x88)
DIMMER   = RGBColor(0x44, 0x44, 0x44)
GREEN    = RGBColor(0x3e, 0xff, 0xa0)
YELLOW   = RGBColor(0xff, 0xe0, 0x66)
RED      = RGBColor(0xff, 0x60, 0x60)
BLUE     = RGBColor(0x60, 0xb8, 0xff)
CARD_BG  = RGBColor(0x12, 0x12, 0x1a)
CARD_HL  = RGBColor(0x0d, 0x1a, 0x12)
CARD_WN  = RGBColor(0x1a, 0x0d, 0x0d)
CARD_INF = RGBColor(0x0d, 0x12, 0x20)

# ---------------------------------------------------------------------------
# Slide dimensions (16:9 widescreen)
# ---------------------------------------------------------------------------
W = Inches(13.333)
H = Inches(7.5)


def new_prs() -> Presentation:
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs


def blank_slide(prs: Presentation):
    layout = prs.slide_layouts[6]   # completely blank
    slide = prs.slides.add_slide(layout)
    # Dark background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG
    return slide


def add_textbox(slide, text, left, top, width, height,
                size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
                italic=False, wrap=True):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size    = Pt(size)
    run.font.bold    = bold
    run.font.italic  = italic
    run.font.color.rgb = color
    return txb


def add_rich_textbox(slide, lines, left, top, width, height, wrap=True):
    """
    lines: list of dicts with keys:
      text, size, bold, color, align, space_before (pts)
    """
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf  = txb.text_frame
    tf.word_wrap = wrap
    first = True
    for spec in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = spec.get("align", PP_ALIGN.LEFT)
        if "space_before" in spec:
            p.space_before = Pt(spec["space_before"])
        run = p.add_run()
        run.text = spec["text"]
        run.font.size  = Pt(spec.get("size", 18))
        run.font.bold  = spec.get("bold", False)
        run.font.color.rgb = spec.get("color", WHITE)
    return txb


def add_filled_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
        shape.line.fill.background()
    return shape


def tag_label(slide, text, left, top):
    """Small uppercase blue label."""
    add_textbox(slide, text, left, top, Inches(4), Inches(0.35),
                size=9, bold=True, color=BLUE)


# ---------------------------------------------------------------------------
# Slide builders
# ---------------------------------------------------------------------------

def slide1_title(prs):
    slide = blank_slide(prs)
    tag_label(slide, "CAPSTONE RESEARCH", Inches(0.9), Inches(0.7))

    add_rich_textbox(slide, [
        {"text": "Adversarial Patch", "size": 44, "bold": True, "color": WHITE},
        {"text": "Attacks on YOLO",   "size": 44, "bold": True, "color": GREEN, "space_before": 2},
    ], Inches(0.9), Inches(1.2), Inches(9), Inches(2.0))

    add_textbox(slide,
        "Gradient-based person detection suppression across YOLOv8n, YOLO11n, and YOLO26n",
        Inches(0.9), Inches(3.0), Inches(9), Inches(0.8),
        size=16, color=DIM)

    add_textbox(slide, "April 2026",
        Inches(0.9), Inches(4.2), Inches(4), Inches(0.5),
        size=13, color=DIMMER)


def slide2_what_is(prs):
    slide = blank_slide(prs)
    tag_label(slide, "BACKGROUND", Inches(0.9), Inches(0.4))

    add_rich_textbox(slide, [
        {"text": "What Is an", "size": 36, "bold": True, "color": WHITE},
        {"text": "Adversarial Patch?", "size": 36, "bold": True, "color": BLUE, "space_before": 2},
    ], Inches(0.9), Inches(0.85), Inches(11), Inches(1.6))

    # Left column
    lx = Inches(0.9)
    rx = Inches(6.8)
    cy = Inches(2.4)
    cw = Inches(5.5)

    add_textbox(slide, "THE IDEA", lx, cy, cw, Inches(0.3), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "A small image region, optimized through gradient descent, that causes a neural "
        "network to stop detecting objects — even when the object is fully visible.",
        lx, Inches(2.75), cw, Inches(1.0), size=13, color=RGBColor(0xcc,0xcc,0xcc))

    add_textbox(slide, "HOW IT'S DIFFERENT FROM OCCLUSION", lx, Inches(3.85), cw, Inches(0.3),
                size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "Covering a face with any object reduces features. An adversarial patch exploits "
        "the model's internal representations — creating activation patterns the detector "
        "interprets as 'no person.'",
        lx, Inches(4.2), cw, Inches(1.1), size=13, color=RGBColor(0xcc,0xcc,0xcc))

    # Right column — card 1
    add_filled_rect(slide, rx, cy, cw, Inches(1.85), CARD_INF)
    add_textbox(slide, "TRAINING LOOP", rx + Inches(0.2), cy + Inches(0.15), cw - Inches(0.4), Inches(0.3),
                size=9, bold=True, color=BLUE)
    add_rich_textbox(slide, [
        {"text": "• Freeze model weights",                     "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Overlay patch on person's torso",          "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Forward pass → detection confidence",       "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Backpropagate to patch pixels only",        "size": 12, "color": GREEN},
        {"text": "• Repeat until detections suppress",          "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
    ], rx + Inches(0.2), cy + Inches(0.5), cw - Inches(0.3), Inches(1.2))

    # Right column — card 2
    add_filled_rect(slide, rx, Inches(4.4), cw, Inches(1.6), CARD_BG)
    add_textbox(slide, "ROBUSTNESS AUGMENTATIONS", rx + Inches(0.2), Inches(4.55), cw, Inches(0.3),
                size=9, bold=True, color=BLUE)
    add_rich_textbox(slide, [
        {"text": "• Random rotation ±15°",          "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Cutout masking (T-SEA)",         "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Block erasing (DePatch)",        "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Non-Printability Score loss",    "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
    ], rx + Inches(0.2), Inches(4.9), cw - Inches(0.3), Inches(1.0))


def slide3_results(prs):
    slide = blank_slide(prs)
    tag_label(slide, "RESULTS", Inches(0.9), Inches(0.4))

    add_rich_textbox(slide, [
        {"text": "Detection", "size": 38, "bold": True, "color": WHITE},
        {"text": "Suppression", "size": 38, "bold": True, "color": GREEN, "space_before": 2},
    ], Inches(0.9), Inches(0.85), Inches(11), Inches(1.6))

    # Three stat cards
    card_w = Inches(3.6)
    card_h = Inches(3.2)
    card_y = Inches(2.5)
    gap    = Inches(0.4)
    x1 = Inches(0.9)
    x2 = x1 + card_w + gap
    x3 = x2 + card_w + gap

    # v8n — green
    add_filled_rect(slide, x1, card_y, card_w, card_h, CARD_HL)
    add_textbox(slide, "90%",   x1, card_y + Inches(0.3),  card_w, Inches(0.9), size=54, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    add_textbox(slide, "YOLOv8n", x1, card_y + Inches(1.25), card_w, Inches(0.4), size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide, "20 → 2 detections", x1, card_y + Inches(1.65), card_w, Inches(0.35), size=13, color=DIM, align=PP_ALIGN.CENTER)
    add_textbox(slide, "1000 epochs · loss 0.543", x1, card_y + Inches(2.05), card_w, Inches(0.3), size=10, color=DIM, align=PP_ALIGN.CENTER)

    # v11n — yellow
    add_filled_rect(slide, x2, card_y, card_w, card_h, RGBColor(0x1a, 0x18, 0x0d))
    add_textbox(slide, "72.7%", x2, card_y + Inches(0.3),  card_w, Inches(0.9), size=54, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
    add_textbox(slide, "YOLO11n", x2, card_y + Inches(1.25), card_w, Inches(0.4), size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide, "33 → 9 detections", x2, card_y + Inches(1.65), card_w, Inches(0.35), size=13, color=DIM, align=PP_ALIGN.CENTER)
    add_textbox(slide, "1000 epochs · loss 0.597", x2, card_y + Inches(2.05), card_w, Inches(0.3), size=10, color=DIM, align=PP_ALIGN.CENTER)

    # v26n — red
    add_filled_rect(slide, x3, card_y, card_w, card_h, CARD_WN)
    add_textbox(slide, "16.3%", x3, card_y + Inches(0.3),  card_w, Inches(0.9), size=54, bold=True, color=RED, align=PP_ALIGN.CENTER)
    add_textbox(slide, "YOLO26n", x3, card_y + Inches(1.25), card_w, Inches(0.4), size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide, "43 → 36 detections", x3, card_y + Inches(1.65), card_w, Inches(0.35), size=13, color=DIM, align=PP_ALIGN.CENTER)
    add_textbox(slide, "1000 epochs · loss 0.108 ⚠", x3, card_y + Inches(2.05), card_w, Inches(0.3), size=10, color=DIM, align=PP_ALIGN.CENTER)

    add_rich_textbox(slide, [
        {"text": "Patch size: 100×100 px  ·  Image size: 640×640  ·  2.4% of total pixels",
         "size": 13, "color": RGBColor(0xcc, 0xcc, 0xcc)},
        {"text": "⚠ Within v26n runs, better objective convergence did not yield better suppression — see next slide",
         "size": 10, "color": DIMMER, "space_before": 6},
    ], Inches(0.9), Inches(5.85), Inches(11.5), Inches(0.9))


def slide4_paradox(prs):
    slide = blank_slide(prs)
    tag_label(slide, "KEY RESEARCH FINDING", Inches(0.9), Inches(0.4))

    add_rich_textbox(slide, [
        {"text": "The ", "size": 36, "bold": True, "color": WHITE},
        {"text": "v26n Paradox", "size": 36, "bold": True, "color": RED},
    ], Inches(0.9), Inches(0.85), Inches(11), Inches(1.2))

    lx = Inches(0.9)
    rx = Inches(7.0)
    cy = Inches(2.0)
    cw = Inches(5.7)

    # Left — "What happened"
    add_filled_rect(slide, lx, cy, cw, Inches(1.55), CARD_WN)
    add_textbox(slide, "WHAT HAPPENED", lx + Inches(0.2), cy + Inches(0.15), cw, Inches(0.25), size=9, bold=True, color=BLUE)
    add_rich_textbox(slide, [
        {"text": "The optimized objective converged on the scored head.", "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "final_det_loss = 0.108  on the one2many path.", "size": 12, "color": RED},
        {"text": "Suppression: only 16.3%.", "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
    ], lx + Inches(0.2), cy + Inches(0.5), cw - Inches(0.3), Inches(0.95))

    # Left — "Root cause"
    add_filled_rect(slide, lx, Inches(3.65), cw, Inches(2.4), CARD_INF)
    add_textbox(slide, "ROOT CAUSE", lx + Inches(0.2), Inches(3.8), cw, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide, "YOLO26n uses end-to-end Hungarian matching (head_end2end: true).",
                lx + Inches(0.2), Inches(4.1), cw - Inches(0.3), Inches(0.5), size=12, color=RGBColor(0xcc,0xcc,0xcc))
    add_rich_textbox(slide, [
        {"text": "• Training  optimizes the one2many auxiliary head", "size": 12, "color": YELLOW},
        {"text": "• Inference uses the one2one head for final detections", "size": 12, "color": GREEN},
        {"text": "• These heads are architecturally separate", "size": 12, "bold": True, "color": RGBColor(0xcc,0xcc,0xcc)},
    ], lx + Inches(0.2), Inches(4.65), cw - Inches(0.3), Inches(1.1))

    # Right — "Warm-start"
    add_filled_rect(slide, rx, cy, cw, Inches(1.9), CARD_BG)
    add_textbox(slide, "WARM-START EXPERIMENT", rx + Inches(0.2), cy + Inches(0.15), cw, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "Initialized v26n training from the v8n 90% patch. Trained 2000 epochs.",
        rx + Inches(0.2), cy + Inches(0.5), cw - Inches(0.3), Inches(0.5), size=12, color=RGBColor(0xcc,0xcc,0xcc))
    add_textbox(slide, "Result: 14.0%", rx + Inches(0.2), cy + Inches(1.05), cw - Inches(0.3), Inches(0.35), size=13, bold=True, color=WHITE)
    add_textbox(slide, "The barrier is structural, not a local minimum you can escape from.",
                rx + Inches(0.2), cy + Inches(1.42), cw - Inches(0.3), Inches(0.4), size=11, color=DIM)

    # Right — "What this means"
    add_filled_rect(slide, rx, Inches(4.05), cw, Inches(1.95), CARD_HL)
    add_textbox(slide, "WHAT THIS MEANS", rx + Inches(0.2), Inches(4.2), cw, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "YOLO26n shows strong resistance to this attack class in the current setup. "
        "The correct follow-up is to use an attack objective aligned with the inference path.",
        rx + Inches(0.2), Inches(4.55), cw - Inches(0.3), Inches(1.2), size=12, color=RGBColor(0xcc,0xcc,0xcc))


def slide5_transfer(prs):
    slide = blank_slide(prs)
    tag_label(slide, "CROSS-MODEL GENERALIZATION", Inches(0.9), Inches(0.4))

    add_rich_textbox(slide, [
        {"text": "Transfer ", "size": 36, "bold": True, "color": WHITE},
        {"text": "Matrix",    "size": 36, "bold": True, "color": BLUE},
    ], Inches(0.9), Inches(0.85), Inches(11), Inches(1.2))

    # ---- Left table: single-source transfers ----
    lx = Inches(0.9)
    ty = Inches(2.1)

    add_textbox(slide, "SINGLE-SOURCE TRANSFERS", lx, ty, Inches(5.8), Inches(0.3), size=9, bold=True, color=BLUE)

    headers = ["Patch source", "Eval model", "Suppression"]
    rows = [
        ("v8n",  "v11n",  "36.4%",  YELLOW),
        ("v11n", "v8n",   "50.0%",  GREEN),
        ("v26n", "v8n",   "45.0%",  GREEN),
        ("v26n", "v11n",  "24.2%",  YELLOW),
        ("v8n",  "v26n",  "11.6%",  RED),
        ("v11n", "v26n",  "9.3%",   RED),
    ]

    row_h = Inches(0.42)
    col_x = [lx, lx + Inches(1.8), lx + Inches(3.4)]
    col_w = [Inches(1.7), Inches(1.5), Inches(2.5)]

    # Header row
    hy = ty + Inches(0.35)
    for i, h in enumerate(headers):
        add_textbox(slide, h, col_x[i], hy, col_w[i], Inches(0.3), size=9, bold=False, color=DIM)

    # Data rows
    for ri, (src, evl, pct, col) in enumerate(rows):
        ry = hy + Inches(0.32) + ri * row_h
        if ri % 2 == 0:
            add_filled_rect(slide, lx - Inches(0.1), ry - Inches(0.05),
                            Inches(5.9), row_h, RGBColor(0x12, 0x12, 0x1a))
        add_textbox(slide, src, col_x[0], ry, col_w[0], row_h, size=12, color=RGBColor(0xcc,0xcc,0xcc))
        add_textbox(slide, evl, col_x[1], ry, col_w[1], row_h, size=12, color=RGBColor(0xcc,0xcc,0xcc))
        add_textbox(slide, pct, col_x[2], ry, col_w[2], row_h, size=12, bold=True, color=col)

    # ---- Right side ----
    rx = Inches(7.0)
    cw = Inches(5.7)

    add_textbox(slide, "JOINT PATCHES", rx, ty, cw, Inches(0.3), size=9, bold=True, color=BLUE)

    jrows = [
        ("v8n + v11n", "v8n",   "85%",   GREEN),
        ("v8n + v11n", "v11n",  "66.7%", GREEN),
        ("v8n + v26n", "v26n",  "18.6%", RED),
    ]
    jcol_x = [rx, rx + Inches(2.1), rx + Inches(3.5)]
    jcol_w = [Inches(2.0), Inches(1.3), Inches(1.5)]

    jhy = ty + Inches(0.35)
    for i, h in enumerate(["Joint source", "Eval", "Suppression"]):
        add_textbox(slide, h, jcol_x[i], jhy, jcol_w[i], Inches(0.3), size=9, color=DIM)

    for ri, (src, evl, pct, col) in enumerate(jrows):
        ry = jhy + Inches(0.32) + ri * row_h
        if ri % 2 == 0:
            add_filled_rect(slide, rx - Inches(0.1), ry - Inches(0.05),
                            cw, row_h, RGBColor(0x12, 0x12, 0x1a))
        add_textbox(slide, src, jcol_x[0], ry, jcol_w[0], row_h, size=12, color=RGBColor(0xcc,0xcc,0xcc))
        add_textbox(slide, evl, jcol_x[1], ry, jcol_w[1], row_h, size=12, color=RGBColor(0xcc,0xcc,0xcc))
        add_textbox(slide, pct, jcol_x[2], ry, jcol_w[2], row_h, size=12, bold=True, color=col)

    # Key insight card
    insight_y = jhy + Inches(0.32) + len(jrows) * row_h + Inches(0.3)
    add_filled_rect(slide, rx, insight_y, cw, Inches(1.5), CARD_INF)
    add_textbox(slide, "KEY INSIGHT", rx + Inches(0.2), insight_y + Inches(0.15), cw, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "Transfer rates vary by architecture — not by patch placement. "
        "This rules out occlusion as the primary mechanism.",
        rx + Inches(0.2), insight_y + Inches(0.5), cw - Inches(0.3), Inches(0.85),
        size=12, color=RGBColor(0xcc,0xcc,0xcc))


def slide6_demo(prs, patch_path: Path):
    slide = blank_slide(prs)
    tag_label(slide, "LIVE DEMONSTRATION", Inches(0.9), Inches(0.4))

    lx = Inches(0.9)
    rx = Inches(8.5)
    cy = Inches(1.2)

    add_textbox(slide, "Live Demo", lx, cy, Inches(6), Inches(0.95), size=40, bold=True, color=GREEN)
    add_textbox(slide,
        "Split-screen: clean YOLO detections on the left,\npatch digitally overlaid on the right.",
        lx, Inches(2.25), Inches(6.5), Inches(0.8), size=14, color=RGBColor(0xcc,0xcc,0xcc))

    add_rich_textbox(slide, [
        {"text": "• Patch: 100×100 px, YOLOv8n",                        "size": 13, "color": GREEN},
        {"text": "• Placed on torso of largest detected person",          "size": 13, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "• Rolling 30-frame suppression average",               "size": 13, "color": RGBColor(0xcc,0xcc,0xcc)},
    ], lx, Inches(3.2), Inches(6.5), Inches(1.0))

    # Physical print card
    add_filled_rect(slide, lx, Inches(4.35), Inches(6.5), Inches(1.65), CARD_WN)
    add_textbox(slide, "PHYSICAL PRINT", lx + Inches(0.2), Inches(4.5), Inches(6), Inches(0.25), size=9, bold=True, color=BLUE)
    add_rich_textbox(slide, [
        {"text": "Patch exported at 300 DPI, 8\"×8\".", "size": 12, "color": YELLOW},
        {"text": "Physical suppression ~30–60% (printer colour shift, lighting).", "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
        {"text": "NPS loss during training partially compensates.", "size": 12, "color": RGBColor(0xcc,0xcc,0xcc)},
    ], lx + Inches(0.2), Inches(4.8), Inches(6.2), Inches(1.0))

    # Patch image
    if patch_path.exists():
        slide.shapes.add_picture(
            str(patch_path),
            rx, Inches(1.5), Inches(3.5), Inches(3.5)
        )
        add_textbox(slide, "YOLOv8n patch — 90% suppression\n100×100 px · shown 2×",
                    rx, Inches(5.1), Inches(3.5), Inches(0.7), size=10, color=DIM, align=PP_ALIGN.CENTER)


def slide7_conclusions(prs):
    slide = blank_slide(prs)
    tag_label(slide, "CONCLUSIONS", Inches(0.9), Inches(0.4))

    add_rich_textbox(slide, [
        {"text": "What We", "size": 38, "bold": True, "color": WHITE},
        {"text": "Learned",  "size": 38, "bold": True, "color": GREEN, "space_before": 2},
    ], Inches(0.9), Inches(0.85), Inches(11), Inches(1.6))

    card_w = Inches(3.6)
    card_h = Inches(2.4)
    card_y = Inches(2.5)
    gap    = Inches(0.4)
    x1 = Inches(0.9)
    x2 = x1 + card_w + gap
    x3 = x2 + card_w + gap

    # Card 1
    add_filled_rect(slide, x1, card_y, card_w, card_h, CARD_HL)
    add_textbox(slide, "PATCHES WORK", x1 + Inches(0.2), card_y + Inches(0.2), card_w, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "A 2.4% image patch suppresses YOLOv8n person detection by 90%. "
        "The effect transfers across model families at 10–50%.",
        x1 + Inches(0.2), card_y + Inches(0.6), card_w - Inches(0.3), Inches(1.6),
        size=13, color=RGBColor(0xcc,0xcc,0xcc))

    # Card 2
    add_filled_rect(slide, x2, card_y, card_w, card_h, CARD_INF)
    add_textbox(slide, "ARCHITECTURE MATTERS", x2 + Inches(0.2), card_y + Inches(0.2), card_w, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "YOLO26n's end-to-end matching breaks the usual assumption that "
        "optimizing the attack objective will directly reduce detections.",
        x2 + Inches(0.2), card_y + Inches(0.6), card_w - Inches(0.3), Inches(1.6),
        size=13, color=RGBColor(0xcc,0xcc,0xcc))

    # Card 3
    add_filled_rect(slide, x3, card_y, card_w, card_h, RGBColor(0x1a, 0x18, 0x0d))
    add_textbox(slide, "NEXT STEPS", x3 + Inches(0.2), card_y + Inches(0.2), card_w, Inches(0.25), size=9, bold=True, color=BLUE)
    add_textbox(slide,
        "Route gradients through the one2one head (Wang et al. 2026). "
        "Adversarial training as a defense. Physical robustness evaluation.",
        x3 + Inches(0.2), card_y + Inches(0.6), card_w - Inches(0.3), Inches(1.6),
        size=13, color=RGBColor(0xcc,0xcc,0xcc))

    add_textbox(slide,
        "Training script · Colab notebook · Live demo · All results  →  github.com/Cmaddock99/Patch_Yolo",
        Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.45),
        size=12, color=BLUE)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).parent.parent
    patch_path = root / "outputs" / "yolov8n_patch_v2" / "patches" / "patch.png"
    out_path   = root / "presentation.pptx"

    prs = new_prs()
    slide1_title(prs)
    slide2_what_is(prs)
    slide3_results(prs)
    slide4_paradox(prs)
    slide5_transfer(prs)
    slide6_demo(prs, patch_path)
    slide7_conclusions(prs)

    prs.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
