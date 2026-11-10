"""Foreman Dot's pixel form for The Hill (Pillow only, drawn in code).

foreman_dot(view="front")    front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

28 px tall with the outline (0.85 m body plus the hat, traced from refs/jarling/foreman_dot_side_sprite.png):
hard hat 5 rows (ridge row, dome, brim on the brow line), face 7, torso 7, pants 3, boots 4. Short and stocky: a 13 px
torso. A human site lead, not the library's Gnome Foreman: round yellow hat, clean chin, no clipboard, no whistle.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#D99E6E", "#B97F55"
HAIR = "#4A2F23"
HAT, HAT_L, HAT_D = "#F5C518", "#FFE066", "#C99A0E"
TEE, TEE_D = "#F28A1E", "#D0700F"
STRIPE = "#FFFFFF"
PANTS = "#1F2D4F"
BOOT, SOLE = "#7A4E2A", "#4A3020"
MOUTH, TEETH = "#6A2232", "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21), 0),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22), 1),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21), 0),
    "walk1": ("pass", 0, 0, (0, 0), (22, 20), 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21), 0),
    "walk3": ("pass2", 0, 0, (0, 0), (22, 20), 0),
    "jump": ("tuck", 1, 0, (-1, -3), (23, 15), 0),
    "fall": ("dangle", 0, 0, (-1, -4), (24, 14), 0),
    "side0": ("stand", 0, -1, (0, 0), (18, 16), 0),
    "side1": ("contact", 0, 1, (1, -1), (22, 19), 0),
    "side2": ("stand", 0, 0, (0, 0), (21, 20), 0),
    "down0": ("stand", 0, 0, (0, -1), (22, 11), 0),
    "down1": ("crouch", 0, 1, (0, 0), (24, 18), 1),
    "down2": ("stand", 0, 0, (0, 0), (23, 17), 0),
}

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs 3 px, boots 5 px
LEGS = {
    "stand": ((10, 10, 30), (16, 16, 30)),
    "contact": ((10, 8, 30), (16, 18, 30)),
    "pass": ((11, 10, 28), (15, 15, 30)),
    "contact2": ((10, 14, 30), (16, 12, 30)),
    "pass2": ((10, 11, 30), (16, 15, 28)),
    "tuck": ((10, 9, 28), (16, 17, 28)),
    "dangle": ((10, 9, 30), (16, 17, 30)),
    "crouch": ((10, 8, 30), (16, 18, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the hip (row `top`) to the sole (row fy): navy pants, a chunky brown boot, toe right."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 4, y, SOLE)
        elif y >= fy - 3 and i > 0:
            s.r(x, y, x + (3 if y == fy - 3 else 4), y, BOOT)
            if back:
                s.px(SOLE, (x, y))
        else:
            s.r(x, y, x + 2, y, PANTS)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 24 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm, legs, pants band
    for x, y in _line(9, 18 + oy, 7 + bax, 22 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(8, 17 + oy, 9, 18 + oy, TEE_D)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(10, hip, 20, hip, PANTS)
    # torso: orange tee, one white hi-vis stripe row
    s.r(10, 17 + oy, 20, 17 + oy, TEE)
    s.r(9, 18 + oy, 21, hip - 1, TEE)
    s.r(9, 18 + oy, 9, hip - 1, TEE_D); s.r(10, hip - 1, 20, hip - 1, TEE_D)
    s.r(9, 20 + oy, 21, 20 + oy, STRIPE)
    # head (three-quarter, face to the right): bob at the back down to the jaw
    hx, hy = hdx, oy
    s.r(10 + hx, 10 + hy, 21 + hx, 15 + hy, SKIN)
    s.r(11 + hx, 16 + hy, 20 + hx, 16 + hy, SKIN)
    s.r(10 + hx, 10 + hy, 13 + hx, 15 + hy, HAIR); s.px(HAIR, (14 + hx, 10 + hy), (11 + hx, 16 + hy))
    s.px(SKIN_D, (13 + hx, 12 + hy), (13 + hx, 13 + hy))                            # ear
    # hard hat: ridge row, dome, brim on the brow line sticking 2 px out at the right
    s.r(14 + hx, 5 + hy, 17 + hx, 5 + hy, HAT)
    s.r(12 + hx, 6 + hy, 19 + hx, 6 + hy, HAT)
    s.r(11 + hx, 7 + hy, 20 + hx, 8 + hy, HAT)
    s.r(9 + hx, 9 + hy, 23 + hx, 9 + hy, HAT)
    s.px(HAT_L, (15 + hx, 5 + hy), (16 + hx, 5 + hy), (16 + hx, 6 + hy), (16 + hx, 7 + hy), (17 + hx, 8 + hy), (22 + hx, 9 + hy), (23 + hx, 9 + hy))
    s.px(HAT_D, (11 + hx, 7 + hy), (11 + hx, 8 + hy), (12 + hx, 8 + hy), (9 + hx, 9 + hy), (10 + hx, 9 + hy), (11 + hx, 9 + hy))
    # face: eyes right under the brim, open smile with a white top row
    if eyes_shut:
        s.px(OUT, (14 + hx, 11 + hy), (15 + hx, 11 + hy), (18 + hx, 11 + hy), (19 + hx, 11 + hy))
    else:
        s.px(OUT, (15 + hx, 10 + hy), (15 + hx, 11 + hy), (19 + hx, 10 + hy), (19 + hx, 11 + hy))
    s.px(SKIN_D, (21 + hx, 12 + hy))                                                # nose bump
    s.r(16 + hx, 13 + hy, 19 + hx, 13 + hy, TEETH)
    s.r(16 + hx, 14 + hy, 19 + hx, 14 + hy, MOUTH); s.r(17 + hx, 15 + hy, 18 + hx, 15 + hy, MOUTH)
    # front arm: orange sleeve, then skin to a mitten hand
    pts = _line(20, 17 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TEE if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def foreman_dot(view="front"):
    s = Spr(jf.W, jf.H)
    # arms
    for x in (11, 26):
        s.r(x, 17, x + 1, 18, TEE); s.r(x, 19, x + 1, 22, SKIN); s.px(SKIN_D, (x, 22), (x + 1, 22))
    # pants, legs, chunky boots
    s.r(14, 24, 24, 24, PANTS)
    for x in (14, 21):
        s.r(x, 25, x + 3, 26, PANTS)
    s.r(13, 27, 18, 29, BOOT); s.r(20, 27, 25, 29, BOOT)
    s.r(13, 30, 18, 30, SOLE); s.r(20, 30, 25, 30, SOLE)
    s.px(SOLE, (13, 27), (25, 27))
    # torso, 13 px wide, one hi-vis stripe
    s.r(14, 17, 24, 17, TEE); s.r(13, 18, 25, 23, TEE)
    s.r(13, 23, 25, 23, TEE_D); s.px(TEE_D, (13, 22), (25, 22))
    s.r(13, 20, 25, 20, STRIPE)
    # head: face, bob at the sides down to the jaw
    s.r(14, 10, 25, 15, SKIN); s.r(16, 16, 23, 16, SKIN)
    s.r(14, 10, 14, 15, HAIR); s.r(25, 10, 25, 15, HAIR); s.px(HAIR, (15, 10), (24, 10), (15, 16), (24, 16))
    # hard hat: ridge, dome, brim on the brow line
    s.r(17, 5, 22, 5, HAT); s.r(15, 6, 24, 6, HAT); s.r(14, 7, 25, 8, HAT); s.r(12, 9, 27, 9, HAT)
    s.px(HAT_L, (19, 5), (20, 5), (19, 6), (19, 7), (19, 8), (16, 7))
    s.px(HAT_D, (25, 7), (25, 8), (24, 8), (12, 9), (27, 9), (26, 9))
    # face
    s.px(OUT, (17, 10), (17, 11), (22, 10), (22, 11))
    s.r(18, 13, 21, 13, TEETH); s.r(18, 14, 21, 14, MOUTH); s.r(19, 15, 20, 15, MOUTH)
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/foreman_dot/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = foreman_dot(), sheet()
    frames.save(f"{out}/foreman_dot_frames.png")
    front.save(f"{out}/foreman_dot_pixel.png")
    with open(f"{out}/foreman_dot_frames.json", "w") as f:
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
    rev.save(f"{out}/foreman_dot_pixel_sheet.png")
    print("wrote", out)
