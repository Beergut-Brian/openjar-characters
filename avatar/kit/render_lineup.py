"""Any characters in 3D at true relative scale on one ground line.

    blender -b --factory-startup -P avatar/kit/render_lineup.py -- --cast jeff,chuck,zorp --out characters/batch1_lineup.png [--samples 64]
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import jarling_kit as kit
import render_common as rc

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--cast", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--samples", type=int, default=64); ap.add_argument("--gap", type=float, default=0.3)
a = ap.parse_args(argv)

def bounds(j):
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

kit.reset_scene()
rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
rc.sunny_lights(2.8, 2.6)
rc.ground("#D3E3EC", size=400)
x = 0.0; sizes = []
for i, c in enumerate(a.cast.split(",")):
    j = kit.build_jarling(json.load(open(os.path.join(ROOT, "characters", c, "jarling.json"))), prefix=f"l{i}_")
    kit.pose_at(j, "idle", 1)
    lo, hi = bounds(j)
    rc.place(j, (x - lo.x, 0, 0), 0)
    sizes.append((c, round(hi.z, 2)))
    x += (hi.x - lo.x) + a.gap
total = x - a.gap
W, H = 2400, 1000
top = max(h for _, h in sizes)
ortho = max(total * 1.06, top * 1.25 * W / H)
cz = ortho * H / W / 2 - 0.08 * ortho * H / W
rc.setup_render(W, H, a.samples)
rc.camera((total / 2, -60, cz), (total / 2, 0, cz), ortho=ortho)
rc.render(os.path.join(ROOT, a.out))
print("LINEUP heights (m):", sizes)
