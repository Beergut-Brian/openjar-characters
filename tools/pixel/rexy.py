"""Rexy's pixel form for The Hill (Pillow only, drawn in code).

rexy(view="front")           front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

About 31 px tall with the outline (the 3D is 1.15 m with the hood spikes, about 31 px at true scale): spikes 2 rows, big
round hood 13 rows (oval face opening inside it), short torso 9, short legs 5 with footies. Small kid, big head.
Dino read: yellow spikes over the hood and down the back, a short orange tail with yellow spikes behind (left in the frames),
white felt teeth (3 px) along the top edge of the face opening. The open grin is the only thing at the mouth.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#F0BE94", "#D09C72"
ORG, ORG_D = "#F7941D", "#D2780F"
SPIKE = "#FFD23F"
TEETH = "#F7F7F2"
MOUTH, TONGUE = "#6A2232", "#E8708A"
EYE_HI = "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21), 0),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22), 1),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21), 0),
    "walk1": ("pass", 1, 0, (0, 0), (22, 20), 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21), 0),
    "walk3": ("pass2", 1, 0, (0, 0), (22, 20), 0),
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
    """One leg from the hip (row `top`) to the footie sole (row fy): orange, toe to the right, shaded sole."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 3, y, ORG_D)
        elif y == fy - 1:
            s.r(x, y, x + 3, y, ORG_D if back else ORG)
        else:
            s.r(x, y, x + 2, y, ORG_D if back else ORG)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 25 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # tail (behind, left) with yellow spikes on its top edge
    s.r(8, hip - 2 + oy, 11, hip - 1 + oy, ORG); s.r(5, hip - 1 + oy, 7, hip + oy, ORG); s.px(ORG, (4, hip + 1 + oy), (3, hip + 1 + oy))
    s.px(SPIKE, (8, hip - 3 + oy), (6, hip - 2 + oy), (4, hip + oy))
    # back arm, legs
    for x, y in _line(11, 17 + oy, 10 + bax, 22 + oy + bay):
        s.r(x, y, x + 1, y + 1, ORG_D)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    # torso: short, orange, a darker belly pixel row at the hem
    s.r(11, 16 + oy, 19, hip, ORG)
    s.r(12, hip, 19, hip, ORG_D)
    s.px(SPIKE, (10, 18 + oy), (10, 21 + oy), (9, 19 + oy))   # spikes down the back
    # head: big round hood, 13 rows (3..15), oval face opening on the right
    hx, hy = hdx, oy
    s.r(12 + hx, 3 + hy, 19 + hx, 3 + hy, ORG)
    s.r(10 + hx, 4 + hy, 21 + hx, 5 + hy, ORG)
    s.r(9 + hx, 6 + hy, 22 + hx, 14 + hy, ORG)
    s.r(10 + hx, 15 + hy, 21 + hx, 15 + hy, ORG)
    s.px(ORG_D, (9 + hx, 12 + hy), (9 + hx, 13 + hy), (9 + hx, 14 + hy), (10 + hx, 15 + hy), (11 + hx, 15 + hy), (12 + hx, 15 + hy), (13 + hx, 15 + hy), (14 + hx, 15 + hy), (15 + hx, 15 + hy), (16 + hx, 15 + hy), (17 + hx, 15 + hy), (18 + hx, 15 + hy), (19 + hx, 15 + hy), (20 + hx, 15 + hy), (21 + hx, 15 + hy))
    # spikes over the hood (row 2 and the back edge)
    s.px(SPIKE, (11 + hx, 2 + hy), (14 + hx, 2 + hy), (17 + hx, 2 + hy), (11 + hx, 3 + hy), (14 + hx, 3 + hy), (17 + hx, 3 + hy))
    s.px(SPIKE, (9 + hx, 4 + hy), (8 + hx, 5 + hy), (9 + hx, 5 + hy), (8 + hx, 8 + hy), (8 + hx, 9 + hy))
    # face opening: oval, skin
    s.r(15 + hx, 7 + hy, 21 + hx, 14 + hy, SKIN)
    s.px(ORG, (15 + hx, 14 + hy), (21 + hx, 14 + hy), (15 + hx, 7 + hy))
    s.px(SKIN_D, (15 + hx, 8 + hy), (15 + hx, 9 + hy))
    s.px(TEETH, (16 + hx, 7 + hy), (18 + hx, 7 + hy), (20 + hx, 7 + hy))
    # eyes, big open grin
    if eyes_shut:
        s.px(OUT, (16 + hx, 10 + hy), (17 + hx, 9 + hy), (18 + hx, 10 + hy), (20 + hx, 10 + hy), (21 + hx, 9 + hy))
    else:
        s.r(16 + hx, 8 + hy, 17 + hx, 9 + hy, OUT); s.px(EYE_HI, (17 + hx, 8 + hy))
        s.r(20 + hx, 8 + hy, 20 + hx, 9 + hy, OUT)
    s.r(16 + hx, 11 + hy, 21 + hx, 12 + hy, MOUTH)
    s.r(17 + hx, 13 + hy, 20 + hx, 13 + hy, MOUTH)
    s.px(TONGUE, (18 + hx, 13 + hy), (19 + hx, 13 + hy))
    # front arm: orange sleeve, skin mitten hand
    pts = _line(19, 17 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, ORG if i < len(pts) - 1 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def rexy(view="front"):
    s = Spr(jf.W, jf.H)
    # tail sliver behind the legs
    s.r(24, 27, 27, 28, ORG); s.px(SPIKE, (26, 26))
    # arms
    for x in (13, 25):
        s.r(x, 18, x + 1, 22, ORG); s.px(SKIN, (x, 23), (x + 1, 23)); s.px(SKIN_D, (x, 23))
    # legs and footies
    s.r(16, 25, 23, 25, ORG_D)
    for x in (16, 21):
        s.r(x, 26, x + 2, 28, ORG)
    s.r(15, 29, 18, 29, ORG); s.r(21, 29, 24, 29, ORG)
    s.r(15, 30, 18, 30, ORG_D); s.r(21, 30, 24, 30, ORG_D)
    # torso
    s.r(15, 16, 24, 24, ORG)
    s.r(16, 24, 23, 24, ORG_D)
    # hood
    s.r(17, 3, 22, 3, ORG); s.r(15, 4, 24, 5, ORG); s.r(14, 6, 25, 14, ORG); s.r(15, 15, 24, 15, ORG)
    s.r(14, 15, 25, 15, ORG_D)
    s.px(SPIKE, (16, 2), (19, 2), (22, 2), (16, 3), (19, 3), (22, 3), (14, 4), (25, 4), (13, 6), (26, 6))
    # face opening
    s.r(16, 7, 23, 14, SKIN)
    s.px(ORG, (16, 7), (23, 7), (16, 14), (23, 14))
    s.px(TEETH, (18, 7), (20, 7), (22, 7))
    s.r(17, 8, 18, 9, OUT); s.r(21, 8, 22, 9, OUT); s.px(EYE_HI, (18, 8), (22, 8))
    s.r(17, 11, 22, 12, MOUTH); s.r(18, 13, 21, 13, MOUTH); s.px(TONGUE, (19, 13), (20, 13))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/rexy/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = rexy(), sheet()
    frames.save(f"{out}/rexy_frames.png")
    front.save(f"{out}/rexy_pixel.png")
    with open(f"{out}/rexy_frames.json", "w") as f:
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
    rev.save(f"{out}/rexy_pixel_sheet.png")
    print("wrote", out)
