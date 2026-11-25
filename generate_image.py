#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Wednesday 25 November 2026.

A newspaper-style summary of the day's world news, drawn entirely in
code with Pillow: masthead, lead story with a painted scene, six story
cards with small illustrations, and a briefs strip. Output: entry.png,
1024 x 1024, well under 1 MiB.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (26, 26, 26)
RULE = (26, 26, 26)
RED = (178, 34, 28)
MUTED = (90, 84, 72)
SKY_TOP = (44, 62, 96)
SKY_MID = (196, 96, 44)
SKY_LOW = (232, 150, 66)
SEA = (16, 42, 66)
SEA_DARK = (10, 30, 50)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(text, fnt, width):
    """Split text into lines that fit `width` pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines of text; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def draw_masthead(draw):
    title = font(SERIF_B, 92)
    draw.text((W // 2, 6), "THE WORLD", font=title, fill=INK, anchor="ma")
    rule(draw, 20, 108, W - 20, 3)
    date_f = font(SANS_B, 21)
    draw.text(
        (W // 2, 118),
        "WEDNESDAY, 25 NOVEMBER 2026",
        font=date_f,
        fill=INK,
        anchor="ma",
    )
    small = font(SANS, 13)
    draw.text((20, 122), "No. 329", font=small, fill=MUTED, anchor="la")
    draw.text((W - 20, 122), "Price $2.50", font=small, fill=MUTED, anchor="ra")
    rule(draw, 20, 150, W - 20, 1)


def flame(draw, cx, base_y, size):
    """A stylised flame: layered teardrop polygons in yellow/orange/red."""
    layers = [
        ((255, 214, 64), 0.55),
        ((255, 140, 26), 0.8),
        ((214, 48, 16), 1.0),
    ]
    for colour, scale in layers:
        s = size * scale
        pts = [
            (cx, base_y - s * 1.9),
            (cx + s * 0.62, base_y - s * 0.7),
            (cx + s * 0.45, base_y),
            (cx - s * 0.45, base_y),
            (cx - s * 0.62, base_y - s * 0.7),
        ]
        draw.polygon(pts, fill=colour)


def smoke(draw, cx, top_y, puffs):
    for i, (dx, r, shade) in enumerate(puffs):
        y = top_y - i * 16
        draw.ellipse(
            [cx + dx - r, y - r, cx + dx + r, y + r], fill=shade
        )


def tanker(draw, x, y, w, h, hull=(58, 58, 62), deck=(150, 40, 30)):
    """A simple oil tanker silhouette: hull, deck, bridge tower, funnel."""
    draw.rectangle([x, y, x + w, y + h], fill=hull)
    draw.rectangle([x, y - h * 0.28, x + w, y], fill=deck)
    bx = x + w * 0.78
    draw.rectangle([bx, y - h * 1.15, bx + w * 0.14, y - h * 0.28], fill=(40, 40, 44))
    draw.rectangle([bx - w * 0.02, y - h * 1.3, bx + w * 0.16, y - h * 1.15], fill=(40, 40, 44))
    fx = x + w * 0.12
    draw.rectangle([fx, y - h * 0.85, fx + w * 0.09, y - h * 0.28], fill=(196, 60, 30))
    for wx in range(4):
        draw.rectangle(
            [x + w * 0.18 + wx * w * 0.14, y + h * 0.25, x + w * 0.26 + wx * w * 0.14, y + h * 0.62],
            fill=(232, 220, 190),
        )


def draw_lead_scene(draw, x0, y0, x1, y1):
    """Dusk over the Strait of Hormuz: two tankers burning, a mine."""
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.52)
    for i in range(horizon - y0):
        t = i / max(1, horizon - y0)
        r = int(SKY_TOP[0] + (SKY_MID[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_MID[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_MID[2] - SKY_TOP[2]) * t)
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    draw.ellipse(
        [x0 + w * 0.72, y0 + 18, x0 + w * 0.72 + 64, y0 + 82],
        fill=(240, 190, 110),
    )
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    for i in range(5):
        yy = horizon + 14 + i * 16
        draw.line([(x0 + 12, yy), (x1 - 12, yy)], fill=SEA_DARK, width=2)
    # far tanker, burning
    tanker(draw, x0 + 60, horizon + 26, 300, 34)
    flame(draw, x0 + 150, horizon + 22, 30)
    flame(draw, x0 + 300, horizon + 22, 22)
    smoke(draw, x0 + 200, horizon - 6, [(0, 12, (96, 96, 100)), (10, 14, (80, 80, 84)), (-8, 16, (66, 66, 70))])
    # near tanker, burning harder
    tanker(draw, x0 + w - 430, horizon + 36, 360, 34)
    flame(draw, x0 + w - 330, horizon + 32, 34)
    flame(draw, x0 + w - 180, horizon + 32, 24)
    smoke(draw, x0 + w - 260, horizon + 10, [(0, 13, (96, 96, 100)), (12, 15, (80, 80, 84)), (-10, 17, (66, 66, 70))])
    # naval mine in the foreground water, clear of both tankers
    mx, my = x0 + 70, y1 - 24
    draw.ellipse([mx - 15, my - 15, mx + 15, my + 15], fill=(24, 24, 28))
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]:
        draw.line([(mx, my), (mx + dx * 24, my + dy * 24)], fill=(24, 24, 28), width=3)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_lead(draw):
    y = 158
    head_f = font(SERIF_B, 46)
    y = text_block(draw, 20, y, ["TWO TANKERS ABLAZE", "IN THE STRAIT OF HORMUZ"], head_f, leading=52)
    sub_f = font(SERIF, 20)
    draw.text(
        (20, y + 2),
        "Iran says both ships struck naval mines on an unauthorised route",
        font=sub_f,
        fill=MUTED,
    )
    draw_lead_scene(draw, 20, 292, W - 20, 452)
    cap_f = font(SANS, 12)
    draw.text(
        (20, 458),
        "Fire and smoke rise from two tankers in the Strait of Hormuz on Wednesday.",
        font=cap_f,
        fill=MUTED,
    )
    body_f = font(SERIF, 17)
    body = (
        "Iran's Revolutionary Guard said two oil tankers struck naval mines and "
        "caught fire in the Strait of Hormuz on Wednesday, after straying onto "
        "an unauthorised route. The blasts deepen a widening war at sea as "
        "Houthi attacks spread to Saudi oil sites."
    )
    text_block(draw, 20, 478, wrap(body, body_f, W - 40), body_f, leading=22)
    rule(draw, 20, 556, W - 20, 2)


def refinery_icon(draw, x0, y0, x1, y1, flame_on=True):
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 232))
    base = y1 - 8
    draw.rectangle([x0 + 14, base - 46, x0 + 30, base], fill=(96, 104, 110))
    draw.rectangle([x0 + 40, base - 62, x0 + 52, base], fill=(120, 128, 134))
    draw.rectangle([x0 + 62, base - 38, x0 + 96, base], fill=(140, 148, 154))
    draw.rectangle([x0 + 104, base - 54, x0 + 116, base], fill=(96, 104, 110))
    draw.rectangle([x0 + 124, base - 30, x0 + 150, base], fill=(120, 128, 134))
    if flame_on:
        flame(draw, x0 + 46, base - 62, 13)
        smoke(draw, x0 + 46, base - 84, [(0, 8, (120, 120, 124)), (6, 10, (100, 100, 104))])
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def drone_icon(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(24, 34, 52))
    cx, cy = (x0 + x1) // 2, y0 + 26
    draw.ellipse([cx - 26, cy - 8, cx + 26, cy + 8], fill=(200, 200, 205))
    for dx in (-34, 34):
        draw.ellipse([cx + dx - 12, cy - 14, cx + dx + 12, cy - 2], fill=(150, 150, 155))
        draw.line([(cx + dx - 16, cy - 8), (cx + dx + 16, cy - 8)], fill=(220, 220, 225), width=2)
    draw.line([(cx, cy + 8), (cx, cy + 22)], fill=(200, 200, 205), width=3)
    flame(draw, cx, y1 - 4, 12)
    refinery_icon(draw, x0, y1 - 34, x1, y1, flame_on=False)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def city_icon(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 214, 188))
    base = y1 - 6
    heights = [52, 70, 44, 62, 38]
    bx = x0 + 10
    for hgt in heights:
        bw = (x1 - x0 - 20) // 5 - 4
        draw.rectangle([bx, base - hgt, bx + bw, base], fill=(74, 74, 84))
        for wy in range(2):
            for wx in range(2):
                draw.rectangle(
                    [bx + 4 + wx * (bw // 2), base - hgt + 8 + wy * 18, bx + 8 + wx * (bw // 2), base - hgt + 14 + wy * 18],
                    fill=(255, 214, 120),
                )
        bx += bw + 4
    smoke(draw, x0 + 60, y0 + 22, [(0, 9, (110, 110, 114)), (8, 11, (92, 92, 96))])
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def court_icon(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(226, 228, 232))
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 70, y0 + 26), (cx + 70, y0 + 26), (cx, y0 + 4)], fill=(96, 100, 110))
    draw.rectangle([x0 + 18, y0 + 26, x1 - 18, y0 + 32], fill=(70, 74, 84))
    for i in range(4):
        col_x = x0 + 26 + i * 34
        draw.rectangle([col_x, y0 + 32, col_x + 12, y1 - 10], fill=(150, 154, 162))
    draw.rectangle([x0 + 14, y1 - 10, x1 - 14, y1 - 4], fill=(70, 74, 84))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def space_icon(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(12, 20, 44))
    for sx, sy in [(24, 14), (70, 30), (120, 10), (150, 34), (40, 44), (96, 48)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1], fill=(255, 255, 255))
    draw.ellipse([x0 + 12, y1 - 22, x1 - 12, y1], fill=(38, 96, 150))
    draw.ellipse([x0 + 34, y1 - 14, x1 - 34, y1], fill=(58, 128, 178))
    cx, cy = (x0 + x1) // 2, y0 + 30
    draw.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=(210, 210, 215))
    draw.rectangle([cx - 46, cy - 3, cx - 8, cy + 3], fill=(90, 130, 200))
    draw.rectangle([cx + 8, cy - 3, cx + 46, cy + 3], fill=(90, 130, 200))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def islands_icon(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(168, 206, 226))
    draw.ellipse([x0 + 16, y0 + 34, x0 + 74, y0 + 66], fill=(96, 150, 96))
    draw.ellipse([x0 + 96, y0 + 16, x0 + 146, y0 + 52], fill=(120, 168, 110))
    draw.ellipse([x0 + 60, y0 + 8, x0 + 78, y0 + 22], fill=(255, 255, 255))
    for i in range(9):
        t = i / 8
        px = x0 + 46 + int((x1 - x0 - 92) * t)
        py = y0 + 50 - int(14 * (1 - (2 * t - 1) ** 2))
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


STORIES = [
    (
        "HOUTHIS HIT SAUDI REFINERY",
        "Yemen's Houthis say they struck the Ras Tanura oil refinery. A day earlier a drone hit a Riyadh tower, injuring 11.",
        refinery_icon,
    ),
    (
        "UKRAINE DRONES HIT TWO REFINERIES",
        "Ukrainian drones set Rosneft's Syzran and Kuibyshev refineries ablaze overnight; 145 drones were downed, one person killed.",
        drone_icon,
    ),
    (
        "ODESA STRIKE KILLS TWO",
        "A Russian strike on the Odesa region killed two and hurt three, a child among them; a Kyiv apartment block was hit too.",
        city_icon,
    ),
    (
        "HUAWEI CONVICTED IN U.S.",
        "A Brooklyn jury convicts Huawei on 10 counts, including bank fraud and stealing trade secrets; the racketeering charge fails.",
        court_icon,
    ),
    (
        "SHENZHOU-24 DOCKS AT TIANGONG",
        "China's Shenzhou-24 docks with the Tiangong station hours after launch, carrying Pakistan's first astronaut into orbit.",
        space_icon,
    ),
    (
        "PACIFIC TREATY SIGNED",
        "Australia and the Solomon Islands sign a treaty in Canberra making Australia the Solomons' main defence partner.",
        islands_icon,
    ),
]


def draw_grid(draw):
    margin, gap = 20, 12
    cw = (W - 2 * margin - 2 * gap) // 3
    ch = 168
    y_top = 572
    head_f = font(SERIF_B, 17)
    body_f = font(SERIF, 13)
    for idx, (headline, body, icon) in enumerate(STORIES):
        row, col = divmod(idx, 3)
        x0 = margin + col * (cw + gap)
        y0 = y_top + row * (ch + gap)
        icon(draw, x0, y0, x0 + cw, y0 + 76)
        y = y0 + 84
        y = text_block(draw, x0, y, wrap(headline, head_f, cw), head_f, leading=20)
        text_block(draw, x0, y + 2, wrap(body, body_f, cw), body_f, leading=16)
    rule(draw, 20, y_top + 2 * ch + gap + 6, W - 20, 2)


BRIEFS = [
    ("MARKETS", "Dow closes above 50,000 for the first time, at 50,018.70; KOSPI falls 6.2%."),
    ("SUDAN", "RSF drone strikes kill 19 civilians in two cities, a rights group says."),
    ("COLOMBIA", "Troops free all hostages in a Cartagena supermarket siege; one captor killed."),
    ("POPE", "Leo XIV laments the COP31 failure as climate extremes grow more frequent."),
]


def draw_briefs(draw):
    y0 = 938
    label_f = font(SANS_B, 13)
    body_f = font(SERIF, 13)
    margin, gap = 20, 12
    cw = (W - 2 * margin - 3 * gap) // 4
    for i, (label, text) in enumerate(BRIEFS):
        x0 = margin + i * (cw + gap)
        draw.text((x0, y0), label, font=label_f, fill=RED)
        text_block(draw, x0, y0 + 18, wrap(text, body_f, cw), body_f, leading=16)
    rule(draw, 20, 1012, W - 20, 1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_grid(draw)
    draw_briefs(draw)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
