# El Burrito — look

## Kaden's sheet (verbatim)
Short and wide. Gold luchador mask with purple trim covering the head, purple cape, gold shirt with a purple star, purple shorts, white wrestling boots. Eyes and big grin show through the mask.

## Must survive every art style
- Gold luchador-style mask with purple trim covering the head
- Purple cape
- Gold shirt with a purple star
- Purple shorts, white wrestling boots
- Short and wide; eyes and big grin show through the mask

## Silhouette
Short, wide block with a smooth masked head and a cape flaring behind: a wide triangle.

## Face
Eyes and a big grin through the mask openings. Expressions to build: showman grin (default), tragic (mouth wide open, brows up), pose-proud (eyes closed, grin).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- mask: `#E0B12E`
- mask trim + star: `#6B2FA8` (accent)
- cape: `#6B2FA8`
- shirt: `#E0B12E`
- shorts: `#6B2FA8`
- boots: `#F5F5F2`

## Signature props
- Full-head mask (headwear; eye and mouth openings, purple trim around them)
- Purple cape on the `back` slot (cloth or sway bones)

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/el_burrito/jarling.json` (standard humanoid body, kit v2; costume pieces sit over the standard body, same skeleton, actions, slots and collision as every playable character).
- **body:** `stocky`, height 0.85, leg_scale 0.85, width 1.3, belly 0.35 (short and wide)
- **head:** `round` 1.0, no ears, skin `#D99E6E` (shows only through the openings)
- **face extra:** `mask` `#E0B12E` with `#6B2FA8` trim round the eyes and mouth and a centre stripe (the whole head takes the mask colour)
- **top:** `tee` `#E0B12E` + `emblem` star `#6B2FA8`; **bottoms:** `shorts` `#6B2FA8`; **shoes:** `wrestling_boots` `#F5F5F2`, laces `#6B2FA8`
- **costume:** `cape` `#6B2FA8` with gold trim (back)
- **face:** Expressions: neutral = showman grin (`grin_top`), happy = pose-proud (eyes closed, grin), surprised = tragic (`o`, big eyes), determined = `grit`
- **ref action:** `cheer` frame 10, pose-proud (`el_burrito_cheer.png`)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/el_burrito.glb`: the 3D master
- `refs/jarling/el_burrito_turnaround.png`, `el_burrito_expressions.png`, `el_burrito_cheer.png`
- `refs/jarling/el_burrito_side.png`, `el_burrito_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/el_burrito_pixel.png`, `el_burrito_frames.png` (+ `.json`), `el_burrito_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/el_burrito.py` (`el_burrito()`)

- **Height:** 27 px with the outline (the 3D is about 1.02 m, 27 px at the 32 px = 1.2 m scale, no squeezing): round mask head 12 x 11 (clipped corners),
  torso 7, purple shorts 2-3, tall white boots 4-5. Short and wide: a 12 px torso, the widest of the batch.
- **Palette:** mask and shirt `#E0B12E` (shade `#BC9022`, a few shadow-side pixels only), purple trim, star, cape, shorts `#6B2FA8` (shade `#54238A`), skin `#D99E6E`
  (+ `#B97F52`), eyes `#2A1E2C`, mouth `#6A2232`, teeth and boots `#F5F5F2` (sole `#C9C9C2`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions; the jump
  and fall lift the body, tucking the cape).
- **Should read as:**
  - a masked wrestler with a cape (not a bald head, not a helmet, not a bee): the whole head is gold with no hair or ears; skin
    shows only inside the two eye openings and the mouth opening
  - 1 px purple rings round two separate eye openings (2 x 2: skin plus a dark eye, 2 px of gold between; the far eye a narrower ring in the frames) and the mouth (a big grin with teeth), and a 1 px purple forehead stripe, so the head stays mostly gold
  - gold shirt with a purple 5 px star on the chest, bare skin arms
  - purple cape hanging behind the shoulders to knee level with a gold hem pixel: flared out at the left in the frames, peeking out
    either side of the body below the arms in the front form
  - purple shorts and tall white boots with purple lace pixels
