"""Mayor Pip's pixel form for The Hill (Pillow only, drawn in code).

mayor_pip(view="front")      front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

32 px tall with the outline, but the smallest body (0.8 m body under a 1.85x top hat): top hat 13 rows (crown 10 with a
highlight column, gold band 2 at its base, brim 1), head 7, then chin to soles 10 (shirt 5, pants 3, shoes 2).
The hands sit 4 rows lower and 1 px further back than The Hill's standard POSES, because the shoulders are at row 22.
Note: jarling_frames.sheet builds the ride frame from the top 14 rows of idle0, which for Pip is almost all hat.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#EFBB90", "#CF9A70"
HAIR = "#4A2F23"
HAT, HAT_L, BAND = "#1C1C22", "#3A3A46", "#D9B23A"
SHIRT, SHIRT_D = "#A8CFF0", "#86B4DA"
SASH = "#D9B23A"
PANTS = "#7D8088"
SHOE, SHOE_L = "#15151A", "#4A4A55"
MOUTH = "#6A2232"

HAND = (21, 25)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop
# The Hill's POSES hands shifted (-1, +4) for the tiny body; no lift (the hat fills the frame top).
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (21, 25), 0),
    "idle1": ("stand", 0, 0, (0, 1), (21, 26), 1),
    "walk0": ("contact", 0, 0, (1, 0), (21, 25), 0),
    "walk1": ("pass", 0, 0, (0, 0), (21, 24), 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (21, 25), 0),
    "walk3": ("pass2", 0, 0, (0, 0), (21, 24), 0),
    "jump": ("tuck", 0, 0, (-1, -2), (22, 19), 0),
    "fall": ("dangle", 0, 0, (-1, -3), (23, 18), 0),
    "side0": ("stand", 0, -1, (0, 0), (17, 20), 0),
    "side1": ("contact", 0, 1, (1, -1), (21, 23), 0),
    "side2": ("stand", 0, 0, (0, 0), (20, 24), 0),
    "down0": ("stand", 0, 0, (0, -1), (21, 15), 0),
    "down1": ("crouch", 0, 1, (0, 0), (23, 22), 1),
    "down2": ("stand", 0, 0, (0, 0), (22, 21), 0),
}

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs 2 px, shoes 3-4 px
LEGS = {
    "stand": ((13, 13, 30), (16, 16, 30)),
    "contact": ((13, 11, 30), (16, 18, 30)),
    "pass": ((13, 12, 29), (15, 15, 30)),
    "contact2": ((13, 15, 30), (16, 13, 30)),
    "pass2": ((13, 13, 30), (16, 16, 29)),
    "tuck": ((13, 12, 29), (16, 17, 29)),
    "dangle": ((13, 12, 30), (16, 17, 30)),
    "crouch": ((13, 11, 30), (16, 18, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the hip (row `top`) to the sole (row fy): grey pants, a black shoe, toe right."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 3, y, SHOE)
        elif y == fy - 1 and i > 0:
            s.r(x, y, x + 2, y, SHOE)
            if not back:
                s.px(SHOE_L, (x + 2, y))
        else:
            s.r(x, y, x + 1, y, PANTS)


def _hat(s, cx, top):
    """Top hat, crown x cx..cx+7 from row `top`: 10 crown rows with a highlight column, 2 gold band rows, 12 px brim."""
    s.r(cx, top, cx + 7, top + 9, HAT)
    s.r(cx + 2, top, cx + 2, top + 9, HAT_L)
    s.r(cx, top + 10, cx + 7, top + 11, BAND)
    s.r(cx - 2, top + 12, cx + 9, top + 12, HAT)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 26 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm (long sleeve, shaded), legs, pants band
    pts = _line(12, 22 + oy, 11 + bax, 25 + oy + bay)
    for x, y in pts:
        s.px(SHIRT_D, (x, y))
    s.px(SKIN_D, pts[-1])
    s.px(SHIRT_D, (11, 22 + oy))
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 18, hip, PANTS)
    # shirt with the gold sash (shoulder to hip)
    s.r(12, 21 + oy, 18, hip - 1, SHIRT)
    s.r(12, 21 + oy, 12, hip - 1, SHIRT_D)
    for i, y in enumerate(range(21 + oy, hip)):
        x = 13 + round(i * 1.4)
        s.px(SASH, (x, y), (x + 1, y))
    # head (three-quarter, face to the right), 10 px wide, hair under the brim
    hx, hy = hdx, oy
    s.r(11 + hx, 14 + hy, 20 + hx, 19 + hy, SKIN)
    s.r(12 + hx, 20 + hy, 19 + hx, 20 + hy, SKIN)
    s.r(11 + hx, 14 + hy, 20 + hx, 14 + hy, HAIR)
    s.r(11 + hx, 15 + hy, 13 + hx, 17 + hy, HAIR); s.px(HAIR, (14 + hx, 15 + hy))
    s.px(SKIN_D, (13 + hx, 17 + hy), (13 + hx, 18 + hy))                            # ear
    _hat(s, 12 + hx, 1 + hy)
    # stern face: brow px over one dark px (half-lidded), flat 2 px mouth
    if eyes_shut:
        s.px(OUT, (15 + hx, 17 + hy), (16 + hx, 17 + hy), (18 + hx, 17 + hy), (19 + hx, 17 + hy))
    else:
        s.px(HAIR, (15 + hx, 16 + hy), (16 + hx, 16 + hy), (18 + hx, 16 + hy), (19 + hx, 16 + hy))
        s.px(OUT, (16 + hx, 17 + hy), (19 + hx, 17 + hy))
    s.px(SKIN_D, (20 + hx, 18 + hy))                                                # nose bump
    s.px(MOUTH, (17 + hx, 19 + hy), (18 + hx, 19 + hy))
    # front arm: long sleeve to a skin hand
    pts = _line(18, 22 + oy, hand[0], hand[1])
    for x, y in pts:
        s.r(x, y, x + 1, y, SHIRT_D)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1], SKIN)
    return s.im


def mayor_pip(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: long sleeves, skin hands
    for x in (15, 23):
        s.r(x, 21, x + 1, 24, SHIRT); s.r(x, 25, x + 1, 25, SKIN)
    s.r(15, 22, 15, 24, SHIRT_D); s.r(24, 22, 24, 24, SHIRT_D)
    # pants, legs, shoes
    s.r(17, 26, 22, 26, PANTS)
    for x in (17, 21):
        s.r(x, 27, x + 1, 28, PANTS)
    s.r(16, 29, 18, 30, SHOE); s.r(21, 29, 23, 30, SHOE)
    s.px(SHOE_L, (17, 29), (22, 29))
    # shirt and the gold sash
    s.r(17, 21, 22, 25, SHIRT)
    for i, y in enumerate(range(21, 26)):
        x = 17 + round(i * 1.1)
        s.px(SASH, (x, y), (x + 1, y))
    # head, 10 px wide
    s.r(15, 14, 24, 19, SKIN); s.r(16, 20, 23, 20, SKIN)
    s.r(15, 14, 24, 14, HAIR); s.r(15, 15, 15, 16, HAIR); s.r(24, 15, 24, 16, HAIR)
    s.px(SKIN_D, (14, 17), (25, 17))                                                # ears
    _hat(s, 16, 1)
    s.px(HAIR, (17, 16), (18, 16), (21, 16), (22, 16))
    s.px(OUT, (18, 17), (21, 17))
    s.px(MOUTH, (19, 19), (20, 19))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/mayor_pip/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = mayor_pip(), sheet()
    frames.save(f"{out}/mayor_pip_frames.png")
    front.save(f"{out}/mayor_pip_pixel.png")
    with open(f"{out}/mayor_pip_frames.json", "w") as f:
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
    rev.save(f"{out}/mayor_pip_pixel_sheet.png")
    print("wrote", out)
