# Bloom — look

## Kaden's sheet (verbatim)
Short with a soft, rounded build. Huge floppy straw sun hat with one flower on the brim, pink shirt, denim-blue skirt with muddy knees below it, purple garden clogs. Rosy cheeks, gentle smile.

## Must survive every art style
- Huge floppy straw sun hat with one flower on the brim
- Pink shirt
- Denim-blue skirt with muddy knees below it
- Purple garden clogs
- Short, soft, rounded; rosy cheeks, gentle smile

## Silhouette
Short soft body under a very wide floppy hat brim (wider than the shoulders), skirt, chunky clogs. A mushroom outline.

## Face
Rosy cheeks, gentle smile, soft eyes. Expressions to build: gentle smile (default), encouraging (eyes arcs, open smile), humming (eyes closed, small `o`).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- straw sun hat: `#E3C27A`
- flower petals: `#8E9BF0` (accent)
- flower centre: `#FFD23F` (accent)
- shirt: `#F7A8CB`
- skirt: `#5B7FB8`
- mud: `#6B4A33` (accent)
- clogs: `#8A4FC4`
- cheeks: `#F4A3B4` (accent)

## Signature props
- Straw sun hat with one flower (periwinkle petals, yellow centre) on the brim
- Optional small watering can as gear in `hand_r`

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/bloom/jarling.json` (standard humanoid body, kit v2).
- **body:** `puffy`, height 0.85, leg_scale 0.85, width 1.1, belly 0.2 (short and soft; about 1.1 m with the hat)
- **head:** `round` 1.0; skin `#BF8150`; `bob` hair `#3A2418`
- **headwear:** `sun_hat` straw `#E3C27A`, pink band `#F7A8CB`, brim 1.3, raised (`fit` 0.55) so the brim clears the eyes; one flower on
  the band at the front right: periwinkle petals `#8E9BF0`, yellow centre `#FFD23F`
- **face:** round eyes, soft brows, `smile`; rosy cheeks `#F4A3B4` (`blush_color`, blush 0.9). Expressions: neutral = gentle smile,
  encouraging = eye arcs and an open smile, humming = eyes closed, small `o`
- **top:** `tee` `#F7A8CB`; **bottoms:** `shorts` `#5B7FB8` under the skirt; **skirt:** costume piece `long_skirt` `#5B7FB8`, length 0.22,
  with mud `#6B4A33` on the knees below the hem (the kit's mud is a decal pair on the legs); **shoes:** `clogs` `#8A4FC4`
- **gear:** `watering_can` in `hand_r` (`one_hand_low`) for the ref pose; `ref_action` is idle frame 1 holding it
- **Kit limits:** the skirt is the generic `long_skirt` costume piece (no dedicated knee skirt); the brim is a wavy sculpted piece, not a soft body

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/bloom.glb`: the 3D master
- `refs/jarling/bloom_turnaround.png`, `bloom_expressions.png`, `bloom_idle.png` (holding the watering can), `bloom_hold.png` (grip check, front and 3/4)
- `refs/jarling/bloom_side.png`, `bloom_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/bloom_pixel.png`, `bloom_frames.png` (+ `.json`), `bloom_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/bloom.py` (`bloom()`)

- **Height:** 30 px with the outline (the 3D is about 29.5 px at true scale): hat crown 3 rows (the last is the pink band), brim 2,
  face 8 (with the chin row), tee 5, skirt 5, bare legs 4, clogs 3. Body 10 px wide, skirt 12.
- **Palette:** straw `#E3C27A` (shade `#C2A15C`), band and tee `#F7A8CB` (shade `#D98BAE`), petals `#8E9BF0`, flower centre `#FFD23F`,
  skin `#BF8150` (+ `#9E6538`), hair `#3A2418`, cheeks `#F4A3B4`, eyes `#2A1E2C` with a `#FFFFFF` highlight, mouth `#6A2232`,
  skirt `#5B7FB8` (shade `#48689A`), mud `#6B4A33`, clogs `#8A4FC4` (sole `#6B3A9C`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride, sleep0-1
  (three-quarter view facing right, feet on row 30, hand at (22, 21) idle; the hem sways 1 px in the walk). No watering can.
- **Should read as:**
  - huge floppy straw sun hat: a 14 px brim, 2 px wider than the 10 px body on each side, over a 3-row crown with a pink band
  - one flower on the brim: a 2 x 2 patch of three periwinkle pixels and one yellow centre pixel, on the band at the front
  - pink shirt over a denim-blue skirt; two brown mud pixels, one on each bare knee below the hem
  - purple garden clogs: 4 px wide, 2 rows plus a darker sole
  - short and soft: rosy cheek pixels and a small smile
