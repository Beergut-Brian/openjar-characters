# Snooze — look

## Kaden's sheet (verbatim)
Medium, slightly slouched. Long striped nightcap with a pom-pom that flops to one side, light blue pajamas with white stars, fuzzy yellow slippers. Eyes permanently closed in happy arcs.

## Must survive every art style
- Long striped nightcap with a pom-pom that flops to one side
- Light blue pajamas with white stars
- Fuzzy yellow slippers
- Medium, slightly slouched
- Eyes permanently closed in happy arcs

## Silhouette
Medium slouched body with a long cone nightcap flopping over to one side, pom-pom hanging at shoulder height. The droop is the outline.

## Face
Eyes always closed in happy arcs (never open). Expressions to build: content (closed arcs, small smile), yawn (mouth big `o`, eyes squeezed), snore (mouth slightly open).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- nightcap stripe A: `#6F7FD8`
- nightcap stripe B + pom: `#F5F5F2`
- pajamas: `#A9D4F2`
- pajama stars: `#FFFFFF` (accent)
- slippers: `#FFD95A`

## Signature props
- Nightcap (headwear: long cone, flops to one side, pom-pom tip, sway bones)
- No gear

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/snooze/jarling.json` (standard humanoid body, kit v2; costume pieces sit over the standard body, same skeleton, actions, slots and collision as every playable character).
- **body:** `regular`, height 1.0, leg_scale 0.95; posture `spine_lean` 7, `head_lean` 4 (slightly slouched)
- **head:** `round` 1.0, skin `#F7CFAE`; `short` hair `#7A4B2A`
- **headwear:** `nightcap` `#6F7FD8` / stripe `#F5F5F2` / pom `#F5F5F2`, `length` **1.6** (longer than the kit default so it flops over to one side; the pom-pom is on its own bob bone)
- **top:** `long` `#A9D4F2` + `stars` `#FFFFFF`; **bottoms:** `pants` `#A9D4F2` + `stars`; **shoes:** `slippers` `#FFD95A`
- **face:** eyes closed happy arcs in every expression (never open). neutral = happy = content (small smile), surprised = yawn (eyes squeezed, big `o`), determined = snore (arcs, small `o`)
- **ref action:** `idle` frame 1 with the yawn face (`snooze_idle.png`)
- **3D size:** 1.31 m with the cap

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/snooze.glb`: the 3D master
- `refs/jarling/snooze_turnaround.png`, `snooze_expressions.png`, `snooze_idle.png`
- `refs/jarling/snooze_side.png`, `snooze_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/snooze_pixel.png`, `snooze_frames.png` (+ `.json`), `snooze_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/snooze.py` (`snooze()`)

- **Height:** 32 px with the outline (the 3D is about 1.31 m with the cap, squeezed to the 32 px frame): nightcap 8 rows
  (dome 7 + white brim row), face 7, torso 7, pants 5, slippers 3. Medium build; in the frames the head sits 1 px forward of
  the torso (slight slouch).
- **Palette:** cap stripes `#6F7FD8` / `#F5F5F2` (brim and pom-pom `#F5F5F2`), hair `#7A4B2A`, skin `#EFBB90` (+ `#CF9A70`),
  eyes `#2A1E2C`, mouth `#6A2232`, blush `#F4A9A0`, pyjamas `#A9D4F2` (back sleeve and leg `#8CBAD9`), star pixels `#FFFFFF`,
  slippers `#FFD95A` (sole `#D9B03A`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions).
- **Should read as:**
  - a sleepy kid in pyjamas and a floppy nightcap (not a gnome, not a wizard, the cap tip not a horn): 2 px diagonal stripes
    on the dome, a white brim row, the cap flopping to one side (the viewer's right in the front form, back/left in the frames)
    and hanging down so a round white 3 x 3 pom-pom ends at ear/shoulder level beside the head
  - eyes always closed: 3 px happy arcs in every frame including `eyes_shut`, a small smile, a faint blush pixel; brown hair under the brim
  - light blue pyjamas with scattered single white star pixels (not a grid) and fuzzy, rounded, slightly wide yellow slippers
