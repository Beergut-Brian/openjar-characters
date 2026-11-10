# Lampy — look

## Kaden's sheet (verbatim)
Tall and thin. White miner's helmet with a big round headlamp, dusty teal overalls-style top, brown pants, dirt smudge on one cheek, grey boots. Wide curious eyes.

## Must survive every art style
- White miner's helmet with a big round headlamp
- Dusty teal overalls-style top
- Brown pants, grey boots
- Dirt smudge on one cheek
- Tall and thin; wide curious eyes

## Silhouette
Tall, thin column topped by a white helmet with a big round lamp sticking out front; long legs. Reads like a lit match.

## Face
Wide, round curious eyes, small mouth, a dirt smudge on one cheek (left). Expressions to build: curious (eyes wide), wonder gasp (mouth `o`, brows up), shy smile (eyes half-lidded, small smile).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- miner's helmet: `#F1F1EC`
- headlamp lens: `#FFE9A8` (accent)
- overalls top: `#3F8A99`
- pants: `#7A5536`
- cheek smudge: `#6B5A4A` (accent)
- boots: `#7B7F86`

## Signature props
- Headlamp on the helmet: a real light (emissive lens + a spot light in 3D; the light can be toggled by the game)
- A rock (gear, `hand_r`) for idle and win

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/lampy/jarling.json` (standard humanoid body, kit v2).
- **body:** `slim`, height 1.25, leg_scale 1.15, width 0.8 (tall and thin)
- **head:** `round` 1.0; skin `#EFBB90`; `short` hair `#7A4B2A` under the helmet
- **headwear:** `miner_helmet` `#F1F1EC`, `lamp_size` 1.3 (the "big round headlamp"): dark housing, emissive pale-yellow lens, and a
  **real spot light** in the glb (`lampy_headlamp`, 30 W, 55 degree cone, on the head bone; Godot imports it as a light a game can toggle)
- **face:** round eyes (scale 1.15 to 1.3), thin brows, `smile`; `smudge` `#6B5A4A` on one cheek. Expressions: neutral = curious,
  happy = shy closed-eye smile, surprised = wonder gasp (`o`, brows up), determined = set mouth
- **top:** `tee` `#3F8A99` with the `bib` pattern (`#35778A`) for the overalls look; **bottoms:** `pants` `#7A5536`; **shoes:** `chunky_boots` `#7B7F86`
- **ref action:** `cheer` frame 10, wonder face
- **Not built:** the rock (a held prop; waits for the held-item hold styles from the residents-d49 lane, not on `main` yet)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/lampy.glb`: the 3D master
- `refs/jarling/lampy_turnaround.png`, `lampy_expressions.png`, `lampy_cheer.png`
- `refs/jarling/lampy_side.png`, `lampy_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/lampy_pixel.png`, `lampy_frames.png` (+ `.json`), `lampy_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/lampy.py` (`lampy()`)

- **Height:** 32 px with the outline, the tallest of the Hillville four (the 3D is about 35 px at true scale, squeezed to the
  32 px frame): helmet dome 6 rows, brim 1, face 8 (with the chin row), torso 7, pants 5, boots 3. Narrow 8 px torso, long legs.
- **Palette:** helmet `#F1F1EC` (shade `#CFCFC8`), lamp housing `#3A3A46`, lens `#FFE9A8`, skin `#EFBB90` (+ `#CF9A70`),
  hair `#7A4B2A`, eyes `#2A1E2C` with a `#FFFFFF` highlight, mouth `#6A2232`, smudge `#6B5A4A`, top `#3F8A99`, bib and straps
  `#35778A` (also the back sleeve), pants `#7A5536` (back leg `#5E4129`), boots `#7B7F86` (sole `#4A4D55`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions; Lampy fills
  the frame, so the jump tucks the feet up 2 px instead of lifting the body).
- **Should read as:**
  - miner's helmet with a headlamp (not a cap badge, not a third eye): a white 6-row dome with a thin brim row and a shaded back;
    the lamp is a 4 x 4 dark housing with a 2 x 2 pale-yellow lens, centred high on the dome in the front form and sticking
    2 px out past the dome at the right in the frames
  - dirt smudge (not a moustache or a pipe): one `#6B5A4A` pixel on the outer cheek, level with or above the mouth and 3 px from it
  - wide curious eyes: 2 x 2 dark eyes with a white highlight pixel (the far eye 1 x 2 in the frames)
  - overalls-style top: a darker 4 px bib on the teal top with two strap pixels above its corners
  - tall and thin: 8 px torso, 2 px arms, 5-row brown legs into chunky grey boots with a dark sole
