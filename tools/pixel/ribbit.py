"""Ribbit's pixel form for The Hill (Pillow only, drawn in code). See characters/ribbit/look.md.

ribbit()      front form, 40 x 32, outlined, feet on the bottom row
frame(name)   unoutlined 32 x 32 three-quarter frame facing right, feet on row 30, feet centre x=16
sheet()       the 128 x 224 player sheet
Scale: 26 px drawn (28 with the outline): frog-eye bumps 3 px above the hood, hood 12, torso 8,
shorts 2, feet 2. The 3D at true scale traces 31 px; it is compressed (mostly the big hood) so Ribbit
reads small next to Jeff (32) and the hop can lift him 4 px inside the 32 px frame.
The walk row is a two-footed hop: walk0 crouch, walk1 push off, walk2 top (tucked, +4 px), walk3 land.
"""
import os

from px import Spr, up, silhouette, OUT
import jarling_frames

TEAL, TEAL_D = "#2A9DB0", "#1F7F8F"           # frog hoodie; far side / back arm
WHITE, PUPIL = "#F5F5F2", "#15151A"           # hood eyes
SKIN, SKIN_D = "#F0BE94", "#D9A27A"
BELLY = "#F6D44A"                              # belly panel and footies
FEET, FEET_D = "#F6D44A", "#D9B630"
SHORTS, SHORTS_D = "#22336B", "#18264F"
BLUSH = "#F2A08C"

HAND = (22, 22)

# leg sets: lift (whole figure up), body dy (squash: upper body sinks onto the feet),
# feet (back dx, front dx), feet raised (tuck), toes down (push off / dangle)
LEGS = {
    "stand":  dict(lift=0, dy=0, feet=(0, 0), raise_=0, toes=False),
    "crouch": dict(lift=0, dy=2, feet=(-1, 1), raise_=0, toes=False),
    "push":   dict(lift=2, dy=0, feet=(0, 0), raise_=0, toes=True),
    "top":    dict(lift=4, dy=0, feet=(1, 1), raise_=1, toes=False),
    "land":   dict(lift=0, dy=1, feet=(-1, 1), raise_=0, toes=False),
    "tuck":   dict(lift=2, dy=0, feet=(1, 1), raise_=1, toes=False),
    "dangle": dict(lift=0, dy=0, feet=(0, 0), raise_=0, toes=True),
    "step":   dict(lift=0, dy=0, feet=(-1, 1), raise_=0, toes=False),
}
# name: legs, head dx, back-arm offset, hand (The Hill's POSES for Jeff; walk = the hop)
POSES = {
    "idle0": ("stand", 0, (0, 0), (22, 22)),
    "idle1": ("land", 0, (0, 1), (22, 23)),
    "walk0": ("crouch", 0, (0, 1), (22, 24)),
    "walk1": ("push", 0, (-1, -1), (23, 18)),
    "walk2": ("top", 0, (-1, -2), (23, 15)),
    "walk3": ("land", 0, (0, 1), (22, 23)),
    "jump": ("tuck", 0, (-1, -3), (23, 15)),
    "fall": ("dangle", 0, (-1, -4), (24, 14)),
    "side0": ("stand", -1, (0, 0), (18, 16)),
    "side1": ("step", 1, (1, -1), (22, 19)),
    "side2": ("stand", 0, (0, 0), (21, 20)),
    "down0": ("stand", 0, (0, -1), (22, 11)),
    "down1": ("crouch", 1, (0, 0), (24, 18)),
    "down2": ("stand", 0, (0, 0), (23, 17)),
}


def _line(x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def _bump(s, x, y, pupil_dx=1):
    """A frog eye on the hood: 5x5 teal ball, 3x3 white, dark pupil pixel facing forward."""
    s.e(x, y, x + 4, y + 4, TEAL)
    s.r(x + 1, y + 1, x + 3, y + 3, WHITE)
    s.px(PUPIL, (x + 2 + pupil_dx, y + 2))


def _face(s, ex, ey, mx, my, shut):
    """Half-lidded calm eyes (2 px dark under a skin-shade lid) and the wide flat smile."""
    for x in ex:
        if shut:
            s.px(OUT, (x, ey + 1), (x + 1, ey + 1))
        else:
            s.px(SKIN_D, (x, ey), (x + 1, ey))
            s.px(OUT, (x, ey + 1), (x + 1, ey + 1))
    s.r(mx, my, mx + 4, my, OUT)                        # 5 px flat smile, nothing sticking out


def ribbit(view="front"):
    s = Spr(jarling_frames.W, jarling_frames.H)
    # arms behind the body
    s.e(8, 15, 12, 21, TEAL); s.e(28, 15, 32, 21, TEAL)
    s.r(9, 20, 10, 21, SKIN); s.r(30, 20, 31, 21, SKIN)
    s.e(11, 13, 29, 23, TEAL)                           # round torso
    s.e(14, 15, 26, 22, BELLY)                          # belly panel
    s.r(13, 21, 27, 22, SHORTS); s.px(SHORTS_D, (20, 22))
    s.r(15, 23, 16, 23, SKIN); s.r(24, 23, 25, 23, SKIN)
    s.r(13, 24, 18, 25, FEET); s.r(22, 24, 27, 25, FEET)  # bare-look footies
    s.px(FEET_D, (14, 25), (16, 25), (23, 25), (25, 25))  # toe splits
    s.e(11, 3, 29, 15, TEAL)                            # hood dome
    _bump(s, 13, 0, 0); _bump(s, 23, 0, 0)
    s.e(14, 5, 26, 14, SKIN)                            # face opening
    _face(s, (16, 23), 8, 18, 12, False)
    s.px(BLUSH, (15, 11), (25, 11))
    return jarling_frames.fin(s)


def _foot(s, x, y, col, dark, toes):
    if toes:     # pointing down (push off / dangle): narrow and one row taller
        s.r(x + 1, y - 2, x + 3, y, col); s.px(dark, (x + 2, y))
    else:
        s.r(x, y - 1, x + 3, y, col); s.r(x + 4, y, x + 4, y, col); s.px(dark, (x + 2, y), (x + 4, y))


def _arm(s, shoulder, hand, sleeve):
    for x, y in _line(*shoulder, *hand):
        s.r(x, y, x + 1, y + 1, sleeve)
    s.r(hand[0], hand[1], hand[0] + 1, hand[1] + 1, SKIN)


def frame(name, eyes_shut=False):
    legs, hdx, (bax, bay), hand = POSES[name]
    L = LEGS[legs]
    lift, dy = L["lift"], L["dy"]
    o = dy - lift                                       # upper body offset
    fy = 30 - lift - L["raise_"]                        # foot bottom row
    s = Spr(jarling_frames.FW, jarling_frames.FH)
    bdx, fdx = L["feet"]
    _arm(s, (11, 20 + o), (9 + bax, 24 + bay + o), TEAL_D)
    _foot(s, 11 + bdx, fy, FEET_D, SHORTS_D, L["toes"])
    s.px(SKIN_D, (13 + bdx, fy - 2), (14 + bdx, fy - 2))
    _foot(s, 15 + fdx, fy, FEET, FEET_D, L["toes"])
    s.px(SKIN, (16 + fdx, fy - 2), (17 + fdx, fy - 2))
    s.e(9, 18 + o, 22, 27 + o, TEAL)                    # round torso
    s.e(13, 20 + o, 22, 26 + o, BELLY)                  # belly panel, toward the front
    s.r(10, 26 + o, 21, 27 + o, SHORTS); s.px(SHORTS_D, (10, 27 + o), (11, 27 + o))
    hx, ht = hdx, 5 + o                                 # head block (hood top row 7 + o)
    s.e(8 + hx, ht + 2, 23 + hx, ht + 14, TEAL)         # hood dome
    s.px(TEAL_D, (8 + hx, ht + 8), (8 + hx, ht + 9))
    _bump(s, 10 + hx, ht, 1); _bump(s, 16 + hx, ht, 1)  # two frog eyes, 1 px teal gap between balls
    s.e(13 + hx, ht + 5, 23 + hx, ht + 13, SKIN)        # face opening, shifted right
    s.px(TEAL, (23 + hx, ht + 7), (23 + hx, ht + 11))   # hood rim on the near edge
    _face(s, (15 + hx, 20 + hx), ht + 7, 16 + hx, ht + 11, eyes_shut)
    s.px(BLUSH, (21 + hx, ht + 10))
    _arm(s, (19, 20 + o), hand, TEAL)
    return s.im


def sheet():
    return jarling_frames.sheet(frame)


if __name__ == "__main__":
    from PIL import Image
    import json
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    outd = os.path.join(root, "characters", "ribbit", "refs", "pixel")
    os.makedirs(outd, exist_ok=True)
    front, sh = ribbit(), sheet()
    sh.save(os.path.join(outd, "ribbit_frames.png"))
    front.save(os.path.join(outd, "ribbit_pixel.png"))
    with open(os.path.join(outd, "ribbit_frames.json"), "w") as f:
        json.dump(jarling_frames.manifest(HAND), f, indent=2)
    bb = front.getbbox()
    fig = front.crop(bb)
    k16 = 16 / fig.height
    sil = silhouette(fig).resize((max(1, round(fig.width * k16)), 16), Image.NEAREST)
    parts = [up(front, 8), up(sh, 4), front, up(front, 2), up(sil, 4)]
    W = sum(p.width for p in parts) + 24 * (len(parts) + 1)
    H = max(p.height for p in parts) + 48
    rev = Image.new("RGBA", (W, H), (0xF6, 0xEF, 0xE0, 255))
    x = 24
    for p in parts:
        rev.alpha_composite(p, (x, 24)); x += p.width + 24
    rev.convert("RGB").save(os.path.join(outd, "ribbit_pixel_sheet.png"))
    print("PIXEL ribbit", front.getbbox(), "figure", fig.size)
