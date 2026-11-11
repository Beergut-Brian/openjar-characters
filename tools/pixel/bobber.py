"""Bobber's pixel form for The Hill and Life of a Worm (Pillow only, drawn in code, traced from the 3D side view).

bobber(view="front")          front form, 40 x 32, outlined, feet on the bottom row
frame(name, eyes_shut=False)  unoutlined 32 x 32 three-quarter frame facing right, feet on row 30
sheet()                       the 128 x 224 player sheet
sit_dock(frame=0)             unoutlined 32 x 48 cutscene frame (Life of a Worm): sitting on the dock edge, facing right,
                              seat line on row 24 (the frame's mid-height), the dock edge at x 19 (seat point (21, 24)),
                              knees bent over the edge, lower legs and sandals dangling; frame 1 swings the feet

31 px tall with the outline (0.85 m kid body, 22 rows to the top of the head, plus the oversized sou'wester, traced from
refs/jarling/bobber_side_sprite.png): rain hat 7 rows (round dome crown 6 rows + one brim row, the brim much wider than the
head and drooping 4 rows longer at the back: the biggest shape), head 7 rows (sandy hair peeking under the brim, big round
dark eyes, freckles, gap-toothed grin), striped tee 7 rows (teal and cream alternate rows), denim shorts 2 rows + a light
cuff row, bare legs 3 rows, little brown sandals 2 rows. No hat tie (nothing at the mouth), no rod (the rod is 3D gear).
No player colours anywhere.
"""
import os
from PIL import Image
from px import Spr, OUT, up, silhouette, rgba, outline
import jarling_frames as jf

SKIN, SKIN_D = "#F0B488", "#D0926A"
HAIR = "#8A5A34"
FRECKLE = HAIR                       # a lighter freckle brown drifts under ΔE00 20 from P2
HAT, HAT_D = "#F6C833", "#C79F1E"
TEE, TEE_D, STRIPE, STRIPE_D = "#2FA7A0", "#23807B", "#F1E7CF", "#D3C7AA"
DENIM, DENIM_D, CUFF = "#3D5A88", "#2E4670", "#5873A0"
SANDAL, SANDAL_D = "#9A6A3C", "#7A5230"
WHITE, MOUTH = "#F7F7F5", "#6A2232"

HAND = (19, 21)
SIT_W, SIT_H, SEAT = 32, 48, (21, 24)

# name: legs, lift, head dx, back-arm (dx, dy), hand (x, y), body drop  (hands from The Hill's POSES, kid-sized)
# Bobber's hat fills the frame top, so the jump tucks the feet instead of lifting the body.
POSES = {
    "idle0": ("stand", 0, 0, (0, 0), (19, 21), 0),
    "idle1": ("stand", 0, 0, (0, 1), (19, 22), 1),
    "walk0": ("contact", 0, 0, (1, 0), (19, 21), 0),
    "walk1": ("pass", 0, 0, (0, 0), (19, 20), 0),
    "walk2": ("contact2", 0, 0, (-1, 0), (19, 21), 0),
    "walk3": ("pass2", 0, 0, (0, 0), (19, 20), 0),
    "jump": ("tuck", 0, 0, (-1, -3), (22, 17), 0),
    "fall": ("dangle", 0, 0, (-1, -4), (23, 16), 0),
    "side0": ("stand", 0, -1, (0, 0), (17, 17), 0),
    "side1": ("contact", 0, 1, (1, -1), (21, 19), 0),
    "side2": ("stand", 0, 0, (0, 0), (20, 20), 0),
    "down0": ("stand", 0, 0, (0, -1), (22, 16), 0),
    "down1": ("crouch", 0, 1, (0, 0), (22, 19), 1),
    "down2": ("stand", 0, 0, (0, 0), (21, 18), 0),
}

# ((back hip x, back foot x, back foot y), (front hip x, front foot x, front foot y)); shorts 3 px wide, legs 2, sandals 4
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
    """One leg from the hip (row `top`) to the sole row fy: 2 rows of denim, a light cuff row, bare skin, then a little
    sandal (a strap row over the foot, toes peeking out in front, a sole row; toe to the right)."""
    for i, y in enumerate(range(top, fy + 1)):
        t = i / max(1, fy - top)
        x = round(hx + (fx - hx) * t)
        if y == fy:
            s.r(x, y, x + 3, y, SANDAL_D if back else SANDAL)
        elif y == fy - 1:
            s.r(x, y, x + 3, y, SKIN_D if back else SKIN)
            s.r(x, y, x + 1, y, SANDAL_D if back else SANDAL)                      # strap
        elif y < top + 2:
            s.r(x, y, x + 2, y, DENIM_D if back else DENIM)
        elif y == top + 2:
            s.r(x, y, x + 2, y, DENIM_D if back else CUFF)
        else:
            s.r(x + 1, y, x + 2, y, SKIN_D if back else SKIN)


def _hat_side(s, hx, hy):
    """Sou'wester, three-quarter facing right: round dome crown (6 rows), one brim row much wider than the head, and a long
    back brim that droops 4 rows down behind the neck (the biggest shape on the figure)."""
    for y, x0, x1 in ((2, 12, 18), (3, 11, 19), (4, 10, 20), (5, 10, 20), (6, 10, 20), (7, 9, 21)):
        s.r(x0 + hx, y + hy, x1 + hx, y + hy, HAT)
    s.px(HAT_D, (10 + hx, 5 + hy), (10 + hx, 6 + hy), (9 + hx, 7 + hy), (11 + hx, 3 + hy), (12 + hx, 2 + hy))
    s.px(WHITE, (16 + hx, 3 + hy), (17 + hx, 3 + hy))                                 # shine on the dome
    s.r(5 + hx, 8 + hy, 24 + hx, 8 + hy, HAT)                                        # brim, wider than the head
    s.px(HAT_D, (24 + hx, 8 + hy))                                                   # front lip turns down
    s.r(3 + hx, 9 + hy, 9 + hx, 9 + hy, HAT)                                         # long back brim drooping
    s.r(2 + hx, 10 + hy, 7 + hx, 10 + hy, HAT)
    s.r(2 + hx, 11 + hy, 5 + hx, 11 + hy, HAT)
    s.px(HAT_D, (2 + hx, 12 + hy), (3 + hx, 12 + hy), (2 + hx, 11 + hy), (8 + hx, 9 + hy), (9 + hx, 9 + hy),
         (6 + hx, 10 + hy), (7 + hx, 10 + hy), (4 + hx, 11 + hy), (5 + hx, 11 + hy))  # underside


def _head_side(s, hx, hy, eyes_shut=False):
    s.r(11 + hx, 9 + hy, 21 + hx, 14 + hy, SKIN)
    s.r(12 + hx, 15 + hy, 20 + hx, 15 + hy, SKIN)
    s.r(10 + hx, 9 + hy, 12 + hx, 12 + hy, HAIR); s.px(HAIR, (11 + hx, 13 + hy))       # hair peeking under the back brim
    s.r(13 + hx, 9 + hy, 18 + hx, 9 + hy, HAIR)                                       # fringe under the brim
    s.px(SKIN_D, (13 + hx, 12 + hy), (13 + hx, 13 + hy))                              # ear
    _hat_side(s, hx, hy)
    if eyes_shut:
        s.px(OUT, (15 + hx, 11 + hy), (16 + hx, 11 + hy), (19 + hx, 11 + hy), (20 + hx, 11 + hy))
    else:                                                                             # big round dark eyes, glints
        s.r(15 + hx, 10 + hy, 16 + hx, 11 + hy, OUT); s.px(WHITE, (16 + hx, 10 + hy))
        s.r(19 + hx, 10 + hy, 20 + hx, 11 + hy, OUT); s.px(WHITE, (20 + hx, 10 + hy))
    s.px(FRECKLE, (14 + hx, 11 + hy), (18 + hx, 12 + hy), (21 + hx, 11 + hy))         # freckles
    s.px(SKIN_D, (22 + hx, 11 + hy), (22 + hx, 12 + hy))                              # button nose
    s.px(MOUTH, (16 + hx, 12 + hy), (20 + hx, 12 + hy))                               # grin corners, turned up
    s.px(WHITE, (16 + hx, 13 + hy), (17 + hx, 13 + hy), (19 + hx, 13 + hy))           # teeth with a 1 px gap
    s.px(MOUTH, (18 + hx, 13 + hy), (20 + hx, 13 + hy))
    s.r(17 + hx, 14 + hy, 19 + hx, 14 + hy, MOUTH)


def _tee(s, x0, x1, y0, y1):
    """Teal tee with cream stripes on alternate rows (teal on top at the collar)."""
    for y in range(y0, y1 + 1):
        s.r(x0, y, x1, y, STRIPE if (y - y0) % 2 else TEE)
    for y in range(y0, y1 + 1):
        s.px(STRIPE_D if (y - y0) % 2 else TEE_D, (x0, y))                            # shade at the back


def _upper(s, oy, hx, bax, bay, hand, eyes_shut=False):
    """Back arm, striped tee (rows 16-22 + oy), head and hat, front arm."""
    for i, (x, y) in enumerate(_line(11, 17 + oy, 10 + bax, 21 + oy + bay)):          # back arm: sleeve, skin
        s.r(x, y, x + 1, y + 1, TEE_D if i < 2 else SKIN_D)
    _tee(s, 11, 19, 16 + oy, 22 + oy)
    s.r(20, 18 + oy, 20, 21 + oy, TEE)                                                # a little tummy
    s.px(STRIPE, (20, 19 + oy), (20, 21 + oy))
    _head_side(s, hx, oy, eyes_shut)
    for i, (x, y) in enumerate(_line(17, 17 + oy, hand[0], hand[1])):                 # front arm: striped sleeve, skin
        s.r(x, y, x + 1, y + 1, (TEE, STRIPE)[i] if i < 2 else SKIN)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)
    s.px(SKIN_D, (hand[0], hand[1] + 1))


def frame(name, eyes_shut=False):
    legs, lift, hdx, (bax, bay), hand, drop = POSES[name]
    s = Spr(jf.FW, jf.FH)
    oy = drop - lift
    hip = 23 - lift + (1 if legs == "crouch" else 0)
    (bh, bf, by_), (fh, ff, fy_) = LEGS[legs]
    _leg(s, bh, bf, by_ - lift, hip, back=True)
    _leg(s, fh, ff, fy_ - lift, hip)
    s.r(11, hip - 1 + (1 if legs == "crouch" else 0), 18, hip, DENIM)                 # shorts seat
    s.px(DENIM_D, (11, hip), (12, hip))
    _upper(s, oy, hdx, bax, bay, hand, eyes_shut)
    return s.im


def sit_dock(frame=0):
    """Sitting on the dock edge facing right (Life of a Worm). Seat line row 24 (the frame's mid-height), dock edge at
    x 21: the shorts sit on rows 22-23, the knees bend over the edge and the lower legs and sandals dangle below the seat.
    frame 0: front foot straight down, back foot forward; frame 1: front foot kicked forward, back foot back."""
    s = Spr(SIT_W, SIT_H)
    oy = 22 - 23                                       # the tee ends on row 21, one row above the shorts
    # dangling lower legs: knee (x, 24) -> sandal; (dx per row) for back and front leg
    swing = {0: ((0, 1, 1, 2, 2), (0, 0, 0, 0, 0)), 1: ((0, 0, 0, -1, -1), (0, 1, 1, 2, 3))}[frame]
    for back, kx, dxs in ((True, 21, swing[0]), (False, 23, swing[1])):
        sk, sd = (SKIN_D, SANDAL_D) if back else (SKIN, SANDAL)
        for i, dx in enumerate(dxs):                                                  # shins rows 24-28
            s.r(kx + dx, 24 + i, kx + dx + 1, 24 + i, sk)
        x = kx + dxs[-1]
        s.r(x, 29, x + 2, 29, sk); s.r(x, 29, x + 1, 29, sd)                          # strap over the foot, toes out
        s.r(x, 30, x + 2, 30, sd)                                                     # sole
    # thighs: horizontal on the seat, back thigh darker, cuff at the knee
    s.r(11, 22, 22, 23, DENIM); s.r(11, 23, 14, 23, DENIM_D)
    s.r(21, 22, 22, 23, CUFF)
    s.r(23, 22, 24, 23, SKIN); s.px(SKIN_D, (23, 23))                                 # knees over the edge
    # back hand rests on the dock behind the hip, front hand on the knee
    _upper(s, oy, 0, -1, 2, (22, 20))
    return s.im


def bobber(view="front"):
    s = Spr(jf.W, jf.H)
    # arms: striped sleeves, skin to small hands at the shorts
    for x in (13, 25):
        s.r(x, 16, x + 1, 16, TEE); s.r(x, 17, x + 1, 17, STRIPE); s.r(x, 18, x + 1, 18, TEE)
        s.r(x, 19, x + 1, 22, SKIN); s.px(SKIN_D, (x, 22), (x + 1, 22))
    # sandals: strap over the foot with toes peeking, sole; toes flare outward
    for x, fl in ((15, -1), (21, 1)):
        s.r(x, 29, x + 3, 29, SKIN); s.r(x + 1, 29, x + 2, 29, SANDAL)
        s.r(x, 30, x + 3, 30, SANDAL); s.px(SANDAL_D, (x if fl < 0 else x + 3, 30))
    # bare legs
    for x in (16, 22):
        s.r(x, 26, x + 1, 28, SKIN); s.px(SKIN_D, (x + 1 if x < 19 else x, 26))
    # denim shorts with light cuffs and a split between the legs
    s.r(15, 23, 24, 24, DENIM); s.px(DENIM_D, (15, 23), (24, 23))
    s.r(15, 25, 18, 25, CUFF); s.r(21, 25, 24, 25, CUFF)
    s.r(19, 24, 20, 24, DENIM_D)
    # striped tee
    _tee(s, 15, 24, 16, 22); s.px(TEE_D, (24, 16), (24, 18), (24, 20), (24, 22)); s.px(STRIPE_D, (24, 17), (24, 19), (24, 21))
    # head
    s.r(15, 9, 24, 14, SKIN); s.r(16, 15, 23, 15, SKIN)
    s.r(15, 9, 24, 9, HAIR); s.r(15, 10, 15, 11, HAIR); s.r(24, 10, 24, 11, HAIR)
    s.px(SKIN_D, (14, 12), (25, 12))                                                  # ears
    # sou'wester: round dome crown, one wide brim row, brim drooping down at both sides (longer behind)
    for y, x0, x1 in ((2, 17, 22), (3, 16, 23), (4, 15, 24), (5, 14, 25), (6, 14, 25), (7, 14, 25)):
        s.r(x0, y, x1, y, HAT)
    s.px(WHITE, (17, 3), (18, 3)); s.px(HAT_D, (14, 6), (14, 7), (25, 6), (25, 7))
    s.r(9, 8, 30, 8, HAT)
    s.r(8, 9, 13, 9, HAT); s.r(26, 9, 31, 9, HAT)
    s.r(8, 10, 11, 10, HAT); s.r(28, 10, 31, 10, HAT)
    s.px(HAT_D, (8, 10), (9, 10), (10, 10), (11, 10), (28, 10), (29, 10), (30, 10), (31, 10), (12, 9), (13, 9), (26, 9),
         (27, 9))
    # face: big round dark eyes with glints, freckles, gap-toothed grin
    s.r(17, 10, 18, 11, OUT); s.px(WHITE, (18, 10))
    s.r(21, 10, 22, 11, OUT); s.px(WHITE, (22, 10))
    s.px(FRECKLE, (16, 12), (18, 12), (21, 12), (23, 12))
    s.px(MOUTH, (17, 13), (22, 13))
    s.r(18, 13, 21, 13, WHITE); s.px(MOUTH, (20, 13))                                 # the gap
    s.r(19, 14, 20, 14, MOUTH)
    return jf.fin(s)


def sheet():
    return jf.sheet(frame)


def sit_strip():
    """Both sit_dock frames side by side, outlined, native (64 x 48)."""
    out = Image.new("RGBA", (SIT_W * 2, SIT_H), (0, 0, 0, 0))
    for i in (0, 1):
        out.alpha_composite(outline(sit_dock(i)), (i * SIT_W, 0))
    return out


def colours():
    """Every pixel colour used (for the player-colour check)."""
    return [v for k, v in globals().items() if isinstance(v, str) and v.startswith("#") and k.isupper()] + [OUT]


if __name__ == "__main__":
    import json
    out = "characters/bobber/refs/pixel"
    os.makedirs(out, exist_ok=True)
    front, frames, sits = bobber(), sheet(), sit_strip()
    frames.save(f"{out}/bobber_frames.png")
    front.save(f"{out}/bobber_pixel.png")
    sits.save(f"{out}/bobber_sit_dock.png")
    with open(f"{out}/bobber_frames.json", "w") as f:
        json.dump(jf.manifest(HAND), f, indent=2); f.write("\n")
    sil = silhouette(front.crop(front.getbbox()))
    sil = sil.resize((max(1, round(sil.width * 16 / sil.height)), 16), Image.NEAREST)
    big, fs, ss = up(front, 8), up(frames, 4), up(sits, 4)
    pad = 16
    W = pad * 4 + big.width + fs.width
    H = max(big.height + pad * 4 + front.height * 2 + ss.height, fs.height) + pad * 2
    rev = Image.new("RGBA", (W, H), rgba("#F6EFE0"))
    rev.alpha_composite(big, (pad, pad))
    y = pad * 2 + big.height
    rev.alpha_composite(front, (pad, y)); rev.alpha_composite(up(front, 2), (pad * 2 + front.width, y))
    rev.alpha_composite(up(sil, 4), (pad * 4 + front.width * 3, y))
    rev.alpha_composite(ss, (pad, y + front.height * 2 + pad))
    rev.alpha_composite(fs, (pad * 3 + big.width, pad))
    rev.save(f"{out}/bobber_pixel_sheet.png")
    print("wrote", out, "height", front.getbbox()[3] - front.getbbox()[1])
