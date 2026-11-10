# Mayor Pip — look

## Kaden's sheet (verbatim)
The smallest body type. Oversized black top hat that is nearly half his height, light blue shirt with a gold sash, grey pants, shiny black shoes. Always carries a look of great importance.

## Must survive every art style
- Oversized black top hat, nearly half his height
- Light blue shirt with a gold sash
- Grey pants, shiny black shoes
- The smallest body; a look of great importance

## Silhouette
Tiny body with a huge tall black top hat: nearly a 1:1 hat-to-body column. Unmistakable in outline.

## Face
Brows raised in importance, small pursed mouth. Expressions to build: important (chin up, small set mouth), flustered (eyes wide, mouth `o`, hat askew), proud declaration (open mouth, eyes closed).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- top hat: `#1C1C22`
- hat band: `#D4A82A` (accent)
- shirt: `#A8CFF0`
- sash: `#D4A82A` (accent)
- pants: `#7D8088`
- shoes: `#15151A`

## Signature props
- Top hat (the silhouette; headwear)
- Gold sash (costume piece over the shirt)
- Ribbon scissors are mimed for the generic set; a pair may be gear in `hand_r` for cameos

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `slim`
- **height:** 0.8 (the minimum; Kaden's "smallest body type")
- **leg_scale:** 0.8
- **width / belly:** narrow, no belly
- **head:** `round`, size 1.0
- **hair:** `none` under the hat
- **headwear:** **new** `top_hat`, tall: crown height about 0.8x the body's torso+legs so the hat reads as nearly half his height; gold band. Hat is visual only: it must not change collision
- **top:** `shirt` (collared), light blue, with **new** costume piece `sash` (gold diagonal)
- **bottoms:** `pants`, grey
- **shoes:** **new** `dress_shoes`, glossy black
- **gear:** optional ribbon scissors in `hand_r`
- **pieces needed:** top_hat (tall), sash, dress_shoes, collared shirt, ribbon scissors (gear)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. About 18 px body plus a 12 to 14 px black top hat to reach the 32 px frame: the hat is the sprite. One gold pixel row for the band, a diagonal gold sash line.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
