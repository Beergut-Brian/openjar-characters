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

### Jarling 3D (master)
Built 2026-11-10 from `characters/mayor_pip/jarling.json` (standard humanoid body, kit v2).
- **body:** `slim`, height 0.8, leg_scale 0.8, width 0.9: the bottom of the playable range (the smallest playable Jarling, 0.88 m to the top of his head)
- **head:** `round` 1.0; skin `#EFBB90`; `short` hair `#4A2F23`
- **headwear:** `top_hat` `#1C1C22` with a gold band `#D9B23A`, `height` 1.85, `scale` 1.12. The hat is about 0.53 m tall, 46% of his own
  height ("nearly half"), and its crown is at 1.41 m: no higher than the tallest playable bare head (1.43 m), so his silhouette stays
  inside the playable range. The sheet example's 2.3 put the crown at 1.53 m, taller than Big Tiny
- **face:** button eyes, arched raised brows, half lids, `set` mouth (great importance). Expressions: happy = small smile,
  surprised = flustered (`o`, eyes wide), determined = set mouth, brows down
- **top:** `long` `#A8CFF0` with a gold `sash` `#D9B23A`; **bottoms:** `pants` `#7D8088`; **shoes:** `dress` `#15151A`
- **ref action:** `kick` frame 17
- **Not built:** ribbon scissors (a held prop; waits for the held-item hold styles, not on `main` yet)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. About 18 px body plus a 12 to 14 px black top hat to reach the 32 px frame: the hat is the sprite. One gold pixel row for the band, a diagonal gold sash line.

## Refs
- `refs/jarling/mayor_pip.glb`: the 3D master
- `refs/jarling/mayor_pip_turnaround.png`, `mayor_pip_expressions.png`, `mayor_pip_kick.png`
- `refs/jarling/mayor_pip_side.png`, `mayor_pip_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/mayor_pip_pixel.png`, `mayor_pip_frames.png` (+ `.json`), `mayor_pip_pixel_sheet.png`: The Hill pixel form
