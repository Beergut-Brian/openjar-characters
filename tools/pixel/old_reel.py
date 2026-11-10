"""Old Reel's pixel form for The Hill (Pillow only, drawn in code, from the 3D side view).

old_reel(view="front")        front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet

32 px tall with the outline (1.28 m in 3D, squeezed to the frame): bucket hat dome 4 rows + 1 brim row (1 px downturned
each end), face 8 rows, round 8-row vest torso, 2 rows of pants, yellow boots 5 rows + a dark sole row.
One blue lure (2 px) with a yellow tip pixel pinned to the hat band at the side; white brow pixels; half-lidded eyes.
No rod in the pixel frames.
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#E0A882", "#C08A64"
HAIR = "#F2F0EA"
HAT, HAT_D = "#C8A97A", "#A88C5E"
LURE, LURE_Y = "#3F8FD8", "#F2C230"
SHIRT, VEST, VEST_D = "#F1E7CF", "#A89B6E", "#8A7F58"
PANTS, PANTS_D = "#6E4B30", "#553A25"
BOOT, BOOT_D, SOLE = "#F6C833", "#C79F1E", "#6B5316"
MOUTH = "#6A2232"

HAND = (22, 21)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES)
# Old Reel fills the frame top to bottom, so the jump tucks the feet instead of lifting the body.
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


# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); legs are 3 px wide, boots 4
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
    """One leg from the hip (row `top`) to the sole row fy: brown pants, then a 5-row yellow rain boot (toe to the right)."""
    for i, y in enumerate(range(top, fy + 1)):
        t = i / max(1, fy - top)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 4, y, SOLE)
        elif y >= fy - 5:
            s.r(x, y, x + (4 if y == fy - 1 else 3), y, BOOT_D if back else BOOT)
            if not back and y < fy - 1:
                s.px(BOOT_D, (x, y))
        else:
            s.r(x, y, x + 2, y, PANTS_D if back else PANTS)


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 23 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    for x, y in _line(11, 17 + oy, 10 + bax, 21 + oy + bay):      # back arm
        s.r(x, y, x + 1, y + 1, SKIN_D)
    s.r(10, 16 + oy, 11, 17 + oy, SHIRT)
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(12, hip, 20, hip, PANTS)
    # round torso: khaki vest, cream shirt strip down the open front, belly bulge to the right
    s.r(11, 15 + oy, 21, hip - 1, VEST)
    s.r(22, 17 + oy, 22, hip - 3, VEST)
    s.r(17, 15 + oy, 19, hip - 1, SHIRT)
    s.px(VEST_D, (12, hip - 1), (13, hip - 1), (20, hip - 1), (21, hip - 1), (22, hip - 3), (16, 18 + oy), (16, 19 + oy))
    s.px(VEST_D, (14, 20 + oy), (15, 20 + oy))                                       # pocket
    hx, hy = hdx, oy
    # head (three-quarter, face right)
    s.r(11 + hx, 7 + hy, 21 + hx, 13 + hy, SKIN)
    s.r(12 + hx, 14 + hy, 20 + hx, 14 + hy, SKIN)
    s.r(10 + hx, 7 + hy, 11 + hx, 10 + hy, HAIR); s.px(HAIR, (11 + hx, 11 + hy))
    s.px(SKIN_D, (12 + hx, 11 + hy), (12 + hx, 12 + hy), (13 + hx, 12 + hy))        # ear
    # bucket hat: dome rows 1-4 (band on 4), brim row 5, brim tips turned down on row 6
    s.r(14 + hx, 1 + hy, 19 + hx, 1 + hy, HAT)
    s.r(12 + hx, 2 + hy, 21 + hx, 3 + hy, HAT)
    s.r(11 + hx, 4 + hy, 22 + hx, 4 + hy, HAT_D)
    s.r(9 + hx, 5 + hy, 24 + hx, 5 + hy, HAT)
    s.px(HAT, (9 + hx, 6 + hy), (24 + hx, 6 + hy))
    s.px(HAT_D, (10 + hx, 5 + hy), (23 + hx, 5 + hy))
    s.px(LURE, (18 + hx, 3 + hy), (18 + hx, 4 + hy)); s.px(LURE_Y, (19 + hx, 4 + hy))
    # face: bushy white brows, sleepy half-lidded eyes, gentle smile
    s.px(HAIR, (14 + hx, 8 + hy), (15 + hx, 8 + hy), (16 + hx, 8 + hy), (17 + hx, 8 + hy), (14 + hx, 7 + hy),
         (19 + hx, 8 + hy), (20 + hx, 8 + hy), (21 + hx, 8 + hy))
    if eyes_shut:
        s.px(OUT, (14 + hx, 10 + hy), (15 + hx, 10 + hy), (16 + hx, 10 + hy), (19 + hx, 10 + hy), (20 + hx, 10 + hy))
    else:
        s.r(15 + hx, 10 + hy, 16 + hx, 10 + hy, OUT)
        s.px(OUT, (20 + hx, 10 + hy)); s.px(SKIN_D, (15 + hx, 9 + hy), (16 + hx, 9 + hy), (20 + hx, 9 + hy))   # heavy lids
    s.px(SKIN_D, (21 + hx, 11 + hy))                                                # nose bump
    s.px(MOUTH, (17 + hx, 13 + hy), (18 + hx, 13 + hy), (19 + hx, 12 + hy))
    # front arm: cream sleeve then skin to a mitten hand
    for i, (x, y) in enumerate(_line(20, 16 + oy, hand[0], hand[1])):
        s.r(x, y, x + 1, y + 1, SHIRT if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def old_reel(view="front"):
    s = Spr(jf.W, jf.H)
    for x in (13, 25):                                                 # arms: cream sleeves, skin hands at the belly sides
        s.r(x, 16, x + 1, 18, SHIRT); s.r(x, 19, x + 1, 21, SKIN); s.px(SKIN_D, (x, 21), (x + 1, 21))
    # legs: pants stubs into tall yellow boots (5 rows + sole)
    s.r(16, 23, 23, 23, PANTS)
    for x in (16, 21):
        s.r(x, 24, x + 2, 24, PANTS)
    for x, fl in ((15, -1), (21, 1)):                                   # boots 4 wide, 2 px apart, toes flare outward
        s.r(x, 25, x + 3, 29, BOOT); s.px(BOOT_D, (x + 3 if fl < 0 else x, 25), (x + 3 if fl < 0 else x, 26), (x + 3 if fl < 0 else x, 27))
        s.px(BOOT, (x - 1 if fl < 0 else x + 4, 29)); s.r(x, 30, x + 3, 30, SOLE); s.px(SOLE, (x - 1 if fl < 0 else x + 4, 30))
    # round torso: vest sides, cream shirt strip
    s.r(14, 15, 25, 22, VEST); s.r(15, 22, 24, 22, VEST)
    s.r(18, 15, 21, 22, SHIRT); s.px(VEST_D, (14, 22), (25, 22), (16, 19), (23, 19), (16, 20), (23, 20))
    # head
    s.r(15, 7, 24, 13, SKIN); s.r(16, 14, 23, 14, SKIN)
    s.r(14, 7, 14, 10, HAIR); s.r(25, 7, 25, 10, HAIR)
    # bucket hat
    s.r(17, 1, 22, 1, HAT); s.r(15, 2, 24, 3, HAT); s.r(14, 4, 25, 4, HAT_D)
    s.r(12, 5, 27, 5, HAT); s.px(HAT_D, (13, 5), (26, 5)); s.px(HAT, (12, 6), (27, 6))
    s.px(LURE, (24, 3), (24, 4)); s.px(LURE_Y, (23, 4))
    # face
    s.px(HAIR, (16, 8), (17, 8), (18, 8), (21, 8), (22, 8), (23, 8), (16, 7), (23, 7))
    s.r(17, 10, 18, 10, OUT); s.r(21, 10, 22, 10, OUT); s.px(SKIN_D, (17, 9), (18, 9), (21, 9), (22, 9))
    s.px(MOUTH, (18, 13), (19, 13), (20, 13), (21, 12), (17, 12))
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/old_reel/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = old_reel(), sheet()
    frames.save(f"{out}/old_reel_frames.png")
    front.save(f"{out}/old_reel_pixel.png")
    with open(f"{out}/old_reel_frames.json", "w") as f:
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
    rev.save(f"{out}/old_reel_pixel_sheet.png")
    print("wrote", out)
