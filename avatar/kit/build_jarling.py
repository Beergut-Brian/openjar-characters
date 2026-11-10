"""Build a Jarling from a parameter file and export it as .glb (with idle/run/kick/cheer).

    blender -b --factory-startup -P avatar/kit/build_jarling.py -- \
        --params characters/jeff/jarling.json --out characters/jeff/refs/jarling/jeff.glb [--blend out.blend]

`--seed N` instead of `--params` builds a random generic Jarling.
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
import jarling_kit as kit

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--params"); ap.add_argument("--seed", type=int)
ap.add_argument("--out", required=True); ap.add_argument("--blend")
a = ap.parse_args(argv)

kit.reset_scene()
bpy.context.scene.render.fps = kit.FPS
params = json.load(open(a.params)) if a.params else kit.random_params(a.seed)
j = kit.build_jarling(params)
kit.pose_at(j, "idle", 1)

bpy.ops.object.select_all(action="DESELECT")
for ob in [j.rig] + list(j.rig.children_recursive):   # body, separable parts, hat, slot markers
    ob.select_set(True)
bpy.context.view_layer.objects.active = j.rig
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=a.out, export_format="GLB", use_selection=True, export_apply=True,
    export_animations=True, export_animation_mode="ACTIONS", export_skins=True,
    export_extras=True, export_yup=True, export_force_sampling=True, export_frame_range=False,
    export_reset_pose_bones=True, export_image_format="AUTO", export_lights=bool(getattr(j, "lamp_obs", None)))
if a.blend:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.blend), compress=True)
print("JARLING_OK", a.out)
