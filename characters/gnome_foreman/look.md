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
Status of the 3D form: **approved (Kaden 2026-11-10, D49 a with the Gnome whistle fix)**: the whistle is a referee whistle on a cord, hanging on his chest below the beard (barrel, ring, cord); it is at his mouth only in the `whistle` action / expression cell; nothing is near his mouth at rest and nothing may read as a pipe in any style. The clipboard is gripped in a fist at his side (hold style `one_hand_low`). The 3D master is the source of truth for silhouette, proportions and colours; the pixel form is traced from it (3D-first, `tools/pixel/retrace.sh`).
- **Body type: `standard`.** He is a person, so the kit body with params does it: `build` stocky, `height` 0.6, head `wide` at size 0.85. About 0.79 m to the top of his head and about 1.24 m with the hat, so the cone and hard hat are about 40% of his height, as in the sprite.
- New kit pieces (`avatar/kit/pieces_hill.py`): `cone_hat` headwear (part `headwear`) with the tiny hard hat as a separate object `gnome_foreman_hat` on the head bone (`jarling_detachable`, like Chuck's hat, so it can fall off the tip); `gnome_beard` (hides the mouth; mouth `none`); `vest_stripes`; `whistle`: a chunky yellow referee whistle (short drum facing front, flat mouthpiece out to the side, dark slot on top in a darker shade of the whistle yellow, ring on top) hanging on his chest just below the beard tip (beard `length` 1.15 to make room) on a two-strand cord from the sides of his neck; nothing is near his mouth at rest. Bones `whistle`, `cord.L`, `cord.R` (children of `head`, like the beard, so it stays under the beard tip); `clipboard` in his right hand (part `prop`). Big 3D nose in the nose colour, bushy cream brows.
- Face (atlas, five cells): `stern` (resting), `approving`, `sorry`, `hopeful`, `whistle`. Brows and eyes do the work.
- Actions: the standard `idle`, `run`, `kick`, `cheer`, plus `march` (loop), `write` (loop: clipboard up, scribble and tick), `salute` (with the clipboard) and `whistle` (frames 1-34: the free left hand lifts the whistle to the corner of his mouth by frame 9, two puffs at 13 and 20, back on his chest at 34; the cord follows). The `whistle` cell of the expression sheet is posed at frame 16 (`expression_poses` in `jarling.json`).
- Equipment: all ten slots. A hat in the head slot replaces the cone (it is his `headwear` part).
- Files: `jarling.json`, `refs/jarling/gnome_foreman.glb`, `gnome_foreman_turnaround.png`, `gnome_foreman_expressions.png`, `gnome_foreman_write.png`, `gnome_foreman_side.png`, `gnome_foreman_side_sprite.png`.
- Changes from the 2D look and colours not on the fixed list: sleeves and trousers are the vest orange `#F7932F` (as the sprite draws them); the vest stripes and the clipboard clip use the hard-hat cream `#F4F1E6`; the whistle cord is the clipboard wood `#B07A3C`. Not built: the "hard hat off, waiting" pose (detach the hat in the game).

## 2D pixel (The Hill)
- **3D-first redraw, 2026-11-10** (Kaden: the 3D master is the source of truth). Traced from the 3D master: `avatar/kit/render_trace.py` (flat colour, orthographic, 512 px per 1.2 m) -> `tools/pixel/trace3d.py` (palette-snapped, 32 px = 1.2 m) -> hand-clean passes in `tools/pixel/residents.py`; 1 px #2A1E2C outline, fixed colours only. Re-run: `tools/pixel/retrace.sh`. Read check at game size (x2): `characters/read_check.png`.
- 32 px tall including the outline (true 3D scale: 1.23 m with the cone), on the 40 x 32 frame.
- Traced: cone, beard, vest, boots, clipboard, arms; the whistle pose. Hand-cleaned: the tiny hard hat (dome and brim on the cone tip), nose, eyes, brows, cheeks, the clipboard's lines and clip, the whistle.
- The whistle hangs on its cord on his chest BELOW the beard (yellow barrel, dark ring, wood cord); it is raised to his mouth only in the `whistle` pose/expression, with yellow sound lines. Nothing sits beside his mouth at rest (the old sprite read as a pipe).
- Must still read at 16 px: the teal cone, the white dot on its tip, the cream beard and the orange vest.
- Poses: idle (clipboard), whistle, hat in hands. Views: front, side, back.
- Expressions: stern (neutral), approving, sorry, hopeful, whistle.

## Refs
`refs/look_sheet.png` (turnaround, key poses, expressions, arc pictograms) and `characters/residents_lineup.png` for scale.
