"""Held items for every Jarling body type (standard, critter, giant): grips, hold styles, fists.

The same rules run in Godot (`godot/jarling_hold.gd`); this is the Blender side, used for the
renders, for the checks and to bake a kit piece's hold into a character's own actions.

A held item defines, in its own space (Blender axes: x = the character's left, -y = front, z up):
    grip_r   where the main hand closes (the hand whose slot the item is in; right by default)
    grip_l   optional: where the off hand closes (two-handed items)
    axis     optional: the handle's direction at grip_r, pointing at the item's top. The item is
             turned so `axis` runs along the fist (slot -y). Without it the item keeps slot axes.
    style    one of STYLES

A hold style is body-independent: it says where the main arm points, how the fist (the hand slot)
is turned and where the off arm aims, all as directions in character space. From those and the
rig's rest pose come the arm and hand rotations (`hold_locals`), which are layered over an action
with `follow` (0 = the hold pose, 1 = the action's own arms). For a two-handed item the main hand
then turns about its wrist and the off arm aims so the off fist sits exactly on grip_l
(sphere-sphere intersection: no elbows, so the reach is fixed; the arm stretches a little if the
grip is out of reach).
"""
import math, os, sys
import bpy, bmesh
from mathutils import Vector, Matrix, Quaternion
import jarling_kit as kit

# Right hand is the main hand; mirrored in x for the left. arm = where the main arm points,
# axis = where the fist axis (slot -y, the handle) points, up = the slot's +z, off = where the
# off arm aims before it snaps to grip_l. follow = how much of the action's own arm motion shows.
STYLES = {
    "one_hand_low":      dict(arm=(-0.20, -0.22, -1.0), axis=(0.0, -1.0, -0.10), up=(0, 0, 1), follow=0.35),
    "one_hand_raised":   dict(arm=(-0.42, -1.0, -0.62), axis=(-0.30, -0.22, 1.0), up=(0, 1, 0.2), follow=0.2),
    "two_hand_diagonal": dict(arm=(-0.30, -0.62, -1.0), axis=(0.75, -0.30, 1.0), up=(0, 1, 0.3),
                              off=(-0.45, -1.0, 0.12), follow=0.15),
    "two_hand_front":    dict(arm=(0.02, -1.0, -0.62), axis=(0, -1, 0), up=(0, 0, 1), off=(-0.02, -1.0, -0.62), follow=0.15),
    "chest_clutch":      dict(arm=(0.42, -1.0, -0.42), axis=(0, -1, 0), up=(0, 0, 1), off=(-0.42, -1.0, -0.42), follow=0.15),
}
# per body type tweaks (same keys). Critter arms are short and start low on a wide body; a giant's
# stubby arms sit beside a huge belly.
BODY_STYLES = {
    "critter": {"one_hand_low": dict(arm=(-1.0, -0.45, -0.75)),
                "one_hand_raised": dict(arm=(-0.8, -1.0, -0.1)),
                "two_hand_diagonal": dict(arm=(0.20, -1.0, -0.35), axis=(0.6, -0.2, 1.0), off=(-0.30, -1.0, 0.65)),
                "two_hand_front": dict(arm=(0.25, -1.0, 0.0), off=(-0.25, -1.0, 0.0)),
                "chest_clutch": dict(arm=(0.45, -1.0, 0.1), off=(-0.45, -1.0, 0.1))},
    "giant": {"one_hand_low": dict(arm=(-0.75, -0.8, -0.6)),
              "one_hand_raised": dict(arm=(-0.7, -1.0, 0.0)),
              "two_hand_diagonal": dict(arm=(-0.5, -1.0, -0.5), off=(-0.2, -1.0, 0.1)),
              "two_hand_front": dict(arm=(-0.2, -1.0, -0.2), off=(0.2, -1.0, -0.2)),
              "chest_clutch": dict(arm=(0.0, -1.0, 0.0), off=(0.0, -1.0, 0.0))},
}
ACTION_RIGID = {"dig"}               # in these the action aims the tool itself: the main hand is not turned, the off arm reaches (and stretches) to grip_l
ACTION_FOLLOW = {"cheer": 0.45, "dig": 1.0}     # the action's arms show more in these (unless the item says otherwise)
FIST = (0.040, 0.047, 0.044)        # fist radii in hand-slot space (x thickness, y front-back, z height)
THUMB = ((-0.012, -0.036, 0.004), (0.020, 0.018, 0.026))   # thumb centre (for the left hand; x mirrored) and radii

def body_type(j):
    return (j.P.get("body") or {}).get("type", "standard")

def style_for(style, side="R", btype="standard"):
    """`style` is a name from STYLES, or a dict with the same keys (an action's own key pose)."""
    if isinstance(style, dict):
        st = dict(style)
    else:
        st = dict(STYLES[style]); st.update(BODY_STYLES.get(btype, {}).get(style, {}))
    if side == "L":
        for k in ("arm", "axis", "up", "off"):
            if k in st:
                st[k] = (-st[k][0], st[k][1], st[k][2])
    return st

def arc(a, b):
    return Vector(a).normalized().rotation_difference(Vector(b).normalized())

def slot_frame(axis, up):
    """3x3 rotation whose -y column is `axis` and +z column is `up` (made square to it)."""
    g = Vector(axis).normalized()
    u = Vector(up); u = (u - g * u.dot(g)).normalized()
    y = -g
    return Matrix((y.cross(u), y, u)).transposed()

def item_matrix(grip_r=(0, 0, 0), axis=None):
    """Item space -> slot space: turns `axis` onto the fist axis and puts grip_r at the slot origin."""
    A = arc(axis, (0, -1, 0)).to_matrix().to_4x4() if axis else Matrix.Identity(4)
    return A @ Matrix.Translation(-Vector(grip_r))

def _about(p, q):
    return Matrix.Translation(p) @ q.to_matrix().to_4x4() @ Matrix.Translation(-Vector(p))

def hold_locals(rig, style, side="R", btype="standard"):
    """{bone: pose quaternion} for the style's arm pose on this rig, from the rest pose alone."""
    st = style_for(style, side, btype)
    o = "L" if side == "R" else "R"
    bones = rig.data.bones
    out = {}
    Ma, Mh = bones[f"arm.{side}"].matrix_local, bones[f"hand.{side}"].matrix_local
    sh, wr = Ma.translation, Mh.translation
    Ma2 = _about(sh, arc(wr - sh, st["arm"])) @ Ma
    out[f"arm.{side}"] = (Ma.inverted() @ Ma2).to_quaternion()
    Mh_par = Ma2 @ Ma.inverted() @ Mh                 # the hand carried by the arm
    Mh2 = Matrix.Translation(Mh_par.translation) @ slot_frame(st["axis"], st["up"]).to_4x4() @ Matrix.Translation(-wr) @ Mh
    out[f"hand.{side}"] = (Mh_par.inverted() @ Mh2).to_quaternion()
    if "off" in st:
        Mo, Mho = bones[f"arm.{o}"].matrix_local, bones[f"hand.{o}"].matrix_local
        out[f"arm.{o}"] = (Mo.inverted() @ _about(Mo.translation, arc(Mho.translation - Mo.translation, st["off"])) @ Mo).to_quaternion()
        out[f"hand.{o}"] = Quaternion()
    return out

def follow_for(hold, action):
    f = hold.get("follow")
    if isinstance(f, dict):
        if action in f:
            return float(f[action])
        f = f.get("default")
    if f is None:
        f = ACTION_FOLLOW.get(action, STYLES[hold["style"]]["follow"])
    return float(f)

def piece_matrix(B, side, grip_r=(0, 0, 0), axis=None):
    """For a kit piece modelled upright in item space: item space -> the rest pose, in the fist of
    B's `side` hand (the piece is skinned to that hand bone; the hold pose is baked into the actions)."""
    return Matrix.Translation(B.hand_c[side]) @ Matrix.Scale(B.L["limb"], 4) @ item_matrix(grip_r, axis)

# ------------------------------------------------------------------------------------ fists
def fist_bm(side="R", scale=1.0, claws=0):
    """A closed mitten in hand-slot space (origin = the grip). `claws` adds curled claw tips."""
    s = 1 if side == "L" else -1
    bm = kit.ellipsoid_bm((0, 0, 0), tuple(r * scale for r in FIST), segs=22, rings=12)
    parts = [bm]
    c, r = THUMB
    parts.append(kit.ellipsoid_bm((s * c[0] * scale, c[1] * scale, c[2] * scale), tuple(x * scale for x in r), segs=14, rings=8))
    for k in range(claws):
        off = (k - (claws - 1) / 2) * 0.026 * scale
        parts.append(kit.ellipsoid_bm((s * -0.006 * scale, -0.030 * scale + abs(off) * 0.15, off - 0.012 * scale),
                                      (0.018 * scale, 0.026 * scale, 0.014 * scale), segs=12, rings=8))
    return parts

def add_fist(j, side):
    """Blender renders: hide the open hand part and put a fist on the hand slot. Returns the fist."""
    sl = side.lower()
    part = getattr(j, "part_obs", {}).get(f"hand_{sl}")
    if part is None or part.hide_render:
        return None
    marker = j.slots[f"hand_{sl}"]
    claws = int((j.P.get("paws") or {}).get("claws", 0)) if (j.P.get("paws") or {}).get("style", "") == "claws" else 0
    out = bmesh.new()
    for pbm in fist_bm(side, 1.0, claws):
        vm = {v: out.verts.new(v.co) for v in pbm.verts}
        for f in pbm.faces:
            out.faces.new([vm[v] for v in f.verts]).smooth = True
        pbm.free()
    out.normal_update()
    me = bpy.data.meshes.new(f"{j.prefix}fist_{sl}"); out.to_mesh(me); out.free()
    me.materials.append(part.data.materials[0])
    ob = bpy.data.objects.new(me.name, me)
    j.coll.objects.link(ob) if hasattr(j, "coll") else bpy.context.scene.collection.objects.link(ob)
    ob.parent = marker
    part.hide_render = True; part.hide_viewport = True
    return ob

# ------------------------------------------------------------------------------- gear in Blender
def _gear():
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gear")
    if here not in sys.path:
        sys.path.insert(0, here)
    import build_gear
    return build_gear

def attach_gear(j, gear_id, side=None):
    """Build a gear item in the scene on j's hand slot (as the Godot runtime does) and return its
    hold: {"side", "style", "grip_l" (slot space, or None), "follow", "id"}. Items without grips sit
    at the slot origin exactly as before."""
    bg = _gear()
    spec = bg.ITEMS[gear_id]
    try:
        ok = all(m.name in bpy.data.materials for m in bg.M.cache.values())
    except ReferenceError:
        ok = False
    if not ok:
        bg.M.cache.clear()      # the scene was reset since the last item
    root = spec["fn"]()
    slot = spec["slots"][0]
    side = side or ("L" if slot.endswith("_l") else "R")
    marker = j.slots[f"hand_{side.lower()}"]
    root.parent = marker
    h = spec.get("hold")
    if not h:
        return None
    fit = spec.get("fit", {})
    fit = fit.get(j.P.get("id"), fit.get(body_type(j) if body_type(j) != "standard" else j.P["body"].get("build"), {}))
    k = fit.get("scale", 1.0)
    M = Matrix.Scale(float(k if not isinstance(k, (list, tuple)) else k[0]), 4) @ item_matrix(h.get("grip_r", (0, 0, 0)), h.get("axis"))
    root.matrix_basis = M
    add_fist(j, side)
    gl = h.get("grip_l")
    if gl is not None:
        add_fist(j, "L" if side == "R" else "R")
    return {"id": gear_id, "side": side, "style": h["style"], "grip_l": (M @ Vector(gl)) if gl is not None else None,
            "follow": h.get("follow")}

# ------------------------------------------------------------------------------- posing
def _circle_point(W, rho, c, r, t0):
    """The point at rho from W and r from c nearest t0; (point, reachable)."""
    n = c - W; d = n.length
    if d < 1e-9:
        return W + (t0 - W).normalized() * rho, False
    n /= d
    if d >= rho + r or d <= abs(rho - r):
        return W + n * (rho if d >= rho + r or rho > r else -rho), False
    a = (rho * rho - r * r + d * d) / (2 * d)
    h = math.sqrt(max(rho * rho - a * a, 0.0))
    m = W + n * a
    v = (t0 - m); v -= n * v.dot(n)
    if v.length < 1e-9:
        v = n.orthogonal()
    return m + v.normalized() * h, True

def apply(j, holds, action="idle"):
    """Layer the hold poses over j's current pose (call after kit.pose_at) and snap two-handed
    grips. The rig's action is detached so the pose stays. Returns {(id, hand): distance in m}."""
    rig = j.rig
    bt = body_type(j)
    bpy.context.view_layer.update()
    snap = {pb.name: (pb.rotation_quaternion.copy(), pb.location.copy(), pb.scale.copy()) for pb in rig.pose.bones}
    if rig.animation_data:
        rig.animation_data.action = None
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion, pb.location, pb.scale = snap[pb.name]
    inv = lambda: rig.matrix_world.inverted()
    for h in holds:
        f = follow_for(h, action)
        for bone, q in hold_locals(rig, h["style"], h["side"], bt).items():
            pb = rig.pose.bones[bone]
            pb.rotation_quaternion = q.slerp(snap[bone][0], f)
            if bone.startswith("arm"):
                pb.location = snap[bone][1] * f
    bpy.context.view_layer.update()
    out = {}
    for h in holds:
        S = h["side"]; O = "L" if S == "R" else "R"
        key = h.get("id", h["style"])
        out[(key, "main")] = 0.0
        if h.get("grip_l") is None:
            continue
        for _ in range(8):      # parents with squash and stretch make one pass slightly inexact
            pbh, pbo = rig.pose.bones[f"hand.{S}"], rig.pose.bones[f"arm.{O}"]
            W, c = pbh.head.copy(), pbo.head.copy()
            g = (inv() @ j.slots[f"hand_{S.lower()}"].matrix_world) @ Vector(h["grip_l"])
            t0 = (inv() @ j.slots[f"hand_{O.lower()}"].matrix_world).translation
            r, rho = (t0 - c).length, (g - W).length
            p, ok = _circle_point(W, rho, c, r, t0)
            if action in ACTION_RIGID:
                p, ok = g, abs((g - c).length - r) < 1e-5
            pbh.matrix = _about(W, arc(g - W, p - W)) @ pbh.matrix
            bpy.context.view_layer.update()
            if not ok:                      # out of reach: stretch (or squash) the off arm along its length
                yb = (pbo.tail - pbo.head).normalized()
                along = (t0 - c).dot(yb); perp2 = max(r * r - along * along, 0.0)
                D = (p - c).length
                k = math.sqrt(max(D * D - perp2, 1e-8)) / max(along, 1e-6)
                pbo.scale.y = min(max(pbo.scale.y * k, 0.5), 2.5)
                bpy.context.view_layer.update()
                t0 = (inv() @ j.slots[f"hand_{O.lower()}"].matrix_world).translation
            pbo.matrix = _about(c, arc(t0 - c, p - c)) @ pbo.matrix
            bpy.context.view_layer.update()
        g = (inv() @ j.slots[f"hand_{S.lower()}"].matrix_world) @ Vector(h["grip_l"])
        t = (inv() @ j.slots[f"hand_{O.lower()}"].matrix_world).translation
        out[(key, "off")] = (g - t).length
    return out
