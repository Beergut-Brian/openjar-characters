# Captain Crumbs — look

## Kaden's sheet (verbatim)
Tall with a round middle. Tall white chef hat with a small skull-and-spoon badge, black eyepatch, white chef jacket with navy buttons, navy striped pants, black boots. Big curly moustache over a grin.

## Must survive every art style
- Tall white chef hat with a small skull-and-spoon badge
- Black eyepatch
- White chef jacket with navy buttons
- Navy striped pants, black boots
- Big curly moustache over a grin; tall with a round middle; usually dusted in flour

## Silhouette
Tall body with a round middle under a very tall puffed chef hat; curly moustache. A tall exclamation mark with a puffy top.

## Face
Eyepatch over one eye (left), big curly moustache, broad grin. Expressions to build: hearty grin (default), "arrr" growl (mouth open, brow down), laughing (eye closed, head back).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- chef hat: `#F7F7F2`
- badge: `#1F2D55` (accent)
- eyepatch: `#18181C` (accent)
- chef jacket: `#F7F7F2`
- buttons: `#1F2D55` (accent)
- pants stripe navy: `#1F2D55`
- pants stripe white: `#F7F7F2`
- boots: `#18181C`
- moustache: `#4A3324`

## Signature props
- Chef hat with skull-and-spoon badge (headwear)
- Eyepatch (face slot)
- Optional wooden spoon in `hand_r`
- Flour-puff particle on claps (effect, not a mesh)

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/captain_crumbs/jarling.json` (standard humanoid body, kit v2; costume pieces sit over the standard body, same skeleton, actions, slots and collision as every playable character).
- **body:** `round`, height 1.2, width 1.15, belly 0.6 (tall with a round middle)
- **head:** `round` 1.0, skin `#D99E6E`; `short` hair `#4A3324`; thick brows
- **headwear:** `chef_hat` `#F7F7F2` with a round navy badge `#1F2D55` (a plain badge, not a drawn skull and spoon: kit limit)
- **costume:** `eyepatch` over his left eye (strap round the head), `moustache` curly `#4A3324` lying on the face over the grin
- **top:** `long` `#F7F7F2` + `buttons` `#1F2D55` (two rows); **bottoms:** `pants` `#1F2D55` + `vstripes` `#F7F7F2`; **shoes:** `chunky_boots` `#18181C`
- **face:** Expressions: neutral = hearty grin (`grin_top`), happy = laughing (eyes closed), surprised = `o`, determined = "arrr" growl (`grit`, brow down)
- **ref action:** `cheer` frame 10, laughing (`captain_crumbs_cheer.png`)
- **3D size:** 1.58 m with the hat, the tallest playable Jarling
- **Not built:** the optional wooden spoon; flour dusting (in-game particle on claps)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
`refs/`: 3D renders in `refs/jarling/` (kit lane).
- `refs/pixel/captain_crumbs_pixel.png`, `captain_crumbs_frames.png` (+ `.json`), `captain_crumbs_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/captain_crumbs.py` (`captain_crumbs()`)

- **Height:** 32 px with the outline, the tallest of the batch (the 3D is about 42 px at true scale, squeezed to the 32 px
  frame): chef hat 8 rows (7 puff + band row), face 7, jacket 8, pants 4, boots 3. Round middle: jacket 14 px wide, head 10.
- **Palette:** hat and jacket `#F7F7F2` (shade `#D9D9D2`), badge and buttons and pants `#1F2D55`, skin `#D99E6E` (+ `#B97F52`),
  hair and moustache `#4A3324`, eyepatch and boots `#18181C`, eye `#2A1E2C` with `#FFFFFF` highlight, mouth `#6A2232`, outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle).
- **Should read as:** a pirate-ish chef
  - chef hat: tall puffy white 7-row puff with a shaded band row and one navy badge pixel
  - eyepatch (not a bruise): 2 x 2 black patch over his left eye (viewer's right in front, the far eye in the frames) with a strap pixel line up to the hat band; the other eye is open, 2 x 2 dark with a white highlight
  - curly moustache (not a pipe or cigarette): two symmetric curls under the nose in the front form; in the frames it lies flat on the face, ends inside the face edge with an upturned end, grin below
  - chef jacket: white, two vertical columns of navy button pixels, belly wider than the head
  - navy pants with a white vertical stripe on each leg, black boots
