"""The hold sheet and the hold check: every body type holding things.

    blender -b --factory-startup -P avatar/kit/render_hold.py -- [--only jeff_lantern,...] [--samples 32] [--check]
    python3 avatar/kit/hold_sheet.py            # lays the cells out -> avatar/kit/renders/hold_check.png

Each cell is one character in one action frame with one held item (a gear item from avatar/gear, or
the character's own kit piece), rendered front and 3/4 into .scratch/hold/<cell>_<view>.png.
`--check` renders nothing: it poses every cell (and more frames of idle / run / cheer) and measures
how far each fist is from its grip; prints `HOLD_CHECK PASS` when all are within 3 mm.
"""
import sys, os, json, argparse, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import jarling_kit as kit
import render_common as rc
import hold

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# cell id: (character, gear item or None for the character's own pieces, action, frame, expression, caption)
CELLS = {
    "jeff_lantern": ("jeff", "lantern", "idle", 1, None, "Jeff: lantern (one_hand_low)"),
    "jeff_shovel": ("jeff", "shovel", "idle", 1, None, "Jeff: shovel (two_hand_diagonal)"),
    "chuck_pennant": ("chuck", "pennant", "idle", 1, None, "Chuck: pennant (one_hand_raised)"),
    "chuck_crate": ("chuck", "crate", "idle", 1, None, "Chuck: crate (two_hand_front)"),
    "chuck_parcel": ("chuck", "parcel", "run", 5, None, "Chuck: parcel, running (chest_clutch)"),
    "jeff_pennant_cheer": ("jeff", "pennant", "cheer", 7, "happy", "Jeff: pennant, cheering"),
    "mole_idle": ("mole", None, "idle", 1, None, "Mole: idle, claws out, no shovel"),
    "mole_dig": ("mole", "shovel", "dig", 9, None, "Mole: digging, shovel in both claws"),
    "gnome_clipboard": ("gnome_foreman", None, "idle", 1, None, "Gnome Foreman: clipboard (kit piece, one_hand_low)"),
    "gnome_whistle": ("gnome_foreman", None, "whistle", None, "whistle", "Gnome Foreman: whistle raised"),
    "caveman_club": ("caveman", None, "idle", 1, None, "Caveman: cloth club (kit piece, one_hand_raised)"),
    "dragon_lantern": ("dragon", "lantern", "idle", 1, None, "Dragon: lantern (one_hand_low)"),
}
EXTRA_CHECKS = [("jeff", "lantern", "run", 5), ("jeff", "shovel", "run", 1), ("jeff", "shovel", "cheer", 7), ("jeff", "crate", "run", 9),
                ("jeff", "parcel", "idle", 25), ("chuck", "shovel", "idle", 13), ("chuck", "pennant", "run", 1),
                ("mole", "shovel", "idle", 1), ("mole", "lantern", "run", 5), ("mole", "crate", "idle", 1), ("mole", "parcel", "idle", 1),
                ("mole", "pennant", "cheer", 8), ("mole", "shovel", "dig", 1), ("mole", "shovel", "dig", 17),
                ("gnome_foreman", "shovel", "idle", 1), ("caveman", "crate", "idle", 1), ("caveman", "shovel", "run", 5),
                ("dragon", "shovel", "idle", 1), ("dragon", "crate", "idle", 1), ("dragon", "parcel", "cheer", 1), ("dragon", "pennant", "idle", 1)]

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--only", default=""); ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--adhoc", default="", help="extra cells char:gear:action:frame,... (for tuning; not on the sheet)")
ap.add_argument("--check", action="store_true"); ap.add_argument("--px", type=int, default=520)
a = ap.parse_args(argv)
OUT = os.path.join(ROOT, ".scratch", "hold"); os.makedirs(OUT, exist_ok=True)
load = lambda c: json.load(open(os.path.join(ROOT, "characters", c, "jarling.json")))

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

def pose(char, gear, action, frame, expr=None):
    """Build `char`, give it `gear`, pose it. Returns (jarling, {(item, hand): metres})."""
    P = load(char)
    j = kit.build_jarling(P)
    if frame is None:      # the character's own posed expression (the Gnome's whistle)
        ep = (P.get("expression_poses") or {}).get(expr) or {}
        action, frame = ep.get("action", action), ep.get("frame", 1)
    holds = [h for h in [hold.attach_gear(j, gear)] if h] if gear else []
    kit.pose_at(j, action, frame)
    if expr:
        kit.set_expression(j, expr)
    d = hold.apply(j, holds, action) if holds else {}
    for h in getattr(j, "held", []):       # the character's own pieces: fist centre to the piece's grip, in the rest pose
        d[(h["piece"], "main")] = (Vector(h["grip"]) - Vector(j.hand_c[h["side"]])).length
    return j, d

worst = 0.0; lines = []
def note(tag, d):
    global worst
    for (item, hand), v in sorted(d.items()):
        worst = max(worst, v)
        lines.append(f"  {'ok  ' if v <= 0.003 else 'FAIL'} {tag}: {item} {hand} hand {v * 1000:.2f} mm from its grip")

if a.check:
    for cid, (char, gear, action, frame, expr, _cap) in CELLS.items():
        kit.reset_scene()
        j, d = pose(char, gear, action, frame, expr)
        note(f"{cid} ({action} f{frame})", d)
    for char, gear, action, frame in EXTRA_CHECKS:
        kit.reset_scene()
        j, d = pose(char, gear, action, frame)
        note(f"{char} + {gear} ({action} f{frame})", d)
    print("[hold] fist-to-grip distances")
    print("\n".join(lines))
    bad = [l for l in lines if "FAIL" in l]
    print(f"HOLD_CHECK {'PASS' if not bad and lines else 'FAIL'} ({len(lines)} grips, worst {worst * 1000:.2f} mm)")
    sys.exit(0)

for spec in [x for x in a.adhoc.split(",") if x]:
    c, g, ac, fr = spec.split(":")
    CELLS[f"adhoc_{c}_{g}_{ac}{fr}"] = (c, g or None, ac, int(fr), None, spec)
only = [x for x in a.only.split(",") if x] or [k for k in CELLS if not a.adhoc or k.startswith("adhoc_")]
for cid in only:
    char, gear, action, frame, expr, cap = CELLS[cid]
    kit.reset_scene()
    rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    rc.ground("#D3E3EC", size=400)
    j, d = pose(char, gear, action, frame, expr)
    note(cid, d)
    for view, yaw in (("front", 0), ("34", -35)):
        rc.place(j, (0, 0, 0), yaw)
        lo, hi = bounds(j)
        cx, w = (lo.x + hi.x) / 2, (hi.x - lo.x)
        h = hi.z
        size = max(w * 1.12, h * 1.12)
        rc.setup_render(a.px, a.px, a.samples)
        for ob in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(ob)
        rc.camera((cx, -80, h / 2 - 0.02 * size), (cx, 0, h / 2 - 0.02 * size), ortho=size)
        rc.render(os.path.join(OUT, f"{cid}_{view}.png"))
print("\n".join(lines))
