# Jarling equipment: the contract

*Equipment lane, 2026-11-09. Owner of the format: this repo. Games consume it, they do not fork it.*

Gear is something a Jarling **wears**: shoes, kneepads, a cape, a jetpack, a hat. It sits in a named
**slot**, follows the body as it animates, can **replace** a body part (shoes hide the bare feet),
and a slot holds **one item at a time**. Getting the same item again levels it up; it never stacks.

## Kit v2 notes (2026-11-10)

- **Fat and skinny bodies.** Slot markers are measured from the built surface, so their scale is
  the fit: on the widest body (`width` 1.5, `belly` 1) the waist, back, knee, hand and foot slots
  are bigger, on the skinniest smaller. Nothing changes for gear authors.
- **Head features** (`feature_antennae`, `feature_horns`, `feature_pointy_ears`, `feature_fins`) are
  body parts. Gear hides them only if its JSON says so: `"hides_features": ["antennae"]` or `true`
  (all). `JarlingEquipment.features()` lists what a Jarling has. Hats normally leave it out and the
  antennae poke through.
- The head slot fit follows the scalp, not hair pieces: a tall hairdo can poke through a hat.

## 1. Slots

Every Jarling `.glb` built by `avatar/kit` (Jeff, Chuck, every generic) has ten slot markers. Each
one is a `Node3D` named `slot_<name>` that the Godot importer puts under a `BoneAttachment3D` for
its bone, so it moves with the animation.

| Slot | Bone | Origin (rest pose) | Fit scale = this Jarling / reference | For |
| --- | --- | --- | --- | --- |
| `head` | `head` | head centre | crown height (top of head, hair or hood) / 0.27 m, uniform | hats, helmets |
| `face` | `head` | front of the face, at eye level (head centre is 0.235 m behind, -Z) | head width / 0.235 m, uniform | glasses, masks, moustaches |
| `back` | `spine` | middle of the back surface, at shoulder height | torso width / 0.152 m, uniform | capes, jetpacks, wings |
| `waist` | `spine` | torso axis at belt height (the shirt/trouser hem) | torso half-width / 0.155 m on X, half-depth / 0.127 m on Z, 1 on Y | belts, floaties |
| `hand_l`, `hand_r` | `hand.L/R` | centre of the mitten hand | limb thickness, uniform | gloves, foam fingers |
| `knee_l`, `knee_r` | `leg.L/R` | on the leg axis, 45% of the way from hip to ankle | leg radius at the knee / 0.049 m, uniform | kneepads |
| `foot_l`, `foot_r` | `foot.L/R` | on the ground, under the ankle | limb thickness, uniform | shoes, boots, skates |

- **Axes** are the model's at rest: +Y up, **+Z front** (the way the Jarling faces), +X the
  character's left. `_l` / `.L` is always the character's own left.
- **Fit** is baked into the marker's scale. A piece made for the reference Jarling (regular build,
  round head, size 1, short hair) at scale 1 fits every build. The marker also carries the build
  name in its `extras` meta (`jarling_build`), for the optional per-build `fit` table below.
- There is one leg bone per leg (rigid capsules, no knee bend), so `knee_*` follows the whole leg.
  If the kit later grows a knee joint, `knee_*` moves to the lower leg bone and keeps its name.

## 2. Separable body parts

Parts a piece of gear may hide are their own skinned meshes on the same skeleton, named
`<id>_part_<name>` (Godot: `MeshInstance3D` under the `Skeleton3D`), with `extras.jarling_part = <name>`.

| Part | What it is |
| --- | --- |
| `foot_l`, `foot_r` | bare foot, or the character's own shoes (Chuck's boots, including the boot shafts) |
| `hand_l`, `hand_r` | the mitten hand |
| `headwear` | Chuck's trucker hat (`chuck_hat`, still detachable as before); Jeff's comb; a generic's cap, beanie or headband |
| `tail` | Jeff's tail feathers |

A part only exists if that Jarling has it; hiding a missing part is a no-op. The rest of the body
stays one mesh. With nothing equipped every Jarling looks exactly as before.

## 3. A gear item

Two files side by side, both in `avatar/gear/`:

```jsonc
// avatar/gear/sneakers.json
{
  "id": "sneakers",                      // unique; the "same item" test
  "name": "Sneakers",
  "slots": ["foot_l", "foot_r"],         // or "slot": "back" for a single slot
  "scene": "sneakers.glb",               // relative to this file
  "replaces_body_part": ["foot_l", "foot_r"],   // hidden while worn, back when removed
  "fit": {"puffy": {"offset": [0, 0, 0], "scale": 1.0}},   // optional, per build, on top of the marker fit
  "level_up": {"max": 3, "scale_step": 0.06},  // optional; these are the defaults
  "spring": {"node": "cape_pivot", "stiffness": 45, "damping": 7, "gain": 0.5,
             "rest_deg": 6, "max_deg": 60}       // optional: a node that swings (capes)
}
```

The `.glb` is authored in **slot space** (origin and axes of the slot, reference size):

- **Paired items** (`slots` with two entries) have one top-level node per slot, named after the
  slot: `foot_l` and `foot_r`. Each is attached to its own marker. If there is a single top-level
  node instead, it is used for every slot listed.
- Nodes named `trim*` are the **level-up trim** (a gold stripe, a sparkle band). The runtime hides
  them at level 1 and shows them from level 2.
- Nodes named `fx_*` are effect hooks (rocket flames, jetpack exhaust). They ship visible; a game
  hides or animates them.
- The `spring` node is the pivot a cape hangs from. The runtime swings it around its X axis (positive =
  away from the back) from how fast the slot moves forward and up/down.
- Smooth-shaded, flat colours, no outlines, original designs (see `avatar/README.md`). About 1-5k
  triangles per piece.

`replaces_body_part` vs wrap: shoes and gloves **replace** (the part is hidden and the gear is the new
foot or hand). Kneepads, belts, capes and jetpacks **wrap** (nothing hidden).

## 4. The rules

1. **One item per slot.** Equipping into a filled slot **swaps**: the old item comes off all of its
   slots (both shoes go, not one), its hidden body parts come back, then the new item goes on. A
   `poof` is emitted at the slot.
2. **No duplicates.** Equipping an item whose `id` is already worn calls `level_up` on it instead.
   Level up: +6% scale per level (max level 3), trim shown from level 2, a `poof`. Nothing new is
   added to the scene.
3. **Hidden parts are reference counted.** A part comes back only when no worn item still hides it.
4. Gear never changes the character's fixed colours or its own meshes; it only hides parts and adds nodes.

## 5. Godot runtime: `godot/jarling_equipment.gd`

```gdscript
class_name JarlingEquipment extends Node     # child of an instanced Jarling glb (or set `jarling`)
signal item_equipped(slot: StringName, item: JarlingGear)    # once per slot
signal item_unequipped(slot: StringName, item: JarlingGear)
signal item_leveled_up(slot: StringName, item: JarlingGear, level: int)
signal poof(slot: StringName, at: Vector3)    # play your puff / sfx here (equip, swap, level up)

@export var jarling: Node3D                   # default: the parent
@export var pop_in := true                    # scale-in tween on equip

func equip(item: JarlingGear) -> bool          # false when it levelled up an existing item instead
func unequip(slot: StringName) -> JarlingGear  # removes the whole item (both shoes); null if empty
func unequip_all() -> void
func equipped(slot: StringName) -> JarlingGear # null if empty
func has_item(id: StringName) -> bool
func level_up(slot: StringName) -> int         # new level (capped); 0 if the slot is empty
func level(slot: StringName) -> int
func slot_node(slot: StringName) -> Node3D     # the slot_<name> marker, for game-side effects
```

`godot/jarling_gear.gd` is the item (`class_name JarlingGear extends Resource`):
`JarlingGear.load_json("res://addons/openjar/characters/avatar/gear/cape.json")`, or build one in
code / a `.tres` with the same fields (`id`, `name`, `slots`, `scene`, `replaces_body_part`, `fit`,
`level_up`, `spring`).

The GDScript names differ from the first brief in one place: a class cannot have a method and a
signal both called `equipped`, so the method is `equipped(slot)` and the signal is `item_equipped`.

**Exports:** Godot does not export `.json` by default. A game that loads gear from JSON adds
`*.json` to the export preset's *Filters to export non-resource files*, or converts items to `.tres`.

## 5b. Other body types

Non-standard bodies (`critter`, `giant`; `characters.json` `body_types` lists each type's slots)
keep the slot names, axes and fit rule above; they just may lack some slots. Today `critter` and
`giant` have no `knee_l` / `knee_r`. `JarlingEquipment` adds `has_slot(slot)`, `missing_slots()`
(the SLOTS this body lacks) and `body_type()` (from the rig's `jarling_body_type`, default
`"standard"`), and the signal `slot_missing(slot, item)`. `equip(item)` on a body lacking ANY of the
item's slots adds nothing, hides nothing, emits `slot_missing` once per missing slot, warns once and
returns false; it never crashes and never parents gear to the root. `unequip`, `level_up`,
`equipped` and `level` on a missing slot are safe no-ops. Behaviour on the standard body is unchanged.

## 5c. Held items

A hand-slot item with a `hold` block in its JSON (`style`, `grip_r`, optional `grip_l` and `axis`) is *held*: the fist closes on `grip_r`, the arm takes the hold style's pose and the off hand goes to `grip_l`. Items without `hold` behave exactly as before. API: `hold_style(slot)`, `grip_error(slot)`. Full description and the five styles: [`avatar/README.md`](../avatar/README.md) "Holding items".

## 6. Versioning

The slot names, part names, the JSON keys and the API above are the contract. Adding a slot, a part
or an optional key is a minor change; renaming or removing one is a breaking change and needs a new
tag and a note in each consuming game's contracts.
