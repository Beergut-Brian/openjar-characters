# The Gnome Foreman: look

## Must survive every art style
- A tall teal cone hat, about half his height, with a tiny white hard hat perched on the very tip.
- A big cream beard triangle that hides his mouth.
- Hi-vis orange vest with cream stripes.
- A big round nose and bushy cream brows.
- Clipboard and whistle on a cord.

## Silhouette
A spike: a cone hat, a small body and a beard triangle. Identifiable in outline alone.

## Face
Stern (neutral), approving, sorry, hopeful, whistle. The mouth is hidden by the beard, so the brows and nose do the work.

## Fixed colours
- Cone hat: #1E9AA0
- Tiny hard hat: #F4F1E6
- Beard: #EDE6D6
- Vest: #F7932F with cream stripes
- Skin: #E8B48C
- Nose: #E59A86
- Boots: #4A3B3B
- Clipboard: #B07A3C, paper #FFFDF4
- Whistle: #FFD23F
- Outline in pixel art: #2A1E2C

## Signature props
The tiny hard hat (separate, it can fall off the cone tip), the clipboard and the whistle on its cord.

## Jarling 3D
Status of the 3D form: **proposed** (Character lane 2026-11-10, awaiting Kaden). The 2D look above is approved (D46 a). Since Kaden's 3D-first direction (2026-11-10) this model is meant to become the master for silhouette, proportions and colours, and the 2D sprites get redrawn from `refs/jarling/gnome_foreman_side.png` / `gnome_foreman_side_sprite.png`.
- **Body type: `standard`.** He is a person, so the kit body with params does it: `build` stocky, `height` 0.6, head `wide` at size 0.85. About 0.79 m to the top of his head and about 1.24 m with the hat, so the cone and hard hat are about 40% of his height, as in the sprite.
- New kit pieces (`avatar/kit/pieces_hill.py`): `cone_hat` headwear (part `headwear`) with the tiny hard hat as a separate object `gnome_foreman_hat` on the head bone (`jarling_detachable`, like Chuck's hat, so it can fall off the tip); `gnome_beard` (hides the mouth; mouth `none`); `vest_stripes`; `whistle` on its cord; `clipboard` in his right hand (part `prop`). Big 3D nose in the nose colour, bushy cream brows.
- Face (atlas, five cells): `stern` (resting), `approving`, `sorry`, `hopeful`, `whistle`. Brows and eyes do the work.
- Actions: the standard `idle`, `run`, `kick`, `cheer`, plus `march` (loop), `write` (loop: clipboard up, scribble and tick) and `salute` (with the clipboard).
- Equipment: all ten slots. A hat in the head slot replaces the cone (it is his `headwear` part).
- Files: `jarling.json`, `refs/jarling/gnome_foreman.glb`, `gnome_foreman_turnaround.png`, `gnome_foreman_expressions.png`, `gnome_foreman_write.png`, `gnome_foreman_side.png`, `gnome_foreman_side_sprite.png`.
- Changes from the 2D look and colours not on the fixed list: sleeves and trousers are the vest orange `#F7932F` (as the sprite draws them); the vest stripes and the clipboard clip use the hard-hat cream `#F4F1E6`; the whistle cord is the clipboard wood `#B07A3C`. Not built: the "hard hat off, waiting" pose (detach the hat in the game).

## 2D pixel (The Hill)
- 32 px tall including a 1 px #2A1E2C outline, on 16 px tiles, drawn on a 40 x 32 canvas.
- Must still read at 16 px: the teal cone, the white dot on its tip, the cream beard and the orange vest.
- Poses: march, stop and write, salute with the clipboard, hard hat off (waiting), whistle.
- Expressions: stern (neutral), approving, sorry, hopeful, whistle.

## Refs
`refs/look_sheet.png` (turnaround, key poses, expressions, arc pictograms) and `characters/residents_lineup.png` for scale.
