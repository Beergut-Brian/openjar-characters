"""Style mock (Jeff + Chuck at the kick line, crowd, sunny park) and the generic lineup.

    blender -b --factory-startup -P avatar/kit/render_scenes.py -- --outdir avatar/kit/renders [--only mock,lineup]
"""
import sys, os, json, argparse, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
import jarling_kit as kit
import render_common as rc
from render_scenes_ball import make_ball

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--outdir", required=True); ap.add_argument("--only", default="mock,lineup")
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--lineup-seeds", default="2,11,20,30,17,4,34,67")
ap.add_argument("--crowd-seeds", default="9,1,52,72")
a = ap.parse_args(argv)
os.makedirs(a.outdir, exist_ok=True)
only = a.only.split(",")
load = lambda c: json.load(open(os.path.join(ROOT, "characters", c, "jarling.json")))

def obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    return o

if "lineup" in only:
    kit.reset_scene()
    rc.sky_world("#8CCBF5", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    rc.ground("#D3E3EC")
    rc.setup_render(1920, 660, a.samples)
    seeds = [int(x) for x in a.lineup_seeds.split(",")]
    for i, sd in enumerate(seeds):
        j = kit.build_jarling(kit.random_params(sd), prefix=f"g{i}_")
        rc.place(j, ((i - (len(seeds) - 1) / 2) * 0.72, 0, 0), 0)
        kit.pose_at(j, "idle", 1 + 6 * i)
        kit.set_expression(j, ["neutral", "happy"][i % 2])
    rc.camera((0, -14, 2.6), (0, 0, 0.62), ortho=6.1)
    rc.render(os.path.join(os.path.abspath(a.outdir), "generic_lineup.png"))

# ------------------------------------------------------------------------------------ style mock
def lawn():
    me = bpy.data.meshes.new("lawn"); s = 120
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    o = bpy.data.objects.new("lawn", me); bpy.context.scene.collection.objects.link(o)
    m = bpy.data.materials.new("lawn"); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes["Principled BSDF"]
    p.inputs["Roughness"].default_value = 0.95; p.inputs["Specular IOR Level"].default_value = 0.1
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 1 / 1.4
    nt.links.new(sep.outputs["X"], mul.inputs[0])
    sn = nt.nodes.new("ShaderNodeMath"); sn.operation = "PINGPONG"; sn.inputs[1].default_value = 1.0
    nt.links.new(mul.outputs[0], sn.inputs[0])
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.5
    nt.links.new(sn.outputs[0], gt.inputs[0])
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs["A"].default_value = (*kit.srgb_to_lin(kit.hex_rgb("#86C45A")), 1)
    mix.inputs["B"].default_value = (*kit.srgb_to_lin(kit.hex_rgb("#79B850")), 1)
    nt.links.new(gt.outputs[0], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], p.inputs["Base Color"])
    me.materials.append(m)

if "mock" in only:
    kit.reset_scene()
    rc.sky_world("#3E98EC", "#BFE6FF", 0.9, ground="#BFE6FF")
    rc.sun("key", (48, 0, -30), 2.7, "#FFF2D9", angle=7)
    rc.sun("rim", (-58, 0, 160), 2.6, "#F4FAFF", angle=4)
    rc.setup_render(1920, 1080, a.samples)
    lawn()
    M = kit.Mats("scn_")
    rng = random.Random(7)
    # kick direction: toward camera-left
    d = Vector((-0.8, -0.75, 0)).normalized()
    yaw = math.degrees(math.atan2(-d.x, d.y)) + 180
    perp = Vector((-d.y, d.x, 0))
    # kick line: a painted strip across the kick direction, just in front of Jeff
    p0 = d * 0.42
    line = bmesh.new()
    for v in [p0 + perp * 6 + d * 0.04, p0 - perp * 6 + d * 0.04, p0 - perp * 6 - d * 0.04, p0 + perp * 6 - d * 0.04]:
        line.verts.new((v.x, v.y, 0.004))
    line.faces.new(line.verts)
    obj("kickline", line, M.flat("chalk", "#FFFFFF", rough=0.9, spec=0.1))
    # Jeff mid follow-through, Chuck watching
    jeff = kit.build_jarling(load("jeff"), prefix="m_")
    rc.place(jeff, (0, 0, 0), yaw)
    kit.pose_at(jeff, "kick", 18); kit.set_expression(jeff, "happy")
    chuck = kit.build_jarling(load("chuck"), prefix="m_")
    rc.place(chuck, (1.25, 0.75, 0), yaw + 35)
    kit.pose_at(chuck, "idle", 25); kit.set_expression(chuck, "surprised")
    # the ball, flying up and away
    ballpos = d * 2.0 + Vector((0, 0, 2.35))   # on its way to space
    ball = make_ball("ball", ballpos, 0.15, M)
    # crowd behind a little rope line, cheering
    seeds = [int(x) for x in a.crowd_seeds.split(",")]
    for i, sd in enumerate(seeds):
        g = kit.build_jarling(kit.random_params(sd), prefix=f"c{i}_")
        x = [-2.55, -1.75, 0.2, 2.15][i % 4] + rng.uniform(-0.08, 0.08)
        y = 3.4 + rng.uniform(-0.25, 0.25)
        rc.place(g, (x, y, 0), rng.uniform(-25, 10))
        kit.pose_at(g, "cheer", [3, 7, 11, 19][i % 4]); kit.set_expression(g, ["happy", "surprised", "happy", "happy"][i % 4])
    post_m = M.flat("post", "#FFFFFF", rough=0.5); rope_m = M.flat("rope", "#FFC83D", rough=0.6)
    pts = []
    for k in range(7):
        x = -3.0 + k * 1.0
        obj(f"post{k}", kit.capsule_bm((x, 2.7, 0.0), (x, 2.7, 0.42), 0.03, 0.035, segs=12, hem=3), post_m)
        pts.append((x, 2.7, 0.40))
    sag = []
    for (x0, y0, z0), (x1, y1, z1) in zip(pts, pts[1:]):
        for t in [i / 8 for i in range(8)]:
            sag.append((x0 + (x1 - x0) * t, y0, z0 - 0.08 * math.sin(math.pi * t)))
    sag.append(pts[-1])
    obj("rope", kit.tube_bm(sag, 0.014), rope_m)
    # bunting between two poles behind the crowd
    pole_m = M.flat("pole", "#F4F4F0", rough=0.5)
    for x in (-3.4, 3.4):
        obj(f"pole{x}", kit.capsule_bm((x, 4.6, 0), (x, 4.6, 2.3), 0.035, 0.035, segs=12, hem=3), pole_m)
    flag_cols = ["#3E7BEA", "#FFD23F", "#FFFFFF", "#FF9A2E", "#9B5DE5", "#5CC6F2"]
    n = 18
    string = []
    for k in range(n + 1):
        t = k / n; x = -3.4 + 6.8 * t
        string.append((x, 4.6, 2.2 - 0.45 * math.sin(math.pi * t)))
    obj("bunting_string", kit.tube_bm(string, 0.008), pole_m)
    for k in range(n):
        (x0, y0, z0), (x1, y1, z1) = string[k], string[k + 1]
        fb = bmesh.new()
        v = [fb.verts.new((x0 + 0.02, y0, z0)), fb.verts.new((x1 - 0.02, y1, z1)),
             fb.verts.new(((x0 + x1) / 2, y0 + 0.01, (z0 + z1) / 2 - 0.26))]
        fb.faces.new(v)
        sol = kit.solidify_bm(fb, 0.01)
        obj(f"flag{k}", sol, M.flat(f"flag{k % len(flag_cols)}", flag_cols[k % len(flag_cols)], rough=0.7))
    # trees, hills, clouds
    trunk_m = M.flat("trunk", "#9A6A44", rough=0.8)
    leaf_ms = [M.flat("leaf1", "#3E9E72", rough=0.85), M.flat("leaf2", "#5DAE7E", rough=0.85), M.flat("leaf3", "#7DB85A", rough=0.85)]
    for k, (x, y, sc) in enumerate([(-7.5, 10, 1.3), (-4.8, 13, 1.0), (-10.5, 15, 1.5), (6.5, 11, 1.2), (9.5, 14.5, 1.6),
                                     (3.8, 16, 1.0), (-1.5, 19, 1.1), (13, 18, 1.4), (-14, 12, 1.2)]):
        obj(f"trunk{k}", kit.capsule_bm((x, y, 0), (x, y, 1.6 * sc), 0.12 * sc, 0.1 * sc, segs=12, hem=3), trunk_m)
        for j in range(3):
            c = Vector((x + rng.uniform(-0.5, 0.5) * sc, y + rng.uniform(-0.3, 0.3), (1.9 + j * 0.45 + rng.uniform(0, 0.3)) * sc))
            r = (0.95 - j * 0.18) * sc
            obj(f"leaf{k}_{j}", kit.ellipsoid_bm(c, (r, r, r * 0.92), segs=24, rings=14), leaf_ms[(k + j) % 3])
    hill_m = [M.flat("hill1", "#A6D877", rough=0.95), M.flat("hill2", "#B5E08A", rough=0.95)]
    for k, (x, y, rx, rz) in enumerate([(-30, 55, 32, 7), (12, 65, 38, 9), (45, 50, 26, 6), (-55, 40, 25, 5)]):
        obj(f"hill{k}", kit.ellipsoid_bm((x, y, -1.0), (rx, 14, rz), segs=40, rings=20), hill_m[k % 2])
    cloud_m = bpy.data.materials.new("cloud"); cloud_m.use_nodes = True
    cp = cloud_m.node_tree.nodes["Principled BSDF"]
    cp.inputs["Base Color"].default_value = (1, 1, 1, 1); cp.inputs["Roughness"].default_value = 1.0
    cp.inputs["Emission Color"].default_value = (0.85, 0.92, 1.0, 1); cp.inputs["Emission Strength"].default_value = 0.45
    for k, (x, y, z, sc) in enumerate([(-20, 60, 13, 3.4), (6, 70, 15.5, 4), (28, 62, 11.5, 3), (-44, 75, 16, 4.2)]):
        for j in range(5):
            c = (x + (j - 2) * 1.1 * sc + rng.uniform(-0.3, 0.3) * sc, y, z + rng.uniform(-0.2, 0.5) * sc - abs(j - 2) * 0.35 * sc)
            r = sc * (1.1 - abs(j - 2) * 0.22)
            obj(f"cloud{k}_{j}", kit.ellipsoid_bm(c, (r, r * 0.8, r * 0.75), segs=20, rings=12), cloud_m)
    rc.camera((1.5, -5.6, 1.6), (0.0, 0.9, 1.05), lens=34)
    rc.render(os.path.join(os.path.abspath(a.outdir), "style_mock.png"))
