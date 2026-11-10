"""Kit v2 headwear and head accessories for the standard Jarling body.

All sizes are multiples of the head radius R, so every piece fits every head size and shape.
Colours default to neutral toy colours (never the player colours). `separate`: true puts a hat on
the detachable `<id>_hat` object instead of the body (all hats except the hoods/fishbowl/box).

Headwear (`headwear.type`):
  animal_hood  color="#2BB3A3", opening_deg=52, inner=<color darker>, eyes=None {"color": "#FFFFFF", "pupil": "#1B1B20", "size": 1.0}, teeth=None (colour), spikes=None (colour), spike_n=6, ears=None (colour); hair hide
  fishbowl     tint="#CFE8FF", alpha=0.12, scale=1.0, collar="#F4F4F0", highlight=True; hair free
"""
import math
import bmesh
import numpy as np
from mathutils import Vector, Euler, Matrix
import jarling_kit as kit
from jarling_kit import lathe, ellipsoid_bm, capsule_bm, tube_bm, grid_bm, solidify_bm, cap_shell_bm, shade

# ------------------------------------------------------------------------------------ helpers
def xform(bm, M):
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    return bm

def aim(bm, pos, d, up="Y"):
    """Move a piece modelled along +Z at the origin to `pos`, its +Z pointing along d."""
    q = Vector(d).normalized().to_track_quat("Z", up)
    return xform(bm, Matrix.Translation(pos) @ q.to_matrix().to_4x4())

def put(B, hw, bm, mat):
    """A hat piece: on the detachable hat object when `separate`, else skinned to the head."""
    if hw.get("separate"):
        B.hat_parts.append((bm, mat))
    else:
        B.add(bm, mat, "head")

def cone_bm(length, r0, r1=0.0, segs=20, n=8, sy=1.0, round_tip=0.35, sx=1.0):
    """A soft cone along +Z from radius r0 at z=0 to r1 at the tip; the tip is rounded off."""
    rings = [(0.0, 0, 0, 0, 0)]
    for k in range(n + 1):
        t = k / n
        r = r0 + (r1 - r0) * t
        if t > 1 - round_tip:   # round the tip
            u = (t - (1 - round_tip)) / round_tip
            r = max(r, r0 * 0.18 * math.sqrt(max(0.0, 1 - u * u)))
        rings.append((length * t, r * sx, r * sy, 0, 0))
    rings.append((length * 1.02, 0, 0, 0, 0))
    return lathe(rings, segs)

def face_pt(B, x, z, s=1.0):
    """Point on the face from face-atlas style unit coords (x across, z up, same convention as the
    core's nose and face slot: atlas value * face scale)."""
    L = B.L; R, c = L["R"], L["head_c"]
    y = math.sqrt(max(0.0, 1 - x * x - z * z))
    return c + Vector((R * L["hsx"] * s * x, -R * L["hsy"] * s * y, R * L["hsz"] * s * z))

def face_scale(B):
    return float(B.P["face"].get("scale", 1.3))

def bob_bone(B, name, head, tail):
    B.add_bob_bone(name, head, tail)
    return name

def glass(B, key, hexcol, alpha):
    return B.mats.glass(key, hexcol, alpha=alpha)

def emit(B, key, hexcol, strength=4.0):
    return B.mats.emit(key, hexcol, strength=strength)

# --------------------------------------------------------------------------------- animal hood
def animal_hood(B, hw):
    """A soft costume hood (the chicken hood's shell and face rim) with frog eyes on top, felt
    teeth over the face opening, soft spikes down the back, round ears."""
    L = B.L; R, c = L["R"], L["head_c"]
    color = hw.get("color", "#2BB3A3")
    col = B.mats.flat("animal_hood", color, rough=0.75, spec=0.25)
    inner = B.mats.flat("animal_hood_inner", hw.get("inner", shade(color, 0.82)), rough=0.8, spec=0.2)
    open_a = math.radians(hw.get("opening_deg", 52))
    HR = 1.13
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=56, v_segments=36, radius=1.0)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > math.cos(open_a) + 1e-4], context="VERTS")
    rot = Matrix.Rotation(math.radians(90), 4, "X")
    for v in bm.verts:
        co = rot @ v.co
        drop = 0.25 * max(0.0, -co.z) * max(0.0, co.y + 0.3)   # hangs down the back into the collar
        v.co = c + Vector((co.x * R * L["hsx"] * HR, co.y * R * L["hsy"] * HR, (co.z - drop) * R * L["hsz"] * HR))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    B.add(solidify_bm(bm, 0.07 * R), col, "head")
    rr = math.sin(open_a) * HR; dz = math.cos(open_a) * HR
    def rim_pt(a, k=0.0, dy=0.0):
        return Vector((c.x + R * L["hsx"] * (rr - 0.02 - k) * math.cos(a), c.y - R * L["hsy"] * (dz - 0.02) - dy,
                       c.z + R * L["hsz"] * (rr - 0.02 - k) * math.sin(a)))
    B.add(tube_bm([tuple(rim_pt(a)) for a in np.linspace(0, 2 * math.pi, 56, endpoint=False)], 0.075 * R, cyclic=True), inner, "head")
    # outward surface point/normal of the hood at elevation el (from the front axis, 0 = front,
    # 90 = top, 180 = back) on the centre line or rotated by phi round the vertical
    def hood_pt(el_deg, phi=0.0, s=1.0):
        e = math.radians(el_deg)
        u = Vector((math.sin(phi) * math.sin(e), -math.cos(e), math.cos(phi) * math.sin(e)))   # unit dir, before scale
        p = c + Vector((u.x * R * L["hsx"] * HR * s, u.y * R * L["hsy"] * HR * s, u.z * R * L["hsz"] * HR * s))
        n = Vector((u.x / L["hsx"], u.y / L["hsy"], u.z / L["hsz"])).normalized()
        return p, n
    if hw.get("eyes"):
        ey = hw["eyes"] if isinstance(hw["eyes"], dict) else {}
        er = 0.30 * R * float(ey.get("size", 1.0))
        white = B.mats.flat("hood_eye", ey.get("color", "#FFFFFF"), rough=0.35, spec=0.5)
        pupil = B.mats.flat("hood_pupil", ey.get("pupil", "#1B1B20"), rough=0.3, spec=0.6)
        for s in (-1, 1):
            p, n = hood_pt(ey.get("el", 50), s * math.radians(ey.get("apart", 34)))
            ctr = p + n * er * 0.45 + Vector((0, 0, er * 0.25))
            B.add(ellipsoid_bm(ctr, (er, er * 0.95, er), segs=28, rings=16), white, "head")
            # lid: hood-coloured cap over the top and back of the ball
            lid = ellipsoid_bm((0, 0, 0), (er * 1.1, er * 1.1, er * 1.1), segs=28, rings=16)
            bmesh.ops.delete(lid, geom=[v for v in lid.verts if v.co.z < -0.02 * er], context="VERTS")
            xform(lid, Matrix.Translation(ctr) @ Matrix.Rotation(math.radians(-58), 4, "X"))   # open to the front
            B.add(solidify_bm(lid, 0.05 * R), col, "head")
            B.add(ellipsoid_bm(ctr + Vector((0, -er * 0.93, -er * 0.12)), (er * 0.42, er * 0.14, er * 0.46), segs=20, rings=10),
                  pupil, "head")
            B.add(ellipsoid_bm(ctr + Vector((-er * 0.16, -er * 1.0, er * 0.06)), (er * 0.13, er * 0.05, er * 0.13), segs=12, rings=6),
                  white, "head")
    if hw.get("teeth"):
        tooth = B.mats.flat("hood_teeth", hw["teeth"], rough=0.85, spec=0.15)
        n_t = int(hw.get("teeth_n", 6))
        span = math.radians(hw.get("teeth_span", 110))
        for k in range(n_t):
            a = math.pi / 2 - span / 2 + span * (k + 0.5) / n_t
            base = rim_pt(a, k=0.02, dy=0.035 * R)
            d = Vector((-math.cos(a), 0, -math.sin(a)))
            B.add(aim(cone_bm(0.27 * R, 0.115 * R, 0.0, segs=16, n=6, sy=0.45, round_tip=0.25), base, d), tooth, "head")
    if hw.get("spikes"):
        sp = B.mats.flat("hood_spikes", hw["spikes"], rough=0.7, spec=0.25)
        n_s = int(hw.get("spike_n", 6))
        for k in range(n_s):
            el = 48 + (150 - 48) * k / max(1, n_s - 1)
            sz = 1.0 - 0.35 * abs(k - (n_s - 1) * 0.3) / max(1, n_s - 1)
            p, n = hood_pt(el)
            B.add(aim(cone_bm(0.44 * R * sz, 0.21 * R * sz, 0.0, segs=18, n=7, sx=0.5, round_tip=0.4),
                      p - n * 0.03 * R, n), sp, "head")
    if hw.get("ears"):
        em = B.mats.flat("hood_ears", hw["ears"], rough=0.75, spec=0.25)
        for s in (-1, 1):
            p, n = hood_pt(70, s * math.radians(62))
            rot = Vector((0, -1, 0)).rotation_difference(Vector((0, -1, 0.35)).normalized()).to_matrix()
            B.add(ellipsoid_bm(p + n * 0.12 * R, (0.26 * R, 0.08 * R, 0.24 * R), rot=rot, segs=24, rings=12), em, "head")

# ------------------------------------------------------------------------------------ fishbowl
def fishbowl(B, hw):
    """A clear round space helmet over the whole head (room for side hair puffs), on an opaque
    collar ring at the neck."""
    L = B.L; R, c = L["R"], L["head_c"]
    k = float(hw.get("scale", 1.0))
    rb = 1.42 * R * k * max(L["hsx"], L["hsz"])
    ctr = c + Vector((0, 0, 0.15 * R))
    zcut = c.z - 0.98 * R   # the bowl ends at the neck ring
    gm = glass(B, "fishbowl", hw.get("tint", "#CFE8FF"), float(hw.get("alpha", 0.12)))
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=40, radius=1.0)
    hz = (zcut - ctr.z) / rb
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < hz - 1e-4], context="VERTS")
    for v in bm.verts:
        v.co = ctr + v.co * rb
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    B.add(bm, gm, "head")
    rr = math.sqrt(max(0.0, rb * rb - (zcut - ctr.z) ** 2))
    cm = B.mats.flat("fishbowl_collar", hw.get("collar", "#F4F4F0"), rough=0.4, spec=0.5)
    B.add(lathe([(zcut - 0.16 * R, 0, 0, 0, 0), (zcut - 0.16 * R, rr * 0.92, rr * 0.92, 0, 0), (zcut - 0.10 * R, rr * 1.03, rr * 1.03, 0, 0),
                 (zcut + 0.04 * R, rr * 1.03, rr * 1.03, 0, 0), (zcut + 0.06 * R, rr * 0.9, rr * 0.9, 0, 0),
                 (zcut + 0.06 * R, rr * 0.75, rr * 0.75, 0, 0), (zcut - 0.02 * R, 0, 0, 0, 0)], 56), cm, "head")
    B.add(tube_bm([(rr * 1.03 * math.cos(a), rr * 1.03 * math.sin(a), zcut - 0.04 * R) for a in np.linspace(0, 2 * math.pi, 56, endpoint=False)],
                  0.06 * R, cyclic=True), cm, "head")
    if hw.get("highlight", True):   # a soft glint strip on the upper left of the glass
        hm = glass(B, "fishbowl_glint", "#FFFFFF", 0.55)
        pts = []
        for t in np.linspace(0, 1, 12):
            el = math.radians(28 + 42 * t); ph = math.radians(-38 + 8 * t)
            pts.append(tuple(ctr + Vector((rb * 1.012 * math.sin(ph) * math.cos(el), -rb * 1.012 * math.cos(ph) * math.cos(el), rb * 1.012 * math.sin(el)))))
        B.add(tube_bm(pts, 0.035 * R, radii=[math.sin(math.pi * (0.08 + 0.84 * i / 11)) for i in range(12)]), hm, "head")

kit.HEADWEAR["animal_hood"] = animal_hood
kit.HEADWEAR["fishbowl"] = fishbowl
kit.HEADWEAR_OPTS["animal_hood"] = {"hair": "hide"}
kit.HEADWEAR_OPTS["fishbowl"] = {"hair": "free"}

# ------------------------------------------------------------------------------- shared shapes
def rbox(c, hw, hd, hh, power=8, segs=32):
    """Rounded box centred on c: half width (x), half depth (y), half height (z)."""
    cx, cy, cz = c
    k = 0.82
    return lathe([(cz - hh, 0, 0, cx, cy), (cz - hh, hw * k, hd * k, cx, cy), (cz - hh * 0.9, hw, hd, cx, cy),
                  (cz + hh * 0.9, hw, hd, cx, cy), (cz + hh, hw * k, hd * k, cx, cy), (cz + hh, 0, 0, cx, cy)], segs, power)

def place_parts(B, hw, parts, tilt_deg=0.0, lift=0.0):
    """Parts modelled around the head centre (origin = head centre): tilt about X (positive lowers
    the front), lift in R, then add them as hat pieces."""
    L = B.L; R, c = L["R"], L["head_c"]
    M = Matrix.Translation(c + Vector((0, 0, lift * R))) @ Matrix.Rotation(math.radians(tilt_deg), 4, "X")
    for bm, mat in parts:
        put(B, hw, xform(bm, M), mat)
    return M

def dome(rx, ry, h, zb, n=12, flat_top=0.0):
    """Closed half-ellipsoid helmet shell from z=zb up (r -> flat_top * r at the top)."""
    rings = [(zb, 0, 0, 0, 0)]
    for k in range(n + 1):
        th = (math.pi / 2) * k / n
        f = flat_top + (1 - flat_top) * math.cos(th)
        rings.append((zb + h * math.sin(th), rx * f, ry * f, 0, 0))
    rings.append((zb + h, 0, 0, 0, 0))
    return lathe(rings, 56)

def brim_ring(rx, ry, zb, bx, by, oy=0.0, th=0.04, droop=0.0):
    """Flat brim ring round a crown of radii (rx, ry) out to (bx, by) (centre shifted by oy)."""
    return lathe([(zb - th, rx * 0.97, ry * 0.97, 0, 0), (zb - th - droop, bx, by, 0, oy), (zb + th - droop, bx, by, 0, oy),
                  (zb + th, rx * 0.97, ry * 0.97, 0, 0)], 56)

def sweep(points, radii, segs=24, closed_end=True):
    """Tube through `points` (XZ-plane curve, Y is the binormal) with per-point radius."""
    bm = bmesh.new()
    rings = []
    Y = Vector((0, 1, 0))
    for i, p in enumerate(points):
        a = points[max(0, i - 1)]; b = points[min(len(points) - 1, i + 1)]
        T = (Vector(b) - Vector(a)).normalized()
        N = Y.cross(T).normalized()
        rings.append([bm.verts.new(Vector(p) + radii[i] * (math.cos(2 * math.pi * j / segs) * N + math.sin(2 * math.pi * j / segs) * Y))
                      for j in range(segs)])
    for A, Bv in zip(rings, rings[1:]):
        for j in range(segs):
            bm.faces.new((A[j], A[(j + 1) % segs], Bv[(j + 1) % segs], Bv[j]))
    if closed_end:
        bm.faces.new(list(reversed(rings[-1])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm

def bez3(p0, p1, p2, p3, t):
    u = 1 - t
    return Vector(p0) * u ** 3 + Vector(p1) * 3 * u * u * t + Vector(p2) * 3 * u * t * t + Vector(p3) * t ** 3

# ------------------------------------------------------------------------------------ hard hat
def hard_hat(B, hw):
    L = B.L; R = L["R"]
    mat = B.mats.flat("hard_hat", hw.get("color", "#FFC93C"), rough=0.35, spec=0.5)
    fit = float(hw.get("fit", 0.30))
    rx, ry, h = 1.12 * R * L["hsx"], 1.17 * R * L["hsy"], 1.0 * R * L["hsz"]
    zb = fit * R * L["hsz"]
    parts = [(dome(rx, ry, h, zb, flat_top=0.0), mat),
             (brim_ring(rx, ry, zb, rx * 1.10, ry * 1.24, oy=-0.12 * R, th=0.035 * R, droop=0.03 * R), mat)]
    pts = []
    for t in np.linspace(0.12, 0.88, 16):
        a = math.pi * t
        pts.append((0, -ry * math.cos(a) * 1.0, zb + h * math.sin(a) * 1.0))
    parts.append((tube_bm(pts, 0.10 * R, radii=[0.6 + 0.4 * math.sin(math.pi * i / 15) for i in range(16)]), mat))
    place_parts(B, hw, parts, hw.get("tilt_deg", 6))

# ------------------------------------------------------------------------------------- top hat
def top_hat(B, hw):
    L = B.L; R = L["R"]
    k = float(hw.get("scale", 1.0))
    mat = B.mats.flat("top_hat", hw.get("color", "#2A2A33"), rough=0.45, spec=0.4)
    band = B.mats.flat("top_hat_band", hw.get("band", "#7E57C2"), rough=0.6, spec=0.3)
    rt = 0.70 * R * L["hsx"] * k
    H = float(hw.get("height", 1.6)) * R * k
    zb = max(0.30, math.sqrt(max(0.0, 1 - (0.66 * k) ** 2))) * R * L["hsz"]
    parts = [(lathe([(zb, 0, 0, 0, 0), (zb, rt, rt, 0, 0), (zb + H * 0.5, rt * 0.98, rt * 0.98, 0, 0), (zb + H * 0.97, rt * 1.07, rt * 1.07, 0, 0),
                     (zb + H, rt * 1.03, rt * 1.03, 0, 0), (zb + H, 0, 0, 0, 0)], 48, power=2.1), mat)]
    parts.append((lathe([(zb + 0.03 * R, rt * 1.02, rt * 1.02, 0, 0), (zb + 0.03 * R + 0.30 * R * k, rt * 1.0, rt * 1.0, 0, 0)], 48), band))
    bR = 1.22 * R * k * L["hsx"]
    def brim_pt(u, v):
        a = 2 * math.pi * u
        r = rt * 0.95 + (bR - rt * 0.95) * v
        z = zb + 0.16 * R * k * (math.sin(a) ** 2) * v ** 2.2
        return (r * math.sin(a), -r * math.cos(a) * 0.92, z)
    parts.append((solidify_bm(grid_bm(brim_pt, 64, 6, closed_u=True), 0.05 * R * k), mat))
    place_parts(B, hw, parts, hw.get("tilt_deg", 0))

# -------------------------------------------------------------------------------- miner helmet
def miner_helmet(B, hw):
    L = B.L; R = L["R"]
    mat = B.mats.flat("miner_helmet", hw.get("color", "#F4F4F0"), rough=0.35, spec=0.5)
    dark = B.mats.flat("miner_lamp", hw.get("lamp", "#3A3A46"), rough=0.4, spec=0.5)
    lens = B.mats.emit("miner_lens", hw.get("light", "#FFF2C0"), strength=float(hw.get("glow", 6.0)))
    rx, ry, h = 1.12 * R * L["hsx"], 1.15 * R * L["hsy"], 1.02 * R * L["hsz"]
    zb = float(hw.get("fit", 0.28)) * R * L["hsz"]
    parts = [(dome(rx, ry, h, zb), mat), (brim_ring(rx, ry, zb, rx * 1.09, ry * 1.12, oy=-0.03 * R, th=0.035 * R, droop=0.02 * R), mat)]
    t = math.radians(30)
    p = Vector((0, -ry * math.cos(t), zb + h * math.sin(t)))
    d = Vector((0, -1, -0.12)).normalized()
    lr = 0.25 * R * float(hw.get("lamp_size", 1.0))
    parts.append((aim(lathe([(-0.25 * R, 0, 0, 0, 0), (-0.25 * R, lr * 0.8, lr * 0.8, 0, 0), (0.05 * R, lr, lr, 0, 0),
                              (0.16 * R, lr * 1.08, lr * 1.08, 0, 0), (0.20 * R, lr * 1.08, lr * 1.08, 0, 0), (0.20 * R, lr * 0.84, lr * 0.84, 0, 0),
                              (0.16 * R, 0, 0, 0, 0)], 32), p, d), dark))
    lens_c = p + d * 0.18 * R
    parts.append((aim(ellipsoid_bm((0, 0, 0), (lr * 0.84, lr * 0.84, 0.06 * R), segs=28, rings=10), lens_c, d), lens))
    M = place_parts(B, hw, parts, hw.get("tilt_deg", 0))
    B.lamps.append(dict(name="headlamp", pos=M @ (lens_c + d * 0.07 * R), dir=(M.to_3x3() @ Vector((0, -1, -0.25))).normalized(),
                        color=hw.get("light", "#FFF2C0"), watts=float(hw.get("watts", 30)), spot_deg=float(hw.get("spot_deg", 55))))

# ------------------------------------------------------------------------------------ colander
def colander(B, hw):
    L = B.L; R = L["R"]
    metal = B.mats.flat("colander", hw.get("color", "#C8CDD3"), rough=0.25, spec=0.8)
    hole = B.mats.flat("colander_holes", hw.get("holes", "#3A3F48"), rough=0.6, spec=0.2)
    rb = 1.14 * R * L["hsx"]; sy = L["hsy"] / L["hsx"]
    h = 0.95 * R * L["hsz"]
    zb = float(hw.get("fit", 0.25)) * R * L["hsz"]
    ft = 0.62
    def prof(th):
        return rb * (ft + (1 - ft) * math.cos(th)), zb + h * math.sin(th)
    rings = [(zb, 0, 0, 0, 0)]
    for k in range(13):
        r, z = prof((math.pi / 2) * k / 12)
        rings.append((z, r, r * sy, 0, 0))
    rings.append((zb + h, 0, 0, 0, 0))
    parts = [(lathe(rings, 56), metal)]
    parts.append((brim_ring(rb, rb * sy, zb, rb * 1.12, rb * sy * 1.12, th=0.03 * R), metal))
    parts.append((tube_bm([(rb * 1.12 * math.sin(a), -rb * sy * 1.12 * math.cos(a), zb) for a in np.linspace(0, 2 * math.pi, 64, endpoint=False)],
                          0.045 * R, cyclic=True), metal))
    for s in (-1, 1):   # side handles
        pts = [(s * (rb * 1.12 + 0.30 * R * math.sin(a)), 0.30 * R * math.cos(a), zb + 0.02 * R) for a in np.linspace(0, math.pi, 12)]
        parts.append((tube_bm(pts, 0.05 * R), metal))
    for k in range(3):   # the foot ring's three feet, on top since it is worn upside down
        a = 2 * math.pi * k / 3 + math.pi / 3
        b = Vector((rb * ft * 0.7 * math.sin(a), -rb * ft * 0.7 * math.cos(a) * sy, zb + h - 0.02 * R))
        parts.append((capsule_bm(b, b + Vector((0, 0, 0.14 * R)), 0.07 * R, 0.06 * R, segs=16, hem=3), metal))
    for row, (th, n) in enumerate(((0.35, 22), (0.75, 18), (1.12, 12))):
        r, z = prof(th)
        nr = Vector((h * math.cos(th), 0, rb * (1 - ft) * math.sin(th)))
        for j in range(n):
            a = 2 * math.pi * (j + 0.5 * row) / n
            p = Vector((r * math.sin(a), -r * math.cos(a) * sy, z))
            nn = Vector((nr.x * math.sin(a), -nr.x * math.cos(a), nr.z)).normalized()
            parts.append((aim(ellipsoid_bm((0, 0, 0), (0.05 * R, 0.05 * R, 0.012 * R), segs=10, rings=6), p, nn), hole))
    for j in range(7):   # holes on the flat top
        a = 2 * math.pi * j / 7
        rr = 0.0 if j == 0 else rb * ft * 0.35
        p = Vector((rr * math.sin(a), -rr * math.cos(a), zb + h))
        parts.append((ellipsoid_bm(p, (0.05 * R, 0.05 * R, 0.012 * R), segs=10, rings=6), hole))
    place_parts(B, hw, parts, hw.get("tilt_deg", 4))

# ---------------------------------------------------------------------------------- pot helmet
def pot_helmet(B, hw):
    L = B.L; R = L["R"]
    metal = B.mats.flat("pot", hw.get("color", "#B9C0C8"), rough=0.3, spec=0.75)
    grip = B.mats.flat("pot_handle", hw.get("handle", "#2A2A33"), rough=0.5, spec=0.3)
    rb = 1.10 * R * L["hsx"]; sy = L["hsy"] / L["hsx"]
    zb = float(hw.get("fit", 0.18)) * R * L["hsz"]
    H = 0.85 * R * float(hw.get("height", 1.0))
    e = 0.14 * R
    rings = [(zb, 0, 0, 0, 0), (zb, rb, rb * sy, 0, 0), (zb + H - e, rb, rb * sy, 0, 0)]
    for th in np.linspace(0, math.pi / 2, 6)[1:]:
        rr = rb - e + e * math.cos(th)
        rings.append((zb + H - e + e * math.sin(th), rr, rr * sy, 0, 0))
    rings.append((zb + H, 0, 0, 0, 0))
    parts = [(lathe(rings, 56), metal)]
    parts.append((tube_bm([(rb * 1.01 * math.sin(a), -rb * sy * 1.01 * math.cos(a), zb + 0.02 * R) for a in np.linspace(0, 2 * math.pi, 64, endpoint=False)],
                          0.05 * R, cyclic=True), metal))
    hz = zb + H * 0.32
    ln = float(hw.get("handle_len", 1.5)) * R
    p0 = Vector((0, rb * sy * 0.92, hz)); p1 = p0 + Vector((0, ln, 0.12 * R))
    parts.append((capsule_bm(p0, p1, 0.085 * R, 0.10 * R, segs=20, hem=4, sx=1.5), grip))
    parts.append((rbox((0, rb * sy * 1.02, hz), 0.16 * R, 0.05 * R, 0.12 * R, power=4), metal))
    parts.append((xform(tube_bm([(0.05 * R * math.cos(a), 0.05 * R * math.sin(a), 0) for a in np.linspace(0, 2 * math.pi, 16, endpoint=False)],
                                0.018 * R, cyclic=True), Matrix.Translation(p1 + Vector((0, -0.08 * R, 0.002)))), metal))
    place_parts(B, hw, parts, hw.get("tilt_deg", 0))

# ------------------------------------------------------------------------------------ nightcap
def nightcap(B, hw):
    L = B.L; R, c = L["R"], L["head_c"]
    col = B.mats.flat("nightcap", hw.get("color", "#3E7BEA"), rough=0.85, spec=0.2)
    stripe = B.mats.flat("nightcap_stripe", hw.get("stripe", "#F4F4F0"), rough=0.85, spec=0.2)
    pom = B.mats.flat("nightcap_pom", hw.get("pom", hw.get("stripe", "#F4F4F0")), rough=0.95, spec=0.1)
    s = 1 if hw.get("side", "L") == "L" else -1
    radii = (R * L["hsx"], R * L["hsy"], R * L["hsz"])
    thr = lambda phi: 0.36 - 0.40 * ((1 - math.cos(phi)) / 2)
    B.add(solidify_bm(cap_shell_bm(c, radii, thr, lambda el, phi: 1.08), 0.05 * R), col, "head")
    B.add(tube_bm([tuple(B.head_point(thr(phi) + 0.08, phi, 1.09)) for phi in np.linspace(0, 2 * math.pi, 48, endpoint=False)],
                  0.11 * R, cyclic=True), stripe, "head")
    ln = float(hw.get("length", 1.0))
    P0 = Vector((0, 0, 0.55 * R * L["hsz"])); P1 = Vector((0, 0.05 * R, 1.55 * R))
    P2 = Vector((s * 0.85 * R * ln, 0.08 * R, 1.9 * R)); P3 = Vector((s * 1.45 * R * ln, 0.1 * R, (1.9 - 0.95 * ln) * R))
    r0 = 0.88 * R * L["hsx"]
    N = 48
    pts = [c + bez3(P0, P1, P2, P3, i / N) for i in range(N + 1)]
    rad = [r0 * (1 - i / N) ** 0.95 + 0.07 * R * (i / N) for i in range(N + 1)]
    n_st = int(hw.get("stripes", 6))
    for b in range(n_st):
        i0, i1 = round(b * N / n_st), round((b + 1) * N / n_st)
        B.add(sweep(pts[i0:i1 + 1], rad[i0:i1 + 1], closed_end=(b == n_st - 1)), stripe if b % 2 else col, "head")
    tip = pts[-1]
    bone = B.add_bob_bone("nightcap_pom", tip, tip + Vector((0, 0, -0.5 * R)), amount=float(hw.get("bob", 1.0)), side=s)
    B.add(ellipsoid_bm(tip + Vector((0, 0, -0.10 * R)), (0.24 * R,) * 3, segs=24, rings=14,
                       deform=lambda co: co * (1 + 0.04 * math.sin(co.x * 400) * math.sin(co.z * 400))), pom, bone)

# ------------------------------------------------------------------------------------ chef hat
def chef_hat(B, hw):
    L = B.L; R = L["R"]
    white = B.mats.flat("chef_hat", hw.get("color", "#FBFBF7"), rough=0.8, spec=0.2)
    bandm = B.mats.flat("chef_band", hw.get("band", hw.get("color", "#F1F0EA")), rough=0.75, spec=0.2)
    rb = 1.0 * R * L["hsx"]; sy = L["hsy"] / L["hsx"]
    zb = float(hw.get("fit", 0.32)) * R * L["hsz"]
    bh = 0.36 * R
    parts = [(lathe([(zb, 0, 0, 0, 0), (zb, rb, rb * sy, 0, 0), (zb + bh, rb * 1.03, rb * 1.03 * sy, 0, 0), (zb + bh, 0, 0, 0, 0)], 56), bandm)]
    Hk = float(hw.get("height", 1.0))
    prof = [(0.0, 0.96), (0.12, 1.12), (0.35, 1.22), (0.7, 1.26), (0.95, 1.2), (1.1, 1.02), (1.2, 0.7), (1.25, 0.0)]
    z0 = zb + bh - 0.04 * R
    rings = [(z0 + dz * R * Hk, r * rb, r * rb * sy, 0, 0) for dz, r in prof]
    rings.insert(0, (z0, 0, 0, 0, 0))
    bm = lathe(rings, 64)
    for v in bm.verts:   # soft pleats round the puff
        w = min(1.0, max(0.0, (v.co.z - z0) / (0.15 * R)))
        a = math.atan2(v.co.y, v.co.x)
        k = 1 + 0.045 * w * math.cos(9 * a)
        v.co.x *= k; v.co.y *= k
    parts.append((bm, white))
    if hw.get("badge"):
        bd = B.mats.flat("chef_badge", hw["badge"], rough=0.4, spec=0.5)
        parts.append((aim(ellipsoid_bm((0, 0, 0), (0.13 * R, 0.13 * R, 0.035 * R), segs=24, rings=10),
                          Vector((0, -rb * sy * 1.03, zb + bh * 0.5)), Vector((0, -1, 0))), bd))
    place_parts(B, hw, parts, hw.get("tilt_deg", 0))

# ---------------------------------------------------------------------------------- bucket hat
def bucket_hat(B, hw):
    L = B.L; R, c = L["R"], L["head_c"]
    mat = B.mats.flat("bucket_hat", hw.get("color", "#C9B48A"), rough=0.85, spec=0.2)
    bandm = B.mats.flat("bucket_band", hw.get("band", shade(hw.get("color", "#C9B48A"), 0.75)), rough=0.8, spec=0.2)
    rc_ = 1.08 * R * L["hsx"]; sy = L["hsy"] / L["hsx"]
    zb = float(hw.get("fit", 0.20)) * R * L["hsz"]
    ch = 0.95 * R * L["hsz"]
    rings = [(zb, 0, 0, 0, 0), (zb, rc_, rc_ * sy, 0, 0), (zb + ch * 0.75, rc_ * 0.86, rc_ * 0.86 * sy, 0, 0)]
    for th in np.linspace(0, math.pi / 2, 6)[1:]:
        rr = rc_ * 0.86 * (0.55 + 0.45 * math.cos(th))
        rings.append((zb + ch * 0.75 + ch * 0.25 * math.sin(th), rr, rr * sy, 0, 0))
    rings.append((zb + ch, 0, 0, 0, 0))
    parts = [(lathe(rings, 56), mat)]
    parts.append((lathe([(zb + 0.02 * R, rc_ * 1.01, rc_ * 1.01 * sy, 0, 0), (zb + 0.22 * R, rc_ * 0.965, rc_ * 0.965 * sy, 0, 0)], 56), bandm))
    bw = float(hw.get("brim", 0.55)) * R
    def brim_pt(u, v):
        a = 2 * math.pi * u
        r = rc_ * 0.97 + bw * v
        return (r * math.sin(a), -r * math.cos(a) * sy, zb + 0.02 * R - 0.30 * R * v ** 1.4)
    parts.append((solidify_bm(grid_bm(brim_pt, 64, 6, closed_u=True), 0.05 * R), mat))
    M = place_parts(B, hw, parts, hw.get("tilt_deg", 4))
    if hw.get("lure"):
        lm = B.mats.flat("lure", hw["lure"], rough=0.3, spec=0.6)
        silver = B.mats.flat("lure_hook", "#C8CDD3", rough=0.25, spec=0.8)
        eye = B.mats.flat("lure_eye", "#1B1B20", rough=0.3, spec=0.5)
        a = math.radians(hw.get("lure_deg", 50))
        pin = M @ Vector(((rc_ * 0.93 + 0.03 * R) * math.sin(a), -(rc_ * 0.93 + 0.03 * R) * math.cos(a) * sy, zb + ch * 0.45))
        out = Vector((math.sin(a), -math.cos(a), 0))
        bone = B.add_bob_bone("lure", pin, pin + Vector((0, 0, -0.4 * R)), amount=1.2, side=1.0)
        top = pin + out * 0.04 * R
        body = top + Vector((0, 0, -0.26 * R))
        B.add(tube_bm([tuple(pin), tuple(top + Vector((0, 0, -0.04 * R)))], 0.015 * R), silver, bone)
        rot = Vector((0, 0, 1)).rotation_difference(out).to_matrix() @ Matrix.Rotation(math.pi / 2, 3, "X")
        B.add(ellipsoid_bm(body, (0.07 * R, 0.17 * R, 0.07 * R), segs=20, rings=12,
                           rot=Matrix.Rotation(math.atan2(out.x, -out.y), 3, "Z") @ Matrix.Rotation(-math.pi / 2, 3, "X")), lm, bone)
        B.add(ellipsoid_bm(body + out * 0.06 * R + Vector((0, 0, 0.09 * R)), (0.025 * R,) * 3, segs=10, rings=6), eye, bone)
        hk = [body + Vector((0, 0, -0.16 * R)) + Vector((0.06 * R * math.sin(t) * out.x, 0.06 * R * math.sin(t) * out.y, -0.06 * R + 0.06 * R * math.cos(t)))
              for t in np.linspace(0, 1.4 * math.pi, 8)]
        B.add(tube_bm([tuple(body + Vector((0, 0, -0.14 * R)))] + [tuple(p) for p in hk], 0.014 * R), silver, bone)

# ------------------------------------------------------------------------------------- sun hat
def sun_hat(B, hw):
    L = B.L; R = L["R"]
    straw = B.mats.flat("sun_hat", hw.get("color", "#E9C97A"), rough=0.85, spec=0.2)
    bandm = B.mats.flat("sun_band", hw.get("band", "#E86FA6"), rough=0.6, spec=0.3)
    rc_ = 1.07 * R * L["hsx"]; sy = L["hsy"] / L["hsx"]
    zb = float(hw.get("fit", 0.24)) * R * L["hsz"]
    ch = 0.9 * R * L["hsz"]
    rings = [(zb, 0, 0, 0, 0)]
    for th in np.linspace(0, math.pi / 2, 10):
        rr = rc_ * (0.45 + 0.55 * math.cos(th) ** 0.6)
        rings.append((zb + ch * math.sin(th), rr, rr * sy, 0, 0))
    rings.append((zb + ch, 0, 0, 0, 0))
    parts = [(lathe(rings, 56), straw)]
    parts.append((lathe([(zb + 0.02 * R, rc_ * 1.015, rc_ * 1.015 * sy, 0, 0), (zb + 0.24 * R, rc_ * 0.99, rc_ * 0.99 * sy, 0, 0)], 56), bandm))
    bw = float(hw.get("brim", 1.3)) * R
    waves = int(hw.get("waves", 7))
    def brim_pt(u, v):
        a = 2 * math.pi * u
        r = rc_ * 0.97 + bw * v
        z = zb + 0.02 * R + (0.10 * R * math.sin(waves * a) - 0.16 * R) * v ** 2
        return (r * math.sin(a), -r * math.cos(a) * sy, z)
    parts.append((solidify_bm(grid_bm(brim_pt, 140, 8, closed_u=True), 0.045 * R), straw))
    if hw.get("flower"):
        fm = B.mats.flat("sun_flower", hw["flower"], rough=0.6, spec=0.3)
        mid = B.mats.flat("sun_flower_mid", hw.get("flower_mid", "#FFD23F"), rough=0.6, spec=0.3)
        a = math.radians(hw.get("flower_deg", 40))
        u, v = a / (2 * math.pi) % 1.0, 0.18
        fc = Vector(brim_pt(u, v)) + Vector((0, 0, 0.05 * R))
        fc = Vector((rc_ * 1.02 * math.sin(a), -rc_ * 1.02 * math.cos(a) * sy, zb + 0.16 * R))
        out = Vector((math.sin(a), -math.cos(a), 0.3)).normalized()
        for k in range(5):
            b = 2 * math.pi * k / 5
            parts.append((aim(ellipsoid_bm((0.13 * R * math.cos(b), 0.13 * R * math.sin(b), 0), (0.12 * R, 0.12 * R, 0.035 * R),
                                           segs=16, rings=8), fc, out), fm))
        parts.append((aim(ellipsoid_bm((0, 0, 0.03 * R), (0.08 * R, 0.08 * R, 0.05 * R), segs=16, rings=8), fc, out), mid))
    place_parts(B, hw, parts, hw.get("tilt_deg", 3))

# ------------------------------------------------------------------------------------ box head
def box_head(B, hw):
    L = B.L; R = L["R"]
    card = B.mats.flat("box_head", hw.get("color", "#C49A6C"), rough=0.9, spec=0.15)
    tape = B.mats.flat("box_tape", hw.get("tape", "#E6CFA0"), rough=0.6, spec=0.3)
    inside = B.mats.flat("box_inside", shade(hw.get("color", "#C49A6C"), 0.7), rough=0.9, spec=0.1)
    k = float(hw.get("scale", 1.0))
    W, D, H = 1.12 * R * L["hsx"] * k, 1.12 * R * L["hsy"] * k, 1.06 * R * L["hsz"] * k
    t = 0.05 * R
    cz = 0.06 * R
    hx = float(hw.get("hole_w", 0.64)) * R * L["hsx"]
    z0, z1 = -0.70 * R * L["hsz"] - cz, 0.42 * R * L["hsz"] - cz   # face cut-out, relative to the box centre
    pw = dict(power=10, segs=40)
    parts = [(rbox((0, 0, cz + H - t), W, D, t, **pw), card), (rbox((0, D - t, cz), W, t, H, **pw), card)]
    for s in (-1, 1):
        parts.append((rbox((s * (W - t), 0, cz), t, D, H, **pw), card))
    fy = -D + t
    parts.append((rbox((0, fy, cz + (z1 + H) / 2), W, t, (H - z1) / 2, **pw), card))
    parts.append((rbox((0, fy, cz + (z0 - H) / 2), W, t, (z0 + H) / 2, **pw), card))
    for s in (-1, 1):
        parts.append((rbox((s * (hx + W) / 2, fy, cz + (z0 + z1) / 2), (W - hx) / 2, t, (z1 - z0) / 2, **pw), card))
    parts.append((rbox((0, fy + 0.008 * R, cz + (z0 + z1) / 2), hx + 0.02 * R, t * 0.9, (z1 - z0) / 2 + 0.02 * R, **pw), inside))
    parts.append((rbox((0, 0, cz + H + 0.004 * R), 0.17 * R * k, D + 0.008 * R, 0.012 * R, power=6), tape))
    parts.append((rbox((0, -D - 0.004 * R, cz + H - 0.12 * R), 0.17 * R * k, 0.012 * R, 0.13 * R, power=6), tape))
    parts.append((rbox((0, D + 0.004 * R, cz + H - 0.12 * R), 0.17 * R * k, 0.012 * R, 0.13 * R, power=6), tape))
    place_parts(B, hw, parts, hw.get("tilt_deg", 0))

for _n, _f, _hair in (("hard_hat", hard_hat, "tuck"), ("top_hat", top_hat, "tuck"), ("miner_helmet", miner_helmet, "tuck"),
                      ("colander", colander, "tuck"), ("pot_helmet", pot_helmet, "tuck"), ("nightcap", nightcap, "tuck"),
                      ("chef_hat", chef_hat, "tuck"), ("bucket_hat", bucket_hat, "tuck"), ("sun_hat", sun_hat, "tuck"),
                      ("box_head", box_head, "hide")):
    kit.HEADWEAR[_n] = _f
    kit.HEADWEAR_OPTS[_n] = {"hair": _hair}
