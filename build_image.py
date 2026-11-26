"""Render the front page for Thursday 26 November 2026.

Draws a clean newspaper front page (1024x1024) with six stories from
26 November 2026, all phrased in the author's own words: a lead story,
a two-by-two grid of four more, and a closing strip. Everything is
drawn with Pillow primitives and DejaVu fonts; no image files, no
network, no randomness, no time or date is used, so the output is
identical on every run.

Run:  python3 build_image.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (20, 20, 20)
GREY = (90, 90, 90)
RED = (178, 34, 34)
DARK_BLUE = (28, 48, 88)
ORANGE = (232, 116, 24)
FLAME = (244, 164, 40)
SAND = (196, 154, 92)
SKY = (214, 230, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=4):
    """Draw lines of text; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def fit_text(draw, text, fnt, x, y, max_w, max_lines, fill=INK, leading=4):
    """Draw wrapped text, cut to max_lines; returns y below the text."""
    lines = wrap(text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # Trim the last line so an ellipsis fits.
        while lines and fnt.getlength(lines[-1] + "...") > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "..."
    return draw_lines(draw, lines, x, y, fnt, fill=fill, leading=leading)


def rule(draw, y, x0=36, x1=988, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- pictures

def pic_cairo(draw, x, y, w, h):
    """Night road, an overturned tanker and flames."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 30, 36))
    # Distant skyline.
    for bx, bw, bh in [(10, 60, 40), (90, 44, 66), (160, 70, 34), (260, 50, 58),
                       (340, 60, 44), (420, 40, 30)]:
        draw.rectangle([x + bx, y + h - 150 - bh, x + bx + bw, y + h - 150],
                       fill=(52, 52, 62))
    # Road.
    draw.rectangle([x, y + h - 150, x + w, y + h], fill=(74, 74, 78))
    draw.line([(x, y + h - 74), (x + w, y + h - 74)], fill=(220, 200, 90),
              width=4)
    # Overturned tanker: cylinder body on its side, cab at the front.
    draw.rounded_rectangle([x + 60, y + h - 132, x + 330, y + h - 92],
                           radius=18, fill=(150, 152, 158))
    draw.rounded_rectangle([x + 330, y + h - 128, x + 396, y + h - 92],
                           radius=8, fill=(120, 40, 36))
    draw.ellipse([x + 96, y + h - 96, x + 132, y + h - 60], fill=(20, 20, 20))
    draw.ellipse([x + 250, y + h - 96, x + 286, y + h - 60], fill=(20, 20, 20))
    # Flames rising from the tanker.
    flames = [
        [(x + 90, y + h - 130), (x + 130, y + h - 220), (x + 170, y + h - 130)],
        [(x + 170, y + h - 130), (x + 215, y + h - 250), (x + 260, y + h - 130)],
        [(x + 260, y + h - 130), (x + 300, y + h - 200), (x + 340, y + h - 130)],
    ]
    for poly in flames:
        draw.polygon(poly, fill=ORANGE)
    draw.polygon([(x + 180, y + h - 130), (x + 215, y + h - 205),
                  (x + 250, y + h - 130)], fill=FLAME)
    # Smoke.
    for cx, cy, r in [(140, 60, 26), (210, 40, 32), (280, 66, 24)]:
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(140, 140, 148))


def pic_stocks(draw, x, y, w, h):
    """A chart line falling, with red bars."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=GREY, width=1)
    # Grid lines.
    for gy in (y + h // 3, y + 2 * h // 3):
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(220, 220, 220), width=1)
    # Falling bars.
    bars = [44, 38, 40, 32, 34, 25, 27, 18, 20, 10]
    bw = (w - 24) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 12 + i * bw
        draw.rectangle([bx, y + h - 8 - bh, bx + bw - 4, y + h - 8],
                       fill=(200, 60, 60))
    # Falling line with arrow.
    pts = [(x + 14, y + 14), (x + 80, y + 18), (x + 146, y + 16),
           (x + 212, y + 30), (x + 278, y + 28), (x + 344, y + 44),
           (x + 410, y + 42), (x + w - 16, y + 62)]
    draw.line(pts, fill=RED, width=4, joint="curve")
    draw.polygon([(x + w - 16, y + 62), (x + w - 32, y + 54),
                  (x + w - 30, y + 72)], fill=RED)
    draw.text((x + w - 58, y + 6), "-4%", font=SANS_B(20), fill=RED)


def pic_tariffs(draw, x, y, w, h):
    """A globe beside stacked cargo containers."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # Globe.
    cx, cy, r = x + 66, y + h // 2, 32
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 120, 190))
    draw.ellipse([cx - 18, cy - 22, cx + 4, cy - 2], fill=(90, 170, 90))
    draw.ellipse([cx - 2, cy + 6, cx + 22, cy + 22], fill=(90, 170, 90))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255),
             width=2)
    # Containers, stacked on the right.
    draw.rectangle([x + 130, y + 14, x + w - 90, y + 38], fill=(178, 34, 34))
    draw.rectangle([x + 146, y + 42, x + w - 74, y + 66], fill=(28, 90, 140))
    draw.text((x + w - 66, y + 22), "15%", font=SANS_B(26), fill=INK)


def pic_mumbai(draw, x, y, w, h):
    """The Gateway of India arch against a warm sky."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 226, 178))
    draw.ellipse([x + w - 66, y + 8, x + w - 28, y + 46], fill=(244, 190, 90))
    # Arch: two pillars, a curved top and an open doorway.
    draw.rectangle([x + 180, y + 34, x + 206, y + h - 6], fill=SAND)
    draw.rectangle([x + 254, y + 34, x + 280, y + h - 6], fill=SAND)
    draw.pieslice([x + 180, y + 6, x + 280, y + 62], 180, 360, fill=SAND)
    draw.pieslice([x + 214, y + 34, x + 246, y + 66], 180, 360,
                  fill=(250, 226, 178))
    draw.rectangle([x + 214, y + 50, x + 246, y + h - 6],
                   fill=(250, 226, 178))
    draw.rectangle([x + 168, y + 28, x + 292, y + 36], fill=(170, 128, 70))
    draw.rectangle([x + 160, y + h - 12, x + 300, y + h - 6],
                   fill=(170, 128, 70))
    # Small dome on top.
    draw.ellipse([x + 222, y + 0, x + 238, y + 12], fill=SAND)
    # Sea line.
    draw.line([(x, y + h - 4), (x + w, y + h - 4)], fill=(90, 140, 180),
              width=3)


def pic_hera(draw, x, y, w, h):
    """A cratered asteroid tumbling beside its companion."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 14, 28))
    # Stars.
    for sx, sy in [(16, 12), (60, 34), (120, 10), (200, 26), (250, 12),
                   (300, 30), (400, 10), (440, 40), (24, 60), (420, 66)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                     fill=(255, 255, 255))
    # Didymos, the larger companion.
    draw.ellipse([x + 330, y + 12, x + 420, y + 72], fill=(150, 148, 140))
    for cx, cy, r in [(352, 28, 7), (382, 48, 9), (356, 58, 5)]:
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(120, 118, 110))
    # Dimorphos, flattened by a stadium-sized crater.
    draw.ellipse([x + 60, y + 8, x + 170, y + 76], fill=(180, 178, 170))
    draw.ellipse([x + 76, y + 16, x + 154, y + 66], fill=(110, 108, 100))
    draw.ellipse([x + 100, y + 32, x + 130, y + 56], fill=(70, 68, 62))
    # Loose boulders.
    for bx, by, r in [(220, 24, 6), (250, 56, 4), (210, 66, 5),
                      (280, 40, 4)]:
        draw.ellipse([x + bx - r, y + by - r, x + bx + r, y + by + r],
                     fill=(160, 158, 150))


def pic_storm(draw, x, y, w, h):
    """A dark rain cloud, rain and a lightning bolt over a coast."""
    draw.rectangle([x, y, x + w, y + h], fill=(70, 86, 110))
    # Sea.
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=(40, 90, 130))
    for wx in range(0, w, 46):
        draw.arc([x + wx, y + h - 34, x + wx + 40, y + h - 6], 0, 180,
                 fill=(255, 255, 255), width=2)
    # Cloud.
    for cx, cy, r in [(70, 44, 30), (140, 32, 38), (210, 46, 32),
                      (262, 54, 24)]:
        draw.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                     fill=(40, 44, 54))
    draw.rectangle([x + 46, y + 44, x + 272, y + 76], fill=(40, 44, 54))
    # Rain.
    for rx in range(50, 280, 26):
        draw.line([(x + rx, y + 84), (x + rx - 8, y + 108)],
                  fill=(200, 220, 240), width=3)
    # Lightning.
    draw.polygon([(x + 252, y + 22), (x + 232, y + 70), (x + 248, y + 70),
                  (x + 230, y + 118), (x + 272, y + 62), (x + 256, y + 62)],
                 fill=(250, 220, 60))


# ------------------------------------------------------------------ page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    title = "WORLD NEWS"
    d.text(((W - SERIF_B(66).getlength(title)) / 2, 18), title,
           font=SERIF_B(66), fill=INK)
    d.text(((W - SANS_B(21).getlength("THURSDAY, 26 NOVEMBER 2026")) / 2, 100),
           "THURSDAY, 26 NOVEMBER 2026", font=SANS_B(21), fill=INK)
    rule(d, 132)
    rule(d, 137, width=1)

    # ---- Lead story: Cairo tanker fire.
    pic_cairo(d, 36, 150, 464, 242)
    d.rectangle([36, 150, 500, 392], outline=GREY, width=1)
    lx = 520
    d.text((lx, 152), "EGYPT  —  DISASTER", font=SANS_B(16), fill=RED)
    y = fit_text(d, "Tanker fire kills 31 on Cairo ring road",
                 SERIF_B(33), lx, 178, 468, 2, leading=2)
    y = fit_text(
        d,
        "A fuel tanker carrying petroleum products overturned on the "
        "Greater Cairo Ring Road and burst into flames, killing at least "
        "31 people and injuring 21. The blaze spread to dozens of cars "
        "before fire crews brought it under control.",
        SANS(17), lx, y + 6, 468, 5)
    rule(d, 408)

    # ---- Grid of four stories.
    cells = [
        ("UNITED STATES  —  MARKETS", "Wall Street slides as AI sell-off deepens",
         "The Nasdaq fell almost 4% as investors fled artificial-intelligence "
         "shares, dragging all three main US indexes down.", pic_stocks),
        ("TRADE  —  TARIFFS", "Taipei welcomes lowest US tariff rate",
         "Taiwan said Washington's proposed 15% duty puts it in the lowest "
         "tier, beside Japan, South Korea and the EU.", pic_tariffs),
        ("INDIA  —  REMEMBRANCE", "India marks 18 years since Mumbai attacks",
         "India remembered the 26/11 siege of 2008, when gunmen attacked "
         "the city and more than 160 people were killed.", pic_mumbai),
        ("SPACE  —  ASTEROIDS", "Hera reveals a cratered, tumbling asteroid",
         "Europe's Hera probe sent back the first close views of Dimorphos, "
         "the asteroid struck by NASA's DART mission in 2022.", pic_hera),
    ]
    grid_x = [36, 524]
    grid_y = [422, 618]
    for i, (kicker, head, body, pic) in enumerate(cells):
        cx = grid_x[i % 2]
        cy = grid_y[i // 2]
        pic(d, cx, cy, 464, 76)
        d.text((cx, cy + 82), kicker, font=SANS_B(13),
               fill=RED if i % 2 == 0 else DARK_BLUE)
        y = fit_text(d, head, SERIF_B(21), cx, cy + 100, 464, 2, leading=1)
        fit_text(d, body, SANS(14), cx, y + 2, 464, 2, leading=2)
    rule(d, 826)

    # ---- Closer: Thanksgiving storm.
    pic_storm(d, 36, 840, 300, 124)
    sx = 356
    d.text((sx, 840), "UNITED STATES  —  WEATHER", font=SANS_B(15), fill=RED)
    y = fit_text(d, "Thanksgiving storm batters the East Coast",
                 SERIF_B(25), sx, 864, 632, 1)
    fit_text(
        d,
        "Heavy rain, gusts of up to 60 mph and major coastal flooding hit "
        "the US East Coast on Thanksgiving Day, snarling travel for "
        "millions. High winds may ground the balloons at New York's parade.",
        SANS(15), sx, y + 4, 632, 3)

    # Footer.
    rule(d, 980, width=1)
    foot = "WORLD NEWS  •  THURSDAY, 26 NOVEMBER 2026  •  COMPILED FROM WIRE REPORTS"
    d.text(((W - SANS(13).getlength(foot)) / 2, 988), foot, font=SANS(13),
           fill=GREY)

    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("Wrote", out, img.size)


if __name__ == "__main__":
    main()
