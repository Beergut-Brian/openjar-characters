"""Kit v2 sheets: the fat/skinny range lineup and gear-fit proofs.

    blender -b --factory-startup -P avatar/kit/render_range.py -- --out avatar/kit/renders/kit_v2_range.png [--samples 48]
    blender -b --factory-startup -P avatar/kit/render_range.py -- --lineup a.json,b.json --out .scratch/x.png   (x_front.png, x_back.png)
    blender -b --factory-startup -P avatar/kit/render_range.py -- --proof a.json,b.json --out .scratch/proof.png \
        [--gear sneakers,kneepads,cape,hat,sunglasses,gloves,belt] [--action kick --frame 17]

Range: skinniest, regular, round, widest at heights 0.8 / 1.0 / 1.3 (twelve Jarlings on one skeleton),
with human and fantasy skins. Proof: each params file twice (idle, and the action pose) wearing the
starter gear, built straight from avatar/gear/build_gear.py and parented to the slot markers exactly
as jarling_equipment.gd does in Godot (slot scale = fit).
"""
import sys, os, json, argparse, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "gear"))
import bpy
from mathutils import Matrix
import jarling_kit as kit
import render_common as rc

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True); ap.add_argument("--samples", type=int, default=48)
ap.add_argument("--proof", default=""); ap.add_argument("--gear", default="sneakers,kneepads,cape,hat,sunglasses,gloves,belt")
ap.add_argument("--lineup", default="")    # params files: each once, front and 3/4 back views, no gear
ap.add_argument("--action", default="kick"); ap.add_argument("--frame", type=int, default=17)
a = ap.parse_args(argv)

WIDTHS = [("skinniest", {"build": "slim", "width": 0.75}), ("regular", {"build": "regular"}),
          ("round", {"build": "round", "width": 1.15, "belly": 0.5}), ("widest", {"build": "round", "width": 1.5, "belly": 1.0})]
HEIGHTS = [0.8, 1.0, 1.3]
SKINS = ["#F0BE94", "#9FD6F0", "#8A5A3C", "#B79BE8", "#D4F25A", "#F7CFAE", "#A9B0B8", "#D99E6E", "#7FD9C4", "#5C3720", "#F2C29B", "#7C8FE0"]
TOPS = ["#3E7BEA", "#FFD23F", "#FF9A2E", "#F4F4F0", "#9B5DE5", "#1FB5A8", "#FF7AB6", "#5CC6F2", "#2C3E7A", "#FFD23F", "#7E57C2", "#F4F4F0"]

def studio():
    kit.reset_scene()
    rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    rc.ground("#D3E3EC", size=200)

def wear(j, gear_ids):
    """Put starter gear on a built Jarling the way jarling_equipment.gd does."""
    import build_gear as bg
    bg.M.cache.clear()
    for gid in gear_ids:
        spec = bg.ITEMS[gid]
        root = spec["fn"]()
        for s in spec["slots"]:
            piece = next((c for c in root.children if c.name.split(".")[0] == s), None) if len(spec["slots"]) > 1 else root
            piece.parent = j.slots[s]
            piece.matrix_parent_inverse = Matrix.Identity(4)
            piece.matrix_basis = Matrix.Identity(4)
        for tag in spec.get("replaces_body_part", []):
            ob = j.part_obs.get(tag)
            if ob:
                ob.hide_render = True
            if tag == "headwear" and j.hat:
                j.hat.hide_render = True

if a.lineup:
    files = a.lineup.split(",")
    studio()
    n = len(files)
    rc.setup_render(min(520 * n, 3640), 1100, a.samples)
    for row, (yaw, y) in enumerate(((-18, 0.0), (155, 0.0))):
        for i, f in enumerate(files):
            j = kit.build_jarling(json.load(open(f)), prefix=f"l{row}{i}_")
            rc.place(j, ((i - (n - 1) / 2) * 1.05, 0, 0), yaw)
            kit.pose_at(j, "idle", 1)
        sc = bpy.context.scene
        sc.render.resolution_y = int(sc.render.resolution_x * 1.75 / (1.05 * n))    # 1.75 m tall view
        rc.camera((0, -14, 1.75), (0, 0, 0.80), ortho=1.05 * n)
        rc.render(os.path.abspath(a.out).replace(".png", f"_{'front' if row == 0 else 'back'}.png"))
        for ob in list(bpy.data.objects):
            if ob.name.startswith("l0"):
                bpy.data.objects.remove(ob, do_unlink=True)
elif a.proof:
    files = a.proof.split(",")
    gear = [g for g in a.gear.split(",") if g]
    studio()
    rc.setup_render(640 * 2 * len(files), 760, a.samples)
    n = 2 * len(files)
    for i, f in enumerate(files):
        P = json.load(open(f))
        for k, (act, fr, yaw) in enumerate((("idle", 1, -20), (a.action, a.frame, -35))):
            j = kit.build_jarling(P, prefix=f"p{i}{k}_")
            rc.place(j, ((i * 2 + k - (n - 1) / 2) * 1.35, 0, 0), yaw)
            wear(j, gear)
            kit.pose_at(j, act, fr)
    ortho = 1.35 * n * 1.02
    rc.camera((0, -14, 1.9), (0, 0, 0.72), ortho=ortho)
    rc.render(os.path.abspath(a.out))
else:
    studio()
    n = len(WIDTHS) * len(HEIGHTS)
    rc.setup_render(2640, 560, a.samples)
    step = 0.80; gap = 0.35
    x = -((n - 1) * step + (len(HEIGHTS) - 1) * gap) / 2
    i = 0
    for hi, h in enumerate(HEIGHTS):
        for wi, (label, body) in enumerate(WIDTHS):
            P = {"id": f"range{i}", "skin": SKINS[i], "body": dict(body, height=h),
                 "head": {"shape": "round", "ears": "round"},
                 "face": {"eyes": ["drop", "round", "wide", "button"][wi], "mouth": ["smile", "grin", "grin_top", "smile"][hi % 4], "nose": "button"},
                 "hair": {"style": ["short", "puffs", "buzz", "top_bun", "upright", "bob", "none", "curly", "mohawk", "afro", "pigtails", "tuft_top"][i],
                          "color": ["#4A2F23", "#2A2026", "#2A2026", "#F2F0EA", "#3B2A6B", "#A34E25", "#2A2026", "#7A4B2A", "#1E6E66", "#2A2026", "#E3B85E", "#27306B"][i]},
                 "outfit": {"top": {"style": "tee", "color": TOPS[i]},
                            "bottoms": {"style": ["pants", "shorts"][i % 2], "color": ["#3B5BA5", "#8A8F99", "#5B4636", "#2C3E7A"][wi]},
                            "shoes": {"style": "sneaker", "color": "#F4F4F0"}}}
            if i in (1, 6):
                P["head"]["features"] = [{"type": "antennae"}] if i == 1 else [{"type": "horns", "style": "nub"}]
                P["head"]["ears"] = "none"
            if i == 4:
                P["head"]["features"] = [{"type": "pointy_ears"}]
            if i == 8:
                P["head"]["features"] = [{"type": "fins", "count": 3}]; P["head"]["ears"] = "none"
            if i == 11:
                P["head"]["features"] = [{"type": "horns", "style": "curved"}]
            j = kit.build_jarling(P, prefix=f"r{i}_")
            rc.place(j, (x, 0, 0), 0)
            kit.pose_at(j, "idle", 1)
            x += step + (gap if wi == len(WIDTHS) - 1 else 0)
            i += 1
    total = (n - 1) * step + (len(HEIGHTS) - 1) * gap + 1.2
    view_h = total * 560 / 2640
    rc.camera((0, -16, view_h / 2 + 0.75), (0, 0, view_h / 2 - 0.16), ortho=total)
    rc.render(os.path.abspath(a.out))
