"""Granny Gravel's pixel form for The Hill (Pillow only, drawn in code).

granny_gravel(view="front")   front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet

30 px tall with the outline and the bun (traced from refs/jarling/granny_gravel_side_sprite.png):
bun 3 rows (its base sits in the hair dome), hair 4 with the safety goggles pushed up into it, face 6 (two skin rows
between the goggles and the dot eyes), cardigan 6, A-line skirt 7, sneakers 2. The skirt hides the legs: in the walk
and dig frames only the sneakers step and the hem sways 1 px.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#F7CFAE", "#DDAE8C"
HAIR, HAIR_D = "#F2F0EA", "#CFCBC2"
GOG, LENS, LENS_L = "#4A4F5A", "#9FD8F0", "#D8F1FA"
BROW = "#B9B4AE"
CHEEK = "#F2A9A0"
MOUTH = "#6A2232"
CARD, CARD_D = "#B9A3D9", "#9C84C4"
BUTTON = "#F2F0EA"
SKIRT, SKIRT_D = "#8C8F96", "#74777E"
SHOE, SOLE = "#FFD93B", "#D9B21E"

HAND = (22, 21)

# name: feet, lift, head dx, back-arm (dx, dy), hand (x, y), body drop, hem sway  (hands from The Hill's POSES)
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21), 0, 0),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22), 1, 0),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21), 0, 1),
    "walk1": ("pass", 0, 0, (0, 0), (22, 20), 0, 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21), 0, -1),
    "walk3": ("pass2", 0, 0, (0, 0), (22, 20), 0, 0),
    "jump": ("tuck", 1, 0, (-1, -3), (23, 15), 0, 0),
    "fall": ("dangle", 0, 0, (-1, -4), (24, 14), 0, 0),
    "side0": ("stand", 0, -1, (0, 0), (18, 16), 0, 0),
    "side1": ("contact", 0, 1, (1, -1), (22, 19), 0, 1),
    "side2": ("stand", 0, 0, (0, 0), (21, 20), 0, 0),
    "down0": ("stand", 0, 0, (0, -1), (22, 11), 0, 0),
    "down1": ("crouch", 0, 1, (0, 0), (24, 18), 1, -1),
    "down2": ("stand", 0, 0, (0, 0), (23, 17), 0, 0),
}

# sneakers only (the skirt hides the legs): ((back foot x, sole row), (front foot x, sole row)); 4 px, toe right.
# A sole row above 30 lifts the foot up under the hem, so only part of it shows.
FEET = {
    "stand": ((11, 30), (16, 30)),
    "contact": ((8, 30), (19, 30)),
    "pass": ((11, 29), (16, 30)),
    "contact2": ((15, 30), (11, 30)),
    "pass2": ((11, 30), (16, 29)),
    "tuck": ((10, 29), (17, 29)),
    "dangle": ((10, 30), (17, 30)),
    "crouch": ((8, 30), (19, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _shoe(s, x, y):
    s.r(x, y - 1, x + 3, y - 1, SHOE); s.r(x, y, x + 3, y, SOLE)


def _skirt(s, x0, x1, top, hem, sway=0, folds=()):
    """Long grey A-line skirt over columns x0..x1 at the waist, 1 px wider each side for the 2 rows above the
    3-row hem band, 2 px wider for the hem band; `sway` shifts the hem band sideways by 1 px."""
    for y in range(top, hem + 1):
        k = hem - y
        w, dx = (2, sway) if k <= 2 else (1, 0) if k <= 4 else (0, 0)
        s.r(x0 - w + dx, y, x1 + w + dx, y, SKIRT)
        s.px(SKIRT_D, (x0 - w + dx, y), (x0 - w + 1 + dx, y))
        for fx in folds:
            if k <= 4:
                s.px(SKIRT_D, (fx + (dx if k <= 2 else 0), y))
    s.r(x0 - 2 + sway, hem, x1 + 2 + sway, hem, SKIRT_D)


def frame(name, eyes_shut=False):
    feet, lift, hdx, (bax, bay), hand, drop, sway = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    (bx, by_), (fx, fy_) = FEET[feet]
    # back arm: shaded lavender sleeve, skin hand
    pts = _line(9, 18 + oy, 8 + bax, 21 + oy + bay)
    for x, y in pts:
        s.r(x, y, x + 1, y + 1, CARD_D)
    s.r(pts[-1][0], pts[-1][1] + 2, pts[-1][0] + 1, pts[-1][1] + 2, SKIN_D)
    # sneakers first, the skirt hem covers whatever is lifted
    _shoe(s, bx, by_ - lift); s.px(SOLE, (bx, by_ - 1 - lift))
    _shoe(s, fx, fy_ - lift)
    _skirt(s, 10, 21, 22 + oy, 28 - lift, sway, folds=(15,))
    # cardigan
    y0, y1 = 17 + oy, 21 + oy
    s.r(10, y0, 21, y1, CARD); s.r(9, y0 + 1, 22, y1, CARD)
    s.r(9, y0 + 1, 10, y1, CARD_D)
    s.px(CARD_D, (16, y0), (18, y0), (17, y0 + 1))                     # V neck
    s.px(BUTTON, (17, y0 + 2), (17, y0 + 4))                           # centre button line
    s.px(CARD_D, (17, y0 + 3))
    # head (three-quarter, face to the right): bun rows 3-5 on a 2 px neck (row 6), dome from row 7
    hx, hy = hdx, oy
    s.r(10 + hx, 8 + hy, 21 + hx, 15 + hy, SKIN)
    s.r(11 + hx, 16 + hy, 20 + hx, 16 + hy, SKIN); s.px(SKIN_D, (11 + hx, 16 + hy), (20 + hx, 16 + hy))
    s.r(11 + hx, 7 + hy, 20 + hx, 7 + hy, HAIR)
    s.r(10 + hx, 8 + hy, 21 + hx, 10 + hy, HAIR)
    s.r(9 + hx, 8 + hy, 13 + hx, 14 + hy, HAIR)
    s.px(HAIR_D, (9 + hx, 12 + hy), (9 + hx, 13 + hy), (9 + hx, 14 + hy), (10 + hx, 14 + hy), (11 + hx, 7 + hy), (20 + hx, 7 + hy))
    s.r(13 + hx, 3 + hy, 16 + hx, 5 + hy, HAIR); s.cut(13 + hx, 3 + hy, 13 + hx, 3 + hy); s.cut(16 + hx, 3 + hy, 16 + hx, 3 + hy)
    s.px(HAIR_D, (16 + hx, 4 + hy), (16 + hx, 5 + hy), (15 + hx, 5 + hy))     # bun shade
    s.r(14 + hx, 6 + hy, 15 + hx, 6 + hy, HAIR_D)                               # where the bun is pinned on
    s.px(SKIN_D, (12 + hx, 12 + hy), (12 + hx, 13 + hy), (13 + hx, 13 + hy))     # ear
    s.px(HAIR, (12 + hx, 11 + hy))
    # safety goggles pushed up into the hair: strap row 9 back through the hair, two lenses on the hairline
    s.r(9 + hx, 9 + hy, 21 + hx, 9 + hy, GOG)
    for lx in (14, 19):
        s.r(lx - 1 + hx, 8 + hy, lx + 2 + hx, 10 + hy, GOG)
        s.r(lx + hx, 8 + hy, lx + 1 + hx, 9 + hy, LENS); s.px(LENS_L, (lx + hx, 8 + hy))
    s.px(HAIR, (17 + hx, 10 + hy))
    # face: brows raised (a skin row under them), dot eyes, rosy cheek, tiny smile
    s.px(BROW, (15 + hx, 11 + hy), (19 + hx, 11 + hy))
    if eyes_shut:
        s.px(OUT, (15 + hx, 13 + hy), (16 + hx, 13 + hy), (19 + hx, 13 + hy), (20 + hx, 13 + hy))
    else:
        s.px(OUT, (15 + hx, 13 + hy), (19 + hx, 13 + hy))
    s.px(SKIN_D, (21 + hx, 13 + hy))                                   # nose bump
    s.px(CHEEK, (20 + hx, 14 + hy), (14 + hx, 14 + hy))
    s.px(MOUTH, (17 + hx, 14 + hy), (18 + hx, 15 + hy), (19 + hx, 15 + hy))
    # front arm: lavender sleeve to a skin hand
    pts = _line(21, 18 + oy, hand[0], hand[1])
    for x, y in pts:
        s.r(x, y, x + 1, y + 1, CARD)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def granny_gravel(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: lavender sleeves, skin hands
    for x in (11, 27):
        s.r(x, 18, x + 1, 21, CARD); s.px(CARD_D, (x if x < 20 else x + 1, 19), (x if x < 20 else x + 1, 21))
        s.r(x, 22, x + 1, 23, SKIN); s.px(SKIN_D, (x, 23), (x + 1, 23))
    # sneakers under the skirt hem
    _shoe(s, 15, 30); _shoe(s, 21, 30)
    _skirt(s, 14, 25, 22, 28, 0, folds=(18, 21))
    # cardigan
    s.r(14, 17, 25, 21, CARD); s.r(13, 18, 26, 21, CARD)
    s.r(13, 18, 13, 21, CARD_D); s.r(26, 18, 26, 21, CARD_D)
    s.px(CARD_D, (18, 17), (21, 17), (19, 18), (20, 18))                          # V neck
    s.r(19, 17, 20, 17, SKIN)
    s.px(BUTTON, (19, 19), (20, 19), (19, 21), (20, 21)); s.px(CARD_D, (19, 20), (20, 20))   # centre button line
    # head: bun rows 3-5 on a 2 px neck (row 6), dome from row 7
    s.r(14, 8, 25, 15, SKIN); s.r(15, 16, 24, 16, SKIN); s.px(SKIN_D, (15, 16), (24, 16))
    s.px(SKIN_D, (13, 12), (13, 13), (26, 12), (26, 13))                          # ears
    s.r(15, 7, 24, 7, HAIR); s.r(14, 8, 25, 10, HAIR); s.r(13, 8, 14, 11, HAIR); s.r(25, 8, 26, 11, HAIR)
    s.px(HAIR_D, (13, 10), (13, 11), (26, 10), (26, 11), (15, 7), (24, 7))
    s.r(18, 3, 21, 5, HAIR); s.cut(18, 3, 18, 3); s.cut(21, 3, 21, 3)
    s.px(HAIR_D, (21, 4), (21, 5), (20, 5)); s.r(19, 6, 20, 6, HAIR_D)
    # safety goggles up in the hair: strap row, two framed lenses on the hairline
    s.r(13, 9, 26, 9, GOG)
    for lx in (16, 22):
        s.r(lx - 1, 8, lx + 2, 10, GOG)
        s.r(lx, 8, lx + 1, 9, LENS); s.px(LENS_L, (lx, 8))
    # face: raised brows, dot eyes, rosy cheeks, tiny smile
    s.px(BROW, (16, 11), (23, 11))
    s.px(OUT, (16, 13), (23, 13))
    s.px(CHEEK, (15, 14), (24, 14))
    s.px(SKIN_D, (19, 13), (20, 13))
    s.px(MOUTH, (18, 14), (19, 15), (20, 15), (21, 14))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/granny_gravel/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = granny_gravel(), sheet()
    frames.save(f"{out}/granny_gravel_frames.png")
    front.save(f"{out}/granny_gravel_pixel.png")
    with open(f"{out}/granny_gravel_frames.json", "w") as f:
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
    rev.save(f"{out}/granny_gravel_pixel_sheet.png")
    print("wrote", out)
