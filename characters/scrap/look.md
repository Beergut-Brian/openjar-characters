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
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Colander a silver dome with two darker hole pixels and one handle pixel each side. Shoes: one orange pixel pair, one purple pixel pair. About 26 px tall in the 32 px frame (kid).

## Refs
- `refs/jarling/scrap.glb`: the 3D master
- `refs/jarling/scrap_turnaround.png`, `scrap_expressions.png`, `scrap_kick.png`
- `refs/jarling/scrap_side.png`, `scrap_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/scrap_pixel.png`, `scrap_frames.png` (+ `.json`), `scrap_pixel_sheet.png`: The Hill pixel form
