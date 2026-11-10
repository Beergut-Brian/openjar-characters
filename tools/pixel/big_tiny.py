"""Big Tiny's pixel form for The Hill (Pillow only, drawn in code).

big_tiny(view="front")       front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

32 px tall with the outline (1.3 m body, fills the frame): beanie 3 rows (perched on the crown, rows overlap the
head top), head 11, belly 10, pants 4, sneakers 3. The widest Jarling: the belly is 24 px across in the front form
(head 12 px), 21 px in the frames. Tiny navy beanie, 4 px wide: a light pom pixel pair, a navy row and a light cuff
row, with brown buzz hair either side. Eyes are closed happy arcs in every frame.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#D99E6E", "#B97F55"
HAIR = "#4A2F23"
BEANIE, BEANIE_L = "#2E3A66", "#46558C"
TEE, TEE_D = "#7EC8F2", "#5FA9D6"
PANTS, PANTS_D = "#80848C", "#6A6E76"
SHOE, SOLE = "#F7F7F5", "#B9BDC4"
MOUTH = "#6A2232"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# Big Tiny fills the frame top to bottom, so the jump tucks the feet instead of lifting the body.
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

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs 3 px, sneakers 7 px
LEGS = {
    "stand": ((10, 9, 30), (16, 16, 30)),
    "contact": ((10, 6, 30), (16, 19, 30)),
    "pass": ((11, 9, 28), (15, 14, 30)),
    "contact2": ((10, 13, 30), (16, 10, 30)),
    "pass2": ((10, 10, 30), (16, 15, 28)),
    "tuck": ((10, 9, 28), (16, 16, 28)),
    "dangle": ((10, 9, 30), (16, 16, 30)),
    "crouch": ((10, 6, 30), (16, 19, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the hip (row `top`) to the sole (row fy): grey pants, an enormous white sneaker, toe right."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 6, y, SOLE)
        elif y == fy - 1:
            s.r(x, y, x + 6, y, SHOE)
            if back:
                s.px(SOLE, (x, y), (x + 1, y))
        elif y == fy - 2:
            s.r(x, y, x + 4, y, SHOE)
            s.px(SOLE, (x, y))
        else:
            s.r(x, y, x + 2, y, PANTS_D if back else PANTS)


def _beanie(s, x, y):
    """Tiny beanie 4 px wide, top-left at (x, y): 2 px light pom, navy crown row, light cuff row."""
    s.px(BEANIE_L, (x + 1, y), (x + 2, y))
    s.r(x, y + 1, x + 3, y + 1, BEANIE)
    s.r(x, y + 2, x + 3, y + 2, BEANIE_L)


def _belly(s, rows, shade_rows=2):
    """rows: [(y, x0, x1)], top to bottom; the last `shade_rows` rows are the shaded belly underside."""
    for i, (y, a, b) in enumerate(rows):
        s.r(a, y, b, y, TEE_D if i >= len(rows) - shade_rows else TEE)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 24 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm (behind the belly), legs, pants
    for x, y in _line(6, 16 + oy, 3 + bax, 21 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(5, 15 + oy, 7, 16 + oy, TEE_D)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(9, hip, 21, hip, PANTS_D); s.r(10, hip + 1, 20, hip + 1, PANTS)
    # belly, bulging forward (right)
    _belly(s, [(14 + oy, 11, 20), (15 + oy, 8, 22), (16 + oy, 7, 24), (17 + oy, 6, 25), (18 + oy, 6, 26),
               (19 + oy, 6, 26), (20 + oy, 6, 26), (21 + oy, 6, 25), (22 + oy, 7, 24), (23 + oy, 9, 22)])
    s.px(TEE_D, (6, 19 + oy), (6, 20 + oy), (6, 21 + oy), (7, 21 + oy))
    # head (three-quarter, face to the right), buzz hair, beanie on the crown
    hx, hy = hdx, oy
    s.r(12 + hx, 3 + hy, 19 + hx, 3 + hy, HAIR)
    s.r(11 + hx, 4 + hy, 20 + hx, 4 + hy, HAIR)
    s.r(10 + hx, 5 + hy, 21 + hx, 12 + hy, SKIN)
    s.r(11 + hx, 13 + hy, 20 + hx, 13 + hy, SKIN)
    s.r(10 + hx, 5 + hy, 21 + hx, 5 + hy, HAIR)
    s.r(10 + hx, 6 + hy, 13 + hx, 9 + hy, HAIR); s.px(HAIR, (14 + hx, 6 + hy), (10 + hx, 10 + hy), (11 + hx, 10 + hy))
    s.px(SKIN_D, (12 + hx, 10 + hy), (12 + hx, 11 + hy), (13 + hx, 11 + hy))       # ear
    _beanie(s, 14 + hx, 1 + hy)
    # closed happy eyes (^ ^), small smile
    for ex in (15, 19):
        s.px(OUT, (ex - 1 + hx, 9 + hy), (ex + hx, 8 + hy), (ex + 1 + hx, 9 + hy))
    s.px(SKIN_D, (21 + hx, 10 + hy))                                                # nose bump
    s.px(MOUTH, (17 + hx, 11 + hy), (18 + hx, 12 + hy), (19 + hx, 12 + hy), (20 + hx, 11 + hy))
    # front arm: sleeve, then skin to a mitten hand (in front of the belly)
    pts = _line(19, 15 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TEE if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def big_tiny(view="front"):
    s = Spr(jf.W, jf.H)
    # arms, hanging outside the belly (drawn first, the belly covers the shoulders)
    for sx, ax in ((7, 6), (31, 32)):
        s.r(sx, 16, sx + 1, 18, TEE); s.r(ax, 19, ax + 1, 22, SKIN); s.px(SKIN_D, (ax, 22), (ax + 1, 22))
    # pants, legs, sneakers
    s.r(12, 24, 27, 24, PANTS_D); s.r(13, 25, 26, 25, PANTS)
    for x in (13, 24):
        s.r(x, 26, x + 2, 27, PANTS)
    s.r(11, 28, 17, 29, SHOE); s.r(22, 28, 28, 29, SHOE)
    s.r(11, 30, 17, 30, SOLE); s.r(22, 30, 28, 30, SOLE)
    s.px(SOLE, (11, 28), (28, 28))
    # belly, 24 px across
    _belly(s, [(14, 14, 25), (15, 11, 28), (16, 10, 29), (17, 9, 30), (18, 8, 31), (19, 8, 31),
               (20, 8, 31), (21, 9, 30), (22, 10, 29), (23, 12, 27)])
    s.px(TEE_D, (8, 20), (31, 20), (9, 21), (30, 21))
    # head, 12 px wide
    s.r(16, 3, 23, 3, HAIR); s.r(15, 4, 24, 4, HAIR); s.r(14, 5, 25, 5, HAIR)
    s.r(14, 6, 25, 12, SKIN); s.r(15, 13, 24, 13, SKIN)
    s.r(14, 6, 15, 6, HAIR); s.r(24, 6, 25, 6, HAIR); s.px(HAIR, (14, 7), (25, 7))
    s.px(SKIN_D, (13, 9), (13, 10), (26, 9), (26, 10))                              # ears
    _beanie(s, 18, 1)
    for ex in (17, 22):
        s.px(OUT, (ex - 1, 9), (ex, 8), (ex + 1, 9))
    s.px(SKIN_D, (19, 10), (20, 10))
    s.px(MOUTH, (18, 11), (19, 12), (20, 12), (21, 11))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/big_tiny/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = big_tiny(), sheet()
    frames.save(f"{out}/big_tiny_frames.png")
    front.save(f"{out}/big_tiny_pixel.png")
    with open(f"{out}/big_tiny_frames.json", "w") as f:
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
    rev.save(f"{out}/big_tiny_pixel_sheet.png")
    print("wrote", out)
