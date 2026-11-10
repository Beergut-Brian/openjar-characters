# Granny Gravel — look

## Kaden's sheet (verbatim)
The white-bun grandma body type. Safety goggles pushed up into her hair, lavender cardigan-style top, long grey skirt, bright yellow sneakers. Tiny smile, raised eyebrows.

## Must survive every art style
- White bun (the grandma hair)
- Safety goggles pushed up into the hair
- Lavender cardigan-style top
- Long grey skirt
- Bright yellow sneakers

## Silhouette
Round head with a tall white bun on top and goggles as a band across it, a soft cardigan torso and a long skirt that hides the legs down to bright sneakers: a bell shape topped with a bun.

## Face
Tiny smile, raised eyebrows. Expressions to build: sweet (tiny smile, brows up), gleeful driving cackle (mouth wide, eyes narrowed), innocent denial (eyes closed, little smile).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- hair (bun): `#F2F0EA`
- goggle frame: `#6E7681` (accent)
- goggle lens: `#A9D6E5` (accent)
- cardigan top: `#B9A3D9`
- skirt: `#8C8F96`
- sneakers: `#FFD93B`

## Signature props
- Safety goggles (headwear, pushed up; can be pulled down)
- Imaginary cookies are mimed: no prop

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/granny_gravel/jarling.json` (standard humanoid body, kit v2).
- **body:** `regular`, height 0.9, leg_scale 0.85
- **head:** `round` 1.0; skin `#F7CFAE`; hair preset `top_bun` `#F2F0EA` (white, bun on the crown)
- **goggles:** costume piece `goggles`, `safety` style, frame `#4A4F5A`, on the forehead at `height` 0.56 and `size` 0.85: pushed up into the
  white hair under the bun, well clear of the eyes and mouth
- **face:** button eyes, thin raised brows, tiny `smile`. Expressions: happy = closed-eye grin, surprised = `o`, determined = the
  behind-the-wheel cackle (open grin, brows down)
- **top:** `long` `#B9A3D9` with a `collar` (`#9C84C4`) and one row of `buttons` (cardigan); **bottoms:** `long_skirt` `#8C8F96` (length 0.85)
  over same-colour pants; **shoes:** `sneaker` `#FFD93B`
- **ref action:** `cheer` frame 10

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/granny_gravel.glb`: the 3D master
- `refs/jarling/granny_gravel_turnaround.png`, `granny_gravel_expressions.png`, `granny_gravel_cheer.png`
- `refs/jarling/granny_gravel_side.png`, `granny_gravel_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/granny_gravel_pixel.png`, `granny_gravel_frames.png` (+ `.json`), `granny_gravel_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/granny_gravel.py` (`granny_gravel()`)

- **Height:** 30 px with the outline and the bun (traced from `granny_gravel_side_sprite.png`): bun 3 rows sitting right
  on the hair, hair dome 4 (goggles in its lower 3 rows), face 6 (two skin rows with the brows, dot eyes, cheeks/smile,
  chin), cardigan 6, A-line skirt 7, sneakers 2.
- **Palette:** hair `#F2F0EA` (+ `#CFCBC2`), goggles frame `#4A4F5A` with lenses `#9FD8F0` (+ glint `#D8F1FA`), skin `#F7CFAE`
  (+ `#DDAE8C`), brows `#B9B4AE`, eyes `#2A1E2C`, cheeks `#F2A9A0`, smile `#6A2232`, cardigan `#B9A3D9` (+ `#9C84C4`),
  button line `#F2F0EA`, skirt `#8C8F96` (+ `#74777E`), sneakers `#FFD93B` (sole `#D9B21E`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions). The
  skirt hides the legs: only the sneakers step (a lifted foot shows just its sole row under the hem) and the hem band
  sways 1 px (walk0 +1, walk2 -1, side1 +1, down1 -1).
- **Should read as:**
  - a round white bun on the crown (not a hat tip, not a spire): rows of 3, 4, 4 px (flat-ish top, one top corner cut),
    sitting directly on a flat-topped hair dome, one `#CFCBC2` shade pixel low on one side; one px back from centre in
    the frames
  - safety goggles pushed up into the hair (not glasses over the eyes, not a hairband): a dark `#4A4F5A` strap row with two
    4 x 3 dark frames each holding a 2 x 2 light-blue lens, on the hairline with white hair above and at the sides, two skin
    rows (brows in the upper one) between them and the eyes; in the frames the strap runs back through the white hair
  - a grandma's face: 1 px dot eyes, a light grey brow pixel raised one row above each, a rosy cheek pixel each side,
    a tiny 3-4 px smile, nothing poking out of it
  - lavender cardigan: long lavender sleeves with skin hands, a shaded V neck and a white centre button line
  - long grey A-line skirt: waist to just above the shoes, 1 px wider each side for 2 rows then 2 px for the 3-row hem
    band, dark fold pixels, a darker hem row
  - loud yellow sneakers: 4 px yellow with a darker sole row, peeking out under the hem
