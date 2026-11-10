"""Professor Fizz's pixel form for The Hill (Pillow only, drawn in code).

professor_fizz(view="front")  front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet

32 px tall with the outline (the 3D at true scale is 36 px with the hair, squeezed to the frame):
hair mass 5 rows (tufts merged at the base over 2 solid rows), head 12 (rimmed goggles on the forehead, a skin
row, scorched brow, eyes, a skin row, grin, chin), lab coat 7, pants 3, sock 1, shoes 2. One brow only (her
left), a dark zigzag scorch mark apart from the eye. Socks: her left orange, her right blue.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#F7CFAE", "#DDAE8C"
HAIR, HAIR_D = "#F7F7F2", "#D9D9D2"
BRASS, STRAP, LENS, LENS_L = "#B8862E", "#8A6420", "#9FD3E6", "#E6F5FA"
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

# hair: rows of (W hair, S shade, . empty) from column X0, top row 1. Four pointed locks of uneven height
# (tips off-centre, notches down to the last row, which the outline turns into dark gaps between the locks): spiky hair, not a crown (no band, uneven
# points) and not a chef hat (no flat puffy top). Director's redraw after the read check.
FRONT_HAIR = (10, [
    "........W......W....",
    "........WW..W.SW....",
    "....W..SWW.SW.SWW...",
    "...SWW.SWW.SWWSWW...",
    "...SWWWWWWWWWWWWW...",
])
FRAME_HAIR = (7, [
    ".......W......W...",
    ".......WW..W.SW...",
    "...W..SWW.SW.SWW..",
    "..SWW.SWW.SWWSWW..",
    "..SWWWWWWWWWWWWW..",
])


def _hair(s, mass, dx=0, dy=0):
    x0, rows = mass
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c != ".":
                s.px(HAIR if c == "W" else HAIR_D, (x0 + j + dx, 1 + i + dy))


def _lens(s, x, y):
    """A 2 x 2 lens at (x, y) with a 1 px brass rim (corners left open, so it reads round)."""
    s.r(x, y - 1, x + 1, y - 1, BRASS); s.r(x, y + 2, x + 1, y + 2, BRASS)
    s.r(x - 1, y, x - 1, y + 1, BRASS); s.r(x + 2, y, x + 2, y + 1, BRASS)
    s.r(x, y, x + 1, y + 1, LENS); s.px(LENS_L, (x, y))


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


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
    y0, y1 = 18 + oy, 24 + oy
    s.r(10, y0, 21, y1, COAT); s.r(9, y0 + 1, 22, y1, COAT)
    s.r(9, y0 + 1, 10, y1, COAT_D); s.r(11, y1, 21, y1, COAT_D)          # back edge + hem shade
    s.px(PURPLE, (15, y0), (19, y0), (16, y0 + 1), (18, y0 + 1), (17, y0 + 2))   # collar V
    s.px(SKIN, (16, y0), (17, y0), (18, y0), (17, y0 + 1))
    s.px(PURPLE, (17, y0 + 3), (17, y0 + 5))                            # buttons
    # head (three-quarter, face to the right): hair mass rows 1-5, goggles 6-9, skin row 10, brow 11-12,
    # eyes 13-14, grin 16-17, chin 17
    hx, hy = hdx, oy
    s.r(10 + hx, 6 + hy, 21 + hx, 16 + hy, SKIN)
    s.r(11 + hx, 17 + hy, 20 + hx, 17 + hy, SKIN)
    s.px(SKIN_D, (11 + hx, 17 + hy), (20 + hx, 17 + hy))
    _hair(s, FRAME_HAIR, hx, hy)
    s.r(9 + hx, 6 + hy, 12 + hx, 14 + hy, HAIR); s.px(HAIR, (13 + hx, 6 + hy))     # back and side of the head
    s.px(HAIR_D, (9 + hx, 11 + hy), (9 + hx, 12 + hy), (9 + hx, 13 + hy), (9 + hx, 14 + hy), (10 + hx, 14 + hy), (11 + hx, 8 + hy))
    s.px(SKIN_D, (12 + hx, 12 + hy), (12 + hx, 13 + hy), (13 + hx, 13 + hy))     # ear
    # goggles on the forehead: two rimmed lenses, a 1 px bridge, the strap back over the white hair
    _lens(s, 14 + hx, 7 + hy); _lens(s, 19 + hx, 7 + hy)
    s.px(BRASS, (17 + hx, 7 + hy))
    s.r(9 + hx, 7 + hy, 12 + hx, 7 + hy, STRAP)
    # face: both eyes alike; the scorch mark is a separate zigzag over the near eye, touching it only diagonally
    if eyes_shut:
        s.px(OUT, (14 + hx, 14 + hy), (15 + hx, 14 + hy), (19 + hx, 14 + hy), (20 + hx, 14 + hy))
    else:
        for ex in (14, 19):
            s.r(ex + hx, 13 + hy, ex + 1 + hx, 14 + hy, OUT); s.px(EYE_HI, (ex + 1 + hx, 13 + hy))
    s.px(BROW, (18 + hx, 12 + hy), (19 + hx, 11 + hy), (20 + hx, 11 + hy), (21 + hx, 12 + hy))
    s.px(SKIN_D, (21 + hx, 14 + hy))                                  # nose bump
    s.r(17 + hx, 16 + hy, 19 + hx, 16 + hy, MOUTH); s.r(18 + hx, 17 + hy, 19 + hx, 17 + hy, MOUTH)   # small grin, 3 px
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
    s.r(14, 18, 25, 24, COAT); s.r(13, 19, 26, 24, COAT)
    s.r(13, 19, 13, 24, COAT_D); s.r(26, 19, 26, 24, COAT_D); s.r(14, 24, 25, 24, COAT_D)
    s.px(PURPLE, (16, 18), (17, 19), (18, 20), (23, 18), (22, 19), (21, 20), (19, 21), (20, 21))   # collar V
    s.r(17, 18, 22, 18, SKIN); s.r(18, 19, 21, 19, SKIN); s.r(19, 20, 20, 20, SKIN)
    s.px(PURPLE, (19, 23), (20, 23))                                   # button
    # head: hair mass rows 1-5, goggles 6-9, skin row 10, brow 11-12, eyes 13-14, grin 16-17
    s.r(14, 6, 25, 16, SKIN); s.r(15, 17, 24, 17, SKIN); s.px(SKIN_D, (15, 17), (24, 17))
    s.px(SKIN_D, (13, 12), (13, 13), (26, 12), (26, 13))                # ears
    _hair(s, FRONT_HAIR)
    s.r(13, 6, 14, 11, HAIR); s.r(25, 6, 26, 11, HAIR)                 # down both sides to the ears
    s.px(HAIR_D, (13, 9), (13, 10), (13, 11), (26, 9), (26, 10), (26, 11))
    # goggles: two rimmed lenses, a bridge, darker strap from the rims to the head edge over the side hair
    _lens(s, 16, 7); _lens(s, 22, 7)
    s.r(19, 7, 20, 7, BRASS)
    s.r(13, 7, 14, 7, STRAP); s.r(25, 7, 26, 7, STRAP)
    # face: both eyes alike, scorch zigzag over her left eye only (image right), touching it only diagonally
    for ex in (16, 22):
        s.r(ex, 13, ex + 1, 14, OUT); s.px(EYE_HI, (ex + 1, 13))
    s.px(BROW, (21, 12), (22, 11), (23, 11), (24, 12))
    s.px(SKIN_D, (19, 14), (20, 14))
    s.r(18, 16, 21, 16, MOUTH); s.r(19, 17, 20, 17, MOUTH)
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
