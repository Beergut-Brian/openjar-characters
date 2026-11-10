# Scrap — look

## Kaden's sheet (verbatim)
Small kid body type. Metal colander worn as a helmet, patched yellow shirt, blue shorts, one orange shoe and one purple shoe. Gap-toothed grin, freckles.

## Must survive every art style
- Metal colander worn as a helmet
- Patched yellow shirt
- Blue shorts
- One orange shoe and one purple shoe
- Gap-toothed grin, freckles; small kid body

## Silhouette
Small kid body with a holey domed colander on top (small handles at the sides), shorts and two different shoes.

## Face
Gap-toothed grin, freckles across the nose. Expressions to build: cheeky grin (gap tooth), dibs shout (mouth wide), suspicious squint at junk.

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- colander helmet: `#B9BEC4`
- shirt: `#F2C230`
- patch tan: `#D9B38C` (accent)
- patch blue: `#5A8FD0` (accent)
- shorts: `#3E6DB5`
- shoe L: `#F28C28`
- shoe R: `#8A4FC4`
- freckles: `#C8936A` (accent)

## Signature props
- Colander helmet (headwear: dome with holes and two little side handles)
- A bit of junk as gear in `hand_r` (spring, gear wheel) for idle and win

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/scrap/jarling.json` (standard humanoid body, kit v2).
- **body:** `regular`, height 0.85, leg_scale 0.85 (small kid)
- **head:** `round` 1.05; skin `#F0BE94`; `short` hair `#B5651D`
- **headwear:** `colander` `#B9BEC4` (upturned bowl with holes, rim, two side handles and three little feet on top)
- **face:** `grin_gap` (gap-toothed), `freckles_big`. Expressions: happy = closed-eye grin, surprised = `o`, determined = scrappy grin, brows down
- **top:** `tee` `#F2C230` with `patches` (`#E8873D`, `#5B8FD6`); **bottoms:** `shorts` `#3E6DB5`
- **shoes:** `sneaker`, left `#F28C28` (orange), right `#8A4FC4` (purple). Kit fix: per-side shoe colours now get their own material
  (`avatar/kit/jarling_kit.py`; before, both shoes took the first colour)
- **ref action:** `kick` frame 17, determined face

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/scrap.glb`: the 3D master
- `refs/jarling/scrap_turnaround.png`, `scrap_expressions.png`, `scrap_kick.png`
- `refs/jarling/scrap_side.png`, `scrap_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/scrap_pixel.png`, `scrap_frames.png` (+ `.json`), `scrap_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/scrap.py` (`scrap()`)

- **Height:** 29 px with the outline (a small kid with a big head, traced from `scrap_side_sprite.png`): colander feet 1 row,
  bowl 4, rim 1, head 8, tee 6, shorts 2, bare legs 3, shoes 2. The head (13-14 px) is wider than the 10 px tee.
- **Palette:** colander `#B9BEC4` (+ light `#DDE1E5`, shade `#8E949B`), holes `#3A3F48`, hair `#B5651D`, skin `#F0BE94`
  (+ `#D29D74`), freckles `#C98A5E`, eyes `#2A1E2C` with a `#FFFFFF` catch-light, mouth `#6A2232` with teeth `#FFFFFF`,
  tee `#F2C230` (+ `#D4A51E`), patches `#E8873D` / `#5B8FD6`, shorts `#3E6DB5` (+ `#325A96`), shoes `#F28C28` (his left) /
  `#8A4FC4` (his right), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions; kid legs
  2 px wide).
- **Should read as:**
  - a kitchen colander worn as a helmet (not a hard hat, not a polka-dot cap): an upturned grey bowl with a flat-ish top
    (narrowing 2 px per side over 3 rows), two 1 px shaded feet on the top, staggered dark hole dots on two rows (3 over 4),
    a light rim row 1 px wider than the head each side and a flat 2 px darker handle nub past each rim end (only the back
    one in the frames)
  - auburn hair under the rim: at both sides and a short fringe (front), the back of the head and a fringe (frames)
  - gap-toothed grin: a dark mouth with a white tooth row broken by one dark gap pixel, a dark row below, nothing poking out
  - freckles: two `#C98A5E` pixels on each cheek
  - patched yellow tee: a 2 x 2 orange patch and a 2 px blue patch on the tee, short yellow sleeves, skin arms
  - odd shoes: orange on his left foot (image right in the front form), purple on his right; in every frame the near foot
    is orange and the far foot purple
