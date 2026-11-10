"""Jarlings: Open Jar Games' own avatar kit.

Library used by build_jarling.py, render_refs.py and render_scenes.py (run inside Blender 5.x).
Everything is procedural: geometry from bmesh, face parts drawn as signed-distance shapes into a
2x2 expression atlas with numpy. No external assets.

Conventions: metres, Z up, the Jarling faces -Y (glTF/Godot: faces +Z), feet on Z=0.
Character's left is +X.
"""
import math, random, copy
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler, Quaternion

# --------------------------------------------------------------------------------------- colour
def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def srgb_to_lin(c):
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

def shade(h, k):
    r, g, b = hex_rgb(h)
    return "#%02X%02X%02X" % tuple(int(max(0, min(1, x * k)) * 255 + 0.5) for x in (r, g, b))

def mix_hex(a, b, t):
    ca, cb = hex_rgb(a), hex_rgb(b)
    return "#%02X%02X%02X" % tuple(int((x * (1 - t) + y * t) * 255 + 0.5) for x, y in zip(ca, cb))

PLAYER_GREEN = "#3CC24A"
PLAYER_RED = "#E4393C"

def is_fantasy_skin(skin):
    """True for skins outside the human range (blue, green, purple, grey...): their blush, brows
    and face lines are derived from the skin colour instead of the human defaults."""
    import colorsys
    h, s_, _v = colorsys.rgb_to_hsv(*hex_rgb(skin))
    return not (7 / 360 <= h <= 45 / 360 and s_ >= 0.12)

def luminance(h):
    r, g, b = srgb_to_lin(hex_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def face_colours(face, skin):
    """Blush, line and brow colours for a face. Explicit `blush_color` / `line_color` /
    `brow_color` win; otherwise human skins keep the kit's originals and fantasy skins derive
    them from the skin so they read on blue, green, purple or grey."""
    fantasy = is_fantasy_skin(skin)
    dark = luminance(skin) < 0.16
    line = mix_hex(face["eye_color"], MOUTH_DARK, 0.35)
    if hex_rgb(skin)[0] < 0.5 and not fantasy:   # deep skin: darker lines so the mouth still reads
        line = shade(line, 0.7)
    blush = "#FF7F86"
    brow = face["brow_color"]
    if fantasy:
        blush = mix_hex(shade(skin, 0.72), "#F0509A", 0.5) if not dark else mix_hex(skin, "#FF9AC8", 0.45)
        line = mix_hex(shade(skin, 0.30), face["eye_color"], 0.35) if not dark else shade(skin, 0.35)
        if face.get("_brow_auto"):
            brow = shade(skin, 0.42) if not dark else mix_hex(skin, "#FFFFFF", 0.5)
    return dict(blush=face.get("blush_color") or blush, line=face.get("line_color") or line, brow=brow)

from colour_rule import delta_e2000, de2000_lab, main_colours, player_colour_clashes, PLAYER_DE_MIN   # noqa: E402  (pure Python, also used by tools/check_colours.py)

# ------------------------------------------------------------------------------------- defaults
DEFAULTS = {
    "id": "jarling", "name": "Jarling",
    "head": {"shape": "round", "size": 1.0, "ears": "round"},
    "skin": "#F2C29B",
    "face": {
        "eyes": "drop", "brows": "soft", "nose": "button", "mouth": "smile",
        "eye_color": "#2A1E2C", "brow_color": "#5A3A28", "lid": 0.0, "lid_low": 0.0,
        "lid_tilt": 0.0, "brow_tilt": 0.0, "brow_raise": 0.0, "blush": 0.45,
        "freckles": False, "eye_spacing": 0.34, "expressions": {},
    },
    "hair": {"style": "short", "color": "#5A3A28"},
    "headwear": {"type": "none"},
    "body": {"build": "regular", "height": 1.0},
    "outfit": {
        "top": {"style": "tee", "color": "#3E7BEA", "accent": "#FFFFFF"},
        "bottoms": {"style": "pants", "color": "#3B5BA5"},
        "shoes": {"style": "sneaker", "color": "#FFFFFF", "sole": "#F4F4F0"},
    },
    "costume": [],
    "posture": {"spine_lean": 0.0, "head_lean": 0.0, "arm_out": 0.0},
}

def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out

# ----------------------------------------------------------------------- 2D signed-distance canvas
class Canvas:
    """Float RGB canvas, Y up. Coordinates are mapped from frame (x0..x1, y0..y1)."""
    def __init__(self, w, h, frame, bg):
        self.w, self.h = w, h
        self.x0, self.x1, self.y0, self.y1 = frame
        self.img = np.empty((h, w, 3), np.float32)
        self.img[:] = hex_rgb(bg) if isinstance(bg, str) else bg
        self.px = (self.x1 - self.x0) / w

    def grid(self, bx0, by0, bx1, by1):
        sx = (self.x1 - self.x0) / self.w; sy = (self.y1 - self.y0) / self.h
        j0 = max(0, int((bx0 - self.x0) / sx) - 2); j1 = min(self.w, int((bx1 - self.x0) / sx) + 3)
        i0 = max(0, int((self.y1 - by1) / sy) - 2); i1 = min(self.h, int((self.y1 - by0) / sy) + 3)
        if j1 <= j0 or i1 <= i0:
            return None, None, None
        xs = self.x0 + (np.arange(j0, j1) + 0.5) * sx
        ys = self.y1 - (np.arange(i0, i1) + 0.5) * sy
        X, Y = np.meshgrid(xs, ys)
        return (slice(i0, i1), slice(j0, j1)), X.astype(np.float32), Y.astype(np.float32)

    def paint(self, sl, d, color, opacity=1.0, soft=0.0):
        if sl is None:
            return
        a = np.clip(0.5 - d / (self.px + soft), 0.0, 1.0) * opacity
        c = np.array(hex_rgb(color) if isinstance(color, str) else color, np.float32)
        reg = self.img[sl]
        reg[:] = reg * (1 - a[..., None]) + c * a[..., None]

def sd_ellipse(X, Y, cx, cy, rx, ry, rot=0.0):
    x = X - cx; y = Y - cy
    if rot:
        c, s = math.cos(rot), math.sin(rot)
        x, y = c * x + s * y, -s * x + c * y
    k0 = np.sqrt((x / rx) ** 2 + (y / ry) ** 2)
    k1 = np.sqrt((x / rx ** 2) ** 2 + (y / ry ** 2) ** 2) + 1e-6
    return k0 * (k0 - 1.0) / k1

def sd_circle(X, Y, cx, cy, r):
    return np.sqrt((X - cx) ** 2 + (Y - cy) ** 2) - r

def sd_stroke(X, Y, pts, w0, w1=None):
    """Distance to a tapered polyline (round caps). Width goes w0 -> w1 along the line."""
    w1 = w0 if w1 is None else w1
    lens = [0.0]
    for a, b in zip(pts, pts[1:]):
        lens.append(lens[-1] + math.dist(a, b))
    total = lens[-1] or 1.0
    d = None
    for k, (a, b) in enumerate(zip(pts, pts[1:])):
        ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy + 1e-12
        h = np.clip(((X - ax) * dx + (Y - ay) * dy) / L2, 0, 1)
        dist = np.sqrt((X - ax - dx * h) ** 2 + (Y - ay - dy * h) ** 2)
        t = (lens[k] + h * math.sqrt(L2)) / total
        dk = dist - (w0 + (w1 - w0) * t) * 0.5
        d = dk if d is None else np.minimum(d, dk)
    return d

def bez(p0, p1, p2, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in np.linspace(0, 1, n)]

def sd_rrect(X, Y, cx, cy, hw, hh, r):
    qx = np.abs(X - cx) - hw + r; qy = np.abs(Y - cy) - hh + r
    return np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r

def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)

# --------------------------------------------------------------------------------- face parts
# All sizes in face units: the head's front half spans -1..1 in x and z.
EYES = {
    "drop":   dict(rx=0.100, ry=0.140),
    "round":  dict(rx=0.115, ry=0.118),
    "button": dict(rx=0.075, ry=0.082),
    "wide":   dict(rx=0.128, ry=0.105),
    "almond": dict(rx=0.120, ry=0.090, rot=0.12),
    "lash":   dict(rx=0.100, ry=0.135, lash=True),
}
BROWS = {  # inner width, outer width, half length, arch
    "thin":   (0.026, 0.020, 0.085, 0.025),
    "soft":   (0.042, 0.032, 0.090, 0.022),
    "arched": (0.030, 0.022, 0.090, 0.050),
    "thick":  (0.080, 0.064, 0.110, 0.012),
    "bushy":  (0.095, 0.050, 0.105, 0.030),
    "none":   None,
}
NOSES = ["button", "dot", "curve", "bump", "none"]   # "bump" is a small 3D nose, not drawn
MOUTHS = ["smile", "grin", "grin_two", "grin_top", "o", "smirk", "set", "grit", "flat", "frown", "none"]   # "none": hidden (e.g. by a beard)

EXPRESSIONS = ["neutral", "happy", "surprised", "determined"]
EXPR_DEFAULTS = {
    "neutral": {},
    "happy": {"eye_mode": "arc", "brow_raise": 0.035, "mouth": "grin_top", "blush_add": 0.25},
    "surprised": {"eye_scale": 1.22, "lid": 0.0, "lid_low": 0.0, "lid_tilt": 0.0,
                  "brow_raise": 0.085, "brow_tilt": -0.18, "mouth": "o"},
    "determined": {"lid": 0.36, "lid_low": 0.0, "lid_tilt": 0.28, "brow_raise": -0.035,
                   "brow_tilt": 0.40, "mouth": "grit"},
}
# Godot/glTF UV offset for each expression cell (texture v grows downwards in glTF).
EXPR_UV_OFFSET = {"neutral": (0.0, 0.0), "happy": (0.5, 0.0), "surprised": (0.0, 0.5), "determined": (0.5, 0.5)}

EYE_Y = -0.04
MOUTH_Y = -0.40
NOSE_Y = -0.22
MOUTH_DARK = "#6A2232"
TONGUE = "#F2848C"
TEETH = "#FFFFFF"

def expression_names(face):
    """The character's expression list. `face.expression_list` (up to 6 names, the first is the
    resting face) or the standard four."""
    return list(face.get("expression_list") or EXPRESSIONS)

def expr_grid(n):
    """(cols, rows) of the face atlas for n expressions: 2x2 up to four, 3x2 up to six."""
    assert 1 <= n <= 6, "at most six expressions per face atlas"
    return (2, 2) if n <= 4 else (3, 2)

def expr_offsets(names):
    """Godot/glTF UV offset per expression (cell 0 is top-left; v grows downwards in glTF)."""
    cols, rows = expr_grid(len(names))
    return {n: ((i % cols) / cols, (i // cols) / rows) for i, n in enumerate(names)}

def expr_spec(face, name):
    spec = dict(lid=face["lid"], lid_low=face["lid_low"], lid_tilt=face["lid_tilt"],
                brow_tilt=face["brow_tilt"], brow_raise=face["brow_raise"], mouth=face["mouth"],
                eye_mode="open", eye_scale=1.0, blush_add=0.0)
    if name != "neutral":
        spec.update(EXPR_DEFAULTS.get(name, {}))
    spec.update(face.get("expressions", {}).get(name, {}))
    return spec

def draw_eye(cv, cx, cy, kind, spec, col):
    e = EYES[kind]
    s = spec["eye_scale"]
    rx, ry, rot = e["rx"] * s, e["ry"] * s, e.get("rot", 0.0) * (1 if cx > 0 else -1)
    side = 1 if cx > 0 else -1
    if spec["eye_mode"] == "shut":    # squeezed shut: a sideways chevron pointing at the nose
        pts = [(cx + side * rx * 1.1, cy + ry * 0.55), (cx - side * rx * 0.9, cy), (cx + side * rx * 1.1, cy - ry * 0.55)]
        sl, X, Y = cv.grid(cx - rx * 1.6, cy - ry * 1.2, cx + rx * 1.6, cy + ry * 1.2)
        cv.paint(sl, sd_stroke(X, Y, pts, 0.05, 0.05), col)
        return
    if spec["eye_mode"] == "arc":     # closed happy eye: an upward arch
        pts = bez((cx - rx * 1.15, cy - ry * 0.25), (cx, cy + ry * 1.25), (cx + rx * 1.15, cy - ry * 0.25))
        sl, X, Y = cv.grid(cx - rx * 1.5, cy - ry, cx + rx * 1.5, cy + ry * 1.2)
        cv.paint(sl, sd_stroke(X, Y, pts, 0.058, 0.058), col)
        return
    sl, X, Y = cv.grid(cx - rx * 1.4, cy - ry * 1.4, cx + rx * 1.4, cy + ry * 1.4)
    E = sd_ellipse(X, Y, cx, cy, rx, ry, rot)
    vis = E
    lid = spec["lid"]
    if lid > 0.01:
        slope = side * math.tan(spec["lid_tilt"])
        y0 = cy + ry - 2 * ry * lid
        d_lid = (Y - (y0 + (X - cx) * slope)) / math.sqrt(1 + slope * slope)
        vis = np.maximum(vis, d_lid)
    low = spec["lid_low"]
    if low > 0.01:   # cheek push from below: a big circle under the eye
        R = ry * 2.2
        d_low = sd_circle(X, Y, cx, cy - ry - R + 2 * ry * low, R)
        vis = np.maximum(vis, -d_low)
    cv.paint(sl, vis, col)
    # highlights sit near the top of what is visible, same side on both eyes (one light)
    top = cy + ry * (1 - 2 * lid) if lid > 0.01 else cy + ry
    vis_h = max(0.02, top - (cy - ry * (1 - 2 * low)))
    hr = rx * (0.36 if lid < 0.3 else 0.30)
    hx, hy = cx - rx * 0.28, top - min(vis_h * 0.38, ry * 0.62)
    cv.paint(sl, np.maximum(sd_circle(X, Y, hx, hy, hr), vis + 0.004), "#FFFFFF")
    cv.paint(sl, np.maximum(sd_circle(X, Y, cx + rx * 0.35, cy - ry * 0.35, rx * 0.15), vis + 0.004), "#FFFFFF", 0.9)
    if lid > 0.01:   # lash line along the lid so a half-lidded eye reads as a lid, not a cut-off
        lw = 0.028
        line = np.abs(d_lid) - lw * 0.5
        cv.paint(sl, np.maximum(line, E - 0.012), col)
    if e.get("lash"):
        ox = cx + side * rx * 0.85
        pts = [(ox, cy + ry * 0.45), (ox + side * rx * 0.45, cy + ry * 0.85)]
        cv.paint(sl, sd_stroke(X, Y, pts, 0.03, 0.012), col)

def draw_brow(cv, cx, cy, kind, spec, col):
    b = BROWS.get(kind)
    if not b:
        return
    w0, w1, hl, arch = b
    side = 1 if cx > 0 else -1
    t = spec["brow_tilt"] * side     # positive tilt: inner end lower (determined)
    inner = (cx - side * hl, cy)
    outer = (cx + side * hl, cy)
    ctrl = (cx, cy + arch * 2)
    def rotp(p):
        dx, dy = p[0] - cx, p[1] - cy
        c, s = math.cos(t), math.sin(t)
        return (cx + c * dx - s * dy, cy + s * dx + c * dy)
    pts = [rotp(p) for p in bez(inner, ctrl, outer)]
    sl, X, Y = cv.grid(cx - hl * 1.6, cy - hl, cx + hl * 1.6, cy + hl)
    cv.paint(sl, sd_stroke(X, Y, pts, w0, w1), col)

def draw_nose(cv, kind, skin):
    y = NOSE_Y
    if kind == "button":
        sl, X, Y = cv.grid(-0.12, y - 0.1, 0.12, y + 0.1)
        cv.paint(sl, sd_ellipse(X, Y, 0, y, 0.062, 0.046), shade(skin, 0.86), soft=0.01)
        cv.paint(sl, sd_ellipse(X, Y, -0.018, y + 0.014, 0.018, 0.012), mix_hex(skin, "#FFFFFF", 0.45), soft=0.008)
    elif kind == "dot":
        sl, X, Y = cv.grid(-0.08, y - 0.06, 0.08, y + 0.06)
        cv.paint(sl, sd_ellipse(X, Y, 0, y, 0.034, 0.026), shade(skin, 0.72))
    elif kind == "curve":
        sl, X, Y = cv.grid(-0.1, y - 0.1, 0.1, y + 0.1)
        pts = bez((0.012, y + 0.05), (0.06, y - 0.01), (-0.02, y - 0.035))
        cv.paint(sl, sd_stroke(X, Y, pts, 0.024, 0.024), shade(skin, 0.7))

def open_mouth(cv, w, y, h, teeth, line):
    sl, X, Y = cv.grid(-w - 0.05, y - h - 0.06, w + 0.05, y + 0.1)
    ytop = y + 0.03 + 0.05 * (X / w) ** 2
    M = np.maximum(sd_ellipse(X, Y, 0, y + 0.02, w, h), Y - ytop)
    cv.paint(sl, M, MOUTH_DARK)
    cv.paint(sl, np.maximum(sd_ellipse(X, Y, 0, y - h * 0.78, w * 0.58, h * 0.48), M), TONGUE)
    if teeth == "top":
        cv.paint(sl, np.maximum(M, ytop - 0.045 - Y), TEETH)
    elif teeth == "two":
        for tx in (-0.03, 0.03):
            cv.paint(sl, np.maximum(sd_rrect(X, Y, tx, y + 0.005, 0.027, 0.045, 0.012), M), TEETH)
    cv.paint(sl, np.abs(M) - 0.007, line)

def draw_mouth(cv, kind, line, wscale=1.0):
    y = MOUTH_Y; w = 0.17 * wscale
    sl, X, Y = cv.grid(-0.32, y - 0.25, 0.32, y + 0.15)
    if kind in MOUTH_DRAW:
        MOUTH_DRAW[kind](cv, line, y, w)
    elif kind == "smile":
        cv.paint(sl, sd_stroke(X, Y, bez((-w, y + 0.05), (0, y - 0.075), (w, y + 0.05)), 0.036), line)
    elif kind == "grin":
        open_mouth(cv, w * 1.05, y, 0.13, None, line)
    elif kind == "grin_top":
        open_mouth(cv, w * 1.1, y, 0.14, "top", line)
    elif kind == "grin_two":
        open_mouth(cv, w * 1.08, y, 0.135, "two", line)
    elif kind == "o":
        M = sd_ellipse(X, Y, 0, y - 0.02, 0.07, 0.088)
        cv.paint(sl, M, MOUTH_DARK)
        cv.paint(sl, np.maximum(sd_ellipse(X, Y, 0, y - 0.085, 0.05, 0.035), M), TONGUE)
        cv.paint(sl, np.abs(M) - 0.007, line)
    elif kind == "smirk":
        cv.paint(sl, sd_stroke(X, Y, bez((-w * 0.75, y + 0.0), (w * 0.1, y - 0.03), (w * 0.85, y + 0.07)), 0.038), line)
    elif kind == "set":
        cv.paint(sl, sd_stroke(X, Y, bez((-w * 0.7, y - 0.01), (0, y + 0.02), (w * 0.7, y - 0.01)), 0.038), line)
    elif kind == "flat":
        cv.paint(sl, sd_stroke(X, Y, [(-w * 0.6, y), (w * 0.6, y)], 0.036), line)
    elif kind == "frown":
        cv.paint(sl, sd_stroke(X, Y, bez((-w * 0.6, y - 0.04), (0, y + 0.045), (w * 0.6, y - 0.04)), 0.034), line)
    elif kind == "grit":
        M = sd_rrect(X, Y, 0, y, w * 0.95, 0.055, 0.05)
        cv.paint(sl, M, TEETH)
        cv.paint(sl, np.maximum(np.abs(Y - y) - 0.006, M), shade(line, 1.4))
        cv.paint(sl, np.abs(M) - 0.008, line)

def draw_face_cell(face, expr, skin):
    cell = FACE_CELL
    k = 0.5 * (1 - 2 * FACE_MARGIN) * float(face.get("scale", 1.3))
    cv = Canvas(cell, cell, (-0.5 / k, 0.5 / k, -0.5 / k, 0.5 / k), skin)
    spec = expr_spec(face, expr)
    fcol = face_colours(face, skin)
    extras = [(FACE_EXTRAS[e["type"]], e) for e in ([{"type": x} if isinstance(x, str) else x for x in face.get("extras", [])])]
    for (fn, layer), e in extras:
        if layer == "under":
            fn(cv, face, e, skin, spec)
    blush = min(1.0, face["blush"] + spec["blush_add"])
    if blush > 0.01:
        for sx in (-1, 1):
            sl, X, Y = cv.grid(sx * 0.56 - 0.25, -0.5, sx * 0.56 + 0.25, -0.05)
            cv.paint(sl, sd_ellipse(X, Y, sx * 0.56, -0.29, 0.12, 0.075), fcol["blush"], 0.5 * blush, soft=0.09)
    if face.get("freckles"):
        for sx in (-1, 1):
            for fx, fy in ((0.46, -0.22), (0.55, -0.19), (0.50, -0.29), (0.62, -0.27)):
                sl, X, Y = cv.grid(sx * fx - 0.03, fy - 0.03, sx * fx + 0.03, fy + 0.03)
                cv.paint(sl, sd_circle(X, Y, sx * fx, fy, 0.013), shade(skin, 0.72), 0.8)
    line = fcol["line"]
    ex = face["eye_spacing"]
    ey = float(face.get("eye_y", EYE_Y))   # lower eyes (and brows) for a face under a low hat brim
    for sx in (-1, 1):
        draw_eye(cv, sx * ex, ey, face["eyes"], spec, face["eye_color"])
        bry = ey + EYES[face["eyes"]]["ry"] * spec["eye_scale"] + 0.11 + spec["brow_raise"]
        if sx > 0:   # one brow up (baffled): the character's left brow
            bry += spec.get("brow_raise_left", 0.0)
        if not (face.get("brow_skip") == ("L" if sx > 0 else "R")):   # a face extra draws that brow (scorch mark)
            draw_brow(cv, sx * (ex + 0.01), bry, face["brows"], spec, fcol["brow"])
    draw_nose(cv, face["nose"], skin)
    draw_mouth(cv, spec["mouth"], line, float(face.get("mouth_width", 1.0)))
    for (fn, layer), e in extras:
        if layer != "under":
            fn(cv, face, e, skin, spec)
    return cv.img

FACE_CELL = 1024
FACE_MARGIN = 0.03

def face_atlas(face, skin, draw=None):
    """Atlas of the character's expressions, one square cell each (see expr_grid). `draw(face,
    name, skin)` returns one FACE_CELL x FACE_CELL x 3 float image; default is the humanoid face."""
    c = FACE_CELL
    names = expression_names(face)
    cols, rows = expr_grid(len(names))
    A = np.empty((rows * c, cols * c, 3), np.float32)
    for i in range(cols * rows):                      # unused cells repeat the resting face
        r, col = i // cols, i % cols
        A[r * c:(r + 1) * c, col * c:(col + 1) * c] = (draw or draw_face_cell)(face, names[min(i, len(names) - 1)] if i < len(names) else names[0], skin)
    return A

def np_to_image(name, arr):
    h, w = arr.shape[:2]
    img = bpy.data.images.new(name, w, h, alpha=False)
    rgba = np.ones((h, w, 4), np.float32)
    rgba[..., :3] = np.flipud(arr)
    img.pixels.foreach_set(rgba.ravel())
    img.pack()
    return img

# ------------------------------------------------------------------------------------- textures
def tiedye_texture(name, base, swirl, w=1024, h=512):
    u = (np.arange(w) + 0.5) / w; v = (np.arange(h) + 0.5) / h
    U, V = np.meshgrid(u, v[::-1])
    out = np.empty((h, w, 3), np.float32); out[:] = hex_rgb(base)
    red = np.zeros((h, w), np.float32); white = np.zeros((h, w), np.float32)
    for uc, vc, turn in ((0.5, 0.56, 1), (0.0, 0.56, -1)):
        du = ((U - uc + 0.5) % 1.0) - 0.5
        x = du * 0.95; y = (V - vc) * 0.42
        r = np.sqrt(x * x + y * y); a = np.arctan2(y, x)
        wob = 0.35 * np.sin(a * 5 + r * 9) + 0.25 * np.sin(U * 40 + V * 23)
        s = np.sin(3 * a * turn + r * 32 + wob)
        fall = np.clip(1.25 - r * 3.2, 0, 1)
        red = np.maximum(red, np.clip((s - 0.42) / 0.3, 0, 1) * fall)
        white = np.maximum(white, np.clip(1 - np.abs(s + 0.55) / 0.09, 0, 1) * fall * 0.75)
    red = np.clip(red, 0, 1)[..., None]; white = white[..., None]
    out = out * (1 - red) + np.array(hex_rgb(swirl), np.float32) * red
    out = out * (1 - white) + np.array((0.97, 0.95, 0.95), np.float32) * white
    return np_to_image(name, out)

def trex_patch_texture(name, bg, fg, w=640, h=480):
    cv = Canvas(w, h, (-1.0, 1.0, -0.75, 0.75), bg)
    sl, X, Y = cv.grid(-1, -0.75, 1, 0.75)
    body = sd_ellipse(X, Y, -0.08, -0.02, 0.36, 0.25, 0.38)
    head = sd_ellipse(X, Y, 0.34, 0.33, 0.25, 0.155, -0.08)
    jaw = sd_ellipse(X, Y, 0.37, 0.215, 0.20, 0.08, -0.05)
    neck = sd_stroke(X, Y, [(0.12, 0.12), (0.28, 0.27)], 0.2)
    tail = sd_stroke(X, Y, bez((-0.32, 0.0), (-0.68, 0.08), (-0.9, -0.3)), 0.25, 0.04)
    leg1 = sd_stroke(X, Y, [(-0.02, -0.12), (0.02, -0.45)], 0.15, 0.11)
    leg2 = sd_stroke(X, Y, [(-0.24, -0.12), (-0.26, -0.45)], 0.15, 0.11)
    foot1 = sd_ellipse(X, Y, 0.07, -0.5, 0.1, 0.045)
    foot2 = sd_ellipse(X, Y, -0.21, -0.5, 0.1, 0.045)
    arm = sd_stroke(X, Y, [(0.2, 0.04), (0.31, -0.03), (0.33, -0.08)], 0.05, 0.035)
    d = smin(body, head, 0.05)
    for p in (jaw, neck, tail, leg1, leg2, foot1, foot2):
        d = smin(d, p, 0.04)
    d = np.minimum(d, arm)
    for sx in (-0.05, 0.11, 0.27):   # little back plates
        d = np.minimum(d, sd_circle(X, Y, -0.26 + sx, 0.21 + sx * 0.35, 0.05))
    cv.paint(sl, d, fg)
    cv.paint(sl, sd_circle(X, Y, 0.43, 0.38, 0.036), bg)                      # eye
    cv.paint(sl, sd_stroke(X, Y, bez((0.30, 0.25), (0.42, 0.21), (0.55, 0.26)), 0.025), bg)  # grin
    border = np.abs(sd_rrect(X, Y, 0, 0, 0.94, 0.69, 0.18)) - 0.025
    cv.paint(sl, border, fg)
    return np_to_image(name, cv.img)

# ------------------------------------------------------------------------------------ materials
class Mats:
    def __init__(self, prefix):
        self.prefix = prefix; self.cache = {}

    def flat(self, key, hexcol, rough=0.6, spec=0.35):
        name = f"{self.prefix}{key}"
        if name in self.cache:
            return self.cache[name]
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        p = m.node_tree.nodes.get("Principled BSDF")
        p.inputs["Base Color"].default_value = (*srgb_to_lin(hex_rgb(hexcol)), 1.0)
        p.inputs["Roughness"].default_value = rough
        p.inputs["Specular IOR Level"].default_value = spec
        m.diffuse_color = (*srgb_to_lin(hex_rgb(hexcol)), 1.0)
        self.cache[name] = m
        return m

    def glass(self, key, hexcol, alpha=0.22, rough=0.08):
        """See-through material (fishbowl helmet, lenses): exports as glTF alpha blend."""
        m = self.flat(key, hexcol, rough=rough, spec=0.6)
        m.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value = alpha
        m.diffuse_color = (*srgb_to_lin(hex_rgb(hexcol)), alpha)
        if hasattr(m, "surface_render_method"):
            m.surface_render_method = "BLENDED"
        return m

    def emit(self, key, hexcol, strength=4.0):
        """Glowing material (lamp lenses, lights)."""
        m = self.flat(key, hexcol, rough=0.5, spec=0.2)
        p = m.node_tree.nodes.get("Principled BSDF")
        p.inputs["Emission Color"].default_value = (*srgb_to_lin(hex_rgb(hexcol)), 1.0)
        p.inputs["Emission Strength"].default_value = strength
        return m

    def tex(self, key, image, rough=0.6, spec=0.3):
        name = f"{self.prefix}{key}"
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        p = nt.nodes.get("Principled BSDF")
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = image; t.interpolation = "Linear"
        nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
        p.inputs["Roughness"].default_value = rough
        p.inputs["Specular IOR Level"].default_value = spec
        self.cache[name] = m
        return m

# ------------------------------------------------------------------------------------- geometry
def superxy(a, p):
    c, s = math.cos(a), math.sin(a)
    e = 2.0 / p
    return math.copysign(abs(c) ** e, c), math.copysign(abs(s) ** e, s)

def lathe(rings, segs=32, power=2.0):
    """rings: list of (z, rx, ry, cx, cy) bottom->top. r<=1e-5 makes a pole."""
    bm = bmesh.new()
    dirs = [superxy(2 * math.pi * j / segs, power) for j in range(segs)]
    layers = []
    for z, rx, ry, cx, cy in rings:
        if rx <= 1e-5:
            layers.append(bm.verts.new((cx, cy, z)))
        else:
            layers.append([bm.verts.new((cx + rx * dx, cy + ry * dy, z)) for dx, dy in dirs])
    for A, B in zip(layers, layers[1:]):
        if isinstance(A, list) and isinstance(B, list):
            for j in range(segs):
                bm.faces.new((A[j], A[(j + 1) % segs], B[(j + 1) % segs], B[j]))
        elif isinstance(B, list):
            for j in range(segs):
                bm.faces.new((A, B[(j + 1) % segs], B[j]))
        elif isinstance(A, list):
            for j in range(segs):
                bm.faces.new((A[j], A[(j + 1) % segs], B))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

def envelope(t, n):
    return max(0.0, 1 - abs(2 * t - 1) ** n) ** (1.0 / n)

def smooth_interp(t, pts):
    """Cosine interpolation through (t, value) control points."""
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t <= t1:
            u = (t - t0) / max(1e-9, t1 - t0)
            u = (1 - math.cos(math.pi * u)) / 2
            return v0 + (v1 - v0) * u
    return pts[-1][1]

def blob(z0, z1, widths, depth=0.82, n_end=2.4, power=2.0, chest=None, segs=40, nrings=28):
    rings = []
    for i in range(nrings + 1):
        s = i / nrings
        t = (1 - math.cos(math.pi * s)) / 2
        e = envelope(t, n_end)
        w = smooth_interp(t, widths)
        cy = -(chest(t) if callable(chest) else smooth_interp(t, chest)) if chest else 0.0
        rings.append((z0 + (z1 - z0) * t, w * e, w * e * depth, 0.0, cy))
    return lathe(rings, segs, power)

def capsule_bm(p0, p1, r0, r1, segs=24, hem=6, sx=1.0, sy=1.0, power=2.0):
    p0, p1 = Vector(p0), Vector(p1)
    L = (p1 - p0).length
    rings = [(-r0, 0, 0, 0, 0)]
    for k in range(1, hem + 1):
        a = -math.pi / 2 + (math.pi / 2) * k / hem
        rings.append((r0 * math.sin(a), r0 * math.cos(a) * sx, r0 * math.cos(a) * sy, 0, 0))
    for k in range(0, hem):
        a = (math.pi / 2) * k / hem
        rings.append((L + r1 * math.sin(a), r1 * math.cos(a) * sx, r1 * math.cos(a) * sy, 0, 0))
    rings.append((L + r1, 0, 0, 0, 0))
    bm = lathe(rings, segs, power)
    q = Vector((0, 0, 1)).rotation_difference((p1 - p0).normalized())
    bmesh.ops.transform(bm, matrix=Matrix.Translation(p0) @ q.to_matrix().to_4x4(), verts=bm.verts)
    return bm

def ellipsoid_bm(center, radii, rot=None, segs=32, rings=16, floor=None, deform=None):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0)
    for v in bm.verts:
        co = Vector((v.co.x * radii[0], v.co.y * radii[1], v.co.z * radii[2]))
        if deform:
            co = deform(co)
        if rot is not None:
            co = rot @ co
        co = co + Vector(center)
        if floor is not None and co.z < floor:
            co.z = floor
        v.co = co
    return bm

def tube_bm(points, radius, cyclic=False, res=6, radii=None):
    cu = bpy.data.curves.new("tube_tmp", "CURVE")
    cu.dimensions = "3D"; cu.bevel_depth = radius; cu.bevel_resolution = 3
    cu.use_fill_caps = True; cu.resolution_u = res
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for k, (p, c) in enumerate(zip(sp.points, points)):
        p.co = (c[0], c[1], c[2], 1.0)
        if radii:
            p.radius = radii[k]
    sp.use_cyclic_u = cyclic
    ob = bpy.data.objects.new("tube_tmp", cu)
    bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bpy.data.objects.remove(ob); bpy.data.curves.remove(cu)
    bm = bmesh.new(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    return bm

def solidify_bm(bm, thickness):
    me = bpy.data.meshes.new("sol_tmp"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("sol_tmp", me)
    bpy.context.scene.collection.objects.link(ob)
    mod = ob.modifiers.new("s", "SOLIDIFY"); mod.thickness = thickness; mod.offset = -1.0
    mod.use_even_offset = True
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bpy.data.objects.remove(ob); bpy.data.meshes.remove(me)
    out = bmesh.new(); out.from_mesh(me2); bpy.data.meshes.remove(me2)
    return out

def grid_bm(fn, nu, nv, closed_u=False):
    """fn(u, v) -> point, u,v in 0..1. Returns an open quad grid."""
    bm = bmesh.new()
    cols = nu if closed_u else nu + 1
    V = [[bm.verts.new(fn(i / nu, j / nv)) for i in range(cols)] for j in range(nv + 1)]
    for j in range(nv):
        for i in range(nu):
            i2 = (i + 1) % cols if closed_u else i + 1
            bm.faces.new((V[j][i], V[j][i2], V[j + 1][i2], V[j + 1][i]))
    return bm

def cap_shell_bm(center, radii, thr_fn, scale_fn, n_phi=72, n_t=22, taper=None):
    """Spherical cap from the top down to elevation thr_fn(phi). phi=0 is the front (-Y)."""
    cx, cy, cz = center
    def pt(el, phi, t=0.0):
        s = scale_fn(el, phi)
        if taper is not None:   # hair hugs the scalp at the hairline instead of ending in a helmet rim
            s = 1.0 + (s - 1.0) * min(1.0, taper + (1 - t) * 2.2)
        return (cx + radii[0] * s * math.sin(phi) * math.cos(el),
                cy - radii[1] * s * math.cos(phi) * math.cos(el),
                cz + radii[2] * s * math.sin(el))
    bm = bmesh.new()
    top = bm.verts.new(pt(math.pi / 2, 0))
    rings = []
    for i in range(1, n_t + 1):
        t = i / n_t
        ring = []
        for j in range(n_phi):
            phi = 2 * math.pi * j / n_phi
            el = math.pi / 2 - t * (math.pi / 2 - thr_fn(phi))
            ring.append(bm.verts.new(pt(el, phi, t)))
        rings.append(ring)
    for j in range(n_phi):
        bm.faces.new((top, rings[0][j], rings[0][(j + 1) % n_phi]))
    for A, B in zip(rings, rings[1:]):
        for j in range(n_phi):
            bm.faces.new((A[j], B[j], B[(j + 1) % n_phi], A[(j + 1) % n_phi]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

# ----------------------------------------------------------------------------------- the builder
BUILDS = {   # torso width, limb thickness, torso depth, end roundness, cross-section power, belly
    "slim":    dict(w=0.86, limb=0.88, depth=0.82, n=2.3, power=2.0, belly=0.0),
    "regular": dict(w=1.00, limb=1.00, depth=0.82, n=2.4, power=2.0, belly=0.0),
    "stocky":  dict(w=1.16, limb=1.16, depth=0.86, n=2.6, power=2.2, belly=0.01),
    "round":   dict(w=1.10, limb=1.04, depth=0.95, n=2.2, power=2.0, belly=0.045),
    "boxy":    dict(w=1.08, limb=1.10, depth=0.80, n=3.2, power=3.0, belly=0.0),
    "puffy":   dict(w=1.16, limb=1.08, depth=0.92, n=2.2, power=2.0, belly=0.03),
}
HEAD_SHAPES = {   # sx, sy, sz, jaw (positive widens the bottom)
    "round": (1.0, 1.0, 1.0, 0.0), "wide": (1.08, 1.0, 0.94, 0.04), "tall": (0.94, 0.97, 1.06, -0.04),
    "soft_square": (1.02, 1.0, 0.98, 0.10), "pear": (1.0, 1.0, 1.0, 0.16), "egg": (0.97, 0.98, 1.04, -0.10),
}

# Equipment (docs/equipment.md). Slot name -> what it is for; markers are `slot_<name>` empties.
SLOTS = ["head", "face", "back", "hand_l", "hand_r", "waist", "knee_l", "knee_r", "foot_l", "foot_r"]
# Separable body parts: own mesh `<id>_part_<name>`, hidden by gear that `replaces_body_part` them.
# (Chuck's separate hat also counts as `headwear`.)
BODY_PARTS = ["foot_l", "foot_r", "hand_l", "hand_r", "headwear", "tail"]
# The reference Jarling (regular build, round head, size 1, short hair): slot scale 1.0 means this.
SLOT_REF = dict(head_crown=0.27, face_r=0.235, back_tw=0.152, waist_rx=0.155, waist_ry=0.127, knee_r=0.049)

# Registries filled by the plug-in modules next to this file (loaded at the bottom):
#   pieces_*.py  kit pieces for the standard body;  body_*.py  non-standard body types.
HEADWEAR = {}     # headwear type -> fn(builder, headwear_dict)   (builder.cur_part is "headwear")
COSTUME = {}      # costume piece -> fn(builder, piece_dict)
ACTIONS = {}      # extra action  -> (fn(builder) -> [(frame, pose), ...], loops: bool); listed in params "actions"
BODY_TYPES = {}   # body.type     -> class with the Builder interface (see avatar/README.md "Body types")
# Kit v2 registries (docs/kit-v2.md):
HEADWEAR_OPTS = {}  # headwear type -> {"hair": "tuck" (default: hair clamped under the hat) | "free" | "hide"}
SHOES = {}        # shoes.style   -> fn(builder, s, side, ank, shoes): one foot (s +1 = the character's left)
PATTERNS = {}     # pattern name  -> fn(img, U, V, spec, part): paints a top / bottoms texture in place
FACE_EXTRAS = {}  # face extra    -> (fn(canvas, face, extra, skin, spec), "under" | "over")
MOUTH_DRAW = {}   # mouth name    -> fn(canvas, line_colour, y, w)
FEATURES = {}     # head feature  -> fn(builder, feature_dict)   (builder.cur_part is "feature_<type>")
HAIR_PIECES = {}  # hair piece    -> fn(builder, piece_dict, material)
HAIR_PRESETS = {} # hair.style    -> {"base": <cap style>, "pieces": [...]}   data-only styles

WIDTH_RANGE = (0.75, 1.5)   # body.width
BELLY_RANGE = (0.0, 1.0)    # body.belly

class Builder:
    def __init__(self, params, prefix=""):
        self.P = deep_merge(DEFAULTS, params)
        self.prefix = prefix or ""
        self.mats = Mats(f"{self.prefix}{self.P['id']}_")
        self.parts = []          # (bm, material, bone)
        self.part_tags = []      # parallel to parts: None (main body) or a separable body part, see BODY_PARTS
        self.cur_part = None
        self.extra_bones = []
        self.bob_bones = []      # (bone, amount, side sign): follow the comb's secondary bob in every action
        self.lamps = []          # real lights on the head bone: dict(name, pos, dir, color, watts, spot_deg)
        self.P["face"]["_brow_auto"] = "brow_color" not in (params or {}).get("face", {})
        self.coll = bpy.context.scene.collection

    def add_bob_bone(self, name, head, tail, amount=1.0, side=1.0, parent="head"):
        """A floppy bone under the head that gets the comb's soft secondary bob (scaled by
        `amount`; `side` -1 mirrors the sideways sway). Skin pieces to it with add(bm, mat, name)."""
        self.extra_bones.append((name, Vector(head), Vector(tail)))
        if amount:
            self.bob_bones.append((name, float(amount), float(side)))
        return name

    def pattern_image(self, key, d, part, w=1024, h=512):
        """Texture for `top` / `bottoms` with `pattern`: a name, a layer dict or a list of layers."""
        u = (np.arange(w) + 0.5) / w; v = (np.arange(h) + 0.5) / h
        U, V = np.meshgrid(u.astype(np.float32), v[::-1].astype(np.float32))
        img = np.empty((h, w, 3), np.float32); img[:] = hex_rgb(d["color"])
        layers = d["pattern"] if isinstance(d["pattern"], list) else [d["pattern"]]
        for layer in layers:
            layer = {"type": layer} if isinstance(layer, str) else dict(layer)
            for k in ("color", "accent", "accent2"):
                if k not in layer and k in d:
                    layer[k] = d[k]
            layer.setdefault("accent", "#FFFFFF")
            if layer["type"] not in PATTERNS:
                raise ValueError(f"unknown pattern {layer['type']!r}; known: {', '.join(sorted(PATTERNS))}")
            PATTERNS[layer["type"]](img, U, V, layer, part)
        return np_to_image(f"{self.mats.prefix}{key}", np.clip(img, 0, 1))

    def chest_at(self, t):
        """How far the torso centre line is pushed forward (-Y) at height fraction t (chest / belly)."""
        return self.torso_chest(t) if getattr(self, "torso_chest", None) else 0.0

    def torso_point(self, t, th, grow=1.0):
        """Point on the torso surface at height fraction t (0 bottom, 1 top) and lathe angle th
        (-pi/2 = front, 0 = the character's left, pi/2 = back). Follows build, width and belly."""
        L = self.L; b = L["b"]
        t = min(1.0, max(0.0, t))
        w = smooth_interp(t, self.torso_widths) * envelope(t, b["n"]) * grow
        dx, dy = superxy(th, b["power"])
        return Vector((w * dx, -self.chest_at(t) + w * b["depth"] * dy, L["torso_z0"] + (L["torso_z1"] - L["torso_z0"]) * t))

    def add(self, bm, mat, bone, uv_fn=None):
        uv = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
        if uv_fn:
            uv_fn(bm, uv)
        self.parts.append((bm, mat, bone))
        self.part_tags.append(self.cur_part)

    # --- layout
    def layout(self):
        P = self.P
        b = dict(BUILDS[P["body"]["build"]])
        width = float(P["body"].get("width", 1.0))
        belly = P["body"].get("belly")
        if not WIDTH_RANGE[0] - 1e-9 <= width <= WIDTH_RANGE[1] + 1e-9:
            raise ValueError(f"body.width {width} is outside {WIDTH_RANGE}")
        if belly is not None and not BELLY_RANGE[0] - 1e-9 <= float(belly) <= BELLY_RANGE[1] + 1e-9:
            raise ValueError(f"body.belly {belly} is outside {BELLY_RANGE}")
        self.belly01 = float(belly or 0.0)
        self.reshaped = width != 1.0 or self.belly01 > 0.0
        hip_floor = 1.0
        if width != 1.0:      # fat / skinny on the same skeleton: torso and limbs scale, bones do not move
            b["w"] *= width
            b["limb"] *= 1 + 0.45 * (width - 1)
            hip_floor = min(1.0, 1 - 0.9 * (1 - width))
        if self.belly01 > 0.0:
            b["belly"] += 0.075 * self.belly01
        h = float(P["body"].get("height", 1.0))
        R = 0.235 * float(P["head"].get("size", 1.0))
        sx, sy, sz, jaw = HEAD_SHAPES[P["head"]["shape"]]
        L = dict(h=h, b=b, R=R, hsx=sx, hsy=sy, hsz=sz, jaw=jaw)
        L["ankle_z"] = 0.075
        L["hip_z"] = 0.075 + 0.235 * h
        L["torso_z0"] = L["hip_z"] - 0.085
        L["torso_z1"] = L["hip_z"] + 0.33 * h
        L["shoulder_z"] = L["torso_z1"] - 0.075
        L["head_c"] = Vector((0, 0, L["torso_z1"] + 0.015 + R * 0.93 * sz))
        L["tw"] = 0.152 * b["w"]
        L["hip_x"] = 0.072 * max(hip_floor, b["w"] * 0.95)
        L["ank_x"] = L["hip_x"] * 1.05 + float(P.get("posture", {}).get("stance", 0.0))   # stance: feet wider apart
        L["limb"] = b["limb"]
        self.L = L
        return L

    # --- head + face
    def build_head(self):
        P, L = self.P, self.L
        R, c = L["R"], L["head_c"]
        face = P["face"]
        img = np_to_image(f"{self.mats.prefix}face", face_atlas(face, P["skin"]))
        self.face_mat = self.mats.tex("face", img, rough=0.55, spec=0.3)
        self.face_mat["jarling_face_atlas"] = True
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=40, radius=1.0)
        uv = bm.loops.layers.uv.new("UVMap")
        k = 0.5 * (1 - 2 * FACE_MARGIN)
        self.expr_names = expression_names(face)
        self.expr_uv = expr_offsets(self.expr_names)
        cols, rows = expr_grid(len(self.expr_names))
        cu, cv_ = 1.0 / cols, 1.0 / rows
        for f in bm.faces:
            fc = f.calc_center_median()
            front = -fc.y > 0.22
            for lp in f.loops:
                u0 = lp.vert.co
                if front:
                    lp[uv].uv = (cu * (0.5 + u0.x * k), 1 - cv_ + cv_ * (0.5 + u0.z * k))
                else:
                    lp[uv].uv = (cu * (0.5 + 0.97 * k), 1 - cv_ + cv_ * (0.5 + 0.97 * k))
        for v in bm.verts:
            x, y, z = v.co
            jw = 1 + L["jaw"] * (-z) * 0.5
            v.co = Vector((x * R * L["hsx"] * jw, y * R * L["hsy"] * (1 + L["jaw"] * (-z) * 0.25),
                           z * R * L["hsz"])) + c
        self.add(bm, self.face_mat, "head")
        skin = self.mats.flat("skin", P["skin"], rough=0.55, spec=0.3)
        self.skin = skin
        if P["head"].get("ears", "round") != "none" and not any(f.get("type") == "pointy_ears" for f in P["head"].get("features", [])):
            for s in (-1, 1):
                e = ellipsoid_bm(c + Vector((s * R * L["hsx"] * 0.97, 0.01, -0.06 * R)),
                                 (0.10 * R, 0.13 * R, 0.17 * R), segs=20, rings=12)
                self.add(e, skin, "head")
        if face["nose"] == "bump":
            nz = NOSE_Y * float(face.get("scale", 1.3))
            ns = float(face.get("nose_size", 1.0))   # >1: a big round nose, pushed out so it sits on the face
            n = ellipsoid_bm(c + Vector((0, -R * L["hsy"] * math.sqrt(1 - nz * nz) * 0.99 - 0.05 * R * (ns - 1), nz * R * L["hsz"])),
                             (0.1 * R * ns, 0.08 * R * ns, 0.085 * R * ns), segs=20 if ns <= 1 else 28, rings=12 if ns <= 1 else 16)
            nmat = self.mats.flat("nose", face["nose_color"], rough=0.5, spec=0.3) if face.get("nose_color") else skin
            self.add(n, nmat, "head")
        # neck
        self.add(capsule_bm((0, 0, L["torso_z1"] - 0.05), (0, 0, c.z - R * 0.6), 0.045, 0.045, segs=16, hem=3),
                 skin, "head")

    def head_point(self, el, phi, s=1.0):
        L = self.L; R = L["R"]; c = L["head_c"]
        return c + Vector((R * L["hsx"] * s * math.sin(phi) * math.cos(el),
                           -R * L["hsy"] * s * math.cos(phi) * math.cos(el),
                           R * L["hsz"] * s * math.sin(el)))

    # --- hair
    def build_hair(self):
        """Hair = a scalp cap (`hair.style`) plus data-driven pieces (`hair.pieces`, or the pieces
        of a HAIR_PRESETS style). Under headwear: "tuck" clamps the cap and drops the pieces (a
        piece with `"keep": true` stays), "free" leaves everything, "hide" builds no hair."""
        P = self.P
        hair = P["hair"]; style = hair["style"]
        pieces = list(hair.get("pieces", []))
        if style in HAIR_PRESETS:
            pieces = copy.deepcopy(HAIR_PRESETS[style]["pieces"]) + pieces
            style = HAIR_PRESETS[style]["base"]
        hw_t = P["headwear"]["type"]
        mode = P["headwear"].get("hair") or HEADWEAR_OPTS.get(hw_t, {}).get("hair", "tuck")
        if hw_t == "chicken_hood" or mode == "hide":
            return
        self._hair_cap(style, mode == "tuck")
        n0 = len(self.parts)
        for pc in pieces:
            if hw_t != "none" and mode == "tuck" and not pc.get("keep"):
                continue
            if pc["type"] not in HAIR_PIECES:
                raise ValueError(f"unknown hair piece {pc['type']!r}; known: {', '.join(sorted(HAIR_PIECES))}")
            col = pc.get("color") or hair.get("color", "#5A3A28")
            mat = self.mats.flat("hair" if col == hair.get("color") else f"hair_{col.lstrip('#')}", col, rough=0.5, spec=0.4)
            HAIR_PIECES[pc["type"]](self, pc, mat)
        self.crown_skip = set(range(n0, len(self.parts)))   # hat fit follows the scalp, not buns and spikes

    def build_features(self):
        """`head.features`: antennae, horns, pointy ears, fins... Body features of the species, not
        hats: each is its own part `<id>_part_feature_<type>` on its own bone(s) under `head`."""
        for f in self.P["head"].get("features", []):
            f = {"type": f} if isinstance(f, str) else f
            if f["type"] not in FEATURES:
                raise ValueError(f"unknown head feature {f['type']!r}; known: {', '.join(sorted(FEATURES))}")
            self.cur_part = f"feature_{f['type']}"
            FEATURES[f["type"]](self, f)
            self.cur_part = None

    def _hair_cap(self, style, tuck):
        P, L = self.P, self.L
        if style in ("none", "bald"):
            return
        col = P["hair"]["color"]
        mat = self.mats.flat("hair", col, rough=0.5, spec=0.4)
        R, c = L["R"], L["head_c"]
        radii = (R * L["hsx"], R * L["hsy"] * 1.0, R * L["hsz"])
        def blend(front, back, p=1.6, side=None):
            def f(phi):
                fr = ((1 + math.cos(phi)) / 2) ** p
                v = back + (front - back) * fr
                if side is not None:   # sideburns: dip in front of the ears
                    v -= side * math.exp(-((abs(phi) if phi <= math.pi else 2 * math.pi - phi) - 1.25) ** 2 / 0.06)
                return v
            return f
        def tufts(base, n, depth, width=1.0):
            def f(phi):
                fr = ((1 + math.cos(phi)) / 2) ** 6
                return base(phi) - depth * fr * max(0.0, math.cos(phi * n)) ** 4 * width
            return f
        th = 0.035
        hairstyle = style
        if P["headwear"]["type"] in ("cap", "beanie", "trucker") and style in ("spiky", "afro", "curly", "bun", "bob", "swoop"):
            hairstyle = "short"
        style = hairstyle
        if style == "buzz":
            thr, sc, th = blend(0.52, -0.5, side=0.25), (lambda el, phi: 1.03), 0.02
        elif style == "short":
            thr = tufts(blend(0.52, -0.5, side=0.3), 7, 0.13)
            sc = lambda el, phi: 1.07 + 0.08 * max(0, math.sin(el)) ** 3
        elif style == "swoop":
            base = blend(0.52, -0.5, side=0.3)
            thr = lambda phi: base(phi) - 0.2 * max(0, math.sin(phi)) * ((1 + math.cos(phi)) / 2) ** 2
            sc = lambda el, phi: 1.08 + 0.12 * max(0, math.sin(el)) ** 2 * (1 + 0.3 * math.sin(phi))
        elif style == "bob":
            base = blend(0.40, -0.85, 1.0)
            thr = lambda phi: base(phi) + 0.03 * math.cos(phi * 14) * ((1 + math.cos(phi)) / 2) ** 4
            sc = lambda el, phi: 1.09 + 0.12 * max(0, math.cos(el)) * ((1 - math.cos(phi)) / 2 + 0.4)
        elif style in ("bun", "ponytail", "long", "sleek"):
            thr = tufts(blend(0.50, -0.55, side=0.35), 5, 0.08)
            sc = lambda el, phi: 1.06 + 0.06 * max(0, math.sin(el)) ** 2
        elif style == "spiky":
            thr, sc = tufts(blend(0.52, -0.45, side=0.25), 9, 0.10), (lambda el, phi: 1.06)
        elif style == "curly":
            thr = tufts(blend(0.46, -0.5, side=0.2), 8, 0.08)
            sc = lambda el, phi: 1.15 + 0.06 * math.sin(phi * 9) * math.sin(el * 7) + 0.1 * max(0, math.sin(el))
        elif style == "mane":   # a huge wild mass framing the face, down past the jaw at the sides
            def thr(phi):
                a = abs(phi) if phi <= math.pi else 2 * math.pi - phi
                return 0.46 - 1.75 * (1 / (1 + math.exp(-(a - 1.12) * 9)))
            sc = lambda el, phi: (1.30 + 0.07 * math.sin(phi * 13) * math.cos(el * 7) + 0.05 * math.sin(phi * 5 + el * 3)
                                  + 0.04 * max(0, math.sin(el)) ** 1.5 + 0.14 * max(0.0, -math.cos(phi)) * max(0.0, math.cos(el))
                                  + 0.30 * abs(math.sin(phi)) * max(0.0, math.cos(el)) ** 2)
        elif style == "afro":
            thr = blend(0.42, -0.3, side=0.15)
            sc = lambda el, phi: 1.22 + 0.04 * math.sin(phi * 11) * math.cos(el * 9) + 0.26 * max(0, math.sin(el)) ** 1.5
        else:
            raise ValueError(f"unknown hair style {style}")
        if P["headwear"]["type"] != "none" and style != "mane" and tuck:   # keep hair inside hats (a mane wears its hat on top)
            sc0 = sc
            sc = lambda el, phi: min(sc0(el, phi), 1.05)
        taper = None if style in ("afro",) else (0.0 if style == "mane" else 0.12)
        bm = solidify_bm(cap_shell_bm(c, radii, thr, sc, taper=taper), th * R)
        self.add(bm, mat, "head")
        if style == "bun":
            self.add(ellipsoid_bm(self.head_point(1.05, math.pi, 1.12), (0.42 * R, 0.4 * R, 0.4 * R), segs=24, rings=14), mat, "head")
        if style == "ponytail":
            p0 = self.head_point(0.55, math.pi, 1.05); p1 = p0 + Vector((0, 0.16 * R, -0.85 * R))
            self.add(capsule_bm(p0, p1, 0.24 * R, 0.17 * R, segs=18), mat, "head")
        if style == "long":
            p0 = self.head_point(0.2, math.pi, 0.92); p1 = p0 + Vector((0, 0.08 * R, -0.95 * R))
            self.add(capsule_bm(p0, p1, 0.62 * R, 0.5 * R, segs=24, sx=1.25, sy=0.65), mat, "head")
        if style == "spiky":
            for el, phi, ln in ((1.35, 0, 0.5), (1.0, 0.3, 0.45), (1.0, -0.3, 0.45), (0.9, 1.2, 0.4),
                                (0.9, -1.2, 0.4), (0.95, 2.4, 0.42), (0.95, -2.4, 0.42), (1.0, math.pi, 0.45),
                                (0.75, 0.55, 0.32), (0.75, -0.55, 0.32)):
                base = self.head_point(el, phi, 1.0)
                n = (base - c).normalized()
                tip = base + n * ln * R + Vector((0, 0.1 * R, 0))
                self.add(capsule_bm(base, tip, 0.2 * R, 0.035 * R, segs=14, hem=4), mat, "head")

    # --- torso, arms, legs, feet
    def build_body(self):
        P, L = self.P, self.L
        b = L["b"]; tw = L["tw"]; limb = L["limb"]
        top = P["outfit"]["top"]; bot = P["outfit"]["bottoms"]; shoes = P["outfit"]["shoes"]
        z0, z1 = L["torso_z0"], L["torso_z1"]
        widths = [(0.0, tw * 1.08), (0.3, tw * (1.08 + b["belly"] * 3)), (0.62, tw * 0.98), (0.9, tw * 1.0), (1.0, tw)]
        if self.belly01 > 0.0:   # a belly is a soft ball, not a ridge: the bulge carries up towards the chest
            k = self.belly01
            widths = [(0.0, tw * 1.08), (0.34, tw * (1.08 + b["belly"] * 3)), (0.62, tw * (0.98 + 0.20 * k)), (0.9, tw * (1.0 + 0.04 * k)), (1.0, tw)]
        chest = None
        if b["power"] > 2.5:   # boxy: chest out
            chest = [(0.0, 0.0), (0.45, 0.0), (0.78, 0.022), (1.0, 0.01)]
        self.torso_chest = (lambda t, _c=chest: smooth_interp(t, _c)) if chest else None
        if self.belly01 > 0.0:   # belly: the middle of the torso is pushed forward as well as out
            fwd = 0.17 * tw * self.belly01
            bump = [(0.0, 0.0), (0.12, 0.45 * fwd), (0.38, fwd), (0.62, 0.55 * fwd), (0.86, 0.0), (1.0, 0.0)]
            self.torso_chest = (lambda t, _c=chest, _b=bump: (smooth_interp(t, _c) if _c else 0.0) + smooth_interp(t, _b))
            chest = self.torso_chest
        torso_bm = blob(z0, z1, widths, depth=b["depth"], n_end=b["n"], power=b["power"], chest=chest)
        def cyl_uv(bm, uv):
            for f in bm.faces:
                us = []
                for lp in f.loops:
                    co = lp.vert.co
                    us.append(0.5 + math.atan2(co.x, -co.y) / (2 * math.pi))
                if max(us) - min(us) > 0.5:
                    us = [u + 1 if u < 0.5 else u for u in us]
                for lp, u in zip(f.loops, us):
                    lp[uv].uv = (u, (lp.vert.co.z - z0) / (z1 - z0))
        if top.get("pattern") and top["style"] not in ("tiedye", "bare"):
            tmat = self.mats.tex("shirt", self.pattern_image("shirt_pattern", top, "top"), rough=0.75, spec=0.25)
            sleeve_mat = self.mats.flat("shirt_sleeve", top.get("sleeve", top["color"]), rough=0.75, spec=0.25)
            self.add(torso_bm, tmat, "spine", cyl_uv)
        elif top["style"] == "tiedye":
            img = tiedye_texture(f"{self.mats.prefix}tiedye", top["color"], top.get("accent", PLAYER_RED))
            tmat = self.mats.tex("shirt", img, rough=0.8, spec=0.2)
            sleeve_mat = self.mats.flat("shirt_sleeve", top["color"], rough=0.8, spec=0.2)
            def cyl_uv(bm, uv):
                for f in bm.faces:
                    us = []
                    for lp in f.loops:
                        co = lp.vert.co
                        us.append(0.5 + math.atan2(co.x, -co.y) / (2 * math.pi))
                    if max(us) - min(us) > 0.5:
                        us = [u + 1 if u < 0.5 else u for u in us]
                    for lp, u in zip(f.loops, us):
                        lp[uv].uv = (u, (lp.vert.co.z - z0) / (z1 - z0))
            self.add(torso_bm, tmat, "spine", cyl_uv)
        else:
            tmat = self.skin if top["style"] == "bare" else self.mats.flat("shirt", top["color"], rough=0.75, spec=0.25)
            sleeve_mat = tmat
            self.add(torso_bm, tmat, "spine", cyl_uv if bot.get("pattern") else None)
            if top["style"] == "stripe":
                acc = self.mats.flat("shirt_accent", top.get("accent", "#FFFFFF"), rough=0.75, spec=0.25)
                rings = []
                for t in np.linspace(0.50, 0.66, 5):
                    w = smooth_interp(t, widths) * envelope(t, b["n"]) * 1.012 + 0.002
                    rings.append((z0 + (z1 - z0) * t, w, w * b["depth"], 0, -self.chest_at(t) if self.belly01 > 0.0 else 0))
                self.add(lathe(rings, 40, b["power"]), acc, "spine")
        self.torso_widths = widths
        # bottoms: the lower part of the torso takes the trouser material, a hem ring covers the join
        pants = self.skin if bot["style"] == "none" else self.mats.flat("pants", bot["color"], rough=0.8, spec=0.2)
        pat_uv = None
        if bot.get("pattern") and bot["style"] != "none":
            pants = self.mats.tex("pants", self.pattern_image("pants_pattern", bot, "bottoms"), rough=0.8, spec=0.2)
        self.pants = pants
        z_split = z0 + (z1 - z0) * 0.24
        L["waist_z"] = z0 + (z1 - z0) * 0.245   # middle of the hem ring: where a belt sits
        if bot["style"] != "skirt":
            for i_, (tbm, tmat_, _) in enumerate(self.parts):
                if tbm is torso_bm:
                    self.parts[i_] = (torso_bm, {"split": (z_split, tmat_, pants)}, "spine")
        hem_mat = sleeve_mat
        rings = []
        for t in np.linspace(0.215, 0.275, 3):
            w = smooth_interp(t, widths) * envelope(t, b["n"]) * 1.018 + 0.002
            rings.append((z0 + (z1 - z0) * t, w, w * b["depth"], 0, -self.chest_at(t) if chest else 0))
        self.add(lathe(rings, 40, b["power"]), hem_mat, "spine")
        if bot["style"] == "skirt":
            rings = [(L["hip_z"] - 0.13, 0.0, 0.0, 0, 0)]
            for t in np.linspace(0, 1, 8):
                z = L["hip_z"] - 0.13 + t * 0.23
                r = (tw * 1.45) * (1 - t) + (tw * 1.02) * t
                rings.append((z, r, r * 0.85, 0, 0))
            rings.append((L["hip_z"] + 0.1, 0.0, 0.0, 0, 0))
            self.add(lathe(rings, 40), pants, "spine")
        # legs
        leg_r = 0.047 * limb * float(P["body"].get("leg_scale", 1.0))
        self.leg_r = leg_r
        flare = bot["style"] == "flared"
        for s, side in ((1, "L"), (-1, "R")):
            hip = Vector((s * L["hip_x"], 0, L["hip_z"] + 0.02))
            ank = Vector((s * L["ank_x"], 0, L["ankle_z"]))
            bone = f"leg.{side}"
            n_leg0 = len(self.parts)
            bow = float(P.get("posture", {}).get("leg_bow", 0.0))
            if bot["style"] in ("shorts", "skirt", "none") and bow > 0:   # bowed legs: knees out
                knee = hip + (ank - hip) * 0.5 + Vector((s * bow, 0, 0))
                self.add(capsule_bm(hip, knee, leg_r * 0.95, leg_r * 0.92), self.skin, bone)
                self.add(capsule_bm(knee, ank, leg_r * 0.92, leg_r * 0.85), self.skin, bone)
            elif bot["style"] in ("shorts", "skirt", "none"):
                self.add(capsule_bm(hip, ank, leg_r * 0.92, leg_r * 0.85), self.skin, bone)
                if bot["style"] == "shorts":
                    mid = hip + (ank - hip) * 0.42
                    self.add(capsule_bm(hip, mid, leg_r * 1.22, leg_r * 1.18), pants, bone)
            else:
                r1 = leg_r * (1.55 if flare else 1.0)
                if flare:
                    rings = [(0, 0, 0, 0, 0)]
                    n = 10
                    for k in range(n + 1):
                        t = k / n
                        r = leg_r * 1.02 + (r1 - leg_r) * max(0, (t - 0.45) / 0.55) ** 1.6
                        rings.append((t, r, r, 0, 0))
                    rings.append((1.0, 0, 0, 0, 0))
                    bm = lathe(rings, 24)
                    d = (ank - hip); Lg = d.length
                    bmesh.ops.scale(bm, vec=(1, 1, Lg), verts=bm.verts)
                    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
                    bmesh.ops.transform(bm, matrix=Matrix.Translation(hip) @ q.to_matrix().to_4x4(), verts=bm.verts)
                    # round the top so it tucks into the hips
                    self.add(ellipsoid_bm(hip, (leg_r * 1.02,) * 3, segs=20, rings=10), pants, bone)
                    self.add(bm, pants, bone)
                    self.flare_hem = (ank, r1)
                else:
                    self.add(capsule_bm(hip, ank, leg_r * 1.05, leg_r * 1.02), pants, bone)
            if bot.get("pattern") and bot["style"] != "none":   # patterned trousers: UVs around each leg
                def leg_uv(bm, uv, _hip=hip, _ank=ank):
                    for f in bm.faces:
                        us = []
                        for lp in f.loops:
                            co = lp.vert.co
                            tt = (co.z - _ank.z) / max(1e-6, _hip.z - _ank.z)
                            us.append(0.5 + math.atan2(co.x - (_ank.x + (_hip.x - _ank.x) * tt), -co.y) / (2 * math.pi))
                        if max(us) - min(us) > 0.5:
                            us = [u + 1 if u < 0.5 else u for u in us]
                        for lp, u in zip(f.loops, us):
                            lp[uv].uv = (u, (lp.vert.co.z - _ank.z) / max(1e-6, _hip.z - _ank.z))
                for pbm, pm, _pb in self.parts[n_leg0:]:
                    if pm is pants:
                        leg_uv(pbm, pbm.loops.layers.uv.get("UVMap"))
            self.cur_part = f"foot_{side.lower()}"   # shoes and bare feet, incl. boot shafts and socks
            sh = dict(shoes)
            for k in ("color", "sole", "style"):          # mismatched shoes: color_l / color_r ...
                if f"{k}_{side.lower()}" in shoes:
                    sh[k] = shoes[f"{k}_{side.lower()}"]
            n_foot0 = len(self.parts)
            socks = shoes.get("socks")
            if socks:                                      # {"color", "color_l", "color_r", "height" 0..1 of the leg, "cuff"}
                socks = {"color": socks} if isinstance(socks, str) else socks
                scol = socks.get(f"color_{side.lower()}", socks.get("color", "#FFFFFF"))
                smat = self.mats.flat(f"sock_{scol.lstrip('#')}", scol, rough=0.85, spec=0.15)
                top_p = ank + (hip - ank) * float(socks.get("height", 0.35))
                self.add(capsule_bm(ank + Vector((0, 0, -0.02)), top_p, leg_r * 1.13, leg_r * 1.13), smat, bone)
                cuff = socks.get("cuff")
                if cuff:
                    self.add(ellipsoid_bm(top_p, (leg_r * 1.24, leg_r * 1.24, 0.016), segs=20, rings=8),
                             self.mats.flat(f"sock_{cuff.lstrip('#')}", cuff, rough=0.85, spec=0.15), bone)
            self.build_foot(s, side, ank, sh)
            size = float(shoes.get("size", 1.0))
            if size != 1.0:                                # oversized / tiny shoes, scaled about the ground point
                M = Matrix.Translation((ank.x, 0, 0)) @ Matrix.Scale(size, 4) @ Matrix.Translation((-ank.x, 0, 0))
                for pbm, _m, _b in self.parts[n_foot0:]:
                    bmesh.ops.transform(pbm, matrix=M, verts=pbm.verts)
            self.cur_part = None

    def build_foot(self, s, side, ank, shoes):
        L = self.L; limb = L["limb"]
        bone = f"foot.{side}"
        x = ank.x
        st = shoes["style"]
        if st in SHOES:
            SHOES[st](self, s, side, ank, shoes)
            return
        if st not in ("barefoot", "boots", "sneaker"):
            raise ValueError(f"unknown shoes.style {st!r}; known: barefoot, boots, sneaker, {', '.join(sorted(SHOES))}")
        if st == "barefoot":
            n0 = len(self.parts)
            sc = 1.25 * float(shoes.get("foot_size", 1.0))
            self.add(ellipsoid_bm((x, -0.035, 0.042), (0.064 * sc, 0.105 * sc, 0.046 * sc), floor=0.004, segs=28),
                     self.skin, bone)
            fs = float(shoes.get("foot_size", 1.0))
            for k, (tx, tr) in enumerate(((-0.040, 0.026), (-0.012, 0.023), (0.014, 0.021), (0.036, 0.019))):
                tx, tr = tx * s * -1 * fs, tr * fs   # big toe on the inner side
                ty = -0.035 - 0.118 * sc + abs(tx) * 0.35
                self.add(ellipsoid_bm((x + tx, ty, 0.026), (tr, tr * 1.05, tr * 0.95), segs=14, rings=8, floor=0.004),
                         self.skin, bone)
            toe_in = math.radians(float(self.P.get("posture", {}).get("toe_in", 0.0)))   # pigeon-toed bare feet
            if toe_in:
                M = Matrix.Translation((x, 0, 0)) @ Matrix.Rotation(-s * toe_in, 4, "Z") @ Matrix.Translation((-x, 0, 0))
                for pbm, _m, _b in self.parts[n0:]:
                    bmesh.ops.transform(pbm, matrix=M, verts=pbm.verts)
            return
        col = self.mats.flat(f"shoe_{st}", shoes["color"], rough=0.55, spec=0.4)
        if st == "boots":
            sole = self.mats.flat("boot_heel", shoes.get("sole", shade(shoes["color"], 0.62)), rough=0.6)
            def pointy(co):
                if co.y < 0:
                    f = (-co.y / 0.12) ** 1.6
                    co.x *= 1 - 0.5 * f
                    co.z += 0.012 * f
                return co
            self.add(ellipsoid_bm((x, -0.03, 0.058), (0.056, 0.12, 0.048), floor=0.03, deform=pointy, segs=28),
                     col, bone)
            self.add(ellipsoid_bm((x, -0.04, 0.03), (0.054, 0.115, 0.012), deform=pointy, segs=28), sole, bone)
            heel = lathe([(0.0, 0, 0, x, 0.045), (0.0, 0.03, 0.026, x, 0.045), (0.045, 0.034, 0.03, x, 0.045),
                          (0.045, 0, 0, x, 0.045)], 24, power=3.5)
            self.add(heel, sole, bone)
            top_z = 0.215
            self.add(lathe([(0.045, 0, 0, x, 0.0), (0.045, 0.062, 0.06, x, 0.0),
                            (top_z, 0.066, 0.062, x, 0.0), (top_z, 0.0, 0.0, x, 0.0)], 28),
                     col, f"leg.{side}")
            stitch = self.mats.flat("boot_stitch", shoes.get("stitch", PLAYER_RED), rough=0.5)
            for zz, rr in ((top_z - 0.012, 0.0675), (0.12, 0.0655)):
                pts = [(x + rr * math.cos(a), rr * 0.94 * math.sin(a), zz) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
                self.add(tube_bm(pts, 0.0065, cyclic=True), stitch, f"leg.{side}")
            return
        # sneaker
        solec = self.mats.flat("shoe_sole", shoes.get("sole", "#F4F4F0"), rough=0.6)
        self.add(ellipsoid_bm((x, -0.03, 0.055), (0.066 * limb, 0.108, 0.054), floor=0.014, segs=28), col, bone)
        self.add(ellipsoid_bm((x, -0.032, 0.022), (0.071 * limb, 0.114, 0.022), floor=0.0, segs=28), solec, bone)

    def build_arms(self):
        P, L = self.P, self.L
        tw, limb = L["tw"], L["limb"]
        top = P["outfit"]["top"]
        ar = 0.04 * limb
        sleeve = self.mats.cache.get(f"{self.mats.prefix}shirt_sleeve") or self.mats.cache.get(f"{self.mats.prefix}shirt")
        self.arm_pts = {}
        for s, side in ((1, "L"), (-1, "R")):
            sh = Vector((s * tw * 0.92, 0, L["shoulder_z"]))
            wr = Vector((s * (tw * 0.92 + 0.07), -0.005, L["shoulder_z"] - 0.205 * L["h"] ** 0.5))
            if self.reshaped:   # fat bodies: the hands hang clear of the belly
                tz = (wr.z - 0.04 - L["torso_z0"]) / (L["torso_z1"] - L["torso_z0"])
                edge = max(abs(self.torso_point(tz + d, 0.0).x) for d in (-0.08, 0.0, 0.08))
                wr.x = s * max(abs(wr.x), edge + 0.042 * limb)
            self.arm_pts[side] = (sh, wr)
            bone = f"arm.{side}"
            if top["style"] in ("long", "costume"):
                self.add(capsule_bm(sh, wr, ar * 1.08, ar * 1.0), sleeve, bone)
            elif top["style"] == "bare":
                self.add(capsule_bm(sh, wr, ar * 1.0, ar * 0.92), self.skin, bone)
            else:
                self.add(capsule_bm(sh, wr, ar * 0.92, ar * 0.88), self.skin, bone)
                mid = sh + (wr - sh) * 0.42
                self.add(capsule_bm(sh, mid, ar * 1.2, ar * 1.16), sleeve, bone)
            # mitten hand: palm faces the body, thumb forward
            hc = wr + Vector((s * 0.004, -0.004, -0.036))
            self.hand_c = getattr(self, "hand_c", {}); self.hand_c[side] = hc
            self.cur_part = f"hand_{side.lower()}"
            hand_mat = self.skin
            if top.get("gloves"):
                hand_mat = self.mats.flat("gloves", top["gloves"], rough=0.6)
            self.add(ellipsoid_bm(hc, (0.036 * limb, 0.047 * limb, 0.052 * limb), segs=22, rings=12), hand_mat, f"hand.{side}")
            self.add(ellipsoid_bm(hc + Vector((-s * 0.016, -0.034, 0.008)), (0.016, 0.02, 0.026), segs=14, rings=8),
                     hand_mat, f"hand.{side}")
            self.cur_part = None

    # --- costume pieces and headwear
    def build_costume(self):
        P, L = self.P, self.L
        R, c = L["R"], L["head_c"]
        for piece in P["costume"]:
            kind = piece["piece"]
            if kind == "wing_tips":
                mat = self.mats.flat("wing_tips", piece["color"], rough=0.6)
                for s, side in ((1, "L"), (-1, "R")):
                    sh, wr = self.arm_pts[side]
                    for k, (ang, ln) in enumerate(((-0.35, 0.075), (0.05, 0.088), (0.45, 0.075))):
                        base = wr + (sh - wr) * 0.12 + Vector((s * 0.03, 0.012 + 0.018 * k - 0.018, 0.0))
                        rot = (Euler((ang * 0.6, -s * 0.55, 0)).to_matrix())
                        self.add(ellipsoid_bm(base + rot @ Vector((0, 0, -ln * 0.5)), (0.013, 0.03, ln * 0.62),
                                              rot=rot, segs=16, rings=10), mat, f"arm.{side}")
            elif kind == "tail_feathers":
                self.cur_part = "tail"
                mat = self.mats.flat("tail", piece.get("color", "#FFD84D"), rough=0.7)
                for k, ang in enumerate((-0.45, 0.0, 0.45)):
                    rot = Euler((-0.9, 0, ang)).to_matrix()
                    base = Vector((0, L["tw"] * 0.75, L["hip_z"] + 0.03))
                    self.add(ellipsoid_bm(base + rot @ Vector((0, 0.0, 0.06)), (0.03, 0.022, 0.085), rot=rot, segs=16, rings=10),
                             mat, "spine")
                self.cur_part = None
            elif kind in COSTUME:
                COSTUME[kind](self, piece)
                self.cur_part = None
            elif kind == "jeans_stitch":
                mat = self.mats.flat("stitch", piece["color"], rough=0.6)
                if hasattr(self, "flare_hem"):
                    for s, side in ((1, "L"), (-1, "R")):
                        hip = Vector((s * L["hip_x"], 0, L["hip_z"] + 0.02))
                        ank = Vector((s * L["ank_x"], 0, L["ankle_z"]))
                        r1 = self.flare_hem[1]
                        zz = ank.z + 0.022
                        pts = [(ank.x + (r1 + 0.001) * math.cos(a), (r1 + 0.001) * math.sin(a), zz)
                               for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
                        self.add(tube_bm(pts, 0.0075, cyclic=True), mat, f"leg.{side}")
                        # outer seam
                        pts = []
                        for t in np.linspace(0.05, 0.93, 12):
                            p = hip + (ank - hip) * t
                            leg_r = 0.047 * L["limb"] * float(P["body"].get("leg_scale", 1.0))
                            r = leg_r * 1.02 + (r1 - leg_r) * max(0, (t - 0.45) / 0.55) ** 1.6
                            pts.append((p.x + s * (r + 0.002), p.y, p.z))
                        self.add(tube_bm(pts, 0.0055), mat, f"leg.{side}")

    def build_headwear(self):
        P, L = self.P, self.L
        hw = P["headwear"]; t = hw["type"]
        R, c = L["R"], L["head_c"]
        self.hat_parts = []
        if t == "none":
            return
        if t == "chicken_hood":
            self.build_hood(hw)
            return
        self.cur_part = "headwear"   # caps, beanies, headbands: an equipped hat hides them
        if t in ("trucker", "cap"):
            self.build_cap(hw, trucker=(t == "trucker"))
        elif t == "beanie":
            mat = self.mats.flat("beanie", hw["color"], rough=0.85, spec=0.2)
            cuff = self.mats.flat("beanie_cuff", hw.get("accent", shade(hw["color"], 0.85)), rough=0.85, spec=0.2)
            radii = (R * L["hsx"], R * L["hsy"], R * L["hsz"])
            thr = lambda phi: 0.40 - 0.42 * ((1 - math.cos(phi)) / 2)
            bm = solidify_bm(cap_shell_bm(c, radii, thr, lambda el, phi: 1.10 + 0.06 * max(0, math.sin(el)) ** 4), 0.05 * R)
            self.add(bm, mat, "head")
            pts = []
            for phi in np.linspace(0, 2 * math.pi, 48, endpoint=False):
                pts.append(tuple(self.head_point(thr(phi) + 0.1, phi, 1.09)))
            self.add(tube_bm(pts, 0.12 * R, cyclic=True), cuff, "head")
            self.add(ellipsoid_bm(c + Vector((0, 0.05 * R, R * L["hsz"] * 1.2)), (0.24 * R,) * 3, segs=20, rings=12), cuff, "head")
            bs = float(hw.get("scale", 1.0))
            if bs != 1.0:    # a tiny beanie perched on the crown (or an oversized one)
                top_pt = c + Vector((0, 0, R * L["hsz"] * 1.08))
                lift = 0.0
                if bs < 1.0:   # sit on the crown (over the hair) instead of sinking into it
                    lift = (1.07 * math.sqrt(max(0.0, 1 - (bs / 1.07) ** 2)) - (1.08 - 0.865 * bs) - 0.05 * bs) * R * L["hsz"] * min(1.0, (1 - bs) / 0.4)
                M = Matrix.Translation(top_pt + Vector((0, 0, lift))) @ Matrix.Scale(bs, 4) @ Matrix.Translation(-top_pt)
                for pbm, _m, _b in self.parts[-3:]:
                    bmesh.ops.transform(pbm, matrix=M, verts=pbm.verts)
        elif t == "headband":
            self.add_headband(hw["color"])
        elif t in HEADWEAR:
            HEADWEAR[t](self, hw)
        self.cur_part = None

    def add_headband(self, color, el=0.50, s=1.0):
        mat = self.mats.flat("headband", color, rough=0.6)
        pts = [tuple(self.head_point(el - 0.12 * ((1 - math.cos(phi)) / 2), phi, s)) for phi in np.linspace(0, 2 * math.pi, 56, endpoint=False)]
        self.add(tube_bm(pts, 0.065 * self.L["R"], cyclic=True), mat, "head")

    def build_hood(self, hw):
        L = self.L; R, c = L["R"], L["head_c"]
        col = self.mats.flat("costume", hw["color"], rough=0.75, spec=0.25)
        inner = self.mats.flat("costume_inner", shade(hw["color"], 0.82), rough=0.8, spec=0.2)
        open_a = math.radians(hw.get("opening_deg", 52))
        HR = 1.13
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=56, v_segments=36, radius=1.0)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > math.cos(open_a) + 1e-4], context="VERTS")
        rot = Matrix.Rotation(math.radians(90), 4, "X")
        for v in bm.verts:
            co = rot @ v.co
            # let the hood hang down the back of the neck into the costume
            drop = 0.25 * max(0.0, -co.z) * max(0.0, co.y + 0.3)
            v.co = c + Vector((co.x * R * L["hsx"] * HR, co.y * R * L["hsy"] * HR, (co.z - drop) * R * L["hsz"] * HR))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm = solidify_bm(bm, 0.07 * R)
        self.add(bm, col, "head")
        # soft rim around the face opening
        rr = math.sin(open_a) * HR; dz = math.cos(open_a) * HR
        pts = [(c.x + R * L["hsx"] * (rr - 0.02) * math.cos(a), c.y - R * L["hsy"] * (dz - 0.02), c.z + R * L["hsz"] * (rr - 0.02) * math.sin(a))
               for a in np.linspace(0, 2 * math.pi, 56, endpoint=False)]
        self.add(tube_bm(pts, 0.075 * R, cyclic=True), inner, "head")
        # beak above the face, pointing forward and a little down
        beak = self.mats.flat("beak", hw.get("beak", "#F7932F"), rough=0.45, spec=0.45)
        el = open_a + math.radians(hw.get("beak_deg", 14))   # angle from the forward axis, above the opening
        base = self.head_point(el, 0, HR * 0.99)
        d = Vector((0, -1, -0.12)).normalized()
        q = d.to_track_quat("Z", "Y")
        rings = []
        n = 12
        for k in range(n + 1):
            t = k / n
            r = (1 - t ** 1.4) ** 0.9
            rings.append((t * 0.55 * R, 0.34 * R * r, 0.15 * R * r, 0, 0))
        rings.insert(0, (-0.05 * R, 0.0, 0.0, 0, 0))
        rings[-1] = (0.55 * R, 0.0, 0.0, 0, 0)
        bm = lathe(rings, 28)
        for v in bm.verts:   # flatten the underside a touch, curve the tip down
            z = v.co.z / (0.5 * R)
            v.co.y -= 0.05 * R * z * z
        bmesh.ops.transform(bm, matrix=Matrix.Translation(base) @ q.to_matrix().to_4x4(), verts=bm.verts)
        self.add(bm, beak, "head")
        # comb: three bumps along the top, on its own floppy bone
        comb = self.mats.flat("comb", hw.get("comb", "#D63384"), rough=0.5, spec=0.4)
        self.extra_bones.append(("comb", self.head_point(math.radians(80), 0, HR), self.head_point(math.radians(80), 0, HR) + Vector((0, 0, 0.12))))
        self.cur_part = "headwear"   # a hat from the equipment set hides the comb
        for elv, sz in ((70, 0.85), (88, 1.0), (106, 0.85)):
            e = math.radians(elv)
            p = c + Vector((0, -R * HR * math.cos(e) * L["hsy"], R * HR * math.sin(e) * L["hsz"]))
            n_ = (p - c).normalized()
            rot = Vector((0, 0, 1)).rotation_difference(n_).to_matrix()
            self.add(ellipsoid_bm(p + n_ * 0.07 * R * sz, (0.085 * R * sz, 0.17 * R * sz, 0.22 * R * sz), rot=rot, segs=20, rings=12),
                     comb, "comb")
        self.cur_part = None
        if hw.get("headband"):
            self.add_headband(hw["headband"], el=0.42, s=1.0)

    def build_cap(self, hw, trucker):
        L = self.L; R, c = L["R"], L["head_c"]
        body = self.mats.flat("hat", hw["color"], rough=0.7, spec=0.25)
        brim = self.mats.flat("hat_brim", hw.get("brim", hw["color"]), rough=0.6, spec=0.3)
        parts = []
        rx, ry = 1.07 * R * L["hsx"], 1.10 * R * L["hsy"]
        zb, zt = 0.12 * R, (1.10 if trucker else 1.08) * R * L["hsz"]
        rr = (0.24 if trucker else 0.55) * R
        oy = -0.03 * R
        zs = zt - rr
        def crown(t):
            """(z, scale, centre y) at height fraction t of the straight part: the front stays upright,
            the back slopes forward, like a trucker cap."""
            k = 1 - 0.12 * t ** 1.5
            return zb + (zs - zb) * t, k, oy - (0.10 * R * t ** 1.3 if trucker else 0.0)
        def crown_xy(a, t, grow=1.0):
            z, k, cy = crown(t)
            return rx * k * grow * math.sin(a), cy - ry * k * grow * math.cos(a), z
        rings = [(zb, 0, 0, 0, oy)]
        for t in np.linspace(0, 1, 8):
            z, k, cy = crown(t)
            rings.append((z, rx * k, ry * k, 0, cy))
        z1, k1, cy1 = crown(1.0)
        for th in np.linspace(0, math.pi / 2, 8)[1:]:
            kk = k1 * ((1 - rr / R) + (rr / R) * math.cos(th))
            rings.append((zs + rr * math.sin(th), rx * kk, ry * kk, 0, cy1))
        rings[-1] = (zt, 0, 0, 0, cy1)
        parts.append((lathe(rings, 48), body))
        # brim: curved bill at the front of the crown base
        a0 = math.radians(62); Lb = 0.8 * R
        def brim_pt(u, v):
            a = -a0 + 2 * a0 * u
            px, py = rx * math.sin(a), oy - ry * math.cos(a)
            nx, ny = math.sin(a) / rx, -math.cos(a) / ry
            nl = math.hypot(nx, ny); nx, ny = nx / nl, ny / nl
            ln = Lb * max(0.0, math.cos(a * 1.25)) ** 0.8 * v
            z = zb + 0.004 + ln * math.tan(math.radians(6)) - 0.55 * R * (math.sin(a) ** 2) * v * 0.35
            return (px + nx * ln, py + ny * ln, z)
        bm = solidify_bm(grid_bm(brim_pt, 30, 6), 0.045 * R)
        parts.append((bm, brim))
        if trucker:
            pipe = self.mats.flat("hat_piping", hw.get("piping", PLAYER_RED), rough=0.55, spec=0.35)
            pts = [(rx * 1.005 * math.sin(a), oy - ry * 1.005 * math.cos(a), zb + 0.012) for a in np.linspace(0, 2 * math.pi, 64, endpoint=False)]
            parts.append((tube_bm(pts, 0.035 * R, cyclic=True), pipe))
            ap = math.radians(50)
            th = math.radians(45)
            kr = (1 - rr / R) + (rr / R) * math.cos(th)
            zr = zs + rr * math.sin(th)
            line = [crown_xy(-ap, t, 1.004) for t in np.linspace(0.03, 1, 7)]
            line += [(kr * k1 * rx * math.sin(a_), cy1 - kr * k1 * ry * math.cos(a_), zr) for a_ in np.linspace(-ap, ap, 16)]
            line += [crown_xy(ap, t, 1.004) for t in np.linspace(1, 0.03, 7)]
            parts.append((tube_bm(line, 0.03 * R), pipe))
            # T-Rex patch on the front panel
            img = trex_patch_texture(f"{self.mats.prefix}trex", hw["color"], hw.get("patch", "#FFD84D"))
            pmat = self.mats.tex("hat_patch", img, rough=0.65, spec=0.25)
            pa = math.radians(36); tv0, tv1 = 0.2, 0.93
            def patch_pt(u, v):
                return crown_xy(-pa + 2 * pa * u, tv0 + (tv1 - tv0) * v, 1.012)
            pb = grid_bm(patch_pt, 16, 8)
            uvl = pb.loops.layers.uv.new("UVMap")
            vmap = {}
            for j_ in range(9):
                for i_ in range(17):
                    vmap[tuple(round(c_, 6) for c_ in patch_pt(i_ / 16, j_ / 8))] = (i_ / 16, j_ / 8)
            for f in pb.faces:
                for lp in f.loops:
                    lp[uvl].uv = vmap[tuple(round(c_, 6) for c_ in lp.vert.co)]
            bmesh.ops.recalc_face_normals(pb, faces=pb.faces)
            # make sure the patch faces outwards (-Y)
            if sum(f.normal.y for f in pb.faces) > 0:
                bmesh.ops.reverse_faces(pb, faces=pb.faces)
            parts.append((pb, pmat))
        tilt = Matrix.Rotation(math.radians(-hw.get("tilt_deg", 12)), 4, "X")
        place = Matrix.Translation(c + Vector((0, 0, hw.get("lift", 0.03) * R))) @ tilt
        for bm, mat in parts:
            bmesh.ops.transform(bm, matrix=place, verts=bm.verts)
            if hw.get("separate"):
                self.hat_parts.append((bm, mat))
            else:
                self.add(bm, mat, "head")

    # --- assembly
    def make_mesh(self, name, parts, with_groups=True):
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        uv_out = bm.loops.layers.uv.new("UVMap")
        deform = bm.verts.layers.deform.verify()
        mats, groups = [], []
        for pbm, mat, bone in parts:
            split = None
            if isinstance(mat, dict):
                split = mat["split"]; mat = split[1]
                if split[2] not in mats:
                    mats.append(split[2])
            if mat not in mats:
                mats.append(mat)
            if bone not in groups:
                groups.append(bone)
            mi, gi = mats.index(mat), groups.index(bone)
            uv_in = pbm.loops.layers.uv.get("UVMap")
            vmap = {}
            for v in pbm.verts:
                nv = bm.verts.new(v.co)
                nv[deform][gi] = 1.0
                vmap[v] = nv
            for f in pbm.faces:
                try:
                    nf = bm.faces.new([vmap[v] for v in f.verts])
                except ValueError:
                    continue
                nf.material_index = mi
                if split and f.calc_center_median().z < split[0]:
                    nf.material_index = mats.index(split[2])
                nf.smooth = True
                if uv_in:
                    for lo, li in zip(nf.loops, f.loops):
                        lo[uv_out].uv = li[uv_in].uv
            pbm.free()
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
        self.coll.objects.link(ob)
        for m in mats:
            me.materials.append(m)
        if with_groups:
            for g in groups:
                ob.vertex_groups.new(name=g)
        return ob

    def build_armature(self):
        L = self.L
        pid = self.P["id"]
        arm = bpy.data.armatures.new(f"{self.prefix}{pid}_rig")
        ob = bpy.data.objects.new(f"{self.prefix}{pid}", arm)
        self.coll.objects.link(ob)
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode="EDIT")
        eb = arm.edit_bones
        def bone(name, h, t, parent=None):
            b = eb.new(name); b.head = h; b.tail = t; b.roll = 0.0
            if parent:
                b.parent = eb[parent]; b.use_connect = False
            return b
        hc = L["head_c"]
        bone("root", (0, 0, 0), (0, 0, 0.15))
        bone("spine", (0, 0, L["hip_z"]), (0, 0, L["torso_z1"] - 0.02), "root")
        bone("head", (0, 0, L["torso_z1"] - 0.01), (0, 0, hc.z + L["R"]), "spine")
        for side in ("L", "R"):
            sh, wr = self.arm_pts[side]
            s = 1 if side == "L" else -1
            bone(f"arm.{side}", sh, wr, "spine")
            bone(f"hand.{side}", wr, wr + Vector((0, 0, -0.075)), f"arm.{side}")
            hip = (s * L["hip_x"], 0, L["hip_z"])
            ank = (s * L["ank_x"], 0, L["ankle_z"])
            bone(f"leg.{side}", hip, ank, "root")
            bone(f"foot.{side}", ank, (ank[0], -0.11, 0.03), f"leg.{side}")
        for name, h, t in self.extra_bones:
            bone(name, tuple(h), tuple(t), "head")
        bpy.ops.object.mode_set(mode="OBJECT")
        return ob

    # --- equipment slots (docs/equipment.md)
    def _cos(self, bones, tags=(None,)):
        for (bm, _m, bone), tag in zip(self.parts, self.part_tags):
            if bone in bones and tag in tags:
                for v in bm.verts:
                    yield v.co

    def measure_slots(self):
        """Slot origin (armature space, Blender axes), bone and fit scale, measured from the real
        geometry so gear made for the reference Jarling fits every build."""
        L, P = self.L, self.P
        c, R = L["head_c"], L["R"]
        out = {}
        skip = getattr(self, "crown_skip", ())
        crown = max(v.co.z for i, ((bm, _m, bone), tag) in enumerate(zip(self.parts, self.part_tags))
                    if bone == "head" and tag is None and i not in skip for v in bm.verts) - c.z
        out["head"] = ("head", c.copy(), (crown / SLOT_REF["head_crown"],) * 3)
        fs = float(P["face"].get("scale", 1.3))
        ez = EYE_Y * fs
        fy = c.y - R * L["hsy"] * math.sqrt(1 - ez * ez)
        s = R * L["hsx"] / SLOT_REF["face_r"]
        out["face"] = ("head", Vector((0, fy, c.z + ez * R * L["hsz"])), (s, s, s))
        zs = L["shoulder_z"]
        back = max(co.y for co in self._cos({"spine"}) if abs(co.z - zs) < 0.03 and abs(co.x) < 0.04)
        s = L["tw"] / SLOT_REF["back_tw"]
        out["back"] = ("spine", Vector((0, back, zs)), (s, s, s))
        zw = L["waist_z"]
        band = [co for co in self._cos({"spine"}) if abs(co.z - zw) < 0.012]
        rx = max(abs(co.x) for co in band)
        y0, y1 = min(co.y for co in band), max(co.y for co in band)
        out["waist"] = ("spine", Vector((0, (y0 + y1) / 2, zw)),
                        (rx / SLOT_REF["waist_rx"], (y1 - y0) / 2 / SLOT_REF["waist_ry"], 1.0))
        for side, sg in (("L", 1), ("R", -1)):
            hip = Vector((sg * L["hip_x"], 0, L["hip_z"] + 0.02))
            ank = Vector((sg * L["ank_x"], 0, L["ankle_z"]))
            k = hip + (ank - hip) * 0.45
            d = ank - hip; dl = d.length; d = d / dl
            rk = 0.0   # leg radius around the knee: perpendicular distance from the hip-ankle axis
            for co in self._cos({f"leg.{side}"}):
                t = (co - hip).dot(d) / dl
                if -0.02 < t < 0.5:
                    rk = max(rk, ((co - hip) - d * (co - hip).dot(d)).length)
            out[f"knee_{side.lower()}"] = (f"leg.{side}", k, (rk / SLOT_REF["knee_r"],) * 3)
            lb = L["limb"]
            out[f"foot_{side.lower()}"] = (f"foot.{side}", Vector((ank.x, 0, 0)), (lb, lb, lb))
            out[f"hand_{side.lower()}"] = (f"hand.{side}", self.hand_c[side].copy(), (lb, lb, lb))
        return out

    def add_slots(self, rig, fit):
        bpy.context.view_layer.update()
        obs = {}
        for name in SLOTS:
            bone, pos, scale = fit[name]
            e = bpy.data.objects.new(f"{self.prefix}slot_{name}", None)
            e.empty_display_type = "ARROWS"; e.empty_display_size = 0.05
            self.coll.objects.link(e)
            e.parent = rig; e.parent_type = "BONE"; e.parent_bone = bone
            b = rig.data.bones[bone]
            e.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local @ Matrix.Translation((0, b.length, 0))).inverted()
            e.matrix_basis = Matrix.LocRotScale(pos, None, Vector(scale))
            e["jarling_slot"] = name
            e["jarling_build"] = self.P["body"]["build"]
            e["jarling_id"] = self.P["id"]
            obs[name] = e
        bpy.context.view_layer.update()
        return obs

    def build(self):
        self.layout()
        self.build_head()
        self.build_body()
        self.build_arms()
        self.build_hair()
        self.build_features()
        self.build_costume()
        self.build_headwear()
        pid = self.P["id"]
        rig = self.build_armature()
        slot_fit = self.measure_slots()
        main = [p for p, t in zip(self.parts, self.part_tags) if t is None]
        body = self.make_mesh(f"{self.prefix}{pid}_body", main)
        body.parent = rig
        mod = body.modifiers.new("Armature", "ARMATURE"); mod.object = rig
        # separable body parts: their own skinned meshes on the same rig, so gear can hide them
        self.part_obs = {}
        tags = BODY_PARTS + sorted({t for t in self.part_tags if t and t not in BODY_PARTS})
        for tag in tags:
            pp = [p for p, t in zip(self.parts, self.part_tags) if t == tag]
            if not pp:
                continue
            ob = self.make_mesh(f"{self.prefix}{pid}_part_{tag}", pp)
            ob.parent = rig
            m = ob.modifiers.new("Armature", "ARMATURE"); m.object = rig
            ob["jarling_part"] = tag
            self.part_obs[tag] = ob
        body["jarling_expressions"] = {k: list(v) for k, v in self.expr_uv.items()}
        rig["jarling"] = 1
        rig["jarling_body_type"] = "standard"
        extra = {}
        loops = ["idle", "run", "cheer"]
        for name in self.P.get("actions", []):       # extra actions a character's bible needs
            fn, loop = ACTIONS[name]
            extra[name] = fn(self)
            if loop:
                loops.append(name)
        rig["jarling_loops"] = loops
        self.rig, self.body, self.hat = rig, body, None
        if self.hat_parts:
            hat = self.make_mesh(f"{self.prefix}{pid}_hat", [(bm, m, "hat") for bm, m in self.hat_parts], with_groups=False)
            # hat mesh is built in armature space; parent to the head bone without moving it
            b = rig.data.bones["head"]
            hat.parent = rig; hat.parent_type = "BONE"; hat.parent_bone = "head"
            hat.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local @ Matrix.Translation((0, b.length, 0))).inverted()
            hat["jarling_detachable"] = True
            hat["jarling_part"] = "headwear"
            self.hat = hat
        self.lamp_obs = []
        for lp in self.lamps:     # real lights (a miner's headlamp): spot lights on the head bone, exported in the glb
            ld = bpy.data.lights.new(f"{self.prefix}{pid}_{lp.get('name', 'lamp')}", "SPOT")
            ld.energy = float(lp.get("watts", 30)); ld.color = srgb_to_lin(hex_rgb(lp.get("color", "#FFF2C0")))
            ld.spot_size = math.radians(float(lp.get("spot_deg", 55))); ld.spot_blend = 0.4; ld.shadow_soft_size = 0.03
            lo = bpy.data.objects.new(ld.name, ld)
            self.coll.objects.link(lo)
            b = rig.data.bones["head"]
            lo.parent = rig; lo.parent_type = "BONE"; lo.parent_bone = "head"
            lo.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local @ Matrix.Translation((0, b.length, 0))).inverted()
            q = Vector(lp.get("dir", (0, -1, 0))).normalized().to_track_quat("-Z", "Y")
            lo.matrix_basis = Matrix.LocRotScale(Vector(lp["pos"]), q, None)
            lo["jarling_lamp"] = lp.get("name", "lamp")
            self.lamp_obs.append(lo)
        self.slots = self.add_slots(rig, slot_fit)
        rig["jarling_slots"] = list(self.slots.keys())
        if self.reshaped:
            rig["jarling_width"] = float(self.P["body"].get("width", 1.0)); rig["jarling_belly"] = self.belly01
        feats = sorted(t[len("feature_"):] for t in self.part_obs if t.startswith("feature_"))
        if feats:
            rig["jarling_features"] = feats
        build_actions(rig, self.P.get("posture", {}), self.prefix, extra=extra, bob=self.bob_bones)
        return self

# -------------------------------------------------------------------------------------- actions
FPS = 24

def _to_local(pb, R=None, t=None):
    B = pb.bone.matrix_local.to_3x3()
    Bi = B.inverted()
    q = (Bi @ R @ B).to_quaternion() if R is not None else Quaternion()
    loc = Bi @ Vector(t) if t is not None else Vector()
    return q, loc

def _world_scale_local(pb, sxyz):
    B = pb.bone.matrix_local.to_3x3()
    out = [1.0, 1.0, 1.0]
    for i in range(3):   # local axis i -> world axis it lines up with best
        col = Vector((B[0][i], B[1][i], B[2][i]))
        w = max(range(3), key=lambda k: abs(col[k]))
        out[i] = sxyz[w]
    return out

def pose_entry(name, e):
    """Turn a friendly pose entry into an armature-space rotation."""
    rx = ry = rz = 0.0
    s = 1 if name.endswith(".L") else -1
    if name.startswith(("arm", "leg", "hand")):
        rx -= e.get("swing", 0.0)                 # + swings forward
        ry += -s * e.get("out", 0.0)              # + raises sideways away from the body
        rz += e.get("twist", 0.0)
    elif name.startswith("foot"):
        rx += e.get("point", 0.0)                 # + points the toe down
        ry += -s * e.get("out", 0.0)
    else:
        rx += e.get("lean", 0.0)                  # + leans forward
        ry += e.get("tilt", 0.0)
        rz += e.get("twist", 0.0)
    return Euler((math.radians(rx), math.radians(ry), math.radians(rz)), "XYZ").to_matrix()

def mirror(pose):
    out = {}
    for k, v in pose.items():
        if k.endswith(".L"):
            out[k[:-2] + ".R"] = v
        elif k.endswith(".R"):
            out[k[:-2] + ".L"] = v
        else:
            v = dict(v)
            if "twist" in v: v["twist"] = -v["twist"]
            if "tilt" in v: v["tilt"] = -v["tilt"]
            out[k] = v
    return out

def action_keys(posture):
    sl, hl, ao = posture.get("spine_lean", 0.0), posture.get("head_lean", 0.0), posture.get("arm_out", 0.0)
    def base(extra=None):
        p = {"spine": {"lean": sl}, "head": {"lean": hl}, "arm.L": {"out": ao + 4}, "arm.R": {"out": ao + 4}}
        for k, v in (extra or {}).items():
            cur = dict(p.get(k, {}))
            for kk, vv in v.items():
                cur[kk] = cur.get(kk, 0.0) + vv if not isinstance(vv, tuple) else vv
            p[k] = cur
        return p
    acts = {}
    acts["idle"] = [
        (1, base({"comb": {"tilt": 6}})),
        (13, base({"spine": {"scale": (1.01, 1.01, 1.015)}, "head": {"lean": -1.0, "scale": (0.99, 0.99, 0.985)}, "comb": {"tilt": -6},
                   "arm.L": {"out": 1.5}, "arm.R": {"out": 1.5}})),
        (25, base({"spine": {"scale": (1.02, 1.02, 1.03)}, "head": {"lean": -2.5, "tilt": 2, "scale": (0.98, 0.98, 0.97)}, "comb": {"tilt": 6},
                   "arm.L": {"out": 3}, "arm.R": {"out": 3}})),
        (37, base({"spine": {"scale": (1.01, 1.01, 1.015)}, "head": {"lean": -1.0, "scale": (0.99, 0.99, 0.985)}, "comb": {"tilt": -6},
                   "arm.L": {"out": 1.5}, "arm.R": {"out": 1.5}})),
        (49, base({"comb": {"tilt": 6}})),
    ]
    c1 = {"root": {"loc": (0, 0, -0.012), "scale": (1.04, 1.04, 0.94)}, "spine": {"lean": 14, "twist": 8}, "head": {"lean": -10},
          "leg.L": {"swing": 42}, "leg.R": {"swing": -42}, "foot.L": {"point": -12}, "foot.R": {"point": 30},
          "arm.L": {"swing": -50, "out": 8}, "arm.R": {"swing": 50, "out": 8}, "hand.L": {"swing": -10}, "hand.R": {"swing": 20},
          "comb": {"lean": -14}}
    c2 = {"root": {"loc": (0, 0, 0.05), "scale": (0.97, 0.97, 1.05)}, "spine": {"lean": 12}, "head": {"lean": -8},
          "leg.L": {"swing": 0}, "leg.R": {"swing": 0}, "foot.L": {"point": 10}, "foot.R": {"point": 10},
          "arm.L": {"out": 10}, "arm.R": {"out": 10}, "comb": {"lean": 10}}
    acts["run"] = [(1, base(c1)), (5, base(c2)), (9, base(mirror(c1))), (13, base(mirror(c2))), (17, base(c1))]
    acts["kick"] = [
        (1, base()),
        (7, base({"root": {"loc": (0, 0, -0.015), "scale": (1.03, 1.03, 0.95)}, "spine": {"lean": -8}, "head": {"lean": 6},
                  "leg.R": {"swing": -55}, "foot.R": {"point": 20}, "leg.L": {"swing": 5},
                  "arm.L": {"swing": 35, "out": 25}, "arm.R": {"swing": -30, "out": 20}})),
        (11, base({"root": {"loc": (0, 0, -0.03), "scale": (1.05, 1.05, 0.92)}, "spine": {"lean": -14, "twist": -10}, "head": {"lean": 10},
                   "leg.R": {"swing": -78}, "foot.R": {"point": 35},
                   "leg.L": {"swing": 8, "scale": (1.10, 1.10, 0.84)}, "foot.L": {"scale": (1.18, 1.18, 0.80)},
                   "arm.L": {"swing": 50, "out": 45}, "arm.R": {"swing": -45, "out": 35}, "comb": {"lean": 15}})),
        (14, base({"root": {"loc": (0, 0, 0.0)}, "spine": {"lean": 8, "twist": 6}, "head": {"lean": 6},
                   "leg.R": {"swing": 72}, "foot.R": {"point": 35},
                   "leg.L": {"swing": -4, "scale": (0.95, 0.95, 1.07)}, "foot.L": {"scale": (0.96, 0.96, 1.05)},
                   "arm.L": {"swing": -40, "out": 35}, "arm.R": {"swing": 50, "out": 25}, "comb": {"lean": -20}})),
        (19, base({"root": {"loc": (0, 0, 0.06), "scale": (0.95, 0.95, 1.07)}, "spine": {"lean": -16, "twist": 10}, "head": {"lean": -12},
                   "leg.R": {"swing": 112}, "foot.R": {"point": 30},
                   "leg.L": {"swing": -10, "scale": (0.95, 0.95, 1.08)}, "foot.L": {"point": 25},
                   "arm.L": {"swing": -20, "out": 85}, "arm.R": {"swing": 30, "out": 75}, "comb": {"lean": 25}})),
        (26, base({"root": {"loc": (0, 0, -0.02), "scale": (1.06, 1.06, 0.90)}, "spine": {"lean": 6}, "head": {"lean": 4},
                   "leg.R": {"swing": 14}, "foot.R": {"point": 5}, "leg.L": {"scale": (1.05, 1.05, 0.93)},
                   "arm.L": {"out": 30}, "arm.R": {"out": 25}, "comb": {"lean": -12}})),
        (37, base()),
    ]
    up = {"arm.L": {"out": 112, "swing": 10}, "arm.R": {"out": 112, "swing": 10}, "head": {"lean": -6}}
    acts["cheer"] = [
        (1, base({**up, "root": {"scale": (1.06, 1.06, 0.90)}, "hand.L": {"twist": -15}, "hand.R": {"twist": 15}})),
        (4, base({**up, "root": {"loc": (0, 0, 0.06), "scale": (0.95, 0.95, 1.08)}, "comb": {"lean": 15}})),
        (7, base({"arm.L": {"out": 128, "swing": 12}, "arm.R": {"out": 128, "swing": 12}, "head": {"lean": -14}, "root": {"loc": (0, 0, 0.10)},
                  "leg.L": {"out": 8}, "leg.R": {"out": 8}, "hand.L": {"twist": 25}, "hand.R": {"twist": -25}, "comb": {"lean": -10}})),
        (10, base({**up, "root": {"loc": (0, 0, 0.05), "scale": (0.96, 0.96, 1.06)}})),
        (13, base({**up, "root": {"scale": (1.06, 1.06, 0.90)}, "hand.L": {"twist": 15}, "hand.R": {"twist": -15}})),
        (16, base({**up, "root": {"loc": (0, 0, 0.06), "scale": (0.95, 0.95, 1.08)}, "comb": {"lean": 15}})),
        (19, base({"arm.L": {"out": 128, "swing": 12}, "arm.R": {"out": 128, "swing": 12}, "head": {"lean": -14, "tilt": 6}, "root": {"loc": (0, 0, 0.10)},
                   "leg.L": {"out": 8}, "leg.R": {"out": 8}, "hand.L": {"twist": -25}, "hand.R": {"twist": 25}, "comb": {"lean": -10}})),
        (22, base({**up, "root": {"loc": (0, 0, 0.05), "scale": (0.96, 0.96, 1.06)}})),
        (25, base({**up, "root": {"scale": (1.06, 1.06, 0.90)}, "hand.L": {"twist": -15}, "hand.R": {"twist": 15}})),
    ]
    return acts

def apply_pose(rig, pose, frame=None):
    for pb in rig.pose.bones:
        e = pose.get(pb.name, {})
        R = pose_entry(pb.name, e)
        q, loc = _to_local(pb, R, e.get("loc"))
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = q
        pb.location = loc
        pb.scale = _world_scale_local(pb, e.get("scale", (1, 1, 1)))
        if frame is not None:
            for path in ("rotation_quaternion", "location", "scale"):
                pb.keyframe_insert(path, frame=frame, group=pb.name)

def _with_bob(pose, bob):
    """Copy the comb's secondary motion onto the other floppy head bones (antennae, pom-poms...)."""
    src = pose.get("comb")
    if not bob or not src:
        return pose
    pose = dict(pose)
    for name, amount, side in bob:
        if name not in pose:
            pose[name] = {k: (v * amount * (side if k == "tilt" else 1.0)) for k, v in src.items() if not isinstance(v, tuple)}
    return pose

def build_actions(rig, posture, prefix="", extra=None, acts=None, bob=None):
    """Key the actions on `rig`. `acts` replaces the standard set (other body types pass their
    own {name: [(frame, pose), ...]}, which must include "idle"); `extra` is added to it."""
    rig.animation_data_create()
    acts = dict(acts) if acts is not None else action_keys(posture)
    acts.update(extra or {})
    made = {}
    for name, keys in acts.items():
        act = bpy.data.actions.new(f"{prefix}{name}" if prefix else name)
        act.use_fake_user = True
        rig.animation_data.action = act
        for f, pose in keys:
            apply_pose(rig, _with_bob(pose, bob), f)
        act.frame_range = (keys[0][0], keys[-1][0])
        act.use_frame_range = True
        made[name] = act
    rig.animation_data.action = made["idle"]
    rig["jarling_actions"] = list(made.keys())
    return made

def pose_at(builder, action, frame):
    """Pose a built Jarling at `frame` of `action` (for renders)."""
    rig = builder.rig
    name = f"{builder.prefix}{action}" if builder.prefix else action
    act = bpy.data.actions[name]
    rig.animation_data.action = act
    if hasattr(rig.animation_data, "action_slot") and act.slots:
        rig.animation_data.action_slot = act.slots[0]
    bpy.context.scene.frame_set(frame)

def set_expression(builder, expr):
    """Shift the face UVs to another atlas cell (Blender UV space: v up)."""
    du, dv = getattr(builder, "expr_uv", EXPR_UV_OFFSET)[expr]
    cur = builder.__dict__.get("_expr_off", (0.0, 0.0))
    me = builder.body.data
    mi = list(me.materials).index(builder.face_mat)
    uv = me.uv_layers["UVMap"].data
    for p in me.polygons:
        if p.material_index == mi:
            for li in p.loop_indices:
                u, v = uv[li].uv
                uv[li].uv = (u - cur[0] + du, v + cur[1] - dv)
    builder._expr_off = (du, dv)

def build_jarling(params, prefix=""):
    t = params.get("body", {}).get("type", "standard")
    if t == "standard":
        return Builder(params, prefix).build()
    if t not in BODY_TYPES:
        raise ValueError(f"unknown body.type {t!r}; known: standard, {', '.join(sorted(BODY_TYPES))}")
    return BODY_TYPES[t](params, prefix).build()

# ------------------------------------------------------------------------------- random generics
SKIN_TONES = ["#FFE1CC", "#F7CFAE", "#EFBB90", "#D99E6E", "#BF8150", "#9A6239", "#7A4A2C", "#5C3720"]
HAIR_COLOURS = ["#2A2026", "#4A2F23", "#7A4B2A", "#A34E25", "#E3B85E", "#D9782D", "#BDB7B2", "#4A72D9", "#F08CB8", "#8A5CC9"]
# Generic outfits avoid the player colours so crowds never read as P1/P2.
OUTFIT_COLOURS = ["#3E7BEA", "#5CC6F2", "#FF9A2E", "#FFD23F", "#9B5DE5", "#FF7AB6", "#1FB5A8", "#F4F4F0", "#2C3E7A", "#7E57C2"]
PANTS_COLOURS = ["#3B5BA5", "#2C3E7A", "#5B4636", "#8A8F99", "#D9C9A3", "#3A3A46", "#6FA8DC"]
HAIR_STYLES = ["short", "swoop", "bob", "bun", "ponytail", "spiky", "curly", "afro", "buzz", "long", "none"]

def random_params(seed):
    r = random.Random(seed)
    skin = r.choice(SKIN_TONES)
    hair_c = r.choice(HAIR_COLOURS[:7]) if r.random() < 0.8 else r.choice(HAIR_COLOURS[7:])
    style = r.choice(HAIR_STYLES)
    top_c = r.choice(OUTFIT_COLOURS)
    head_t = "none"
    hw = {"type": "none"}
    x = r.random()
    if x < 0.18:
        hw = {"type": "cap", "color": r.choice(OUTFIT_COLOURS), "brim": r.choice(OUTFIT_COLOURS), "tilt_deg": 8}
    elif x < 0.3:
        hw = {"type": "beanie", "color": r.choice(OUTFIT_COLOURS), "accent": "#F4F4F0"}
    brow_c = shade(hair_c, 0.75) if hair_c not in HAIR_COLOURS[7:] else "#4A2F23"
    return {
        "id": f"generic{seed}", "name": f"Generic {seed}",
        "head": {"shape": r.choice(list(HEAD_SHAPES)), "size": r.uniform(0.95, 1.05), "ears": "round"},
        "skin": skin,
        "face": {"eyes": r.choice(list(EYES)), "brows": r.choice(["thin", "soft", "arched", "thick", "bushy"]),
                 "nose": r.choice(NOSES), "mouth": r.choice(["smile", "smile", "grin", "grin_top", "smirk"]),
                 "brow_color": brow_c, "blush": r.uniform(0.2, 0.6), "freckles": r.random() < 0.2,
                 "eye_spacing": r.uniform(0.31, 0.37), "lid": r.choice([0, 0, 0, 0.18])},
        "hair": {"style": style, "color": hair_c},
        "headwear": hw,
        "body": {"build": r.choice(["slim", "regular", "stocky", "round"]), "height": r.uniform(0.9, 1.1)},
        "outfit": {
            "top": {"style": r.choice(["tee", "tee", "long", "stripe"]), "color": top_c,
                    "accent": r.choice([c for c in OUTFIT_COLOURS if c != top_c])},
            "bottoms": {"style": r.choice(["pants", "pants", "shorts", "skirt"]), "color": r.choice(PANTS_COLOURS)},
            "shoes": {"style": "sneaker", "color": r.choice(OUTFIT_COLOURS + ["#2A2A33"]), "sole": "#F4F4F0"},
        },
        "costume": [],
        "posture": {"spine_lean": r.uniform(-3, 3), "head_lean": r.uniform(-3, 2), "arm_out": r.uniform(0, 4)},
    }

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

# ---------------------------------------------------------------------------------- plug-ins
def _load_plugins():
    import glob, importlib, os
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here, "pieces_*.py")) + glob.glob(os.path.join(here, "body_*.py"))):
        importlib.import_module(os.path.splitext(os.path.basename(f))[0])

_load_plugins()
