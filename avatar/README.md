# Jarlings: the Open Jar avatar kit

*Working name, logged by Gary on 2026-11-09. Kaden can rename it.*

A **Jarling** is Open Jar's own simple, friendly 3D avatar, built for Spaceballs (a sunny, sporty
"party game on the lawn" look) and reusable by any 3D game. Kaden's brief was to make our own take on
the friendly-avatar style of the classic living-room sports games. Everything here is an original
design built from code. It copies no proportions, face-part shapes or assets from any existing
avatar system.

![style mock](kit/renders/style_mock.png)

## What a Jarling looks like (the style rules)

- **Big round head** (head diameter is about 42% of total height), small capsule body, short
  capsule limbs, **mitten hands**, **chunky rounded shoes**. Readable from 10 feet.
- **Smooth, soft shading.** Every part is smooth-shaded. Nothing is flat-faceted, and nothing is outlined.
- **Face drawn on the head** from simple 2D parts: eyes, brows, nose, mouth, blush, freckles. The
  features sit low on the head (big forehead) and the eyes are big, with two catch-lights, so faces
  stay friendly from couch distance.
- **Saturated flat colours**, one colour per material. Fixed character colours are exact in the
  materials.
- **A bright, sunny world.** Warm key sun, cool rim light from behind for pop (the house style allows
  rim light instead of outlines), soft shadows, gradient blue sky.
- **Squash-and-stretch friendly.** Body parts are rigid pieces with ball joints, so bone *scale*
  (squash and stretch) never tears the mesh.

## Files

```
avatar/kit/jarling_kit.py      the kit: face-part library, geometry, rig, actions, random generics
avatar/kit/build_jarling.py    params JSON -> .glb (CLI)
avatar/kit/render_refs.py      turnaround / expressions / kick renders for one Jarling (Cycles CPU)
avatar/kit/render_scenes.py    style_mock.png and generic_lineup.png
avatar/kit/render_common.py    shared lights / sky / camera
avatar/kit/render_scenes_ball.py  the six-panel ball used in renders
avatar/kit/label_sheet.py      Pillow: caption bar under the sheets
avatar/kit/make_all.sh         rebuilds every deliverable (about 7 minutes on 6 CPU cores)
avatar/kit/renders/            style_mock.png, generic_lineup.png
characters/<name>/jarling.json the character's parameters
characters/<name>/refs/jarling/<name>.glb + turnaround / expressions / kick PNGs
```

## Build one

```sh
# a named character
blender -b --factory-startup -P avatar/kit/build_jarling.py -- \
    --params characters/jeff/jarling.json --out characters/jeff/refs/jarling/jeff.glb
# a random generic Jarling (deterministic per seed)
blender -b --factory-startup -P avatar/kit/build_jarling.py -- --seed 42 --out /tmp/generic42.glb
# everything (glbs, sheets, mock, lineup)
./avatar/kit/make_all.sh            # REF_SAMPLES=64 MOCK_SAMPLES=128 by default
```

Tested with Blender 5.2.3 in background mode. Renders use Cycles on the CPU, because EEVEE needs a GPU.

## Parameter format (`jarling.json`)

Every key is optional: missing keys fall back to `DEFAULTS` in `jarling_kit.py`. Colours are sRGB hex.

```jsonc
{
  "id": "chuck", "name": "Chuck",
  "head": {"shape": "round|wide|tall|soft_square|pear|egg", "size": 1.0, "ears": "round|none"},
  "skin": "#E0A97C",
  "face": {
    "eyes":  "drop|round|button|wide|almond|lash",
    "brows": "thin|soft|arched|thick|bushy|none",
    "nose":  "button|dot|curve|bump|none",          // bump = small 3D nose
    "mouth": "smile|grin|grin_two|grin_top|o|smirk|set|grit|flat",
    "eye_color": "#2A1E2C", "brow_color": "#3A2418",
    "lid": 0.34,        // 0 open .. 0.6 heavy upper lid (half-lidded / squint)
    "lid_low": 0.0,     // cheek push from below (happy squint)
    "lid_tilt": 0.12,   // + inner corner lower (determined), - outer lower (sleepy)
    "brow_tilt": 0.22, "brow_raise": 0.0, "blush": 0.2, "freckles": false,
    "eye_spacing": 0.34, "scale": 1.3,               // scale = size of the whole face
    "expressions": {"determined": {"lid": 0.45, "mouth": "grit"}}   // per-expression overrides
  },
  "hair": {"style": "short|swoop|bob|bun|ponytail|long|spiky|curly|afro|buzz|none", "color": "#5A3A26"},
  "headwear": {"type": "none|cap|trucker|beanie|headband|chicken_hood", "color": "...",
               "separate": true},                     // separate=true exports it as its own object
  "body": {"build": "slim|regular|stocky|round|boxy|puffy", "height": 1.0, "leg_scale": 1.0},
  "outfit": {
    "top": {"style": "tee|long|stripe|tiedye|costume", "color": "...", "accent": "..."},
    "bottoms": {"style": "pants|flared|shorts|skirt", "color": "..."},
    "shoes": {"style": "sneaker|boots|barefoot", "color": "...", "sole": "...", "stitch": "..."}
  },
  "costume": [{"piece": "wing_tips|tail_feathers|jeans_stitch", "color": "..."}],
  "posture": {"spine_lean": -5, "head_lean": -6, "arm_out": 6},   // degrees, added to every action
  "ref_kick_expression": "determined"                               // used by render_refs.py only
}
```

Character-specific headwear options: `chicken_hood` takes `comb`, `beak`, `headband`, `opening_deg`
and `beak_deg`. `trucker` takes `brim`, `piping`, `patch`, `tilt_deg` and `lift`.

Generic Jarlings come from `random_params(seed)`. Their outfits use a palette that **excludes the
player green and red**, so a crowd never reads as P1 or P2. The lineup uses seeds
`2,11,20,30,17,4,34,67` and the mock crowd uses `9,1,52,72`. These were picked to show range. They
were not tuned per character.

## What is in the .glb

| Thing | Detail |
| --- | --- |
| Units / axes | metres, Y up, faces **+Z** (Godot's model front), feet at y=0, about 1.1 m tall |
| Skeleton | `root` > `spine` > `head` (> `comb` on Jeff), `arm.L/R` > `hand.L/R`, `root` > `leg.L/R` > `foot.L/R`. `.L` is the character's left (+X). |
| Skinning | rigid: every vertex is weighted 1.0 to exactly one bone, which makes squash and stretch safe |
| Animations | `idle` (48 f, loop), `run` (16 f, loop), `kick` (36 f, one-shot: wind-up f11 with plant-foot squash, contact about f14, follow-through f19, land f26), `cheer` (24 f, loop). 24 fps. |
| Materials | Principled / StandardMaterial3D, flat base colours. Textures only for the face atlas, Chuck's tie-dye and his T-Rex patch. |
| Face | material `<id>_face`: a 2048² atlas of four expressions (2×2 cells) |
| Extras | body node `jarling_expressions` = UV offsets; rig node `jarling_actions`, `jarling_loops`; Chuck's hat node `jarling_detachable` |
| Size | about 30k triangles, 1.2–1.5 MB per character |

## Using it in Godot 4.7.2

1. Drop the `.glb` in the project (from the `addons/openjar/characters/` submodule) and instance it.
   The importer makes a `Skeleton3D`, a skinned `MeshInstance3D` and an `AnimationPlayer` holding
   `idle`, `run`, `kick` and `cheer`.
2. **Loops.** In the Advanced Import Settings, set `idle`, `run` and `cheer` to *Loop: Linear*, or
   do it in code with `anim.loop_mode = Animation.LOOP_LINEAR`. The last key repeats the first, so
   the loop is seamless.
3. **Expressions.** The face is one material with a 2×2 atlas. To switch, set the UV offset on that
   material (make it unique per instance first):
   ```gdscript
   const EXPR := {"neutral": Vector3(0,0,0), "happy": Vector3(0.5,0,0),
                  "surprised": Vector3(0,0.5,0), "determined": Vector3(0.5,0.5,0)}
   func set_expression(body: MeshInstance3D, e: String) -> void:
       for s in body.mesh.get_surface_count():
           var m := body.get_active_material(s)
           if m and m.resource_name.ends_with("_face"):
               m = m.duplicate(); m.uv1_offset = EXPR[e]
               body.set_surface_override_material(s, m)
   ```
   The same offsets are stored on the body node as the `extras` meta (`jarling_expressions`).
4. **Chuck's hat** imports as `BoneAttachment3D("head") / chuck_hat`. To knock it off, reparent
   `chuck_hat` to the world, keeping its global transform, and give it a `RigidBody3D` with a
   cylinder or convex shape. To put it back, reparent it under the attachment and zero its local
   transform. Its local transform at import is the rest fit.
5. **Rim light.** The look depends on rim light. Turn on `rim_enabled` (rim about 0.4, tint about
   0.3) in the imported materials, or override them, and use a warm key DirectionalLight3D with
   soft shadows plus a sky-coloured ambient. The `.glb` materials hold colours only.
6. **Squash and stretch.** The animations already scale `root`, `spine`, `leg.L` and `foot.L`.
   Game-side juice can scale those bones further. Rigid skinning keeps that clean.

## Verified vs not

**Verified (2026-11-09):**
- Both character `.glb`s and a random generic (`--seed 9`) import headless in **Godot 4.7.2**. Each
  has 4 animations with the expected lengths, the expected bones and a skinned body. The kick track
  drives `leg.R` when played. Chuck's hat comes in as a `BoneAttachment3D` on `head`. Extras arrive
  as node meta.
- Every render in this folder and in `characters/*/refs/jarling/` was looked at and fixed where
  something was off: floating parts, hair poking through hats, arms hidden behind the head in
  `cheer`, beak placement and so on.
- Fixed colours are exact in the material base colours: Jeff `#FFD84D` / `#3B5BA5` / `#3CC24A`;
  Chuck `#2B2B33` / `#FFD84D` / `#1E1E26` / `#3B5BA5` / `#8A5A2B` / `#E4393C`.

**Not verified:**
- The game-side expression swap, rim-light setup and hat physics described above have **not been
  rendered in Godot**: there is no GPU here, so the Godot check was import-only.
- The animations were only checked as single poses in stills (kick f17/f18, cheer, idle f1). Full
  motion playback was not reviewed.
- Performance with many Jarlings on screen has not been tested. About 30k triangles each is fine for
  a handful of characters; a big crowd would want a decimated LOD.
