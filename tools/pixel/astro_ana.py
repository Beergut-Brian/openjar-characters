"""Astro Ana's pixel form for The Hill (Pillow only, drawn in code). See jarling_frames.py for the rules.

Traced from characters/astro_ana/refs/jarling/astro_ana_side_sprite.png: boots + legs 9 px, torso 8 px,
collar 1 px, head inside the bowl. The 3D body with hair is 30 px; the bowl would add 3 px more, so the
head is drawn 2 px shorter inside a 13 px bowl (body below the collar at true scale, 30 px drawn, 32 with
the outline). The helmet is an opaque pixel bowl: light-blue ring inside the outline, pale glass fill,
white glint at the upper left, white collar row with one orange pixel at the neck.
"""
from PIL import Image
from px import Spr, OUT, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#BF8150", "#9E6740"
HAIR = "#3B2A20"
SUIT, SUIT_D = "#F2F4F6", "#C9D1DA"
ORANGE, ORANGE_D = "#F7941D", "#D2741A"
RING, GLASS, WHITE = "#8FC7E8", "#D8EEF8", "#FFFFFF"
HAND = (22, 21)

LEGEND = {"P": SUIT, "p": SUIT_D, "O": ORANGE, "o": ORANGE_D, "W": WHITE, "w": SUIT_D}
# 18 wide, column 0 at x = 7 (feet centre x = 16); last row on the feet row. Lower case = the far leg.
LEGS = {
    "stand": ["....PPPPPPPPPp....", "....PPPPpPPPPp....", "....PPPp.PPPPp....", "....PPPp.PPPPp....",
              "....PPPp.PPPPp....", "...OOOOo.OOOOOo...", "...OOOOo.OOOOOOo..", "...OOOOo.OOOOOOo..",
              "...WWWWW.WWWWWWW.."],
    "contact": ["....PPPPPPPPPp....", "....PPPPpPPPPp....", "...pppp..PPPPp....", "..pppp....PPPPp...",
                ".pppp......PPPPp..", ".ooo.......OOOOOo.", "ooooo......OOOOOOo", "ooooo......OOOOOOo",
                "wwwww......WWWWWWW"],
    "pass": ["....PPPPPPPPPp....", "....PPPPpPPPPp....", "....pppPPPPPp.....", "...pppp.PPPPp.....",
             "..pppp..PPPPp.....", ".oooo...OOOOOo....", "ooooo...OOOOOOo...", "wwww....OOOOOOo...",
             "........WWWWWWW..."],
    "contact2": ["....PPPPPPPPPp....", "....PPPPpPPPPp....", "...PPPP..ppppp....", "..PPPP....ppppp...",
                 ".PPPP......ppppp..", ".OOO.......oooooo.", "OOOOO......ooooooo", "OOOOO......ooooooo",
                 "WWWWW......wwwwwww"],
    "pass2": ["....PPPPPPPPPp....", "....PPPPpPPPPp....", ".....PPPPppppp....", ".....PPPPp.pppp...",
              ".....PPPPp..pppp..", ".....OOOOOo.oooo..", "....OOOOOOo.ooooo.", "....OOOOOOo.wwww..",
              "....WWWWWWW......."],
    "tuck": ["....PPPPPPPPPp....", "...PPPPpPPPPPPp...", "..PPPPp...PPPPPp..", ".oooo......OOOOo..",
             "ooooo......OOOOOo.", "oooooo.....OOOOOOo", ".wwww......WWWWWW."],
    "dangle": ["....PPPPPPPPPp....", "....PPPPpPPPPp....", "....PPPp.PPPPp....", "...pppp...PPPPp...",
               "...pppp...PPPPp...", "..oooo.....OOOOo..", "..ooooo....OOOOOo.", "..ooooo....OOOOOo.",
               "...www......WWWW.."],
    "crouch": ["...PPPPPPPPPPp....", "..PPPPpPPPPPPPp...", ".pppp.....PPPPPp..", ".oooo......OOOOo..",
               "oooooo.....OOOOOo.", "oooooo.....OOOOOOo", "wwwwww.....WWWWWWW"],
}
# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y)   (The Hill's POSES for Jeff)
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21)),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22)),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21)),
    "walk1": ("pass", 0, 0, (0, 0), (22, 20)),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21)),
    "walk3": ("pass2", 0, 0, (0, 0), (22, 20)),
    "jump": ("tuck", 2, 0, (-1, -3), (23, 15)),
    "fall": ("dangle", 0, 0, (-1, -4), (24, 14)),
    "side0": ("stand", 0, -1, (0, 0), (18, 16)),
    "side1": ("contact", 0, 1, (1, -1), (22, 19)),
    "side2": ("stand", 0, 0, (0, 0), (21, 20)),
    "down0": ("stand", 0, 0, (0, -1), (22, 11)),
    "down1": ("crouch", 0, 1, (0, 0), (24, 18)),
    "down2": ("stand", 0, 0, (0, 0), (23, 17)),
}


BOWL_HALF = [4, 6, 7, 8, 8, 8, 8, 8, 8, 8, 7, 6]   # half width per row of the 17 x 12 bowl (row 12 = collar)


def helmet(s, cx, top, view="front", eyes_shut=False):
    """Bowl, head, puffs and collar: 17 px wide, 13 rows from `top` (the last row is the collar).
    The bowl's edge pixels are the light-blue ring (the outline goes round it), the rest pale glass."""
    G = {}
    inside = {(c, r) for r, h in enumerate(BOWL_HALF) for c in range(8 - h, 9 + h)}
    for c, r in inside:
        edge = any((c + dx, r + dy) not in inside for dx, dy in ((1, 0), (-1, 0), (0, -1))) or (r == 11 and abs(c - 8) > 5)
        G[c, r] = RING if edge else GLASS
    G[5, 1] = G[4, 2] = WHITE                                   # glint, upper left
    put = lambda col, *pts: [G.__setitem__(p, col) for p in pts]
    row = lambda col, r, c0, c1: put(col, *[(c, r) for c in range(c0, c1 + 1)])
    f = 0 if view == "front" else 1                             # 3/4: the face moves 1 px to the right
    for r, (c0, c1) in {5: (4, 12), 6: (4, 12), 7: (4, 12), 8: (4, 12), 9: (4, 12), 10: (5, 11), 11: (6, 10)}.items():
        row(SKIN, r, c0 + f, c1 + f)
    row(HAIR, 3, 6 + f, 10 + f); row(HAIR, 4, 6 + f, 10 + f); row(HAIR, 5, 4 + f, 12 + f)
    if view == "front":
        put(HAIR, (4, 6), (12, 6), (4, 7), (12, 7))
        puffs = (2, 12)
        eyes, m0 = (6, 10), 6
    else:
        row(HAIR, 6, 5, 7); row(HAIR, 7, 5, 7); row(HAIR, 8, 5, 6); put(HAIR, (5, 9), (13, 6))
        put(SKIN_D, (7, 8))                                     # ear
        puffs = (2, 12)
        eyes, m0 = (9, 12), 9
    for p0 in puffs:                                            # two round puffs, upper sides, 1 px clear of the ring
        put(HAIR, (p0 + 1, 3), (p0, 4), (p0 + 1, 4), (p0 + 2, 4), (p0, 5), (p0 + 1, 5), (p0 + 2, 5))
    for ex in eyes:
        put(OUT, (ex, 8)) if eyes_shut else put(OUT, (ex, 7), (ex, 8))
    put(OUT, (m0, 9), (m0 + 4, 9)); row(WHITE, 10, m0 + 1, m0 + 3)  # grin: corners up, teeth
    for c in range(2, 15):
        G[c, 12] = WHITE
    G[8 + 2 * f, 12] = ORANGE                                   # the collar's orange pixel at the neck
    for (c, r), col in G.items():
        s.px(col, (cx - 8 + c, top + r))


def arm(s, shoulder, hand, back=False):
    sl = SUIT_D if back else SUIT
    (x0, y0), (x1, y1) = shoulder, hand
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
        s.r(x, y, x + 1, y + 1, sl)
    s.r(x1, y1, x1 + 1, y1 + 1, SKIN_D if back else SKIN)


def legs(s, name, bottom):
    rows = LEGS[name]
    top = bottom - len(rows) + 1
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                s.px(LEGEND[ch], (7 + i, top + j))
    return top


def frame(name, eyes_shut=False):
    lg, lift, hdx, (bx, by), hand = POSES[name]
    s = Spr(jf.FW, jf.FH)
    cx = 16
    ltop = legs(s, lg, 30 - lift)
    oy = ltop - 22                                              # body rows 1..21 when standing
    arm(s, (cx - 4, 15 + oy), (cx - 5 + bx, 20 + oy + by), back=True)
    s.r(cx - 4, 14 + oy, cx + 4, 21 + oy, SUIT)
    s.px(SUIT_D, *[(cx - 4, y) for y in range(15 + oy, 22 + oy)])
    s.r(cx - 4, 18 + oy, cx + 4, 18 + oy, ORANGE)
    s.r(cx - 4, 21 + oy, cx + 4, 21 + oy, SUIT)
    s.px(SUIT_D, (cx - 4, 21 + oy))
    helmet(s, cx + hdx, 1 + oy, "34", eyes_shut)
    arm(s, (cx + 3, 15 + oy), hand)
    return s.im


def astro_ana(view="front"):
    s = Spr(jf.W, jf.H)
    cx = 20
    # legs and moon boots
    s.r(cx - 4, 22, cx - 1, 26, SUIT); s.r(cx + 1, 22, cx + 4, 26, SUIT); s.r(cx - 4, 21, cx + 4, 22, SUIT)
    s.px(SUIT_D, *[(cx - 1, y) for y in range(23, 27)])
    s.r(cx - 5, 27, cx - 1, 29, ORANGE); s.r(cx + 1, 27, cx + 5, 29, ORANGE)
    s.r(cx - 5, 30, cx - 1, 30, WHITE); s.r(cx + 1, 30, cx + 5, 30, WHITE)
    s.px(ORANGE_D, (cx - 1, 28), (cx - 1, 29), (cx + 5, 28), (cx + 5, 29))
    # arms (sleeves, hands)
    for sx in (cx - 7, cx + 6):
        s.r(sx, 15, sx + 1, 20, SUIT); s.r(sx, 21, sx + 1, 22, SKIN)
    s.px(SUIT_D, (cx - 7, 20), (cx + 7, 20))
    # torso with the orange chest stripe
    s.r(cx - 5, 14, cx + 5, 21, SUIT)
    s.r(cx - 5, 18, cx + 5, 18, ORANGE)
    s.px(SUIT_D, *[(x, y) for y in range(16, 22) for x in (cx - 5, cx + 5)])   # arm / body seam
    helmet(s, cx, 1, "front")
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


def check(im):
    """Puffs and hair never touch the ring (1 px glass between); highlight pixels present."""
    p = im.load()
    hair, ring = rgba(HAIR), rgba(RING)
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y] != hair:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < im.width and 0 <= ny < im.height:
                        assert p[nx, ny] != ring and p[nx, ny][3], f"hair at {(x, y)} touches the ring/outline"


if __name__ == "__main__":
    import json, os
    from px import up, silhouette
    out = "characters/astro_ana/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = astro_ana(), sheet()
    check(front)
    for n in jf.FRAMES:
        check(frame(n))
    assert front.getbbox()[3] - front.getbbox()[1] <= 32
    frames.save(f"{out}/astro_ana_frames.png")
    front.save(f"{out}/astro_ana_pixel.png")
    with open(f"{out}/astro_ana_frames.json", "w") as f:
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
    rev.save(f"{out}/astro_ana_pixel_sheet.png")
    print("wrote", out)
