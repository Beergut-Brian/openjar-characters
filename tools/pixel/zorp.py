"""Zorp's pixel form for The Hill (Pillow only, drawn in code). See characters/zorp/look.md.

zorp()        front form, 40 x 32, outlined, feet on the bottom row
frame(name)   unoutlined 32 x 32 three-quarter frame facing right, feet on row 30, feet centre x=16
sheet()       the 128 x 224 player sheet
Scale: head + body + legs are 26 px (the 3D at true scale is 32 px without the antennae, so the
whole figure is squeezed to fit the antennae in), antennae 4 px (2 px stalk + 2x2 bobble); 30 px
drawn, 32 px with the outline.
"""
import os

from px import Spr, rgba, up, silhouette, OUT
import jarling_frames

SKIN, SKIN_D = "#9FD6F0", "#7FB9D6"          # skin; stalks and the far-side shade
BOB = "#FFD23F"                               # antenna bobbles
BAND = "#C9CED4"                              # headband
SHIRT, SHIRT_D, PINK, PINK_L = "#FFD23F", "#E8B92A", "#FF7EB9", "#FFA9D0"
SHORTS, SHORTS_D = "#F5F5F2", "#D9D9D4"
SANDAL, SANDAL_D = "#C89A63", "#A57B4B"
WHITE = "#FFFFFF"

HAND = (22, 21)

# leg sets: (back foot dx, back lift), (front foot dx, front lift); body dy
LEGS = {
    "stand": ((0, 0), (0, 0), 0),
    "contact": ((-3, 0), (3, 0), 0),
    "pass": ((-1, 2), (0, 0), 0),
    "contact2": ((3, 0), (-3, 0), 0),
    "pass2": ((0, 0), (1, 2), 0),
    "tuck": ((-1, 2), (1, 2), 0),
    "dangle": ((-1, 0), (1, 0), 0),
    "crouch": ((-2, 0), (2, 0), 1),
}
# name: legs, head dx, back-arm offset, hand (The Hill's POSES for Jeff)
POSES = {
    "idle0": ("stand", 0, (0, 0), (22, 21)),
    "idle1": ("stand", 0, (0, 1), (22, 22)),
    "walk0": ("contact", 0, (1, 0), (22, 21)),
    "walk1": ("pass", 0, (0, 0), (22, 20)),
    "walk2": ("contact2", 0, (-1, 0), (22, 21)),
    "walk3": ("pass2", 0, (0, 0), (22, 20)),
    "jump": ("tuck", 0, (-1, -3), (23, 15)),
    "fall": ("dangle", 0, (-1, -4), (24, 14)),
    "side0": ("stand", -1, (0, 0), (18, 16)),
    "side1": ("contact", 1, (1, -1), (22, 19)),
    "side2": ("stand", 0, (0, 0), (21, 20)),
    "down0": ("stand", 0, (0, -1), (22, 11)),
    "down1": ("crouch", 1, (0, 0), (24, 18)),
    "down2": ("stand", 0, (0, 0), (23, 17)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _head(s, x0, y0, x1, y1):
    """Tall egg head with the silver headband two rows below the crown."""
    s.e(x0, y0, x1, y1, SKIN)
    xs = [x for x in range(x0, x1 + 1) if s.im.getpixel((x, y0 + 2))[3]]
    s.r(xs[0] - 1, y0 + 2, xs[-1] + 1, y0 + 2, BAND)   # worn band: 1 px proud of the head each side


def _antenna(s, base, dx, top_y):
    """1 px stalk rising from `base` outward by `dx` per row, 2x2 bobble on top (a V pair)."""
    x, y = base
    pts = []
    while y > top_y + 1:
        pts.append((x, y)); x += dx; y -= 1
    s.px(SKIN_D, *pts)
    bx = pts[-1][0] if dx > 0 else pts[-1][0] - 1   # bobble over the stalk tip, leaning out
    s.r(bx, top_y, bx + 1, top_y + 1, BOB)


def _print(s, x0, y0, x1, y1):
    """Loud holiday print: scattered pink pixels on the yellow."""
    w, h = x1 - x0 + 1, y1 - y0 + 1
    for i, (u, v) in enumerate(((1, 1), (4, 0), (6, 2), (2, 3), (5, 4), (0, 5), (3, 5), (7, 5))):
        if u < w and v < h:
            s.px(PINK if i % 3 else PINK_L, (x0 + u, y0 + v))


def _eyes(s, xs, y, shut):
    for x in xs:
        if shut:
            s.px(OUT, (x, y + 1), (x + 1, y + 1))
        else:
            s.r(x, y, x + 1, y + 2, OUT); s.px(WHITE, (x, y))


def zorp(view="front"):
    s = Spr(jarling_frames.W, jarling_frames.H)
    _antenna(s, (18, 5), -1, 1); _antenna(s, (22, 5), 1, 1)
    _head(s, 15, 5, 25, 16)
    _eyes(s, (16, 23), 10, False)
    s.px(OUT, (20, 14), (20, 15))                       # small amazed "o"
    s.r(14, 17, 26, 18, SHIRT)                          # shoulders + short sleeves
    s.r(17, 17, 23, 22, SHIRT)
    s.px(SKIN, (19, 17), (20, 17), (21, 17), (20, 18))  # open collar
    _print(s, 17, 17, 23, 22); s.px(PINK, (14, 17), (26, 18))
    for x in (14, 25):                                  # arms, hands
        s.r(x, 19, x + 1, 22, SKIN)
    s.r(17, 23, 23, 25, SHORTS); s.cut(20, 25, 20, 25)
    for x in (17, 22):
        s.r(x, 26, x + 1, 28, SKIN)
    for x0 in (16, 21):                                 # sandals: foot, strap, sole
        s.r(x0, 29, x0 + 3, 29, SKIN); s.px(SANDAL, (x0 + 1, 29) if x0 == 16 else (x0 + 2, 29))
        s.r(x0, 30, x0 + 3, 30, SANDAL)
    return jarling_frames.fin(s)


def _leg(s, hip_x, hip_y, fdx, lift, skin, sole):
    ax, ay = hip_x + fdx, 28 - lift
    for x, y in _line(hip_x, hip_y, ax, ay):
        s.r(x, y, x + 1, y, skin)
    s.r(ax, ay + 1, ax + 2, ay + 1, skin); s.px(sole, (ax + 1, ay + 1))
    s.r(ax, ay + 2, ax + 3, ay + 2, sole)


def _arm(s, shoulder, hand, skin, sleeve):
    for x, y in _line(*shoulder, *hand):
        s.r(x, y, x + 1, y + 1, skin)
    s.r(shoulder[0], shoulder[1], shoulder[0] + 1, shoulder[1] + 1, sleeve)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, skin)


def frame(name, eyes_shut=False):
    legs, hdx, (bax, bay), hand = POSES[name]
    (bdx, blift), (fdx, flift), dy = LEGS[legs]
    s = Spr(jarling_frames.FW, jarling_frames.FH)
    # back arm and back leg (shaded), then torso, front leg, head, front arm
    _arm(s, (12, 17 + dy), (11 + bax, 21 + bay + dy), SKIN_D, SHIRT_D)
    _leg(s, 13, 26 + dy, bdx, blift, SKIN_D, SANDAL_D)
    s.r(12, 17 + dy, 19, 22 + dy, SHIRT)
    s.px(SKIN, (17, 17 + dy), (18, 17 + dy))             # open collar toward the face
    _print(s, 12, 17 + dy, 19, 22 + dy)
    s.r(12, 23 + dy, 19, 25 + dy, SHORTS); s.px(SHORTS_D, (15, 25 + dy))
    _leg(s, 17, 26 + dy, fdx, flift, SKIN, SANDAL)
    hx, top = 11 + hdx, 1 + dy
    _antenna(s, (hx + 3, top + 4), -1, top); _antenna(s, (hx + 7, top + 4), 1, top)
    _head(s, hx, top + 4, hx + 10, top + 15)
    _eyes(s, (hx + 4, hx + 8), top + 8, eyes_shut)
    if not eyes_shut:
        s.px(OUT, (hx + 7, top + 13), (hx + 7, top + 14))   # small amazed "o"
    else:
        s.px(OUT, (hx + 7, top + 14))
    _arm(s, (18, 17 + dy), hand, SKIN, SHIRT)
    s.px(PINK, (18, 18 + dy))
    im = s.im
    assert not any(im.getpixel((x, y))[3] for x in range(32) for y in (0, 31)), name
    assert not any(im.getpixel((x, y))[3] for y in range(32) for x in (0, 31)), name
    return im


def sheet():
    return jarling_frames.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = os.path.join("characters", "zorp", "refs", "pixel"); os.makedirs(out, exist_ok=True)
    front, sh = zorp(), sheet()
    sh.save(os.path.join(out, "zorp_frames.png")); front.save(os.path.join(out, "zorp_pixel.png"))
    with open(os.path.join(out, "zorp_frames.json"), "w") as f:
        json.dump(jarling_frames.manifest(HAND), f, indent=2); f.write("\n")
    sil = silhouette(front)
    bb = sil.getbbox(); sil = sil.crop(bb)
    k = 16 / sil.height
    small = sil.resize((max(1, round(sil.width * k)), 16), Image.BOX)
    small.putalpha(small.getchannel("A").point(lambda v: 255 if v >= 100 else 0))
    rv = Image.new("RGBA", (16 + 320 + 16 + 512 + 16, 16 + 896 + 16), rgba("#F6EFE0"))
    rv.alpha_composite(up(front, 8), (16, 16))
    rv.alpha_composite(up(sh, 4), (16 + 320 + 16, 16))
    rv.alpha_composite(front, (16, 16 + 256 + 24))
    rv.alpha_composite(up(front, 2), (16 + 56, 16 + 256 + 24))
    rv.alpha_composite(up(small, 4), (16 + 56 + 96, 16 + 256 + 24))
    rv.save(os.path.join(out, "zorp_pixel_sheet.png"))
    print("PIXEL zorp", front.getbbox(), "front height", front.getbbox()[3] - front.getbbox()[1])
