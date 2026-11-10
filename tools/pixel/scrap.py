"""Scrap's pixel form for The Hill (Pillow only, drawn in code).

scrap(view="front")           front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet

29 px tall with the outline (a small kid with a big head, traced from refs/jarling/scrap_side_sprite.png):
colander feet 1 row, bowl 4, rim 1, head 8, tee 6, shorts 2, bare legs 3, shoes 2.
The colander carries itself with a flat-ish top and two foot pixels, staggered dark hole dots, a rim row
1 px wider than the head each side and a handle nub at each end of the rim. Odd shoes: his left
foot orange, right foot purple (frames: near foot orange, far foot purple).
"""
import os
from px import Spr, OUT, up, silhouette, rgba
import jarling_frames as jf

SKIN, SKIN_D = "#F0BE94", "#D29D74"
FRECKLE = "#C98A5E"
HAIR = "#B5651D"
COL, COL_L, COL_D, HOLE = "#B9BEC4", "#DDE1E5", "#8E949B", "#3A3F48"
TEE, TEE_D = "#F2C230", "#D4A51E"
PATCH_O, PATCH_B = "#E8873D", "#5B8FD6"
SHORTS, SHORTS_D = "#3E6DB5", "#325A96"
SHOE_O, SHOE_P = "#F28C28", "#8A4FC4"
MOUTH, TOOTH = "#6A2232", "#FFFFFF"
EYE_HI = "#FFFFFF"

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

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); kid legs 2 px wide
LEGS = {
    "stand": ((12, 12, 30), (17, 17, 30)),
    "contact": ((12, 9, 30), (17, 20, 30)),
    "pass": ((13, 11, 28), (16, 16, 30)),
    "contact2": ((12, 15, 30), (17, 12, 30)),
    "pass2": ((12, 13, 30), (17, 16, 28)),
    "tuck": ((12, 11, 28), (17, 18, 28)),
    "dangle": ((12, 11, 30), (17, 18, 30)),
    "crouch": ((12, 9, 30), (17, 20, 30)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _leg(s, hx, fx, fy, top, shoe, back=False):
    """One bare leg from the shorts hem (row `top`) to the shoe sole (row fy), shoe toe to the right."""
    rows = list(range(top, fy + 1))
    for i, y in enumerate(rows):
        t = i / max(1, len(rows) - 1)
        x = round(hx + (fx - hx) * t)
        if y >= fy - 1:
            s.r(x, y, x + 3, y, shoe)
        else:
            s.r(x, y, x + 1, y, SKIN_D if back else SKIN)
            if not back:
                s.px(SKIN_D, (x, y))


def _colander(s, x0, x1, top, holes, back_nub=True, front_nub=True):
    """Upturned colander bowl over head columns x0..x1: foot pixels on row top, flat-ish bowl rows top+1..top+4
    (narrowing to the top), dark holes on rows top+2 and top+4, rim row top+5 1 px wider than the head each side,
    handle nubs past the rim ends."""
    y = top
    s.r(x0 + 2, y + 1, x1 - 2, y + 1, COL)
    s.r(x0 + 1, y + 2, x1 - 1, y + 2, COL)
    s.r(x0, y + 3, x1, y + 4, COL)
    s.r(x0 + 3, y + 1, x0 + 5, y + 1, COL_L); s.px(COL_L, (x0 + 2, y + 2), (x0 + 1, y + 3))       # sheen, top left
    s.px(COL_D, (x1 - 2, y + 1), (x1 - 1, y + 2), (x1, y + 3), (x1, y + 4))                      # shade, right edge
    for hy, hxs in holes:
        s.px(HOLE, *[(hx, y + hy) for hx in hxs])
    s.px(COL_D, (x0 + 4, y), (x1 - 4, y))                                                        # two little feet
    s.r(x0 - 1, y + 5, x1 + 1, y + 5, COL_L); s.px(COL_D, (x1 + 1, y + 5))                       # rim
    if back_nub:
        s.px(COL_D, (x0 - 2, y + 5), (x0 - 3, y + 5))
    if front_nub:
        s.px(COL_D, (x1 + 2, y + 5), (x1 + 3, y + 5))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 26 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    # back arm: shaded sleeve, skin arm
    pts = _line(10, 19 + oy, 9 + bax, 23 + oy + bay)
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y, TEE_D if i < 1 else SKIN_D)
    s.r(10, 18 + oy, 11, 19 + oy, TEE_D)
    # legs: near foot orange (his left), far foot purple
    _leg(s, bh, bf, by_ - lift, hip, SHOE_P, back=True)
    _leg(s, fh, ff, fy_ - lift, hip, SHOE_O)
    s.r(11, hip - 2, 20, hip - 1, SHORTS); s.r(11, hip - 1, 13, hip - 1, SHORTS_D)
    # patched tee
    y0, y1 = 18 + oy, 23 + oy
    s.r(12, y0, 19, y0, TEE); s.r(11, y0 + 1, 20, y1, TEE)
    s.r(11, y0 + 1, 11, y1, TEE_D); s.r(12, y1, 20, y1, TEE_D)
    s.r(16, y0 + 2, 17, y0 + 3, PATCH_O)
    s.px(PATCH_B, (13, y0 + 3), (13, y0 + 4))
    # head (three-quarter, face to the right)
    hx, hy = hdx, oy
    s.r(9 + hx, 10 + hy, 21 + hx, 16 + hy, SKIN)
    s.r(10 + hx, 17 + hy, 20 + hx, 17 + hy, SKIN); s.px(SKIN_D, (10 + hx, 17 + hy), (20 + hx, 17 + hy))
    # auburn hair under the rim: back and side, a short fringe
    s.r(9 + hx, 10 + hy, 13 + hx, 13 + hy, HAIR); s.r(9 + hx, 14 + hy, 10 + hx, 14 + hy, HAIR)
    s.r(14 + hx, 10 + hy, 18 + hx, 10 + hy, HAIR)
    s.px(SKIN_D, (12 + hx, 13 + hy), (12 + hx, 14 + hy), (13 + hx, 14 + hy))                   # ear
    _colander(s, 9 + hx, 21 + hx, 4 + hy, [(2, (13 + hx, 16 + hx, 19 + hx)), (4, (10 + hx, 12 + hx, 15 + hx, 18 + hx))],
              front_nub=False)
    # face
    if eyes_shut:
        s.px(OUT, (15 + hx, 13 + hy), (16 + hx, 13 + hy), (19 + hx, 13 + hy), (20 + hx, 13 + hy))
    else:
        s.px(OUT, (16 + hx, 12 + hy), (16 + hx, 13 + hy), (19 + hx, 12 + hy), (20 + hx, 12 + hy), (19 + hx, 13 + hy), (20 + hx, 13 + hy))
        s.px(EYE_HI, (20 + hx, 12 + hy))
    s.px(FRECKLE, (14 + hx, 14 + hy), (15 + hx, 15 + hy), (19 + hx, 14 + hy), (21 + hx, 14 + hy))
    s.px(SKIN_D, (21 + hx, 13 + hy))                                                             # nose bump
    s.px(MOUTH, (16 + hx, 15 + hy), (20 + hx, 15 + hy))
    s.px(TOOTH, (17 + hx, 15 + hy), (19 + hx, 15 + hy)); s.px(MOUTH, (18 + hx, 15 + hy))         # gap tooth
    s.r(17 + hx, 16 + hy, 19 + hx, 16 + hy, MOUTH)
    # front arm: yellow sleeve, then skin to a mitten hand
    pts = _line(20, 19 + oy, hand[0], hand[1])
    for i, (x, y) in enumerate(pts):
        s.r(x, y, x + 1, y + 1, TEE if i < 1 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))
    return s.im


def scrap(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: yellow sleeves, skin
    for x in (13, 25):
        s.r(x, 18, x + 1, 19, TEE); s.r(x, 20, x + 1, 22, SKIN); s.px(SKIN_D, (x, 22), (x + 1, 22))
    s.px(TEE_D, (13, 19), (26, 19))
    # bare legs, odd shoes: image left = his right = purple, image right = his left = orange
    for x in (16, 22):
        s.r(x, 26, x + 1, 28, SKIN); s.px(SKIN_D, (x, 28))
    s.r(15, 29, 18, 30, SHOE_P); s.r(21, 29, 24, 30, SHOE_O)
    s.r(15, 24, 24, 25, SHORTS); s.r(19, 25, 20, 25, SHORTS_D)
    # patched tee
    s.r(16, 18, 23, 18, TEE); s.r(15, 19, 24, 23, TEE)
    s.r(15, 19, 15, 23, TEE_D); s.r(24, 19, 24, 23, TEE_D); s.r(16, 23, 23, 23, TEE_D)
    s.r(21, 19, 22, 20, PATCH_O)
    s.r(17, 21, 18, 21, PATCH_B)
    # head
    s.r(13, 10, 26, 16, SKIN); s.r(14, 17, 25, 17, SKIN); s.px(SKIN_D, (14, 17), (25, 17))
    s.r(13, 10, 14, 12, HAIR); s.r(25, 10, 26, 12, HAIR); s.r(15, 10, 17, 10, HAIR); s.r(22, 10, 24, 10, HAIR)
    s.px(SKIN_D, (12, 13), (12, 14), (27, 13), (27, 14))                                        # ears
    _colander(s, 13, 26, 4, [(2, (17, 20, 23)), (4, (15, 18, 21, 24))])
    # face: big eyes, freckles, gap-toothed grin
    s.px(OUT, (16, 12), (17, 12), (16, 13), (17, 13), (22, 12), (23, 12), (22, 13), (23, 13))
    s.px(EYE_HI, (17, 12), (23, 12))
    s.px(FRECKLE, (15, 14), (16, 15), (24, 14), (23, 15))
    s.px(SKIN_D, (19, 14), (20, 14))
    s.px(MOUTH, (17, 15), (22, 15))
    s.px(TOOTH, (18, 15), (19, 15), (21, 15)); s.px(MOUTH, (20, 15))                           # gap tooth
    s.r(18, 16, 21, 16, MOUTH)
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


if __name__ == "__main__":
    import json
    from PIL import Image
    out = "characters/scrap/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames = scrap(), sheet()
    frames.save(f"{out}/scrap_frames.png")
    front.save(f"{out}/scrap_pixel.png")
    with open(f"{out}/scrap_frames.json", "w") as f:
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
    rev.save(f"{out}/scrap_pixel_sheet.png")
    print("wrote", out)
