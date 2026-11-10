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
- **headwear:** `top_hat` `#1C1C22` with a gold band `#D9B23A`, `height` 1.85, `scale` 1.12. The hat rises 0.53 m above his 0.88 m head top, 38% of his
  1.41 m silhouette (the example's 2.3 was 42% of 1.53 m), and its crown at 1.41 m is no higher than the tallest playable bare head (1.43 m), so his silhouette stays
  inside the playable range. The sheet example's 2.3 put the crown at 1.53 m, taller than Big Tiny
- **face:** button eyes, arched raised brows, half lids, `set` mouth (great importance). Expressions: happy = small smile,
  surprised = flustered (`o`, eyes wide), determined = set mouth, brows down
- **top:** `long` `#A8CFF0` with a gold `sash` `#D9B23A`; **bottoms:** `pants` `#7D8088`; **shoes:** `dress` `#15151A`
- **ref action:** `kick` frame 17
- **Not built:** ribbon scissors (a held prop; waits for the held-item hold styles, not on `main` yet)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/mayor_pip.glb`: the 3D master
- `refs/jarling/mayor_pip_turnaround.png`, `mayor_pip_expressions.png`, `mayor_pip_kick.png`
- `refs/jarling/mayor_pip_side.png`, `mayor_pip_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/mayor_pip_pixel.png`, `mayor_pip_frames.png` (+ `.json`), `mayor_pip_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/mayor_pip.py` (`mayor_pip()`)

- **Height:** 32 px with the outline, but the smallest body (0.8 m body under the 1.85x top hat): top hat 13 rows (crown 10,
  gold band 2, brim 1), head 7 (10 px wide), then chin to soles 10: shirt 5, pants 3, shoes 2. The shirt is 6 px wide in the front form.
- **Palette:** top hat `#1C1C22` (highlight column `#3A3A46`), band and sash `#D9B23A`, hair and brows `#4A2F23`, skin `#EFBB90`
  (+ `#CF9A70`), eyes `#2A1E2C`, mouth `#6A2232`, shirt `#A8CFF0` (shade `#86B4DA`, also both sleeves in the frames), pants
  `#7D8088`, shoes `#15151A` (highlight `#4A4A55`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (21, 25) idle: The Hill's dig hand positions moved 1 px back
  and 4 rows down for the low shoulders, the manifest carries the idle hand; no jump lift, the hat fills the frame top). The ride
  frame (`jarling_frames.sheet`, top 14 rows of idle0) is almost all hat for Pip: left as it is.
- **Should read as:**
  - a very small person under a huge top hat (not a chimney, not a tall dark hairdo): an 8 px crown, 10 rows tall, with one
    `#3A3A46` highlight column so it reads as a cylinder, a 2-row gold band at its base and a 12 px brim row over the brown hair
  - stern little face: a hair-coloured brow pixel pair over one dark pixel per eye (half-lidded), a flat 2 px mouth
  - mayoral sash: a 2 px gold diagonal across the light-blue shirt, shoulder to hip
  - small black dress shoes with one grey highlight pixel each
