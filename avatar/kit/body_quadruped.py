"""Body type `quadruped`: a farm animal or pet that walks on four legs (cow, pig, sheep, goat, dog, horse).

One rounded barrel body (bone `spine`), a Jarling-sized head blob low on the front with the standard
face atlas (bone `head`), four short stub legs with hooves or paws and a tail (`tail.1` > `tail.2`).
Contract: avatar/README.md "Body types". The shared eleven bones keep their meaning for game code:
`arm.L/R` > `hand.L/R` are the front legs and hooves, `leg.L/R` > `foot.L/R` the hind ones. There are
no hands, so the hand slots are missing (as the critter lacks knees); held things go in the `mouth`
slot (hold style `in_mouth`, avatar/kit/hold.py). Everything species-specific comes from the params:

    "body":  {"type": "quadruped", "height": 0.95,     # standard Jarlings (1.0 = 1.1 m), to the top of the head
              "length": 1.0, "girth": 0.27,             # barrel length and vertical radius (both / height)
              "width": 1.0, "leg": 0.24, "head": 0.22}, # side radius / girth, visible leg length, head radius
    "skin":  "#F4F1EA",                                 # coat (legs, head, face atlas background)
    "coat":  {"pattern": "patches|spots|none", "accent": "#2B2B33", "seed": 3, "amount": 5,
              "patches": [[deg, along, size], ...]},    # explicit patches (deg round the barrel, 90 = top;
                                                        # along -1 back .. 1 front; size / height)
    "snout": {"style": "muzzle|disc|none", "color": "#F2B8C0", "nostril": "#B85C70"},
    "ears":  {"style": "side|floppy|none", "color": ..., "inner": "#F2B8C0"},
    "horns": {"style": "nubs|none", "color": "#EFE2C4"},   # a body feature (part feature_horns), not a hat
    "hooves": {"style": "hooves|paws", "color": "#4A3B3B"},
    "tail":  {"style": "tuft|curl|nub|none", "color": ..., "tip": "#2B2B33"},
    "face":  {"expression_list": [...], "eye_color": ..., "lashes": true, "patch": [cx, cy, rx, ry] | null}

Lengths below are fractions of the total height `T` unless noted. Blender axes: -Y is the front.
"""
import math
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import jarling_kit as kit

QUAD_DEFAULTS = {
    "id": "quadruped", "name": "Quadruped",
    "skin": "#F4F1EA",
    "body": {"type": "quadruped", "build": "quadruped", "height": 0.95, "length": 1.0, "girth": 0.27,
             "width": 1.0, "leg": 0.24, "head": 0.22},
    "coat": {"pattern": "none", "accent": "#2B2B33", "seed": 3, "amount": 5},
    "snout": {"style": "muzzle", "color": "#F2B8C0", "nostril": "#B85C70"},
    "ears": {"style": "side", "inner": "#F2B8C0"},
    "horns": {"style": "none", "color": "#EFE2C4"},
    "hooves": {"style": "hooves", "color": "#4A3B3B"},
    "tail": {"style": "tuft", "tip": "#2B2B33"},
    "face": {"eye_color": "#2A1E2C", "lashes": False, "patch": None,
             "expression_list": ["neutral", "happy", "wide_eyed", "dizzy", "smug", "panicked"], "expressions": {}},
    "posture": {},
}
QUAD_SLOTS = ["head", "face", "back", "waist", "mouth"]
QUAD_ACTIONS = ["idle", "run", "cheer", "tipped", "stiff", "graze", "sit"]
QUAD_LOOPS = ["idle", "run", "cheer", "tipped", "stiff", "graze", "sit"]

# Expression looks. eye: open | arc | spiral; lid 0 open .. 0.6 heavy; iris radius; look = iris shift.
EXPR_LOOK = {
    "neutral":   dict(eye="open", sclera=0.15, iris=0.10, lid=0.30, brow=None, mouth="smile_small"),
    "happy":     dict(eye="arc", brow=None, mouth="smile", blush=True),
    "wide_eyed": dict(eye="open", sclera=0.18, iris=0.075, lid=0.0, brow=("raised", 0.10), mouth="o"),
    "dizzy":     dict(eye="spiral", brow=None, mouth="wobble"),
    "smug":      dict(eye="open", sclera=0.15, iris=0.10, lid=0.52, look=0.035, brow=("one_up", 0.06), mouth="smirk"),
    "panicked":  dict(eye="open", sclera=0.19, iris=0.055, lid=0.0, brow=("worried", 0.08), mouth="open", sweat=True),
}


def rot_front():
    """Lathe space (built along +z) -> body space: local z runs to the front (-Y), local y is up."""
    return Matrix.Rotation(math.radians(90), 4, "X")


def superend(t, n=2.6):
    return max(0.0, 1 - abs(t) ** n) ** (1 / n)


class QuadrupedBuilder(kit.Builder):
    def __init__(self, params, prefix=""):
        self.P = kit.deep_merge(QUAD_DEFAULTS, params)
        self.P["body"]["build"] = "quadruped"
        self.prefix = prefix or ""
        self.mats = kit.Mats(f"{self.prefix}{self.P['id']}_")
        self.parts, self.part_tags, self.cur_part = [], [], None
        self.extra_bones, self.hat_parts = [], []
        self.coll = bpy.context.scene.collection

    # ------------------------------------------------------------------ layout
    def layout(self):
        B = self.P["body"]
        T = 1.1 * float(B.get("height", 0.95))
        Lb = float(B.get("length", 1.0)) * T              # barrel length, end to end
        g = float(B.get("girth", 0.27)) * T                # vertical radius
        w = g * float(B.get("width", 1.0))                 # side radius
        leg = float(B.get("leg", 0.24)) * T
        R = float(B.get("head", 0.22)) * T
        zb = leg + g * 0.92                                # barrel centre height (legs tuck in a little)
        hz = T - R
        hy = -Lb / 2 + 0.10 * R                            # head centre: on the front of the barrel
        L = dict(T=T, Lb=Lb, g=g, w=w, leg=leg, R=R, zb=zb, hz=hz, hy=hy)
        L["head_c"] = Vector((0, hy, hz))
        L["lr"] = 0.30 * g                                 # leg radius
        L["leg_x"] = 0.56 * w
        L["front_y"], L["hind_y"] = -0.30 * Lb, 0.31 * Lb
        L["hoof_h"] = 0.075 * T
        self.L = L
        return L

    def barrel_r(self, zl):
        """(side, vertical) radius of the barrel at lathe coordinate zl (-Lb/2 back .. +Lb/2 front)."""
        L = self.L
        f = superend(zl / (L["Lb"] / 2))
        return L["w"] * f, L["g"] * f

    # ------------------------------------------------------------------ barrel + coat pattern
    def coat_patches(self):
        L, co = self.L, self.P.get("coat") or {}
        if co.get("pattern", "none") == "none":
            return []
        if co.get("patches"):
            src = co["patches"]
        else:
            rng = np.random.RandomState(int(co.get("seed", 3)))
            n = int(co.get("amount", 5))
            big = co.get("pattern") == "patches"
            src = [[float(rng.uniform(-30, 210)), float(rng.uniform(-0.8, 0.8)),
                    float(rng.uniform(0.13, 0.22) if big else rng.uniform(0.05, 0.08))] for _ in range(n)]
        out = []
        for deg, along, size in src:
            zl = along * L["Lb"] / 2
            rx, ry = self.barrel_r(zl)
            a = math.radians(deg)
            out.append((np.array([rx * math.cos(a), ry * math.sin(a), zl]), size * L["T"], deg))
        return out

    def coat_image(self, W=1024, H=512):
        L, P = self.L, self.P
        co = P.get("coat") or {}
        img = np.empty((H, W, 3), np.float32); img[:] = kit.hex_rgb(P["skin"])
        patches = self.coat_patches()
        if not patches:
            return None
        u = (np.arange(W) + 0.5) / W; v = (np.arange(H) + 0.5) / H
        U, V = np.meshgrid(u, v[::-1])
        th = 2 * np.pi * U
        zl = (V - 0.5) * L["Lb"]
        f = np.maximum(0.0, 1 - np.abs(zl / (L["Lb"] / 2)) ** 2.6) ** (1 / 2.6)
        X, Y, Z = L["w"] * f * np.cos(th), L["g"] * f * np.sin(th), zl
        acc = np.array(kit.hex_rgb(co.get("accent", "#2B2B33")), np.float32)
        for k, (c, s, deg) in enumerate(patches):
            d = np.sqrt((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2) / s
            wob = 1 + 0.16 * np.sin(3.0 * np.arctan2(Y - c[1], Z - c[2]) + 1.7 * k) + 0.08 * np.sin(5.0 * np.arctan2(X - c[0], Z - c[2]) + k)
            a = np.clip((1.0 - d / wob) * 40.0, 0, 1)[..., None]
            img = img * (1 - a) + acc * a
        return kit.np_to_image(f"{self.mats.prefix}coat", np.clip(img, 0, 1))

    def build_body(self):
        L, P = self.L, self.P
        T, Lb = L["T"], L["Lb"]
        self.skin = self.mats.flat("coat_flat", P["skin"], rough=0.7, spec=0.25)
        co = P.get("coat") or {}
        wool = co.get("style") == "wool"
        img = None if wool else self.coat_image()
        coat = self.mats.tex("coat", img, rough=0.7, spec=0.25) if img else self.skin
        if wool:
            coat = self.mats.flat("wool", co.get("color", "#F2EEE4"), rough=0.9, spec=0.15)
        n, segs = 40, 64
        rings = [(-Lb / 2, 0, 0, 0, 0)]
        for i in range(1, n):
            t = -1 + 2 * i / n
            t = math.copysign(abs(t) ** 0.8, t)           # denser at the round ends
            zl = t * Lb / 2
            rx, ry = self.barrel_r(zl)
            rings.append((zl, rx, ry, 0, 0))
        rings.append((Lb / 2, 0, 0, 0, 0))
        bm = kit.lathe(rings, segs, power=2.2)
        uv = bm.loops.layers.uv.new("UVMap")
        for f in bm.faces:
            us = []
            for lp in f.loops:
                c = lp.vert.co
                rx, ry = self.barrel_r(c.z)
                th = math.atan2(c.y / max(ry, 1e-6), c.x / max(rx, 1e-6)) if (rx > 1e-6) else 0.0
                us.append(((th / (2 * math.pi)) % 1.0, c.z / Lb + 0.5, c))
            umax = max(x[0] for x in us)
            for lp, (uu, vv, c) in zip(f.loops, us):
                if umax - uu > 0.5:
                    uu += 1.0
                if abs(c.x) < 1e-6 and abs(c.y) < 1e-6:      # poles: take the face's mean u
                    uu = sum(x[0] for x in us) / len(us)
                lp[uv].uv = (uu, vv)
        bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L["zb"])) @ rot_front(), verts=bm.verts)
        self.add(bm, coat, "spine")
        if wool:                                          # fleece: a coat of soft lumps over the barrel
            for i in range(9):
                zl = (-0.84 + 1.68 * i / 8) * Lb / 2
                rx, ry = self.barrel_r(zl)
                for k in range(9):
                    a = math.radians(-35 + 250 * k / 8 + (12 if i % 2 else 0))
                    c = Vector((rx * math.cos(a), ry * math.sin(a), zl))
                    c = rot_front() @ c + Vector((0, 0, L["zb"]))
                    r = 0.085 * T * (0.8 + 0.4 * ((i * 7 + k * 3) % 5) / 4)
                    self.add(kit.ellipsoid_bm(c, (r, r, r * 0.9), segs=16, rings=10), coat, "spine")
            hc = L["head_c"]
            for k in range(5):                            # a tuft on the head
                a = math.radians(-60 + 30 * k)
                self.add(kit.ellipsoid_bm((0.45 * L["R"] * math.sin(a), hc.y + 0.1 * L["R"], hc.z + 0.82 * L["R"] + 0.1 * L["R"] * math.cos(a)),
                                          (0.24 * L["R"],) * 3, segs=16, rings=10), coat, "head")
        # neck: a soft blob from the top front of the barrel into the back of the head (follows the head)
        hc = L["head_c"]
        nk = kit.ellipsoid_bm((0, hc.y + 0.55 * L["R"], hc.z - 0.42 * L["R"]), (0.62 * L["w"], 0.55 * L["R"], 0.62 * L["R"]),
                              segs=40, rings=20)
        self.add(nk, self.skin, "head")

    # ------------------------------------------------------------------ head, snout, ears, horns
    def snout_geom(self):
        """Snout shape in head-radius units (front view): centre (x, z), half sizes, for the atlas."""
        st = (self.P.get("snout") or {}).get("style", "muzzle")
        if st == "muzzle":
            return dict(style=st, cz=-0.44, rx=0.60, rz=0.36, depth=0.42, fwd=0.80, nost=(0.24, -0.34, 0.07, 0.045), mouth=-0.64)
        if st == "disc":
            return dict(style=st, cz=-0.30, rx=0.36, rz=0.30, depth=0.24, fwd=0.96, nost=(0.12, -0.30, 0.05, 0.075), mouth=-0.74)
        return dict(style="none", mouth=-0.50)

    def build_head(self):
        L, P = self.L, self.P
        T, R = L["T"], L["R"]
        hc = L["head_c"]
        face = dict(P["face"])
        face["_snout"] = self.snout_geom()
        face["_snout_col"] = (P.get("snout") or {}).get("color", "#F2B8C0")
        face["_nostril"] = (P.get("snout") or {}).get("nostril", "#B85C70")
        face["_accent"] = (P.get("coat") or {}).get("accent", "#2B2B33")
        img = kit.np_to_image(f"{self.mats.prefix}face", kit.face_atlas(face, P["skin"], draw=draw_quad_face))
        self.face_mat = self.mats.tex("face", img, rough=0.7, spec=0.25)
        self.face_mat["jarling_face_atlas"] = True
        self.expr_names = kit.expression_names(face)
        self.expr_uv = kit.expr_offsets(self.expr_names)
        k0 = 0.5 * (1 - 2 * kit.FACE_MARGIN)
        cols, rows = kit.expr_grid(len(self.expr_names))
        cu, cv_ = 1.0 / cols, 1.0 / rows
        corner = (cu * (0.5 + 0.97 * k0), 1 - cv_ + cv_ * (0.5 + 0.97 * k0))
        clamp = lambda x: max(-1.0, min(1.0, x))
        def planar(lp, co):
            lp[uvl].uv = (cu * (0.5 + clamp(co.x / R) * k0), 1 - cv_ + cv_ * (0.5 + clamp((co.z - hc.z) / R) * k0))
        hd = kit.ellipsoid_bm(hc, (1.04 * R, 0.96 * R, R), segs=64, rings=32)
        uvl = hd.loops.layers.uv.new("UVMap")
        for f in hd.faces:
            fc = f.calc_center_median()
            front = f.normal.y < -0.3 and abs(fc.x) < 0.95 * R and abs(fc.z - hc.z) < 0.95 * R
            for lp in f.loops:
                if front:
                    planar(lp, lp.vert.co)
                else:
                    lp[uvl].uv = corner
        self.add(hd, self.face_mat, "head")
        sg = face["_snout"]
        if sg["style"] != "none":                         # the snout takes the face atlas too (planar), so the
            c = Vector((0, hc.y - sg["fwd"] * R, hc.z + sg["cz"] * R))    # nostrils and mouth are drawn on it
            if sg["style"] == "muzzle":
                sn = kit.ellipsoid_bm(c, (sg["rx"] * R, sg["depth"] * R, sg["rz"] * R), segs=48, rings=24)
            else:
                rr = sg["rx"] * R; d = sg["depth"] * R
                rings = [(-d, 0, 0, 0, 0), (-d, rr * 0.9, rr * 0.8, 0, 0)]
                for k in range(0, 6):
                    a = k / 5 * math.pi / 2
                    rings.append((d * 0.6 + 0.12 * rr * math.sin(a), rr * (0.88 + 0.12 * math.cos(a)) if k < 5 else rr * 0.9,
                                  rr * 0.83 * (0.88 + 0.12 * math.cos(a)), 0, 0))
                rings.append((d * 0.6 + 0.14 * rr, 0, 0, 0, 0))
                sn = kit.lathe(rings, 40, power=2.0)
                bmesh.ops.transform(sn, matrix=Matrix.Translation(c) @ rot_front(), verts=sn.verts)
            uvl = sn.loops.layers.uv.new("UVMap")
            for f in sn.faces:
                for lp in f.loops:
                    planar(lp, lp.vert.co)
            self.add(sn, self.face_mat, "head")
            self.snout_c = c
            self.snout_front = hc.y - (sg["fwd"] + sg["depth"] * (1.0 if sg["style"] == "muzzle" else 0.75)) * R
        else:
            self.snout_c = Vector((0, hc.y - 0.9 * R, hc.z - 0.5 * R))
            self.snout_front = hc.y - R
        self.build_ears()
        self.build_horns()

    def build_ears(self):
        L, P = self.L, self.P
        ea = P.get("ears") or {}
        st = ea.get("style", "side")
        if st == "none":
            return
        R, hc = L["R"], L["head_c"]
        col = self.mats.flat("ears", ea.get("color", P["skin"]), rough=0.7, spec=0.25)
        inner = self.mats.flat("ears_inner", ea["inner"], rough=0.6, spec=0.3) if ea.get("inner") else None
        for s in (-1, 1):
            if st == "side":
                c = Vector((s * 1.02 * R, hc.y + 0.08 * R, hc.z + 0.30 * R))
                rot = Euler((0, math.radians(s * 22), math.radians(-s * 12))).to_matrix()
                self.add(kit.ellipsoid_bm(c, (0.36 * R, 0.10 * R, 0.17 * R), rot=rot, segs=28, rings=14), col, "head")
                if inner:
                    self.add(kit.ellipsoid_bm(c + Vector((s * 0.03 * R, -0.035 * R, -0.005 * R)), (0.27 * R, 0.07 * R, 0.11 * R), rot=rot,
                                              segs=24, rings=12), inner, "head")
            else:                                         # floppy: hangs forward over the brow
                c = Vector((s * 0.62 * R, hc.y - 0.30 * R, hc.z + 0.72 * R))
                rot = Euler((math.radians(-55), math.radians(s * 25), math.radians(s * 20))).to_matrix()
                self.add(kit.ellipsoid_bm(c, (0.28 * R, 0.07 * R, 0.30 * R), rot=rot, segs=28, rings=14), col, "head")

    def build_horns(self):
        L, P = self.L, self.P
        hn = P.get("horns") or {}
        if hn.get("style", "none") == "none":
            return
        R, hc = L["R"], L["head_c"]
        col = self.mats.flat("horns", hn.get("color", "#EFE2C4"), rough=0.45, spec=0.4)
        self.cur_part = "feature_horns"
        for s in (-1, 1):
            pts = [(s * 0.48 * R, hc.y + 0.05 * R, hc.z + 0.76 * R), (s * 0.66 * R, hc.y + 0.01 * R, hc.z + 0.92 * R),
                   (s * 0.76 * R, hc.y - 0.03 * R, hc.z + 1.04 * R)]
            self.add(kit.tube_bm(pts, 0.15 * R, radii=[1.0, 0.78, 0.5]), col, "head")
            self.add(kit.ellipsoid_bm(pts[-1], (0.075 * R,) * 3, segs=12, rings=8), col, "head")
        self.cur_part = None

    # ------------------------------------------------------------------ legs, hooves, tail
    def build_legs(self):
        L, P = self.L, self.P
        T, g, zb = L["T"], L["g"], L["zb"]
        hv = P.get("hooves") or {}
        hcol = self.mats.flat("hooves", hv.get("color", "#4A3B3B"), rough=0.45, spec=0.4)
        lr, hh = L["lr"], L["hoof_h"]
        self.legs = {}
        for name, y in (("arm", L["front_y"]), ("leg", L["hind_y"])):
            for s, side in ((1, "L"), (-1, "R")):
                x = s * L["leg_x"]
                top = Vector((x, y, zb - 0.25 * g))
                ank = Vector((x, y, hh))
                self.legs[f"{name}.{side}"] = (top, ank)
                self.add(kit.capsule_bm(top, ank + Vector((0, 0, 0.3 * lr)), lr, lr * 0.94, segs=24, hem=5), self.skin, f"{name}.{side}")
                tip = "hand" if name == "arm" else "foot"
                if hv.get("style", "hooves") == "paws":
                    self.add(kit.ellipsoid_bm((x, y - 0.25 * lr, hh * 0.6), (lr * 1.12, lr * 1.35, hh * 0.75), floor=0.0015,
                                              segs=24, rings=12), hcol, f"{tip}.{side}")
                else:
                    r0 = lr * 1.06
                    rings = [(0.0015, 0, 0, 0, 0), (0.0015, r0 * 1.02, r0 * 1.02, 0, 0), (hh * 0.5, r0 * 1.0, r0, 0, 0),
                             (hh, r0 * 0.96, r0 * 0.96, 0, 0), (hh * 1.06, r0 * 0.7, r0 * 0.7, 0, 0), (hh * 1.08, 0, 0, 0, 0)]
                    bm = kit.lathe(rings, 24)
                    bmesh.ops.translate(bm, vec=(x, y, 0), verts=bm.verts)
                    self.add(bm, hcol, f"{tip}.{side}")

    def build_tail(self):
        L, P = self.L, self.P
        tl = P.get("tail") or {}
        st = tl.get("style", "tuft")
        T, Lb, g, zb = L["T"], L["Lb"], L["g"], L["zb"]
        zt = zb + 0.55 * g
        yt = Lb / 2 * 0.86
        a = Vector((0, yt, zt))
        if st == "curl":
            b = a + Vector((0, 0.06 * T, 0.02 * T)); c = b + Vector((0, 0.02 * T, -0.03 * T))
        elif st == "nub":
            b = a + Vector((0, 0.04 * T, -0.02 * T)); c = b + Vector((0, 0.01 * T, -0.02 * T))
        else:
            b = a + Vector((0, 0.07 * T, -0.17 * T)); c = b + Vector((0, 0.025 * T, -0.15 * T))
        self.tail_pts = (a, b, c)
        if st == "none":
            return
        col = self.mats.flat("tail", tl.get("color", P["skin"]), rough=0.7, spec=0.25)
        self.cur_part = "tail"
        if st == "tuft":
            r = 0.022 * T
            self.add(kit.capsule_bm(a, b, r, r * 0.9, segs=12, hem=3), col, "tail.1")
            self.add(kit.capsule_bm(b, c, r * 0.9, r * 0.8, segs=12, hem=3), col, "tail.2")
            tip = self.mats.flat("tail_tip", tl.get("tip", "#2B2B33"), rough=0.8, spec=0.2)
            d = (c - b).normalized()
            q = Vector((0, 0, -1)).rotation_difference(d).to_matrix()
            self.add(kit.ellipsoid_bm(c + d * 0.03 * T, (0.045 * T, 0.04 * T, 0.075 * T), rot=q, segs=20, rings=12), tip, "tail.2")
        elif st == "curl":
            pts = []
            for k in range(19):
                t = k / 18
                ang = t * 2.2 * math.pi
                rr = 0.05 * T * (1 - 0.45 * t)
                pts.append(a + Vector((rr * math.sin(ang) * 0.9, 0.03 * T + 0.05 * T * t + rr * (1 - math.cos(ang)) * 0.3,
                                       rr * (1 - math.cos(ang)))))
            self.add(kit.tube_bm(pts[:10], 0.016 * T), col, "tail.1")
            self.add(kit.tube_bm(pts[9:], 0.016 * T, radii=[1.0 - 0.4 * k / 9 for k in range(10)]), col, "tail.2")
        else:
            self.add(kit.ellipsoid_bm(b, (0.05 * T, 0.05 * T, 0.045 * T), segs=20, rings=12), col, "tail.1")
        self.cur_part = None

    # ------------------------------------------------------------------ rig, slots
    def build_armature(self):
        L = self.L
        T, zb, Lb = L["T"], L["zb"], L["Lb"]
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
        bone("root", (0, 0, 0), (0, 0, 0.12 * T))
        bone("spine", (0, 0.05 * Lb, zb), (0, -0.30 * Lb, zb), "root")             # along the barrel, pivot near its middle
        bone("head", (0, -0.42 * Lb, zb + 0.35 * L["g"]), (0, hc.y, hc.z + L["R"]), "spine")   # pivot at the neck
        for name, tip, parent in (("arm", "hand", "spine"), ("leg", "foot", "root")):
            for side in ("L", "R"):
                top, ank = self.legs[f"{name}.{side}"]
                bone(f"{name}.{side}", top, ank, parent)
                bone(f"{tip}.{side}", ank, (ank.x, ank.y - 0.01 * T, 0.0), f"{name}.{side}")
        a, b, c = self.tail_pts
        bone("tail.1", a, b, "spine")
        bone("tail.2", b, c, "tail.1")
        bpy.ops.object.mode_set(mode="OBJECT")
        return ob

    def measure_slots(self):
        L = self.L
        T, R, hc, zb, g, w, Lb = L["T"], L["R"], L["head_c"], L["zb"], L["g"], L["w"], L["Lb"]
        out = {}
        crown = max(co.z for co in self._cos({"head"})) - hc.z
        out["head"] = ("head", hc.copy(), None, (crown / kit.SLOT_REF["head_crown"],) * 3)
        s = R / kit.SLOT_REF["face_r"]
        out["face"] = ("head", Vector((0, hc.y - 0.93 * R, hc.z + 0.16 * R)), None, (s, s, s))
        # back: the top of the barrel; gear's back (+y) turned to face up, its up (+z) towards the head
        yb = 0.02 * Lb
        s = w / kit.SLOT_REF["back_tw"] * 0.75
        out["back"] = ("spine", Vector((0, yb, zb + self.barrel_r(-yb)[1])), Matrix.Rotation(math.radians(90), 3, "X"), (s, s, s))
        # waist: a girth strap round the barrel; a belt's ring axis (z) runs along the body, its buckle on the left side
        yw = -0.12 * Lb
        rx, ry = self.barrel_r(-yw)
        rot = Matrix(((0, -1, 0), (0, 0, -1), (1, 0, 0)))            # columns: x->Z, y->-X, z->-Y
        out["waist"] = ("spine", Vector((0, yw, zb)), rot, (ry / kit.SLOT_REF["waist_rx"], rx / kit.SLOT_REF["waist_ry"], 1.0))
        # mouth: the bite point under the front of the snout; character axes, scale like the face
        sc = self.snout_c
        out["mouth"] = ("head", Vector((0, self.snout_front + 0.10 * R, sc.z - 0.22 * R)), None, (R / kit.SLOT_REF["face_r"],) * 3)
        return out

    def add_slots(self, rig, fit):
        bpy.context.view_layer.update()
        obs = {}
        for name in QUAD_SLOTS:
            bone, pos, rot, scale = fit[name]
            e = bpy.data.objects.new(f"{self.prefix}slot_{name}", None)
            e.empty_display_type = "ARROWS"; e.empty_display_size = 0.05
            self.coll.objects.link(e)
            e.parent = rig; e.parent_type = "BONE"; e.parent_bone = bone
            b = rig.data.bones[bone]
            e.matrix_parent_inverse = (rig.matrix_world @ b.matrix_local @ Matrix.Translation((0, b.length, 0))).inverted()
            e.matrix_basis = Matrix.LocRotScale(pos, rot.to_quaternion() if rot is not None else None, Vector(scale))
            e["jarling_slot"] = name
            e["jarling_build"] = "quadruped"
            e["jarling_id"] = self.P["id"]
            obs[name] = e
        bpy.context.view_layer.update()
        return obs

    # ------------------------------------------------------------------ actions
    def actions(self):
        T, L = self.L["T"], self.L
        def P(*ds):
            out = {}
            for d in ds:
                for k, v in d.items():
                    out.setdefault(k, {}).update(v)
            return out
        legs = lambda fl, fr, hl, hr: {"arm.L": {"swing": fl}, "arm.R": {"swing": fr}, "leg.L": {"swing": hl}, "leg.R": {"swing": hr}}
        tail = lambda lean, twist, l2=None, t2=None: {"tail.1": {"lean": lean, "twist": twist},
                                                     "tail.2": {"lean": lean * 0.6 if l2 is None else l2, "twist": twist * 0.8 if t2 is None else t2}}
        acts = {}
        # idle: breathing, a slow chew, the tail swishes the flies away
        acts["idle"] = [
            (1, P(tail(8, 0))),
            (13, P({"spine": {"scale": (1.01, 1.015, 1.015)}, "head": {"lean": 3, "twist": 2}}, tail(10, 22))),
            (25, P({"spine": {"scale": (1.02, 1.03, 1.03)}, "head": {"lean": 1, "tilt": 4, "twist": -2}}, tail(8, 0))),
            (37, P({"spine": {"scale": (1.01, 1.015, 1.015)}, "head": {"lean": 3, "twist": 2}}, tail(10, -22))),
            (49, P(tail(8, 0))),
        ]
        # run: a trot, diagonal pairs (front left with hind right)
        c1 = P(legs(26, -26, -22, 22), {"hand.L": {"swing": 10}, "hand.R": {"swing": -25}, "foot.L": {"point": 25}, "foot.R": {"point": -10},
                                        "root": {"loc": (0, 0, 0.0), "scale": (1.02, 0.98, 0.97)}, "spine": {"tilt": 2, "lean": 1},
                                        "head": {"lean": 2, "tilt": -2}}, tail(35, 8))
        c2 = P(legs(0, 0, 0, 0), {"root": {"loc": (0, 0, 0.045 * T), "scale": (0.99, 1.02, 1.03)}, "spine": {"lean": -1},
                                   "head": {"lean": -4}}, tail(45, 0))
        acts["run"] = [(1, c1), (5, c2), (9, kit.mirror(c1)), (13, kit.mirror(c2)), (17, c1)]
        # cheer: a happy hop (two hops per loop)
        crouch = P(legs(-6, -6, 6, 6), {"root": {"loc": (0, 0, -0.025 * T), "scale": (1.06, 1.04, 0.90)}, "head": {"lean": 6}}, tail(20, 0))
        up = lambda tw: P(legs(28, 28, -26, -26), {"root": {"loc": (0, 0, 0.16 * T), "scale": (0.96, 1.04, 1.06)},
                                                   "spine": {"lean": -6}, "head": {"lean": -12, "tilt": tw},
                                                   "hand.L": {"swing": 25}, "hand.R": {"swing": 25}}, tail(60, tw * 3))
        rise = P(legs(14, 14, -12, -12), {"root": {"loc": (0, 0, 0.09 * T), "scale": (0.95, 1.03, 1.08)}, "head": {"lean": -6}}, tail(45, 0))
        acts["cheer"] = [(1, crouch), (5, rise), (8, up(5)), (11, rise), (13, crouch), (17, rise), (20, up(-5)), (23, rise), (25, crouch)]
        # tipped: rolled onto her right side, legs stuck out stiff, a feeble kick now and then
        roll = {"root": {"tilt": 90, "loc": (-L["zb"], 0, L["w"] * 1.0)}}
        def lying(k):
            return P(roll, {"arm.L": {"swing": 12 + k, "out": 6}, "arm.R": {"swing": 18 - k, "out": -6},
                            "leg.L": {"swing": -14 - k, "out": 6}, "leg.R": {"swing": -20 + k, "out": -6},
                            "head": {"tilt": -22, "lean": -6}}, tail(-10, 25))
        acts["tipped"] = [(1, lying(0)), (7, lying(8)), (13, lying(0)), (19, lying(-6)), (25, lying(0))]
        # stiff: the same legs-out pose with no roll, for games whose physics body has already rolled over
        def stiff(k):
            return P({"arm.L": {"swing": 12 + k, "out": 30}, "arm.R": {"swing": 18 - k, "out": 30},
                      "leg.L": {"swing": -14 - k, "out": 30}, "leg.R": {"swing": -20 + k, "out": 30},
                      "head": {"lean": -8}}, tail(-10, 25))
        acts["stiff"] = [(1, stiff(0)), (7, stiff(8)), (13, stiff(0)), (19, stiff(-6)), (25, stiff(0))]
        # graze: head down to the grass, nibbling
        gz = lambda lean, tw: P({"head": {"lean": lean, "twist": tw}, "spine": {"lean": 7}, "root": {"loc": (0, 0, 0.012 * T)}},
                                legs(-7, -7, 0, 0), tail(10, tw * 6))
        acts["graze"] = [(1, gz(66, 0)), (9, gz(72, 3)), (17, gz(66, 0)), (25, gz(72, -3)), (33, gz(66, 0))]
        # sit: haunches down, front legs straight, head up
        def sit(b):
            return P({"root": {"loc": (0, 0, -0.12 * T)}, "spine": {"lean": -24, "scale": (1 + b, 1 + b, 1 + b)},
                      "arm.L": {"swing": -6}, "arm.R": {"swing": -6}, "hand.L": {"swing": 0}, "hand.R": {"swing": 0},
                      "leg.L": {"swing": 78, "out": 8}, "leg.R": {"swing": 78, "out": 8}, "foot.L": {"point": -60}, "foot.R": {"point": -60},
                      "head": {"lean": 18 + b * 100}}, tail(-40, 10))
        acts["sit"] = [(1, sit(0)), (25, sit(0.02)), (49, sit(0))]
        return acts

    # ------------------------------------------------------------------ build
    def build(self):
        self.layout()
        self.build_body()
        self.build_head()
        self.build_legs()
        self.build_tail()
        pid = self.P["id"]
        rig = self.build_armature()
        slot_fit = self.measure_slots()
        main = [p for p, t in zip(self.parts, self.part_tags) if t is None]
        body = self.make_mesh(f"{self.prefix}{pid}_body", main)
        body.parent = rig
        body.modifiers.new("Armature", "ARMATURE").object = rig
        self.part_obs = {}
        for tag in sorted(set(t for t in self.part_tags if t)):
            pp = [p for p, t in zip(self.parts, self.part_tags) if t == tag]
            ob = self.make_mesh(f"{self.prefix}{pid}_part_{tag}", pp)
            ob.parent = rig
            ob.modifiers.new("Armature", "ARMATURE").object = rig
            ob["jarling_part"] = tag
            self.part_obs[tag] = ob
        body["jarling_expressions"] = {k: list(v) for k, v in self.expr_uv.items()}
        rig["jarling"] = 1
        rig["jarling_body_type"] = "quadruped"
        rig["jarling_loops"] = list(QUAD_LOOPS)
        self.rig, self.body, self.hat = rig, body, None
        self.slots = self.add_slots(rig, slot_fit)
        rig["jarling_slots"] = list(self.slots.keys())
        kit.build_actions(rig, {}, self.prefix, acts=self.actions())
        return self


# ---------------------------------------------------------------------------- the face atlas cell
def draw_quad_face(face, expr, skin):
    """One atlas cell. Canvas units are head radii, origin at the head centre (see build_head)."""
    c = kit.FACE_CELL
    k0 = 0.5 * (1 - 2 * kit.FACE_MARGIN)
    cv = kit.Canvas(c, c, (-0.5 / k0, 0.5 / k0, -0.5 / k0, 0.5 / k0), skin)
    look = dict(EXPR_LOOK.get(expr, EXPR_LOOK["neutral"]))
    look.update(face.get("expressions", {}).get(expr, {}))
    col = face.get("eye_color", "#2A1E2C")
    ex, ey = float(face.get("eye_spacing", 0.40)), float(face.get("eye_y", 0.16))
    # coat patch on the face (painted first)
    pt = face.get("patch")
    if pt:
        sl, X, Y = cv.grid(-1.1, -1.1, 1.1, 1.1)
        d = kit.sd_ellipse(X, Y, pt[0], pt[1], pt[2], pt[3], rot=pt[4] if len(pt) > 4 else 0.0)
        d = d - 0.035 * np.sin(5 * np.arctan2(Y - pt[1], X - pt[0]))
        cv.paint(sl, d, face["_accent"])
    sg = face["_snout"]
    if sg["style"] != "none":                        # snout colour, a touch bigger than its silhouette
        sl, X, Y = cv.grid(-sg["rx"] - 0.1, sg["cz"] - sg["rz"] - 0.1, sg["rx"] + 0.1, sg["cz"] + sg["rz"] + 0.1)
        cv.paint(sl, kit.sd_ellipse(X, Y, 0, sg["cz"], sg["rx"] + 0.03, sg["rz"] + 0.03), face["_snout_col"])
        nx, ny, nrx, nry = sg["nost"]
        for s in (-1, 1):
            sl, X, Y = cv.grid(s * nx - 0.12, ny - 0.12, s * nx + 0.12, ny + 0.12)
            cv.paint(sl, kit.sd_ellipse(X, Y, s * nx, ny, nrx, nry, rot=s * 0.35 if sg["style"] == "muzzle" else 0.0), face["_nostril"])
    if look.get("blush"):
        for s in (-1, 1):
            sl, X, Y = cv.grid(s * 0.62 - 0.2, -0.12, s * 0.62 + 0.2, 0.12)
            cv.paint(sl, kit.sd_ellipse(X, Y, s * 0.62, -0.02, 0.12, 0.07), "#F49AA8", opacity=0.6)
    W = "#FFFFFF"
    def ink(sl, d, halo=0.03):
        if pt:
            cv.paint(sl, d - halo, skin)
        cv.paint(sl, d, col)
    for sx in (-1, 1):
        cx = sx * ex
        sl, X, Y = cv.grid(cx - 0.32, ey - 0.32, cx + 0.32, ey + 0.5)
        if look["eye"] == "arc":
            ink(sl, kit.sd_stroke(X, Y, kit.bez((cx - 0.13, ey - 0.03), (cx, ey + 0.13), (cx + 0.13, ey - 0.03)), 0.075))
        elif look["eye"] == "spiral":
            pts = []
            for k in range(40):
                t = k / 39
                a = sx * t * 3.2 * math.pi
                r = 0.015 + 0.12 * t
                pts.append((cx + r * math.cos(a), ey + r * math.sin(a)))
            ink(sl, kit.sd_stroke(X, Y, pts, 0.04))
        else:
            rs, ri, lid = look["sclera"], look["iris"], look.get("lid", 0.0)
            cut = ey + rs * (1 - 2 * lid)               # upper lid line
            lid_d = (Y - cut)                            # > 0 above the lid
            if pt:
                cv.paint(sl, np.maximum(kit.sd_circle(X, Y, cx, ey, rs + 0.03), lid_d - 0.03), skin)
            cv.paint(sl, np.maximum(kit.sd_circle(X, Y, cx, ey, rs), lid_d), W)
            ix = cx + look.get("look", 0.0)
            iy = ey - 0.015
            cv.paint(sl, np.maximum(kit.sd_circle(X, Y, ix, iy, ri), lid_d), col)
            cv.paint(sl, np.maximum(kit.sd_circle(X, Y, ix - 0.35 * ri, iy + 0.4 * ri, 0.32 * ri), lid_d), W)
            cv.paint(sl, np.maximum(kit.sd_circle(X, Y, ix + 0.4 * ri, iy - 0.35 * ri, 0.15 * ri), lid_d), W)
            # outline of the eye (below the lid) and the lid line
            ring = np.abs(kit.sd_circle(X, Y, cx, ey, rs)) - 0.012
            cv.paint(sl, np.maximum(ring, lid_d), col)
            if lid > 0:
                half = math.sqrt(max(0.0, rs * rs - (cut - ey) ** 2))
                ink(sl, kit.sd_stroke(X, Y, [(cx - half - 0.01, cut), (cx + half + 0.01, cut)], 0.035), 0.02)
            if face.get("lashes"):
                top = min(cut, ey + rs)
                ox = cx + sx * rs * 0.75
                for k in range(2):
                    a0 = (ox + sx * 0.01 * k, top - 0.04 - 0.05 * k)
                    ink(sl, kit.sd_stroke(X, Y, [a0, (a0[0] + sx * 0.08, a0[1] + 0.05)], 0.028, 0.012), 0.02)
        br = look.get("brow")
        if br:
            kind, raise_ = br
            by = ey + 0.26 + raise_
            if kind == "worried":
                pts = [(sx * (ex - 0.13), by + 0.05), (sx * (ex + 0.10), by - 0.04)]
            elif kind == "one_up":
                if sx < 0:
                    pts = [(sx * (ex - 0.12), by - 0.03), (sx * (ex + 0.12), by - 0.03)]
                else:
                    pts = kit.bez((sx * (ex - 0.12), by + 0.02), (sx * ex, by + 0.09), (sx * (ex + 0.12), by + 0.02))
            else:
                pts = kit.bez((sx * (ex - 0.12), by), (sx * ex, by + 0.06), (sx * (ex + 0.12), by))
            ink(sl, kit.sd_stroke(X, Y, pts, 0.05))
    if look.get("sweat"):
        sl, X, Y = cv.grid(0.55, 0.45, 0.95, 0.95)
        d = kit.smin(kit.sd_circle(X, Y, 0.74, 0.58, 0.07), kit.sd_stroke(X, Y, [(0.74, 0.60), (0.74, 0.76)], 0.02, 0.0), 0.05)
        cv.paint(sl, d, "#7CC8F2")
    my = sg.get("mouth", -0.6)
    m = look.get("mouth", "smile_small")
    sl, X, Y = cv.grid(-0.4, my - 0.3, 0.4, my + 0.25)
    if m == "smile":
        d = kit.sd_stroke(X, Y, kit.bez((-0.20, my + 0.05), (0, my - 0.12), (0.20, my + 0.05)), 0.05)
    elif m == "smile_small":
        d = kit.sd_stroke(X, Y, kit.bez((-0.13, my + 0.025), (0, my - 0.05), (0.13, my + 0.025)), 0.045)
    elif m == "smirk":
        d = kit.sd_stroke(X, Y, kit.bez((-0.12, my - 0.01), (0.06, my - 0.04), (0.17, my + 0.06)), 0.045)
    elif m == "wobble":
        d = kit.sd_stroke(X, Y, [(-0.16, my - 0.02), (-0.08, my + 0.03), (0.0, my - 0.02), (0.08, my + 0.03), (0.16, my - 0.02)], 0.045)
    elif m == "o":
        cv.paint(sl, kit.sd_ellipse(X, Y, 0, my - 0.02, 0.07, 0.075), "#6A2232")
        d = np.abs(kit.sd_ellipse(X, Y, 0, my - 0.02, 0.07, 0.075)) - 0.018
    elif m == "open":
        cv.paint(sl, kit.sd_ellipse(X, Y, 0, my - 0.05, 0.16, 0.12), "#6A2232")
        cv.paint(sl, np.maximum(kit.sd_ellipse(X, Y, 0, my - 0.13, 0.10, 0.06), kit.sd_ellipse(X, Y, 0, my - 0.05, 0.16, 0.12)), "#F2848C")
        d = np.abs(kit.sd_ellipse(X, Y, 0, my - 0.05, 0.16, 0.12)) - 0.02
    else:
        d = kit.sd_stroke(X, Y, [(-0.1, my), (0.1, my)], 0.045)
    cv.paint(sl, d, col)
    return cv.img


kit.BODY_TYPES["quadruped"] = QuadrupedBuilder
