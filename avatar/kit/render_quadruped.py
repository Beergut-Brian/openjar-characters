"""Sheets for the `quadruped` body type (avatar/kit/body_quadruped.py).

    blender -b --factory-startup -P avatar/kit/render_quadruped.py -- \
        --params proposals/cow/jarling.json --outdir proposals/cow/refs/jarling \
        [--only actions,scale,kit] [--samples 32]

- `actions`: `<id>_actions.png`, one 3/4 panel per action (trot, hop, tipped, stiff, graze, sit, idle with
  a pail in the mouth). Captions: `label_sheet.py`.
- `scale`: `.scratch/quad/<id>_scale.png`, the character beside Jeff at Junk Yard Zap's grow/shrink steps
  (1.3 per step, 4 each way): the 3D half of the read check (tools/pixel/cow.py makes the sheet).
- `kit`: `avatar/kit/renders/quadruped_check.png`: Jeff for scale, the cow, and a pig and a sheep built from
  the same body with other pieces and params (avatar/kit/examples/quadruped/*.json, proposal art only).
"""
import sys, os, json, argparse, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import jarling_kit as kit
import render_common as rc
import hold

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--params", default=os.path.join(ROOT, "proposals", "cow", "jarling.json"))
ap.add_argument("--outdir", default=None)
ap.add_argument("--only", default="actions,scale,kit"); ap.add_argument("--samples", type=int, default=32)
a = ap.parse_args(argv)
P = json.load(open(a.params)); pid = P["id"]
OUT = os.path.abspath(a.outdir or os.path.join(os.path.dirname(a.params), "refs", "jarling"))
SCR = os.path.join(ROOT, ".scratch", "quad"); os.makedirs(SCR, exist_ok=True)
only = a.only.split(",")
JEFF = json.load(open(os.path.join(ROOT, "characters", "jeff", "jarling.json")))


def studio(ground="#CFE3C4"):
    kit.reset_scene()
    rc.sky_world("#9FD3F7", "#EAF6FF", 0.75, ground="#EAF6FF")
    rc.sunny_lights(2.8, 2.6)
    if ground:
        rc.ground(ground, size=300)


def freeze(j, action, frame, expr=None):
    kit.pose_at(j, action, frame)
    j.rig.animation_data.action = None          # keep this pose: the scene frame is shared
    if expr:
        kit.set_expression(j, expr)


def scaled(j, k):
    j.rig.scale = (k, k, k)


def label(path, *labels):
    import subprocess
    subprocess.run([sys.executable if sys.executable.endswith("python3") else "python3",
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "label_sheet.py"), path, *labels], check=True)


if "actions" in only:
    panels = [("run", 1, "happy", 38, "trot (run) f1"), ("run", 9, "happy", 38, "trot f9"), ("cheer", 8, "happy", 30, "hop (cheer) f8"),
              ("tipped", 1, "dizzy", -28, "tipped"), ("stiff", 7, "panicked", -150, "stiff (box rolled over)"),
              ("graze", 9, "neutral", 40, "graze"), ("sit", 1, "smug", 40, "sit"), ("idle", 1, "neutral", 30, "idle, pail in mouth")]
    T = 1.1 * P["body"].get("height", 0.95)
    files = []
    for i, (act, fr, ex, yaw, _l) in enumerate(panels):
        studio()
        rc.setup_render(640, 480, a.samples)
        j = kit.build_jarling(P, prefix=f"a{i}_")
        rc.place(j, (0, 0, 0), yaw)
        if act == "stiff":                           # as a game shows it: the physics box has rolled onto its back
            j.rig.rotation_euler = (0, math.radians(180), math.radians(yaw))
            j.rig.location = (0, 0, 2 * j.L["zb"] - 0.02 * T)
        if act == "idle":
            hold.attach_mouth(j, "pail")
        freeze(j, act, fr, ex)
        rc.camera((-1.9 * T, -3.3 * T, 1.35 * T), (0, 0, 0.42 * T), lens=42)
        f = os.path.join(SCR, f"{pid}_panel{i}.png")
        rc.render(f)
        files.append(f)
    import subprocess
    path = os.path.join(OUT, f"{pid}_actions.png")
    code = """
import sys
from PIL import Image, ImageDraw, ImageFont
out, labels, title, files = sys.argv[1], sys.argv[2].split('|'), sys.argv[3], sys.argv[4:]
ims = [Image.open(f).convert('RGB') for f in files]
w, h = ims[0].size; bar = 44; top = 52; cols = 4; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, top + rows * (h + bar)), (255, 255, 255))
d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('DejaVuSans-Bold.ttf', 22)
except OSError: font = ImageFont.load_default()
d.text((20, 14), title, fill=(60, 70, 90), font=font)
for i, (im, t) in enumerate(zip(ims, labels)):
    x, y = (i % cols) * w, top + (i // cols) * (h + bar)
    sheet.paste(im, (x, y))
    d.text((x + (w - d.textlength(t, font=font)) / 2, y + h + 9), t, fill=(60, 70, 90), font=font)
sheet.save(out)
"""
    title = f"{P.get('name', pid)} the Cow ({pid}, proposal): actions" if pid == "cow" else f"{P.get('name', pid)} ({pid}): actions"
    subprocess.run(["python3", "-c", code, path, "|".join(p[-1] for p in panels), title] + files, check=True)
    print("ACTIONS", path)

if "scale" in only:
    studio()
    steps = [-4, -2, 0, 2, 4]
    rc.setup_render(2200, 900, a.samples)
    x = 0.0
    for i, s in enumerate(steps):
        k = 1.3 ** s
        jf = kit.build_jarling(JEFF, prefix=f"sj{i}_")
        j = kit.build_jarling(P, prefix=f"sc{i}_")
        T = 1.1 * P["body"]["height"] * k
        rc.place(jf, (x, 0, 0), -20)
        x += 0.55 + 0.5 * T
        rc.place(j, (x, 0, 0), -60)
        scaled(j, k)
        freeze(jf, "idle", 1); freeze(j, "idle", 1, "neutral" if s <= 0 else "smug")
        x += 1.1 * T + 0.9
    W = x
    rc.camera((W / 2 - 0.9, -60, 9), (W / 2 - 0.9, 0, 1.4), ortho=W * 1.02)
    rc.render(os.path.join(SCR, f"{pid}_scale.png"))

if "kit" in only:
    ex = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples", "quadruped")
    others = [json.load(open(os.path.join(ex, f))) for f in ("pig.json", "sheep.json")]
    studio()
    rc.setup_render(2000, 820, a.samples)
    cast = [(JEFF, "happy", -20, 0.0), (P, "happy", -38, 1.25), (others[0], "happy", -38, 3.0), (others[1], "neutral", -38, 4.55)]
    for i, (pp, e, yaw, x) in enumerate(cast):
        j = kit.build_jarling(pp, prefix=f"k{i}_")
        rc.place(j, (x, 0, 0), yaw)
        freeze(j, "idle", 1, e)
    rc.camera((2.3 - 1.0, -40, 9.0), (2.3, 0, 0.55), ortho=6.2)
    path = os.path.join(ROOT, "avatar", "kit", "renders", "quadruped_check.png")
    rc.render(path)
