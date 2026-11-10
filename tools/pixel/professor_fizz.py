"""Professor Fizz's pixel form for The Hill (Pillow only, drawn in code).

professor_fizz(view="front")  front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet

32 px tall with the outline (the 3D at true scale is 36 px with the hair, squeezed to the frame):
hair spray 6 rows, head 10 (hair/goggles on the forehead, a skin row, scorched brow, eyes, grin, chin),
lab coat 8, pants 3, sock 1, shoes 2. The goggles sit on the forehead with a skin row between them and the
eyes; one brow only (her left), a dark jagged scorch mark. Socks: her left orange, her right blue.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#F7CFAE", "#DDAE8C"
HAIR, HAIR_D = "#F7F7F2", "#D9D9D2"
BRASS, LENS, LENS_L = "#B8862E", "#9FD3E6", "#E6F5FA"
BROW = "#3A2E2A"
COAT, COAT_D = "#F4F5F2", "#D5D8D6"
PURPLE = "#7B3FB5"
PANTS, PANTS_D = "#5E2F94", "#4A2478"
SOCK_L, SOCK_R = "#FFB627", "#3FA7D6"      # her left (orange), her right (blue)
SHOE, SHOE_L = "#1B1B20", "#44444E"
MOUTH = "#6A2232"
EYE_HI = "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# (jump has no lift: the hair already starts on row 1; the tucked feet carry the jump)
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

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs 3 px wide
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

# hair spikes (tip x, tip row, base x) for the three-quarter frame, back to front; the outer ones lean out
SPIKES = [(8, 3, 10), (13, 1, 13), (16, 4, 16), (19, 2, 19)]
FRONT_SPIKES = [(12, 2, 14), (17, 1, 17), (20, 4, 20), (23, 1, 22), (27, 4, 25)]


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _spikes(s, spikes, base, dx=0, dy=0):
    """A jagged white spray: each spike 1 px at its tip, then 2 px (shaded on its left), down to the base row,
    with 1 px gaps between spikes so the spray never closes into a crown."""
    for tx, top, bx in spikes:
        for y in range(top + dy, base + dy + 1):
            k = y - top - dy
            x = round(tx + (bx - tx) * k / max(1, base - top)) + dx
            if k == 0:
                s.px(HAIR, (x, y))
            else:
                s.r(x, y, x + 1, y, HAIR); s.px(HAIR_D, (x, y))


def _leg(s, hx, fx, fy, top, sock, back=False):
    """One leg from the pants band (row `top`) to the shoe sole (row fy): pants, one sock row, black shoe."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y >= fy - 1:                                # shoe, toe to the right
            s.r(x, y, x + 3, y, SHOE)
            if y == fy - 1 and not back:
                s.px(SHOE_L, (x + 2, y))
        elif y == fy - 2:
            s.r(x, y, x + 2, y, sock)
        else:
            s.r(x, y, x + 2, y, PANTS_D if back else PANTS)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 26 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm: shaded long sleeve, skin hand
    pts = _line(9, 18 + oy, 8 + bax, 22 + oy + bay)
    for x, y in pts:
        s.r(x, y, x + 1, y + 1, COAT_D)
    s.r(pts[-1][0], pts[-1][1] + 1, pts[-1][0] + 1, pts[-1][1] + 1, SKIN_D)
    # legs: near leg (her left) orange sock, far leg blue
    _leg(s, bh, bf, by_ - lift, hip, SOCK_R, back=True)
    _leg(s, fh, ff, fy_ - lift, hip, SOCK_L)
    s.r(10, hip - 1, 21, hip - 1, PANTS); s.r(10, hip - 1, 12, hip - 1, PANTS_D)
    # lab coat
    y0, y1 = 17 + oy, 24 + oy
    s.r(10, y0, 21, y1, COAT); s.r(9, y0 + 1, 22, y1, COAT)
    s.r(9, y0 + 1, 10, y1, COAT_D); s.r(11, y1, 21, y1, COAT_D)          # back edge + hem shade
    s.px(PURPLE, (15, y0), (19, y0), (16, y0 + 1), (18, y0 + 1), (17, y0 + 2))   # collar V
    s.px(SKIN, (16, y0), (17, y0), (18, y0), (17, y0 + 1))
    s.px(PURPLE, (17, y0 + 4), (17, y0 + 6))                            # buttons
    # head (three-quarter, face to the right)
    hx, hy = hdx, oy
    s.r(10 + hx, 7 + hy, 21 + hx, 15 + hy, SKIN)
    s.r(11 + hx, 16 + hy, 20 + hx, 16 + hy, SKIN)
    s.px(SKIN_D, (11 + hx, 16 + hy), (20 + hx, 16 + hy))
    # hair: spray on top, a cap over the crown, white at the back and side down to the ear
    _spikes(s, SPIKES, 5, hx, hy)
    s.r(10 + hx, 6 + hy, 21 + hx, 7 + hy, HAIR)
    s.r(9 + hx, 7 + hy, 12 + hx, 14 + hy, HAIR); s.px(HAIR_D, (9 + hx, 12 + hy), (9 + hx, 13 + hy), (9 + hx, 14 + hy), (10 + hx, 14 + hy))
    s.px(HAIR, (13 + hx, 8 + hy), (13 + hx, 9 + hy))
    s.px(SKIN_D, (12 + hx, 11 + hy), (12 + hx, 12 + hy), (13 + hx, 12 + hy))   # ear
    s.px(HAIR, (12 + hx, 10 + hy))
    # goggles on the forehead: strap row going back, one round lens at the front right
    s.r(9 + hx, 9 + hy, 17 + hx, 9 + hy, BRASS)
    s.r(18 + hx, 7 + hy, 21 + hx, 9 + hy, BRASS)
    s.cut(18 + hx, 7 + hy, 18 + hx, 7 + hy); s.px(HAIR, (18 + hx, 7 + hy))
    s.r(19 + hx, 8 + hy, 20 + hx, 9 + hy, LENS); s.px(LENS_L, (19 + hx, 8 + hy))
    # face: skin row 11, scorched brow over the near eye on row 11, eyes 12-13, grin 14-15
    if eyes_shut:
        s.px(OUT, (14 + hx, 13 + hy), (15 + hx, 13 + hy), (18 + hx, 13 + hy), (19 + hx, 12 + hy), (20 + hx, 13 + hy))
    else:
        s.px(OUT, (15 + hx, 12 + hy), (15 + hx, 13 + hy), (19 + hx, 12 + hy), (20 + hx, 12 + hy), (19 + hx, 13 + hy), (20 + hx, 13 + hy))
        s.px(EYE_HI, (20 + hx, 12 + hy))
    s.px(BROW, (18 + hx, 11 + hy), (19 + hx, 11 + hy), (21 + hx, 11 + hy))
    s.px(SKIN_D, (21 + hx, 13 + hy))                                  # nose bump
    s.r(17 + hx, 14 + hy, 20 + hx, 14 + hy, MOUTH); s.r(18 + hx, 15 + hy, 19 + hx, 15 + hy, MOUTH)
    # front arm: long white sleeve to a skin hand
    pts = _line(21, 18 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, COAT)
        s.px(COAT_D, (x, y + 1))
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def professor_fizz(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: long white sleeves, skin hands
    for x in (11, 27):
        s.r(x, 18, x + 1, 22, COAT); s.px(COAT_D, (x if x < 20 else x + 1, 19), (x if x < 20 else x + 1, 21))
        s.r(x, 23, x + 1, 24, SKIN); s.px(SKIN_D, (x, 24), (x + 1, 24))
    # legs: pants, one sock row (image left = her right = blue, image right = her left = orange), shoes
    for x, sock in ((15, SOCK_R), (22, SOCK_L)):
        s.r(x, 26, x + 2, 27, PANTS); s.r(x, 28, x + 2, 28, sock)
    s.px(PANTS_D, (17, 26), (17, 27), (22, 26), (22, 27))
    s.r(14, 29, 18, 30, SHOE); s.r(21, 29, 25, 30, SHOE); s.px(SHOE_L, (15, 29), (22, 29))
    s.r(14, 25, 25, 25, PANTS); s.r(19, 25, 20, 25, PANTS_D)
    # lab coat
    s.r(14, 17, 25, 24, COAT); s.r(13, 18, 26, 24, COAT)
    s.r(13, 18, 13, 24, COAT_D); s.r(26, 18, 26, 24, COAT_D); s.r(14, 24, 25, 24, COAT_D)
    s.px(PURPLE, (16, 17), (17, 18), (18, 19), (23, 17), (22, 18), (21, 19), (19, 20), (20, 20))   # collar V
    s.r(17, 17, 22, 17, SKIN); s.r(18, 18, 21, 18, SKIN); s.r(19, 19, 20, 19, SKIN)
    s.px(PURPLE, (19, 22), (20, 22))                                   # button
    # head
    s.r(14, 7, 25, 15, SKIN); s.r(15, 16, 24, 16, SKIN); s.px(SKIN_D, (15, 16), (24, 16))
    s.px(SKIN_D, (13, 11), (13, 12), (26, 11), (26, 12))                # ears
    # hair: spray + crown + sides
    _spikes(s, FRONT_SPIKES, 5)
    s.r(14, 6, 25, 7, HAIR); s.r(13, 7, 14, 10, HAIR); s.r(25, 7, 26, 10, HAIR)
    s.px(HAIR_D, (13, 9), (13, 10), (26, 9), (26, 10))
    # goggles: brass row across the forehead with two round lenses
    s.r(13, 8, 26, 9, BRASS)
    for lx in (16, 22):
        s.r(lx - 1, 7, lx + 2, 9, BRASS); s.px(HAIR, (lx - 1, 7), (lx + 2, 7))
        s.r(lx, 8, lx + 1, 9, LENS); s.px(LENS_L, (lx, 8))
    # face: brow over her left eye only (image right), wide eyes, grin
    s.px(OUT, (16, 12), (17, 12), (16, 13), (17, 13), (22, 12), (23, 12), (22, 13), (23, 13))
    s.px(EYE_HI, (17, 12), (23, 12))
    s.px(BROW, (21, 11), (22, 11), (24, 11))
    s.px(SKIN_D, (19, 13), (20, 13))
    s.r(18, 14, 21, 14, MOUTH); s.r(19, 15, 20, 15, MOUTH)
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/professor_fizz/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = professor_fizz(), sheet()
    frames.save(f"{out}/professor_fizz_frames.png")
    front.save(f"{out}/professor_fizz_pixel.png")
    with open(f"{out}/professor_fizz_frames.json", "w") as f:
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
    rev.save(f"{out}/professor_fizz_pixel_sheet.png")
    print("wrote", out)
