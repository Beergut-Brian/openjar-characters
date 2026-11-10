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
- **headwear:** `hard_hat` `#F5C518`, `fit` 0.34, tilted back 12 degrees: it sits low, on her brows (they are hidden; the eyes are
  lowered with `eye_y` -0.13 so they stay visible, also from a camera above her. The example's `fit` 0.22 hid her eyes)
- **face:** round eyes, thick brows, `grin_top` (confident open smile). Expressions: happy = closed-eye grin, surprised = `o`, determined = grin, brows down
- **top:** `tee` `#F28A1E` with one white `hstripe` (hi-vis); **bottoms:** `pants` `#1F2D4F`; **shoes:** `chunky_boots` `#7A4E2A`
- **ref action:** `cheer` frame 10
- **Not the Gnome Foreman.** Dot is a clean-shaven human with a round yellow hard hat, dark bob, navy pants, 1.11 m to the hat top; the Gnome
  Foreman (resident) has a tall teal cone hat, a big white beard, suspenders and a clipboard (1.23 m to the cone tip, so they are about the same size). Side by side: `characters/batch2_foremen.png`.
  Their shirts are the same orange (Dot `#F28A1E`, the Gnome's vest `#F7932F`, ΔE2000 2.3) and both are called "Foreman": flagged for Kaden.
  Told apart by hat (round yellow vs teal cone), beard, and navy pants
- **Not built:** a clipboard in hand (held props wait for the held-item hold styles, not on `main` yet)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/foreman_dot.glb`: the 3D master
- `refs/jarling/foreman_dot_turnaround.png`, `foreman_dot_expressions.png`, `foreman_dot_cheer.png`
- `refs/jarling/foreman_dot_side.png`, `foreman_dot_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/foreman_dot_pixel.png`, `foreman_dot_frames.png` (+ `.json`), `foreman_dot_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/foreman_dot.py` (`foreman_dot()`)

- **Height:** 28 px with the outline (0.85 m stocky body plus the hat, traced from `foreman_dot_side_sprite.png`): hard hat 5 rows
  (ridge row, 3 dome rows, brim row on the brow line), face 7, torso 7, pants 3, boots 4. Short and stocky: a 13 px torso.
- **Palette:** hard hat `#F5C518` (ridge and highlight `#FFE066`, shade `#C99A0E`), bob `#4A2F23`, skin `#D99E6E` (+ `#B97F55`),
  eyes `#2A1E2C`, mouth `#6A2232` with a `#FFFFFF` top row, tee `#F28A1E` (shade `#D0700F`), hi-vis stripe `#FFFFFF`, pants
  `#1F2D4F`, boots `#7A4E2A` (sole `#4A3020`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions).
- **Should read as:**
  - a yellow hard hat sitting low (not a gnome cone, not a cap): a round dome with a pale centre ridge column, shaded at the back,
    its brim row directly on the brow line with the eyes just under it, the brim 2 px past the face at the right in the frames
  - a human site lead, not the Gnome Foreman (`residents.py` `foreman()`): clean chin and jaw, dark bob at the sides and back down
    to the jaw, round hat, no clipboard, no whistle
  - confident open smile: a 4 px white row over a 4 px dark row and a 2 px dark row, nothing poking out of it
  - hi-vis tee: orange with exactly one full-width white stripe row across the chest
  - chunky boots: brown, 5-6 px long, 3 rows plus a dark sole
