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
Status of the 3D form: **approved (Kaden 2026-11-10, D49 a with the Gnome whistle fix)**: broader and heavier like his sprite (`body.width` 1.45, `body.belly` 0.55, big shaggy beard); the cloth club is gripped in a fist and carried upright (hold style `one_hand_raised`). The 3D master is the source of truth for silhouette, proportions and colours; the pixel form is traced from it (3D-first, `tools/pixel/retrace.sh`).
- **Body type: `standard`.** `build` boxy, `height` 0.8, `leg_scale` 0.75, kit v2 `width` 1.45 and `belly` 0.55 (a broad heavy wedge like the approved sprite, Kaden 2026-11-10; limbs thicken with the width), head `wide`, bowed legs (`posture.leg_bow`), big bare feet (`shoes.foot_size`). About 1.2 m tall including the ice cube.
- New kit pieces (`avatar/kit/pieces_hill.py`): hair `mane` plus `mane_beard` (one wild chestnut mass round the whole face; the beard is wider than the face, `width` 1.2, `length` 1.5, with a ragged edge (`shag`, `tufts`) and nine pointed hanging tufts (`clumps`), leaning out over the belly so it sits on the chest above the tunic); `ice_cube` headwear (part `headwear`); `fur_tunic` (one shoulder, spots, zigzag hem) over top `bare` and bottoms `none`; `cloth_club` in his left hand (part `prop`).
- Face (atlas, five cells): `delighted` (resting), `baffled`, `sorry`, `hopeful`, `amazed`. Eyes `wide`, brows `bushy`.
- Actions: the standard `idle`, `run`, `kick`, `cheer`, plus `polish` (loop, the signature rub), `point` (whole arm) and `wave`.
- Equipment: all ten slots. A hat in the head slot replaces the ice cube (his `headwear` part), so games that keep the "never melts" rule should not offer him hats.
- Files: `jarling.json`, `refs/jarling/caveman.glb`, `caveman_turnaround.png`, `caveman_expressions.png`, `caveman_polish.png`, `caveman_side.png`, `caveman_side_sprite.png`.
- Changes from the 2D look: none in colour. The knee equipment slot sits on the straight hip-to-ankle line, about 3 cm inside his bowed knee. Not built: the sneeze (snowflakes are a game effect).

## 2D pixel (The Hill)
- **3D-first redraw, 2026-11-10** (Kaden: the 3D master is the source of truth). Traced from the 3D master: `avatar/kit/render_trace.py` (flat colour, orthographic, 512 px per 1.2 m) -> `tools/pixel/trace3d.py` (palette-snapped, 32 px = 1.2 m) -> hand-clean passes in `tools/pixel/residents.py`; 1 px #2A1E2C outline, fixed colours only. Re-run: `tools/pixel/retrace.sh`. Read check at game size (x2): `characters/read_check.png`.
- 32 px tall including the outline (true 3D scale: 1.21 m with the ice cube), on the 40 x 32 frame; broader and heavier, as the 3D master.
- Traced: hair and beard mass, ice cube, tunic and spots, legs and feet, the cloth club. Hand-cleaned: eyes, brows, mouth, blush, the ice cube's white glint, the club's teal string.
- Must still read at 16 px: the hair mass, the pale blue ice dot on top and the bowed legs.
- Poses: idle, polish, wave. Views: front, side, back.
- Expressions: delighted (neutral), baffled, sorry, hopeful, amazed.

## Refs
`refs/look_sheet.png` (turnaround, key poses, expressions, arc pictograms) and `characters/residents_lineup.png` for scale.
