"""Boxbot's pixel form for The Hill (Pillow only, drawn in code).

boxbot(view="front")         front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

27 px tall with the outline (the 3D is about 0.98 m, 26-27 px at true scale): head box 10 rows (tape strip on the top row),
torso box 8, pants 6, shoes 3. The head box is 10 px wide, the torso box 12 px, so the head is the smaller box.
The face shows in a 6 x 6 cut-out window (5 x 6 in the frames); the arms are ribbed hose sleeves with alternating rows.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#EFBB90", "#CF9A70"
BOX, BOX_D, TAPE = "#C49A6C", "#A47C52", "#E6CFA0"
INK = "#2A2A30"
BLUE, YELLOW = "#3B6FD1", "#F2C230"
HOSE, HOSE_D = "#C0C4CA", "#9A9EA6"
PANTS, PANTS_D = "#80848C", "#63676F"
SHOE, SOLE = "#3B6FD1", "#2C54A0"
HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
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
    """One leg from the hip (row `top`) to the shoe sole (row fy): grey pants, blue shoe (toe to the right)."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 3, y, SOLE)
        elif y >= fy - 2:
            s.r(x, y, x + 3 if y == fy - 1 else x + 2, y, SHOE)
        else:
            s.r(x, y, x + 2, y, PANTS_D if back else PANTS)


def _arm(s, pts, back=False):
    """Hose sleeve along pts (2 x 2 blocks), alternating light and dark rib rows."""
    for i, (x, y) in enumerate(pts):
        c = HOSE_D if (i % 2 == 0) else HOSE
        if back:
            c = HOSE_D if i % 2 == 0 else "#80848C"
        s.r(x, y, x + 1, y + 1, c)


def _torso(s, x0, x1, top, bot, cx):
    s.r(x0, top, x1, bot, BOX)
    s.r(x0, top, x0, bot, BOX_D); s.r(x0, bot, x1, bot, BOX_D)
    # marker details: a dial pair, a speaker slot of dashes, a panel line
    s.px(BLUE, (cx, top + 2)); s.px(YELLOW, (cx + 2, top + 2))
    s.px(INK, (cx - 1, top + 2), (cx + 1, top + 2), (cx + 3, top + 2))
    s.r(cx - 1, top + 5, cx + 3, top + 5, INK)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 22 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    _arm(s, _line(9, 15 + oy, 8 + bax, 20 + oy + bay), back=True)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 19, hip, PANTS)
    _torso(s, 10, 21, 14 + oy, hip - 1, 15)
    # head box (10 wide, rows 4-13): shaded left column and bottom row, tape strip on the top row
    hx, hy = hdx, oy
    s.r(11 + hx, 4 + hy, 20 + hx, 13 + hy, BOX)
    s.r(11 + hx, 4 + hy, 11 + hx, 13 + hy, BOX_D); s.r(11 + hx, 13 + hy, 20 + hx, 13 + hy, BOX_D)
    s.r(14 + hx, 4 + hy, 17 + hx, 4 + hy, TAPE)
    s.r(15 + hx, 6 + hy, 19 + hx, 11 + hy, SKIN)           # face cut-out
    s.px(SKIN_D, (15 + hx, 11 + hy))
    if eyes_shut:
        s.px(INK, (16 + hx, 8 + hy), (17 + hx, 8 + hy), (19 + hx, 8 + hy))
    else:
        s.px(INK, (16 + hx, 8 + hy), (19 + hx, 8 + hy))
    s.px(INK, (17 + hx, 10 + hy), (18 + hx, 10 + hy), (19 + hx, 10 + hy))
    # front arm: hose sleeve to a skin mitten hand
    pts = _line(20, 15 + oy, hand[0], hand[1] - 1)
    _arm(s, pts)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def boxbot(view="front"):
    s = Spr(jf.W, jf.H)
    _arm(s, [(12, 15 + i) for i in range(0, 6)])
    _arm(s, [(26, 15 + i) for i in range(0, 6)])
    for x in (12, 26):
        s.r(x, 21, x + 1, 22, SKIN); s.px(SKIN_D, (x, 22), (x + 1, 22))
    # legs and shoes
    s.r(16, 22, 23, 22, PANTS)
    for x in (16, 21):
        s.r(x, 23, x + 2, 27, PANTS)
    s.r(15, 28, 18, 29, SHOE); s.r(21, 28, 24, 29, SHOE)
    s.r(15, 30, 18, 30, SOLE); s.r(21, 30, 24, 30, SOLE)
    _torso(s, 14, 25, 14, 21, 17)
    s.r(15, 4, 24, 13, BOX)
    s.r(15, 4, 15, 13, BOX_D); s.r(15, 13, 24, 13, BOX_D)
    s.r(18, 4, 21, 4, TAPE)
    s.r(17, 6, 22, 11, SKIN)
    s.px(INK, (18, 8), (21, 8), (19, 10), (20, 10), (18, 10), (21, 10))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/boxbot/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = boxbot(), sheet()
    frames.save(f"{out}/boxbot_frames.png")
    front.save(f"{out}/boxbot_pixel.png")
    with open(f"{out}/boxbot_frames.json", "w") as f:
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
    rev.save(f"{out}/boxbot_pixel_sheet.png")
    print("wrote", out)
