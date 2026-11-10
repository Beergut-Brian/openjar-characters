"""The Hill's cast in 3D: the lineup at true relative scale, and front views for the 2D/3D compare sheet.

    blender -b --factory-startup -P avatar/kit/render_residents.py -- [--only lineup,fronts] [--samples 64]

lineup -> characters/residents_3d_lineup.png  (Jeff, Chuck, Mole, Gnome Foreman, Caveman, Dragon; one ground line)
fronts -> .scratch/fronts/<id>.png            (transparent front views; compare_sheet.py pairs them with the sprites)
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
ap.add_argument("--only", default="lineup,fronts"); ap.add_argument("--samples", type=int, default=64)
a = ap.parse_args(argv)
only = a.only.split(",")
CAST = ["jeff", "chuck", "mole", "gnome_foreman", "caveman", "dragon"]
load = lambda c: json.load(open(os.path.join(ROOT, "characters", c, "jarling.json")))

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

if "lineup" in only:
    kit.reset_scene()
    rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    rc.ground("#D3E3EC", size=400)
    x = 0.0; gap = 0.45; sizes = []
    for i, c in enumerate(CAST):
        j = kit.build_jarling(load(c), prefix=f"l{i}_")
        kit.pose_at(j, "idle", 1)
        lo, hi = bounds(j)
        if c == "dragon":
            x += 0.5
        rc.place(j, (x - lo.x, 0, 0), 0)
        sizes.append((c, round(hi.z, 2)))
        x += (hi.x - lo.x) + gap
    total = x - gap
    W, H = 2400, 1200
    top = max(h for _, h in sizes)
    ortho = max(total * 1.06, top * 1.16 * W / H)
    cz = ortho * H / W / 2 - 0.06 * ortho * H / W
    rc.setup_render(W, H, a.samples)
    rc.camera((total / 2, -60, cz), (total / 2, 0, cz), ortho=ortho)
    rc.render(os.path.join(ROOT, "characters", "residents_3d_lineup.png"))
    print("LINEUP heights (m):", sizes)

if "fronts" in only:
    out = os.path.join(ROOT, ".scratch", "fronts"); os.makedirs(out, exist_ok=True)
    for c in CAST[2:]:
        kit.reset_scene()
        rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
        rc.sunny_lights(2.8, 2.6)
        j = kit.build_jarling(load(c), prefix="f_")
        kit.pose_at(j, "idle", 1)
        lo, hi = bounds(j)
        w = max(hi.x, -lo.x) * 2 * 1.08; h = hi.z * 1.06
        px = 900 / h
        sc = rc.setup_render(round(w * px), 900, a.samples)
        sc.render.film_transparent = True; sc.render.image_settings.color_mode = "RGBA"
        rc.camera((0, -60, hi.z / 2), (0, 0, hi.z / 2), ortho=max(w, h))
        rc.render(os.path.join(out, f"{c}.png"))
