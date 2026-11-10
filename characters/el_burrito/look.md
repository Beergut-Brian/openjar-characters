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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `stocky`
- **height:** 0.85 (short)
- **leg_scale:** 0.85
- **width / belly:** wide shoulders, flat belly
- **head:** `round`, size 1.0
- **hair:** `none` (mask)
- **headwear:** **new** `wrestler_mask` (full-head, gold, purple trim around eye and mouth openings)
- **top:** `tee`, gold, with **new** `star_emblem` (purple)
- **back:** **new** `cape`, purple (cosmetic, no collision)
- **bottoms:** **new** `shorts` (shared), purple
- **shoes:** **new** `wrestling_boots` (tall lace-up), white
- **gear:** none
- **pieces needed:** full-head mask, star emblem, cape, shorts, tall wrestling boots

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Gold head with purple ring pixels round the eyes; purple cape 2 px out behind; gold shirt with a purple star pixel; white boots 4 px tall.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
