"""El Burrito's pixel form for The Hill (Pillow only, drawn in code).

el_burrito(view="front")     front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

27 px tall with the outline (the 3D is about 1.02 m, 27 px at the 32 px = 1.2 m scale, no squeezing): short and wide.
Gold luchador mask head 11 rows (no hair, no ears), torso 7, purple shorts 2, tall white boots 5. 12 px wide torso.
Purple cape behind the shoulders to knee level (flares out at the left in the frames, peeks out at both sides in the
front form) with one gold hem pixel. Star on the chest is 5 px.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#D99E6E", "#B97F52"
GOLD, GOLD_D = "#E0B12E", "#BC9022"
PURP, PURP_D = "#6B2FA8", "#54238A"
BOOT, SOLE = "#F5F5F2", "#C9C9C2"
MOUTH = "#6A2232"

HAND = (22, 21)

POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (22, 21), 0),
    "idle1": ("stand", 0, 0, (0, 1), (22, 22), 1),
    "walk0": ("contact", 0, 0, (1, 0), (22, 21), 0),
    "walk1": ("pass", 0, 0, (0, 0), (22, 20), 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (22, 21), 0),
    "walk3": ("pass2", 0, 0, (0, 0), (22, 20), 0),
    "jump": ("tuck", 3, 0, (-1, -3), (23, 15), 0),
    "fall": ("dangle", 2, 0, (-1, -4), (24, 14), 0),
    "side0": ("stand", 0, -1, (0, 0), (18, 16), 0),
    "side1": ("contact", 0, 1, (1, -1), (22, 19), 0),
    "side2": ("stand", 0, 0, (0, 0), (21, 20), 0),
    "down0": ("stand", 0, 0, (0, -1), (22, 11), 0),
    "down1": ("crouch", 0, 1, (0, 0), (24, 18), 1),
    "down2": ("stand", 0, 0, (0, 0), (23, 17), 0),
}

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs are 4 px wide
LEGS = {
    "stand": ((11, 11, 30), (16, 16, 30)),
    "contact": ((11, 8, 30), (16, 19, 30)),
    "pass": ((12, 10, 28), (15, 15, 30)),
    "contact2": ((11, 14, 30), (16, 12, 30)),
    "pass2": ((11, 12, 30), (16, 15, 28)),
    "tuck": ((11, 10, 30), (16, 17, 30)),
    "dangle": ((11, 10, 30), (16, 17, 30)),
    "crouch": ((11, 8, 30), (16, 19, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, back=False):
    """One leg from the hip (row `top`) to the sole (row fy): purple shorts 2 rows, tall white boot 5 rows, purple lace pixel."""
    for i, y in enumerate(range(top, fy + 1)):
        t = i / max(1, fy - top)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 4, y, SOLE)
        elif y >= fy - 4:
            s.r(x, y, x + 3 if y < fy - 1 else x + 4, y, BOOT)
            if y == fy - 3:
                s.px(PURP, (x + 2, y))
            if back:
                s.px(SOLE, (x, y))
        else:
            s.r(x, y, x + 3, y, PURP_D if back else PURP)


def _star(s, cx, cy):
    s.px(PURP, (cx, cy - 2), (cx - 2, cy - 1), (cx - 1, cy - 1), (cx, cy - 1), (cx + 1, cy - 1), (cx + 2, cy - 1),
         (cx - 1, cy), (cx, cy), (cx + 1, cy), (cx - 1, cy + 1), (cx + 1, cy + 1))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 24 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # cape behind the shoulders, flaring out at the left, gold hem pixel
    for i, y in enumerate(range(17 + oy, 27 + oy - lift // 2)):
        x0 = 9 - (i * 4) // 9
        s.r(x0, y, 12, y, PURP_D if i % 3 == 2 else PURP)
    s.px(GOLD, (5 + (0 if oy else 0), 26 + oy - lift // 2))
    s.r(5, 26 + oy - lift // 2, 6, 26 + oy - lift // 2, GOLD)
    # back arm, legs
    for x, y in _line(10, 18 + oy, 9 + bax, 22 + oy + bay):
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(9, 17 + oy, 11, 18 + oy, GOLD)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(11, hip, 20, hip, PURP)
    # torso: gold top with a purple star
    s.r(10, 17 + oy, 21, hip - 1, GOLD)
    s.px(GOLD_D, (10, hip - 1), (11, hip - 1))
    _star(s, 17, 20 + oy)
    s.px(GOLD_D, (11, 17 + oy), (12, 17 + oy))
    # head: gold mask, round; no ears, no hair
    hx, hy = hdx, oy
    for y, x0, x1 in ((6, 14, 17), (7, 12, 19), (8, 11, 20), (9, 10, 21), (10, 10, 21), (11, 10, 21), (12, 10, 21),
                      (13, 10, 21), (14, 11, 20), (15, 12, 19), (16, 13, 18)):
        s.r(x0 + hx, y + hy, x1 + hx, y + hy, GOLD)                                  # round mask, 12 x 11
    s.px(GOLD_D, (10 + hx, 12 + hy), (10 + hx, 13 + hy), (11 + hx, 14 + hy), (12 + hx, 15 + hy))
    s.r(16 + hx, 6 + hy, 16 + hx, 8 + hy, PURP)                                      # forehead stripe, 1 px
    # eye openings: 1 px purple ring, 2 x 2 opening (skin + dark eye); far eye is a narrow ring
    s.r(12 + hx, 9 + hy, 15 + hx, 12 + hy, PURP)
    s.r(13 + hx, 10 + hy, 14 + hx, 11 + hy, SKIN)
    s.r(18 + hx, 9 + hy, 20 + hx, 12 + hy, PURP)
    s.r(19 + hx, 10 + hy, 19 + hx, 11 + hy, SKIN)
    if eyes_shut:
        s.px(OUT, (13 + hx, 11 + hy), (14 + hx, 11 + hy), (19 + hx, 11 + hy))
    else:
        s.r(14 + hx, 10 + hy, 14 + hx, 11 + hy, OUT)
        s.px(OUT, (19 + hx, 10 + hy), (19 + hx, 11 + hy))
    # mouth opening: 1 px ring, big grin with teeth
    s.r(14 + hx, 14 + hy, 19 + hx, 16 + hy, PURP)
    s.r(15 + hx, 15 + hy, 18 + hx, 15 + hy, SKIN)
    s.px(MOUTH, (15 + hx, 15 + hy), (18 + hx, 15 + hy))
    s.px(BOOT, (16 + hx, 15 + hy), (17 + hx, 15 + hy))
    # front arm: gold sleeve, then skin to a mitten hand
    pts = _line(20, 17 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, GOLD if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 2, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def el_burrito(view="front"):
    s = Spr(jf.W, jf.H)
    # cape edges peeking out either side of the body, below the arms
    for x in (10, 11, 28, 29):
        s.r(x, 21, x, 27, PURP)
    s.px(GOLD, (10, 27), (11, 27), (28, 27), (29, 27))
    # arms: gold sleeve, skin, hand
    for x in (12, 26):
        s.r(x, 18, x + 1, 19, GOLD); s.r(x, 20, x + 1, 23, SKIN); s.px(SKIN_D, (x, 23), (x + 1, 23))
    # shorts and boots
    s.r(15, 24, 24, 26, PURP)
    s.px(PURP_D, (19, 25), (19, 26), (20, 25), (20, 26))
    for x in (15, 21):
        s.r(x, 27, x + 3, 29, BOOT)
        s.px(PURP, (x + 1, 28), (x + 2, 28))
        s.r(x, 30, x + 3, 30, SOLE)
    # torso: gold top, purple star
    s.r(14, 17, 25, 23, GOLD)
    s.px(GOLD_D, (14, 23), (15, 23))
    _star(s, 19, 20)
    # head: round gold mask, 12 x 11
    for y, x0, x1 in ((6, 18, 21), (7, 16, 23), (8, 15, 24), (9, 14, 25), (10, 14, 25), (11, 14, 25), (12, 14, 25),
                      (13, 14, 25), (14, 15, 24), (15, 16, 23), (16, 17, 22)):
        s.r(x0, y, x1, y, GOLD)
    s.px(GOLD_D, (14, 12), (14, 13), (15, 14), (16, 15))
    s.r(19, 7, 19, 8, PURP)                                                         # forehead stripe, 1 px
    for x0 in (15, 21):                                                              # eye openings, 2 px of gold between
        s.r(x0, 9, x0 + 3, 12, PURP); s.r(x0 + 1, 10, x0 + 2, 11, SKIN)
        s.r(x0 + 2, 10, x0 + 2, 11, OUT)
    s.r(17, 14, 22, 16, PURP); s.r(18, 15, 21, 15, SKIN)                            # mouth opening
    s.px(MOUTH, (18, 15), (21, 15)); s.px(BOOT, (19, 15), (20, 15))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/el_burrito/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = el_burrito(), sheet()
    frames.save(f"{out}/el_burrito_frames.png")
    front.save(f"{out}/el_burrito_pixel.png")
    with open(f"{out}/el_burrito_frames.json", "w") as f:
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
    rev.save(f"{out}/el_burrito_pixel_sheet.png")
    print("wrote", out)
