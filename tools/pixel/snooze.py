"""Snooze's pixel form for The Hill (Pillow only, drawn in code).

snooze(view="front")         front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

32 px tall with the outline (the 3D is about 1.31 m with the nightcap, squeezed to the frame): nightcap 8 rows
(dome 7 + brim 1), face 7, torso 7, pants 5, slippers 3. Medium build; in the frames the head sits 1 px forward of
the torso (slouch). The cap flops to one side (viewer's right in the front form, toward the back = left in the
frames) and hangs down so the 3 x 3 pom-pom ends at ear/shoulder level. Eyes are always closed happy arcs.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#EFBB90", "#CF9A70"
HAIR = "#7A4B2A"
CAP, CAP_W = "#6F7FD8", "#F5F5F2"
TOP, TOP_D = "#A9D4F2", "#8CBAD9"
PANTS, PANTS_D = "#A9D4F2", "#8CBAD9"
STAR = "#FFFFFF"
SLIP, SOLE = "#FFD95A", "#D9B03A"
MOUTH = "#6A2232"
BLUSH = "#F4A9A0"

HAND = (22, 21)

POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21), 0),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22), 1),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21), 0),
    "walk1": ("pass", 0, 0, (0, 0), (22, 20), 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21), 0),
    "walk3": ("pass2", 0, 0, (0, 0), (22, 20), 0),
    "jump": ("tuck", 0, 0, (-1, -3), (23, 15), 0),
    "fall": ("dangle", 0, 0, (-1, -4), (24, 14), 0),
    "side0": ("stand", 0, -1, (0, 0), (18, 16), 0),
    "side1": ("contact", 0, 1, (1, -1), (22, 19), 0),
    "side2": ("stand", 0, 0, (0, 0), (21, 20), 0),
    "down0": ("stand", 0, 0, (0, -1), (22, 11), 0),
    "down1": ("crouch", 0, 1, (0, 0), (24, 18), 1),
    "down2": ("stand", 0, 0, (0, 0), (23, 17), 0),
}

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs are 3 px wide
LEGS = {
    "stand": ((12, 11, 30), (16, 16, 30)),
    "contact": ((12, 9, 30), (16, 19, 30)),
    "pass": ((13, 11, 28), (15, 15, 30)),
    "contact2": ((12, 15, 30), (16, 11, 30)),
    "pass2": ((12, 13, 30), (16, 15, 28)),
    "tuck": ((12, 11, 28), (16, 17, 28)),
    "dangle": ((12, 11, 30), (16, 17, 30)),
    "crouch": ((12, 9, 30), (16, 19, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """Pyjama leg from the hip (row `top`) to a rounded, slightly wide fuzzy slipper (toe to the right)."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 4, y, SOLE)
        elif y == fy - 1:
            s.r(x, y, x + 4, y, SLIP)
        elif y == fy - 2:
            s.r(x, y, x + 2, y, SLIP)
        else:
            s.r(x, y, x + 2, y, PANTS_D if back else PANTS)


def _stars(s, pts):
    """White star pixels, only where they land on pyjama cloth."""
    for x, y in pts:
        if s.im.getpixel((x, y))[:3] in (rgba(TOP)[:3], rgba(TOP_D)[:3]):
            s.px(STAR, (x, y))


def _cap(s, dome, tail, pom, rows=(1, 7)):
    """Striped nightcap. dome = (x0, x1) of the 5-row dome (rows 3-7), the top rows narrow; tail = list of (x, y)
    left cells of 2 px wide segments; pom = (x, y) top-left of the 3 x 3 pom-pom. Bands are 2 px."""
    x0, x1 = dome
    def col(x, y): return CAP_W if ((x + y) // 2) % 2 else CAP
    for y, a, b in ((1, x0 + 3, x1 - 3), (2, x0 + 1, x1 - 1)) + tuple((y, x0, x1) for y in range(3, 8)):
        for x in range(a, b + 1):
            s.px(col(x, y), (x, y))
    for x, y in tail:
        c = CAP_W if (y // 2) % 2 and y - tail[0][1] < 6 else CAP
        s.px(c, (x, y), (x + 1, y))
    s.r(pom[0], pom[1], pom[0] + 2, pom[1] + 2, CAP_W)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 23 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    for x, y in _line(11, 17 + oy, 10 + bax, 21 + oy + bay):
        s.r(x, y, x + 1, y + 1, TOP_D)
    s.px(SKIN_D, (10 + bax, 22 + oy + bay), (11 + bax, 22 + oy + bay))
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 19, hip, PANTS)
    s.r(12, 16 + oy, 19, hip - 1, TOP)
    _stars(s, [(13, 17 + oy), (17, 18 + oy), (14, 20 + oy), (18, 21 + oy), (12, 22 + oy), (13, hip + 1), (18, hip + 2), (14, hip + 3)])
    # head, 1 px forward of the torso (slouch)
    hx, hy = 1 + hdx, oy
    s.r(12 + hx, 9 + hy, 20 + hx, 14 + hy, SKIN)
    s.r(13 + hx, 15 + hy, 19 + hx, 15 + hy, SKIN)
    s.r(12 + hx, 9 + hy, 20 + hx, 9 + hy, HAIR); s.r(12 + hx, 10 + hy, 13 + hx, 12 + hy, HAIR); s.px(HAIR, (20 + hx, 10 + hy))
    s.px(SKIN_D, (14 + hx, 12 + hy), (14 + hx, 13 + hy))                              # ear
    # nightcap: brim, dome, tail flopping back (left), pom-pom at ear/shoulder level
    tail = [(10 + hx, 3 + hy), (9 + hx, 4 + hy), (8 + hx, 5 + hy), (8 + hx, 6 + hy), (8 + hx, 7 + hy), (8 + hx, 8 + hy),
            (8 + hx, 9 + hy), (8 + hx, 10 + hy), (8 + hx, 11 + hy)]
    _cap(s, (11 + hx, 20 + hx), tail, (7 + hx, 12 + hy))
    s.r(10 + hx, 8 + hy, 22 + hx, 8 + hy, CAP_W)
    s.px(CAP_W, (8 + hx, 8 + hy), (9 + hx, 8 + hy))
    # face: closed happy arcs (always), small smile, blush
    s.px(OUT, (15 + hx, 12 + hy), (16 + hx, 11 + hy), (17 + hx, 12 + hy), (19 + hx, 12 + hy), (20 + hx, 11 + hy), (21 + hx, 12 + hy))
    s.px(MOUTH, (18 + hx, 14 + hy), (19 + hx, 14 + hy), (20 + hx, 13 + hy))
    s.px(BLUSH, (16 + hx, 13 + hy))
    # front arm
    pts = _line(19, 16 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TOP if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def snooze(view="front"):
    s = Spr(jf.W, jf.H)
    for x in (14, 24):
        s.r(x, 16, x + 1, 17, TOP); s.r(x, 18, x + 1, 21, TOP); s.r(x, 21, x + 1, 21, SKIN)
        s.px(SKIN_D, (x, 21))
    s.r(16, 23, 23, 23, PANTS)
    for x in (16, 21):
        s.r(x, 24, x + 2, 27, PANTS)
    s.r(14, 28, 18, 29, SLIP); s.r(20, 28, 24, 29, SLIP)
    s.r(14, 30, 18, 30, SOLE); s.r(20, 30, 24, 30, SOLE)
    s.r(16, 16, 23, 22, TOP)
    _stars(s, [(17, 17), (21, 18), (18, 20), (22, 21), (16, 22), (15, 18), (24, 19), (17, 25), (22, 24), (22, 26), (18, 27)])
    s.r(15, 9, 24, 14, SKIN); s.r(16, 15, 23, 15, SKIN)
    s.r(15, 9, 24, 9, HAIR); s.r(15, 10, 16, 11, HAIR); s.r(23, 10, 24, 11, HAIR)
    tail = [(23, 2), (24, 3), (25, 4), (26, 5), (26, 6), (26, 7), (26, 8), (26, 9), (26, 10), (26, 11)]
    _cap(s, (15, 24), tail, (26, 12))
    s.r(14, 8, 25, 8, CAP_W)
    s.px(OUT, (17, 12), (18, 11), (19, 12), (21, 12), (22, 11), (23, 12))
    s.px(MOUTH, (19, 14), (20, 14), (18, 13), (21, 13))
    s.px(BLUSH, (16, 13), (23, 13))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/snooze/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = snooze(), sheet()
    frames.save(f"{out}/snooze_frames.png")
    front.save(f"{out}/snooze_pixel.png")
    with open(f"{out}/snooze_frames.json", "w") as f:
        json.dump(jf.manifest(HAND), f, indent=2); f.write("\n")
    sil = silhouette(front.crop(front.getbbox()))
    sil = sil.resize((max(1, round(sil.width * 16 / sil.height)), 16), Image.NEAREST)
    big, fs = up(front, 8), up(frames, 4)
    pad = 16
    W = pad * 4 + big.width + fs.width
    H = max(big.height + pad * 3 + front.height * 2 + sil.height * 4, fs.height) + pad * 2
    rev = Image.new("RGBA", (W, H), rgba("#F6EFE0"))
    rev.alpha_composite(big, (pad, pad))
    y = pad * 2 + big.height
    rev.alpha_composite(front, (pad, y)); rev.alpha_composite(up(front, 2), (pad * 2 + front.width, y))
    rev.alpha_composite(up(sil, 4), (pad * 4 + front.width * 3, y))
    rev.alpha_composite(fs, (pad * 3 + big.width, pad))
    rev.save(f"{out}/snooze_pixel_sheet.png")
    print("wrote", out)
