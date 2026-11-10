"""Kit v2: head features, data-driven hair pieces, hair presets, face extras and extra mouths.

Head features (`head.features`: list of dicts; body features of the species, NOT hats, so any hat
or helmet still goes on top; each is the part `<id>_part_feature_<type>` on its own bones under `head`):
  antennae     count 2 (1..4), color (default: darker skin), tip (default: color), length 0.75 (x R),
               spread 30 (deg from straight up), ball 0.15 (x R), thickness 0.035 (x R),
               back 0 (deg the stalks lean toward the back of the head)
  horns        style "nub"|"curved", count 2 (1 = one centre horn), color "#F1E7CF", size 1.0
  pointy_ears  color (default: skin), length 0.55 (x R), up 0.5 (how much they point up); replace the round ears
  fins         count 1|3 (centre crest, plus one each side), color (default: darker skin), size 1.0

Hair pieces (`hair.pieces`: list; every piece takes `at` [elevation deg, azimuth deg] with azimuth
0 = front, 90 = the character's left, 180 = back; `size` (x R); `color` (default hair colour);
`mirror` true = also at -azimuth; `keep` true = stays when a hat tucks the hair):
  puff      round puff / bun: size 0.32, squash 1.0 (height factor), out 0.55 (how far it sits out)
  bun       same as puff (size 0.36)
  tuft      short soft lock: size 0.2, length 0.45, dir "out"|"up"|[x,y,z]
  spike     pointed lock: size 0.2, length 0.7, dir "out"|"up"|[x,y,z], lean 0.25 (outward lean when "up")
  tail      hanging pony/pig tail: size 0.22, length 0.8

Hair presets (`hair.style`): puffs (two side puffs), top_bun, upright (wild hair straight up),
pigtails, mohawk, tuft_top; plus every cap style of the core (short, buzz, bob, sleek, ...).

Face extras (`face.extras`: list of names or dicts, drawn into the face atlas):
  smudge       side "L"|"R" (the character's), color "#6B5A4A", size 1.0: dirt / flour smudge on a cheek
  scorch_brow  side "L"|"R", color "#2A2420": that eyebrow is a sooty scorch mark
  mask         color, trim, full-head wrestling mask: whole head in `color`, skin shows in eye and
               mouth openings edged in `trim` (use head.ears "none")
  freckles_big  color (default darker skin): bolder freckles across the cheeks and nose

Mouths (`face.mouth`, besides the core's smile, grin, grin_top, grin_two, o, smirk, set, grit, flat, frown, none):
  grin_gap     open grin with a gap between the front teeth
  yell         wide open happy shout
  wide         wide, flat, pleased smile
"""
import math
import numpy as np
from mathutils import Vector
import jarling_kit as kit
from jarling_kit import ellipsoid_bm, capsule_bm, tube_bm, shade, mix_hex, sd_ellipse, sd_circle, sd_stroke, sd_rrect, bez

UP = Vector((0, 0, 1))

def _at(B, el_deg, az_deg, s=1.0):
    return B.head_point(math.radians(el_deg), math.radians(az_deg), s)

def _normal(B, p):
    """Outward direction of the head ellipsoid at p."""
    L = B.L; c = L["head_c"]; R = L["R"]
    d = p - c
    n = Vector((d.x / (R * L["hsx"]) ** 2, d.y / (R * L["hsy"]) ** 2, d.z / (R * L["hsz"]) ** 2))
    return n.normalized()

# ------------------------------------------------------------------------------------ features
def antennae(B, f):
    L = B.L; R = L["R"]; skin = B.P["skin"]
    n = max(1, min(4, int(f.get("count", 2))))
    col = f.get("color") or shade(skin, 0.78)
    stalk = B.mats.flat("feature_antennae", col, rough=0.5, spec=0.4)
    tip = B.mats.flat("feature_antennae_tip", f.get("tip") or col, rough=0.4, spec=0.5)
    ln = float(f.get("length", 0.75)) * R
    spread = float(f.get("spread", 30))
    ball = float(f.get("ball", 0.15)) * R
    th = float(f.get("thickness", 0.035)) * R
    back = float(f.get("back", 0.0))
    bd = _at(B, 0, 180) - L["head_c"]; back_dir = Vector((bd.x, bd.y, 0)).normalized()
    if n == 1:
        azs = [(0.0, 0.0)]
    else:   # spread across the top of the head, left to right
        azs = [(spread * abs(2 * i / (n - 1) - 1), 90.0 if i >= n / 2 else -90.0) for i in range(n)]
    for i, (off, az) in enumerate(azs):
        base = _at(B, 90 - off, az, 0.96)
        out = _normal(B, base)
        d = (out * 0.55 + UP * 0.85).normalized()
        if back:     # lean the stalk toward the back of the head (deg); 0 keeps the old shape
            d = (d + back_dir * math.tan(math.radians(back))).normalized()
        end = base + d * ln
        mid = base + d * ln * 0.5 + Vector((out.x, out.y, 0)) * ln * 0.10
        pts = [tuple(base.lerp(mid, t).lerp(mid.lerp(end, t), t)) for t in np.linspace(0, 1, 9)]
        side = -1.0 if az < 0 else 1.0
        name = B.add_bob_bone(f"feat_antenna.{i + 1}", base, end, amount=1.6, side=side)
        B.add(tube_bm(pts, th), stalk, name)
        B.add(ellipsoid_bm(base, (th * 2.1, th * 2.1, th * 1.3), segs=14, rings=8), stalk, name)
        B.add(ellipsoid_bm(end, (ball,) * 3, segs=20, rings=12), tip, name)

def horns(B, f):
    L = B.L; R = L["R"]
    style = f.get("style", "nub")
    n = int(f.get("count", 2))
    sz = float(f.get("size", 1.0))
    mat = B.mats.flat("feature_horns", f.get("color", "#F1E7CF"), rough=0.4, spec=0.5)
    spots = [(72, 0)] if n == 1 else [(52, 58), (52, -58)]
    for i, (el, az) in enumerate(spots):
        base = _at(B, el, az, 0.95)
        out = _normal(B, base)
        name = B.add_bob_bone(f"feat_horn.{i + 1}", base, base + out * 0.3 * R, amount=0.0)
        if style == "curved":   # sweeps out, then up and a little forward
            s = 1 if az > 0 else (-1 if az < 0 else 0)
            p1 = base + (out * 0.34 + Vector((s * 0.12, 0, 0))) * R * sz
            p2 = p1 + Vector((s * 0.05, -0.10, 0.36)) * R * sz
            pts = [tuple(base.lerp(p1, t).lerp(p1.lerp(p2, t), t)) for t in np.linspace(0, 1, 10)]
            radii = [1.0 - 0.86 * t for t in np.linspace(0, 1, 10)]
            B.add(tube_bm(pts, 0.125 * R * sz, radii=radii), mat, name)
        else:                   # short rounded cone
            tip = base + (out * 0.75 + UP * 0.25).normalized() * 0.34 * R * sz
            B.add(capsule_bm(base - out * 0.04 * R, tip, 0.135 * R * sz, 0.035 * R * sz, segs=18, hem=5), mat, name)

def pointy_ears(B, f):
    L = B.L; R = L["R"]; c = L["head_c"]
    col = f.get("color")
    mat = B.mats.flat("feature_pointy_ears", col, rough=0.55, spec=0.3) if col else B.skin
    ln = float(f.get("length", 0.55)) * R
    up = float(f.get("up", 0.5))
    for s, side in ((1, "L"), (-1, "R")):
        base = c + Vector((s * R * L["hsx"] * 0.93, 0.02, -0.04 * R))
        d = Vector((s * 1.0, 0.22, up)).normalized()
        tip = base + d * ln
        name = B.add_bob_bone(f"feat_ear.{side}", base, tip, amount=0.35, side=s)
        B.add(capsule_bm(base, tip, 0.17 * R, 0.022 * R, segs=18, hem=5, sx=1.0, sy=0.42), mat, name)

def fins(B, f):
    L = B.L; R = L["R"]; skin = B.P["skin"]
    mat = B.mats.flat("feature_fins", f.get("color") or shade(skin, 0.78), rough=0.5, spec=0.4)
    sz = float(f.get("size", 1.0))
    n = int(f.get("count", 1))
    spots = [(78, 180, 0)] + ([(8, 90, 1), (8, -90, -1)] if n >= 3 else [])
    for i, (el, az, s) in enumerate(spots):
        base = _at(B, el, az, 0.94)
        out = _normal(B, base)
        name = B.add_bob_bone(f"feat_fin.{i + 1}", base, base + out * 0.4 * R, amount=0.6, side=s or 1.0)
        if s == 0:   # crest along the centre line: tall, thin, long front to back
            rot = UP.rotation_difference(out).to_matrix()
            B.add(ellipsoid_bm(base + out * 0.16 * R * sz, (0.045 * R, 0.52 * R * sz, 0.36 * R * sz), rot=rot, segs=24, rings=12), mat, name)
        else:        # side fins: thin, fanned out sideways
            rot = UP.rotation_difference((out + UP * 0.35).normalized()).to_matrix()
            B.add(ellipsoid_bm(base + out * 0.2 * R * sz, (0.26 * R * sz, 0.05 * R, 0.36 * R * sz), rot=rot, segs=24, rings=12), mat, name)

kit.FEATURES.update({"antennae": antennae, "horns": horns, "pointy_ears": pointy_ears, "fins": fins})

# --------------------------------------------------------------------------------- hair pieces
def _spots(pc, default_at):
    el, az = pc.get("at", default_at)
    out = [(el, az)]
    if pc.get("mirror") and az % 360 not in (0, 180):
        out.append((el, -az))
    return out

def _dir(B, pc, base, default="out"):
    d = pc.get("dir", default)
    out = _normal(B, base)
    if d == "up":
        return (UP + out * float(pc.get("lean", 0.25))).normalized()
    if d == "out":
        return out
    return Vector(d).normalized()

def hp_puff(B, pc, mat, size=0.32):
    R = B.L["R"]
    r = float(pc.get("size", size)) * R
    for el, az in _spots(pc, (35, 95)):
        p = _at(B, el, az, 1.0)
        c = p + _normal(B, p) * r * float(pc.get("out", 0.55))
        B.add(ellipsoid_bm(c, (r, r, r * float(pc.get("squash", 1.0))), segs=24, rings=14), mat, "head")

def hp_bun(B, pc, mat):
    hp_puff(B, pc, mat, size=0.36)

def hp_tuft(B, pc, mat):
    R = B.L["R"]
    r = float(pc.get("size", 0.2)) * R; ln = float(pc.get("length", 0.45)) * R
    for el, az in _spots(pc, (85, 0)):
        base = _at(B, el, az, 0.98)
        B.add(capsule_bm(base, base + _dir(B, pc, base) * ln, r, r * 0.45, segs=16, hem=5), mat, "head")

def hp_spike(B, pc, mat):
    R = B.L["R"]
    r = float(pc.get("size", 0.2)) * R; ln = float(pc.get("length", 0.7)) * R
    for el, az in _spots(pc, (85, 0)):
        base = _at(B, el, az, 0.96)
        B.add(capsule_bm(base, base + _dir(B, pc, base) * ln, r, r * 0.14, segs=14, hem=4), mat, "head")

def hp_tail(B, pc, mat):
    R = B.L["R"]
    r = float(pc.get("size", 0.22)) * R; ln = float(pc.get("length", 0.8)) * R
    for el, az in _spots(pc, (30, 180)):
        base = _at(B, el, az, 1.04)
        out = _normal(B, base)
        B.add(ellipsoid_bm(base + out * r * 0.3, (r * 0.75,) * 3, segs=16, rings=10), mat, "head")
        B.add(capsule_bm(base + out * r * 0.5, base + out * r * 0.9 + Vector((0, 0, -ln)), r, r * 0.6, segs=18), mat, "head")

kit.HAIR_PIECES.update({"puff": hp_puff, "bun": hp_bun, "tuft": hp_tuft, "spike": hp_spike, "tail": hp_tail})

_UPRIGHT = [{"type": "spike", "at": [el, az], "dir": "up", "size": sz, "length": ln, "lean": 0.3}
            for el, az, sz, ln in ((88, 0, 0.26, 1.0), (62, 0, 0.22, 0.85), (62, 55, 0.22, 0.9), (62, -55, 0.22, 0.9),
                                   (62, 115, 0.22, 0.85), (62, -115, 0.22, 0.85), (62, 180, 0.22, 0.8),
                                   (40, 80, 0.2, 0.7), (40, -80, 0.2, 0.7), (40, 140, 0.2, 0.65), (40, -140, 0.2, 0.65))]
kit.HAIR_PRESETS.update({
    "puffs":    {"base": "sleek", "pieces": [{"type": "puff", "at": [38, 95], "size": 0.32, "mirror": True}]},
    "top_bun":  {"base": "sleek", "pieces": [{"type": "bun", "at": [78, 180], "size": 0.36, "squash": 0.85}]},
    "upright":  {"base": "short", "pieces": _UPRIGHT},
    "pigtails": {"base": "sleek", "pieces": [{"type": "tail", "at": [25, 100], "size": 0.2, "length": 0.75, "mirror": True}]},
    "mohawk":   {"base": "buzz", "pieces": [{"type": "spike", "at": [el, az], "dir": "out", "size": 0.2, "length": 0.55}
                                             for el, az in ((60, 0), (80, 0), (80, 180), (60, 180), (40, 180))]},
    "tuft_top": {"base": "none", "pieces": [{"type": "tuft", "at": [88, 0], "dir": "up", "size": 0.2, "length": 0.5}]},
})

# --------------------------------------------------------------------------------- face extras
def _eye_xy(face, side):
    sx = 1 if side == "L" else -1          # the character's left is +x on the face canvas
    return sx, sx * face["eye_spacing"], float(face.get("eye_y", kit.EYE_Y))

def fx_smudge(cv, face, e, skin, spec):
    sx = 1 if e.get("side", "L") == "L" else -1
    k = float(e.get("size", 1.0)); col = e.get("color", "#6B5A4A")
    cx, cy = sx * 0.50, -0.27
    sl, X, Y = cv.grid(cx - 0.3, cy - 0.25, cx + 0.3, cy + 0.25)
    d = kit.smin(sd_ellipse(X, Y, cx, cy, 0.13 * k, 0.055 * k, 0.5 * sx), sd_ellipse(X, Y, cx + sx * 0.05, cy + 0.06, 0.07 * k, 0.035 * k, -0.3 * sx), 0.04)
    cv.paint(sl, d, col, 0.62, soft=0.03)
    cv.paint(sl, sd_circle(X, Y, cx - sx * 0.13, cy - 0.07, 0.02 * k), col, 0.5, soft=0.015)

def fx_scorch_brow(cv, face, e, skin, spec):
    side = e.get("side", "L")
    sx, ex, ey = _eye_xy(face, side)
    col = e.get("color", "#2A2420")
    by = ey + kit.EYES[face["eyes"]]["ry"] * spec["eye_scale"] + 0.12 + spec["brow_raise"]
    sl, X, Y = cv.grid(ex - 0.26, by - 0.14, ex + 0.26, by + 0.18)
    cv.paint(sl, sd_ellipse(X, Y, ex, by + 0.01, 0.17, 0.075, 0.12 * sx), col, 0.38, soft=0.06)     # soot halo
    pts = [(ex - sx * 0.12, by - 0.012), (ex - sx * 0.05, by + 0.03), (ex + sx * 0.015, by - 0.005), (ex + sx * 0.07, by + 0.035), (ex + sx * 0.13, by + 0.005)]
    cv.paint(sl, sd_stroke(X, Y, pts, 0.05, 0.03), col)                                             # jagged burnt brow
    for dx, dy in ((0.02, 0.085), (-0.07, 0.07), (0.11, 0.075)):
        cv.paint(sl, sd_circle(X, Y, ex + sx * dx, by + dy, 0.012), col, 0.8)

def fx_mask(cv, face, e, skin, spec):
    col = e.get("color", "#E0B12E"); trim = e.get("trim", "#6B2FA8")
    sl, X, Y = cv.grid(cv.x0, cv.y0, cv.x1, cv.y1)
    ey = float(face.get("eye_y", kit.EYE_Y)); ex = face["eye_spacing"]
    holes = None
    for sx in (-1, 1):   # teardrop eye openings, flared outwards
        d = kit.smin(sd_ellipse(X, Y, sx * ex, ey, 0.185, 0.215), sd_ellipse(X, Y, sx * (ex + 0.12), ey + 0.11, 0.10, 0.09), 0.08)
        holes = d if holes is None else np.minimum(holes, d)
    holes = np.minimum(holes, sd_ellipse(X, Y, 0, kit.MOUTH_Y - 0.02, 0.30, 0.185))
    cv.paint(sl, -holes, col)                                   # everything outside the openings
    cv.paint(sl, np.abs(holes - 0.022) - 0.022, trim)           # trim around each opening
    pts = [(0, kit.MOUTH_Y + 0.24), (0, 1.2)]                   # centre seam up the forehead
    cv.paint(sl, np.maximum(sd_stroke(X, Y, pts, 0.03), -holes + 0.04), trim)

def fx_freckles_big(cv, face, e, skin, spec):
    col = e.get("color") or shade(skin, 0.66)
    for sx in (-1, 1):
        for fx, fy in ((0.40, -0.20), (0.50, -0.16), (0.47, -0.27), (0.58, -0.24), (0.33, -0.27)):
            sl, X, Y = cv.grid(sx * fx - 0.04, fy - 0.04, sx * fx + 0.04, fy + 0.04)
            cv.paint(sl, sd_circle(X, Y, sx * fx, fy, 0.019), col, 0.9)
    for fx, fy in ((-0.05, -0.14), (0.06, -0.15), (0.0, -0.10)):
        sl, X, Y = cv.grid(fx - 0.04, fy - 0.04, fx + 0.04, fy + 0.04)
        cv.paint(sl, sd_circle(X, Y, fx, fy, 0.016), col, 0.9)

kit.FACE_EXTRAS.update({"smudge": (fx_smudge, "under"), "scorch_brow": (fx_scorch_brow, "over"),
                        "mask": (fx_mask, "under"), "freckles_big": (fx_freckles_big, "under")})

# -------------------------------------------------------------------------------------- mouths
def m_grin_gap(cv, line, y, w):
    kit.open_mouth(cv, w * 1.1, y, 0.14, "top", line)
    sl, X, Y = cv.grid(-0.06, y - 0.06, 0.06, y + 0.06)
    cv.paint(sl, sd_rrect(X, Y, 0.0, y + 0.012, 0.021, 0.034, 0.008), kit.MOUTH_DARK)   # the gap between the front teeth

def m_yell(cv, line, y, w):
    kit.open_mouth(cv, w * 1.3, y - 0.01, 0.20, "top", line)

def m_wide(cv, line, y, w):
    sl, X, Y = cv.grid(-0.45, y - 0.2, 0.45, y + 0.2)
    pts = [(-w * 1.75, y + 0.035)] + bez((-w * 1.55, y), (0, y - 0.035), (w * 1.55, y)) + [(w * 1.75, y + 0.035)]
    cv.paint(sl, sd_stroke(X, Y, pts, 0.038), line)

kit.MOUTH_DRAW.update({"grin_gap": m_grin_gap, "yell": m_yell, "wide": m_wide})
