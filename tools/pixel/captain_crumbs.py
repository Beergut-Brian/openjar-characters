"""Captain Crumbs' pixel form for The Hill (Pillow only, drawn in code).

captain_crumbs(view="front") front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False) unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                      the 128 x 224 player sheet

32 px tall with the outline (the 3D is 1.58 m with the hat, 42 px at true scale, squeezed to the frame):
chef hat 8 rows (puff 7 + a band row with the navy badge pixel), face 7, jacket 8, pants 4, boots 3.
Round middle: the jacket is 14 px wide in the front form, the head 10. The eyepatch covers his left eye
(viewer's right in the front form, the far eye in the frames) with a strap pixel line up to the hat band.
The moustache is two symmetric 3-4 px curls under the nose in the front form; in the frames it lies flat
on the face (never past the face edge) with an upturned end, so it cannot read as a pipe.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#D99E6E", "#B97F52"
HAIR = "#4A3324"
HAT, HAT_D = "#F7F7F2", "#D9D9D2"
NAVY = "#1F2D55"
BLACK = "#18181C"
MOUSTACHE = "#4A3324"
MOUTH = "#6A2232"
EYE_HI = "#FFFFFF"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# Lampy fills the frame top to bottom, so the jump tucks the feet instead of lifting the body.
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
    """One leg from the hip (row `top`) to the boot sole (row fy): navy pants with a white stripe, black boot."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y >= fy - 2:
            s.r(x, y, x + 3 if y >= fy - 1 else x + 2, y, BLACK)
        else:
            s.r(x, y, x + 2, y, NAVY)
            s.px(HAT_D if back else HAT, (x + 1, y))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 24 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm (shaded sleeve), legs
    for x, y in _line(11, 17 + oy, 10 + bax, 21 + oy + bay):
        s.r(x, y, x + 1, y + 1, HAT_D)
    s.r(10, 16 + oy, 11, 18 + oy, HAT_D)
    s.px(SKIN_D, (10 + bax, 21 + oy + bay))
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 19, hip, NAVY)
    # jacket: 8 rows with a round belly bump at the front, two button columns, shade down the back
    s.r(11, 16 + oy, 19, hip - 1, HAT)
    s.r(20, 18 + oy, 21, hip - 1, HAT)
    s.px(HAT, (20, 17 + oy))
    s.r(11, 16 + oy, 11, hip - 1, HAT_D)
    s.r(12, hip - 1, 21, hip - 1, HAT_D)
    for y in (18 + oy, 20 + oy, 22 + oy):
        s.px(NAVY, (15, y), (18, y))
    # head (three-quarter, face to the right)
    hx, hy = hdx, oy
    s.r(11 + hx, 9 + hy, 21 + hx, 14 + hy, SKIN)
    s.r(12 + hx, 15 + hy, 20 + hx, 15 + hy, SKIN)
    s.r(11 + hx, 9 + hy, 13 + hx, 11 + hy, HAIR)                                    # hair under the hat, back
    s.px(SKIN_D, (13 + hx, 12 + hy), (13 + hx, 13 + hy))                            # ear
    # chef hat: puff rows 1-7, band row 8
    s.r(13 + hx, 1 + hy, 19 + hx, 1 + hy, HAT)
    s.r(11 + hx, 2 + hy, 21 + hx, 2 + hy, HAT)
    s.r(10 + hx, 3 + hy, 22 + hx, 6 + hy, HAT)
    s.r(11 + hx, 7 + hy, 21 + hx, 7 + hy, HAT)
    s.r(11 + hx, 8 + hy, 21 + hx, 8 + hy, HAT_D)
    s.px(HAT_D, (10 + hx, 4 + hy), (10 + hx, 5 + hy), (10 + hx, 6 + hy), (11 + hx, 6 + hy), (11 + hx, 2 + hy),
         (12 + hx, 7 + hy))
    s.px(NAVY, (18 + hx, 8 + hy))                                                   # badge
    # face: near eye open 2 x 2 with a highlight; the patch is over the far eye (his left), strap back over the head
    if eyes_shut:
        s.px(OUT, (15 + hx, 11 + hy), (16 + hx, 11 + hy))
    else:
        s.r(15 + hx, 11 + hy, 16 + hx, 12 + hy, OUT); s.px(EYE_HI, (16 + hx, 11 + hy))
    s.r(19 + hx, 11 + hy, 20 + hx, 12 + hy, BLACK)
    s.px(BLACK, (18 + hx, 10 + hy), (17 + hx, 9 + hy))
    s.px(SKIN_D, (21 + hx, 12 + hy))                                                # nose bump
    # moustache flat on the face, ends within the face edge, upturned curl at the front; grin below
    s.r(16 + hx, 13 + hy, 20 + hx, 13 + hy, MOUSTACHE); s.r(17 + hx, 14 + hy, 20 + hx, 14 + hy, MOUSTACHE)
    s.px(MOUSTACHE, (21 + hx, 13 + hy))                                             # upturned end, inside the face edge
    s.px(MOUTH, (17 + hx, 15 + hy), (18 + hx, 15 + hy), (19 + hx, 15 + hy))
    # front arm: white sleeve, then skin to a mitten hand
    pts = _line(19, 16 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, HAT if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def captain_crumbs(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: white sleeves, skin hands
    for x in (11, 27):
        s.r(x, 17, x + 1, 19, HAT); s.r(x, 20, x + 1, 22, SKIN); s.px(SKIN_D, (x, 22), (x + 1, 22))
    # legs and boots
    s.r(15, 24, 24, 24, NAVY)
    for x in (15, 21):
        s.r(x, 25, x + 3, 27, NAVY); s.px(HAT, (x + 1, 25), (x + 1, 26), (x + 1, 27))
    s.r(14, 28, 18, 30, BLACK); s.r(21, 28, 25, 30, BLACK)
    # jacket: 14 px wide round middle, shade at the sides, two navy button columns
    s.r(13, 16, 26, 23, HAT)
    s.px(HAT_D, (13, 21), (13, 22), (13, 23), (26, 21), (26, 22), (26, 23))
    s.r(14, 23, 25, 23, HAT_D)
    for y in (18, 20, 22):
        s.px(NAVY, (18, y), (21, y))
    # head
    s.r(15, 9, 24, 14, SKIN); s.r(16, 15, 23, 15, SKIN)
    s.px(HAIR, (15, 9), (24, 9), (15, 10), (24, 10))
    # chef hat
    s.r(16, 1, 23, 1, HAT); s.r(14, 2, 25, 2, HAT); s.r(13, 3, 26, 6, HAT); s.r(14, 7, 25, 7, HAT)
    s.r(15, 8, 24, 8, HAT_D); s.px(NAVY, (19, 8))
    s.px(HAT_D, (13, 4), (13, 5), (13, 6), (14, 6), (14, 2), (15, 7))
    # eyepatch over his left eye (viewer's right), strap pixels up to the hat band; open eye on the other side
    s.r(21, 11, 22, 12, BLACK); s.px(BLACK, (23, 10), (24, 9))
    s.r(17, 11, 18, 12, OUT); s.px(EYE_HI, (17, 11))
    s.px(SKIN_D, (19, 13), (20, 13))                                                # nose
    # moustache: two symmetric curls under the nose, ends curling up
    s.px(MOUSTACHE, (16, 13), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14), (23, 13))
    s.px(MOUSTACHE, (18, 13), (21, 13)) if False else None
    s.px(MOUTH, (18, 15), (19, 15), (20, 15), (21, 15))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/captain_crumbs/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = captain_crumbs(), sheet()
    frames.save(f"{out}/captain_crumbs_frames.png")
    front.save(f"{out}/captain_crumbs_pixel.png")
    with open(f"{out}/captain_crumbs_frames.json", "w") as f:
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
    rev.save(f"{out}/captain_crumbs_pixel_sheet.png")
    print("wrote", out)
