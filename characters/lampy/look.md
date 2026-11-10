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
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Helmet a white dome with a 2x2 pale-yellow lamp pixel at the front; in dark areas a light cone sprite in front of the lamp. Smudge one brown pixel on the cheek. Tallest of the Hillville four at 32 px.

## Refs
- `refs/jarling/lampy.glb`: the 3D master
- `refs/jarling/lampy_turnaround.png`, `lampy_expressions.png`, `lampy_cheer.png`
- `refs/jarling/lampy_side.png`, `lampy_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/lampy_pixel.png`, `lampy_frames.png` (+ `.json`), `lampy_pixel_sheet.png`: The Hill pixel form
