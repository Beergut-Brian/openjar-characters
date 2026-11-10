"""The `giant` body type: a huge sitting beanbag creature (avatar/README.md "Body types").

A round head sunk into a bigger, wider round body with a flattened bottom, stubby arms resting on
the belly, big round feet out front with forward-facing sole pads, a thick tail curling round to
the front, optional tiny wings, horn nubs, back spines, a belly patch with soft stripes and a muzzle
bump. Everything character-specific comes from the params (`skin`, `body.height`, `face`, `giant`).

Sizes are fractions of U = body.height * 1.1 m (the top of the horn nubs). Blender axes: Z up,
faces -Y, +X is the character's left.
"""
import math
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix
import jarling_kit as kit

GIANT_DEFAULTS = {
    "shade": "#8C6FC8",
    "belly": {"on": True, "color": "#FFF0C9", "stripes": 4, "stripe_color": "#F0DAA6"},
    "horns": {"on": True, "color": "#FFF0C9"},
    "wings": {"on": True, "color": "#FFB37A"},
    "spines": {"on": True, "color": "#FFB37A", "count": 5},
    "tail": {"on": True, "side": "L", "puff": "#FFB37A", "spines": 3},
    "feet": {"pad": "#FFF0C9"},
    "muzzle": True,
}
FACE_DEFAULTS = {
    "eye_color": "#2A1E2C", "lid_color": "#8C6FC8", "cheek_color": "#F7A6C0",
    "lid": 0.55, "lid_tilt": -0.1, "blush": 0.6, "eye_spacing": 0.56,
}
# per-expression face spec (overridable through face.expressions)
GIANT_EXPR = {
    "sleepy":  dict(eye="lid", mouth="smile", brows=None),
    "yawn":    dict(eye="shut", mouth="yawn", brows=None, blush_add=0.1),
    "happy":   dict(eye="arc", mouth="smile_big", brows=None, blush_add=0.4),
    "sorry":   dict(eye="lid", lid=0.66, lid_tilt=-0.22, mouth="frown", brows="worried"),
    "hopeful": dict(eye="open", lid=0.0, look_up=0.05, mouth="smile", brows="raised", blush_add=0.15),
    "asleep":  dict(eye="closed", mouth="smile", brows=None),
}
SLOTS = ["head", "face", "back", "waist", "hand_l", "hand_r", "foot_l", "foot_r"]
K0 = 0.5 * (1 - 2 * kit.FACE_MARGIN)   # unit face coordinate -> fraction of an atlas cell


# ------------------------------------------------------------------------------------ face atlas
def draw_giant_face(face, name, skin):
    """One atlas cell. Face units: 1.0 = the head's vertical radius, origin at the head centre."""
    c = kit.FACE_CELL
    cv = kit.Canvas(c, c, (-0.5 / K0, 0.5 / K0, -0.5 / K0, 0.5 / K0), skin)
    spec = dict(lid=face["lid"], lid_tilt=face["lid_tilt"], blush_add=0.0, look_up=0.0)
    spec.update(GIANT_EXPR.get(name, GIANT_EXPR["sleepy"]))
    spec.update(face.get("expressions", {}).get(name, {}))
    eye_c, lid_c = face["eye_color"], face["lid_color"]
    ex, ey = face["eye_spacing"], 0.1
    # cheeks: exact colour, soft edge
    b = 0.75 + 0.5 * min(1.0, face["blush"] + spec["blush_add"])
    for s in (-1, 1):
        sl, X, Y = cv.grid(s * 0.74 - 0.36, -0.6, s * 0.74 + 0.36, 0.0)
        cv.paint(sl, kit.sd_ellipse(X, Y, s * 0.74, -0.27, 0.19 * b, 0.12 * b), face["cheek_color"], soft=0.02)
    for s in (-1, 1):
        cx, cy = s * ex, ey + spec["look_up"]
        rx, ry = 0.3, 0.22
        sl, X, Y = cv.grid(cx - 0.45, cy - 0.4, cx + 0.45, cy + 0.45)
        kind = spec["eye"]
        if kind in ("lid", "open"):
            if kind == "open":
                rx, ry = 0.24, 0.3
            E = kit.sd_ellipse(X, Y, cx, cy, rx, ry)
            lid = spec["lid"]
            slope = s * math.tan(spec["lid_tilt"])
            y0 = cy + ry - 2 * ry * lid
            d_lid = (Y - (y0 + (X - cx) * slope)) / math.sqrt(1 + slope * slope)
            vis = np.maximum(E, d_lid) if lid > 0.01 else E
            cv.paint(sl, vis, eye_c)
            top = y0 if lid > 0.01 else cy + ry
            hr = 0.07 if kind == "open" else 0.045
            cv.paint(sl, np.maximum(kit.sd_circle(X, Y, cx - rx * 0.3, top - hr * 1.6, hr), vis + 0.004), "#FFFFFF")
            if kind == "open":
                cv.paint(sl, np.maximum(kit.sd_circle(X, Y, cx + rx * 0.35, cy - ry * 0.2, 0.025), vis + 0.004), "#FFFFFF")
            if lid > 0.01:   # the heavy lid: shade colour over the top of the eye, lash line on its edge
                Eo = kit.sd_ellipse(X, Y, cx, cy, rx + 0.035, ry + 0.035)
                cv.paint(sl, np.maximum(Eo, -d_lid), lid_c)
                cv.paint(sl, np.maximum(np.abs(d_lid) - 0.024, Eo), eye_c)
        elif kind == "arc":     # happy: closed upward arches
            pts = kit.bez((cx - rx, cy - 0.03), (cx, cy + ry * 1.5), (cx + rx, cy - 0.03))
            cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.058), eye_c)
        elif kind == "shut":    # yawn: squeezed shut, slight arch
            pts = kit.bez((cx - rx, cy - 0.01), (cx, cy + ry * 0.9), (cx + rx, cy - 0.01))
            cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.052), eye_c)
        elif kind == "closed":  # asleep: lines curving down
            pts = kit.bez((cx - rx, cy + 0.01), (cx, cy - ry * 0.9), (cx + rx, cy + 0.01))
            cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.048), eye_c)
        if spec.get("brows"):
            by = cy + ry + 0.09 + (0.05 if spec["brows"] == "raised" else 0.0)
            if spec["brows"] == "worried":    # inner end higher
                pts = [(cx - s * 0.14, by + 0.06), (cx + s * 0.13, by - 0.02)]
            else:
                pts = kit.bez((cx - 0.14, by - 0.01), (cx, by + 0.06), (cx + 0.14, by - 0.01))
            cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.04, 0.03), eye_c)
    # nostrils on the muzzle
    for s in (-1, 1):
        sl, X, Y = cv.grid(s * 0.1 - 0.07, -0.26, s * 0.1 + 0.07, -0.1)
        cv.paint(sl, kit.sd_ellipse(X, Y, s * 0.1, -0.18, 0.036, 0.028), eye_c)
    my = -0.37
    sl, X, Y = cv.grid(-0.3, my - 0.25, 0.3, my + 0.12)
    m = spec["mouth"]
    if m in ("smile", "smile_big"):
        w = 0.1 if m == "smile" else 0.14
        pts = kit.bez((-w, my + 0.03), (0, my - 0.06 - (0.02 if m == "smile_big" else 0)), (w, my + 0.03))
        cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.034), eye_c)
    elif m == "frown":
        pts = kit.bez((-0.1, my - 0.05), (0, my + 0.04), (0.1, my - 0.05))
        cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.034), eye_c)
    elif m == "yawn":       # small round mouth, never teeth
        M = kit.sd_ellipse(X, Y, 0, my - 0.06, 0.11, 0.14)
        cv.paint(sl, M, eye_c)
        cv.paint(sl, np.maximum(kit.sd_ellipse(X, Y, 0, my - 0.17, 0.075, 0.055), M + 0.01), face["cheek_color"])
    return cv.img


# ------------------------------------------------------------------------------------ the builder
def sweep_rings(pts, radii, ring=28):
    """Ring vertex positions of a smooth tube through pts (parallel-transported frames, no twist)."""
    rows, prev_n = [], None
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        nrm = Vector((0, 0, 1)) - t * t.z if prev_n is None else prev_n - t * prev_n.dot(t)
        nrm.normalize(); prev_n = nrm
        bi = t.cross(nrm)
        rows.append([p + (nrm * math.cos(a) + bi * math.sin(a)) * radii[i]
                     for a in (2 * math.pi * j / ring for j in range(ring))])
    return rows


def sweep_bm(rows, axis):
    """An open tube (no end caps) from ring rows; outward from the axis points."""
    bm = bmesh.new()
    V = [[bm.verts.new(co) for co in r] for r in rows]
    ring = len(rows[0])
    for A, B in zip(V, V[1:]):
        for j in range(ring):
            bm.faces.new((A[j], A[(j + 1) % ring], B[(j + 1) % ring], B[j]))
    bm.normal_update()
    bm.faces.ensure_lookup_table(); f = bm.faces[0]
    if f.normal.dot(f.calc_center_median() - axis[0].lerp(axis[1], 0.5)) < 0:
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    return bm


def _orient_out(bm, out_dir):
    """Flip faces of an open sheet so their normals point along out_dir(face_center)."""
    flip = [f for f in bm.faces if f.normal.dot(out_dir(f.calc_center_median())) < 0]
    if flip:
        bmesh.ops.reverse_faces(bm, faces=flip)
    return bm


def _frame(e1, hint):
    e1 = e1.normalized()
    e3 = (hint - e1 * hint.dot(e1)).normalized()
    e2 = e3.cross(e1)
    return Matrix((e1, e2, e3)).transposed()   # columns: local x, y, z


class Giant(kit.Builder):
    def __init__(self, params, prefix=""):
        super().__init__(params, prefix)
        self.P["face"] = kit.deep_merge(FACE_DEFAULTS, params.get("face", {}))
        self.G = kit.deep_merge(GIANT_DEFAULTS, params.get("giant", {}))
        self.P["body"]["build"] = params.get("body", {}).get("build", "giant")
        self.U = float(self.P["body"].get("height", 6.0)) * 1.1
        self.hat_parts = []
        self.bones = {}          # name -> (head, tail, parent)

    # --- body profile (analytic, so decals and spines sit on the surface)
    def ring(self, z):
        """(rx, ry, cy) of the body cross-section at height z."""
        L = self.L
        s = max(-1.0, min(1.0, (z - L["bzc"]) / L["brz"]))
        c = math.sqrt(max(0.0, 1 - s * s))
        f = 1 + 0.05 * (-s)                    # a little wider low down: sits heavy
        return L["brx"] * c * f, L["bry"] * c * f, -0.02 * self.U * c

    def body_y(self, x, z, back=False):
        rx, ry, cy = self.ring(z)
        q = math.sqrt(max(0.0, 1 - (x / max(rx, 1e-6)) ** 2))
        return cy + ry * q if back else cy - ry * q

    def layout(self):
        U = self.U
        L = dict(h=self.U / 1.1)
        L["bzc"], L["brz"], L["brx"], L["bry"] = 0.25 * U, 0.32 * U, 0.39 * U, 0.33 * U
        L["head_c"] = Vector((0, -0.04 * U, 0.72 * U))
        L["hr"] = Vector((0.30 * U, 0.26 * U, 0.235 * U))
        L["R"] = L["hr"].x                    # framing radius (render_refs)
        self.L = L
        return L

    # --- head, muzzle, horns
    def face_uv(self, co):
        L = self.L; c = L["head_c"]; rz = L["hr"].z
        X = max(-0.495, min(0.495, (co.x - c.x) / rz * K0))
        Y = max(-0.495, min(0.495, (co.z - c.z) / rz * K0))
        return X, Y

    def build_head(self):
        P, L, U = self.P, self.L, self.U
        face = P["face"]
        img = kit.np_to_image(f"{self.mats.prefix}face", kit.face_atlas(face, P["skin"], draw=draw_giant_face))
        self.face_mat = self.mats.tex("face", img, rough=0.6, spec=0.3)
        self.face_mat["jarling_face_atlas"] = True
        self.skin = self.mats.flat("skin", P["skin"], rough=0.6, spec=0.3)
        self.expr_names = kit.expression_names(face)
        self.expr_uv = kit.expr_offsets(self.expr_names)
        cols, rows = kit.expr_grid(len(self.expr_names))
        cu, cv_ = 1.0 / cols, 1.0 / rows
        corner = (cu * (0.5 + 0.97 * K0), 1 - cv_ + cv_ * (0.5 + 0.97 * K0))
        c, hr = L["head_c"], L["hr"]

        def place(v):
            x, y, z = v.co
            jw = 1 + 0.05 * (-z)               # a touch fuller at the jowls
            v.co = Vector((x * hr.x * jw, y * hr.y, z * hr.z)) + c

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=40, radius=1.0)
        front = {f: -f.calc_center_median().y > 0.2 for f in bm.faces}
        for v in bm.verts:
            place(v)
        uv = bm.loops.layers.uv.new("UVMap")
        for f in bm.faces:
            for lp in f.loops:
                if front[f]:
                    X, Y = self.face_uv(lp.vert.co)
                    lp[uv].uv = (cu * (0.5 + X), 1 - cv_ + cv_ * (0.5 + Y))
                else:
                    lp[uv].uv = corner
        self.add(bm, self.face_mat, "head")
        if self.G["muzzle"]:
            mz = -0.30
            my = c.y - hr.y * math.sqrt(1 - mz * mz) + 0.022 * U
            m = kit.ellipsoid_bm((0, my, c.z + mz * hr.z), (0.12 * U, 0.05 * U, 0.088 * U), segs=32, rings=16)
            uv = m.loops.layers.uv.new("UVMap")
            for f in m.faces:
                for lp in f.loops:
                    X, Y = self.face_uv(lp.vert.co)
                    lp[uv].uv = (cu * (0.5 + X), 1 - cv_ + cv_ * (0.5 + Y))
            self.add(m, self.face_mat, "head")
        hn = self.G["horns"]
        if hn.get("on", True):
            mat = self.mats.flat("horns", hn["color"], rough=0.55)
            el, phi = math.radians(56), math.radians(72)
            for s in (-1, 1):
                base = c + Vector((s * hr.x * math.sin(phi) * math.cos(el), -hr.y * math.cos(phi) * math.cos(el),
                                   hr.z * math.sin(el)))
                nrm = Vector(((base - c).x / hr.x ** 2, (base - c).y / hr.y ** 2, (base - c).z / hr.z ** 2)).normalized()
                self.add(kit.ellipsoid_bm(base + nrm * 0.022 * U, (0.066 * U, 0.062 * U, 0.06 * U), segs=24, rings=14),
                         mat, "head")
        self.head_top = c.z + hr.z

    # --- body, belly patch, spines
    def build_body(self):
        L, U = self.L, self.U
        z0 = 0.0
        s0 = (z0 - L["bzc"]) / L["brz"]
        th0 = math.asin(max(-1.0, s0))
        rings = [(z0, 0.0, 0.0, 0, 0)]
        rx, ry, cy = self.ring(z0 + 1e-4)
        rings.append((z0, rx * 0.93, ry * 0.93, 0, cy))
        rings.append((z0 + 0.006 * U, rx * 0.985, ry * 0.985, 0, cy))
        n = 30
        for i in range(1, n + 1):
            th = th0 + (math.pi / 2 - th0) * i / n
            z = L["bzc"] + L["brz"] * math.sin(th)
            if i == n:
                rings.append((z, 0.0, 0.0, 0, 0))
            else:
                rx, ry, cy = self.ring(z)
                rings.append((z, rx, ry, 0, cy))
        self.add(kit.lathe(rings, 64), self.skin, "spine")
        self.build_belly()
        self.build_spines()

    def build_belly(self):
        b = self.G["belly"]
        if not b.get("on", True):
            return
        U = self.U
        bx, bz, a, h = 0.0, 0.25 * U, 0.215 * U, 0.235 * U
        th = 0.022 * U

        def disk(u, v):
            p, q = 2 * u - 1, 2 * v - 1
            return p * math.sqrt(1 - q * q / 2), q * math.sqrt(1 - p * p / 2)

        def pt(u, v):
            p, q = disk(u, v)
            x, z = bx + a * p, bz + h * q
            r2 = p * p + q * q
            off = th * max(0.0, 1 - r2) ** 0.45 - 0.006 * U
            return (x, self.body_y(x, z) - off, z)

        bm = kit.grid_bm(pt, 28, 32)
        uvl = bm.loops.layers.uv.new("UVMap")
        for f in bm.faces:
            for lp in f.loops:
                co = lp.vert.co
                lp[uvl].uv = (0.5 + (co.x - bx) / (2 * a), 0.5 + (co.z - bz) / (2 * h))
        bm.normal_update()
        _orient_out(bm, lambda p: Vector((0, -1, 0)))
        # stripes: a small texture, soft bands bowed downward in the middle
        W = 256
        cv = kit.Canvas(W, W, (0, 1, 0, 1), b["color"])
        sl, X, Y = cv.grid(0, 0, 1, 1)
        P2 = (2 * X - 1) ** 2
        R2 = P2 + (2 * Y - 1) ** 2
        n = int(b.get("stripes", 4))
        for i in range(n):
            t = 0.14 + 0.62 * i / max(1, n - 1) * 0.9
            d = np.abs(Y - (t - 0.05 * (1 - P2))) - 0.03
            d = np.maximum(d, (R2 - 0.62) * 0.2)
            cv.paint(sl, d, b["stripe_color"], soft=0.004)
        img = kit.np_to_image(f"{self.mats.prefix}belly", cv.img)
        self.add(bm, self.mats.tex("belly", img, rough=0.6), "spine")

    def surface_back(self, z, out=0.0):
        """Point on the back midline at height z and its outward normal."""
        L = self.L
        y = self.body_y(0.0, z, back=True)
        rx, ry, cy = self.ring(z)
        n = Vector((0, (y - cy) / max(ry, 1e-6) ** 2, (z - L["bzc"]) / L["brz"] ** 2)).normalized()
        return Vector((0, y, z)) + n * out, n

    def spine_bump(self, p, n, size, bone, mat):
        rot = _frame(n, Vector((1, 0, 0)))     # local x along the normal, local z sideways
        self.add(kit.ellipsoid_bm(p + n * size * 0.25, (size * 0.9, size, size * 0.6), rot=rot, segs=18, rings=10),
                 mat, bone)

    def build_spines(self):
        sp = self.G["spines"]
        if not sp.get("on", True):
            return
        U, L = self.U, self.L
        mat = self.mats.flat("spines", sp["color"], rough=0.55)
        c, hr = L["head_c"], L["hr"]
        for el in (38, 8):     # on the back of the head
            e = math.radians(el)
            n = Vector((0, math.cos(e) / hr.y, math.sin(e) / hr.z)).normalized()
            p = c + Vector((0, hr.y * math.cos(e), hr.z * math.sin(e)))
            self.spine_bump(p, n, 0.06 * U, "head", mat)
        k = int(sp.get("count", 5))
        for i in range(k):
            z = (0.50 - 0.38 * i / max(1, k - 1)) * U
            p, n = self.surface_back(z)
            self.spine_bump(p, n, (0.07 - 0.015 * i / max(1, k - 1)) * U, "spine", mat)

    # --- arms, legs, feet
    def build_arms(self):
        U = self.U
        self.arm_pts, self.hand_c = {}, {}
        for s, side in ((1, "L"), (-1, "R")):
            sh = Vector((s * 0.29 * U, -0.12 * U, 0.39 * U))
            wr = Vector((s * 0.31 * U, -0.23 * U, 0.31 * U))
            self.arm_pts[side] = (sh, wr)
            self.add(kit.capsule_bm(sh, wr, 0.08 * U, 0.072 * U, segs=24, hem=6), self.skin, f"arm.{side}")
            hc = wr + Vector((-s * 0.012 * U, -0.035 * U, -0.035 * U))
            self.hand_c[side] = hc
            self.cur_part = f"hand_{side.lower()}"
            self.hand_r = (0.075 * U, 0.072 * U, 0.08 * U)
            self.add(kit.ellipsoid_bm(hc, self.hand_r, segs=24, rings=14), self.skin, f"hand.{side}")
            self.add(kit.ellipsoid_bm(hc + Vector((-s * 0.045 * U, -0.03 * U, 0.025 * U)), (0.03 * U, 0.03 * U, 0.035 * U),
                                      segs=16, rings=10), self.skin, f"hand.{side}")   # mitten thumb
            self.cur_part = None
            self.bones[f"arm.{side}"] = (sh, wr, "spine")
            self.bones[f"hand.{side}"] = (wr, hc + Vector((0, 0, -0.06 * U)), f"arm.{side}")

    def build_legs(self):
        U = self.U
        pad = self.mats.flat("pads", self.G["feet"]["pad"], rough=0.6)
        self.foot_c = {}
        for s, side in ((1, "L"), (-1, "R")):
            hip = Vector((s * 0.16 * U, -0.08 * U, 0.15 * U))
            ank = Vector((s * 0.18 * U, -0.27 * U, 0.095 * U))
            self.add(kit.capsule_bm(hip, ank, 0.09 * U, 0.085 * U, segs=20, hem=5), self.skin, f"leg.{side}")
            fc = Vector((s * 0.19 * U, -0.31 * U, 0.098 * U))
            self.foot_c[side] = fc
            self.foot_r = (0.125 * U, 0.13 * U, 0.098 * U)
            self.cur_part = f"foot_{side.lower()}"
            bone = f"foot.{side}"
            self.add(kit.ellipsoid_bm(fc, self.foot_r, segs=28, rings=16, floor=0.0), self.skin, bone)
            fy = fc.y - self.foot_r[1]
            self.add(kit.ellipsoid_bm((fc.x, fy + 0.014 * U, fc.z - 0.004 * U), (0.088 * U, 0.022 * U, 0.07 * U),
                                      segs=24, rings=10), pad, bone)
            self.cur_part = None
            self.bones[f"leg.{side}"] = (hip, ank, "root")
            self.bones[f"foot.{side}"] = (ank, Vector((ank.x, fy, ank.z)), f"leg.{side}")

    # --- wings
    def build_wings(self):
        w = self.G["wings"]
        if not w.get("on", True):
            return
        U = self.U
        mat = self.mats.flat("wings", w["color"], rough=0.55)
        self.cur_part = "wings"
        for s, side in ((1, "L"), (-1, "R")):
            z = 0.47 * U
            root = Vector((s * 0.13 * U, self.body_y(0.13 * U, z, back=True) - 0.03 * U, z))
            d = Vector((s * 0.8, 0.25, 0.55)).normalized()
            rot = _frame(d, Vector((0, 1, 0)))
            e1, e2 = rot.col[0], rot.col[1]
            up = e2 if e2.z > 0 else -e2
            self.add(kit.ellipsoid_bm(root + d * 0.13 * U + up * 0.015 * U, (0.135 * U, 0.08 * U, 0.018 * U), rot=rot,
                                      segs=24, rings=12), mat, f"wing.{side}")
            for t in (0.09, 0.19):     # scalloped lower edge
                self.add(kit.ellipsoid_bm(root + d * t * U - up * 0.04 * U, (0.052 * U, 0.045 * U, 0.016 * U), rot=rot,
                                          segs=16, rings=10), mat, f"wing.{side}")
            self.add(kit.ellipsoid_bm(root + d * 0.25 * U + up * 0.03 * U, (0.04 * U, 0.035 * U, 0.02 * U), rot=rot,
                                      segs=16, rings=10), mat, f"wing.{side}")   # rounded tip knob
            self.bones[f"wing.{side}"] = (root, root + d * 0.27 * U, "spine")
        self.cur_part = None

    # --- tail
    def build_tail(self):
        t = self.G["tail"]
        if not t.get("on", True):
            return
        U = self.U
        s = 1 if t.get("side", "L") == "L" else -1
        # one smooth arc hugging the body: from inside the lower back, round the side, to the front
        n, ring = 72, 28
        th0, th1 = math.radians(-8), math.radians(122)
        pts, rr = [], []
        for i in range(n + 1):
            u = i / n
            th = th0 + (th1 - th0) * u
            r = (0.115 - 0.06 * u ** 0.9) * U                     # tapers toward the tip
            emerge = min(1.0, u / 0.22)                           # starts deep inside the body
            emerge = (1 - math.cos(math.pi * emerge)) / 2
            rx, ry, cy = self.ring(r)
            ox = rx + r * 0.55 + 0.07 * U * u * u
            oy = ry + r * 0.55 + 0.03 * U * u * u
            k = 0.45 + 0.55 * emerge
            pts.append(Vector((s * ox * k * math.sin(th), cy + oy * k * math.cos(th), r * (1.0 + 0.25 * (1 - emerge)) + 0.002 * U)))
            rr.append(r)
        cuts = [0, n // 3, 2 * n // 3, n]
        self.cur_part = "tail"
        rows = sweep_rings(pts, rr, ring)
        for k in range(3):
            a, b = cuts[k], cuts[k + 1]
            bone = f"tail.{k + 1}"
            self.add(sweep_bm(rows[a:b + 1], pts[a:b + 1]), self.skin, bone)
            self.bones[bone] = (pts[a].copy(), pts[b].copy(), "root" if k == 0 else f"tail.{k}")
        # spines along the top of the tail
        mat = self.mats.flat("spines", self.G["spines"]["color"], rough=0.55)
        ns = int(t.get("spines", 3)) if self.G["spines"].get("on", True) else 0
        for i in range(ns):
            j = int(n * (0.18 + 0.5 * i / max(1, ns - 1)))
            p = pts[j] + Vector((0, 0, rr[j] * 0.85))
            bone = f"tail.{1 + min(2, sum(j >= c for c in cuts[1:3]))}"
            self.spine_bump(p, Vector((0, 0, 1)), (0.045 - 0.01 * i / max(1, ns - 1)) * U, bone, mat)
        # the soft puff at the tip, resting on the ground in front
        pm = self.mats.flat("puff", t["puff"], rough=0.7)
        end, prev = pts[-1], pts[-3]
        d = (end - prev); d.z = 0; d.normalize()
        pc = end + d * 0.045 * U
        pr = 0.085 * U
        pc.z = pr * 0.9
        side = Vector((-d.y, d.x, 0))
        for off, r in ((Vector((0, 0, 0)), 1.0), (d * 0.5 + side * 0.45, 0.68), (d * 0.5 - side * 0.45, 0.68),
                       (d * 0.7 + Vector((0, 0, 0.35)), 0.62)):
            self.add(kit.ellipsoid_bm(pc + off * pr, (pr * r,) * 3, segs=22, rings=12, floor=0.0), pm, "tail.3")
        self.cur_part = None

    # --- rig
    def build_armature(self):
        L, U = self.L, self.U
        pid = self.P["id"]
        arm = bpy.data.armatures.new(f"{self.prefix}{pid}_rig")
        ob = bpy.data.objects.new(f"{self.prefix}{pid}", arm)
        self.coll.objects.link(ob)
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode="EDIT")
        eb = arm.edit_bones
        allb = {"root": ((0, 0, 0), (0, 0, 0.12 * U), None),
                "spine": ((0, 0, 0.12 * U), (0, 0, 0.52 * U), "root"),
                "head": ((0, -0.02 * U, 0.53 * U), (0, -0.02 * U, self.head_top), "spine")}
        allb.update(self.bones)
        order = ["root", "spine", "head"] + [k for k in allb if k not in ("root", "spine", "head")]
        order.sort(key=lambda k: (k.count("."), k))     # parents first: root/spine/head, then limbs
        done = set()
        while len(done) < len(order):
            for name in order:
                h, t, par = allb[name]
                if name in done or (par and par not in done):
                    continue
                b = eb.new(name); b.head = tuple(h); b.tail = tuple(t); b.roll = 0.0
                if par:
                    b.parent = eb[par]; b.use_connect = False
                done.add(name)
        bpy.ops.object.mode_set(mode="OBJECT")
        return ob

    # --- equipment
    def measure_slots(self):
        L, U = self.L, self.U
        c, hr = L["head_c"], L["hr"]
        ref = kit.SLOT_REF
        out = {"head": ("head", c.copy(), (hr.z / ref["head_crown"],) * 3)}
        ey = 0.06
        fy = c.y - hr.y * math.sqrt(1 - ey * ey)
        out["face"] = ("head", Vector((0, fy, c.z + ey * hr.z)), (hr.x / ref["face_r"],) * 3)
        zs = 0.45 * U
        back, _n = self.surface_back(zs)
        rx, _ry, _cy = self.ring(zs)
        out["back"] = ("spine", back, (rx / ref["back_tw"],) * 3)
        zw = 0.22 * U
        rx, ry, cy = self.ring(zw)
        out["waist"] = ("spine", Vector((0, cy, zw)), (rx / ref["waist_rx"], ry / ref["waist_ry"], 1.0))
        hs = sum(self.hand_r) / 3 / 0.045
        fs = self.foot_r[0] / 0.066
        for side in ("L", "R"):
            out[f"hand_{side.lower()}"] = (f"hand.{side}", self.hand_c[side].copy(), (hs,) * 3)
            fc = self.foot_c[side]
            out[f"foot_{side.lower()}"] = (f"foot.{side}", Vector((fc.x, fc.y, 0)), (fs,) * 3)
        return out

    def add_slots(self, rig, fit):
        bpy.context.view_layer.update()
        obs = {}
        for name in SLOTS:
            bone, pos, scale = fit[name]
            e = bpy.data.objects.new(f"{self.prefix}slot_{name}", None)
            e.empty_display_type = "ARROWS"; e.empty_display_size = 0.05 * self.U
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
        self.build_legs()
        self.build_wings()
        self.build_tail()
        pid = self.P["id"]
        rig = self.build_armature()
        fit = self.measure_slots()
        main = [p for p, t in zip(self.parts, self.part_tags) if t is None]
        body = self.make_mesh(f"{self.prefix}{pid}_body", main)
        body.parent = rig
        body.modifiers.new("Armature", "ARMATURE").object = rig
        self.part_obs = {}
        for tag in ["hand_l", "hand_r", "foot_l", "foot_r", "wings", "tail"]:
            pp = [p for p, t in zip(self.parts, self.part_tags) if t == tag]
            if not pp:
                continue
            ob = self.make_mesh(f"{self.prefix}{pid}_part_{tag}", pp)
            ob.parent = rig
            ob.modifiers.new("Armature", "ARMATURE").object = rig
            ob["jarling_part"] = tag
            self.part_obs[tag] = ob
        body["jarling_expressions"] = {k: list(v) for k, v in self.expr_uv.items()}
        rig["jarling"] = 1
        rig["jarling_body_type"] = "giant"
        self.rig, self.body, self.hat = rig, body, None
        self.slots = self.add_slots(rig, fit)
        rig["jarling_slots"] = list(self.slots.keys())
        acts, loops = giant_actions(self.P.get("posture", {}), self.U, set(self.bones))
        rig["jarling_loops"] = loops
        kit.build_actions(rig, self.P.get("posture", {}), self.prefix, acts=acts)
        return self


# --------------------------------------------------------------------------------------- actions
def giant_actions(posture, U, have):
    """Slow and soft: 'everything takes two seconds'. Returns ({name: keys}, loop names)."""
    sl, hl = posture.get("spine_lean", 0.0), posture.get("head_lean", 0.0)

    def P(extra=None):
        p = {"spine": {"lean": sl}, "head": {"lean": hl}, "arm.L": {"out": 4}, "arm.R": {"out": 4}}
        for k, v in (extra or {}).items():
            if k not in have and k not in ("root", "spine", "head"):
                continue
            cur = dict(p.get(k, {}))
            for kk, vv in v.items():
                cur[kk] = vv if isinstance(vv, tuple) else cur.get(kk, 0.0) + vv
            p[k] = cur
        return p

    def wings(a):          # a > 0 raises both wings
        return {"wing.L": {"tilt": -a}, "wing.R": {"tilt": a}}

    def breathe(k, head=-1.5):
        return {"root": {"scale": (1 + 0.012 * k, 1 + 0.012 * k, 1 + 0.02 * k)}, "head": {"lean": head * k}}

    acts = {}
    acts["idle"] = [
        (1, P()),
        (25, P({**breathe(0.6), "tail.3": {"twist": 2}})),
        (49, P({**breathe(1.0), "arm.L": {"out": 2}, "arm.R": {"out": 2}, **wings(4)})),
        (61, P({**breathe(0.8), "tail.3": {"twist": -6, "tilt": 3}})),
        (67, P({**breathe(0.6), "tail.3": {"twist": 5}})),
        (73, P({**breathe(0.45), "tail.3": {"twist": -3}})),
        (97, P()),
    ]
    sway = {"root": {"tilt": 4, "loc": (0.03 * U, 0, 0)}, "spine": {"tilt": -1.5}, "head": {"tilt": -2.5},
            "leg.R": {"swing": 6}, "foot.R": {"point": -8}, "arm.L": {"out": 6}, "tail.2": {"twist": -4}}
    mid = {"root": {"loc": (0, 0, 0.012 * U), "scale": (0.99, 0.99, 1.015)}, "head": {"lean": -1}}
    acts["run"] = [(1, P(sway)), (13, P(mid)), (25, P(kit.mirror(sway))), (37, P(mid)), (49, P(sway))]
    up = {"arm.L": {"out": 35, "swing": 12}, "arm.R": {"out": 35, "swing": 12}}
    acts["cheer"] = [
        (1, P({**up, **wings(10), "root": {"scale": (1.02, 1.02, 0.98)}, "head": {"tilt": 4}})),
        (7, P({**up, **wings(32), "root": {"tilt": 3, "scale": (0.99, 0.99, 1.02)}, "head": {"tilt": 6, "lean": -4},
               "hand.L": {"twist": 15}, "hand.R": {"twist": -15}, "tail.3": {"twist": 8}})),
        (13, P({**up, **wings(10), "root": {"scale": (1.02, 1.02, 0.98)}, "head": {"tilt": -4}})),
        (19, P({**up, **wings(32), "root": {"tilt": -3, "scale": (0.99, 0.99, 1.02)}, "head": {"tilt": -6, "lean": -4},
                "hand.L": {"twist": -15}, "hand.R": {"twist": 15}, "tail.3": {"twist": -8}})),
        (25, P({**up, **wings(10), "root": {"scale": (1.02, 1.02, 0.98)}, "head": {"tilt": 4}})),
    ]
    stretch = {"head": {"lean": -16}, "spine": {"lean": -5}, "arm.L": {"out": 72, "swing": 35}, "arm.R": {"out": 72, "swing": 35},
               "hand.L": {"twist": 10}, "hand.R": {"twist": -10}, "root": {"scale": (0.985, 0.985, 1.035)}, **wings(18),
               "tail.3": {"tilt": 4}}
    acts["yawn"] = [
        (1, P()),
        (16, P({**stretch, "head": {"lean": -9}, "arm.L": {"out": 30, "swing": 12}, "arm.R": {"out": 30, "swing": 12}})),
        (30, P(stretch)),
        (40, P({**stretch, "head": {"lean": -17}})),
        (56, P({"head": {"lean": 3}, "root": {"scale": (1.015, 1.015, 0.985)}})),
        (73, P()),
    ]
    wav = {"arm.R": {"out": 75, "swing": 20}, "head": {"tilt": -4}}
    acts["wave"] = [
        (1, P()),
        (16, P({**wav, "hand.R": {"out": -10}})),
        (28, P({**wav, "hand.R": {"out": 25}})),
        (40, P({**wav, "hand.R": {"out": -15}})),
        (52, P({**wav, "hand.R": {"out": 20}})),
        (73, P()),
    ]
    still = {"head": {"lean": -5}}
    acts["flap"] = [(1, P({**still, **wings(-8)})), (7, P({**still, **wings(38), "root": {"scale": (0.995, 0.995, 1.01)}})),
                    (13, P({**still, **wings(-8)})), (19, P({**still, **wings(38), "root": {"scale": (0.995, 0.995, 1.01)}})),
                    (25, P({**still, **wings(-8)})), (31, P({**still, **wings(38), "root": {"scale": (0.995, 0.995, 1.01)}})),
                    (37, P({**still, **wings(-8)})), (43, P({**still, **wings(38), "root": {"scale": (0.995, 0.995, 1.01)}})),
                    (49, P({**still, **wings(-8)}))]
    drop = {"head": {"lean": 20, "loc": (0, -0.01 * U, -0.035 * U)}, "spine": {"lean": 5}, "arm.L": {"out": -2},
            "arm.R": {"out": -2}, **wings(-6)}
    acts["sleep"] = [
        (1, P(drop)),
        (49, P({**drop, "root": {"scale": (1.03, 1.03, 0.975)}, "head": {"lean": 22, "loc": (0, -0.01 * U, -0.04 * U)}})),
        (97, P(drop)),
    ]
    return acts, ["idle", "run", "cheer", "flap", "sleep"]


kit.BODY_TYPES["giant"] = Giant
