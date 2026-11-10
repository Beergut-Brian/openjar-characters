"""Coach Whistle's pixel form for The Hill (Pillow only, drawn in code).

coach_whistle(view="front")  front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

29 px tall (1.12 m with the cap, traced from refs/jarling/coach_whistle_side_sprite.png):
cap 5 rows, face 8, barrel torso 9, shorts 2, navy cuff 1, white socks 2, sneakers 2.
The silver whistle hangs at the bottom of a yellow cord V, 6 rows below the mouth, on a dark patch
so it reads on the stripes. It is never held or near the mouth.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#D99E6E", "#B97F55"
HAIR = "#3A2418"
CAP, CAP_L = "#1E2B4D", "#34477A"
BLK, WHT = "#1A1A1E", "#F5F5F2"
SHORTS, SHORTS_D = "#8A8E96", "#6F737B"
SHOE, SOLE = "#F7F7F5", "#B9BDC4"
CUFF = "#1E2B4D"
WHISTLE, WHISTLE_D = "#C9CED4", "#7D848D"
CORD = "#F2C230"
MOUTH, TONGUE = "#6A2232", "#F2848C"

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

# leg sets: ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs are 3 px wide
LEGS = {
    "stand": ((11, 11, 30), (17, 17, 30)),
    "contact": ((11, 8, 30), (17, 20, 30)),
    "pass": ((12, 10, 28), (16, 16, 30)),
    "contact2": ((11, 15, 30), (17, 12, 30)),
    "pass2": ((11, 12, 30), (17, 16, 28)),
    "tuck": ((11, 10, 28), (17, 18, 28)),
    "dangle": ((11, 10, 30), (17, 18, 30)),
    "crouch": ((11, 8, 30), (17, 20, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the shorts hem (row `top`) to the shoe sole (row fy): navy cuff, white sock, sneaker."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y >= fy - 1:                                # sneaker, toe to the right
            s.r(x, y, x + 3, y, SOLE if y == fy else SHOE)
        elif i == 0:
            s.r(x, y, x + 2, y, CUFF)
        else:
            s.r(x, y, x + 2, y, SOLE if back else SHOE)
            if not back:
                s.px(SOLE, (x, y))


def _whistle(s, x, y):
    """2 x 2 silver whistle at (x, y) on a dark patch, its mouthpiece pixel darker."""
    s.r(x - 1, y, x + 2, y + 2, BLK)
    s.r(x, y, x + 1, y + 1, WHISTLE)
    s.px(WHISTLE_D, (x + 1, y + 1))


def _torso(s, x0, x1, y0, y1, phase=0):
    """Barrel torso with 1 px vertical black / white stripes."""
    for y in range(y0, y1 + 1):
        a, b = x0, x1
        if y == y0 or y == y1:
            a, b = x0 + 1, x1 - 1 if y == y1 else x1 - 1
        if y == y0:
            a, b = x0 + 2, x1 - 2
        for x in range(a, b + 1):
            s.px(BLK if (x + phase) % 2 == 0 else WHT, (x, y))


def _cord(s, l, r, wx, wy):
    for x, y in _line(l[0], l[1], wx - 1, wy - 1) + _line(r[0], r[1], wx + 2, wy - 1):
        s.px(CORD, (x, y))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift                                    # upper-body offset
    hip = 26 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm, legs, shorts
    for x, y in _line(9, 17 + oy, 8 + bax, 21 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(8, 16 + oy, 9, 17 + oy, BLK)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(10, hip - 2, 21, hip - 1, SHORTS); s.r(10, hip - 1, 13, hip - 1, SHORTS_D); s.px(SHORTS_D, (16, hip - 1))
    # torso + whistle
    _torso(s, 9, 22, 15 + oy, 23 + oy)
    s.r(13, 15 + oy, 18, 15 + oy, BLK)                  # collar
    wx, wy = 17, 19 + oy
    _cord(s, (12, 15 + oy), (21, 15 + oy), wx, wy)
    _whistle(s, wx, wy)
    # head (three-quarter, face to the right)
    hx, hy = hdx, oy
    s.r(10 + hx, 6 + hy, 21 + hx, 13 + hy, SKIN)
    s.r(11 + hx, 14 + hy, 20 + hx, 14 + hy, SKIN)
    s.r(10 + hx, 6 + hy, 12 + hx, 9 + hy, HAIR); s.px(HAIR, (10 + hx, 10 + hy))
    s.px(SKIN_D, (11 + hx, 10 + hy), (11 + hx, 11 + hy), (12 + hx, 11 + hy))     # ear
    s.r(11 + hx, 2 + hy, 20 + hx, 2 + hy, CAP); s.r(10 + hx, 3 + hy, 21 + hx, 5 + hy, CAP)
    s.r(10 + hx, 6 + hy, 23 + hx, 6 + hy, CAP)          # brim: 2 px past the face
    s.px(CAP_L, (13 + hx, 3 + hy), (14 + hx, 3 + hy), (12 + hx, 4 + hy), (22 + hx, 6 + hy), (23 + hx, 6 + hy))
    if eyes_shut:
        s.px(OUT, (14 + hx, 10 + hy), (15 + hx, 9 + hy), (16 + hx, 10 + hy), (19 + hx, 10 + hy), (20 + hx, 9 + hy), (21 + hx, 10 + hy))
    else:
        s.px(OUT, (15 + hx, 9 + hy), (15 + hx, 10 + hy), (19 + hx, 9 + hy), (19 + hx, 10 + hy))
    s.px(SKIN_D, (21 + hx, 11 + hy))                     # nose bump
    s.r(16 + hx, 12 + hy, 19 + hx, 13 + hy, MOUTH); s.px(TONGUE, (17 + hx, 13 + hy), (18 + hx, 13 + hy))
    # front arm: black sleeve, then skin to a mitten hand
    sh = (21, 16 + oy)
    pts = _line(sh[0], sh[1], hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, BLK if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def coach_whistle(view="front"):
    s = Spr(jf.W, jf.H)
    # arms (behind the torso edge)
    for x in (11, 27):
        s.r(x, 16, x + 1, 18, BLK); s.r(x, 19, x + 1, 22, SKIN); s.px(SKIN_D, (x, 22), (x + 1, 22))
    # legs
    for x in (15, 22):
        s.r(x, 26, x + 2, 26, CUFF); s.r(x, 27, x + 2, 28, SHOE)
    s.r(14, 29, 18, 29, SHOE); s.r(21, 29, 25, 29, SHOE); s.r(14, 30, 18, 30, SOLE); s.r(21, 30, 25, 30, SOLE)
    s.r(14, 24, 25, 25, SHORTS); s.r(19, 25, 20, 25, SHORTS_D)
    _torso(s, 13, 26, 15, 23, phase=1)
    s.r(17, 15, 22, 15, BLK)
    _cord(s, (15, 15), (24, 15), 19, 19)
    _whistle(s, 19, 19)
    # head
    s.r(14, 6, 25, 13, SKIN); s.r(15, 14, 24, 14, SKIN)
    s.r(14, 7, 14, 9, HAIR); s.r(25, 7, 25, 9, HAIR)
    s.px(SKIN_D, (13, 9), (13, 10), (26, 9), (26, 10))                          # ears
    s.r(15, 2, 24, 2, CAP); s.r(14, 3, 25, 5, CAP); s.r(12, 6, 27, 6, CAP)      # dome + front brim
    s.px(CAP_L, (17, 3), (18, 3), (16, 4), (19, 6), (20, 6))
    s.px(OUT, (17, 9), (17, 10), (22, 9), (22, 10))
    s.px(SKIN_D, (19, 11), (20, 11))
    s.r(18, 12, 21, 13, MOUTH); s.px(TONGUE, (19, 13), (20, 13))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/coach_whistle/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = coach_whistle(), sheet()
    frames.save(f"{out}/coach_whistle_frames.png")
    front.save(f"{out}/coach_whistle_pixel.png")
    with open(f"{out}/coach_whistle_frames.json", "w") as f:
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
    rev.save(f"{out}/coach_whistle_pixel_sheet.png")
    print("wrote", out)
