"""Kit pieces for The Hill's people (standard body): the Gnome Foreman and the Caveman.

Headwear: `cone_hat` (teal cone + detachable tiny hard hat), `ice_cube`.
Costume:  `gnome_beard`, `vest_stripes`, `clipboard` (part `prop`), `whistle`,
          `mane_beard`, `fur_tunic`, `cloth_club` (part `prop`).
Actions:  `march`, `write`, `salute` (gnome); `polish`, `point`, `wave` (caveman).
"""
import math, random
import bmesh
from mathutils import Vector, Euler, Matrix
from mathutils.bvhtree import BVHTree
import jarling_kit as kit
from jarling_kit import lathe, ellipsoid_bm, capsule_bm, tube_bm, grid_bm, solidify_bm, smooth_interp, envelope, superxy

# ------------------------------------------------------------------------------------ helpers
def torso_pt(B, t, th, grow=1.0):
    """Point on the torso surface at height fraction t (0 bottom, 1 top), lathe angle th
    (0 = +X / the character's left, -pi/2 = front)."""
    L = B.L; b = L["b"]
    t = min(1.0, max(0.0, t))
    w = smooth_interp(t, B.torso_widths) * envelope(t, b["n"]) * grow
    dx, dy = superxy(th, b["power"])
    cy = 0.0
    if b["power"] > 2.5:
        cy = -smooth_interp(t, [(0.0, 0.0), (0.45, 0.0), (0.78, 0.022), (1.0, 0.01)])
    return Vector((w * dx, cy + w * b["depth"] * dy, L["torso_z0"] + (L["torso_z1"] - L["torso_z0"]) * t))

def rbox(c, hw, hd, hh, power=8, segs=32):
    """Rounded box centred on c: half width (x), half depth (y), half height (z)."""
    cx, cy, cz = c
    k = 0.82
    return lathe([(cz - hh, 0, 0, cx, cy), (cz - hh, hw * k, hd * k, cx, cy), (cz - hh * 0.9, hw, hd, cx, cy),
                  (cz + hh * 0.9, hw, hd, cx, cy), (cz + hh, hw * k, hd * k, cx, cy), (cz + hh, 0, 0, cx, cy)], segs, power)

def xform(bm, M):
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    return bm

def surface_y(bm, x, z):
    """Front-most surface point of bm at (x, z), seen from the front (-Y)."""
    tree = BVHTree.FromBMesh(bm)
    hit = tree.ray_cast(Vector((x, -3.0, z)), Vector((0, 1, 0)))
    return hit[0]

# --------------------------------------------------------------------------------- the gnome
def cone_hat(B, hw):
    L = B.L; R, c = L["R"], L["head_c"]
    mat = B.mats.flat("cone_hat", hw["color"], rough=0.7, spec=0.25)
    rx, ry = 1.10 * R * L["hsx"], 1.08 * R * L["hsy"]
    zb = c.z + hw.get("base", 0.30) * R
    H = hw.get("height", 0.46)
    tip_r = 0.035
    rings = [(zb - 0.005, 0, 0, 0, 0)]
    n = 14
    for k in range(n + 1):
        t = k / n
        f = (1 - t) + (tip_r / rx) * t
        rings.append((zb + H * t * 0.97, rx * f, ry * f, 0, 0.012 * t))
    rings.append((zb + H, 0, 0, 0, 0.012))
    B.add(lathe(rings, 48), mat, "head")
    pts = [(rx * 1.0 * math.sin(a), -ry * 1.0 * math.cos(a), zb + 0.006) for a in [2 * math.pi * i / 56 for i in range(56)]]
    B.add(tube_bm(pts, 0.016, cyclic=True), mat, "head")
    # the tiny hard hat on the tip: detachable (gnome_foreman_hat, jarling_detachable)
    hard = B.mats.flat("hard_hat", hw.get("hard_hat", "#F4F1E6"), rough=0.35, spec=0.5)
    ht = zb + H * 0.80
    rr = rx * (1 - 0.80) + tip_r * 0.80 + 0.012
    dome = ellipsoid_bm((0, 0.006, ht), (rr, rr, H * 0.24), segs=32, rings=16, floor=ht)
    brim = lathe([(ht - 0.004, 0, 0, 0, -0.004), (ht - 0.004, rr * 1.38, rr * 1.42, 0, -0.004),
                  (ht + 0.006, rr * 1.38, rr * 1.42, 0, -0.004), (ht + 0.006, 0, 0, 0, -0.004)], 40, power=2.0)
    ridge = capsule_bm((0, -rr * 0.75, ht + H * 0.16), (0, rr * 0.85, ht + H * 0.16), 0.009, 0.009, segs=12, hem=3)
    xform(ridge, Matrix.Translation((0, 0, 0)))
    for bm in (dome, brim, ridge):
        if hw.get("separate", True):
            B.hat_parts.append((bm, hard))
        else:
            B.add(bm, hard, "head")

def gnome_beard(B, piece):
    """A big cream beard triangle from under the nose down over the chest, a moustache, and the
    hair at the back of the head under the hat."""
    L = B.L; R, c = L["R"], L["head_c"]
    mat = B.mats.flat("beard", piece["color"], rough=0.8, spec=0.2)
    rz = 0.74 * R
    down = piece.get("length", 1.5)
    def tri(co):
        if co.z < 0:
            t = -co.z / rz
            co.x *= 1 - 0.82 * t ** 1.15
            co.y = co.y * (1 - 0.45 * t) - 0.30 * R * t
            co.z *= down
        return co
    beard = ellipsoid_bm(c + Vector((0, -0.42 * R, -0.88 * R)), (1.0 * R * L["hsx"], 0.62 * R, rz), segs=40, rings=24, deform=tri)
    B.add(beard, mat, "head")
    B.beard_bm = beard
    for s in (-1, 1):   # moustache puffs under the nose
        rot = Euler((0, s * 0.25, 0)).to_matrix()
        B.add(ellipsoid_bm(c + Vector((s * 0.22 * R, -0.90 * R, -0.42 * R)), (0.30 * R, 0.17 * R, 0.15 * R), rot=rot,
                           segs=24, rings=12), mat, "head")
    # back of the head: hair under the hat brim
    B.add(ellipsoid_bm(c + Vector((0, 0.30 * R, -0.12 * R)), (0.98 * R * L["hsx"], 0.76 * R, 0.66 * R), segs=32, rings=16), mat, "head")

def vest_stripes(B, piece):
    mat = B.mats.flat("vest_stripe", piece["color"], rough=0.7, spec=0.25)
    for mid in (-math.pi / 2, math.pi / 2):
        for s in (-1, 1):
            th0 = mid + s * piece.get("offset", 0.52)
            hwid = piece.get("width", 0.075)
            fn = lambda u, v, th0=th0: tuple(torso_pt(B, 0.27 + 0.64 * v, th0 - hwid + 2 * hwid * u, 1.022))
            g = grid_bm(fn, 3, 18)
            B.add(solidify_bm(g, 0.006), mat, "spine")

def clipboard(B, piece):
    side = piece.get("hand", "L"); s = 1 if side == "L" else -1
    hc = B.hand_c[side]
    wood = B.mats.flat("clipboard", piece.get("color", "#B07A3C"), rough=0.6, spec=0.3)
    paper = B.mats.flat("paper", piece.get("paper", "#FFFDF4"), rough=0.8, spec=0.2)
    clip = B.mats.flat("clip", piece.get("clip", "#F4F1E6"), rough=0.35, spec=0.5)
    B.cur_part = "prop"
    bc = hc + Vector((s * 0.035, -0.055, 0.03))
    hw_, hh = 0.075, 0.095
    bone = f"hand.{side}"
    B.add(rbox(bc, hw_, 0.008, hh), wood, bone)
    pc = bc + Vector((0, -0.007, -0.006))
    B.add(rbox(pc, hw_ * 0.84, 0.003, hh * 0.86), paper, bone)
    B.add(rbox(bc + Vector((0, -0.008, hh * 0.95)), 0.03, 0.009, 0.013), clip, bone)
    for k, ln in enumerate((0.85, 0.6, 0.75, 0.4)):   # scribble lines
        z = pc.z + hh * 0.5 - k * 0.032
        x0 = pc.x - hw_ * 0.62
        B.add(rbox((x0 + hw_ * 0.62 * ln, pc.y - 0.0035, z), hw_ * 0.62 * ln, 0.0015, 0.0045, power=4, segs=12), wood, bone)
    B.cur_part = None

def whistle(B, piece):
    L = B.L; R, c = L["R"], L["head_c"]
    yel = B.mats.flat("whistle", piece.get("color", "#FFD23F"), rough=0.3, spec=0.6)
    cord = B.mats.flat("whistle_cord", piece.get("cord", "#B07A3C"), rough=0.7, spec=0.2)
    bm = getattr(B, "beard_bm", None)
    wx, wz = piece.get("x", 0.42) * R, c.z - piece.get("drop", 1.45) * R
    def on(x, z, off=0.012):
        h = surface_y(bm, x, z) if bm else None
        y = h.y if h else -L["tw"] * 1.1
        return Vector((x, y - off, z))
    zn = c.z - 0.8 * R
    pts = [on(-0.62 * R + (wx + 0.62 * R) * (k / 8), zn + (wz - zn) * (k / 8) ** 0.8) for k in range(9)]
    pts2 = [on(0.62 * R + (wx - 0.62 * R) * (k / 6), zn + (wz - zn) * (k / 6)) for k in range(7)]
    B.add(tube_bm([tuple(p) for p in pts], 0.004), cord, "spine")
    B.add(tube_bm([tuple(p) for p in pts2], 0.004), cord, "spine")
    p = on(wx, wz, 0.016)
    rot = Euler((0, 0, 0.5)).to_matrix()
    B.add(xform(capsule_bm((0, 0, 0), (0, 0.0, 0.055), 0.016, 0.013, segs=16, hem=4),
                Matrix.Translation(p) @ Matrix.Rotation(-1.2, 4, "Y")), yel, "spine")
    B.add(ellipsoid_bm(p + Vector((0.006, -0.002, -0.008)), (0.022, 0.018, 0.02), segs=16, rings=10), yel, "spine")

# ------------------------------------------------------------------------------- the caveman
def mane_beard(B, piece):
    """The beard half of the caveman's hair mass: one smooth shaggy shell round the jaw, wide enough
    to run into the `mane` at the sides, ending in ragged tufts at the top of the chest."""
    L = B.L; R, c = L["R"], L["head_c"]
    mat = B.mats.flat("hair", piece["color"], rough=0.5, spec=0.4)
    rz = 0.62 * R
    tufts = piece.get("tufts", 9)
    def shag(co):
        a = math.atan2(co.y, co.x)
        co.x *= 1 + 0.03 * math.sin(a * 11 + co.z * 40)
        if co.z < 0:
            t = -co.z / rz
            co.x *= 1 - 0.30 * t ** 2
            co.z *= 1 + 0.30 * t ** 3 * max(0.0, math.cos(a * tufts)) ** 2
        return co
    B.add(ellipsoid_bm(c + Vector((0, -0.12 * R, -0.92 * R)), (1.22 * R * L["hsx"], 0.86 * R, rz), segs=64, rings=32, deform=shag),
          mat, "head")

def ice_cube(B, hw):
    L = B.L; R, c = L["R"], L["head_c"]
    mat = B.mats.flat("ice_cube", hw["color"], rough=0.08, spec=0.8)
    top = max((v.co.z for bm, m, bone in B.parts if bone == "head" for v in bm.verts
               if abs(v.co.x) < 0.04 and abs(v.co.y) < 0.04), default=c.z + R)
    a = hw.get("size", 0.065)
    cube = lathe([(-a, 0, 0, 0, 0), (-a, a * 0.78, a * 0.78, 0, 0), (-a * 0.94, a * 0.96, a * 0.96, 0, 0),
                  (-a * 0.78, a, a, 0, 0), (a * 0.78, a, a, 0, 0), (a * 0.94, a * 0.96, a * 0.96, 0, 0),
                  (a, a * 0.78, a * 0.78, 0, 0), (a, 0, 0, 0, 0)], 32, power=7)
    tilt = Euler((math.radians(hw.get("tilt_x", 8)), math.radians(hw.get("tilt_y", -10)), math.radians(hw.get("turn", 25)))).to_matrix().to_4x4()
    xform(cube, Matrix.Translation((0, 0.01, top + a * 0.62)) @ tilt)
    B.add(cube, mat, "head")

def fur_tunic(B, piece):
    """One-shoulder fur tunic over the bare torso: over the left shoulder, under the right arm,
    brown spots, zigzag hem above the bare legs."""
    L = B.L
    mat = B.mats.flat("tunic", piece["color"], rough=0.85, spec=0.2)
    spot = B.mats.flat("tunic_spots", piece.get("spots", "#7C4E24"), rough=0.85, spec=0.2)
    z0, z1 = L["torso_z0"], L["torso_z1"]
    tz = lambda z: (z - z0) / (z1 - z0)
    teeth, amp = piece.get("teeth", 9), piece.get("zigzag", 0.03)
    z_hem = L["hip_z"] - piece.get("hem_drop", 0.05)
    grow = 1.06
    def surf(th, z):
        t = tz(z)
        if t >= 0.32:
            return torso_pt(B, t, th, grow)
        p = torso_pt(B, 0.32, th, grow * (1 + (0.32 - t) * 0.55))
        p.z = z
        return p
    def zig(th):
        f = (th * teeth / (2 * math.pi)) % 1.0
        return z_hem - amp * (1 - abs(2 * f - 1))
    def ztop(th):
        dx = math.cos(th)
        k = max(0.0, min(1.0, (dx + 0.15) / 1.0)) ** 1.3
        return z0 + (z1 - z0) * (0.66 + 0.33 * k)
    def fn(u, v):
        th = 2 * math.pi * u
        zb, zt = zig(th), ztop(th)
        return tuple(surf(th, zb + (zt - zb) * v))
    shell = grid_bm(fn, 18 * teeth // 3 * 2, 16, closed_u=True)
    B.add(solidify_bm(shell, 0.008), mat, "spine")
    rnd = random.Random(3)
    for _ in range(piece.get("n_spots", 16)):
        th = rnd.uniform(0, 2 * math.pi)
        zb, zt = zig(th) + 0.03, ztop(th) - 0.03
        p = surf(th, rnd.uniform(zb, zt))
        n = Vector((p.x, p.y, 0)).normalized()
        rot = Vector((0, 1, 0)).rotation_difference(n).to_matrix()
        r = rnd.uniform(0.012, 0.02)
        B.add(ellipsoid_bm(p, (r * 1.2, 0.006, r), rot=rot, segs=14, rings=8), spot, "spine")

def cloth_club(B, piece):
    side = piece.get("hand", "R"); s = 1 if side == "L" else -1
    hc = B.hand_c[side]
    wood = B.mats.flat("club_stick", piece.get("stick", "#B07A3C"), rough=0.6, spec=0.3)
    cloth = B.mats.flat("club_cloth", piece.get("color", "#F3EAD2"), rough=0.9, spec=0.15)
    string = B.mats.flat("club_string", piece.get("string", "#1E9AA0"), rough=0.6, spec=0.3)
    bone = f"hand.{side}"
    B.cur_part = "prop"
    p0 = hc + Vector((-s * 0.03, -0.012, -0.075))
    p1 = hc + Vector((s * 0.22, -0.05, 0.27))
    B.add(capsule_bm(p0, p1, 0.014, 0.013, segs=14, hem=3), wood, bone)
    bc = p1 + Vector((s * 0.05, -0.008, 0.07))
    def puff(co):
        co.x *= 1 + 0.06 * math.sin(co.z * 120); return co
    B.add(ellipsoid_bm(bc, (0.085, 0.08, 0.1), segs=28, rings=16, deform=puff), cloth, bone)
    B.add(ellipsoid_bm(bc + Vector((0.02, -0.02, 0.05)), (0.04, 0.04, 0.035), segs=18, rings=10), cloth, bone)
    zt = bc.z - 0.065
    pts = [(bc.x + 0.05 * math.cos(a), bc.y + 0.047 * math.sin(a), zt) for a in [2 * math.pi * i / 28 for i in range(28)]]
    B.add(tube_bm(pts, 0.007, cyclic=True), string, bone)
    for d in (-1, 1):   # the knot's two ends
        a = Vector((bc.x + 0.03 * d * s, bc.y - 0.045, zt))
        B.add(tube_bm([tuple(a), tuple(a + Vector((0.012 * d, -0.012, -0.03)))], 0.005), string, bone)
    B.cur_part = None

kit.HEADWEAR["cone_hat"] = cone_hat
kit.HEADWEAR["ice_cube"] = ice_cube
for _n, _f in (("gnome_beard", gnome_beard), ("vest_stripes", vest_stripes), ("clipboard", clipboard), ("whistle", whistle),
               ("mane_beard", mane_beard), ("fur_tunic", fur_tunic), ("cloth_club", cloth_club)):
    kit.COSTUME[_n] = _f

# --------------------------------------------------------------------------------- actions
def _base(B, extra=None):
    po = B.P.get("posture", {})
    sl, hl, ao = po.get("spine_lean", 0.0), po.get("head_lean", 0.0), po.get("arm_out", 0.0)
    p = {"spine": {"lean": sl}, "head": {"lean": hl}, "arm.L": {"out": ao + 4}, "arm.R": {"out": ao + 4}}
    for k, v in (extra or {}).items():
        cur = dict(p.get(k, {}))
        for kk, vv in v.items():
            cur[kk] = cur.get(kk, 0.0) + vv if not isinstance(vv, tuple) else vv
        p[k] = cur
    return p

def act_march(B):
    hold = {"arm.L": {"swing": 22, "out": 2}, "hand.L": {"swing": 10}}
    def step(lead):   # lead leg up high, the free arm swings stiffly against it
        o = "R" if lead == "L" else "L"
        e = {"root": {"loc": (0, 0, 0.03)}, "spine": {"lean": -5}, "head": {"lean": -4},
             f"leg.{lead}": {"swing": 62}, f"foot.{lead}": {"point": 18}, f"leg.{o}": {"swing": -10}, f"foot.{o}": {"point": 6}}
        e["arm.R"] = {"swing": -38 if lead == "R" else 42}
        e.update(hold)
        return _base(B, e)
    mid = _base(B, {"root": {"loc": (0, 0, -0.01), "scale": (1.03, 1.03, 0.96)}, "spine": {"lean": -5}, "head": {"lean": -4}, **hold})
    return [(1, step("L")), (7, mid), (13, step("R")), (19, mid), (25, step("L"))]

def act_write(B):
    held = {"arm.L": {"swing": 60, "out": -24}, "hand.L": {"swing": -5}, "head": {"lean": 16}, "spine": {"lean": 4}}
    def w(sw, out, hs, extra=None):
        e = dict(held); e["arm.R"] = {"swing": sw, "out": out}; e["hand.R"] = {"swing": hs}
        e.update(extra or {})
        return _base(B, e)
    return [(1, w(72, -30, 20)), (5, w(76, -24, 26)), (9, w(70, -36, 18)), (13, w(77, -28, 28)),
            (17, w(71, -34, 20)), (21, w(80, -26, 34, {"head": {"lean": 16, "tilt": 4}})),
            (24, w(74, -32, 10, {"head": {"lean": 16, "tilt": 4}})), (29, w(72, -30, 20)), (33, w(72, -30, 20))]

def act_salute(B):
    up = {"arm.L": {"swing": 40, "out": 105}, "hand.L": {"swing": 30, "twist": 20}, "spine": {"lean": -8}, "head": {"lean": -6},
          "root": {"loc": (0, 0, 0.01)}}
    return [(1, _base(B)), (7, _base(B, {**up, "root": {"loc": (0, 0, 0.03), "scale": (0.97, 0.97, 1.04)}})),
            (10, _base(B, up)), (24, _base(B, up)),
            (30, _base(B, {"arm.L": {"swing": 20, "out": 40}, "root": {"scale": (1.03, 1.03, 0.97)}})), (37, _base(B))]

def act_polish(B):
    lean = {"spine": {"lean": 24}, "head": {"lean": 6}, "root": {"loc": (0, 0, -0.01)}, "arm.L": {"swing": 40, "out": -6},
            "hand.L": {"swing": 15}}
    def rub(sw, out, tw, sc):
        return _base(B, {**lean, "arm.R": {"swing": sw, "out": out}, "hand.R": {"twist": tw, "swing": -95},
                         "spine": {"lean": 24, "twist": tw * 0.3}, "root": {"loc": (0, 0, -0.01), "scale": sc}})
    return [(1, rub(44, -6, -12, (1.0, 1.0, 1.0))), (7, rub(54, -16, 0, (1.02, 1.02, 0.97))),
            (13, rub(44, -26, 12, (1.0, 1.0, 1.0))), (19, rub(36, -16, 0, (1.02, 1.02, 0.97))), (25, rub(44, -6, -12, (1.0, 1.0, 1.0)))]

def act_point(B):
    pt = {"arm.L": {"swing": 88, "out": 14}, "hand.L": {"swing": 6}, "spine": {"lean": 6, "twist": -12}, "head": {"lean": -4, "twist": -6},
          "arm.R": {"swing": -10}}
    return [(1, _base(B)), (6, _base(B, {**pt, "root": {"scale": (1.04, 1.04, 0.95)}})), (9, _base(B, {**pt, "arm.L": {"swing": 94, "out": 14}})),
            (24, _base(B, pt)), (31, _base(B))]

def act_wave(B):
    def up(h):
        return _base(B, {"arm.L": {"out": 150, "swing": 10}, "hand.L": {"out": h}, "head": {"tilt": -6}, "spine": {"tilt": 4}})
    return [(1, _base(B)), (6, up(0)), (10, up(28)), (14, up(-24)), (18, up(28)), (22, up(-24)), (26, up(0)), (35, _base(B))]

def _prop_side(B, piece, default):
    for pc in B.P.get("costume", []):
        if pc.get("piece") == piece:
            return pc.get("hand", default)
    return default

def _for_prop(fn, piece, designed):
    """Wrap an action designed with `piece` in the `designed` hand: mirror it when the character
    holds the prop in the other hand, so the prop hand always does the work."""
    def f(B):
        keys = fn(B)
        if _prop_side(B, piece, designed) != designed:
            keys = [(fr, kit.mirror(pose)) for fr, pose in keys]
        return keys
    return f

kit.ACTIONS.update({"march": (_for_prop(act_march, "clipboard", "L"), True),
                    "write": (_for_prop(act_write, "clipboard", "L"), True),
                    "salute": (_for_prop(act_salute, "clipboard", "L"), False),
                    "polish": (_for_prop(act_polish, "cloth_club", "R"), True),
                    "point": (_for_prop(act_point, "cloth_club", "R"), False),
                    "wave": (_for_prop(act_wave, "cloth_club", "R"), False)})
