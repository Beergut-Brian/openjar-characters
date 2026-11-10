"""Starter gear set for Jarlings: one .glb + one .json per item (see docs/equipment.md).

    blender -b --factory-startup -P avatar/gear/build_gear.py -- [--outdir avatar/gear] [--only cape,hat]

Every piece is modelled in *slot space* for the reference Jarling (regular build, scale 1):
Blender axes here (Z up, front -Y, character's left +X); the glTF export turns that into Godot's
+Y up, front +Z. The slot markers on each Jarling carry the fit scale, so nothing here is per character.
These are proof pieces: chunky, smooth-shaded, flat colours, original designs. A later Art lane
replaces the art; the node names, origins and JSON are the contract.
"""
import sys, os, json, math, argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kit"))
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import jarling_kit as kit
from jarling_kit import ellipsoid_bm, capsule_bm, tube_bm, lathe, solidify_bm, grid_bm, srgb_to_lin, hex_rgb

# gear palette: away from the player green and red so gear never reads as P1/P2
ORANGE, TEAL, PURPLE, WHITE, DARK, GOLD, STEEL, TAN = (
    "#FF8A1F", "#1FB5A8", "#8E5BD9", "#F4F4F0", "#2E2E3A", "#FFC93C", "#C9D1D9", "#C98A4B")

M = kit.Mats("gear_")

def mat(key, col, rough=0.55, spec=0.35):
    return M.flat(key, col, rough, spec)

def glow(key, col, strength=3.0):
    m = M.flat(key, col, 0.6, 0.2)
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Emission Color"].default_value = (*srgb_to_lin(hex_rgb(col)), 1.0)
    p.inputs["Emission Strength"].default_value = strength
    return m

def obj(name, parts, parent=None):
    """Join (bmesh, material) parts into one smooth-shaded mesh object."""
    me = bpy.data.meshes.new(name)
    out = bmesh.new()
    mats = []
    for pbm, m in parts:
        if m not in mats:
            mats.append(m)
        mi = mats.index(m)
        vmap = {v: out.verts.new(v.co) for v in pbm.verts}
        for f in pbm.faces:
            try:
                nf = out.faces.new([vmap[v] for v in f.verts])
            except ValueError:
                continue
            nf.material_index = mi; nf.smooth = True
        pbm.free()
    out.normal_update()
    out.to_mesh(me); out.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    for m in mats:
        me.materials.append(m)
    if parent:
        ob.parent = parent
    return ob

def empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.05
    bpy.context.scene.collection.objects.link(e)
    if parent:
        e.parent = parent
    e.location = loc
    return e

def ring(cx, cy, z, rx, ry, n=48, power=2.0):
    return [(cx + rx * dx, cy + ry * dy, z) for dx, dy in (kit.superxy(a, power) for a in np.linspace(0, 2 * math.pi, n, endpoint=False))]

def oriented(center, radii, normal, segs=24, rings=12):
    rot = Vector((0, -1, 0)).rotation_difference(Vector(normal).normalized()).to_matrix()
    return ellipsoid_bm(center, radii, rot=rot, segs=segs, rings=rings)

# ------------------------------------------------------------------------------------------ feet
# Foot slot: origin on the ground under the ankle. Ankle at z 0.075, leg radius ~0.05 (Jeff's flared
# jeans hem is 0.067 + a stitch ring), so shafts start wide.

def shoe_base(s, body, sole, length=0.128, height=0.06, toe=None):
    parts = [(ellipsoid_bm((0, -0.035, height), (0.074, length, height), floor=0.022, segs=32, rings=16), body),
             (ellipsoid_bm((0, -0.038, 0.024), (0.079, length + 0.007, 0.024), floor=0.0, segs=32, rings=12), sole)]
    if toe:
        parts.append((ellipsoid_bm((0, -0.105, 0.055), (0.066, 0.064, 0.042), floor=0.026, segs=24, rings=12), toe))
    return parts

def sneakers():
    root = empty("sneakers")
    for side, s in (("l", 1), ("r", -1)):
        node = empty(f"foot_{side}", root)
        body, sole, acc = mat("sneaker", WHITE), mat("sneaker_sole", DARK, 0.7), mat("sneaker_accent", ORANGE)
        parts = shoe_base(s, body, sole, toe=mat("sneaker_toe", TEAL))
        parts.append((tube_bm(ring(0, -0.038, 0.047, 0.077, 0.132), 0.007, cyclic=True), acc))      # midsole stripe
        parts.append((tube_bm(ring(0, 0.0, 0.112, 0.054, 0.052), 0.011, cyclic=True), acc))          # padded collar
        parts.append((ellipsoid_bm((0, -0.045, 0.108), (0.04, 0.045, 0.022), segs=20, rings=10), acc))  # tongue
        for k, y in enumerate((-0.07, -0.095, -0.118)):                                            # laces
            z = 0.06 + 0.06 * math.sqrt(max(0.0, 1 - ((y + 0.035) / 0.128) ** 2)) + 0.004
            parts.append((capsule_bm((-0.024, y, z), (0.024, y, z), 0.0075, 0.0075, segs=12, hem=3), mat("lace", "#FFFFFF", 0.5)))
        obj(f"sneaker_{side}", parts, node)
        obj(f"trim_sneaker_{side}", [(tube_bm(ring(0, -0.038, 0.033, 0.081, 0.136), 0.006, cyclic=True), mat("trim_gold", GOLD, 0.3, 0.7))], node)
    return root

def boot(side, s, body, sole, cuff, extra):
    parts = shoe_base(s, body, sole, length=0.13, height=0.058)
    parts.append((lathe([(0.03, 0.0, 0.0, 0, 0.005), (0.03, 0.074, 0.072, 0, 0.005), (0.1, 0.08, 0.077, 0, 0.005),
                         (0.14, 0.08, 0.077, 0, 0.005), (0.14, 0.0, 0.0, 0, 0.005)], 32), body))          # shaft
    parts.append((tube_bm(ring(0, 0.005, 0.141, 0.081, 0.078), 0.013, cyclic=True), cuff))                 # chunky cuff
    parts.append((lathe([(0.0, 0, 0, 0, 0.055), (0.0, 0.05, 0.035, 0, 0.055), (0.03, 0.054, 0.038, 0, 0.055),
                         (0.03, 0, 0, 0, 0.055)], 24, power=3.0), sole))                                     # heel
    parts += extra
    return parts

def boots():
    root = empty("boots")
    for side, s in (("l", 1), ("r", -1)):
        node = empty(f"foot_{side}", root)
        body, sole, cuff = mat("boot", TAN, 0.6), mat("boot_sole", "#4A3426", 0.7), mat("boot_cuff", "#F2E6C9", 0.9, 0.15)
        strap = mat("boot_strap", DARK, 0.6)
        extra = [(tube_bm(ring(0, -0.0, 0.09, 0.083, 0.08), 0.008, cyclic=True), strap),
                 (ellipsoid_bm((s * 0.083, -0.0, 0.09), (0.008, 0.02, 0.016), segs=12, rings=8), mat("boot_buckle", STEEL, 0.3, 0.6))]
        obj(f"boot_{side}", boot(side, s, body, sole, cuff, extra), node)
        obj(f"trim_boot_{side}", [(tube_bm(ring(0, -0.038, 0.032, 0.082, 0.138), 0.006, cyclic=True), mat("trim_gold", GOLD, 0.3, 0.7))], node)
    return root

def rocket_boots():
    root = empty("rocket_boots")
    for side, s in (("l", 1), ("r", -1)):
        node = empty(f"foot_{side}", root)
        body, sole, cuff = mat("rocket", WHITE, 0.4, 0.5), mat("rocket_sole", DARK, 0.6), mat("rocket_cuff", ORANGE, 0.5)
        steel = mat("rocket_steel", STEEL, 0.3, 0.7)
        extra = [(ellipsoid_bm((0, -0.105, 0.052), (0.068, 0.066, 0.044), floor=0.026, segs=24, rings=12), cuff),
                 # thruster on the heel, pointing back (+Y)
                 (capsule_bm((0, 0.07, 0.085), (0, 0.11, 0.085), 0.032, 0.032, segs=20, hem=4), steel),
                 (lathe([(0.0, 0.026, 0.026, 0, 0), (0.03, 0.036, 0.036, 0, 0), (0.03, 0.0, 0.0, 0, 0)], 20), mat("rocket_nozzle", DARK, 0.5)),
                 ]
        # the nozzle lathe is built along Z; turn it to point back
        bmesh.ops.transform(extra[-1][0], matrix=Matrix.Translation((0, 0.112, 0.085)) @ Matrix.Rotation(math.radians(-90), 4, "X"), verts=extra[-1][0].verts)
        for fs in (1, -1):   # little fins
            extra.append((ellipsoid_bm((fs * 0.036, 0.085, 0.11), (0.006, 0.03, 0.022), rot=Euler((0.5, 0, 0)).to_matrix(), segs=14, rings=8), cuff))
        obj(f"rocket_boot_{side}", boot(side, s, body, sole, cuff, extra), node)
        fl = lathe([(0.0, 0.0, 0.0, 0, 0), (0.0, 0.03, 0.03, 0, 0), (0.035, 0.024, 0.024, 0, 0), (0.09, 0.0, 0.0, 0, 0)], 20)
        bmesh.ops.transform(fl, matrix=Matrix.Translation((0, 0.142, 0.085)) @ Matrix.Rotation(math.radians(-90), 4, "X"), verts=fl.verts)
        obj(f"fx_flame_{side}", [(fl, glow("flame", "#FFB13B"))], node)
        gold_ring = [(0.0335 * math.cos(a), 0.095, 0.085 + 0.0335 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 32, endpoint=False)]
        obj(f"trim_rocket_{side}", [(tube_bm(gold_ring, 0.006, cyclic=True), mat("trim_gold", GOLD, 0.3, 0.7))], node)
    return root

# ----------------------------------------------------------------------------------------- knees
# Knee slot: origin on the leg axis halfway down; reference leg radius 0.049.

def kneepads():
    root = empty("kneepads")
    pad, strap, cap = mat("kneepad", TEAL, 0.5), mat("kneepad_strap", DARK, 0.7), mat("kneepad_cap", WHITE, 0.45)
    for side in ("l", "r"):
        node = empty(f"knee_{side}", root)
        parts = [(ellipsoid_bm((0, -0.028, 0.0), (0.054, 0.042, 0.052), segs=28, rings=14), pad),
                 (ellipsoid_bm((0, -0.064, 0.0), (0.024, 0.01, 0.026), segs=20, rings=10), cap)]
        for z in (-0.03, 0.03):
            parts.append((tube_bm(ring(0, 0, z, 0.054, 0.054), 0.008, cyclic=True), strap))
        obj(f"kneepad_{side}", parts, node)
        obj(f"trim_kneepad_{side}", [(tube_bm([(0.036 * math.cos(a), -0.058 + 0.016 * (1 - abs(math.cos(a))), 0.037 * math.sin(a))
                                               for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)], 0.0055, cyclic=True),
                                      mat("trim_gold", GOLD, 0.3, 0.7))], node)
    return root

# ----------------------------------------------------------------------------------------- hands
# Hand slot: origin at the mitten centre. Mitten radii (0.036, 0.047, 0.052), thumb toward -Y.

def gloves():
    root = empty("gloves")
    g, cuff = mat("glove", WHITE, 0.6), mat("glove_cuff", PURPLE, 0.6)
    for side, s in (("l", 1), ("r", -1)):
        node = empty(f"hand_{side}", root)
        parts = [(ellipsoid_bm((0, 0, -0.002), (0.042, 0.053, 0.058), segs=24, rings=12), g),
                 (ellipsoid_bm((-s * 0.017, -0.037, 0.008), (0.02, 0.024, 0.03), segs=16, rings=8), g),
                 (lathe([(0.026, 0.0, 0.0, -s * 0.004, 0.004), (0.026, 0.047, 0.05, -s * 0.004, 0.004),
                         (0.062, 0.052, 0.055, -s * 0.004, 0.004), (0.062, 0.0, 0.0, -s * 0.004, 0.004)], 28), cuff),
                 (tube_bm(ring(-s * 0.004, 0.004, 0.062, 0.052, 0.055), 0.008, cyclic=True), cuff)]
        obj(f"glove_{side}", parts, node)
        obj(f"trim_glove_{side}", [(tube_bm(ring(-s * 0.004, 0.004, 0.044, 0.054, 0.057), 0.006, cyclic=True), mat("trim_gold", GOLD, 0.3, 0.7))], node)
    return root

# ----------------------------------------------------------------------------------------- waist
# Waist slot: origin on the torso axis at belt height; reference torso half-width 0.155, half-depth 0.127.

def belt():
    root = empty("belt")
    node = empty("waist", root)
    band, buckle = mat("belt", "#7A4A2A", 0.6), mat("belt_buckle", GOLD, 0.3, 0.7)
    rx, ry, p = 0.155, 0.127, 2.6
    rings = [(-0.02, rx + 0.004, ry + 0.004, 0, 0), (-0.016, rx + 0.011, ry + 0.011, 0, 0),
             (0.016, rx + 0.011, ry + 0.011, 0, 0), (0.02, rx + 0.004, ry + 0.004, 0, 0)]
    obj("belt_band", [(lathe(rings, 48, p), band)], node)
    # chunky buckle at the front (-Y)
    bk = ellipsoid_bm((0, -(ry + 0.016), 0), (0.034, 0.012, 0.027), segs=24, rings=12)
    hole = ellipsoid_bm((0, -(ry + 0.026), 0), (0.016, 0.004, 0.012), segs=16, rings=8)
    obj("belt_buckle", [(bk, buckle), (hole, mat("belt_hole", "#5A3A1C", 0.6))], node)
    studs = []
    for a in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        if abs(math.sin(a) + 1) < 0.25:     # skip the buckle
            continue
        dx, dy = kit.superxy(a, p)
        studs.append((ellipsoid_bm(((rx + 0.012) * dx, (ry + 0.012) * dy, 0), (0.008, 0.008, 0.008), segs=12, rings=6), buckle))
    obj("trim_belt_studs", studs, node)
    return root

# ------------------------------------------------------------------------------------------ back
# Back slot: origin on the back surface at shoulder height; "behind" is +Y. Reference torso width 0.152.

def cape():
    root = empty("cape")
    node = empty("back", root)
    pivot = empty("cape_pivot", node, (0, 0.006, 0.03))
    col, clasp = mat("cape", PURPLE, 0.7, 0.2), mat("cape_clasp", GOLD, 0.3, 0.7)
    Lc = 0.33
    def pt(u, v, off=0.0):
        x = (u * 2 - 1)
        w = 0.105 + 0.085 * v
        z = -Lc * v - 0.025 * (1 - math.cos(x * math.pi * 3)) * v ** 3    # wavy hem
        y = 0.006 + 0.05 * v - 0.05 * x * x * (1 - 0.6 * v) + off
        return (x * w, y, z)
    sheet = grid_bm(lambda u, v: pt(u, v), 24, 14)
    bmesh.ops.recalc_face_normals(sheet, faces=sheet.faces)
    if sum(f.normal.y for f in sheet.faces) < 0:     # outside faces back (+Y)
        bmesh.ops.reverse_faces(sheet, faces=sheet.faces)
    obj("cape_cloth", [(solidify_bm(sheet, 0.012), col)], pivot)
    top = [pt(u, 0.02, 0.004) for u in np.linspace(0, 1, 16)]
    obj("cape_collar", [(tube_bm(top, 0.011), clasp),
                        (ellipsoid_bm(top[0], (0.017,) * 3, segs=16, rings=8), clasp),
                        (ellipsoid_bm(top[-1], (0.017,) * 3, segs=16, rings=8), clasp)], pivot)
    hem = [pt(u, 0.985, 0.007) for u in np.linspace(0, 1, 40)]
    obj("trim_cape_hem", [(tube_bm(hem, 0.007), clasp)], pivot)
    return root

def jetpack():
    root = empty("jetpack")
    node = empty("back", root)
    steel, cap, dark = mat("jet_tank", STEEL, 0.3, 0.7), mat("jet_cap", ORANGE, 0.45), mat("jet_dark", DARK, 0.6)
    parts = [(ellipsoid_bm((0, 0.03, -0.09), (0.085, 0.035, 0.12), segs=28, rings=14), dark)]   # back plate
    for x in (-0.058, 0.058):
        parts.append((capsule_bm((x, 0.085, -0.2), (x, 0.085, 0.0), 0.048, 0.048, segs=24, hem=6), steel))
        parts.append((ellipsoid_bm((x, 0.085, 0.03), (0.04, 0.04, 0.03), segs=20, rings=10), cap))
        parts.append((tube_bm(ring(x, 0.085, -0.12, 0.05, 0.05), 0.007, cyclic=True), cap))
        parts.append((lathe([(-0.29, 0.0, 0.0, x, 0.085), (-0.29, 0.034, 0.034, x, 0.085), (-0.255, 0.024, 0.024, x, 0.085),
                             (-0.235, 0.0, 0.0, x, 0.085)], 20), dark))
    for x in (-0.07, 0.07):   # shoulder straps: up the back, over the shoulder, down the chest
        pts = [(x, 0.0, -0.02), (x, -0.01, 0.045), (x * 1.05, -0.06, 0.088), (x * 1.08, -0.14, 0.08), (x * 1.08, -0.215, 0.03),
               (x * 1.06, -0.235, -0.04)]
        parts.append((tube_bm(pts, 0.012), dark))
    obj("jetpack_body", parts, node)
    for side, x in (("l", 0.058), ("r", -0.058)):
        fl = lathe([(-0.42, 0.0, 0.0, x, 0.085), (-0.33, 0.022, 0.022, x, 0.085), (-0.29, 0.03, 0.03, x, 0.085), (-0.29, 0.0, 0.0, x, 0.085)], 20)
        obj(f"fx_flame_{side}", [(fl, glow("flame", "#FFB13B"))], node)
    obj("trim_jetpack", [(tube_bm(ring(x, 0.085, -0.17, 0.05, 0.05), 0.007, cyclic=True), mat("trim_gold", GOLD, 0.3, 0.7)) for x in (-0.058, 0.058)], node)
    return root

# ------------------------------------------------------------------------------------------ head
# Head slot: origin at the head centre; reference crown (top of hair) 0.27 above it.

def hat():
    root = empty("hat")
    node = empty("head", root)
    felt, band = mat("hat", TEAL, 0.75, 0.2), mat("hat_band", ORANGE, 0.6)
    crown = lathe([(0.085, 0.262, 0.262, 0, 0), (0.17, 0.258, 0.258, 0, 0), (0.25, 0.225, 0.225, 0, 0),
                   (0.29, 0.16, 0.16, 0, 0), (0.305, 0.0, 0.0, 0, 0)], 48)
    rings = [(0.102, 0.255), (0.088, 0.30), (0.07, 0.34), (0.055, 0.365)]
    brim = lathe([(z, r, r, 0, 0) for z, r in rings], 48)
    obj("hat_crown", [(crown, felt), (solidify_bm(brim, 0.016), felt),
                      (tube_bm(ring(0, 0, 0.115, 0.262, 0.262), 0.022, cyclic=True), band)], node)
    obj("trim_hat_star", [(oriented((0, -0.28, 0.12), (0.03, 0.01, 0.03), (0, -1, 0), segs=5 * 4, rings=8), mat("trim_gold", GOLD, 0.3, 0.7))], node)
    return root

# ------------------------------------------------------------------------------------------ face
# Face slot: origin on the face at eye level; the head centre is 0.235 behind (+Y here).

def sunglasses():
    root = empty("sunglasses")
    node = empty("face", root)
    lens, frame = mat("lens", "#23233A", 0.12, 0.8), mat("shades_frame", ORANGE, 0.4, 0.5)
    Rh = 0.235; c = Vector((0, Rh, 0))
    def on(az, el, r):
        return c + Vector((r * math.sin(az) * math.cos(el), -r * math.cos(az) * math.cos(el), r * math.sin(el)))
    parts = []
    for s in (1, -1):
        az = s * math.asin(0.105 / Rh)
        p = on(az, 0.0, Rh + 0.016); n = (p - c)
        parts.append((oriented(p, (0.058, 0.01, 0.046), n, segs=28, rings=12), lens))
        rot = Vector((0, -1, 0)).rotation_difference(n.normalized()).to_matrix()
        rim = [p + rot @ Vector((0.06 * math.cos(a), 0.0, 0.048 * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 36, endpoint=False)]
        parts.append((tube_bm(rim, 0.008, cyclic=True), frame))
        temple = [on(s * a, 0.02, Rh + 0.02) for a in np.linspace(math.radians(40), math.radians(96), 8)]
        parts.append((tube_bm(temple, 0.0065), frame))
    bridge = [on(a, 0.06 - 0.04 * (a / 0.2) ** 2, Rh + 0.024) for a in np.linspace(-0.2, 0.2, 9)]
    parts.append((tube_bm(bridge, 0.007), frame))
    obj("sunglasses_frame", parts, node)
    star = []
    for s in (1, -1):
        p = on(s * 0.66, 0.2, Rh + 0.03)
        star.append((ellipsoid_bm(p, (0.012, 0.006, 0.012), segs=12, rings=6), mat("trim_gold", GOLD, 0.3, 0.7)))
    obj("trim_shades_sparkle", star, node)
    return root

# ------------------------------------------------------------------------------------------ held items
# Hand slot: origin at the hand centre. A held item is modelled upright in its own space and says
# where the hands close on it (`hold`: grip_r, grip_l, axis, style; avatar/kit/hold.py). The runtime
# turns `axis` onto the fist and puts grip_r in the main fist; the off hand goes to grip_l.
def rbox(c, hw, hd, hh, power=8, segs=28):
    cx, cy, cz = c; k = 0.82
    return lathe([(cz - hh, 0, 0, cx, cy), (cz - hh, hw * k, hd * k, cx, cy), (cz - hh * 0.9, hw, hd, cx, cy),
                  (cz + hh * 0.9, hw, hd, cx, cy), (cz + hh, hw * k, hd * k, cx, cy), (cz + hh, 0, 0, cx, cy)], segs, power)

def lantern():
    root = empty("hand_r")
    wood, glassm, cap = mat("lantern_frame", DARK, 0.4, 0.5), glow("lantern_glow", GOLD, 2.5), mat("lantern_cap", TEAL)
    parts = [(capsule_bm((0, -0.05, 0), (0, 0.05, 0), 0.011, 0.011, segs=12, hem=3), wood)]       # the bar in the fist
    for y in (-0.05, 0.05):                                                                        # bail down to the cap
        parts.append((tube_bm([(0, y, 0), (0, y * 1.05, -0.04), (0, y * 0.5, -0.075)], 0.006), wood))
    parts.append((lathe([(-0.10, 0, 0, 0, 0), (-0.10, 0.05, 0.05, 0, 0), (-0.085, 0.056, 0.056, 0, 0), (-0.07, 0.03, 0.03, 0, 0),
                         (-0.062, 0, 0, 0, 0)], 28), cap))
    parts.append((ellipsoid_bm((0, 0, -0.15), (0.047, 0.047, 0.056), segs=24, rings=14), glassm))
    parts.append((lathe([(-0.215, 0, 0, 0, 0), (-0.215, 0.05, 0.05, 0, 0), (-0.195, 0.054, 0.054, 0, 0), (-0.19, 0, 0, 0, 0)], 28), cap))
    for a in (0.785, 2.356, 3.927, 5.498):
        x, y = 0.05 * math.cos(a), 0.05 * math.sin(a)
        parts.append((tube_bm([(x, y, -0.10), (x, y, -0.20)], 0.005), wood))
    obj("lantern_body", parts, root)
    return root

def pennant():
    root = empty("hand_r")
    parts = [(capsule_bm((0, 0, -0.075), (0, 0, 0.40), 0.012, 0.011, segs=14, hem=3), mat("pennant_stick", TAN)),
             (ellipsoid_bm((0, 0, 0.41), (0.02, 0.02, 0.02), segs=14, rings=8), mat("pennant_knob", GOLD, 0.3, 0.7))]
    flag = grid_bm(lambda u, v: (-0.012 - 0.19 * u, 0.012 * math.sin(u * 7.0), 0.385 - 0.065 * u - (0.13 * (1 - u)) * v), 10, 6)
    parts.append((solidify_bm(flag, 0.006), mat("pennant_flag", ORANGE)))
    obj("pennant_body", parts, root)
    return root

def shovel():
    root = empty("hand_r")
    wood, steel = mat("shovel_wood", TAN, 0.6, 0.3), mat("shovel_steel", STEEL, 0.35, 0.6)
    parts = [(capsule_bm((0, 0, -0.09), (0, 0, 0.36), 0.013, 0.013, segs=16, hem=3), wood),
             (tube_bm([(-0.035, 0, -0.10), (0.035, 0, -0.10)], 0.012), wood),                      # T grip at the end
             (lathe([(0.335, 0, 0, 0, 0), (0.335, 0.017, 0.017, 0, 0), (0.39, 0.02, 0.018, 0, 0), (0.39, 0, 0, 0, 0)], 20), steel)]
    prof = [(-0.004, 0.0, 0.0), (0.0, 0.050, 0.008), (0.012, 0.070, 0.010), (0.07, 0.076, 0.010),
            (0.13, 0.070, 0.009), (0.18, 0.046, 0.008), (0.21, 0.020, 0.006), (0.22, 0.0, 0.0)]
    blade = lathe([(0.385 + z, rx, ry * 2.0, 0, 0) for z, rx, ry in prof], 40)
    for v in blade.verts:
        v.co.y -= 0.02 * (v.co.x / 0.076) ** 2
    parts.append((blade, steel))
    obj("shovel_body", parts, root)
    return root

def fishing_rod():
    root = empty("hand_r")
    cork, rodm, reelm = mat("rod_cork", "#C9A27A", 0.8, 0.1), mat("rod_shaft", "#4A4033", 0.4, 0.4), mat("rod_reel", STEEL, 0.3, 0.7)
    line, blue, yel = mat("rod_line", "#E8EEF2", 0.5, 0.2), mat("rod_bobber_blue", "#3F8FD8"), mat("rod_bobber_yellow", "#F2C230")
    parts = [(capsule_bm((0, 0, -0.09), (0, 0, 0.10), 0.016, 0.016, segs=16, hem=3), cork)]            # cork handle, fist closes here
    # tapered shaft (thin tube segments), leaning slightly forward (-y)
    pts = [(0, -0.002 * i, 0.10 + 0.075 * i) for i in range(0, 10)]
    for i in range(len(pts) - 1):
        r = 0.011 - 0.0095 * (i / (len(pts) - 1))
        parts.append((tube_bm([pts[i], pts[i + 1]], max(r, 0.0018)), rodm))
    parts.append((lathe([(-0.012, 0, 0, 0.0, -0.045), (-0.012, 0.016, 0.012, 0.0, -0.045), (0.012, 0.016, 0.012, 0.0, -0.045), (0.012, 0, 0, 0.0, -0.045)], 18), reelm))
    tip = pts[-1]
    parts.append((tube_bm([tip, (tip[0], tip[1] - 0.01, tip[2] - 0.12), (tip[0], tip[1] - 0.01, tip[2] - 0.30)], 0.0018), line))
    b = (tip[0], tip[1] - 0.01, tip[2] - 0.33)
    parts.append((ellipsoid_bm((b[0], b[1], b[2] + 0.013), (0.015, 0.015, 0.014), segs=14, rings=8), yel))
    parts.append((ellipsoid_bm((b[0], b[1], b[2] - 0.013), (0.015, 0.015, 0.014), segs=14, rings=8), blue))
    obj("fishing_rod_body", parts, root)
    return root

def watering_can():
    root = empty("hand_r")
    body, trim = mat("can_body", "#7FA3B8", 0.45, 0.5), mat("can_trim", "#5D8296", 0.45, 0.5)
    parts = [(capsule_bm((0, -0.05, 0), (0, 0.05, 0), 0.011, 0.011, segs=12, hem=3), trim)]            # handle bar in the fist
    for y in (-0.05, 0.05):
        parts.append((tube_bm([(0, y, 0), (0, y * 1.05, -0.03), (0, y * 0.9, -0.06)], 0.007), trim))
    parts.append((lathe([(-0.15, 0, 0, 0, 0), (-0.15, 0.062, 0.062, 0, 0), (-0.14, 0.07, 0.07, 0, 0), (-0.09, 0.072, 0.072, 0, 0),
                         (-0.06, 0.066, 0.066, 0, 0), (-0.055, 0.04, 0.04, 0, 0), (-0.055, 0, 0, 0, 0)], 28), body))
    parts.append((tube_bm(ring(0, 0, -0.06, 0.068, 0.068, 28), 0.005, cyclic=True), trim))
    parts.append((tube_bm([(0, -0.06, -0.125), (0, -0.12, -0.10), (0, -0.17, -0.075)], 0.012), trim))    # spout forward and up
    parts.append((lathe([(-0.07, 0, 0, 0, 0), (-0.07, 0.03, 0.03, 0, 0), (-0.065, 0.034, 0.034, 0, 0), (-0.065, 0, 0, 0, 0)], 16), trim))
    parts[-1] = (parts[-1][0], trim)
    obj("watering_can_body", parts, root)
    return root

def crate():
    root = empty("hand_r")
    wood, band = mat("crate_wood", TAN, 0.7, 0.2), mat("crate_band", DARK, 0.5, 0.4)
    parts = [(rbox((0, -0.02, 0.0), 0.095, 0.075, 0.07), wood)]
    for z in (-0.045, 0.045):
        parts.append((tube_bm(ring(0, -0.02, z, 0.097, 0.077, 40, 8), 0.006, cyclic=True), band))
    for s in (-1, 1):                                                                              # rope handles in the fists
        parts.append((tube_bm([(s * 0.092, -0.05, 0.02), (s * 0.125, -0.035, 0.0), (s * 0.125, 0.0, 0.0), (s * 0.125, 0.012, 0.0),
                               (s * 0.092, 0.02, 0.02)], 0.008), band))
    obj("crate_body", parts, root)
    return root

def parcel():
    root = empty("hand_r")
    parts = [(rbox((0, 0.0, 0.01), 0.07, 0.055, 0.075, power=6), mat("parcel_paper", "#E9D8B4", 0.8, 0.15))]
    string = mat("parcel_string", PURPLE)
    parts.append((tube_bm(ring(0, 0.0, 0.01, 0.072, 0.057, 36, 6), 0.006, cyclic=True), string))
    parts.append((tube_bm([(0, -0.057, -0.065), (0, -0.057, 0.085), (0, 0.057, 0.085), (0, 0.057, -0.065)], 0.006), string))
    for s in (-1, 1):
        parts.append((ellipsoid_bm((s * 0.02, -0.03, 0.095), (0.022, 0.012, 0.014), segs=12, rings=8), string))
    obj("parcel_body", parts, root)
    return root

# ------------------------------------------------------------------------------------------ items
ITEMS = {
    "sneakers": dict(name="Sneakers", slots=["foot_l", "foot_r"], replaces_body_part=["foot_l", "foot_r"], fn=sneakers),
    "boots": dict(name="Boots", slots=["foot_l", "foot_r"], replaces_body_part=["foot_l", "foot_r"], fn=boots),
    "rocket_boots": dict(name="Rocket Boots", slots=["foot_l", "foot_r"], replaces_body_part=["foot_l", "foot_r"], fn=rocket_boots),
    "kneepads": dict(name="Kneepads", slots=["knee_l", "knee_r"], fn=kneepads),
    "cape": dict(name="Cape", slots=["back"], replaces_body_part=["tail"], fn=cape,
                 spring={"node": "cape_pivot", "stiffness": 45.0, "damping": 7.0, "gain": 0.25, "rest_deg": 4.0, "max_deg": 65.0}),
    "jetpack": dict(name="Jetpack", slots=["back"], replaces_body_part=["tail"], fn=jetpack),
    "hat": dict(name="Bucket Hat", slots=["head"], replaces_body_part=["headwear"], fn=hat),
    "sunglasses": dict(name="Sunglasses", slots=["face"], fn=sunglasses),
    "gloves": dict(name="Gloves", slots=["hand_l", "hand_r"], replaces_body_part=["hand_l", "hand_r"], fn=gloves),
    "belt": dict(name="Belt", slots=["waist"], fn=belt, fit={"boxy": {"scale": [1.03, 1.0, 1.05]}}),
    # held items: `hold` in item space, Blender axes here; the JSON stores them in glTF/Godot axes (y up, +z front)
    "lantern": dict(name="Lantern", slots=["hand_r"], fn=lantern, fit={"critter": {"scale": 0.62}}, hold=dict(style="one_hand_low", grip_r=(0, 0, 0))),
    "pennant": dict(name="Pennant", slots=["hand_r"], fn=pennant, fit={"critter": {"scale": 0.62}}, hold=dict(style="one_hand_raised", grip_r=(0, 0, 0), axis=(0, 0, 1))),
    "shovel": dict(name="Shovel", slots=["hand_r"], fn=shovel, fit={"critter": {"scale": 0.62}},
                   hold=dict(style="two_hand_diagonal", grip_r=(0, 0, 0), grip_l=(0, 0, 0.27), axis=(0, 0, 1))),
    "fishing_rod": dict(name="Fishing Rod", slots=["hand_r"], fn=fishing_rod, fit={"critter": {"scale": 0.62}},
                        hold=dict(style="one_hand_raised", grip_r=(0, 0, 0), axis=(0, 0, 1))),
    "watering_can": dict(name="Watering Can", slots=["hand_r"], fn=watering_can, fit={"critter": {"scale": 0.62}},
                         hold=dict(style="one_hand_low", grip_r=(0, 0, 0))),
    "crate": dict(name="Crate", slots=["hand_r"], fn=crate, hold=dict(style="two_hand_front", grip_r=(-0.125, 0, 0), grip_l=(0.125, 0, 0))),
    "parcel": dict(name="Parcel", slots=["hand_r"], fn=parcel, hold=dict(style="chest_clutch", grip_r=(-0.078, 0, 0), grip_l=(0.078, 0, 0))),
}

def gl_axes(v):
    """Blender (x, y, z) -> glTF / Godot (x, z, -y)."""
    return [round(v[0], 5), round(v[2], 5), round(-v[1], 5) + 0.0]

def export(root, path):
    bpy.ops.object.select_all(action="DESELECT")
    for ob in [root] + list(root.children_recursive):
        ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True,
                              export_animations=False, export_extras=True, export_yup=True)

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--only", default="")
    a = ap.parse_args(argv)
    only = [x for x in a.only.split(",") if x]
    for gid, spec in ITEMS.items():
        if only and gid not in only:
            continue
        kit.reset_scene()
        M.cache.clear()
        root = spec["fn"]()
        export(root, os.path.join(a.outdir, f"{gid}.glb"))
        d = {"id": gid, "name": spec["name"], "slots": spec["slots"], "scene": f"{gid}.glb",
             "replaces_body_part": spec.get("replaces_body_part", []), "fit": spec.get("fit", {}),
             "level_up": {"max": 3, "scale_step": 0.06}}
        if "spring" in spec:
            d["spring"] = spec["spring"]
        if "hold" in spec:      # grips + the resolved hold poses per body type, all in glTF / Godot axes
            import hold as H
            h = spec["hold"]
            d["hold"] = {"style": h["style"], **{k: gl_axes(h[k]) for k in ("grip_r", "grip_l", "axis") if k in h}}
            poses = {}
            for bt in ["standard"] + sorted(H.BODY_STYLES):
                st = H.style_for(h["style"], "R", bt)
                poses[bt] = {k: (gl_axes(v) if k != "follow" else v) for k, v in st.items()}
            d["hold"]["poses"] = poses
            d["hold"]["action_follow"] = dict(H.ACTION_FOLLOW, **(h.get("follow") or {}))
            d["hold"]["rigid_actions"] = sorted(H.ACTION_RIGID)
            d["hold"]["fist"] = {"radii": gl_axes(H.FIST)[:2] + [H.FIST[1]], "thumb": gl_axes(H.THUMB[0]), "thumb_radii": [H.THUMB[1][0], H.THUMB[1][2], H.THUMB[1][1]]}
        with open(os.path.join(a.outdir, f"{gid}.json"), "w") as f:
            json.dump(d, f, indent=2); f.write("\n")
        print("GEAR_OK", gid)
