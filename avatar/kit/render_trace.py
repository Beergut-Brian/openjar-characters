"""Flat-colour trace renders of one Jarling: the base the 2D pixel forms are traced from.

    blender -b --factory-startup -P avatar/kit/render_trace.py -- --char gnome_foreman \
        [--views front,side,back] [--action idle --frame 1] [--expression whistle] [--gear shovel] [--tag whistle]

Every material becomes emission-only with its exact base colour (image textures, e.g. the face
atlas, are passed straight through), no lights, transparent film, orthographic camera,
512 px per 1.2 m (Jeff with his comb is 32 px in The Hill, so the sprite scale is 1/16).
Writes `.scratch/trace/<id>[_<tag>]_<view>.png` and `.scratch/trace/<id>[_<tag>].json`
(height in metres, px per metre, feet row). `--expression X` alone looks up `expression_poses`
in the params (the Gnome's `whistle`). `--gear` attaches an avatar/gear item with hold.py
(the Mole's dig). See tools/pixel/trace3d.py for the reduction to sprite pixels.
"""
import sys, os, json, argparse, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import jarling_kit as kit
import render_common as rc

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--char", default=None); ap.add_argument("--params", default=None)   # --params: a proposal's jarling.json
ap.add_argument("--views", default="front,side,back")
ap.add_argument("--action", default=None); ap.add_argument("--frame", type=int, default=None)
ap.add_argument("--expression", default=None); ap.add_argument("--gear", default=None)
ap.add_argument("--tag", default=""); ap.add_argument("--out", default=os.path.join(ROOT, ".scratch", "trace"))
a = ap.parse_args(argv)
PX_PER_M = 512 / 1.2
OUT = a.out; os.makedirs(OUT, exist_ok=True)
P = json.load(open(a.params or os.path.join(ROOT, "characters", a.char, "jarling.json")))
a.char = a.char or P["id"]
name = a.char + (f"_{a.tag}" if a.tag else "")
YAW = {"front": 0, "side": -90, "back": 180}       # side faces screen-right


def bounds(j):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for ob in j.rig.children_recursive:
        if ob.type != "MESH" or ob.hide_render:
            continue
        eo = ob.evaluated_get(dg); me = eo.to_mesh()
        for v in me.vertices:
            w = eo.matrix_world @ v.co
            lo = Vector(map(min, lo, w)); hi = Vector(map(max, hi, w))
        eo.to_mesh_clear()
    return lo, hi


def flatten_materials():
    """Emission-only, exact base colour; see-through glass (alpha < 0.3) becomes invisible."""
    for m in bpy.data.materials:
        if not m.use_nodes or not m.node_tree:
            continue
        nt = m.node_tree
        p = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        out = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
        if not p or not out:
            continue
        src = p.inputs["Base Color"]
        alpha = p.inputs["Alpha"].default_value
        em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Strength"].default_value = 1.0
        if src.is_linked:
            nt.links.new(src.links[0].from_socket, em.inputs["Color"])
        else:
            em.inputs["Color"].default_value = src.default_value
        if alpha < 0.3 and not p.inputs["Alpha"].is_linked:
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            nt.links.new(tr.outputs[0], out.inputs["Surface"])
        else:
            nt.links.new(em.outputs[0], out.inputs["Surface"])


def pose():
    kit.reset_scene()
    j = kit.build_jarling(P, prefix="tr_")
    action, frame = a.action, a.frame
    if a.expression and action is None:
        ep = (P.get("expression_poses") or {}).get(a.expression) or {}
        action, frame = ep.get("action"), ep.get("frame")
    action, frame = action or "idle", frame or 1
    holds = []
    if a.gear:
        import hold
        h = hold.attach_gear(j, a.gear)
        holds = [h] if h else []
    kit.pose_at(j, action, frame)
    if a.expression:
        kit.set_expression(j, a.expression)
    if holds:
        import hold
        hold.apply(j, holds, action)
    return j, action, frame


j, action, frame = pose()
flatten_materials()
w = bpy.data.worlds.new("none"); bpy.context.scene.world = w
w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
meta = {"id": a.char, "tag": a.tag, "action": action, "frame": frame, "expression": a.expression,
        "px_per_m": PX_PER_M, "views": {}}
for view in [v for v in a.views.split(",") if v]:
    rc.place(j, (0, 0, 0), YAW[view])
    lo, hi = bounds(j)
    pad = 0.05
    w_m = (hi.x - lo.x) + 2 * pad; h_m = (hi.z - min(lo.z, 0.0)) + 2 * pad
    W, H = max(8, round(w_m * PX_PER_M)), max(8, round(h_m * PX_PER_M))
    sc = rc.setup_render(W, H, 1)
    sc.cycles.use_denoising = False; sc.cycles.use_adaptive_sampling = False
    sc.cycles.pixel_filter_type = "BOX"; sc.cycles.filter_width = 0.01   # one hard sample per pixel
    sc.cycles.max_bounces = 0; sc.cycles.transparent_max_bounces = 16
    sc.render.film_transparent = True; sc.render.image_settings.color_mode = "RGBA"
    for ob in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(ob)
    cx = (hi.x + lo.x) / 2; cz = min(lo.z, 0.0) - pad + h_m / 2
    dist = 4 * max(hi.z, w_m) + 10
    cam = rc.camera((cx, -dist, cz), (cx, 0, cz), ortho=max(w_m, h_m)); cam.data.clip_end = 3 * dist
    path = os.path.join(OUT, f"{name}_{view}.png")
    rc.render(path)
    meta["views"][view] = {"file": os.path.basename(path), "height_m": round(hi.z - min(lo.z, 0.0), 4),
                           "ground_row": round(H - (pad - min(lo.z, 0.0)) * PX_PER_M), "w": W, "h": H}
json.dump(meta, open(os.path.join(OUT, f"{name}.json"), "w"), indent=1)
print(f"TRACE {name}: {action} f{frame}, height {meta['views'] and list(meta['views'].values())[0]['height_m']} m")
