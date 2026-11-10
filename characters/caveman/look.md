# The Caveman: look

## Must survive every art style
- A huge wild chestnut hair-and-beard mass.
- One ice cube frozen to the top of his head. It never melts.
- A one-shoulder ochre fur tunic with brown spots and a zigzag hem.
- Short bowed legs and big bare feet.
- A club-shaped polishing cloth: a soft cloth bundle on a stick, used only for polishing.

## Silhouette
A wide wedge: broad shoulders, a big hair mass, a small ice cube on top, short bowed legs. Identifiable in outline alone.

## Face
Delighted (neutral), baffled, sorry, hopeful, amazed. Wide eyes, bushy brows and a big grin.

## Fixed colours
- Hair and beard: #7A4A2A
- Skin: #D99A6C
- Tunic: #D9A441, spots #7C4E24
- Ice cube: #BFE6F5
- Polishing cloth: #F3EAD2, tied with teal string #1E9AA0 on a wood stick
- Outline in pixel art: #2A1E2C

## Signature props
The cloth club, used only for polishing. The ice cube counts as headwear.

## Jarling 3D
Status of the 3D form: **proposed** (Character lane 2026-11-10, awaiting Kaden). The 2D look above is approved (D46 a). Since Kaden's 3D-first direction (2026-11-10) this model is meant to become the master for silhouette, proportions and colours, and the 2D sprites get redrawn from `refs/jarling/caveman_side.png` / `caveman_side_sprite.png`.
- **Body type: `standard`.** `build` boxy, `height` 0.8, `leg_scale` 0.75, head `wide`, bowed legs (`posture.leg_bow`), big bare feet (`shoes.foot_size`). About 1.2 m tall including the ice cube.
- New kit pieces (`avatar/kit/pieces_hill.py`): hair `mane` plus `mane_beard` (one wild chestnut mass round the whole face); `ice_cube` headwear (part `headwear`); `fur_tunic` (one shoulder, spots, zigzag hem) over top `bare` and bottoms `none`; `cloth_club` in his left hand (part `prop`).
- Face (atlas, five cells): `delighted` (resting), `baffled`, `sorry`, `hopeful`, `amazed`. Eyes `wide`, brows `bushy`.
- Actions: the standard `idle`, `run`, `kick`, `cheer`, plus `polish` (loop, the signature rub), `point` (whole arm) and `wave`.
- Equipment: all ten slots. A hat in the head slot replaces the ice cube (his `headwear` part), so games that keep the "never melts" rule should not offer him hats.
- Files: `jarling.json`, `refs/jarling/caveman.glb`, `caveman_turnaround.png`, `caveman_expressions.png`, `caveman_polish.png`, `caveman_side.png`, `caveman_side_sprite.png`.
- Changes from the 2D look: none in colour. The knee equipment slot sits on the straight hip-to-ankle line, about 3 cm inside his bowed knee. Not built: the sneeze (snowflakes are a game effect).

## 2D pixel (The Hill)
- 32 px tall including a 1 px #2A1E2C outline, on 16 px tiles, drawn on a 40 x 32 canvas.
- Must still read at 16 px: the hair mass, the pale blue ice dot on top and the bowed legs.
- Poses: bounce, point with the whole arm, polish, wave, sneeze (snowflakes).
- Expressions: delighted (neutral), baffled, sorry, hopeful, amazed.

## Refs
`refs/look_sheet.png` (turnaround, key poses, expressions, arc pictograms) and `characters/residents_lineup.png` for scale.
