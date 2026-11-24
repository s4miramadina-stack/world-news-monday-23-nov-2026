"""Draws entry.png: the world's news of Monday 23 November 2026 on one 1024 x 1024 page.

    python3 draw.py            # needs Pillow and the Noto fonts; writes entry.png beside this file

Everything is drawn at 2x and scaled down once, so lines and shapes come out smooth.
The result is deterministic for a given Pillow + font install; main.ts only copies
the finished entry.png, so the graded program needs nothing but Node.
"""
import os
from PIL import Image, ImageDraw, ImageFont

import stories as S

K = 2                       # supersampling factor
W = H = 1024
FD = "/usr/share/fonts/truetype/noto/"

PAPER = (250, 247, 240)
CARD = (255, 255, 255)
INK = (22, 26, 36)
NAVY = (19, 31, 56)
MUTED = (96, 101, 114)
LINE = (214, 207, 192)
RED = (200, 34, 40)
AMBER = (246, 190, 60)
SKY = (196, 222, 240)

img = Image.new("RGB", (W * K, H * K), PAPER)
d = ImageDraw.Draw(img)
_fonts = {}


def F(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FD + name, int(round(size * K)))
    return _fonts[key]


def s(v):
    return int(round(v * K))


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1, r=0):
    box = [s(x0), s(y0), s(x1), s(y1)]
    if r:
        d.rounded_rectangle(box, radius=s(r), fill=fill, outline=outline, width=s(width) if outline else 0)
    else:
        d.rectangle(box, fill=fill, outline=outline, width=s(width) if outline else 0)


def poly(pts, fill=None, outline=None, width=1):
    p = [(s(x), s(y)) for x, y in pts]
    d.polygon(p, fill=fill, outline=outline, width=s(width) if outline else 1)


def line(pts, fill, width=1):
    d.line([(s(x), s(y)) for x, y in pts], fill=fill, width=max(1, s(width)), joint="curve")


def circle(cx, cy, r, fill=None, outline=None, width=1):
    d.ellipse([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], fill=fill, outline=outline,
              width=s(width) if outline else 0)


def tw(text, font):
    return d.textlength(text.replace("\u2212", "-"), font=font) / K


def text(x, y, t, font, fill=INK, anchor="la"):
    t = t.replace("\u2212", "-")   # these Noto cuts lack U+2212; a hyphen reads the same at this size
    d.text((s(x), s(y)), t, font=font, fill=fill, anchor=anchor)


def fit(t, name, size, maxw, minsize=6):
    while size > minsize and tw(t, F(name, size)) > maxw:
        size -= 0.5
    return F(name, size)


def wrap(t, font, maxw):
    words, lines, cur = t.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(trial, font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap_fit(t, name, size, maxw, maxlines, minsize=7):
    while True:
        f = F(name, size)
        ls = wrap(t, f, maxw)
        if len(ls) <= maxlines or size <= minsize:
            return f, ls
        size -= 0.5


def tag(x, y, label, size=7.5, right=False):
    col = S.LABELS[label]
    f = F("NotoSans-Bold.ttf", size)
    w = tw(label, f) + 8
    h = size + 6
    if right:
        x = x - w
    rect(x, y, x + w, y + h, fill=col, r=2.5)
    text(x + w / 2, y + h / 2 + 0.3, label, f, fill=(255, 255, 255), anchor="mm")
    return w


# ---------------------------------------------------------------- scenes
# each scene paints inside (x, y, w, h); simple flat shapes, drawn here from scratch

def sc_chip(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(20, 40, 30))
    cx, cy = x + w * 0.36, y + h * 0.55
    for k in range(-3, 4):
        line([(cx - 22, cy + k * 5), (cx - 28, cy + k * 5)], (180, 190, 160), 1.4)
        line([(cx + 22, cy + k * 5), (cx + 28, cy + k * 5)], (180, 190, 160), 1.4)
    rect(cx - 20, cy - 20, cx + 20, cy + 20, fill=(118, 185, 0), r=3)
    rect(cx - 14, cy - 14, cx + 14, cy + 14, fill=(30, 50, 20), r=2)
    text(cx, cy, "CEO", F("NotoSans-Bold.ttf", 9), fill=(170, 230, 60), anchor="mm")
    ax = x + w * 0.72
    rect(ax - 5, y + 24, ax + 5, y + h - 6, fill=(118, 185, 0))
    poly([(ax - 14, y + 26), (ax, y + 8), (ax + 14, y + 26)], fill=(118, 185, 0))
    text(ax + 20, y + 20, "+31%", F("NotoSans-Black.ttf", 15), fill=(255, 255, 255))


def sc_bull(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 244, 236))
    vals = [30, 26, 22, 18, 14, 16, 44]
    bw = (w * 0.55) / len(vals)
    for i, v in enumerate(vals):
        bx = x + 10 + i * bw
        col = (200, 60, 50) if i < 5 else (30, 150, 80)
        top = y + h - 8 - v
        rect(bx, top, bx + bw - 3, y + h - 8, fill=col)
    line([(x + 6, y + h - 8), (x + w - 6, y + h - 8)], (120, 130, 120), 1)
    text(x + w - 8, y + 8, "S&P +4.73%", F("NotoSans-Black.ttf", 12), fill=(20, 110, 60), anchor="ra")
    text(x + w - 8, y + 24, "NASDAQ +6.51%", F("NotoSans-Bold.ttf", 9.5), fill=(20, 110, 60), anchor="ra")


def sc_eu(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(0, 51, 153))
    import math
    cx, cy, r = x + w * 0.3, y + h / 2, h * 0.32
    for i in range(12):
        a = i * math.pi / 6
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        pts = []
        for j in range(10):
            rr = 3.4 if j % 2 == 0 else 1.4
            b = -math.pi / 2 + j * math.pi / 5
            pts.append((sx + rr * math.cos(b), sy + rr * math.sin(b)))
        poly(pts, fill=(255, 204, 0))
    px = x + w * 0.58
    rect(px, y + 8, px + 62, y + h - 4, fill=(255, 255, 255))
    text(px + 31, y + 14, "22nd", F("NotoSerif-Bold.ttf", 13), fill=(0, 51, 153), anchor="ma")
    text(px + 31, y + 30, "PACKAGE", F("NotoSans-Bold.ttf", 7), fill=(0, 51, 153), anchor="ma")
    for k in range(3):
        line([(px + 8, y + 42 + k * 5), (px + 54, y + 42 + k * 5)], (170, 180, 200), 1.4)


def sc_ship(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(40, 50, 78))
    rect(x, y + h * 0.62, x + w, y + h, fill=(32, 70, 110))
    cx = x + w * 0.42
    base = y + h * 0.66
    poly([(cx - 46, base - 12), (cx + 46, base - 4), (cx + 36, base + 6), (cx - 40, base - 2)], fill=(110, 116, 126))
    rect(cx - 12, base - 26, cx + 8, base - 10, fill=(130, 136, 146))
    line([(cx - 2, base - 26), (cx - 2, base - 38)], (130, 136, 146), 2)
    for (fx, fy, r, c) in [(cx + 10, base - 22, 11, (240, 120, 30)), (cx + 4, base - 30, 8, (250, 180, 50)),
                           (cx + 20, base - 30, 6, (250, 210, 90))]:
        circle(fx, fy, r, fill=c)
    for k in range(4):
        wx = x + 8 + k * 26
        line([(wx, y + h - 8), (wx + 8, y + h - 12), (wx + 16, y + h - 8)], (110, 160, 200), 1.4)
    dx = x + w * 0.82
    poly([(dx - 14, base + 6), (dx + 8, base + 2), (dx + 4, base + 8), (dx - 14, base + 9)], fill=(230, 230, 230))
    line([(dx - 30, base + 8), (dx - 16, base + 7)], (200, 220, 240), 1)


def sc_down(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(250, 236, 234))
    pts = [(x + 8, y + 12), (x + 30, y + 18), (x + 48, y + 14), (x + 70, y + 30), (x + 90, y + 26),
           (x + 112, y + 44), (x + 130, y + h - 8)]
    line(pts, (200, 40, 40), 2.6)
    text(x + w - 10, y + 8, "KOSPI", F("NotoSans-Bold.ttf", 9), fill=(150, 40, 40), anchor="ra")
    text(x + w - 10, y + 20, "\u22123.31%", F("NotoSans-Black.ttf", 15), fill=(200, 30, 30), anchor="ra")
    bx = x + w * 0.34
    rect(bx, y + h - 20, bx + 42, y + h - 6, fill=(60, 60, 70), r=2)
    text(bx + 21, y + h - 13, "HALT 5m", F("NotoSans-Bold.ttf", 7), fill=(255, 255, 255), anchor="mm")


def sc_nato(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(14, 40, 92))
    import math
    cx, cy = x + w * 0.3, y + h / 2
    circle(cx, cy, 18, outline=(255, 255, 255), width=1.6)
    for i in range(4):
        a = i * math.pi / 2
        poly([(cx, cy), (cx + 26 * math.cos(a), cy + 26 * math.sin(a)),
              (cx + 6 * math.cos(a + 0.8), cy + 6 * math.sin(a + 0.8))], fill=(255, 255, 255))
    tx = x + w * 0.56
    rect(tx, y + h * 0.55, tx + 80, y + h * 0.55 + 6, fill=(210, 190, 150), r=2)
    for k in range(5):
        circle(tx + 8 + k * 16, y + h * 0.42, 5, fill=(230, 230, 236))
    text(tx + 40, y + 6, "POLAND ASKED", F("NotoSans-Bold.ttf", 7.5), fill=(200, 210, 240), anchor="ma")


def sc_well(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(236, 224, 204))
    rect(x, y + h - 14, x + w, y + h, fill=(200, 184, 158))
    wx = x + w * 0.3
    rect(wx - 16, y + h - 34, wx + 16, y + h - 14, fill=(150, 150, 156))
    rect(wx - 20, y + h - 38, wx + 20, y + h - 34, fill=(110, 110, 118))
    line([(wx - 14, y + h - 38), (wx - 14, y + 10)], (90, 90, 96), 2)
    line([(wx + 14, y + h - 38), (wx + 14, y + 10)], (90, 90, 96), 2)
    rect(wx - 20, y + 6, wx + 20, y + 12, fill=(90, 90, 96))
    rect(wx + 36, y + 14, wx + 74, y + 34, fill=(0, 158, 219), r=3)
    text(wx + 55, y + 24, "UNRWA", F("NotoSans-Bold.ttf", 7.5), fill=(255, 255, 255), anchor="mm")
    for (rx, ry, rr) in [(x + w - 40, y + h - 18, 9), (x + w - 26, y + h - 16, 7), (x + w - 52, y + h - 15, 6)]:
        circle(rx, ry, rr, fill=(160, 140, 116))


def sc_himalaya(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(214, 232, 246))
    poly([(x, y + h), (x + 40, y + 16), (x + 70, y + 40), (x + 104, y + 8), (x + 150, y + h)], fill=(120, 136, 160))
    poly([(x + 34, y + 26), (x + 40, y + 16), (x + 47, y + 26)], fill=(255, 255, 255))
    poly([(x + 96, y + 18), (x + 104, y + 8), (x + 112, y + 18)], fill=(255, 255, 255))
    rect(x, y + h - 10, x + w, y + h, fill=(90, 150, 200))
    cx = x + w * 0.78
    for k in range(4):
        d.ellipse([s(cx - 16), s(y + h - 18 - k * 6), s(cx + 16), s(y + h - 10 - k * 6)],
                  fill=(232, 182, 40), outline=(170, 120, 20), width=s(1))
    text(cx, y + 6, "$1.62bn", F("NotoSans-Black.ttf", 11), fill=(30, 60, 100), anchor="ma")


def sc_dome(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(232, 240, 230))
    bx = x + w * 0.36
    rect(bx - 44, y + h - 22, bx + 44, y + h - 8, fill=(70, 120, 90))
    d.chord([s(bx - 26), s(y + h - 52), s(bx + 26), s(y + h - 8)], 180, 360, fill=(46, 140, 100))
    d.chord([s(bx - 26 + 26), s(y + h - 52), s(bx + 26 + 26), s(y + h - 8)], 180, 360, fill=(46, 140, 100))
    rect(bx - 50, y + h - 8, bx + 60, y + h - 4, fill=(120, 120, 120))
    for i, nm in enumerate(["1", "2"]):
        cx = x + w * 0.74 + i * 26
        rect(cx - 10, y + 12 + i * 6, cx + 10, y + 40 + i * 6, fill=(255, 255, 255), outline=(150, 40, 40), width=1)
        text(cx, y + 26 + i * 6, nm, F("NotoSans-Bold.ttf", 10), fill=(150, 40, 40), anchor="mm")
    text(x + w * 0.36, y + 6, "MPR", F("NotoSans-Bold.ttf", 9), fill=(40, 90, 60), anchor="ma")


def sc_drone(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(34, 32, 52))
    for k in range(5):
        circle(x + 14 + k * 33, y + 8 + (k % 2) * 6, 0.9, fill=(220, 220, 240))
    bx = x + w * 0.62
    rect(bx - 30, y + h - 30, bx + 30, y + h - 4, fill=(70, 90, 120))
    rect(bx - 30, y + h - 34, bx + 30, y + h - 30, fill=(40, 60, 90))
    for k in range(3):
        rect(bx - 24 + k * 18, y + h - 24, bx - 16 + k * 18, y + h - 16, fill=(240, 220, 120))
    dx, dy = x + w * 0.25, y + 22
    line([(dx - 14, dy), (dx + 14, dy)], (200, 200, 210), 2)
    rect(dx - 5, dy - 3, dx + 5, dy + 4, fill=(200, 200, 210))
    for ox in (-14, 14):
        line([(dx + ox - 6, dy - 3), (dx + ox + 6, dy - 3)], (230, 230, 240), 1.4)
    circle(bx + 22, y + h - 36, 7, fill=(250, 150, 40))
    circle(bx + 26, y + h - 40, 4, fill=(250, 210, 90))


def sc_podium(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(222, 238, 246))
    gx, gy = x + w * 0.7, y + h / 2
    circle(gx, gy, 20, fill=(70, 140, 200))
    d.arc([s(gx - 20), s(gy - 9), s(gx + 20), s(gy + 9)], 0, 360, fill=(220, 240, 255), width=s(1))
    line([(gx, gy - 20), (gx, gy + 20)], (220, 240, 255), 1)
    text(gx, gy, "AI", F("NotoSans-Black.ttf", 12), fill=(255, 255, 255), anchor="mm")
    px = x + w * 0.3
    poly([(px - 18, y + h - 4), (px - 12, y + 24), (px + 12, y + 24), (px + 18, y + h - 4)], fill=(50, 90, 140))
    circle(px, y + 15, 6, fill=(70, 70, 80))
    rect(px - 8, y + 21, px + 8, y + 24, fill=(70, 70, 80))
    text(px, y + 36, "UN", F("NotoSans-Bold.ttf", 8), fill=(255, 255, 255), anchor="mm")


SCENES = {"chip": sc_chip, "bull": sc_bull, "eu": sc_eu, "ship": sc_ship, "down": sc_down, "nato": sc_nato,
          "well": sc_well, "himalaya": sc_himalaya, "dome": sc_dome, "drone": sc_drone, "podium": sc_podium}


# ---------------------------------------------------------------- page

# top strip
rect(0, 0, W, 22, fill=NAVY)
text(10, 11, "THE WORLD ON ONE PAGE", F("NotoSans-Bold.ttf", 10.5), fill=(255, 255, 255), anchor="lm")
n_stories = len(S.CARDS) + len(S.BRIEFS)
text(W - 10, 11, f"{n_stories} STORIES \u00b7 7 REGIONS \u00b7 ALL FROM MONDAY 23 NOVEMBER 2026",
     F("NotoSans-Bold.ttf", 10.5), fill=AMBER, anchor="rm")

# the date, as large as it fits
df = fit(S.DAY, "NotoSerifDisplay-ExtraBold.ttf", 100, 1004)
text(W / 2, 64, S.DAY, df, fill=INK, anchor="mm")

kf = fit(S.KICKER, "NotoSerif-BoldItalic.ttf", 19, 1004)
text(W / 2, 118, S.KICKER, kf, fill=RED, anchor="mm")

# region chips with counts
counts = {}
for c in S.CARDS:
    counts[c[2]] = counts.get(c[2], 0) + 1
for b in S.BRIEFS:
    counts[b[1]] = counts.get(b[1], 0) + 1
cf = F("NotoSans-Bold.ttf", 9.5)
chips = [(S.REGIONS[k][0] + f" {counts.get(k, 0)}", S.REGIONS[k][1]) for k in S.REGIONS]
total_w = sum(tw(t, cf) + 14 for t, _ in chips) + 6 * (len(chips) - 1)
cx = (W - total_w) / 2
for t, col in chips:
    wdt = tw(t, cf) + 14
    rect(cx, 133, cx + wdt, 151, fill=col, r=3)
    text(cx + wdt / 2, 142, t, cf, fill=(255, 255, 255), anchor="mm")
    cx += wdt + 6

# UTC timeline
rect(10, 157, W - 10, 181, fill=NAVY, r=4)
rect(14, 160, 46, 178, fill=RED, r=3)
text(30, 169, "UTC", F("NotoSans-Bold.ttf", 9.5), fill=(255, 255, 255), anchor="mm")
tf_t = F("NotoSans-Bold.ttf", 9.5)
tf_x = F("NotoSans-SemiCondensed.ttf", 9.5)
seg = (W - 10 - 52) / len(S.TIMELINE)
for i, (hh, what) in enumerate(S.TIMELINE):
    x0 = 52 + i * seg
    if i:
        circle(x0 - 3, 169, 1.6, fill=(150, 160, 190))
    text(x0 + 2, 169, hh, tf_t, fill=AMBER, anchor="lm")
    wf = fit(what, "NotoSans-SemiCondensed.ttf", 9.5, seg - tw(hh, tf_t) - 10)
    text(x0 + 6 + tw(hh, tf_t), 169, what, wf, fill=(236, 238, 245), anchor="lm")

# card grid
GX, GY, CW, CH, GAP = 10, 187, 245, 160, 8.6
slots = []
for r in range(3):
    for c in range(4):
        if r == 0 and c == 3:
            continue
        slots.append((GX + c * (CW + GAP), GY + r * (CH + 9)))


def draw_card(card, x, y):
    no, place, reg, field, head, ctx, src, label, scene, _, _ = card
    rect(x + 1.5, y + 2, x + CW + 1.5, y + CH + 2, fill=(226, 220, 206), r=4)
    rect(x, y, x + CW, y + CH, fill=CARD, outline=LINE, width=1, r=4)
    ih = 56
    # illustration
    tmp_top = (x + 1, y + 1)
    SCENES[scene](x + 1, y + 1, CW - 2, ih)
    rcol = S.REGIONS[reg][1]
    rect(x, y, x + CW, y + 3, fill=rcol)
    # number + place pill
    pf = F("NotoSans-Bold.ttf", 8.5)
    pw = tw(place, pf) + 28
    rect(x + 5, y + 6, x + 5 + pw, y + 21, fill=(255, 255, 255), r=7)
    circle(x + 13, y + 13.5, 6.5, fill=INK)
    text(x + 13, y + 13.8, str(no), F("NotoSans-Bold.ttf", 8), fill=(255, 255, 255), anchor="mm")
    text(x + 23, y + 13.8, place, pf, fill=INK, anchor="lm")
    tag(x + CW - 5, y + ih - 13, label, right=True)
    # region . field
    rf = F("NotoSans-Bold.ttf", 8.5)
    text(x + 7, y + ih + 6, f"{S.REGIONS[reg][0]} \u00b7 {field}", rf, fill=rcol)
    # headline
    hf, hl = wrap_fit(head, "NotoSerif-SemiCondensedBold.ttf", 17, CW - 14, 2, 12)
    hy = y + ih + 18
    for ln in hl:
        text(x + 7, hy, ln, hf, fill=INK)
        hy += hf.size / K * 1.15
    # context
    cf2, cl = wrap_fit(ctx, "NotoSans-SemiCondensed.ttf", 10.5, CW - 14, 3, 8.5)
    cy = hy + 3
    for ln in cl:
        text(x + 7, cy, ln, cf2, fill=(52, 56, 66))
        cy += cf2.size / K * 1.2
    text(x + 7, y + CH - 6, src, F("NotoSans-SemiCondensed.ttf", 8), fill=MUTED, anchor="ls")


for card, (x, y) in zip(S.CARDS, slots):
    draw_card(card, x, y)

# the day in numbers (row 1, column 4)
nx, ny = GX + 3 * (CW + GAP), GY
rect(nx, ny, nx + CW, ny + CH, fill=NAVY, r=4)
text(nx + 9, ny + 8, "THE DAY IN NUMBERS", F("NotoSans-Bold.ttf", 10), fill=(255, 255, 255))
line([(nx + 9, ny + 23), (nx + CW - 9, ny + 23)], (70, 86, 120), 1)
yy = ny + 27
for big, cap in S.NUMBERS:
    bf = F("NotoSerif-Bold.ttf", 16)
    text(nx + 9, yy, big, bf, fill=AMBER)
    text(nx + 9 + tw(big, bf) + 7, yy + 6, cap, fit(cap, "NotoSans-SemiCondensed.ttf", 9.5, CW - 30 - tw(big, bf)),
         fill=(214, 222, 238))
    yy += 26

# ---------------------------------------------------------------- also on Monday
AY = GY + 3 * CH + 2 * 9 + 9        # 714
AX1 = 10
AW = 676
text(AX1, AY, "ALSO ON MONDAY 23 NOVEMBER", F("NotoSans-Black.ttf", 12), fill=INK)
lx = AX1 + AW
for lab in ["ONGOING", "CLAIM", "REPORTED", "OFFICIAL", "CONFIRMED"]:
    lx -= tag(lx, AY + 1, lab, size=7, right=True) + 4
line([(AX1, AY + 18), (AX1 + AW, AY + 18)], INK, 1.2)
half = (len(S.BRIEFS) + 1) // 2
colw = (AW - 10) / 2
rowh = 17.6
for i, (no, reg, head, where, label, _, _) in enumerate(S.BRIEFS):
    col = 0 if i < half else 1
    row = i if i < half else i - half
    bx = AX1 + col * (colw + 10)
    by = AY + 23 + row * rowh
    rcol = S.REGIONS[reg][1]
    text(bx, by + 7, str(no), F("NotoSans-Black.ttf", 10.5), fill=rcol, anchor="lm")
    lw = tw(label, F("NotoSans-Bold.ttf", 6.5)) + 8
    hf = fit(head, "NotoSans-SemiCondensedBold.ttf", 10.8, colw - 22 - lw - 4)
    text(bx + 18, by + 7, head, hf, fill=INK, anchor="lm")
    tag(bx + colw, by + 1.5, label, size=6.5, right=True)
    text(bx + 18, by + 15.5, where, F("NotoSans-SemiCondensed.ttf", 7.8), fill=MUTED, anchor="lm")

# ---------------------------------------------------------------- map
MX0, MY0, MX1, MY1 = 696, AY - 2, 1014, AY + 236
rect(MX0, MY0, MX1, MY1, fill=(236, 242, 247), outline=LINE, width=1, r=4)
text(MX0 + 8, MY0 + 6, "WHERE IT HAPPENED", F("NotoSans-Black.ttf", 10.5), fill=INK)
text(MX1 - 8, MY0 + 8, "numbers = cards \u00b7 dots = briefs", F("NotoSans-SemiCondensed.ttf", 7.5), fill=MUTED, anchor="ra")
LON0, LON1, LAT0, LAT1 = -132.0, 182.0, 74.0, -48.0
mx, my, mw = MX0 + 6, MY0 + 26, MX1 - MX0 - 12
mscale = mw / (LON1 - LON0)
mh = (LAT0 - LAT1) * mscale


def P(lon, lat):
    return (mx + (lon - LON0) * mscale, my + (LAT0 - lat) * mscale)


LAND = [
    [(-168, 66), (-160, 71), (-140, 70), (-120, 74), (-95, 72), (-80, 73), (-62, 66), (-55, 52), (-66, 45),
     (-75, 38), (-81, 31), (-80, 25), (-83, 29), (-90, 30), (-97, 26), (-97, 21), (-92, 18), (-87, 21), (-88, 15),
     (-83, 10), (-79, 8), (-82, 8), (-86, 12), (-92, 14), (-105, 20), (-110, 24), (-114, 31), (-117, 33),
     (-122, 37), (-124, 42), (-124, 48), (-131, 55), (-140, 60), (-150, 60), (-158, 57), (-165, 60)],
    [(-55, 60), (-45, 60), (-20, 70), (-18, 78), (-30, 83), (-60, 82), (-70, 77), (-55, 70)],
    [(-79, 8), (-72, 12), (-62, 10), (-52, 5), (-35, -5), (-38, -13), (-40, -22), (-48, -27), (-58, -35),
     (-62, -40), (-65, -45), (-68, -52), (-72, -53), (-75, -45), (-73, -35), (-71, -18), (-76, -14), (-81, -5),
     (-80, 1), (-78, 7)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (2, 51), (8, 54), (10, 57), (5, 62), (15, 69), (25, 71), (40, 68),
     (60, 70), (80, 73), (100, 77), (115, 73), (140, 72), (160, 70), (180, 68), (180, 62), (165, 60), (160, 55),
     (142, 59), (135, 54), (141, 47), (132, 43), (129, 35), (126, 38), (122, 40), (120, 32), (122, 28), (117, 23),
     (108, 21), (106, 17), (109, 12), (104, 9), (100, 13), (100, 7), (103, 1), (98, 8), (97, 16), (92, 21),
     (87, 21), (80, 15), (77, 8), (72, 20), (67, 24), (57, 25), (56, 27), (50, 30), (51, 25), (56, 24), (59, 22),
     (55, 17), (52, 16), (43, 12), (39, 21), (34, 28), (32, 31), (35, 36), (28, 37), (26, 40), (23, 36),
     (21, 40), (19, 42), (13, 45), (16, 41), (12, 38), (9, 44), (3, 43), (0, 39), (-6, 37)],
    [(-17, 21), (-16, 12), (-12, 7), (-5, 5), (5, 5), (9, 4), (10, -2), (13, -8), (12, -17), (15, -27), (18, -34),
     (25, -34), (32, -28), (35, -22), (40, -15), (40, -10), (39, -5), (42, 0), (51, 11), (43, 12), (37, 19),
     (34, 28), (32, 31), (25, 32), (20, 31), (10, 33), (11, 37), (0, 36), (-6, 36), (-10, 30), (-13, 27)],
    [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (151, -34), (146, -39),
     (138, -35), (132, -32), (124, -34), (115, -34), (113, -26)],
    [(-5, 50), (1, 51), (0, 53), (-2, 56), (-3, 58), (-6, 57), (-5, 54)],
    [(130, 31), (135, 34), (140, 36), (142, 40), (141, 45), (140, 42), (136, 36), (131, 34)],
    [(95, 5), (98, 4), (104, -2), (106, -6), (102, -4)],
    [(105, -6), (115, -8), (114, -9), (106, -7)],
    [(109, 1), (113, 4), (119, 6), (118, 1), (116, -4), (110, -3)],
    [(131, -1), (141, -3), (150, -6), (147, -10), (141, -9), (137, -5)],
    [(172, -34), (178, -38), (175, -42), (168, -47), (166, -45), (173, -40)],
    [(44, -25), (47, -25), (50, -15), (49, -12), (44, -17)],
    [(120, 18), (122, 18), (126, 7), (122, 7)],
]
rect(mx, my, mx + mw, my + mh, fill=SKY)
_before = img.copy()
for shape in LAND:
    poly([P(lo, la) for lo, la in shape], fill=(204, 198, 182), outline=(176, 168, 150), width=0.6)
_mask = Image.new("L", img.size, 0)
ImageDraw.Draw(_mask).rectangle([s(mx), s(my), s(mx + mw), s(my + mh)], fill=255)
img = Image.composite(img, _before, _mask)
d = ImageDraw.Draw(img)

for no, reg, _, _, _, lo, la in S.BRIEFS:
    if lo is None:
        continue
    px, py = P(lo, la)
    circle(px, py, 2.3, fill=S.REGIONS[reg][1], outline=(255, 255, 255), width=0.6)

offsets = {3: (-9, -8), 6: (9, -8), 7: (5, 9), 4: (-4, 10)}
for card in S.CARDS:
    no, reg, lo, la = card[0], card[2], card[9], card[10]
    px, py = P(lo, la)
    ox, oy = offsets.get(no, (0, -8))
    qx, qy = px + ox, py + oy
    line([(px, py), (qx, qy)], INK, 0.8)
    circle(px, py, 1.6, fill=INK)
    circle(qx, qy, 6.2, fill=S.REGIONS[reg][1], outline=(255, 255, 255), width=1)
    text(qx, qy + 0.3, str(no), F("NotoSans-Bold.ttf", 7.5), fill=(255, 255, 255), anchor="mm")

# label legend under the map
ly = my + mh + 8
text(MX0 + 8, ly, "HOW SURE EACH STORY IS", F("NotoSans-Bold.ttf", 8), fill=INK)
expl = [("CONFIRMED", "several outlets or official data"), ("OFFICIAL", "government / agency statement"),
        ("REPORTED", "carried by a news wire"), ("CLAIM", "one side's account, unconfirmed"),
        ("ONGOING", "Monday update to an earlier event")]
for i, (lab, ex) in enumerate(expl):
    yy = ly + 13 + i * 13.2
    wl = tag(MX0 + 8, yy, lab, size=6.5)
    text(MX0 + 74, yy + 6.2, ex, F("NotoSans-SemiCondensed.ttf", 8.2), fill=(52, 56, 66), anchor="lm")

# ---------------------------------------------------------------- date check
DY = MY1 + 7
rect(10, DY, W - 10, DY + 58, fill=(255, 250, 246), outline=RED, width=1.4, r=4)
rect(16, DY + 6, 104, DY + 22, fill=RED, r=3)
text(60, DY + 14, "DATE CHECK", F("NotoSans-Black.ttf", 9.5), fill=(255, 255, 255), anchor="mm")
text(112, DY + 14, "Every story on this page happened, or was first reported, on Monday 23 November 2026 (any time zone).",
     fit("Every story on this page happened, or was first reported, on Monday 23 November 2026 (any time zone).",
         "NotoSans-Bold.ttf", 11, W - 10 - 120), fill=INK, anchor="lm")
text(16, DY + 33, "Left out because it happened on an earlier day:", F("NotoSans-Bold.ttf", 9), fill=RED, anchor="lm")
parts = [f"{a} \u2014 {b}" for a, b in S.LEFT_OUT]
lf = F("NotoSans-SemiCondensed.ttf", 9)
row_y = DY + 33
xcur = 16 + tw("Left out because it happened on an earlier day:", F("NotoSans-Bold.ttf", 9)) + 8
for p in parts:
    a, b = p.split(" \u2014 ")
    wa = tw(a + "  ", lf) + tw(b, F("NotoSans-Bold.ttf", 9)) + 14
    if xcur + wa > W - 16:
        row_y += 14
        xcur = 16
    text(xcur, row_y, a, lf, fill=INK, anchor="lm")
    text(xcur + tw(a + "  ", lf), row_y, b, F("NotoSans-Bold.ttf", 9), fill=RED, anchor="lm")
    xcur += wa

# footer
text(W / 2, H - 8, "Times are UTC. Scenes are drawn illustrations, not photographs. "
     "Figures as reported on the day; market closes are New York 21:00 UTC unless stated.",
     F("NotoSans-SemiCondensed.ttf", 8.2), fill=MUTED, anchor="mm")

out = img.resize((W, H), Image.LANCZOS)
here = os.path.dirname(os.path.abspath(__file__))
out.save(os.path.join(here, "entry.png"), optimize=True)
print("entry.png", os.path.getsize(os.path.join(here, "entry.png")), "bytes")
