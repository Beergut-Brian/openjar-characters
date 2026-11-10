# Foreman Dot — look

## Kaden's sheet (verbatim)
Short and stocky. Yellow hard hat sitting slightly too low, orange shirt with one white hi-vis stripe, navy pants, chunky brown boots. Confident open-mouth smile.

## Must survive every art style
- Yellow hard hat sitting slightly too low, brim nearly over the eyes
- Orange shirt with one white hi-vis stripe across the chest
- Navy pants, chunky brown boots
- Short and stocky; confident open-mouth smile under the brim

## Silhouette
Short, wide stocky block with a low, dome hard hat that sits down over the brow line; chunky boots widen the base. A squat triangle-on-a-dome outline.

## Face
Eyes half under the brim, big open-mouth smile. Expressions to build: confident (default open grin), barking an order (mouth wide, brows down), delighted (eyes arc, grin), startled (worm; eyes wide, mouth `o`).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- hard hat: `#F5C518`
- shirt: `#F28A1E`
- hi-vis stripe: `#F4F4F0` (accent)
- pants: `#1F2D4F`
- boots: `#7A4E2A`

## Signature props
- Hard hat (sits low; can be nudged up)
- Optional clipboard in `hand_l` for cameos (gear, not part of the body)

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/foreman_dot/jarling.json` (standard humanoid body, kit v2).
- **body:** `stocky`, height 0.85, leg_scale 0.85, width 1.1 (short and stocky)
- **head:** `round` 1.0; skin `#D99E6E`; `bob` hair `#4A2F23`
- **headwear:** `hard_hat` `#F5C518`, `fit` 0.27, tilted back 12 degrees: it sits low, just above the brows (the first try at `fit` 0.22
  hid her eyes from a camera above her, so it came up a little; eyes lowered with `eye_y` -0.1)
- **face:** round eyes, thick brows, `grin_top` (confident open smile). Expressions: happy = closed-eye grin, surprised = `o`, determined = grin, brows down
- **top:** `tee` `#F28A1E` with one white `hstripe` (hi-vis); **bottoms:** `pants` `#1F2D4F`; **shoes:** `chunky_boots` `#7A4E2A`
- **ref action:** `cheer` frame 10
- **Not the Gnome Foreman.** Dot is a clean-shaven human with a round yellow hard hat, dark bob, navy pants, 0.99 m to the hat top; the Gnome
  Foreman (resident) is about half her height with a teal cone hat and a white beard. Side by side: `characters/batch2_foremen.png`.
  Both wear orange and both are called "Foreman": flagged for Kaden
- **Not built:** a clipboard in hand (held props wait for the held-item hold styles, not on `main` yet)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. The hard hat is a 3-px-tall yellow dome with the brim one px above the eye line; the white stripe is a single row across the orange shirt. Must read at 16 px: yellow dome + orange block.

## Refs
- `refs/jarling/foreman_dot.glb`: the 3D master
- `refs/jarling/foreman_dot_turnaround.png`, `foreman_dot_expressions.png`, `foreman_dot_cheer.png`
- `refs/jarling/foreman_dot_side.png`, `foreman_dot_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/foreman_dot_pixel.png`, `foreman_dot_frames.png` (+ `.json`), `foreman_dot_pixel_sheet.png`: The Hill pixel form
