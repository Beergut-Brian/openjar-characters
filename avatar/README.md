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

## Body types

Kaden, 2026-11-10: *"one standard humanoid size, like we have now, but then non standard sizes for
the Dragon, mole, etc. Let's not go wild adding non standard sizes, but when it makes sense let's
get a new size/body type added."* Characters are designed **3D-first**: the Jarling is the master
for silhouette, proportions and colours, and every 2D style is derived from it.

`body.type` in `jarling.json` picks the body (default `"standard"`). `body.height` always means
"in standard Jarlings" (1.0 is about 1.1 m to the top of a bare head), on every type.

| Type | What it is | Use it for | Code | Characters |
| --- | --- | --- | --- | --- |
| `standard` | the humanoid Jarling: round head, capsule torso, arms, legs | every playable character, and any resident who is a person. Change `build`, `height`, `leg_scale`, head shape; add hats, beards, tunics as kit pieces (`pieces_*.py`) | `jarling_kit.py` | Jeff, Chuck, Gnome Foreman, Caveman, generics |
| `critter` | a small no-neck animal: one pear (a head blob sunk into a body blob), no visible legs, feet peeking out under the body, short arms with big paws | small round animals that stand upright: moles, hedgehogs, penguins, owls, frogs | `body_critter.py` | The Mole |
| `giant` | a huge sitting beanbag creature: round head on a bigger round body, stubby arms, big round feet out front, a thick tail, optional tiny wings and horn nubs | landmark-sized friendly creatures (about 3 to 8 Jarlings tall) | `body_giant.py` | The Dragon |

**When to add a body type.** Only when the standard body can't honestly express the character
*and* the type will be reused by later characters of that kind. Try `height`, `build`, `leg_scale`,
head shape and new kit pieces first. A one-off is a prop, not a body type. Non-standard types are
for non-playable residents only (README "Playable characters").

**What every body type provides** (the contract games and tests rely on, listed per type in
`characters.json` under `body_types`):

- **Bones.** All types share `root`, `spine`, `head`, `arm.L/R`, `hand.L/R`, `leg.L/R`, `foot.L/R`
  with the same meaning and parenting, so game code that nods a head or squashes `root` works on
  anyone. `critter` adds `prop` (a held item, child of `spine`); its leg bones are short stubs
  inside the body. `giant` adds `tail.1` > `tail.2` > `tail.3` (from `root`) and `wing.L/R` (from `spine`).
- **Actions.** Every type has `idle` (loop), `run` (loop: that body's way of getting about, a
  shuffle for a critter, a slow waddle for a giant) and `cheer` (loop). `standard` also has `kick`.
  `critter` adds `popup` and `bow`; `giant` adds `yawn`, `wave`, `flap` (loop) and `sleep` (loop).
  A standard character lists extra actions its bible needs in `"actions"` (registered in a
  `pieces_*.py` module, e.g. `march`, `write`, `polish`).
- **Equipment slots** wherever the body has the matching part, with the same names, axes and fit
  rule as `docs/equipment.md` (gear made for the reference Jarling fits). `critter` and `giant`
  have no knees: they lack `knee_l` / `knee_r`. `JarlingEquipment` reports a missing slot
  (`has_slot`, `missing_slots`, signal `slot_missing`, `equip` returns false) and never crashes.
- **Extras.** Rig: `jarling_body_type`, `jarling_slots`, `jarling_actions`, `jarling_loops`. Body
  mesh: `jarling_expressions`.
- **Rigid skinning, flat exact colours, face atlas, feet at y=0, faces +Z**, as the standard body.

**Expressions.** `face.expression_list` names up to six expressions (the first is the resting
face); the atlas is 2x2 cells for up to four and 3x2 for five or six. Without it a Jarling has the
standard `neutral`, `happy`, `surprised`, `determined`. Read the UV offsets from
`jarling_expressions`, do not hard-code them.

**Writing a body type.** Add `avatar/kit/body_<type>.py` with a class registered in
`kit.BODY_TYPES["<type>"]`. It takes `(params, prefix)` and `build()` returns itself with `.P`,
`.prefix`, `.rig`, `.body`, `.face_mat`, `.expr_names`, `.expr_uv`, `.slots`, `.L["head_c"]` and
`.L["R"]` (head centre and radius, for framing). Use `kit.build_actions(rig, posture, prefix,
acts=...)`, `kit.face_atlas(face, skin, draw=...)` and the kit's geometry helpers. Then add the
type's row to `tools/build_index.py` and the table above.

## Files

```
avatar/kit/jarling_kit.py      the kit: face-part library, geometry, rig, actions, random generics
avatar/kit/build_jarling.py    params JSON -> .glb (CLI)
avatar/kit/render_refs.py      turnaround / expressions / action / side renders for one Jarling of any body type (Cycles CPU)
avatar/kit/sprite_side.py      Pillow: the side render at The Hill's sprite scale (tracing base for 2D)
avatar/kit/pieces_*.py         kit pieces for the standard body (hats, beards, tunics, props, extra actions)
avatar/kit/body_*.py           non-standard body types (critter, giant)
avatar/kit/render_scenes.py    style_mock.png and generic_lineup.png
avatar/kit/render_common.py    shared lights / sky / camera
avatar/kit/render_scenes_ball.py  the six-panel ball used in renders
avatar/kit/label_sheet.py      Pillow: caption bar under the sheets
avatar/kit/make_all.sh         rebuilds every deliverable (about 7 minutes on 6 CPU cores)
avatar/kit/renders/            style_mock.png, generic_lineup.png
avatar/gear/build_gear.py      the starter gear set -> avatar/gear/<id>.glb + <id>.json (equipment)
godot/jarling_equipment.gd     Godot runtime that puts gear on a Jarling (+ jarling_gear.gd, the item)
godot/run_tests.sh             headless tests for it; godot/tools/shots.gd renders real frames
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
# the gear set
blender -b --factory-startup -P avatar/gear/build_gear.py      # [-- --only cape,hat]
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
  "body": {"build": "slim|regular|stocky|round|boxy|puffy", "height": 1.0, "leg_scale": 1.0,
           "width": 1.0, "belly": 0.0},          // kit v2: fat/skinny, see docs/kit-v2.md
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

Options added for the Hill residents (all optional, standard body): mouth `none` (hidden by a beard)
and `frown`; expression `eye_mode` `shut`; `face.eye_y` (moves eyes and brows up or down, default
-0.04, lower it under a low hat brim); `brow_raise_left` (one brow up); `face.nose_color` and
`nose_size` for the 3D `bump` nose; top `bare` (skin torso and arms); bottoms `none` (bare legs);
`posture.leg_bow` (knees out, metres); `shoes.foot_size` (scales bare feet); hair `mane`.
`"actions": [...]` adds extra actions and `"ref_action"` picks the action sheet's pose.
From `pieces_hill.py`: headwear `cone_hat` (with a detachable `hard_hat` tip) and `ice_cube`;
costume pieces `gnome_beard`, `vest_stripes`, `clipboard`, `whistle`, `mane_beard`, `fur_tunic`,
`cloth_club` (`clipboard` and `cloth_club` take `"hand": "L"|"R"` and are part `prop`); actions
`march`, `write`, `salute`, `polish`, `point`, `wave`.

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
| Equipment slots | ten `slot_<name>` nodes on bones: `head`, `face`, `back`, `waist`, `hand_l/r`, `knee_l/r`, `foot_l/r`, fit scale baked in; extras `jarling_slot`, `jarling_build`, `jarling_id` |
| Body parts | `<id>_part_<name>` skinned meshes gear can hide: `foot_l/r` (bare feet or the character's shoes), `hand_l/r`, `headwear` (Jeff's comb, a generic's cap; Chuck's `chuck_hat` also counts), `tail` (Jeff). Extras `jarling_part`. |
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

## Kit v2 (2026-11-10)

Fat/skinny (`body.width` 0.75-1.5, `body.belly` 0-1), any skin colour with skin-derived face
colours, `head.features` (antennae, horns, pointy ears, fins: body parts on their own bones, hats
go on top), data-driven hair (`hair.pieces`, presets), shirt and trouser patterns, more shoes,
headwear, costume pieces and face extras for the 19 sheets. Full reference:
[`docs/kit-v2.md`](../docs/kit-v2.md); sheet-by-sheet params: [`docs/sheets-coverage.md`](../docs/sheets-coverage.md);
the range on one skeleton: `kit/renders/kit_v2_range.png`.

## Equipment (gear that goes *on* the Jarling)

Full contract: [`docs/equipment.md`](../docs/equipment.md). In short:

- Every Jarling has **ten slots** that follow their bones. One item per slot; a pair (shoes,
  gloves, kneepads) fills both sides together.
- A gear item is `avatar/gear/<id>.glb` (modelled in slot space for the reference Jarling; the slot
  marker's scale fits it to each build) plus `<id>.json` (`id`, `slots`, `replaces_body_part`,
  `fit`, `level_up`, `spring`).
- Shoes and gloves **replace** the feet/hands (the body part meshes are hidden), kneepads, belts,
  capes and jetpacks **wrap**. Capes swing on a small spring.
- `godot/jarling_equipment.gd`: `equip(item)` (swaps a filled slot; a repeat item levels up
  instead of stacking), `unequip(slot)`, `equipped(slot)`, `has_item(id)`, `level_up(slot)`,
  signals `item_equipped`, `item_unequipped`, `item_leveled_up`, `poof`.

```gdscript
var eq := JarlingEquipment.new()
jeff.add_child(eq)                               # jeff = the instanced jeff.glb
eq.poof.connect(func(slot, at): Fx.puff(at))     # your puff
eq.equip(JarlingGear.load_json("res://addons/openjar/characters/avatar/gear/sneakers.json"))
```

Starter set (proof art, a later Art lane redoes it): `sneakers`, `boots`, `rocket_boots`,
`kneepads`, `cape`, `jetpack`, `hat`, `sunglasses`, `gloves`, `belt`.

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
