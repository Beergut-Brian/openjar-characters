"""Kit v2 checks that need Blender (run by godot/run_tests.sh):

    blender -b --factory-startup -P avatar/kit/check_kit_v2.py

Prints "  ok   ..." / "  FAIL ..." lines and "KIT_V2_CHECK PASS|FAIL". Checks the body.width /
body.belly limits, that the skeleton does not move with width or belly, that the equipment slots
follow the surface (fit scales grow with the body), head features as parts on their own bones,
skin-derived face colours, hair pieces, and that every registered piece name is documented.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import jarling_kit as kit

fails = 0
def check(ok, what):
    global fails
    fails += 0 if ok else 1
    print(("  ok   " if ok else "  FAIL ") + what)

def build(body=None, **over):
    kit.reset_scene()
    P = {"id": "chk", "body": body or {}}
    P.update(over)
    return kit.build_jarling(P)

def raises(body):
    try:
        build(body)
    except ValueError as e:
        return str(e)
    return None

print("[kit v2] width / belly limits")
check(kit.WIDTH_RANGE == (0.75, 1.5) and kit.BELLY_RANGE == (0.0, 1.0), "limits are width 0.75..1.5, belly 0..1")
for bad in ({"width": 0.74}, {"width": 1.51}, {"width": 3}, {"belly": -0.1}, {"belly": 1.01}):
    check(raises(bad) is not None, f"body {bad} is refused ({raises(bad)})")
for good in ({"width": 0.75}, {"width": 1.5, "belly": 1.0}, {"belly": 0.0}, {"build": "round", "width": 1.5, "belly": 1.0, "height": 1.3},
             {"build": "slim", "width": 0.75, "height": 0.8, "leg_scale": 0.8}):
    check(raises(good) is None, f"body {good} builds")

print("[kit v2] same skeleton, slots follow the surface")
def bones(j):
    return {b.name: (tuple(round(x, 5) for x in b.head_local), tuple(round(x, 5) for x in b.tail_local)) for b in j.rig.data.bones}
def slot(j, name):
    return tuple(j.slots[name].matrix_basis.to_scale())
def hand_clear(j):
    L = j.L
    return all(abs(j.hand_c[s].x) - 0.036 * L["limb"] > abs(j.torso_point((j.hand_c[s].z - L["torso_z0"]) / (L["torso_z1"] - L["torso_z0"]), 0.0).x) - 0.012 for s in ("L", "R"))
def snap(body):     # read everything before the next build clears the scene
    j = build(body)
    return bones(j), {s: slot(j, s) for s in kit.SLOTS}, list(j.rig["jarling_actions"]), hand_clear(j)
core = ["root", "spine", "head"]
ref_bones, ref_slots, ref_acts, _ = snap({"build": "regular"})
fat_bones, fat_slots, fat_acts, fat_clear = snap({"build": "regular", "width": 1.5, "belly": 1.0})
thin_bones, thin_slots, _a, _c = snap({"build": "regular", "width": 0.75})
check(set(ref_bones) == set(fat_bones) == set(thin_bones), "same bone names at width 0.75 / 1.0 / 1.5")
check(all(ref_bones[b] == fat_bones[b] == thin_bones[b] for b in core), "root, spine and head bones do not move with width or belly")
check(all(abs(ref_bones[b][0][2] - fat_bones[b][0][2]) < 1e-5 and abs(ref_bones[b][0][2] - thin_bones[b][0][2]) < 1e-5 for b in ref_bones),
      "every bone keeps its height (limb bones only shift sideways with the body)")
check(all(abs(v - 1.0) < 0.02 for s in kit.SLOTS for v in ref_slots[s]), "reference Jarling has slot scale 1.0 everywhere")
for s in ("waist", "back", "knee_l", "knee_r", "foot_l", "hand_r"):
    check(thin_slots[s][0] < ref_slots[s][0] < fat_slots[s][0],
          f"slot_{s} fit scale grows with the body ({thin_slots[s][0]:.2f} < {ref_slots[s][0]:.2f} < {fat_slots[s][0]:.2f})")
check(fat_slots["waist"][1] > fat_slots["waist"][0] * 0.9, f"waist slot depth follows the belly ({fat_slots['waist'][1]:.2f})")
check(abs(fat_slots["head"][0] - 1.0) < 0.02 and abs(thin_slots["face"][0] - 1.0) < 0.02, "head and face slots do not change with width")
check(set(kit.action_keys({})) == {"idle", "run", "kick", "cheer"} and fat_acts == ref_acts, "same actions on the widest body")
check(fat_clear, "hands hang clear of the widest belly")

print("[kit v2] head features")
j = build(head={"ears": "none", "features": [{"type": "antennae", "count": 2}, {"type": "horns"}, {"type": "pointy_ears"}, {"type": "fins"}]}, skin="#9FD6F0")
for t in ("antennae", "horns", "pointy_ears", "fins"):
    ob = j.part_obs.get(f"feature_{t}")
    check(ob is not None and ob.name == f"chk_part_feature_{t}" and ob.get("jarling_part") == f"feature_{t}", f"feature {t} is the part chk_part_feature_{t}")
names = [b.name for b in j.rig.data.bones]
check(all(n in names for n in ("feat_antenna.1", "feat_antenna.2", "feat_horn.1", "feat_ear.L", "feat_fin.1")), "features have their own bones")
check(all(j.rig.data.bones[n].parent.name == "head" for n in names if n.startswith("feat_")), "feature bones are children of head")
idle = bpy.data.actions["idle"]
def keyed(act, bone):
    try:
        fcs = [fc for layer in act.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]
    except AttributeError:
        fcs = list(act.fcurves)
    spans = [max(k.co[1] for k in fc.keyframe_points) - min(k.co[1] for k in fc.keyframe_points)
             for fc in fcs if f'"{bone}"' in fc.data_path and "rotation" in fc.data_path and len(fc.keyframe_points)]
    return bool(spans) and max(spans) > 1e-4
check(keyed(idle, "feat_antenna.1") and keyed(idle, "feat_antenna.2"), "antennae bob in idle (secondary motion keyed)")
check(not keyed(idle, "feat_horn.1"), "horns stay rigid")
check(list(j.rig.get("jarling_features", [])) == ["antennae", "fins", "horns", "pointy_ears"], "rig lists jarling_features")
j2 = build(head={"features": [{"type": "antennae"}]}, headwear={"type": "cap", "color": "#1E2B4D"})
check("feature_antennae" in j2.part_obs and "headwear" in j2.part_obs, "a feature and a hat coexist as separate parts")
try:
    build(head={"features": [{"type": "tentacle_beard"}]}); check(False, "unknown feature is refused")
except ValueError:
    check(True, "unknown feature is refused")

print("[kit v2] skin-derived face colours")
for skin, human in (("#F0BE94", True), ("#5C3720", True), ("#9FD6F0", False), ("#B79BE8", False), ("#D4F25A", False), ("#A9B0B8", False)):
    check(kit.is_fantasy_skin(skin) != human, f"{skin} is {'human' if human else 'fantasy'}")
f0 = dict(kit.DEFAULTS["face"], _brow_auto=True)
for skin in ("#9FD6F0", "#B79BE8", "#D4F25A", "#A9B0B8", "#3A2A7A"):
    c = kit.face_colours(f0, skin)
    check(c["blush"] != "#FF7F86" and min(kit.delta_e2000(c["blush"], skin), kit.delta_e2000(c["line"], skin), kit.delta_e2000(c["brow"], skin)) > 8,
          f"{skin}: blush {c['blush']}, line {c['line']}, brow {c['brow']} are derived and stand off the skin")
c = kit.face_colours(dict(f0, _brow_auto=False), "#F0BE94")
check(c["blush"] == "#FF7F86" and c["brow"] == f0["brow_color"], "human skins keep the original blush and brows (Jeff and Chuck unchanged)")
check(kit.face_colours(dict(f0, blush_color="#123456"), "#9FD6F0")["blush"] == "#123456", "an explicit blush_color wins")

print("[kit v2] hair pieces and presets")
n0 = len(build(hair={"style": "sleek"}).body.data.vertices)
n1 = len(build(hair={"style": "puffs"}).body.data.vertices)
n2 = len(build(hair={"style": "sleek", "pieces": [{"type": "bun", "at": [70, 180]}, {"type": "spike", "at": [80, 0], "dir": "up"}]}).body.data.vertices)
check(n1 > n0 and n2 > n0, f"preset 'puffs' and hair.pieces add geometry ({n0} -> {n1}, {n2})")
n3 = len(build(hair={"style": "puffs"}, headwear={"type": "cap", "color": "#1E2B4D"}).body.data.vertices)
n4 = len(build(hair={"style": "puffs"}, headwear={"type": "cap", "color": "#1E2B4D", "hair": "free"}).body.data.vertices)
check(n4 > n3, "a hat tucks the pieces away unless headwear.hair is 'free'")
for name in ("puffs", "top_bun", "upright", "pigtails", "mohawk", "tuft_top"):
    check(name in kit.HAIR_PRESETS, f"hair preset {name}")

print("[kit v2] every registered piece is documented")
doc = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "kit-v2.md")).read() if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "kit-v2.md")) else ""
for reg, label in ((kit.HEADWEAR, "headwear"), (kit.COSTUME, "costume"), (kit.SHOES, "shoes"), (kit.PATTERNS, "pattern"), (kit.FEATURES, "feature"),
                   (kit.HAIR_PIECES, "hair piece"), (kit.FACE_EXTRAS, "face extra"), (kit.MOUTH_DRAW, "mouth")):
    missing = [n for n in reg if f"`{n}`" not in doc]
    check(not missing, f"{label}: {len(reg)} registered, all in docs/kit-v2.md {missing}")

print("KIT_V2_CHECK " + ("PASS" if fails == 0 else "FAIL"))
sys.exit(0 if fails == 0 else 1)
