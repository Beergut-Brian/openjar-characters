"""Yoji's pixel form for The Hill (Pillow only, drawn in code, traced from the 3D side view).

yoji(view="front")            front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet

32 px tall with the outline (1.0 m body plus the tall cowboy hat, traced from refs/jarling/yoji_side_sprite.png, capped
at the frame): cowboy hat 5 rows (pinched crown 4 rows with the band on the last, 1 brim row much wider than the head, the
brim tips curled up 1 px), head 9 rows (brown hair at the back and as a fringe under the brim, big grin), navy jersey 7 rows
with broad shoulder pads and a gold hem, a gold waistband and 2 rows of white boxers with navy star pixels, 2 rows of bare
legs, black-and-blue high-tops 4 rows (blue collar above the ankle, white sole).
White "55" on the front form; a white number fragment on the jersey in the frames. No player colours anywhere.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#E8B48A", "#C8936B"
HAIR = "#6B4A2E"
HAT, HAT_D, BAND = "#C8955A", "#A6763F", "#5A3A22"
JERSEY, JERSEY_D, GOLD = "#1F3A6B", "#162B52", "#F2B632"
WHITE, WHITE_D = "#F7F7F5", "#D6D8DE"
SHOE, BLUE = "#1A1A1E", "#2A6FD6"
MOUTH = "#6A2232"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# Yoji fills the frame top to bottom (like Old Reel), so the jump tucks the feet instead of lifting the body.
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

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs are 3 px wide, shoes 4
LEGS = {
    "stand": ((12, 12, 30), (17, 17, 30)),
    "contact": ((12, 9, 30), (17, 20, 30)),
    "pass": ((13, 11, 28), (16, 16, 30)),
    "contact2": ((12, 15, 30), (17, 13, 30)),
    "pass2": ((12, 13, 30), (17, 16, 28)),
    "tuck": ((12, 11, 28), (17, 18, 28)),
    "dangle": ((12, 11, 30), (17, 18, 30)),
    "crouch": ((12, 9, 30), (17, 20, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the hip (row `top`) to the sole row fy: 2 rows of boxer leg, bare skin, then a 4-row high-top
    (blue collar above the ankle, black upper with a blue stripe, white sole; toe to the right)."""
    for i, y in enumerate(range(top, fy + 1)):
        t = i / max(1, fy - top)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 4, y, WHITE_D if back else WHITE)
        elif y >= fy - 2:
            s.r(x, y, x + (4 if y == fy - 1 else 3), y, SHOE)
            if not back and y == fy - 2:
                s.px(BLUE, (x + 1, y), (x + 2, y))
        elif y == fy - 3:
            s.r(x, y, x + 3, y, BLUE)
        elif y < top + 2:
            s.r(x, y, x + 2, y, WHITE_D if back else WHITE)
        else:
            s.r(x, y, x + 2, y, SKIN_D if back else SKIN)


def _hat_side(s, hx, hy):
    """Cowboy hat, three-quarter: pinched crown (two lobes, dented middle), band, brim much wider than the head
    with both tips curled up."""
    # crown lobes with a dent 2 rows deep and 3 px wide between them (it must survive the 16 px reduction)
    s.r(12 + hx, 1 + hy, 13 + hx, 1 + hy, HAT); s.r(19 + hx, 1 + hy, 20 + hx, 1 + hy, HAT)
    s.r(12 + hx, 2 + hy, 14 + hx, 2 + hy, HAT); s.r(18 + hx, 2 + hy, 20 + hx, 2 + hy, HAT)
    s.r(12 + hx, 3 + hy, 20 + hx, 3 + hy, HAT)
    s.px(HAT_D, (15 + hx, 3 + hy), (16 + hx, 3 + hy), (17 + hx, 3 + hy), (20 + hx, 2 + hy), (20 + hx, 3 + hy))
    s.r(12 + hx, 4 + hy, 20 + hx, 4 + hy, BAND)
    s.r(7 + hx, 5 + hy, 25 + hx, 5 + hy, HAT)                                                 # brim
    s.px(HAT_D, (11 + hx, 5 + hy), (21 + hx, 5 + hy))
    s.px(HAT, (6 + hx, 4 + hy), (7 + hx, 4 + hy), (25 + hx, 4 + hy), (26 + hx, 4 + hy))     # tips curled up
    s.px(HAT, (6 + hx, 3 + hy), (26 + hx, 3 + hy))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 23 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    for i, (x, y) in enumerate(_line(11, 17 + oy, 10 + bax, 21 + oy + bay)):      # back arm: navy sleeve, skin
        s.r(x, y, x + 1, y + 1, JERSEY_D if i < 2 else SKIN_D)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    # boxers seat + gold/navy waistband
    s.r(11, hip - 1, 20, hip, WHITE)
    s.r(11, hip - 2, 21, hip - 2, JERSEY_D); s.px(GOLD, (14, hip - 2), (18, hip - 2))
    s.px(JERSEY, (13, hip), (18, hip - 1), (20, hip + 1))                              # star pixels
    s.px(WHITE_D, (11, hip), (12, hip))
    # jersey: broad shoulder pads on rows 15-16, gold hem, white number fragment
    s.r(11, 15 + oy, 21, hip - 3, JERSEY)
    s.r(10, 15 + oy, 22, 15 + oy, JERSEY); s.r(9, 16 + oy, 23, 17 + oy, JERSEY)
    s.px(JERSEY_D, (9, 17 + oy), (10, 17 + oy), (12, 15 + oy), (11, 16 + oy))
    s.r(22, 18 + oy, 22, hip - 4, JERSEY)                                              # a little belly
    s.r(11, hip - 3, 21, hip - 3, GOLD)
    s.px(WHITE, (14, 17 + oy), (15, 17 + oy), (16, 17 + oy), (14, 18 + oy), (14, 19 + oy), (15, 19 + oy), (16, 19 + oy),
         (16, 20 + oy))
    s.px(GOLD, (16, 15 + oy), (17, 15 + oy), (18, 15 + oy))                            # collar
    hx, hy = hdx, oy
    # head (three-quarter, face right)
    s.r(11 + hx, 6 + hy, 21 + hx, 13 + hy, SKIN)
    s.r(12 + hx, 14 + hy, 20 + hx, 14 + hy, SKIN)
    s.r(10 + hx, 6 + hy, 12 + hx, 10 + hy, HAIR); s.px(HAIR, (11 + hx, 11 + hy))
    s.r(13 + hx, 6 + hy, 19 + hx, 6 + hy, HAIR); s.px(HAIR, (13 + hx, 7 + hy))
    s.px(SKIN_D, (12 + hx, 11 + hy), (12 + hx, 12 + hy), (13 + hx, 12 + hy))          # ear
    _hat_side(s, hx, hy)
    # face: thick brows, round eyes, big grin (teeth showing)
    s.px(HAIR, (15 + hx, 8 + hy), (16 + hx, 8 + hy), (19 + hx, 8 + hy), (20 + hx, 8 + hy))
    if eyes_shut:
        s.px(OUT, (15 + hx, 10 + hy), (16 + hx, 10 + hy), (20 + hx, 10 + hy))
    else:
        s.r(15 + hx, 9 + hy, 15 + hx, 10 + hy, OUT); s.px(OUT, (16 + hx, 10 + hy))
        s.r(20 + hx, 9 + hy, 20 + hx, 10 + hy, OUT)
    s.px(SKIN_D, (22 + hx, 10 + hy), (22 + hx, 11 + hy))                              # nose bump
    s.px(MOUTH, (16 + hx, 12 + hy), (21 + hx, 12 + hy))
    s.r(17 + hx, 12 + hy, 20 + hx, 12 + hy, WHITE)
    s.r(17 + hx, 13 + hy, 20 + hx, 13 + hy, MOUTH)
    # front arm: navy sleeve with a gold stripe, then skin to a mitten hand
    for i, (x, y) in enumerate(_line(20, 16 + oy, hand[0], hand[1])):
        s.r(x, y, x + 1, y + 1, JERSEY if i < 1 else (GOLD if i == 1 else SKIN))
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def yoji(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: navy sleeve under the pad with a gold stripe, skin to the hands at the jersey hem
    for x in (12, 26):
        s.r(x, 17, x + 1, 17, JERSEY); s.r(x, 18, x + 1, 18, GOLD)
        s.r(x, 19, x + 1, 21, SKIN); s.px(SKIN_D, (x, 21), (x + 1, 21))
    # high-tops: blue collar, black upper with a blue stripe, white sole, toes flare outward
    for x, fl in ((14, -1), (21, 1)):
        s.r(x, 27, x + 4, 27, BLUE); s.r(x, 28, x + 4, 29, SHOE)
        s.px(BLUE, (x + 1, 28), (x + 2, 28)) if fl < 0 else s.px(BLUE, (x + 2, 28), (x + 3, 28))
        s.px(SHOE, (x - 1 if fl < 0 else x + 5, 29)); s.r(x, 30, x + 4, 30, WHITE)
        s.px(WHITE, (x - 1 if fl < 0 else x + 5, 30))
    # bare legs
    for x in (15, 22):
        s.r(x, 25, x + 2, 26, SKIN); s.px(SKIN_D, (x + 2 if x < 19 else x, 25))
    # boxers: gold/navy waistband, white with navy stars, a split between the legs
    s.r(14, 22, 25, 22, JERSEY_D); s.px(GOLD, (16, 22), (19, 22), (20, 22), (23, 22))
    s.r(14, 23, 25, 24, WHITE); s.px(OUT, (19, 24), (20, 24))
    s.px(JERSEY, (15, 23), (22, 23), (17, 24), (24, 24))
    s.px(WHITE_D, (14, 24), (25, 24))
    # jersey: broad shoulder pads, gold hem, white 55
    s.r(14, 15, 25, 21, JERSEY)
    s.r(12, 15, 27, 16, JERSEY); s.r(13, 14, 15, 14, JERSEY); s.r(24, 14, 26, 14, JERSEY)
    s.px(JERSEY_D, (12, 16), (27, 16), (14, 16), (25, 16))
    s.r(14, 21, 25, 21, GOLD)
    s.r(17, 14, 22, 14, GOLD)                                              # collar under the chin
    for dx in (15, 20):                                                    # "55", 3 x 5 digits
        s.r(dx, 16, dx + 2, 16, WHITE); s.px(WHITE, (dx, 17)); s.r(dx, 18, dx + 2, 18, WHITE)
        s.px(WHITE, (dx + 2, 19)); s.r(dx, 20, dx + 2, 20, WHITE)
    # head
    s.r(15, 6, 24, 12, SKIN); s.r(16, 13, 23, 13, SKIN)
    s.r(14, 6, 14, 10, HAIR); s.r(25, 6, 25, 10, HAIR); s.r(15, 6, 24, 6, HAIR)
    s.px(SKIN_D, (14, 11), (25, 11))                                      # ears
    # cowboy hat: pinched crown (two lobes, dip in the middle), band, brim wider than the head, tips curled up
    s.r(15, 1, 16, 1, HAT); s.r(23, 1, 24, 1, HAT)                      # lobes; the dip is 2 rows deep, 4 px wide
    s.r(15, 2, 17, 2, HAT); s.r(22, 2, 24, 2, HAT)
    s.r(15, 3, 24, 3, HAT); s.px(HAT_D, (18, 3), (19, 3), (20, 3), (21, 3))
    s.r(15, 4, 24, 4, BAND)
    s.r(10, 5, 29, 5, HAT); s.px(HAT_D, (14, 5), (25, 5))
    s.px(HAT, (9, 4), (10, 4), (29, 4), (30, 4), (9, 3), (30, 3))
    # face: thick brows, round eyes, big open grin
    s.px(HAIR, (16, 7), (17, 7), (18, 7), (21, 7), (22, 7), (23, 7))
    s.r(17, 8, 17, 9, OUT); s.r(22, 8, 22, 9, OUT)
    s.px(MOUTH, (17, 11), (22, 11))                                       # grin corners
    s.r(18, 11, 21, 11, WHITE); s.r(18, 12, 21, 12, MOUTH)
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/yoji/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = yoji(), sheet()
    frames.save(f"{out}/yoji_frames.png")
    front.save(f"{out}/yoji_pixel.png")
    with open(f"{out}/yoji_frames.json", "w") as f:
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
    rev.save(f"{out}/yoji_pixel_sheet.png")
    print("wrote", out)
