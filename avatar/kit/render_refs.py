"""Reference renders for one Jarling: turnaround, four expressions, kick pose.

    blender -b --factory-startup -P avatar/kit/render_refs.py -- \
        --params characters/jeff/jarling.json --outdir characters/jeff/refs/jarling [--only turnaround,expressions,kick]
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
ap.add_argument("--only", default="turnaround,expressions,kick"); ap.add_argument("--samples", type=int, default=48)
a = ap.parse_args(argv)
P = json.load(open(a.params)); pid = P["id"]
os.makedirs(a.outdir, exist_ok=True)
only = a.only.split(",")

def studio(ground="#D3E3EC"):
    kit.reset_scene()
    rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    rc.ground(ground)


if "turnaround" in only:
    studio()
    rc.setup_render(1600, 800, a.samples)
    for i, yaw in enumerate((0, -40, -90, 180)):     # front, 3/4, side, back
        j = kit.build_jarling(P, prefix=f"t{i}_")
        rc.place(j, ((i - 1.5) * 0.95, 0, 0), yaw)
        kit.pose_at(j, "idle", 1)
    rc.camera((0, -12, 0.62), (0, 0, 0.62), ortho=3.9)
    rc.render(os.path.join(os.path.abspath(a.outdir), f"{pid}_turnaround.png"))

if "expressions" in only:
    studio()
    rc.setup_render(1600, 520, a.samples)
    for i, ex in enumerate(kit.EXPRESSIONS):
        j = kit.build_jarling(P, prefix=f"e{i}_")
        rc.place(j, ((i - 1.5) * 0.72, 0, 0), 0)
        kit.pose_at(j, "idle", 1)
        kit.set_expression(j, ex)
    hz = j.L["head_c"].z
    rc.camera((0, -12, hz + 2.4), (0, 0, hz - 0.02), ortho=2.9)
    rc.render(os.path.join(os.path.abspath(a.outdir), f"{pid}_expressions.png"))

if "kick" in only:
    studio("#C9DCE8")
    rc.setup_render(1280, 720, a.samples)
    j = kit.build_jarling(P, prefix="k_")
    kit.pose_at(j, "kick", 17)
    kit.set_expression(j, P.get("ref_kick_expression", "happy"))
    import render_scenes_ball as rb
    rb.make_ball("ball", Vector((-0.35, -0.95, 0.62)), 0.11, kit.Mats("refs_"))
    rc.place(j, (0, 0, 0), -28)
    rc.camera((-4.4, -1.6, 1.5), (0, -0.35, 0.55), lens=45)
    rc.render(os.path.join(os.path.abspath(a.outdir), f"{pid}_kick.png"))
