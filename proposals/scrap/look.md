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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `regular` (kid proportions come from height and legs)
- **height:** 0.85
- **leg_scale:** 0.85
- **width / belly:** small, no belly
- **head:** `round`, size 1.05 (kid look)
- **hair:** `short` peeking out under the colander
- **headwear:** **new** `colander` (metal dome with a hole pattern, two side handles)
- **top:** `tee`, yellow, with **new** `patches` costume piece (two patches: tan and blue)
- **bottoms:** **new** `shorts`, blue
- **shoes:** **new** `sneakers` (shared) with per-foot colour (left orange, right purple)
- **face extra:** freckles decal; gap-tooth mouth (`grin_gap`, new)
- **gear:** junk bit in `hand_r` (optional)
- **pieces needed:** colander, shirt patches, shorts, sneakers with per-foot colour, freckles decal, gap-tooth grin

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Colander a silver dome with two darker hole pixels and one handle pixel each side. Shoes: one orange pixel pair, one purple pixel pair. About 26 px tall in the 32 px frame (kid).

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
