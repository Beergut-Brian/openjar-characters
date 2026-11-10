"""Sir Clank's pixel form for The Hill (Pillow only, drawn in code).

sir_clank(view="front")      front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

31 px tall with the outline (the 3D is about 1.16 m with the pot, ~31 px at the sprite scale, so no squeezing):
pot 6 rows (lid, 4 body with a highlight stripe, darker rim), face 8 (brows sit just under the pot rim), torso 7, pants 5, boots 3.
Medium build, standing dead straight (no lean). The pot is a flat-topped cylinder 14 px wide with a rim row;
its dark handle sticks out the BACK (left in the frames), 5 x 2 px, high on the pot at rows 3-4, far from the mouth.
In the front form the handle is hidden behind the pot. Shield on the chest: 3 x 4 yellow, pointed bottom.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#F7CFAE", "#D7AE8C"
HAIR = "#4A2F23"
POT, POT_HI, POT_RIM = "#B8BEC6", "#DDE2E8", "#8D949E"
HANDLE = "#3A3D44"
TOP, TOP_D = "#8A8F98", "#6C7179"
SHIELD = "#F2C230"
PANTS, PANTS_D = "#23305E", "#1A2447"
BOOT, SOLE = "#7A4E2A", "#3F2814"
MOUTH = "#8A3A3A"
EYE_HI = "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# Sir Clank is 31 px, so the jump lifts 1 px and tucks the feet.
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
    """One leg from the hip (row `top`) to the boot sole (row fy): navy pants, brown boot (toe to the right)."""
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
    for x, y in _line(11, 17 + oy, 10 + bax, 21 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(10, 16 + oy, 11, 17 + oy, TOP_D)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 19, hip, PANTS)
    # torso: grey shirt, yellow shield 3 x 4 with a pointed bottom
    s.r(12, 16 + oy, 19, hip - 1, TOP)
    s.r(15, 17 + oy, 17, 19 + oy, SHIELD); s.px(SHIELD, (16, 20 + oy))
    # head (three-quarter, face to the right), straight on the neck
    hx, hy = hdx, oy
    s.r(11 + hx, 6 + hy, 21 + hx, 14 + hy, SKIN)
    s.r(12 + hx, 15 + hy, 20 + hx, 15 + hy, SKIN)
    s.r(10 + hx, 6 + hy, 12 + hx, 11 + hy, HAIR); s.px(HAIR, (11 + hx, 12 + hy))
    s.px(SKIN_D, (12 + hx, 12 + hy), (12 + hx, 13 + hy), (13 + hx, 13 + hy))        # ear
    # pot helmet: rows 2-5, flat top, wider than the head, rim row darker
    s.r(10 + hx, 2 + hy, 22 + hx, 2 + hy, POT_HI)
    s.r(9 + hx, 3 + hy, 22 + hx, 6 + hy, POT)
    s.r(11 + hx, 3 + hy, 11 + hx, 6 + hy, POT_HI)                                 # vertical highlight stripe
    s.r(9 + hx, 7 + hy, 22 + hx, 7 + hy, POT_RIM)
    s.r(4 + hx, 3 + hy, 8 + hx, 4 + hy, HANDLE)                                   # handle out the back, high
    # face: thick serious brows, small eyes, proud closed smile
    s.r(15 + hx, 8 + hy, 17 + hx, 8 + hy, HAIR); s.r(19 + hx, 8 + hy, 21 + hx, 8 + hy, HAIR)
    if eyes_shut:
        s.px(OUT, (15 + hx, 10 + hy), (16 + hx, 10 + hy), (19 + hx, 10 + hy), (20 + hx, 10 + hy))
    else:
        s.r(16 + hx, 9 + hy, 16 + hx, 10 + hy, OUT); s.px(EYE_HI, (15 + hx, 9 + hy))
        s.px(OUT, (20 + hx, 9 + hy), (20 + hx, 10 + hy))
    s.px(SKIN_D, (21 + hx, 11 + hy))                                                # nose bump
    s.px(MOUTH, (17 + hx, 13 + hy), (18 + hx, 13 + hy), (19 + hx, 12 + hy))         # proud smile
    # front arm: grey sleeve, then skin to a mitten hand
    pts = _line(19, 16 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TOP if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def sir_clank(view="front"):
    s = Spr(jf.W, jf.H)
    for x in (14, 24):
        s.r(x, 16, x + 1, 17, TOP); s.r(x, 18, x + 1, 21, SKIN); s.px(SKIN_D, (x, 21), (x + 1, 21))
    s.r(16, 23, 23, 23, PANTS)
    for x in (16, 21):
        s.r(x, 24, x + 2, 27, PANTS)
    s.r(15, 28, 18, 29, BOOT); s.r(21, 28, 24, 29, BOOT)
    s.r(15, 30, 18, 30, SOLE); s.r(21, 30, 24, 30, SOLE)
    s.r(16, 16, 23, 22, TOP)
    s.r(18, 17, 20, 19, SHIELD); s.px(SHIELD, (19, 20))
    s.r(15, 6, 24, 14, SKIN); s.r(16, 15, 23, 15, SKIN)
    s.r(14, 6, 14, 10, HAIR); s.r(25, 6, 25, 10, HAIR)
    s.r(13, 2, 26, 2, POT_HI); s.r(13, 3, 26, 6, POT); s.r(15, 3, 15, 6, POT_HI); s.r(13, 7, 26, 7, POT_RIM)
    s.px(HANDLE, (12, 4))                                                           # handle stub peeking out the back
    s.r(15, 8, 17, 8, HAIR); s.r(22, 8, 24, 8, HAIR)
    s.r(17, 9, 18, 10, OUT); s.r(21, 9, 22, 10, OUT); s.px(EYE_HI, (17, 9), (21, 9))
    s.px(MOUTH, (18, 13), (19, 13), (20, 13), (17, 12), (21, 12))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/sir_clank/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = sir_clank(), sheet()
    frames.save(f"{out}/sir_clank_frames.png")
    front.save(f"{out}/sir_clank_pixel.png")
    with open(f"{out}/sir_clank_frames.json", "w") as f:
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
    rev.save(f"{out}/sir_clank_pixel_sheet.png")
    print("wrote", out)
