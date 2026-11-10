"""Reference renders for one Jarling of any body type: turnaround, expressions, action pose, side view.

    blender -b --factory-startup -P avatar/kit/render_refs.py -- \
        --params characters/jeff/jarling.json --outdir characters/jeff/refs/jarling \
        [--only turnaround,expressions,action,side] [--samples 48]

Outputs `<id>_turnaround.png` (front, 3/4, side, back), `<id>_expressions.png` (the character's
expression list), `<id>_<action>.png` (params `ref_action`, default the kick) and `<id>_side.png`
(orthographic side view, transparent, 512 px per 1.2 m (Jeff with his comb, 32 px in The Hill): the base the 2D sprites
are traced from; `sprite_side.py` makes the sprite-scale sheet from it).

Framing follows the character's real size, so it works for a 0.6 m gnome and a 6 m dragon.
`ref_action` in the params: {"action": "yawn", "frame": 20, "expression": "yawn", "yaw": -28}.
"""
import sys, os, json, argparse, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import jarling_kit as kit
import render_common as rc

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--params", required=True); ap.add_argument("--outdir", required=True)
ap.add_argument("--only", default="turnaround,expressions,action,side"); ap.add_argument("--samples", type=int, default=48)
a = ap.parse_args(argv)
P = json.load(open(a.params)); pid = P["id"]
os.makedirs(a.outdir, exist_ok=True)
only = [("action" if o == "kick" else o) for o in a.only.split(",")]
OUT = os.path.abspath(a.outdir)
STD_H = 1.1          # a standard Jarling, metres
SIDE_PX = 512        # pixels per SPRITE_H in <id>_side.png
SPRITE_H = 1.2       # Jeff with his comb: what The Hill draws 32 px tall

def studio(ground="#D3E3EC"):
    kit.reset_scene()
    rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    if ground:
        rc.ground(ground, size=200)

def bounds(j):
    """World-space bounding box of a built Jarling in its current pose: (min, max) Vectors."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for ob in j.rig.children_recursive:
        if ob.type != "MESH":
            continue
        eo = ob.evaluated_get(dg); me = eo.to_mesh()
        for v in me.vertices:
            w = eo.matrix_world @ v.co
            lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
        eo.to_mesh_clear()
    return lo, hi

def expressions(j):
    return list(getattr(j, "expr_names", None) or kit.EXPRESSIONS)

# measure once (idle pose, at the origin)
kit.reset_scene()
j0 = kit.build_jarling(P, prefix="m_")
kit.pose_at(j0, "idle", 1)
lo, hi = bounds(j0)
H = hi.z; W = max(hi.x, -lo.x) * 2; D = max(hi.y, -lo.y) * 2
HEAD_R = float(getattr(j0, "L", {}).get("R", 0.235))      # head radius: frames the expression sheet
NAMES = expressions(j0)
print(f"REFS {pid}: height {H:.3f} m, width {W:.3f}, depth {D:.3f}, expressions {NAMES}")

if "turnaround" in only:
    studio()
    rc.setup_render(1600, 800, a.samples)
    step = max(max(W, D) * 1.12, H * 0.86, 0.5)
    for i, yaw in enumerate((0, -40, -90, 180)):     # front, 3/4, side, back
        j = kit.build_jarling(P, prefix=f"t{i}_")
        rc.place(j, ((i - 1.5) * step, 0, 0), yaw)
        kit.pose_at(j, "idle", 1)
    ortho = max(step * 4.1, H * 2.0 * 1.14)
    rc.camera((0, -12 * max(1, H), ortho * 0.159), (0, 0, ortho * 0.159), ortho=ortho)
    rc.render(os.path.join(OUT, f"{pid}_turnaround.png"))

if "expressions" in only:
    studio()
    n = len(NAMES)
    rc.setup_render(400 * n, 520, a.samples)
    k = HEAD_R / 0.235
    for i, ex in enumerate(NAMES):
        j = kit.build_jarling(P, prefix=f"e{i}_")
        rc.place(j, ((i - (n - 1) / 2) * 0.72 * k, 0, 0), 0)
        kit.pose_at(j, "idle", 1)
        kit.set_expression(j, ex)
    hz = j.L["head_c"].z
    rc.camera((0, -12 * k, hz + 2.4 * k), (0, 0, hz - 0.02 * k), ortho=0.725 * n * k)
    rc.render(os.path.join(OUT, f"{pid}_expressions.png"))

if "action" in only:
    ra = P.get("ref_action") or {"action": "kick", "frame": 17, "expression": P.get("ref_kick_expression", "happy"), "yaw": -28}
    studio("#C9DCE8")
    rc.setup_render(1280, 720, a.samples)
    j = kit.build_jarling(P, prefix="k_")
    kit.pose_at(j, ra["action"], int(ra.get("frame", 1)))
    if ra.get("expression"):
        kit.set_expression(j, ra["expression"])
    k = H / STD_H
    if ra["action"] == "kick":
        import render_scenes_ball as rb
        rb.make_ball("ball", Vector((-0.35, -0.95, 0.62)), 0.11, kit.Mats("refs_"))
    rc.place(j, (0, 0, 0), float(ra.get("yaw", -28)))
    rc.camera((-4.4 * k, -1.6 * k, 1.5 * k), (0, -0.35 * k * (1 if ra["action"] == "kick" else 0.3), 0.55 * k), lens=45)
    rc.render(os.path.join(OUT, f"{pid}_{ra['action']}.png"))

if "side" in only:
    studio(ground=None)
    j = kit.build_jarling(P, prefix="s_")
    rc.place(j, (0, 0, 0), -90)                      # faces screen-right
    kit.pose_at(j, "idle", 1)
    lo, hi = bounds(j)
    pad = 0.04 * SPRITE_H
    w_m = (hi.x - lo.x) + 2 * pad; h_m = hi.z + 2 * pad
    px = SIDE_PX / SPRITE_H
    sc = rc.setup_render(max(8, round(w_m * px)), max(8, round(h_m * px)), a.samples)
    sc.render.film_transparent = True
    sc.render.image_settings.color_mode = "RGBA"
    cx = (hi.x + lo.x) / 2
    rc.camera((cx, -12 * max(1, H), h_m / 2 - pad), (cx, 0, h_m / 2 - pad), ortho=max(w_m, h_m))
    rc.render(os.path.join(OUT, f"{pid}_side.png"))
    print(f"SIDE {pid}: {SIDE_PX} px per {SPRITE_H} m, feet {round(pad * px)} px above the bottom edge")
