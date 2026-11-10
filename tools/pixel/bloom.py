"""Bloom's pixel form for The Hill (Pillow only, drawn in code).

bloom(view="front")          front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

30 px tall with the outline (the 3D is 1.11 m with the hat, 29.5 px at true scale), traced from refs/jarling/bloom_side_sprite.png:
hat crown 3 rows (the last is the pink band), brim 2 rows (frames 20 px, front 18 px: 3-4 px past the widest body pixel each side, 1 px droop at the tips),
face 8 rows under the brim, tee 5, skirt 5, bare knees and shins 4 (one mud pixel on each knee), clogs 3.
The flower is a 2 x 2 patch on the band at the front of the brim: three periwinkle pixels and one yellow centre.
No watering can in the pixel frames.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#BF8150", "#9E6538"
HAIR = "#3A2418"
STRAW, STRAW_D = "#E3C27A", "#C2A15C"
BAND = "#F7A8CB"
PETAL, CENTRE = "#8E9BF0", "#FFD23F"
TOP, TOP_D = "#F7A8CB", "#D98BAE"
SKIRT, SKIRT_D = "#5B7FB8", "#48689A"
MUD = "#6B4A33"
CLOG, SOLE = "#8A4FC4", "#6B3A9C"
CHEEK = "#F4A3B4"
MOUTH = "#6A2232"
EYE_HI = "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop, hem sway
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21), 0, 0),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22), 1, 0),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21), 0, 1),
    "walk1": ("pass", 0, 0, (0, 0), (22, 20), 0, 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21), 0, -1),
    "walk3": ("pass2", 0, 0, (0, 0), (22, 20), 0, 0),
    "jump": ("tuck", 0, 0, (-1, -3), (23, 15), 0, 0),
    "fall": ("dangle", 0, 0, (-1, -4), (24, 14), 0, 0),
    "side0": ("stand", 0, -1, (0, 0), (18, 16), 0, 0),
    "side1": ("contact", 0, 1, (1, -1), (22, 19), 0, 1),
    "side2": ("stand", 0, 0, (0, 0), (21, 20), 0, 0),
    "down0": ("stand", 0, 0, (0, -1), (22, 11), 0, 0),
    "down1": ("crouch", 0, 1, (0, 0), (24, 18), 1, -1),
    "down2": ("stand", 0, 0, (0, 0), (23, 17), 0, 0),
}

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs 2 px wide, clog 4 px, toe right
LEGS = {
    "stand": ((12, 12, 30), (17, 17, 30)),
    "contact": ((12, 9, 30), (17, 20, 30)),
    "pass": ((13, 11, 28), (16, 16, 30)),
    "contact2": ((12, 15, 30), (17, 12, 30)),
    "pass2": ((12, 13, 30), (17, 16, 28)),
    "tuck": ((12, 11, 28), (17, 17, 28)),
    "dangle": ((12, 11, 30), (17, 17, 30)),
    "crouch": ((12, 9, 30), (17, 20, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from under the skirt (row `top`) to the clog sole (row fy): bare skin, mud pixel on the knee, purple clog."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 3, y, SOLE)
        elif y >= fy - 2:
            s.r(x, y, x + 3 if y == fy - 1 else x + 2, y, CLOG)
        else:
            s.r(x, y, x + 1, y, SKIN_D if back else SKIN)
            if y == top + 1:
                s.px(MUD, (x, y))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop, sway = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 24 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm (darker), legs, skirt
    for x, y in _line(11, 15 + oy, 10 + bax, 20 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(10, 14 + oy, 11, 15 + oy, TOP_D)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(11, hip - 5, 20, hip - 5, SKIRT)
    s.r(10, hip - 4, 21, hip - 4, SKIRT)
    s.r(9 + min(sway, 0), hip - 3, 22 + max(sway, 0), hip - 1, SKIRT)
    s.px(SKIRT_D, (9 + min(sway, 0), hip - 1), (10 + min(sway, 0), hip - 1), (21, hip - 1), (22 + max(sway, 0), hip - 1))
    # tee
    s.r(11, 14 + oy, 20, hip - 6, TOP)
    s.px(TOP_D, (11, hip - 6), (12, hip - 6))
    # head (three-quarter, face right) under the hat
    hx, hy = hdx, oy
    s.r(11 + hx, 6 + hy, 20 + hx, 12 + hy, SKIN)
    s.r(12 + hx, 13 + hy, 19 + hx, 13 + hy, SKIN)
    s.r(10 + hx, 5 + hy, 13 + hx, 10 + hy, HAIR); s.px(HAIR, (11 + hx, 11 + hy), (11 + hx, 12 + hy))   # bob at the back
    s.px(SKIN_D, (12 + hx, 10 + hy), (12 + hx, 11 + hy))                       # ear
    s.r(11 + hx, 6 + hy, 20 + hx, 6 + hy, HAIR)                                  # fringe under the brim
    # hat: crown rows 1-3 (3 = band), brim rows 4-5, 14 px wide
    s.r(14 + hx, 1 + hy, 18 + hx, 1 + hy, STRAW)
    s.r(12 + hx, 2 + hy, 20 + hx, 2 + hy, STRAW)
    s.r(12 + hx, 3 + hy, 20 + hx, 3 + hy, BAND)
    s.r(6 + hx, 4 + hy, 25 + hx, 4 + hy, STRAW)                                  # brim 20 px, 4 px past the skirt each side
    s.r(8 + hx, 5 + hy, 23 + hx, 5 + hy, STRAW_D)
    s.px(STRAW, (6 + hx, 5 + hy), (7 + hx, 5 + hy), (24 + hx, 5 + hy), (25 + hx, 5 + hy))   # downturned droop at the tips
    s.px(STRAW_D, (12 + hx, 2 + hy))
    s.px(PETAL, (19 + hx, 3 + hy), (20 + hx, 4 + hy), (19 + hx, 4 + hy)); s.px(CENTRE, (20 + hx, 3 + hy))
    # face
    if eyes_shut:
        s.px(OUT, (15 + hx, 9 + hy), (16 + hx, 8 + hy), (17 + hx, 9 + hy), (19 + hx, 9 + hy), (20 + hx, 8 + hy))
    else:
        s.r(15 + hx, 8 + hy, 16 + hx, 9 + hy, OUT); s.px(EYE_HI, (16 + hx, 8 + hy))
        s.px(OUT, (19 + hx, 8 + hy), (19 + hx, 9 + hy))
    s.px(CHEEK, (14 + hx, 10 + hy), (14 + hx, 11 + hy), (20 + hx, 11 + hy))
    s.px(MOUTH, (17 + hx, 12 + hy), (18 + hx, 12 + hy), (19 + hx, 11 + hy))
    # front arm: pink sleeve, then skin to a mitten hand
    pts = _line(19, 14 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TOP if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def bloom(view="front"):
    s = Spr(jf.W, jf.H)
    # arms
    for x in (14, 24):
        s.r(x, 14, x + 1, 15, TOP); s.r(x, 16, x + 1, 19, SKIN); s.px(SKIN_D, (x, 19), (x + 1, 19))
    # clogs and legs
    for x in (16, 22):
        s.r(x, 24, x + 1, 27, SKIN); s.px(MUD, (x, 25))
    s.r(15, 28, 18, 29, CLOG); s.r(21, 28, 24, 29, CLOG)
    s.r(15, 30, 18, 30, SOLE); s.r(21, 30, 24, 30, SOLE)
    # tee and skirt
    s.r(16, 14, 23, 18, TOP); s.px(TOP_D, (16, 18), (17, 18))
    s.r(16, 19, 23, 19, SKIRT); s.r(15, 20, 24, 20, SKIRT); s.r(14, 21, 25, 23, SKIRT)
    s.px(SKIRT_D, (14, 23), (15, 23), (24, 23), (25, 23))
    # head and bob
    s.r(15, 6, 24, 12, SKIN); s.r(16, 13, 23, 13, SKIN)
    s.r(14, 5, 14, 10, HAIR); s.r(25, 5, 25, 10, HAIR); s.r(15, 6, 24, 6, HAIR)
    # hat
    s.r(17, 1, 22, 1, STRAW); s.r(15, 2, 24, 2, STRAW); s.r(15, 3, 24, 3, BAND)
    s.r(11, 4, 28, 4, STRAW); s.r(13, 5, 26, 5, STRAW_D)
    s.px(STRAW, (11, 5), (12, 5), (27, 5), (28, 5))                              # downturned droop at the tips
    s.px(PETAL, (23, 3), (24, 4), (23, 4)); s.px(CENTRE, (24, 3))
    # face
    s.r(17, 8, 18, 9, OUT); s.r(21, 8, 22, 9, OUT); s.px(EYE_HI, (18, 8), (22, 8))
    s.px(CHEEK, (16, 10), (16, 11), (23, 10), (23, 11))
    s.px(MOUTH, (19, 12), (20, 12), (18, 11), (21, 11))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/bloom/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = bloom(), sheet()
    frames.save(f"{out}/bloom_frames.png")
    front.save(f"{out}/bloom_pixel.png")
    with open(f"{out}/bloom_frames.json", "w") as f:
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
    rev.save(f"{out}/bloom_pixel_sheet.png")
    print("wrote", out)
