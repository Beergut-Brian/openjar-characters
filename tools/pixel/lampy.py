"""Lampy's pixel form for The Hill (Pillow only, drawn in code).

lampy(view="front")          front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

32 px tall with the outline (the 3D is 1.31 m with the helmet, 35 px at true scale, squeezed to the frame):
helmet dome 6 rows, brim 1, face 8, torso 7, pants 5, boots 3. Narrow 8 px torso, long legs.
The headlamp is a dark housing with a 2 x 2 pale-yellow lens on the helmet front (centre of the dome in the
front form, sticking 2 px out past the dome at the right in the frames). The smudge is one pixel on the outer
cheek, 3 px from the mouth.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#EFBB90", "#CF9A70"
HAIR = "#7A4B2A"
HELM, HELM_D = "#F1F1EC", "#CFCFC8"
LAMP, LENS = "#3A3A46", "#FFE9A8"
SMUDGE = "#6B5A4A"
TOP, BIB = "#3F8A99", "#35778A"
PANTS, PANTS_D = "#7A5536", "#5E4129"
BOOT, SOLE = "#7B7F86", "#4A4D55"
MOUTH = "#6A2232"
EYE_HI = "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# Lampy fills the frame top to bottom, so the jump tucks the feet instead of lifting the body.
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
    "stand": ((12, 12, 30), (16, 16, 30)),
    "contact": ((12, 9, 30), (16, 19, 30)),
    "pass": ((13, 11, 28), (15, 15, 30)),
    "contact2": ((12, 15, 30), (16, 12, 30)),
    "pass2": ((12, 13, 30), (16, 15, 28)),
    "tuck": ((12, 11, 28), (16, 17, 28)),
    "dangle": ((12, 11, 30), (16, 17, 30)),
    "crouch": ((12, 9, 30), (16, 19, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the hip (row `top`) to the boot sole (row fy): brown pants, grey boot (toe to the right)."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 3, y, SOLE)
        elif y >= fy - 2:
            s.r(x, y, x + 3 if y == fy - 1 else x + 2, y, BOOT)
            if back:
                s.px(SOLE, (x, y))
        else:
            s.r(x, y, x + 2, y, PANTS_D if back else PANTS)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 23 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm (darker sleeve), legs
    for x, y in _line(11, 17 + oy, 10 + bax, 21 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(10, 16 + oy, 11, 17 + oy, BIB)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 19, hip, PANTS)
    # torso: teal top, darker bib with two strap pixels (overalls look)
    s.r(12, 16 + oy, 19, hip - 1, TOP)
    s.r(15, 19 + oy, 18, hip - 1, BIB)
    s.px(BIB, (15, 18 + oy), (18, 18 + oy))
    # head (three-quarter, face to the right)
    hx, hy = hdx, oy
    s.r(11 + hx, 8 + hy, 21 + hx, 14 + hy, SKIN)
    s.r(12 + hx, 15 + hy, 20 + hx, 15 + hy, SKIN)
    s.r(10 + hx, 8 + hy, 12 + hx, 11 + hy, HAIR); s.px(HAIR, (11 + hx, 12 + hy))
    s.px(SKIN_D, (12 + hx, 12 + hy), (12 + hx, 13 + hy), (13 + hx, 13 + hy))        # ear
    # helmet: dome rows 1-6, thin brim row 7
    s.r(14 + hx, 1 + hy, 18 + hx, 1 + hy, HELM)
    s.r(12 + hx, 2 + hy, 20 + hx, 2 + hy, HELM)
    s.r(11 + hx, 3 + hy, 21 + hx, 6 + hy, HELM)
    s.r(9 + hx, 7 + hy, 22 + hx, 7 + hy, HELM)
    s.px(HELM_D, (11 + hx, 4 + hy), (11 + hx, 5 + hy), (11 + hx, 6 + hy), (12 + hx, 6 + hy), (13 + hx, 6 + hy),
         (9 + hx, 7 + hy), (10 + hx, 7 + hy), (12 + hx, 2 + hy))
    # headlamp on the helmet front, sticking 2 px out at the right
    s.r(20 + hx, 3 + hy, 23 + hx, 6 + hy, LAMP)
    s.r(22 + hx, 4 + hy, 23 + hx, 5 + hy, LENS)
    # face
    if eyes_shut:
        s.px(OUT, (14 + hx, 11 + hy), (15 + hx, 10 + hy), (16 + hx, 11 + hy), (18 + hx, 11 + hy), (19 + hx, 10 + hy), (20 + hx, 11 + hy))
    else:
        s.r(15 + hx, 10 + hy, 16 + hx, 11 + hy, OUT); s.px(EYE_HI, (16 + hx, 10 + hy))
        s.px(OUT, (19 + hx, 10 + hy), (19 + hx, 11 + hy))
    s.px(SKIN_D, (21 + hx, 12 + hy))                                                # nose bump
    s.px(MOUTH, (17 + hx, 14 + hy), (18 + hx, 14 + hy), (19 + hx, 13 + hy))         # small smile
    s.px(SMUDGE, (14 + hx, 13 + hy))                                                # outer cheek
    # front arm: teal sleeve, then skin to a mitten hand
    pts = _line(19, 16 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TOP if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def lampy(view="front"):
    s = Spr(jf.W, jf.H)
    # arms
    for x in (14, 24):
        s.r(x, 16, x + 1, 17, TOP); s.r(x, 18, x + 1, 21, SKIN); s.px(SKIN_D, (x, 21), (x + 1, 21))
    # legs and boots
    s.r(16, 23, 23, 23, PANTS)
    for x in (16, 21):
        s.r(x, 24, x + 2, 27, PANTS)
    s.r(15, 28, 18, 29, BOOT); s.r(21, 28, 24, 29, BOOT)
    s.r(15, 30, 18, 30, SOLE); s.r(21, 30, 24, 30, SOLE)
    # torso: teal top, bib, straps
    s.r(16, 16, 23, 22, TOP)
    s.r(18, 18, 21, 22, BIB)
    s.px(BIB, (18, 17), (21, 17))
    # head
    s.r(15, 8, 24, 14, SKIN); s.r(16, 15, 23, 15, SKIN)
    s.r(14, 8, 14, 11, HAIR); s.r(25, 8, 25, 11, HAIR); s.px(HAIR, (15, 8), (24, 8))
    # helmet
    s.r(17, 1, 22, 1, HELM); s.r(15, 2, 24, 2, HELM); s.r(14, 3, 25, 6, HELM); s.r(13, 7, 26, 7, HELM)
    s.px(HELM_D, (14, 5), (14, 6), (15, 6), (25, 5), (25, 6), (24, 6), (13, 7), (26, 7))
    # headlamp, centre of the dome
    s.r(18, 2, 21, 5, LAMP); s.r(19, 3, 20, 4, LENS)
    # face: big round eyes, small smile, smudge on the outer (right) cheek = viewer's left
    s.r(17, 10, 18, 11, OUT); s.r(21, 10, 22, 11, OUT); s.px(EYE_HI, (18, 10), (22, 10))
    s.px(MOUTH, (19, 14), (20, 14), (18, 13), (21, 13))
    s.px(SMUDGE, (16, 12))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/lampy/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = lampy(), sheet()
    frames.save(f"{out}/lampy_frames.png")
    front.save(f"{out}/lampy_pixel.png")
    with open(f"{out}/lampy_frames.json", "w") as f:
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
    rev.save(f"{out}/lampy_pixel_sheet.png")
    print("wrote", out)
