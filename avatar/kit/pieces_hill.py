"""Kit pieces for The Hill's people (standard body): the Gnome Foreman and the Caveman.

Headwear: `cone_hat` (teal cone + detachable tiny hard hat), `ice_cube`.
Costume:  `gnome_beard`, `vest_stripes`, `clipboard` (part `prop`), `whistle`,
          `mane_beard`, `fur_tunic`, `cloth_club` (part `prop`).
Actions:  `march`, `write`, `salute`, `whistle` (gnome); `polish`, `point`, `wave` (caveman).
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
    return B.torso_point(t, th, grow)

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
    """Held piece (hold style one_hand_low): the fist closes on the board's inner edge, the board
    faces front and sticks out to the side of the hand. Modelled in hand-slot axes (avatar/kit/hold.py)."""
    import hold
    side = piece.get("hand", "L"); s = 1 if side == "L" else -1
    wood = B.mats.flat("clipboard", piece.get("color", "#B07A3C"), rough=0.6, spec=0.3)
    paper = B.mats.flat("paper", piece.get("paper", "#FFFDF4"), rough=0.8, spec=0.2)
    clip = B.mats.flat("clip", piece.get("clip", "#F4F1E6"), rough=0.35, spec=0.5)
    B.cur_part = "prop"
    M = hold.piece_matrix(B, side)
    hw_, hh = 0.08, 0.10
    bc = Vector((s * (hw_ - 0.012), 0.0, 0.012))
    bone = f"hand.{side}"
    put = lambda bm, mat: B.add(xform(bm, M), mat, bone)
    put(rbox(bc, hw_, 0.008, hh), wood)
    pc = bc + Vector((0, -0.007, -0.006))
    put(rbox(pc, hw_ * 0.84, 0.003, hh * 0.86), paper)
    put(rbox(bc + Vector((0, -0.008, hh * 0.95)), 0.03, 0.009, 0.013), clip)
    for k, ln in enumerate((0.85, 0.6, 0.75, 0.4)):   # scribble lines
        z = pc.z + hh * 0.5 - k * 0.032
        x0 = pc.x - hw_ * 0.62
        put(rbox((x0 + hw_ * 0.62 * ln, pc.y - 0.0035, z), hw_ * 0.62 * ln, 0.0015, 0.0045, power=4, segs=12), wood)
    B.cur_part = None

WHISTLE_R = 0.026        # drum radius (chunky toy referee whistle)

def _whistle_local(r):
    """The whistle's own frame (rest pose, centred on the drum): drum axis Y (faces the camera),
    the flat mouthpiece sticks out along `m` (down and to the character's left), the ring sits on
    top. Returns m, n (mouthpiece 'up'), the mouthpiece length, its tip and the ring centre, relative to the drum."""
    m = Vector((math.cos(math.radians(-32)), 0, math.sin(math.radians(-32))))
    n = Vector((-m.z, 0, m.x))
    k = r / WHISTLE_R
    ml = 0.046 * k
    tip = m * (r * 0.55 + ml) + n * (r - 0.0105 * k)
    ring = Vector((-0.22, 0, 0.975)).normalized() * (r + 0.009 * k)
    return m, n, ml, tip, ring

def whistle(B, piece):
    """A chunky referee whistle on a cord, hanging on his chest just below the beard tip: a short
    drum (axis toward the camera) with a flat mouthpiece out to one side, a slot on top, a ring on
    the top of the drum. Its own bone `whistle`; the cord is two straight segments on `cord.L` /
    `cord.R` from the sides of the neck (under the beard edges) to the ring, so the `whistle` action
    can lift it to his mouth and aim / stretch the cord. All three bones are children of `head`,
    like the beard, so the whistle always stays under the beard tip."""
    L = B.L; R, c = L["R"], L["head_c"]
    yel = B.mats.flat("whistle", piece.get("color", "#FFD23F"), rough=0.3, spec=0.6)
    slot = B.mats.flat("whistle_slot", piece.get("slot", kit.shade(piece.get("color", "#FFD23F"), 0.45)), rough=0.5, spec=0.3)
    cord = B.mats.flat("whistle_cord", piece.get("cord", "#B07A3C"), rough=0.7, spec=0.2)
    r = WHISTLE_R * piece.get("size", 1.0)
    m, n, ml, tip, ring = _whistle_local(r)
    bm = getattr(B, "beard_bm", None)
    tip_z = min(v.co.z for v in bm.verts) if bm else c.z - 1.6 * R
    rz = tip_z - piece.get("gap", 0.004)                      # ring centre just under the beard tip
    dz = rz - ring.z                                          # drum centre height
    tz = (dz - L["torso_z0"]) / (L["torso_z1"] - L["torso_z0"])
    front = min(B.torso_point(tz + d, -math.pi / 2).y for d in (-0.06, 0.0, 0.06))
    k = r / WHISTLE_R
    hd = 0.017 * k                                                # half depth of the drum
    W = Vector((piece.get("x", 0.0), front - hd - 0.006, dz))
    B.whistle_c = W.copy(); B.whistle_r = r
    B.whistle_lips = {}          # where the mouthpiece tip goes in the `whistle` action (rest pose)
    for s_, side in ((1, "L"), (-1, "R")):
        lx, lz = s_ * 0.12 * R, c.z - 0.60 * R
        hit = surface_y(bm, lx, lz) if bm else None
        B.whistle_lips[side] = Vector((lx, (hit.y if hit else -0.95 * R) + 0.008, lz))
    # drum: a short cylinder along Y with rounded edges
    drum = lathe([(-hd, 0, 0, 0, 0), (-hd, r * 0.84, r * 0.84, 0, 0), (-hd * 0.72, r, r, 0, 0),
                  (hd * 0.72, r, r, 0, 0), (hd, r * 0.84, r * 0.84, 0, 0), (hd, 0, 0, 0, 0)], 36, power=2.0)
    xform(drum, Matrix.Translation(W) @ Matrix.Rotation(-math.pi / 2, 4, "X"))   # axis Z -> Y
    B.add(drum, yel, "whistle")
    # flat mouthpiece, its top flush with the top of the drum
    mc = W + m * (r * 0.55 + ml * 0.5) + n * (r - 0.0105 * k)
    mp = rbox((0, 0, 0), 0.0105 * k, 0.0135 * k, ml * 0.5, power=6, segs=24)   # built along Z: x -> n, y -> Y, z -> m
    xform(mp, Matrix.Translation(mc) @ Matrix((n, (0, 1, 0), m)).transposed().to_4x4())
    B.add(mp, yel, "whistle")
    # the slot on top of the drum, next to the mouthpiece
    sc = W + n * (r * 0.98) + m * (r * 0.05)
    sl = rbox((0, 0, 0), 0.008 * k, 0.011 * k, 0.0035 * k, power=6, segs=16)
    xform(sl, Matrix.Translation(sc) @ Matrix((m, (0, 1, 0), n)).transposed().to_4x4())
    B.add(sl, slot, "whistle")
    # ring on top (facing the camera)
    rc_ = W + ring
    pts = [(rc_.x + 0.0085 * k * math.cos(a), rc_.y, rc_.z + 0.0085 * k * math.sin(a)) for a in [2 * math.pi * i / 20 for i in range(20)]]
    B.add(tube_bm(pts, 0.0032 * k, cyclic=True), yel, "whistle")
    B.extra_bones.append(("whistle", W.copy(), W + Vector((0, 0, 0.04))))
    # the cord: from the sides of the neck, under the beard edges, to the top of the ring
    ring_top = rc_ + Vector((0, 0, 0.0085 * k))
    B.whistle_ring = ring_top.copy()
    B.whistle_anchor = {}
    for s, side in ((1, "L"), (-1, "R")):
        a = Vector((s * piece.get("neck_x", 0.62) * R, -piece.get("neck_y", 0.46) * R, c.z - piece.get("neck_z", 1.05) * R))
        B.whistle_anchor[side] = a
        e = ring_top + Vector((s * 0.004, 0.0, 0.0))
        B.add(tube_bm([tuple(a), tuple(e)], 0.0036), cord, f"cord.{side}")
        B.extra_bones.append((f"cord.{side}", a.copy(), e.copy()))

# ------------------------------------------------------------------------------- the caveman
def mane_beard(B, piece):
    """The beard half of the caveman's hair mass: one shaggy shell round the jaw, wide enough
    to run into the `mane` at the sides, ending in ragged tufts on the chest. Params: `width`
    (x the face width, default 1.0), `length` (default 1.0), `tufts` (count), `shag` (how ragged
    the bottom edge is, default 0.3), `clumps` (extra hanging tuft lumps along the edge, default 0)."""
    L = B.L; R, c = L["R"], L["head_c"]
    mat = B.mats.flat("hair", piece["color"], rough=0.5, spec=0.4)
    rz = 0.62 * R * piece.get("length", 1.0)
    wid = piece.get("width", 1.0)
    tufts, shag = piece.get("tufts", 9), piece.get("shag", 0.30)
    cz = c + Vector((0, -0.12 * R, -0.92 * R))
    rx, ry = 1.22 * R * L["hsx"] * wid, 0.86 * R
    # a fat body (kit v2 belly / width) pushes the chest forward: lean the beard's lower half out
    # over it (the top stays round the mouth)
    push = 0.0
    zb = cz.z - rz * 0.75
    tz = (zb - L["torso_z0"]) / (L["torso_z1"] - L["torso_z0"])
    if 0.0 <= tz <= 1.0:
        push = -min(0.0, B.torso_point(tz, -math.pi / 2, 1.08).y - (cz.y - ry * 0.62))
    def ragged(co):
        a = math.atan2(co.y, co.x)
        co.x *= 1 + 0.03 * math.sin(a * 11 + co.z * 40)
        if co.z < 0:
            t = -co.z / rz
            co.x *= 1 - 0.30 * t ** 2
            co.y -= push * min(1.0, t / 0.75)
            co.z *= 1 + shag * t ** 3 * max(0.0, math.cos(a * tufts)) ** 2
        return co
    B.add(ellipsoid_bm(cz, (rx, ry, rz), segs=64, rings=32, deform=ragged), mat, "head")
    n = piece.get("clumps", 0)
    rnd = random.Random(7)
    for k in range(n):        # pointed tufts hanging from the front / side edge
        u = (k + 0.5) / n
        a = math.pi * (0.08 + 0.84 * u)                  # front half: from the left side round to the right
        x = -math.cos(a) * rx * 0.66
        y = -math.sin(a) * ry * 0.62
        z = cz.z - rz * (0.78 - 0.30 * abs(math.cos(a))) * rnd.uniform(0.96, 1.04)
        ln = R * rnd.uniform(0.40, 0.52) * (1.0 - 0.30 * abs(math.cos(a)))
        def point(co, ln=ln):
            if co.z < 0:
                f = (-co.z / ln)
                co.x *= 1 - 0.75 * f; co.y *= 1 - 0.6 * f
            return co
        rot = Euler((0.25 * math.sin(a) * 0, -0.35 * math.cos(a), 0)).to_matrix()
        B.add(ellipsoid_bm(Vector((x, y + cz.y - push * min(1.0, (cz.z - z) / rz / 0.75), z)), (R * 0.20, R * 0.15, ln), rot=rot, segs=18, rings=12, deform=point),
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
    """Held piece (hold style one_hand_raised): modelled upright, the stick passes through the fist
    and the cloth head is at the top; the hold pose (baked into the actions) carries it upright."""
    import hold
    side = piece.get("hand", "R")
    wood = B.mats.flat("club_stick", piece.get("stick", "#B07A3C"), rough=0.6, spec=0.3)
    cloth = B.mats.flat("club_cloth", piece.get("color", "#F3EAD2"), rough=0.9, spec=0.15)
    string = B.mats.flat("club_string", piece.get("string", "#1E9AA0"), rough=0.6, spec=0.3)
    bone = f"hand.{side}"
    B.cur_part = "prop"
    M = hold.piece_matrix(B, side, axis=(0, 0, 1))
    put = lambda bm, mat: B.add(xform(bm, M), mat, bone)
    put(capsule_bm((0, 0, -0.07), (0, 0, 0.27), 0.015, 0.014, segs=14, hem=3), wood)
    bc = Vector((0, 0, 0.34))
    def puff(co):
        co.x *= 1 + 0.06 * math.sin(co.z * 120); return co
    put(ellipsoid_bm(bc, (0.085, 0.08, 0.1), segs=28, rings=16, deform=puff), cloth)
    put(ellipsoid_bm(bc + Vector((0.02, -0.02, 0.05)), (0.04, 0.04, 0.035), segs=18, rings=10), cloth)
    zt = bc.z - 0.065
    pts = [(bc.x + 0.05 * math.cos(a), bc.y + 0.047 * math.sin(a), zt) for a in [2 * math.pi * i / 28 for i in range(28)]]
    put(tube_bm(pts, 0.007, cyclic=True), string)
    for d in (-1, 1):   # the knot's two ends
        a = Vector((bc.x + 0.03 * d, bc.y - 0.045, zt))
        put(tube_bm([tuple(a), tuple(a + Vector((0.012 * d, -0.012, -0.03)))], 0.005), string)
    B.cur_part = None

kit.HELD["clipboard"] = ("L", "one_hand_low")
kit.HELD["cloth_club"] = ("R", "one_hand_raised")
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

def _rig_of(B):
    """The armature being built (build() keys the actions before it sets B.rig)."""
    import bpy
    rig = getattr(B, "rig", None)
    if rig is not None:
        return rig
    for ob in bpy.data.objects:
        if ob.type == "ARMATURE" and ob.name.startswith(f"{B.prefix}{B.P['id']}") and ob.animation_data is None \
                and "whistle" in ob.data.bones:
            return ob
    return None

def _delta(rig, name):
    pb = rig.pose.bones[name]
    return pb.matrix @ pb.bone.matrix_local.inverted()

def _euler_deg(Rm):
    e = Rm.to_euler("XYZ")
    return {"lean": math.degrees(e.x), "tilt": math.degrees(e.y), "twist": math.degrees(e.z)}

def _stretch_scale(rig, name, k):
    """World-axis scale tuple that `apply_pose` maps to local Y = k (the bone's own axis)."""
    B3 = rig.data.bones[name].matrix_local.to_3x3()
    w = [max(range(3), key=lambda a: abs(B3.col[i][a])) for i in range(3)]
    if len(set(w)) < 3:
        return None
    out = [1.0, 1.0, 1.0]; out[w[1]] = k
    return tuple(out)

def _whistle_pose(B, rig, body, lift, side):
    """Pose dict for `lift` (0 hanging .. 1 at his mouth): body pose, the whistle bone placed so its
    mouthpiece meets the corner of his mouth, the free arm solved so the hand holds the drum, the
    cord bones aimed (and stretched) from the neck to the ring."""
    import bpy
    s = 1 if side == "L" else -1
    L = B.L; R, c = L["R"], L["head_c"]
    r = B.whistle_r; W0 = B.whistle_c
    m, n, ml, tip, ring = _whistle_local(r)
    pose = {k: dict(v) for k, v in body.items()}
    kit.apply_pose(rig, pose); bpy.context.view_layer.update()
    Dh = _delta(rig, "head")
    # target frame at the mouth: the mouthpiece comes in from the front, out to his free-hand side
    # the mouth is under the moustache, inside the beard: the mouthpiece tip goes just into the beard
    lips = Dh @ B.whistle_lips[side]
    out = (Dh.to_3x3() @ Vector((s * 0.42, -0.88, -0.10))).normalized()
    d_t = -out                                                  # drum -> lips
    a = Vector((0, 0, 1)).cross(d_t).normalized()
    if a.y > 0:
        a = -a
    if s < 0:
        a = -a
    F_t = Matrix((d_t, a, d_t.cross(a))).transposed()
    F_0 = Matrix((m, Vector((0, 1, 0)), m.cross(Vector((0, 1, 0))))).transposed()
    Rw_up = F_t @ F_0.inverted()
    pw_up = lips - Rw_up @ tip
    # rest (in world, following the head) and the lifted frame, blended
    rest = Dh @ Matrix.Translation(W0)
    up = Matrix.Translation(pw_up) @ Rw_up.to_4x4()
    q = rest.to_quaternion().slerp(up.to_quaternion(), lift)
    pw = rest.translation.lerp(up.translation, lift)
    Mw = Matrix.Translation(pw) @ q.to_matrix().to_4x4()        # the drum's world frame
    loc = Dh.inverted() @ Mw
    pose["whistle"] = {"loc": tuple(loc.translation - W0), **_euler_deg(loc.to_3x3())}
    # cord: from each neck anchor (on the head) to the ring
    ring_w = Mw @ (B.whistle_ring - W0)
    for cs, cside in ((1, "L"), (-1, "R")):
        bn = f"cord.{cside}"
        bone = rig.data.bones[bn]
        h0, t0 = bone.head_local.copy(), bone.tail_local.copy()
        tgt = Dh.inverted() @ ring_w + Vector((cs * 0.004, 0, 0))
        v0, v1 = (t0 - h0), (tgt - h0)
        Rm = v0.normalized().rotation_difference(v1.normalized()).to_matrix()
        e = _euler_deg(Rm)
        sc = _stretch_scale(rig, bn, v1.length / v0.length)
        if sc:
            e["scale"] = sc
        pose[bn] = e
    if lift <= 0:
        return pose
    # the free hand on the drum: hand centre ~1 cm below / outside the drum surface
    grip = Mw @ Vector((0, 0, 0)) - Vector((0, 0, 1)) * (r + 0.009) + Vector((s, 0, 0)) * 0.012 + out * 0.004
    hc0 = B.hand_c[side]
    an, hn = f"arm.{side}", f"hand.{side}"
    x = {"swing": 70.0, "out": 20.0, "twist": 0.0, "hswing": 0.0, "hout": 0.0, "k": 1.0}
    lim = {"swing": (-20, 175), "out": (-60, 110), "twist": (-80, 80), "hswing": (-60, 60), "hout": (-60, 60), "k": (1.0, 1.3)}
    bw = dict(pose.get(an, {}))
    def setp(x):
        p = dict(pose)
        e = dict(bw); e["swing"] = x["swing"]; e["out"] = x["out"]; e["twist"] = x["twist"]
        sc = _stretch_scale(rig, an, x["k"])
        if sc and x["k"] != 1.0:
            e["scale"] = sc
        p[an] = e
        he = {"swing": x["hswing"], "out": x["hout"]}
        hsc = _stretch_scale(rig, hn, 1.0 / x["k"])
        if hsc and x["k"] != 1.0:
            he["scale"] = hsc
        p[hn] = he
        return p
    def cost(x):
        kit.apply_pose(rig, setp(x)); bpy.context.view_layer.update()
        hc = _delta(rig, hn) @ hc0
        return (hc - grip).length + 0.02 * (x["k"] - 1.0)
    best = cost(x)
    for step in (24.0, 12.0, 6.0, 3.0, 1.5, 0.75):
        improved = True
        while improved:
            improved = False
            for key in x:
                for d in (-1, 1):
                    y = dict(x); y[key] = min(lim[key][1], max(lim[key][0], x[key] + d * step * (0.01 if key == "k" else 1.0)))
                    cy = cost(y)
                    if cy < best - 1e-6:
                        x, best, improved = y, cy, True
    B.whistle_grip_err = getattr(B, "whistle_grip_err", {}); B.whistle_grip_err[lift] = best
    return setp(x)

def act_whistle(B):
    """The free hand (not the clipboard hand) lifts the whistle off his chest to the corner of his
    mouth, two blows (cheeks puff), and lets it drop back. Frames 1-34; held at the mouth 9-24."""
    import bpy
    rig = _rig_of(B)
    side = "L" if _prop_side(B, "clipboard", "L") == "R" else "R"
    s = 1 if side == "L" else -1
    body = _base(B, {"head": {"lean": 6, "twist": s * 10, "tilt": s * 6}, "spine": {"lean": 2},
                     f"arm.{('R' if side == 'L' else 'L')}": {"swing": 18, "out": 2}})
    rest = _base(B)
    if rig is None or not hasattr(B, "whistle_c"):
        return [(1, rest), (34, rest)]
    half = _base(B, {"head": {"lean": 3, "twist": s * 5, "tilt": s * 3}, "spine": {"lean": 1},
                     f"arm.{('R' if side == 'L' else 'L')}": {"swing": 9, "out": 1}})
    k0 = _whistle_pose(B, rig, rest, 0.0, side)
    k1 = _whistle_pose(B, rig, half, 0.45, side)
    k2 = _whistle_pose(B, rig, body, 1.0, side)
    def blow(p, puff):
        p = {k: dict(v) for k, v in p.items()}
        p["root"] = {"scale": (1.0 + puff * 0.02, 1.0 + puff * 0.02, 1.0 - puff * 0.02)}
        return p
    kit.apply_pose(rig, {}); bpy.context.view_layer.update()
    return [(1, k0), (5, k1), (9, k2), (13, blow(k2, 1)), (16, k2), (20, blow(k2, 1)), (24, k2), (29, k1), (34, k0)]

def _prop_side(B, piece, default):
    for pc in B.P.get("costume", []):
        if pc.get("piece") == piece:
            return pc.get("hand", default)
    return default

def _for_prop(fn, piece, designed, hand_swing=0.0):
    """Wrap an action designed with `piece` in the `designed` hand: mirror it when the character
    holds the prop in the other hand, so the prop hand always does the work. `hand_swing` is added
    to the prop hand: the club used to stand up out of a hanging hand; now it runs through the fist
    (hold system), which is the same pose with the hand swung 90 degrees."""
    def f(B):
        keys = fn(B)
        side = _prop_side(B, piece, designed)
        if side != designed:
            keys = [(fr, kit.mirror(pose)) for fr, pose in keys]
        if hand_swing:
            out = []
            for fr, pose in keys:
                pose = dict(pose); e = dict(pose.get(f"hand.{side}", {}))
                e["swing"] = e.get("swing", 0.0) + hand_swing
                pose[f"hand.{side}"] = e
                out.append((fr, pose))
            keys = out
        return keys
    return f

kit.ACTIONS.update({"march": (_for_prop(act_march, "clipboard", "L"), True),
                    "write": (_for_prop(act_write, "clipboard", "L"), True),
                    "salute": (_for_prop(act_salute, "clipboard", "L"), False),
                    "whistle": (act_whistle, False),
                    "polish": (_for_prop(act_polish, "cloth_club", "R", 90.0), True),
                    "point": (_for_prop(act_point, "cloth_club", "R", 90.0), False),
                    "wave": (_for_prop(act_wave, "cloth_club", "R", 90.0), False)})
