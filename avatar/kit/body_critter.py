"""Body type `critter`: a small no-neck animal that stands upright (mole, hedgehog, penguin, owl, frog).

One pear: a head blob (bone `head`) sunk into a wider body blob (`spine`), no visible legs (the
`leg.L/R` bones are short stubs inside the body), small feet peeking out under the front, short arms
ending in big paws, an optional snout, tail, ears and a held prop on its own bone `prop` (child of
`spine`). Contract: avatar/README.md "Body types". Everything species-specific comes from the params:

    "body":  {"type": "critter", "height": 0.82,      # standard Jarlings (1.0 = 1.1 m)
              "width": 0.69, "depth": 0.88,           # widest width / height; front-back / side-side
              "widest": 0.33, "head": 0.205},         # height of the widest point, head radius (both / height)
    "skin":  "#56607A",                               # fur (also the face atlas background)
    "belly": {"color": "#8792AC", "size": 1.0} | null,
    "snout": {"style": "cone|button|beak|none", "color": ..., "length": 0.6, "tip": "#E0607A" | null},
    "paws":  {"style": "claws|mitts|flippers", "color": ..., "claws": 3},
    "feet":  {"color": ..., "size": 1.0},
    "tail":  {"style": "nub|none", "color": ...},
    "ears":  {"style": "none|round|tufts", "color": ...},
    "prop":  {"type": "shovel|none", "wood": ..., "steel": ...},   # held upright in both paws
    "face":  {"expression_list": [...], "eye_color": ..., "eyes": "dash|dot", "expressions": {name: {...}}}

Lengths below are fractions of the total height `T` unless noted.
"""
import math
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import jarling_kit as kit

CRITTER_DEFAULTS = {
    "id": "critter", "name": "Critter",
    "skin": "#56607A",
    "body": {"type": "critter", "build": "critter", "height": 0.82, "width": 0.69, "depth": 0.88,
             "widest": 0.33, "head": 0.205},
    "belly": {"color": "#8792AC", "size": 1.0},
    "snout": {"style": "cone", "color": "#F2A0A8", "length": 0.6, "tip": "#E0607A"},
    "paws": {"style": "claws", "color": "#F2A0A8", "claws": 3},
    "feet": {"color": "#F2A0A8", "size": 1.0},
    "tail": {"style": "nub", "color": "#F2A0A8"},
    "ears": {"style": "none"},
    "prop": {"type": "none"},
    "face": {"eye_color": "#2A1E2C", "eyes": "dash", "mouth": True,
             "expression_list": ["squint", "happy", "sorry", "hopeful", "startled"], "expressions": {}},
    "posture": {},
}
CRITTER_SLOTS = ["head", "face", "back", "waist", "hand_l", "hand_r", "foot_l", "foot_r"]
REF_HAND_R = (0.036 + 0.047 + 0.052) / 3      # the reference Jarling's mitten (mean radius)
REF_FOOT_W = 0.066                            # the reference Jarling's sneaker half-width

# Expression looks: eye shape + brows + mouth. Unknown names fall back to the resting face.
EXPR_LOOK = {
    "squint":   dict(eye="dash", tilt=0.0, brow=None, mouth="flat"),
    "neutral":  dict(eye="dash", tilt=0.0, brow=None, mouth="flat"),
    "happy":    dict(eye="arc", tilt=0.0, brow=None, mouth="smile"),
    "sorry":    dict(eye="dash", tilt=-0.08, brow=("worried", 0.04), mouth="wobble"),
    "hopeful":  dict(eye="dash", tilt=0.0, brow=("raised", 0.12), mouth="small_smile"),
    "startled": dict(eye="dot", tilt=0.0, brow=("raised", 0.06), mouth="o"),
}

def smoothstep(a, b, x):
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


class CritterBuilder(kit.Builder):
    def __init__(self, params, prefix=""):
        self.P = kit.deep_merge(CRITTER_DEFAULTS, params)
        self.P["body"]["build"] = "critter"
        self.prefix = prefix or ""
        self.mats = kit.Mats(f"{self.prefix}{self.P['id']}_")
        self.parts, self.part_tags, self.cur_part = [], [], None
        self.extra_bones, self.hat_parts = [], []
        self.coll = bpy.context.scene.collection

    # ------------------------------------------------------------------ layout: the pear profile
    def layout(self):
        B = self.P["body"]
        T = 1.1 * float(B.get("height", 0.82))
        w = 0.5 * float(B.get("width", 0.69)) * T          # widest radius
        hr = float(B.get("head", 0.205)) * T                # head radius
        zm = float(B.get("widest", 0.33)) * T
        hz = 1.05 * hr                                      # head is a touch taller than wide
        zc = T - hz
        L = dict(T=T, w=w, R=hr, hz=hz, zm=zm, zc=zc, d=float(B.get("depth", 0.88)), hunch=float(B.get("hunch", 0.0)) * T)
        L["head_c"] = Vector((0, -L["hunch"] * smoothstep(zm, T, zc), zc))
        L["zj"] = zm + (zc - zm) * 0.45                    # where the head blob sinks into the body
        L["sh_z"] = zm + (zc - zm) * 0.40
        self.L = L
        return L

    def r_pear(self, z):
        """Side-to-side radius of the whole pear at height z."""
        L = self.L
        w, hr, zm, zc, hz = L["w"], L["R"], L["zm"], L["zc"], L["hz"]
        if z <= zm:
            u = min(1.0, (zm - z) / zm)
            return w * max(0.0, 1 - u ** 2.6) ** (1 / 2.6)
        if z <= zc:
            return w - (w - hr) * smoothstep(zm, zc, z)
        u = min(1.0, (z - zc) / hz)
        return hr * math.sqrt(max(0.0, 1 - u * u))

    def cy(self, z):
        """Forward shift of the cross-section at height z (the hunch; -Y is front)."""
        L = self.L
        return -L["hunch"] * smoothstep(L["zm"], L["T"], z)

    def back_y(self, z):
        return self.r_pear(z) * self.L["d"] + self.cy(z)

    def front_y(self, z):
        return -self.r_pear(z) * self.L["d"] + self.cy(z)

    def ring(self, z, r, segs):
        return (z, r, r * self.L["d"], 0.0, self.cy(z))

    # ------------------------------------------------------------------ body + head
    def build_body(self):
        L, P = self.L, self.P
        T, zj = L["T"], L["zj"]
        fur = self.mats.flat("fur", P["skin"], rough=0.7, spec=0.25)
        self.skin = fur
        # body blob: the pear up to just above the junction, then a dome that closes inside the head
        rings = [(0.0, 0, 0, 0, 0)]
        n = 30
        top = zj + 0.04 * T
        for i in range(1, n + 1):
            t = i / n
            z = top * (1 - math.cos(math.pi * t / 2)) if t < 1 else top     # denser near the ground
            z = max(z, 0.002 * T)
            rings.append(self.ring(z, self.r_pear(z), 48))
        for k in range(1, 5):                         # dome tucked under the head surface
            a = k / 5 * math.pi / 2
            z = top + 0.06 * T * math.sin(a)
            rings.append(self.ring(z, self.r_pear(top) * 0.97 * math.cos(a), 48))
        rings.append((top + 0.06 * T, 0, 0, 0, 0))
        self.add(kit.lathe(rings, 48), fur, "spine")
        # belly oval: a shallow bulge on the front
        bl = P.get("belly")
        if bl and bl.get("color"):
            s = float(bl.get("size", 1.0))
            bz = L["zm"] * 0.95
            fy = self.front_y(bz)
            rz = 0.17 * T * s
            belly = kit.ellipsoid_bm((0, fy + 0.10 * T, bz), (0.175 * T * s, 0.10 * T + 0.014 * T, rz), segs=40, rings=24,
                                     floor=0.004)
            self.add(belly, self.mats.flat("belly", bl["color"], rough=0.7, spec=0.25), "spine")

    def build_head(self):
        L, P = self.L, self.P
        T, R, zc, zj = L["T"], L["R"], L["zc"], L["zj"]
        face = P["face"]
        fur_hex = P["skin"]
        img = kit.np_to_image(f"{self.mats.prefix}face", kit.face_atlas(face, fur_hex, draw=draw_critter_face))
        self.face_mat = self.mats.tex("face", img, rough=0.7, spec=0.25)
        self.face_mat["jarling_face_atlas"] = True
        self.expr_names = kit.expression_names(face)
        self.expr_uv = kit.expr_offsets(self.expr_names)
        # head blob: the pear's upper part, a hair proud of it, sinking under the body surface below zj
        off = 0.006 * T
        z_lo = zj - 0.03 * T
        rings = [(z_lo - 0.08 * T, 0, 0, 0, 0)]
        for k in range(1, 6):
            a = k / 6 * math.pi / 2
            z = z_lo - 0.08 * T * math.cos(a)
            rings.append(self.ring(z, (self.r_pear(z_lo) - 0.01 * T) * math.sin(a), 64))
        n = 30
        for i in range(n + 1):
            t = i / n
            z = z_lo + (T - z_lo) * math.sin(math.pi * t / 2)
            if z >= T - 1e-6:
                break
            o = -0.01 * T + (off + 0.01 * T) * smoothstep(z_lo, zj + 0.05 * T, z)
            rings.append(self.ring(z, self.r_pear(z) + o, 64))
        rings.append((T + off * 0.5, 0, 0, 0, self.cy(T)))
        bm = kit.lathe(rings, 64)
        uv = bm.loops.layers.uv.new("UVMap")
        k0 = 0.5 * (1 - 2 * kit.FACE_MARGIN)
        cols, rows = kit.expr_grid(len(self.expr_names))
        cu, cv_ = 1.0 / cols, 1.0 / rows
        corner = (cu * (0.5 + 0.97 * k0), 1 - cv_ + cv_ * (0.5 + 0.97 * k0))
        clamp = lambda x: max(-1.0, min(1.0, x))
        for f in bm.faces:
            fc = f.calc_center_median()
            front = f.normal.y < -0.3 and abs(fc.x) < 0.95 * R and abs(fc.z - zc) < 0.95 * R
            for lp in f.loops:
                co = lp.vert.co
                if front:
                    lp[uv].uv = (cu * (0.5 + clamp(co.x / R) * k0), 1 - cv_ + cv_ * (0.5 + clamp((co.z - zc) / R) * k0))
                else:
                    lp[uv].uv = corner
        self.add(bm, self.face_mat, "head")
        self.build_snout()
        self.build_ears()

    def head_surface(self, z):
        """Front surface point of the head at height z (centre line)."""
        return Vector((0, self.front_y(z) * 1.0 - 0.006 * self.L["T"], z))

    def build_snout(self):
        L, P = self.L, self.P
        sn = P.get("snout") or {}
        st = sn.get("style", "none")
        if st == "none":
            return
        T, R, zc = L["T"], L["R"], L["zc"]
        col = self.mats.flat("snout", sn.get("color", "#F2A0A8"), rough=0.5, spec=0.35)
        zb = zc + float(sn.get("z", -0.25)) * R          # base height on the face
        base = self.head_surface(zb) + Vector((0, 0.16 * R, 0))
        self.snout_z = zb
        if st == "button":
            self.add(kit.ellipsoid_bm(base + Vector((0, -0.06 * R, 0)), (0.22 * R, 0.16 * R, 0.17 * R)), col, "head")
            return
        length = float(sn.get("length", 0.6)) * R
        up = math.radians(float(sn.get("up_deg", 12)))
        d = Vector((0, -math.cos(up), math.sin(up)))
        rb, rt = float(sn.get("base", 0.45)) * R, float(sn.get("tip_r", 0.13)) * R
        rings = [(-0.02 * R, 0, 0, 0, 0)]
        for i in range(13):
            t = i / 12
            r = rt + (rb - rt) * (1 - t ** 1.6)
            rings.append((t * length, r, r * 0.88, 0, 0))
        for k in range(1, 5):                           # rounded tip
            a = k / 5 * math.pi / 2
            rings.append((length + rt * math.sin(a), rt * math.cos(a), rt * math.cos(a) * 0.92, 0, 0))
        rings.append((length + rt, 0, 0, 0, 0))
        bm = kit.lathe(rings, 32)
        q = Vector((0, 0, 1)).rotation_difference(d)
        bmesh.ops.transform(bm, matrix=Matrix.Translation(base) @ q.to_matrix().to_4x4(), verts=bm.verts)
        self.add(bm, col, "head")
        tip = sn.get("tip")
        if tip:
            tr = 0.16 * R
            self.add(kit.ellipsoid_bm(base + d * (length + rt * 0.35), (tr, tr * 0.95, tr * 0.9), segs=24, rings=14),
                     self.mats.flat("nose_tip", tip, rough=0.4, spec=0.45), "head")

    def build_ears(self):
        L, P = self.L, self.P
        ea = P.get("ears") or {}
        st = ea.get("style", "none") if isinstance(ea, dict) else ea
        if st == "none":
            return
        R, zc = L["R"], L["zc"]
        col = self.mats.flat("ears", ea.get("color", P["skin"]), rough=0.7, spec=0.25)
        for s in (-1, 1):
            if st == "tufts":
                c = Vector((s * 0.55 * R, 0, zc + 0.9 * R))
                self.add(kit.ellipsoid_bm(c, (0.12 * R, 0.08 * R, 0.30 * R), rot=Euler((0, s * -0.4, 0)).to_matrix()), col, "head")
            else:
                c = Vector((s * 0.7 * R, 0.05 * R, zc + 0.72 * R))
                self.add(kit.ellipsoid_bm(c, (0.22 * R, 0.10 * R, 0.22 * R)), col, "head")

    # ------------------------------------------------------------------ prop, arms, paws
    def plan_grip(self):
        """Where the held prop stands and where the two paws grab it (rest pose = holding it)."""
        L = self.L
        T = L["T"]
        zg = L["zm"] * 0.62
        hb = Vector((-0.07 * T, self.front_y(zg) - 0.11 * T, zg))       # handle bottom, his right
        top_z = L["zc"] - 0.02 * T
        bx = -(self.r_pear(top_z + 0.10 * T) + 0.075 * T)                    # blade beside the head
        ht = Vector((bx, self.front_y(top_z) - 0.10 * T, top_z))          # handle top (blade starts here)
        self.prop_axis = (hb, ht)
        a = (ht - hb).normalized()
        L_h = (ht - hb).length
        self.grips = {"R": hb + a * L_h * 0.20, "L": hb + a * L_h * 0.47}
        sh_z = L["sh_z"]
        sx = self.r_pear(sh_z) * 0.62
        sy = self.front_y(sh_z) * 0.75
        self.shoulders = {"L": Vector((sx, sy, sh_z)), "R": Vector((-sx, sy, sh_z))}

    def build_arms(self):
        L, P = self.L, self.P
        T = L["T"]
        paws = P.get("paws") or {}
        pcol = self.mats.flat("paws", paws.get("color", "#F2A0A8"), rough=0.5, spec=0.35)
        self.plan_grip()
        ar = 0.08 * T
        self.arm_pts, self.hand_c, self.hand_r = {}, {}, {}
        for s, side in ((1, "L"), (-1, "R")):
            sh = self.shoulders[side]
            g = self.grips[side]
            hc = g + Vector((s * 0.06 * T, 0.03 * T, 0.0))
            a = (hc - sh).normalized()
            wr = hc - a * 0.10 * T
            self.arm_pts[side] = (sh, wr)
            self.hand_c[side] = hc
            self.add(kit.capsule_bm(sh, wr, ar, ar * 0.9, segs=20, hem=5), self.skin, f"arm.{side}")
            # paddle mitt: palm plane holds the arm direction and the vertical
            up = Vector((0, 0, 1)); up = (up - a * up.dot(a)).normalized()
            wv = a.cross(up).normalized()          # broad side: across the arm, tipped to show the front
            tip = math.radians(-s * float(paws.get("tip_deg", 0)))
            wv, up = (wv * math.cos(tip) + up * math.sin(tip)).normalized(), (up * math.cos(tip) - wv * math.sin(tip)).normalized()
            rot = Matrix((up, a, wv)).transposed()  # local x = thickness (vertical), y = length, z = width
            self.cur_part = f"hand_{side.lower()}"
            rp = (0.07 * T, 0.115 * T, 0.12 * T)
            self.hand_r[side] = sum(rp) / 3
            self.add(kit.ellipsoid_bm(hc, rp, rot=rot, segs=28, rings=16), pcol, f"hand.{side}")
            n = int(paws.get("claws", 3)) if paws.get("style", "claws") == "claws" else 0
            for k in range(n):
                off = (k - (n - 1) / 2) * 0.078 * T
                c = hc + a * 0.115 * T + wv * off
                self.add(kit.ellipsoid_bm(c, (0.042 * T, 0.05 * T, 0.042 * T), rot=rot, segs=16, rings=10), pcol, f"hand.{side}")
            self.cur_part = None

    def build_prop(self):
        pr = self.P.get("prop") or {}
        if pr.get("type", "none") != "shovel":
            return
        T = self.L["T"]
        hb, ht = self.prop_axis
        a = (ht - hb).normalized()
        L_h = (ht - hb).length
        q = Vector((0, 0, 1)).rotation_difference(a).to_matrix().to_4x4()
        M = Matrix.Translation(hb) @ q
        wood = self.mats.flat("shovel_wood", pr.get("wood", "#B07A3C"), rough=0.6, spec=0.3)
        steel = self.mats.flat("shovel_steel", pr.get("steel", "#B8C4D0"), rough=0.35, spec=0.6)
        self.cur_part = "prop"
        def put(bm, mat):
            bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
            self.add(bm, mat, "prop")
        hr = 0.019 * T
        put(kit.capsule_bm((0, 0, -0.01 * T), (0, 0, L_h), hr, hr, segs=16, hem=3), wood)
        put(kit.ellipsoid_bm((0, 0, -0.012 * T), (0.03 * T, 0.03 * T, 0.024 * T), segs=16, rings=10), wood)   # knob
        put(kit.lathe([(L_h - 0.03 * T, 0, 0, 0, 0), (L_h - 0.03 * T, 0.022 * T, 0.022 * T, 0, 0),
                       (L_h + 0.04 * T, 0.026 * T, 0.024 * T, 0, 0), (L_h + 0.04 * T, 0, 0, 0, 0)], 20), steel)    # socket
        z0 = L_h + 0.03 * T
        prof = [(-0.004, 0.0, 0.0), (0.0, 0.050, 0.008), (0.012, 0.072, 0.010), (0.07, 0.078, 0.010),
                (0.14, 0.072, 0.009), (0.20, 0.048, 0.008), (0.235, 0.020, 0.006), (0.245, 0.0, 0.0)]
        blade = kit.lathe([(z0 + z * T, rx * T, ry * 2.2 * T, 0, 0) for z, rx, ry in prof], 40, power=2.0)
        for v in blade.verts:                       # a slight scoop: the edges curl forwards
            v.co.y -= 0.022 * T * (v.co.x / (0.078 * T)) ** 2
        put(blade, steel)
        self.prop_top = hb + a * (z0 + 0.245 * T)
        self.cur_part = None

    # ------------------------------------------------------------------ feet, tail
    def build_feet(self):
        L, P = self.L, self.P
        T = L["T"]
        ft = P.get("feet") or {}
        col = self.mats.flat("feet", ft.get("color", "#F2A0A8"), rough=0.5, spec=0.35)
        s = float(ft.get("size", 1.0))
        self.foot_c, self.foot_w = {}, 0.06 * T * s
        for sg, side in ((1, "L"), (-1, "R")):
            x = sg * 0.13 * T
            y = self.front_y(0.03 * T) * 0.85
            c = Vector((x, y, 0.03 * T * s))
            self.foot_c[side] = c
            self.cur_part = f"foot_{side.lower()}"
            self.add(kit.ellipsoid_bm(c, (self.foot_w, 0.085 * T * s, 0.036 * T * s), floor=0.0015, segs=24, rings=12),
                     col, f"foot.{side}")
            for k in (-1, 0, 1):                      # three toe bumps
                tc = c + Vector((k * 0.03 * T * s, -0.07 * T * s + abs(k) * 0.012 * T, -0.006 * T))
                self.add(kit.ellipsoid_bm(tc, (0.02 * T * s, 0.024 * T * s, 0.02 * T * s), floor=0.0015, segs=12, rings=8),
                         col, f"foot.{side}")
            self.cur_part = None

    def build_tail(self):
        L, P = self.L, self.P
        tl = P.get("tail") or {}
        if tl.get("style", "none") == "none":
            return
        T = L["T"]
        z = 0.09 * T
        c = Vector((0, self.back_y(z) - 0.002 * T, z))
        self.cur_part = "tail"
        self.add(kit.ellipsoid_bm(c, (0.035 * T, 0.038 * T, 0.033 * T), rot=Euler((math.radians(-25), 0, 0)).to_matrix(),
                                  segs=20, rings=12), self.mats.flat("tail", tl.get("color", "#F2A0A8"), rough=0.5, spec=0.35), "root")
        self.cur_part = None

    # ------------------------------------------------------------------ rig, slots
    def build_armature(self):
        L = self.L
        T = L["T"]
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
        bone("root", (0, 0, 0), (0, 0, 0.12 * T))
        bone("spine", (0, 0, 0.18 * T), (0, 0, L["zj"] - 0.04 * T), "root")
        bone("head", (0, 0, L["zj"] - 0.03 * T), (0, 0, T), "spine")
        for s, side in ((1, "L"), (-1, "R")):
            sh, wr = self.arm_pts[side]
            bone(f"arm.{side}", sh, wr, "spine")
            a = (wr - sh).normalized()
            bone(f"hand.{side}", wr, wr + a * 0.08 * T, f"arm.{side}")
            fc = self.foot_c[side]
            hip = (s * 0.13 * T, 0, 0.20 * T)
            ank = (fc.x, fc.y * 0.4, 0.06 * T)
            bone(f"leg.{side}", hip, ank, "root")
            bone(f"foot.{side}", ank, (fc.x, fc.y - 0.06 * T, 0.03 * T), f"leg.{side}")
        hb, ht = self.prop_axis
        bone("prop", hb, ht, "spine")
        bpy.ops.object.mode_set(mode="OBJECT")
        return ob

    def measure_slots(self):
        L = self.L
        T, R, zc = L["T"], L["R"], L["zc"]
        out = {}
        crown = max(co.z for co in self._cos({"head"})) - zc
        out["head"] = ("head", L["head_c"].copy(), (crown / kit.SLOT_REF["head_crown"],) * 3)
        ez = zc + 0.36 * R
        s = R / kit.SLOT_REF["face_r"]
        out["face"] = ("head", Vector((0, self.front_y(ez) - 0.006 * T, ez)), (s, s, s))
        zs = L["sh_z"]
        s = self.r_pear(zs) / kit.SLOT_REF["back_tw"]
        out["back"] = ("spine", Vector((0, self.back_y(zs), zs)), (s, s, s))
        zw = L["zm"] * 0.75
        rx = self.r_pear(zw); ry = rx * L["d"]
        out["waist"] = ("spine", Vector((0, self.cy(zw), zw)), (rx / kit.SLOT_REF["waist_rx"], ry / kit.SLOT_REF["waist_ry"], 1.0))
        for side in ("L", "R"):
            sl = side.lower()
            hs = self.hand_r[side] / REF_HAND_R
            out[f"hand_{sl}"] = (f"hand.{side}", self.hand_c[side].copy(), (hs,) * 3)
            fs = self.foot_w / REF_FOOT_W
            fc = self.foot_c[side]
            out[f"foot_{sl}"] = (f"foot.{side}", Vector((fc.x, fc.y, 0)), (fs,) * 3)
        return out

    def add_slots(self, rig, fit):
        bpy.context.view_layer.update()
        obs = {}
        for name in CRITTER_SLOTS:
            bone, pos, scale = fit[name]
            e = bpy.data.objects.new(f"{self.prefix}slot_{name}", None)
            e.empty_display_type = "ARROWS"; e.empty_display_size = 0.05
            self.coll.objects.link(e)
            e.parent = rig; e.parent_type = "BONE"; e.parent_bone = bone
            b = rig.data.bones[bone]
            e.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local @ Matrix.Translation((0, b.length, 0))).inverted()
            e.matrix_basis = Matrix.LocRotScale(pos, None, Vector(scale))
            e["jarling_slot"] = name
            e["jarling_build"] = "critter"
            e["jarling_id"] = self.P["id"]
            obs[name] = e
        bpy.context.view_layer.update()
        return obs

    # ------------------------------------------------------------------ actions
    def group(self, rx=0.0, rz=0.0, loc=(0, 0, 0)):
        """Pose entries that move both arms and the prop as one rigid unit (so the paws stay on the
        handle): rotate by rx (+ tips the top forwards, - lifts the paws) / rz about the shoulder line's centre, then shift."""
        R = Euler((math.radians(rx), 0, math.radians(rz)), "XYZ").to_matrix()
        c = (self.shoulders["L"] + self.shoulders["R"]) / 2
        I = Matrix.Identity(3)
        out = {}
        for name, h in (("arm.L", self.shoulders["L"]), ("arm.R", self.shoulders["R"]), ("prop", self.prop_axis[0])):
            t = (I - R) @ (c - h) + Vector(loc)
            e = {"loc": tuple(t)}
            if name == "prop":
                e.update(lean=rx, twist=rz)
            else:
                e.update(swing=-rx, twist=rz)
            out[name] = e
        return out

    def actions(self):
        T = self.L["T"]
        g = self.group
        def P(*ds):
            out = {}
            for d in ds:
                for k, v in d.items():
                    out.setdefault(k, {}).update(v)
            return out
        acts = {}
        acts["idle"] = [
            (1, P(g())),
            (13, P(g(loc=(0, 0, 0.004 * T)), {"root": {"loc": (0.008 * T, 0, 0)}, "spine": {"tilt": 1.5, "scale": (1.01, 1.01, 1.015)},
                                              "head": {"lean": -1.0, "tilt": -1.0}})),
            (25, P(g(loc=(0, 0, 0.008 * T)), {"spine": {"scale": (1.02, 1.02, 1.03)}, "head": {"lean": -2.5}})),
            (37, P(g(loc=(0, 0, 0.004 * T)), {"root": {"loc": (-0.008 * T, 0, 0)}, "spine": {"tilt": -1.5, "scale": (1.01, 1.01, 1.015)},
                                              "head": {"lean": -1.0, "tilt": 1.0}})),
            (49, P(g())),
        ]
        def step(sg, up):
            ft = "foot.L" if sg > 0 else "foot.R"
            return P(g(rx=-3 if up else 3, loc=(0, 0, 0.02 * T if up else 0)),
                     {"root": {"loc": (0, 0, 0.025 * T if up else 0), "scale": (0.97, 0.97, 1.04) if up else (1.04, 1.04, 0.95)},
                      "spine": {"lean": 6, "tilt": 7 * sg}, "head": {"lean": -3, "tilt": -4 * sg},
                      ft: {"loc": (0, -0.01 * T, 0.03 * T) if up else (0, 0, 0), "point": -15 if up else 0}})
        acts["run"] = [(1, step(1, False)), (5, step(1, True)), (9, step(-1, False)), (13, step(-1, True)), (17, step(1, False))]
        lift = g(rx=-12, loc=(0, -0.02 * T, 0.12 * T))
        acts["cheer"] = [
            (1, P(g(rx=-6, loc=(0, 0, 0.05 * T)), {"root": {"scale": (1.08, 1.08, 0.88)}, "head": {"lean": -4}})),
            (5, P(lift, {"root": {"loc": (0, 0, 0.10 * T), "scale": (0.94, 0.94, 1.09)}, "head": {"lean": -10}})),
            (8, P(lift, {"root": {"loc": (0, 0, 0.13 * T)}, "head": {"lean": -12, "tilt": 4}, "foot.L": {"point": 20}, "foot.R": {"point": 20}})),
            (11, P(lift, {"root": {"loc": (0, 0, 0.07 * T), "scale": (0.96, 0.96, 1.06)}, "head": {"lean": -8}})),
            (13, P(g(rx=-6, loc=(0, 0, 0.05 * T)), {"root": {"scale": (1.08, 1.08, 0.88)}, "head": {"lean": -4}})),
            (17, P(lift, {"root": {"loc": (0, 0, 0.10 * T), "scale": (0.94, 0.94, 1.09)}, "head": {"lean": -10}})),
            (20, P(lift, {"root": {"loc": (0, 0, 0.13 * T)}, "head": {"lean": -12, "tilt": -4}, "foot.L": {"point": 20}, "foot.R": {"point": 20}})),
            (23, P(lift, {"root": {"loc": (0, 0, 0.07 * T), "scale": (0.96, 0.96, 1.06)}, "head": {"lean": -8}})),
            (25, P(g(rx=-6, loc=(0, 0, 0.05 * T)), {"root": {"scale": (1.08, 1.08, 0.88)}, "head": {"lean": -4}})),
        ]
        down = -1.02 * T
        acts["popup"] = [
            (1, P(g(), {"root": {"loc": (0, 0, down), "scale": (0.9, 0.9, 1.1)}})),
            (4, P(g(), {"root": {"loc": (0, 0, down), "scale": (0.9, 0.9, 1.1)}})),
            (9, P(g(rx=-4, loc=(0, 0, 0.03 * T)), {"root": {"loc": (0, 0, 0.08 * T), "scale": (0.86, 0.86, 1.18)}, "head": {"lean": -8}})),
            (13, P(g(loc=(0, 0, -0.02 * T)), {"root": {"loc": (0, 0, 0), "scale": (1.14, 1.14, 0.84)}, "head": {"lean": 4}})),
            (17, P(g(rx=-2), {"root": {"loc": (0, 0, 0.01 * T), "scale": (0.96, 0.96, 1.05)}, "head": {"lean": -3}})),
            (21, P(g(), {"root": {"scale": (1.02, 1.02, 0.98)}})),
            (26, P(g())),
        ]
        acts["bow"] = [
            (1, P(g())),
            (8, P(g(rx=-8), {"spine": {"lean": 14}, "head": {"lean": 10}, "root": {"scale": (1.02, 1.02, 0.98)}})),
            (16, P(g(rx=-10), {"spine": {"lean": 17}, "head": {"lean": 13}, "root": {"scale": (1.02, 1.02, 0.98)}})),
            (22, P(g(rx=-2), {"spine": {"lean": -3}, "head": {"lean": -4}})),
            (28, P(g())),
        ]
        return acts

    # ------------------------------------------------------------------ build
    def build(self):
        self.layout()
        self.build_body()
        self.build_head()
        self.build_feet()
        self.build_arms()
        self.build_prop()
        self.build_tail()
        pid = self.P["id"]
        rig = self.build_armature()
        slot_fit = self.measure_slots()
        main = [p for p, t in zip(self.parts, self.part_tags) if t is None]
        body = self.make_mesh(f"{self.prefix}{pid}_body", main)
        body.parent = rig
        body.modifiers.new("Armature", "ARMATURE").object = rig
        self.part_obs = {}
        for tag in ["hand_l", "hand_r", "foot_l", "foot_r", "tail", "prop"]:
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
        rig["jarling_body_type"] = "critter"
        rig["jarling_loops"] = ["idle", "run", "cheer"]
        self.rig, self.body, self.hat = rig, body, None
        self.slots = self.add_slots(rig, slot_fit)
        rig["jarling_slots"] = list(self.slots.keys())
        kit.build_actions(rig, {}, self.prefix, acts=self.actions())
        return self


# ---------------------------------------------------------------------------- the face atlas cell
def draw_critter_face(face, expr, skin):
    """One atlas cell. Canvas units are head radii, origin at the head centre (see build_head)."""
    c = kit.FACE_CELL
    k0 = 0.5 * (1 - 2 * kit.FACE_MARGIN)
    cv = kit.Canvas(c, c, (-0.5 / k0, 0.5 / k0, -0.5 / k0, 0.5 / k0), skin)
    look = dict(EXPR_LOOK.get(expr, EXPR_LOOK["squint"]))
    look.update(face.get("expressions", {}).get(expr, {}))
    col = face.get("eye_color", "#2A1E2C")
    ey, ex, half, lw = float(face.get("eye_y", 0.36)), float(face.get("eye_spacing", 0.40)), 0.15, 0.085
    for sx in (-1, 1):
        sl, X, Y = cv.grid(sx * ex - 0.3, ey - 0.3, sx * ex + 0.3, ey + 0.45)
        if look["eye"] == "dash":
            t = look["tilt"]                       # + inner end lower; - outer end lower
            d = kit.sd_stroke(X, Y, [(sx * (ex - half), ey - t), (sx * (ex + half), ey + t)], lw)
        elif look["eye"] == "arc":
            d = kit.sd_stroke(X, Y, kit.bez((sx * ex - half, ey - 0.03), (sx * ex, ey + 0.11), (sx * ex + half, ey - 0.03)), lw)
        else:                                       # dot
            d = kit.sd_circle(X, Y, sx * ex, ey + 0.01, 0.062)
        cv.paint(sl, d, col)
        br = look.get("brow")
        if br:
            kind, raise_ = br
            by = ey + 0.17 + raise_
            if kind == "worried":                   # inner end up
                pts = [(sx * (ex - 0.12), by + 0.06), (sx * (ex + 0.08), by - 0.04)]
            else:                                   # raised, a gentle arch
                pts = kit.bez((sx * (ex - 0.10), by), (sx * ex, by + 0.05), (sx * (ex + 0.10), by))
            cv.paint(sl, kit.sd_stroke(X, Y, pts, 0.045), col)
    if face.get("mouth", True):
        my = float(face.get("mouth_y", -0.84))
        sl, X, Y = cv.grid(-0.25, my - 0.2, 0.25, my + 0.2)
        m = look.get("mouth", "flat")
        if m == "smile":
            d = kit.sd_stroke(X, Y, kit.bez((-0.09, my + 0.02), (0, my - 0.07), (0.09, my + 0.02)), 0.05)
        elif m == "small_smile":
            d = kit.sd_stroke(X, Y, kit.bez((-0.06, my + 0.01), (0, my - 0.04), (0.06, my + 0.01)), 0.048)
        elif m == "wobble":
            d = kit.sd_stroke(X, Y, [(-0.08, my - 0.03), (-0.03, my + 0.01), (0.03, my - 0.01), (0.08, my - 0.04)], 0.048)
        elif m == "o":
            d = kit.sd_ellipse(X, Y, 0, my - 0.01, 0.035, 0.045)
        else:
            d = kit.sd_stroke(X, Y, [(-0.05, my), (0.05, my)], 0.048)
        cv.paint(sl, d, col)
    return cv.img


kit.BODY_TYPES["critter"] = CritterBuilder
