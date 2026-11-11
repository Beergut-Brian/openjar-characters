"""Kit v2 outfit pieces for the standard Jarling body: shirt/trouser patterns, shoes, costume pieces.

Patterns (`outfit.top.pattern` / `outfit.bottoms.pattern`, a name, a layer dict or a list of layers;
a layer inherits `color`/`accent` from the top/bottoms dict):
  vstripes     accent "#1A1A1E", count 12 (top) / 8 (bottoms), offset 0.0 (turns, 0.5 = stripe edge at the front)
  vacation     accent "#FF6F91" (flowers), accent2 "#2FA88A" (leaves), center "#FFE066", count 14, seed 7, size 1.0
  hstripe      accent "#F2F2EE", v 0.58, width 0.10, edge null (thin edge lines colour, e.g. silver on hi-vis)
  hstripes     accent "#F1E7CF", count 5, width 0.5 (band height as a fraction of each period), v0 0.30 / v1 0.92 (top; bottoms 0 / 1): even horizontal stripes
  stars        accent "#FFE066", count 26 (top) / 14 (bottoms), size 1.0, seed 3
  patches      accent "#E8A33D", accent2 "#5B8FD6", stitch null (default darker accent), count 3 (2 or 3)
  emblem       shape "star" ("shield"|"star"|"circle"), accent "#FFD23F", size 0.13 (half height in V), v 0.62, rim null, inner null
  buttons      accent "#2A2F5A", rows 1 (1 or 2), count 5, line null (rows 1: darker centre line, default shade of color)
  vest         accent "#5A4A8C" (vest), open 0.10 (front strip half width in U), pockets true, trim null
  collar       accent "#8A5CC9", depth 0.34 (how far the V comes down, in V), width 0.07, inner null (colour inside the V)
  bib          accent "#3E6FB0", top 0.66 (V), width 0.22 (half width in U), button "#F2D16B"
  belly_panel  accent "#FFE38A", v 0.42, width 0.22 (half width in U), height 0.34 (half height in V), soft 0.02
  dials        accent "#FF9F1C", line "#2A2A33", size 1.35
  jersey       accent "#F2B632" (collar band), number "55" (digits), number_color "#F7F7F5", outline null (thin number edge colour; null = accent), front true, back true, size 0.36 (number height in V), v 0.56, v_back 0.50, text null (block letters across the upper back, A-Z 0-9 and space), text_v 0.83, text_size 0.065, aspect 0.62 (glyph width squash: the torso texture is wider than tall)
Shoes (`outfit.shoes.style`; `color` is per side, `size`/`socks` are the core's):
  sandals          color "#8B5A2B" (straps; the sole is a darker shade), foot_size 1.0; the foot is B.skin
  moon_boots       color "#D9DCE3", sole "#7C808A", rings 2
  rain_boots       color "#FFD23F", sole "#2A2A33", height 0.20 (top of the shaft, m above ground)
  clogs            color "#4FB3A9", sole null (darker color), strap true
  slippers         color "#F2B8C6"
  dress            color "#2A2A33", sole null
  footies          color = the shoes colour (match the onesie)
  wrestling_boots  color "#2A3A8C", lace "#F7F7F5", sole null, height 0.235
  chunky_boots     color "#8B5A2B", sole "#3A3330", cap null (toe cap, default darker color)
  high_tops        color "#1A1A1E" (upper), accent "#2A6FD6" (side panel, collar, heel stripe), sole "#F7F7F5", lace "#F7F7F5", height 0.15 (top of the collar, m above ground)
Costume (`costume: [{"piece": name, ...}]`):
  whistle_cord  color "#FFD23F" (whistle), cord "#2A6FD6", t 0.56 (height on the torso), x 0.0 (turn off centre, radians), size 1.0 (whistle scale; Coach Whistle uses 1.5)
  sash          color "#C8A2F0", side "L" (the shoulder it goes over), width 0.17 (in torso height)
  cape          (part "cape") color "#7A2E8C", trim "#F2D16B", length 1.0 (1 = knee height), flare 0.3
  back_spikes   color "#2FA88A", count 5, size 1.0
  dino_tail     (part "tail") color "#5FB85A", spikes null (colour: adds soft spikes along the top), length 1.0
  box_torso     color "#C49A6C", accent "#FF9F1C" (dial fills), line "#3A2A1E" (marker)
  hose_arms     color "#B8BCC4", rings 9
  shoulder_pads  color <top colour> (the pads under the shirt), size 1.0, stripes null (colour: two rings round each short sleeve), hem null (colour: sleeve hem ring); part of the top, on the spine bone, so raised arms swing out from under them
  long_skirt    color "#6A5ACD", length 1.0 (0 = just below the hips, 1 = the ankles), flare 1.0, mud null (colour)
The `whistle` piece in pieces_hill.py sits at a fixed depth (made for the beard), use `whistle_cord` on other bodies.
"""
import math, random
import numpy as np
import bmesh
from mathutils import Vector, Euler, Matrix
import jarling_kit as kit
from jarling_kit import lathe, ellipsoid_bm, capsule_bm, tube_bm, grid_bm, solidify_bm, hex_rgb, shade, mix_hex

if not hasattr(kit, "PATTERNS"):
    kit.PATTERNS = {}
if not hasattr(kit, "SHOES"):
    kit.SHOES = {}

# ================================================================================== helpers
def _rgb(h):
    return np.array(hex_rgb(h), np.float32)

def _cov(d, H):
    """Antialiased coverage of a signed distance in V units (about 1.5 texels soft)."""
    aa = 1.5 / H
    return np.clip(0.5 - d / aa, 0.0, 1.0)

def _put(img, d, col, opacity=1.0):
    a = (_cov(d, img.shape[0]) * opacity)[..., None]
    img[:] = img * (1 - a) + _rgb(col) * a

def _x(U, uc):
    """Signed distance around from uc, in V units (texels are square: du 0.05 = dv 0.10)."""
    return (((U - uc + 0.5) % 1.0) - 0.5) * 2.0

def _sd_poly(X, Y, pts):
    """Signed distance to a closed polygon (numpy, Inigo Quilez)."""
    d = None; s = np.ones_like(X)
    n = len(pts)
    for i in range(n):
        ax, ay = pts[i]; bx, by = pts[i - 1]
        ex, ey = bx - ax, by - ay
        wx, wy = X - ax, Y - ay
        h = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey), 0, 1)
        dx, dy = wx - ex * h, wy - ey * h
        dd = dx * dx + dy * dy
        d = dd if d is None else np.minimum(d, dd)
        c1 = Y >= ay; c2 = Y < by; c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        s = np.where(flip, -s, s)
    return s * np.sqrt(d)

def _star_pts(cx, cy, r, inner=0.48, rot=0.0):
    return [(cx + (r if k % 2 == 0 else r * inner) * math.sin(rot + k * math.pi / 5),
             cy + (r if k % 2 == 0 else r * inner) * math.cos(rot + k * math.pi / 5)) for k in range(10)]

def _sd_circle(X, Y, cx, cy, r):
    return np.sqrt((X - cx) ** 2 + (Y - cy) ** 2) - r

def _sd_rect(X, Y, cx, cy, hw, hh, r=0.0, rot=0.0):
    x, y = X - cx, Y - cy
    if rot:
        c, s = math.cos(rot), math.sin(rot)
        x, y = c * x + s * y, -s * x + c * y
    qx, qy = np.abs(x) - hw + r, np.abs(y) - hh + r
    return np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r

def _window(U, V, uc, vc, rad):
    """Local coords (x, y) in V units around (uc, vc), plus a slice limiting work to a box."""
    H, W = U.shape
    vv = V[:, 0];
    rows = np.nonzero(np.abs(vv - vc) < rad)[0]
    if len(rows) == 0:
        return None
    r0, r1 = rows.min(), rows.max() + 1
    return slice(r0, r1), _x(U[r0:r1], uc), V[r0:r1] - vc

def _tp(B, t, th, grow=1.0):
    return B.torso_point(t, th, grow)

def _normal(B, t, th, grow=1.0):
    p = _tp(B, t, th, grow)
    a = _tp(B, t, th + 0.02, grow) - _tp(B, t, th - 0.02, grow)
    b = _tp(B, min(1, t + 0.02), th, grow) - _tp(B, max(0, t - 0.02), th, grow)
    n = a.cross(b)
    if n.length < 1e-9:
        n = Vector((p.x, p.y, 0))
    n.normalize()
    if n.dot(Vector((p.x, p.y, 0))) < 0:
        n = -n
    return n

def _mat(B, key, hexcol, rough=0.6, spec=0.35):
    """B.mats.flat, but a second colour under the same key (mismatched shoes) gets its own material."""
    m = B.mats.cache.get(f"{B.mats.prefix}{key}")
    if m is not None:
        want = kit.srgb_to_lin(hex_rgb(hexcol))
        if max(abs(a - b) for a, b in zip(tuple(m.diffuse_color)[:3], want)) > 1e-3:
            key = f"{key}_{hexcol.lstrip('#').lower()}"
    return B.mats.flat(key, hexcol, rough=rough, spec=spec)

def _sole(shoes, default):
    """The shoes' `sole`, unless it is just the core's sneaker default (always merged in)."""
    v = shoes.get("sole")
    return default if (not v or v.upper() == "#F4F4F0") else v

def _ring(c, r, z, ry=None, n=36):
    ry = r if ry is None else ry
    return [(c[0] + r * math.cos(a), c[1] + ry * math.sin(a), z) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]

def _orient(bm, p, n):
    q = Vector((0, 0, 1)).rotation_difference(n)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(p) @ q.to_matrix().to_4x4(), verts=bm.verts)
    return bm

# ================================================================================== patterns
def pat_vstripes(img, U, V, spec, part):
    n = int(spec.get("count", 12 if part == "top" else 8))
    f = (U * n + float(spec.get("offset", 0.0)) * 1.0) % 1.0
    d = (np.abs(f - 0.75) - 0.25) / n * 2.0    # accent on half of each period, V units
    _put(img, d, spec.get("accent", "#1A1A1E"))

def pat_hstripe(img, U, V, spec, part):
    v, w = float(spec.get("v", 0.58)), float(spec.get("width", 0.10))
    _put(img, np.abs(V - v) - w / 2, spec.get("accent", "#F2F2EE"))
    if spec.get("edge"):
        for e in (v - w / 2, v + w / 2):
            _put(img, np.abs(V - e) - w * 0.08, spec["edge"])

def pat_hstripes(img, U, V, spec, part):
    """Even horizontal stripes (a striped tee): `count` accent bands between v0 and v1 (in V)."""
    n = int(spec.get("count", 5))
    v0, v1 = float(spec.get("v0", 0.30 if part == "top" else 0.0)), float(spec.get("v1", 0.92 if part == "top" else 1.0))
    p = (v1 - v0) / n
    w = float(spec.get("width", 0.5)) * p            # band height: a fraction of the period
    f = (V - v0) / p
    c = v0 + (np.floor(f) + 0.5) * p                 # centre of this period's band
    d = np.abs(V - c) - w / 2
    d = np.where((V < v0) | (V > v1), 1.0, d)
    _put(img, d, spec.get("accent", "#F1E7CF"))

def _scatter(n, seed, v0, v1, part):
    """Jittered positions (u, v, r) spread evenly around."""
    rnd = random.Random(seed)
    rows = max(1, int(round(math.sqrt(n / 4.0))))
    cols = max(1, int(math.ceil(n / rows)))
    out = []
    for j in range(rows):
        for i in range(cols):
            u = (i + 0.5 + rnd.uniform(-0.3, 0.3) + (0.5 if j % 2 else 0)) / cols
            v = v0 + (v1 - v0) * (j + 0.5 + rnd.uniform(-0.3, 0.3)) / rows
            out.append((u % 1.0, v, rnd.random(), rnd.random()))
    return out

def pat_vacation(img, U, V, spec, part):
    flower, leaf, centre = spec.get("accent", "#FF6F91"), spec.get("accent2", "#2FA88A"), spec.get("center", "#FFE066")
    sz = float(spec.get("size", 1.0)) * (1.0 if part == "top" else 0.6)
    n = int(spec.get("count", 14 if part == "top" else 10))
    seed = int(spec.get("seed", 7))
    v0, v1 = (0.2, 1.05) if part == "top" else (-0.05, 1.05)
    pts = _scatter(n, seed, v0, v1, part)
    rnd = random.Random(seed + 1)
    rib = shade(leaf, 0.7)
    # leaves first: pairs of pointed leaves fanning out from between the flowers
    for (u, v, a, b) in pts:
        for k in range(2):
            ang = a * 6.28 + k * 2.4
            L = 0.11 * sz * (0.85 + 0.3 * b)
            cu = u + math.cos(ang) * L * 0.9 / 2.0; cv = v + math.sin(ang) * L * 0.9
            w = _window(U, V, cu, cv, L * 1.3)
            if w is None: continue
            sl, X, Y = w
            c, s = math.cos(-ang), math.sin(-ang)
            xr, yr = c * X - s * Y, s * X + c * Y
            r = L * 0.95
            dl = np.maximum(_sd_circle(xr, yr, 0, -r * 0.62, r), _sd_circle(xr, yr, 0, r * 0.62, r))  # vesica leaf
            sub = img[sl]
            _put(sub, dl, leaf)
            _put(sub, np.maximum(np.abs(yr) - 0.0035, np.abs(xr) - L * 0.62), rib)
    for (u, v, a, b) in pts:
        r = 0.075 * sz * (0.8 + 0.4 * b)
        w = _window(U, V, u, v, r * 1.6)
        if w is None: continue
        sl, X, Y = w
        rot = a * 6.28
        np_ = 5 if b < 0.6 else 6
        d = None
        for k in range(np_):
            t = rot + k * 2 * math.pi / np_
            dk = _sd_circle(X, Y, math.cos(t) * r * 0.55, math.sin(t) * r * 0.55, r * 0.46)
            d = dk if d is None else np.minimum(d, dk)
        sub = img[sl]
        _put(sub, d - 0.004, shade(flower, 0.75))      # a darker rim so overlapping petals read
        _put(sub, d, flower)
        _put(sub, _sd_circle(X, Y, 0, 0, r * 0.26), centre)

def pat_stars(img, U, V, spec, part):
    n = int(spec.get("count", 26 if part == "top" else 14))
    sz = float(spec.get("size", 1.0)) * (1.0 if part == "top" else 0.75)
    col = spec.get("accent", "#FFE066")
    v0, v1 = (0.27, 1.0) if part == "top" else (0.0, 1.0)
    for (u, v, a, b) in _scatter(n, int(spec.get("seed", 3)), v0, v1, part):
        r = 0.032 * sz * (0.75 + 0.5 * b)
        w = _window(U, V, u, v, r * 1.3)
        if w is None: continue
        sl, X, Y = w
        _put(img[sl], _sd_poly(X, Y, _star_pts(0, 0, r, 0.5, a * 1.2)) - r * 0.08, col)

def pat_patches(img, U, V, spec, part):
    cols = [spec.get("accent", "#E8A33D"), spec.get("accent2", "#5B8FD6")]
    spots = [(0.42, 0.40, 0.07, 0.06, 0.15), (0.0, 0.62, 0.09, 0.075, -0.1), (0.66, 0.70, 0.06, 0.05, -0.2)]
    if part == "bottoms":
        spots = [(0.5, 0.55, 0.13, 0.11, 0.12), (0.05, 0.3, 0.11, 0.1, -0.15)]
    for k, (u, v, hw, hh, rot) in enumerate(spots[:int(spec.get("count", 3))]):
        col = cols[k % 2]
        w = _window(U, V, u, v, max(hw, hh) * 1.6)
        if w is None: continue
        sl, X, Y = w
        sub = img[sl]
        d = _sd_rect(X, Y, 0, 0, hw, hh, 0.012, rot)
        _put(sub, d - 0.003, shade(col, 0.8))
        _put(sub, d, col)
        # stitches: dashes along an inset outline
        inset = d + 0.012
        c, s = math.cos(rot), math.sin(rot)
        xr, yr = c * X + s * Y, -s * X + c * Y
        dash = np.where(np.abs(xr) / hw > np.abs(yr) / hh, yr, xr) * 90.0
        on = (np.sin(dash) > 0.1)
        sd = np.abs(inset) - 0.0028
        sd = np.where(on, sd, 1.0)
        _put(sub, sd, spec.get("stitch") or shade(col, 0.55))

def pat_emblem(img, U, V, spec, part):
    shape, s = spec.get("shape", "star"), float(spec.get("size", 0.13))
    vc = float(spec.get("v", 0.62))
    col = spec.get("accent", "#FFD23F")
    w = _window(U, V, 0.5, vc, s * 1.5)
    if w is None: return
    sl, X, Y = w
    if shape == "circle":
        d = _sd_circle(X, Y, 0, 0, s)
        di = _sd_circle(X, Y, 0, 0, s * 0.55)
    elif shape == "shield":
        pts = [(-s * 0.85, s * 0.9), (s * 0.85, s * 0.9), (s * 0.85, s * 0.05)]
        for k in range(1, 8):
            a = k / 8 * math.pi / 2
            pts.append((s * 0.85 * math.cos(a), s * 0.05 - s * 1.05 * math.sin(a)))
        pts += [(-x, y) for x, y in reversed(pts[3:])][1:] + [(-s * 0.85, s * 0.05)]
        d = _sd_poly(X, Y, pts) - s * 0.06
        di = _sd_poly(X * 1.8, (Y + s * 0.05) * 1.8, pts) / 1.8 - s * 0.03
    else:
        d = _sd_poly(X, Y, _star_pts(0, -s * 0.06, s * 1.05, 0.48)) - s * 0.08
        di = None
    sub = img[sl]
    _put(sub, d - s * 0.1, spec.get("rim") or shade(col, 0.6))
    _put(sub, d, col)
    if di is not None and spec.get("inner"):
        _put(sub, di, spec["inner"])

def pat_buttons(img, U, V, spec, part):
    rows, n = int(spec.get("rows", 1)), int(spec.get("count", 5))
    col = spec.get("accent", "#2A2F5A")
    base = spec.get("color", "#FFFFFF")
    w = _window(U, V, 0.5, 0.6, 0.45)
    if w is None: return
    sl, X, Y = w
    sub = img[sl]; Yv = Y + 0.6
    if rows == 1:
        _put(sub, np.maximum(np.abs(X) - 0.006, 0.26 - Yv), spec.get("line") or shade(base, 0.78))
        xs = [0.0]
    else:
        _put(sub, np.maximum(np.abs(X - 0.035) - 0.003, 0.26 - Yv), spec.get("line") or shade(base, 0.85))   # wrap edge
        xs = [-0.09, 0.09]
    for k in range(n):
        v = 0.33 + (0.86 - 0.33) * k / max(1, n - 1)
        for x in xs:
            d = _sd_circle(X, Yv, x, v, 0.027)
            _put(sub, d, shade(col, 0.7))
            _put(sub, d + 0.005, col)
            for hx in (-0.005, 0.005):
                _put(sub, _sd_circle(X, Yv, x + hx * 1.3, v, 0.0038), shade(col, 0.55))

def pat_vest(img, U, V, spec, part):
    col = spec.get("accent", "#5A4A8C")
    op = float(spec.get("open", 0.10)) * 2.0
    X = _x(U, 0.5)
    half = op * (0.35 + 0.65 * np.clip((V - 0.35) / 0.55, 0, 1))    # V-neck: narrow at the waist, wide at the neck
    d = half - np.abs(X)
    _put(img, d, spec.get("trim") or shade(col, 0.72))
    _put(img, d + 0.008, col)
    if spec.get("pockets", True):
        for sx in (-1, 1):
            w = _window(U, V, 0.5 + sx * 0.11, 0.42, 0.08)
            if w is None: continue
            sl, Xp, Yp = w
            r = _sd_rect(Xp, Yp, 0, 0, 0.055, 0.035, 0.006)
            _put(img[sl], np.maximum(np.abs(r) - 0.003, 0), shade(col, 0.65))
            _put(img[sl], np.maximum(np.abs(Yp - 0.025) - 0.003, np.abs(Xp) - 0.055), shade(col, 0.65))

def pat_collar(img, U, V, spec, part):
    col = spec.get("accent", "#8A5CC9")
    depth, wd = float(spec.get("depth", 0.34)), float(spec.get("width", 0.07))
    X = _x(U, 0.5)
    vt = 1.0 - depth                    # the point of the V
    k = 0.75                            # opening slope (x per v)
    edge = np.abs(X) - (V - vt) * k     # < 0 inside the V
    if spec.get("inner"):
        _put(img, np.maximum(edge, vt - V), spec["inner"])
    lapel = np.maximum(np.maximum(-edge, edge - wd * 1.6), vt - V)
    band = 0.93 - V                     # a band all round the neck
    d = np.minimum(lapel, np.maximum(band, -edge))
    _put(img, d - 0.004, shade(col, 0.7))
    _put(img, d, col)

def pat_bib(img, U, V, spec, part):
    col = spec.get("accent", "#3E6FB0")
    top, hw = float(spec.get("top", 0.66)), float(spec.get("width", 0.22)) * 0.5 * 2.0
    X = _x(U, 0.5)
    bib = _sd_rect(X, V, 0, (top + 0.15) / 2, hw, (top - 0.15) / 2, 0.02)
    straps = None
    for sx in (-1, 1):
        sxp = sx * hw * 0.7
        fr = np.maximum(np.abs(X - sxp) - 0.035, top - 0.02 - V)
        Xb = _x(U, 0.0)
        bk = np.maximum(np.abs(Xb - sx * 0.12 * (V - 0.45) / 0.55) - 0.035, 0.45 - V)   # crossing on the back
        dd = np.minimum(fr, bk)
        straps = dd if straps is None else np.minimum(straps, dd)
    d = np.minimum(bib, straps)
    _put(img, d - 0.004, shade(col, 0.7))
    _put(img, d, col)
    _put(img, np.maximum(np.abs(_sd_rect(X, V, 0, top - 0.11, hw * 0.45, 0.06, 0.01)) - 0.0025, 0), shade(col, 0.65))  # pocket
    for sx in (-1, 1):
        _put(img, _sd_circle(X, V, sx * hw * 0.7, top - 0.035, 0.018), spec.get("button", "#F2D16B"))

def pat_belly_panel(img, U, V, spec, part):
    X = _x(U, 0.5)
    rx, ry = float(spec.get("width", 0.22)) * 2.0, float(spec.get("height", 0.34))
    vc = float(spec.get("v", 0.42))
    r = np.sqrt((X / rx) ** 2 + ((V - vc) / ry) ** 2)
    d = (r - 1.0) * min(rx, ry)
    soft = float(spec.get("soft", 0.02))
    a = np.clip(0.5 - d / max(soft, 1e-4), 0, 1)[..., None]
    img[:] = img * (1 - a) + _rgb(spec.get("accent", "#FFE38A")) * a

def _dials(img, X, Y, acc, line, lw=0.0045):
    """Marker drawing of dials, buttons and a meter in local front coords (V units, Y = V)."""
    for cx, cy, r, ang in ((-0.13, 0.66, 0.065, 0.7), (0.12, 0.70, 0.05, -0.9)):
        dc = _sd_circle(X, Y, cx, cy, r)
        _put(img, dc, mix_hex(acc, "#FFFFFF", 0.55))
        _put(img, np.abs(dc) - lw, line)
        for k in range(5):   # ticks
            t = math.pi * (0.15 + 0.7 * k / 4)
            ox, oy = math.cos(t), math.sin(t)
            seg = np.maximum(np.abs((X - cx) * oy - (Y - cy) * ox) - lw * 0.6,
                             np.abs((X - cx) * ox + (Y - cy) * oy - r * 0.78) - r * 0.12)
            _put(img, seg, line)
        nx, ny = math.cos(math.pi / 2 - ang), math.sin(math.pi / 2 - ang)
        ndl = np.maximum(np.abs((X - cx) * ny - (Y - cy) * nx) - lw * 0.8,
                         np.abs((X - cx) * nx + (Y - cy) * ny - r * 0.35) - r * 0.4)
        _put(img, ndl, line)
        _put(img, _sd_circle(X, Y, cx, cy, r * 0.12), line)
    for k in range(3):   # a row of round buttons
        db = _sd_circle(X, Y, -0.12 + k * 0.12, 0.52, 0.028)
        _put(img, db, acc if k != 1 else shade(acc, 0.75))
        _put(img, np.abs(db) - lw, line)
    dm = _sd_rect(X, Y, 0.0, 0.40, 0.17, 0.045, 0.01)   # the meter
    _put(img, np.abs(dm) - lw, line)
    for k in range(6):
        bx = -0.135 + k * 0.054
        h = (0.02 + 0.012 * k) if k < 5 else 0.01
        _put(img, _sd_rect(X, Y, bx, 0.40 - 0.03 + h, 0.016, h, 0.002), acc)
    _put(img, np.maximum(np.abs(Y - 0.80) - lw, np.abs(X + 0.02) - 0.06), line)   # a little speaker slot

def pat_dials(img, U, V, spec, part):
    k = float(spec.get("size", 1.35))   # the drawing is made at 1.0 around V 0.58
    w = _window(U, V, 0.5, 0.58, 0.32 * k)
    if w is None: return
    sl, X, Y = w
    _dials(img[sl], X / k, Y / k + 0.58, spec.get("accent", "#FF9F1C"), spec.get("line", "#2A2A33"), lw=0.0045 / k)


# block font (5 x 7), for jersey numbers and names: rows top to bottom
_GLYPHS = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"], "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"], "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"], "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"], "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"], "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"], "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"], "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"], "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"], "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"], "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"], "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"], "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"], "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"], "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"], "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"], "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"], "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"], "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    " ": ["00000"] * 7,
}

def _text_sd(X, Y, text, h, aspect, gap=1.0, bold=1.0):
    """Signed distance (V units) to block text centred at (0, 0), cap height h. Each lit cell of the
    5 x 7 glyph is a box; boxes overlap a little (bold) so strokes join."""
    cell = h / 7.0; cw = cell * aspect
    n = len(text)
    total = n * 5 * cw + (n - 1) * gap * cw
    d = np.full(X.shape, 1e3, np.float32)
    for i, ch in enumerate(text.upper()):
        rows = _GLYPHS.get(ch, _GLYPHS[" "])
        x0 = -total / 2 + i * (5 + gap) * cw
        for r, row in enumerate(rows):
            for c_, bit in enumerate(row):
                if bit == "1":
                    cx = x0 + (c_ + 0.5) * cw; cy = h / 2 - (r + 0.5) * cell
                    d = np.minimum(d, _sd_rect(X, Y, cx, cy, cw * 0.5 * bold, cell * 0.5 * bold))
    return d

def pat_jersey(img, U, V, spec, part):
    acc = spec.get("accent", "#F2B632")
    # collar band and a thin hem-side trim
    _put(img, np.abs(V - 0.955) - 0.022, acc)
    num = str(spec.get("number", "55")); ncol = spec.get("number_color", "#F7F7F5")
    out = spec.get("outline") or acc
    asp = float(spec.get("aspect", 0.62)); sz = float(spec.get("size", 0.36))
    places = []
    if spec.get("front", True):
        places.append((0.5, float(spec.get("v", 0.56))))
    if spec.get("back", True):
        places.append((0.0, float(spec.get("v_back", 0.50))))
    for uc, vc in places:
        w = _window(U, V, uc, vc, sz * 0.75)
        if w is None: continue
        sl, X, Y = w
        d = _text_sd(X, Y, num, sz, asp, gap=1.2, bold=1.04)
        _put(img[sl], d - sz * 0.03, out)
        _put(img[sl], d, ncol)
    if spec.get("text") and spec.get("back", True):
        th = float(spec.get("text_size", 0.065)); tv = float(spec.get("text_v", 0.83))
        w = _window(U, V, 0.0, tv, th * 0.8)
        if w is not None:
            sl, X, Y = w
            d = _text_sd(X, Y, spec["text"], th, asp, gap=1.0, bold=1.04)
            _put(img[sl], d, spec.get("text_color", ncol))

for _n, _f in (("vstripes", pat_vstripes), ("vacation", pat_vacation), ("hstripe", pat_hstripe), ("hstripes", pat_hstripes), ("stars", pat_stars),
               ("patches", pat_patches), ("emblem", pat_emblem), ("buttons", pat_buttons), ("vest", pat_vest),
               ("collar", pat_collar), ("bib", pat_bib), ("belly_panel", pat_belly_panel), ("dials", pat_dials),
               ("jersey", pat_jersey)):
    kit.PATTERNS[_n] = _f

# ===================================================================================== shoes
def _bare_foot(B, s, x, bone, lift, fs):
    sc = 1.25 * fs
    B.add(ellipsoid_bm((x, -0.035, 0.042 + lift), (0.064 * sc, 0.105 * sc, 0.046 * sc), floor=0.004 + lift, segs=28),
          B.skin, bone)
    for tx, tr in ((-0.040, 0.026), (-0.012, 0.023), (0.014, 0.021), (0.036, 0.019)):
        tx, tr = tx * s * -1 * fs, tr * fs
        ty = -0.035 - 0.118 * sc + abs(tx) * 0.35
        B.add(ellipsoid_bm((x + tx, ty, 0.026 + lift * 0.7), (tr, tr * 1.05, tr * 0.95), segs=14, rings=8, floor=0.004 + lift),
              B.skin, bone)
    return sc

def shoe_sandals(B, s, side, ank, shoes):
    bone = f"foot.{side}"; x = ank.x
    fs = float(shoes.get("foot_size", 1.0))
    col = shoes.get("color", "#8B5A2B")
    strap = _mat(B, "sandal_strap", col, rough=0.6, spec=0.3)
    sole = _mat(B, "sandal_sole", shade(col, 0.8), rough=0.7, spec=0.2)
    lift = 0.014
    sc = _bare_foot(B, s, x, bone, lift, fs)
    cy, ry = -0.045 * fs, 0.15 * fs
    B.add(lathe([(0.0, 0, 0, x, cy), (0.0, 0.072 * fs, ry * 0.97, x, cy), (0.004, 0.076 * fs, ry, x, cy),
                 (lift + 0.002, 0.076 * fs, ry, x, cy), (lift + 0.004, 0.071 * fs, ry * 0.96, x, cy),
                 (lift + 0.004, 0, 0, x, cy)], 32, power=2.2), sole, bone)
    fc = Vector((x, -0.035, 0.042 + lift)); fr = Vector((0.064 * sc, 0.105 * sc, 0.046 * sc))
    for y0, w in ((-0.10 * fs, 0.0085), (0.005 * fs, 0.0085)):
        f = math.sqrt(max(0.0, 1 - ((y0 - fc.y) / fr.y) ** 2))
        pts = []
        for a in np.linspace(0, math.pi, 15):
            z = fc.z + fr.z * f * math.sin(a) * 1.04
            pts.append((x + fr.x * f * math.cos(a) * 1.05, y0, max(z, lift + 0.004)))
        pts[0] = (pts[0][0], y0, lift); pts[-1] = (pts[-1][0], y0, lift)
        B.add(tube_bm(pts, w), strap, bone)

def shoe_moon_boots(B, s, side, ank, shoes):
    bone, leg = f"foot.{side}", f"leg.{side}"; x = ank.x
    col = shoes.get("color", "#D9DCE3")
    m = _mat(B, "moon_boot", col, rough=0.75, spec=0.3)
    pad = _mat(B, "moon_boot_pad", shade(col, 0.9), rough=0.8, spec=0.25)
    sole = _mat(B, "moon_boot_sole", _sole(shoes, "#7C808A"), rough=0.7, spec=0.2)
    def puff(co):
        co.x *= 1 + 0.04 * math.cos(co.y * 60); return co
    B.add(ellipsoid_bm((x, -0.03, 0.072), (0.082, 0.128, 0.064), floor=0.034, deform=puff, segs=32), m, bone)
    B.add(lathe([(0.0, 0, 0, x, -0.03), (0.0, 0.08, 0.124, x, -0.03), (0.006, 0.088, 0.134, x, -0.03),
                 (0.032, 0.088, 0.134, x, -0.03), (0.04, 0.08, 0.124, x, -0.03), (0.04, 0, 0, x, -0.03)], 36, power=2.4),
          sole, bone)
    top = 0.21
    rings = [(0.06, 0, 0, x, 0.012)]
    for k in range(9):
        t = k / 8; z = 0.06 + (top - 0.06) * t
        r = 0.074 + 0.006 * math.sin(t * math.pi)
        rings.append((z, r, r * 0.96, x, 0.012))
    rings.append((top, 0.0, 0.0, x, 0.012))
    B.add(lathe(rings, 32), m, leg)
    n = int(shoes.get("rings", 2))
    for k in range(n):
        z = top - 0.012 - k * 0.07
        B.add(tube_bm(_ring((x, 0.012), 0.078, z, 0.075), 0.016, cyclic=True), pad, leg)

def shoe_rain_boots(B, s, side, ank, shoes):
    bone, leg = f"foot.{side}", f"leg.{side}"; x = ank.x
    col = shoes.get("color", "#FFD23F")
    m = _mat(B, "rain_boot", col, rough=0.25, spec=0.6)
    sole = _mat(B, "rain_boot_sole", _sole(shoes, "#2A2A33"), rough=0.7, spec=0.2)
    B.add(ellipsoid_bm((x, -0.034, 0.052), (0.064, 0.114, 0.05), floor=0.02, segs=30), m, bone)
    B.add(ellipsoid_bm((x, -0.036, 0.02), (0.067, 0.118, 0.02), floor=0.0, segs=30), sole, bone)
    top = float(shoes.get("height", 0.20))
    rings = [(0.035, 0, 0, x, 0.006)]
    for k in range(7):
        t = k / 6; z = 0.035 + (top - 0.035) * t
        r = 0.061 + 0.008 * t ** 2
        rings.append((z, r, r * 0.95, x, 0.006))
    rings += [(top, 0.058, 0.055, x, 0.006), (top - 0.01, 0.054, 0.051, x, 0.006), (top - 0.01, 0, 0, x, 0.006)]
    B.add(lathe(rings, 32), m, leg)
    B.add(tube_bm(_ring((x, 0.006), 0.065, top - 0.002, 0.062), 0.006, cyclic=True), m, leg)

def shoe_clogs(B, s, side, ank, shoes):
    bone = f"foot.{side}"; x = ank.x
    col = shoes.get("color", "#4FB3A9")
    m = _mat(B, "clog", col, rough=0.45, spec=0.4)
    sole = _mat(B, "clog_sole", _sole(shoes, shade(col, 0.72)), rough=0.6, spec=0.3)
    dark = _mat(B, "clog_hole", shade(col, 0.55), rough=0.7, spec=0.2)
    # heel/sock showing through the open back
    B.add(ellipsoid_bm((x, 0.025, 0.05), (0.046, 0.05, 0.04), floor=0.02, segs=22, rings=12), B.skin, bone)
    def open_back(co):
        if co.y > -0.02:   # the back half is cut down to a low rim
            k = min(1.0, (co.y + 0.02) / 0.05)
            co.z = min(co.z, 0.058 * (1 - k) - 0.012 * k)
        return co
    c = Vector((x, -0.04, 0.03))
    B.add(ellipsoid_bm(c, (0.07, 0.112, 0.062), floor=0.016, deform=open_back, segs=32, rings=18), m, bone)
    B.add(lathe([(0.0, 0, 0, x, -0.035), (0.0, 0.068, 0.118, x, -0.035), (0.02, 0.072, 0.122, x, -0.035),
                 (0.02, 0, 0, x, -0.035)], 32, power=2.4), sole, bone)
    for hx, hy in ((-0.022, -0.1), (0.0, -0.11), (0.022, -0.1), (-0.012, -0.075), (0.012, -0.075)):   # vent holes on top
        yy = c.y + hy + 0.04
        f = max(0.0, 1 - ((hy + 0.0) / 0.112) ** 2 - (hx / 0.07) ** 2)
        zz = c.z + 0.062 * math.sqrt(f)
        B.add(ellipsoid_bm((x + hx, yy, zz - 0.003), (0.0075, 0.0075, 0.005), segs=12, rings=6), dark, bone)
    if shoes.get("strap", True):
        pts = [(x + 0.07 * math.cos(a), 0.0 + 0.055 * math.sin(a), 0.045) for a in np.linspace(0, math.pi, 13)]
        B.add(tube_bm(pts, 0.007), m, bone)

def shoe_slippers(B, s, side, ank, shoes):
    bone = f"foot.{side}"; x = ank.x
    col = shoes.get("color", "#F2B8C6")
    m = _mat(B, "slipper", col, rough=1.0, spec=0.1)
    def lumpy(co):
        a = math.atan2(co.y, co.x)
        k = 1 + 0.05 * math.sin(a * 7 + co.z * 90) + 0.03 * math.sin(co.y * 140)
        co.x *= k; co.z *= 1 + 0.04 * math.sin(co.y * 110 + co.x * 60); return co
    B.add(ellipsoid_bm((x, -0.035, 0.052), (0.074, 0.118, 0.056), floor=0.006, deform=lumpy, segs=36, rings=18), m, bone)
    B.add(ellipsoid_bm((x, 0.012, 0.086), (0.064, 0.06, 0.026), deform=lumpy, segs=28, rings=12), m, bone)   # fuzzy cuff
    B.add(ellipsoid_bm((x, -0.095, 0.098), (0.026, 0.024, 0.022), deform=lumpy, segs=18, rings=10), m, bone)  # a pom on the toe

def shoe_dress(B, s, side, ank, shoes):
    bone = f"foot.{side}"; x = ank.x
    col = shoes.get("color", "#2A2A33")
    m = _mat(B, "dress_shoe", col, rough=0.15, spec=0.7)
    sole = _mat(B, "dress_sole", _sole(shoes, shade(col, 0.6)), rough=0.5, spec=0.3)
    def toe(co):
        if co.y < 0:
            f = (-co.y / 0.105) ** 2
            co.z *= 1 - 0.25 * f
        return co
    B.add(ellipsoid_bm((x, -0.03, 0.05), (0.058, 0.104, 0.045), floor=0.016, deform=toe, segs=30), m, bone)
    B.add(ellipsoid_bm((x, -0.04, 0.012), (0.06, 0.106, 0.008), segs=30, rings=10), sole, bone)
    B.add(lathe([(0.0, 0, 0, x, 0.045), (0.0, 0.034, 0.024, x, 0.045), (0.022, 0.036, 0.026, x, 0.045),
                 (0.022, 0, 0, x, 0.045)], 24, power=3.0), sole, bone)

def shoe_footies(B, s, side, ank, shoes):
    bone, leg = f"foot.{side}", f"leg.{side}"; x = ank.x
    m = _mat(B, "footie", shoes.get("color", "#8FB8E8"), rough=0.85, spec=0.2)
    B.add(ellipsoid_bm((x, -0.032, 0.05), (0.07, 0.112, 0.056), floor=0.004, segs=30), m, bone)
    B.add(capsule_bm((x, 0.0, 0.07), (x, 0.0, 0.14), B.leg_r * 1.15 if hasattr(B, "leg_r") else 0.054, 0.052,
                     segs=24, hem=4), m, leg)

def shoe_wrestling_boots(B, s, side, ank, shoes):
    bone, leg = f"foot.{side}", f"leg.{side}"; x = ank.x
    col = shoes.get("color", "#2A3A8C")
    m = _mat(B, "wrestling_boot", col, rough=0.35, spec=0.5)
    lace = _mat(B, "wrestling_lace", shoes.get("lace", "#F7F7F5"), rough=0.6, spec=0.3)
    sole = _mat(B, "wrestling_sole", _sole(shoes, shade(col, 0.55)), rough=0.6, spec=0.3)
    B.add(ellipsoid_bm((x, -0.03, 0.052), (0.06, 0.106, 0.05), floor=0.014, segs=30), m, bone)
    B.add(ellipsoid_bm((x, -0.032, 0.016), (0.063, 0.11, 0.016), floor=0.0, segs=30), sole, bone)
    top = float(shoes.get("height", 0.235))
    r0 = 0.058
    rings = [(0.035, 0, 0, x, 0.0)]
    for k in range(7):
        t = k / 6; z = 0.035 + (top - 0.035) * t
        r = r0 + 0.004 * math.sin(t * math.pi)
        rings.append((z, r, r * 0.96, x, 0.0))
    rings.append((top, 0, 0, x, 0.0))
    B.add(lathe(rings, 32), m, leg)
    B.add(tube_bm(_ring((x, 0.0), r0 + 0.002, top - 0.006, (r0 + 0.002) * 0.96), 0.007, cyclic=True), lace, leg)
    ry = -(r0 * 0.96) - 0.002
    n = 6
    z0, z1 = 0.07, top - 0.025
    for k in range(n):   # criss-cross laces down the front
        za, zb = z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n
        for d in (-1, 1):
            B.add(tube_bm([(x - d * 0.014, ry, za), (x, ry - 0.002, (za + zb) / 2), (x + d * 0.014, ry, zb)], 0.0035), lace, leg)
    B.add(tube_bm([(x, -0.104, 0.06), (x, -0.07, 0.088), (x, ry, z0)], 0.0035), lace, bone)

def shoe_chunky_boots(B, s, side, ank, shoes):
    bone, leg = f"foot.{side}", f"leg.{side}"; x = ank.x
    col = shoes.get("color", "#8B5A2B")
    m = _mat(B, "chunky_boot", col, rough=0.65, spec=0.3)
    cap = _mat(B, "chunky_cap", shoes.get("cap") or shade(col, 0.78), rough=0.55, spec=0.35)
    sole = _mat(B, "chunky_sole", _sole(shoes, "#3A3330"), rough=0.75, spec=0.2)
    B.add(ellipsoid_bm((x, -0.028, 0.066), (0.074, 0.118, 0.056), floor=0.036, segs=32), m, bone)
    B.add(ellipsoid_bm((x, -0.088, 0.058), (0.07, 0.065, 0.046), floor=0.037, segs=28, rings=14), cap, bone)
    B.add(lathe([(0.0, 0, 0, x, -0.03), (0.0, 0.074, 0.122, x, -0.03), (0.004, 0.08, 0.13, x, -0.03),
                 (0.036, 0.08, 0.13, x, -0.03), (0.042, 0.074, 0.124, x, -0.03), (0.042, 0, 0, x, -0.03)], 36, power=3.0),
          sole, bone)
    top = 0.16
    B.add(lathe([(0.05, 0, 0, x, 0.006), (0.05, 0.064, 0.062, x, 0.006), (top, 0.068, 0.065, x, 0.006),
                 (top, 0, 0, x, 0.006)], 32), m, leg)
    B.add(tube_bm(_ring((x, 0.006), 0.07, top - 0.004, 0.067), 0.012, cyclic=True), cap, leg)   # padded collar
    for k in range(3):   # lace hooks line
        z = 0.08 + k * 0.025
        B.add(ellipsoid_bm((x, -0.066 + 0.0, z), (0.02, 0.006, 0.004), segs=12, rings=6), sole, leg)


def shoe_high_tops(B, s, side, ank, shoes):
    """Basketball high-tops: a sneaker foot with a padded shaft rising above the ankle, a coloured
    side panel, collar and heel stripe, a thick white sole and criss-cross laces. No logos."""
    bone, leg = f"foot.{side}", f"leg.{side}"; x = ank.x
    sfx = shoes.get("_side", "")
    up = _mat(B, "hightop" + sfx, shoes.get("color", "#1A1A1E"), rough=0.45, spec=0.4)
    acc = _mat(B, "hightop_accent", shoes.get("accent", "#2A6FD6"), rough=0.45, spec=0.4)
    sole = _mat(B, "hightop_sole", _sole(shoes, "#F7F7F5"), rough=0.6, spec=0.3)
    lace = _mat(B, "hightop_lace", shoes.get("lace", "#F7F7F5"), rough=0.6, spec=0.3)
    B.add(ellipsoid_bm((x, -0.03, 0.058), (0.066, 0.112, 0.054), floor=0.026, segs=32), up, bone)
    B.add(lathe([(0.0, 0, 0, x, -0.03), (0.0, 0.066, 0.114, x, -0.03), (0.004, 0.071, 0.121, x, -0.03),
                 (0.028, 0.071, 0.121, x, -0.03), (0.033, 0.066, 0.115, x, -0.03), (0.033, 0, 0, x, -0.03)], 36, power=2.6),
          sole, bone)
    B.add(ellipsoid_bm((x, -0.112, 0.042), (0.05, 0.04, 0.03), floor=0.028, segs=24, rings=10), sole, bone)   # toe bumper
    for d in (-1, 1):      # side panels: a swept blue patch on both sides of the upper
        B.add(ellipsoid_bm((x + d * 0.052, -0.005, 0.07), (0.018, 0.07, 0.026),
                           rot=Matrix.Rotation(d * 0.0, 3, "Z") @ Matrix.Rotation(-0.35, 3, "X"), segs=20, rings=10), acc, bone)
    top = float(shoes.get("height", 0.15))
    r0 = 0.06
    rings = [(0.05, 0, 0, x, 0.004)]
    for k in range(6):
        t = k / 5; z = 0.05 + (top - 0.05) * t
        r = r0 + 0.004 * math.sin(t * math.pi)
        rings.append((z, r, r * 0.97, x, 0.004))
    rings.append((top, 0, 0, x, 0.004))
    B.add(lathe(rings, 32), up, leg)
    B.add(tube_bm(_ring((x, 0.004), r0 + 0.003, top - 0.006, (r0 + 0.003) * 0.97), 0.011, cyclic=True), acc, leg)   # padded collar
    B.add(tube_bm([(x, r0 * 0.97 + 0.006, 0.05), (x, r0 * 0.97 + 0.009, top - 0.02)], 0.009), acc, leg)            # heel stripe
    ry = -(r0 * 0.97) - 0.002
    n = 4
    z0, z1 = 0.075, top - 0.03
    for k in range(n):
        za, zb = z0 + (z1 - z0) * k / n, z0 + (z1 - z0) * (k + 1) / n
        for d in (-1, 1):
            B.add(tube_bm([(x - d * 0.016, ry, za), (x, ry - 0.003, (za + zb) / 2), (x + d * 0.016, ry, zb)], 0.0045), lace, leg)
    B.add(tube_bm([(x, -0.108, 0.07), (x, -0.075, 0.098), (x, ry, z0)], 0.0045), lace, bone)
    B.add(ellipsoid_bm((x, ry - 0.004, top - 0.02), (0.02, 0.008, 0.024), segs=14, rings=8), up, leg)                # tongue tab

for _n, _f in (("sandals", shoe_sandals), ("moon_boots", shoe_moon_boots), ("rain_boots", shoe_rain_boots),
               ("clogs", shoe_clogs), ("slippers", shoe_slippers), ("dress", shoe_dress), ("footies", shoe_footies),
               ("wrestling_boots", shoe_wrestling_boots), ("chunky_boots", shoe_chunky_boots), ("high_tops", shoe_high_tops)):
    kit.SHOES[_n] = _f

# ==================================================================================== costume
def whistle_cord(B, piece):
    yel = B.mats.flat("whistle", piece.get("color", "#FFD23F"), rough=0.3, spec=0.6)
    cord = B.mats.flat("whistle_cord", piece.get("cord", "#2A6FD6"), rough=0.7, spec=0.2)
    tw_ = float(piece.get("t", 0.56)); off = float(piece.get("x", 0.0))
    front = -math.pi / 2
    tn = 0.955
    g = 1.03
    # round the back of the neck
    loop = [_tp(B, tn, front + 0.55 + (2 * math.pi - 1.1) * k / 20, g) for k in range(21)]
    def down(th0):
        return [_tp(B, tn + (tw_ + 0.03 - tn) * (k / 10) ** 0.9, th0 + (front + off - th0) * (k / 10), g) for k in range(1, 11)]
    left = down(front + 0.55)
    right = down(front - 0.55)
    pts = list(reversed(left)) + loop + right
    B.add(tube_bm([tuple(p) for p in pts], 0.0042), cord, "spine")
    p = _tp(B, tw_, front + off, 1.0)
    n = _normal(B, tw_, front + off)
    sz = float(piece.get("size", 1.0))              # 1.0 = the original whistle
    p = p + n * 0.02 * sz
    # whistle: a short barrel pointing sideways-down with a round chamber
    side = Vector((1, 0, 0)) - n * n.x
    side.normalize()
    a = p + (side * 0.03 + Vector((0, 0, -0.004))) * sz; b = p - side * 0.012 * sz
    B.add(capsule_bm(tuple(a), tuple(b), 0.012 * sz, 0.014 * sz, segs=16, hem=4), yel, "spine")
    B.add(ellipsoid_bm(p + (-side * 0.012 + Vector((0, 0, -0.004))) * sz, (0.021 * sz, 0.019 * sz, 0.021 * sz), segs=18, rings=10), yel, "spine")
    B.add(tube_bm([tuple(pts[0]), tuple(p + Vector((0, 0, 0.012 * sz)))], 0.0042), cord, "spine")
    hole = B.mats.flat("whistle_hole", "#2A2A33", rough=0.6, spec=0.2)
    B.add(ellipsoid_bm(a + side * 0.011 * sz, (0.004 * sz, 0.008 * sz, 0.006 * sz), segs=10, rings=6), hole, "spine")

def sash(B, piece):
    mat = B.mats.flat("sash", piece.get("color", "#C8A2F0"), rough=0.7, spec=0.25)
    s = 1 if piece.get("side", "L") == "L" else -1
    peak = 0.0 if s > 0 else math.pi
    hw = float(piece.get("width", 0.17)) / 2
    def fn(u, v):
        th = 2 * math.pi * u
        t = 0.60 + 0.34 * math.cos(th - peak) + (v - 0.5) * 2 * hw
        return tuple(_tp(B, min(0.985, t), th, 1.03 + 0.03 * max(0, t - 0.85) / 0.15))
    B.add(solidify_bm(grid_bm(fn, 72, 4, closed_u=True), 0.007), mat, "spine")

def cape(B, piece):
    L = B.L
    B.cur_part = "cape"
    mat = B.mats.flat("cape", piece.get("color", "#7A2E8C"), rough=0.7, spec=0.25)
    trim = B.mats.flat("cape_trim", piece.get("trim", "#F2D16B"), rough=0.5, spec=0.35)
    z_top = L["torso_z0"] + (L["torso_z1"] - L["torso_z0"]) * 0.9
    knee = (L["hip_z"] + L["ankle_z"]) / 2
    z_bot = z_top + (knee - z_top) * float(piece.get("length", 1.0))
    flare = float(piece.get("flare", 0.3))
    t_of = lambda z: (z - L["torso_z0"]) / (L["torso_z1"] - L["torso_z0"])
    th0, th1 = 0.22, math.pi - 0.22
    def fn(u, v):
        th = th0 + (th1 - th0) * u
        z = z_top + (z_bot - z_top) * v
        t = max(0.05, min(0.9, t_of(z)))
        best = None
        for k in range(10):   # hang from the fullest part above this height
            tt = t + (0.9 - t) * k / 9
            q = _tp(B, tt, th, 1.06)
            if best is None or q.y > best.y:
                best = q
        xs = max(abs(_tp(B, tt, th, 1.06).x) for tt in np.linspace(t, 0.9, 6))
        x = math.copysign(xs, best.x) * (1 + flare * v ** 1.3)
        y = best.y + 0.012 + 0.03 * v
        return (x, y, z)
    nu, nv = 20, 18
    B.add(solidify_bm(grid_bm(fn, nu, nv), 0.008), mat, "spine")
    hem = [Vector(fn(u, 1.0)) + Vector((0, 0.004, 0.006)) for u in np.linspace(0, 1, 21)]
    B.add(tube_bm([tuple(p) for p in hem], 0.008), trim, "spine")
    for u in (0.0, 1.0):
        sd = [Vector(fn(u, v)) for v in np.linspace(0, 1, 12)]
        B.add(tube_bm([tuple(p) for p in sd], 0.006), trim, "spine")
    top = [_tp(B, 0.9, th, 1.08) for th in np.linspace(th0 - 0.15, th1 + 0.15, 17)]
    B.add(tube_bm([tuple(p) for p in top], 0.011), trim, "spine")
    for th in (th0 - 0.15, th1 + 0.15):   # clasp buttons where it ties on at the front of the shoulders
        p = _tp(B, 0.9, th, 1.08)
        B.add(ellipsoid_bm(p, (0.016, 0.016, 0.016), segs=14, rings=8), trim, "spine")

def back_spikes(B, piece):
    mat = B.mats.flat("back_spikes", piece.get("color", "#2FA88A"), rough=0.6, spec=0.3)
    n = int(piece.get("count", 5)); sz = float(piece.get("size", 1.0))
    for k in range(n):
        t = 0.2 + 0.72 * (k / max(1, n - 1))
        f = 0.75 + 0.35 * math.sin(math.pi * (k + 0.5) / n)
        h, r = 0.055 * sz * f, 0.03 * sz * f
        p = _tp(B, t, math.pi / 2, 1.0)
        nrm = (_normal(B, t, math.pi / 2) + Vector((0, 0, 0.35))).normalized()
        rings = [(-0.012, 0, 0, 0, 0), (-0.012, r, r * 0.8, 0, 0)]
        for j in range(1, 8):
            q = j / 8
            rings.append((h * q, r * (1 - q) ** 1.2 + 0.006 * q, (r * (1 - q) ** 1.2 + 0.006 * q) * 0.8, 0, 0))
        rings += [(h + 0.004, 0.004, 0.0035, 0, 0), (h + 0.006, 0, 0, 0, 0)]
        B.add(_orient(lathe(rings, 20), p, nrm), mat, "spine")

def dino_tail(B, piece):
    L = B.L
    B.cur_part = "tail"
    col = piece.get("color", "#5FB85A")
    mat = B.mats.flat("dino_tail", col, rough=0.6, spec=0.3)
    ln = float(piece.get("length", 1.0))
    base = _tp(B, 0.2, math.pi / 2, 0.75)
    pts, radii = [], []
    n = 10
    for k in range(n + 1):
        t = k / n
        pts.append((0.0, base.y + 0.30 * ln * t, base.z - (0.20 * t ** 1.5) * ln + 0.01 * math.sin(t * math.pi)))
        radii.append(0.075 * (1 - t) ** 0.9 + 0.012)
    B.add(tube_bm(pts, 1.0, radii=radii), mat, "spine")
    B.add(ellipsoid_bm(pts[-1], (0.012, 0.012, 0.012), segs=12, rings=8), mat, "spine")
    B.add(ellipsoid_bm(tuple(base), (0.07, 0.05, 0.075), segs=20, rings=10), mat, "spine")
    if piece.get("spikes"):
        sp = B.mats.flat("dino_tail_spikes", piece["spikes"], rough=0.6, spec=0.3)
        for k in (1, 3, 5, 7):
            p = Vector(pts[k]); r = radii[k]
            h = 0.028 + 0.012 * (1 - k / n)
            rings = [(-0.01, 0, 0, 0, 0), (-0.01, 0.018, 0.014, 0, 0)] + \
                    [(h * q, 0.018 * (1 - q) + 0.003, (0.018 * (1 - q) + 0.003) * 0.8, 0, 0) for q in (0.3, 0.6, 0.9)] + [(h, 0, 0, 0, 0)]
            B.add(_orient(lathe(rings, 14), p + Vector((0, 0, r * 0.92)), Vector((0, 0.25, 1)).normalized()), sp, "spine")

def box_torso(B, piece):
    L = B.L
    col = piece.get("color", "#C49A6C")
    hw = max(abs(_tp(B, t, 0.0).x) for t in np.linspace(0.05, 0.95, 19)) * 1.10 + 0.01
    hd = max(abs(_tp(B, t, th).y) for t in np.linspace(0.05, 0.95, 19) for th in (-math.pi / 2, math.pi / 2)) * 1.10 + 0.012
    yc = sum(_tp(B, t, th).y for t in (0.3, 0.6) for th in (-math.pi / 2, math.pi / 2)) / 4
    zb, zt = L["hip_z"] - 0.03, L["shoulder_z"] + 0.035
    cz, hh = (zb + zt) / 2, (zt - zb) / 2
    W, H = 512, 512
    u = (np.arange(W) + 0.5) / W; v = (np.arange(H) + 0.5) / H
    X, Y = np.meshgrid(u, v[::-1])
    img = np.empty((H, W, 3), np.float32); img[:] = hex_rgb(col)
    # faint cardboard fluting, then the marker drawing in front coords (x across the face, y up, V-like units)
    img *= (1 - 0.025 * (np.sin(Y * 260) > 0.6))[..., None]
    sx = 2 * hw / (2 * hh)   # keep marker circles round on the face
    FX, FY = (X - 0.5) * sx * 0.62, Y * 0.62 + 0.29
    _dials(img, FX, FY, piece.get("accent", "#FF9F1C"), piece.get("line", "#3A2A1E"), lw=0.006)
    img[(X < 0.04) & (Y < 0.04)] = hex_rgb(col)
    img[:20, :20] = hex_rgb(col)
    timg = kit.np_to_image(f"{B.mats.prefix}box_torso", img)
    mat = B.mats.tex("box_torso", timg, rough=0.85, spec=0.15)
    bm = rbox((0, yc, cz), hw, hd, hh, power=7)
    def uv_fn(bm_, uv):
        for f in bm_.faces:
            front = f.normal.y < -0.6
            for lp in f.loops:
                co = lp.vert.co
                lp[uv].uv = ((0.5 + co.x / (2 * hw), (co.z - zb) / (zt - zb)) if front else (0.995, 0.995))
    B.add(bm, mat, "spine", uv_fn)
    flap = B.mats.flat("box_flap", shade(col, 0.85), rough=0.85, spec=0.15)
    for sx_ in (-1, 1):   # top flaps folded out a little
        B.add(rbox((sx_ * hw * 0.98, yc, zt - 0.004), 0.004, hd * 0.92, 0.01, power=6, segs=16), flap, "spine")

def rbox(c, hw, hd, hh, power=8, segs=40):
    cx, cy, cz = c
    k = 0.86
    return lathe([(cz - hh, 0, 0, cx, cy), (cz - hh, hw * k, hd * k, cx, cy), (cz - hh * 0.96, hw * 0.98, hd * 0.98, cx, cy),
                  (cz - hh * 0.9, hw, hd, cx, cy), (cz + hh * 0.9, hw, hd, cx, cy), (cz + hh * 0.96, hw * 0.98, hd * 0.98, cx, cy),
                  (cz + hh, hw * k, hd * k, cx, cy), (cz + hh, 0, 0, cx, cy)], segs, power)

def hose_arms(B, piece):
    col = piece.get("color", "#B8BCC4")
    mat = B.mats.flat("hose", col, rough=0.3, spec=0.6)
    inner = B.mats.flat("hose_inner", shade(col, 0.8), rough=0.4, spec=0.5)
    ar = 0.04 * B.L["limb"]
    n = int(piece.get("rings", 9))
    for side in ("L", "R"):
        sh, wr = B.arm_pts[side]
        d = (wr - sh).normalized()
        bone = f"arm.{side}"
        B.add(capsule_bm(tuple(sh), tuple(wr - d * 0.004), ar * 1.22, ar * 1.14, segs=24, hem=4), inner, bone)
        q = Vector((0, 0, 1)).rotation_difference(d).to_matrix().to_4x4()
        for k in range(n):
            t = 0.06 + 0.9 * k / (n - 1)
            p = sh + (wr - sh) * t
            r = ar * (1.28 - 0.08 * t)
            ring = tube_bm([(r * math.cos(a), r * math.sin(a), 0) for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)],
                           0.0105, cyclic=True)
            bmesh.ops.transform(ring, matrix=Matrix.Translation(p) @ q, verts=ring.verts)
            B.add(ring, mat, bone)

def long_skirt(B, piece):
    L = B.L
    col = piece.get("color", "#6A5ACD")
    mat = B.mats.flat("long_skirt", col, rough=0.75, spec=0.2)
    hem_m = B.mats.flat("long_skirt_hem", shade(col, 0.8), rough=0.75, spec=0.2)
    t_top = 0.30
    top_z = L["torso_z0"] + (L["torso_z1"] - L["torso_z0"]) * t_top
    rx0 = abs(_tp(B, t_top, 0.0, 1.03).x); ry0 = abs(_tp(B, t_top, -math.pi / 2, 1.03).y)
    ryb = abs(_tp(B, t_top, math.pi / 2, 1.03).y)
    ln = float(piece.get("length", 1.0))
    hip_bot = L["hip_z"] - 0.06
    z_bot = hip_bot + ((L["ankle_z"] + 0.015) - hip_bot) * ln
    leg_r = getattr(B, "leg_r", 0.047 * L["limb"])
    rxb = max(rx0 * 1.05, (L["ank_x"] + leg_r * 1.7) * (0.9 + 0.35 * ln)) * (1 + 0.28 * ln * float(piece.get("flare", 1.0)))
    ry_b = max(ry0 * 1.05, rxb * 0.8)
    rings = []   # bottom (open hem) up to the waist, closed at the top inside the body
    n = 12
    for k in range(n, -1, -1):
        t = k / n
        z = top_z + (z_bot - top_z) * t
        e = t ** 1.25
        rings.append((z, rx0 + (rxb - rx0) * e, ry0 + (ry_b - ry0) * e, 0, (ryb - ry0) / 2 * (1 - e)))
    rings.append((top_z + 0.012, 0, 0, 0, 0))
    bm = lathe(rings, 48)
    B.add(bm, mat, "spine")
    B.add(tube_bm(_ring((0, 0), rxb, z_bot + 0.004, ry_b, 56), 0.008, cyclic=True), hem_m, "spine")
    B.add(tube_bm(_ring((0, (ryb - ry0) / 2), rx0, top_z, ry0 * 0.5 + ryb * 0.5, 48), 0.009, cyclic=True), hem_m, "spine")
    if piece.get("mud"):
        mud = B.mats.flat("mud", piece["mud"], rough=1.0, spec=0.05)
        knee = (L["hip_z"] + L["ankle_z"]) / 2
        for s, side in ((1, "L"), (-1, "R")):
            if z_bot < knee - 0.02:   # on the skirt front over the knees
                tk = (knee - top_z) / (z_bot - top_z)
                e = tk ** 1.25
                rx = rx0 + (rxb - rx0) * e; ry = ry0 + (ry_b - ry0) * e
                a = -math.pi / 2 + s * 0.45
                p = Vector((rx * math.cos(a), ry * math.sin(a), knee))
                nrm = Vector((math.cos(a) / rx, math.sin(a) / ry, 0)).normalized()
                bone = "spine"
            else:
                p = Vector((s * L["hip_x"], -leg_r * 0.95, knee)); nrm = Vector((0, -1, 0)); bone = f"leg.{side}"
            rot = Vector((0, 1, 0)).rotation_difference(-nrm).to_matrix()
            B.add(ellipsoid_bm(p - nrm * 0.002, (0.03, 0.0035, 0.022), rot=rot, segs=16, rings=8), mud, bone)
            B.add(ellipsoid_bm(p - nrm * 0.002 + Vector((s * 0.018, 0, -0.016)), (0.014, 0.003, 0.011), rot=rot, segs=12, rings=6), mud, bone)


def shoulder_pads(B, piece):
    """Football shoulder pads under the shirt: a broad padded yoke over both shoulders (top colour),
    on the spine bone so the arms swing out from under them. Optional sleeve stripes and hem on the
    short sleeves (arm bones)."""
    L = B.L
    top = B.P["outfit"]["top"]
    col = piece.get("color") or top.get("sleeve", top["color"])
    m = B.mats.flat("shoulder_pads", col, rough=0.75, spec=0.25)
    k = float(piece.get("size", 1.0))
    tw, limb = L["tw"], L["limb"]
    ar = 0.04 * limb
    for sgn in (1, -1):
        sh = Vector((sgn * tw * 0.92, 0, L["shoulder_z"]))
        c = Vector((sgn * tw * 0.80, 0.0, L["shoulder_z"] + 0.028 * k))
        rot = Matrix.Rotation(-sgn * 0.42, 3, "Y")
        B.add(ellipsoid_bm(c, (0.078 * k * limb, 0.088 * k * limb, 0.040 * k), rot=rot, segs=28, rings=14), m, "spine")
        B.add(ellipsoid_bm(c + Vector((sgn * 0.03 * k, 0, -0.022 * k)), (0.05 * k * limb, 0.074 * k * limb, 0.045 * k),
                           rot=rot, segs=24, rings=12), m, "spine")
    # the yoke between the pads, low enough to stay under the chin
    B.add(ellipsoid_bm((0, 0, L["shoulder_z"] + 0.02 * k), (tw * 0.80, 0.075 * k * limb, 0.034 * k), segs=32, rings=12), m, "spine")
    for side, sgn in (("L", 1), ("R", -1)):
        sh, wr = B.arm_pts[side]
        d = (wr - sh); dn = d.normalized()
        def ring_at(t, r, w, mat):
            p = sh + d * t
            pts = []
            a1 = dn.orthogonal().normalized(); a2 = dn.cross(a1)
            for a in np.linspace(0, 2 * math.pi, 28, endpoint=False):
                pts.append(tuple(p + (a1 * math.cos(a) + a2 * math.sin(a)) * r))
            B.add(tube_bm(pts, w, cyclic=True), mat, f"arm.{side}")
        if piece.get("stripes"):
            sm = B.mats.flat("sleeve_stripe", piece["stripes"], rough=0.75, spec=0.25)
            for t in (0.25, 0.32):
                ring_at(t, ar * 1.19, 0.0045, sm)
        if piece.get("hem"):
            hm = B.mats.flat("sleeve_hem", piece["hem"], rough=0.75, spec=0.25)
            ring_at(0.41, ar * 1.16, 0.005, hm)

for _n, _f in (("whistle_cord", whistle_cord), ("sash", sash), ("cape", cape), ("back_spikes", back_spikes),
               ("dino_tail", dino_tail), ("box_torso", box_torso), ("hose_arms", hose_arms), ("long_skirt", long_skirt),
               ("shoulder_pads", shoulder_pads)):
    kit.COSTUME[_n] = _f
