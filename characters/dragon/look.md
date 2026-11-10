# The Dragon: look

## Must survive every art style
- A giant round beanbag shape: never scary.
- No visible teeth, no sharp claws, no fire.
- Sleepy half-closed eyes, pink cheeks, two rounded cream horn nubs.
- Wings far too small, stubby arms, big round feet.
- A thick tail curling round to the front, with a soft peach puff tip.
- Round cream belly with soft stripes.

## Silhouette
A big round head on a bigger round body, with tiny wings and a curled tail. Identifiable in outline alone.

## Face
Sleepy (neutral), yawn, happy, sorry, hopeful. Her mouth is never open wide enough to show teeth, even in a yawn.

## Fixed colours
- Body: #A88BE0, shade #8C6FC8
- Belly and horns: #FFF0C9
- Wings, spines and tail puff: #FFB37A
- Cheeks: #F7A6C0
- Smoke rings: #C9C4D4
- Outline in pixel art: #2A1E2C

## Signature props
Smoke rings, sometimes heart-shaped. Gnome lanterns, once they have hung them on her.

## Jarling 3D
Status of the 3D form: **proposed** (Character lane 2026-11-10, awaiting Kaden). The 2D look above is approved (D46 a). Since Kaden's 3D-first direction (2026-11-10) this model is meant to become the master for silhouette, proportions and colours, and the 2D sprites get redrawn from `refs/jarling/dragon_side.png` / `dragon_side_sprite.png`.
- **Body type: `giant`** (`avatar/kit/body_giant.py`): a huge sitting beanbag creature, reusable for later landmark-sized creatures. This replaces the earlier note that she would be a bespoke prop: Kaden's 2026-11-10 direction asks for a named body type. `jarling.json`: `body.type` giant, `body.height` 6.0 (about 6 standard Jarlings, 6.6 m to the top of the horn nubs).
- Shape: a big round head sunk into a bigger round body, stubby arms with mitten hands, big round feet out front with cream sole pads, tiny peach wings high on the back, peach spines down the back and tail, a thick tail curling round to the front with the peach puff tip, round cream belly with soft stripes, two round cream horn nubs. No teeth, no claws, no fire.
- Face (atlas, six cells): `sleepy` (resting, heavy `#8C6FC8` lids), `yawn` (eyes shut, small round mouth), `happy`, `sorry`, `hopeful`, plus `asleep` (closed lines, for the `sleep` action).
- Bones: the shared eleven plus `tail.1` > `tail.2` > `tail.3` and `wing.L/R`. Actions, all slow: `idle`, `run` (a slow waddle in place), `cheer`, `yawn`, `wave` (the signature slow wave), `flap` (the tiny wings; nothing happens), `sleep`.
- Equipment slots: head, face, back, waist, both hands, both feet, with the fit scale baked in, so the same hat that fits Jeff comes out dragon-sized. No knees.
- Files: `jarling.json`, `refs/jarling/dragon.glb`, `dragon_turnaround.png`, `dragon_expressions.png`, `dragon_yawn.png`, `dragon_side.png`, `dragon_side_sprite.png`.
- Changes from the 2D look and colours not on the fixed list: the muzzle is a shaped bump in the body colour (the sprite tints it lighter); the belly stripes use the sprite's `#F0DAA6`. Size: the 3D master is 6 Jarlings tall as the sketch said, while the approved Hill sprite is 3.5 players tall (112 px); the side-view sprite sheet is at the 3D scale. Not built: the curled-asleep pose (the `sleep` action is a sitting nap), smoke rings and lanterns (game effects and props), the "in pieces on the elevator" pose.

## 2D pixel (The Hill)
- Sitting awake: about 128 x 112 px (3.5 players tall), with a 1 px #2A1E2C outline.
- Curled asleep: about 160 x 72 px.
- Must still read at 16 px: the round purple mass, the cream belly and the peach tail puff.
- Poses: asleep (curled), awake and sitting, yawn, wing flap, in pieces on the elevator.
- Expressions: sleepy (neutral), yawn, happy, sorry, hopeful.

## Refs
`refs/look_sheet.png` (turnaround, key poses, expressions, arc pictograms) and `characters/residents_lineup.png` for scale.
