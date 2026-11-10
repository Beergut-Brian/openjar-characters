# Sir Clank — look

## Kaden's sheet (verbatim)
Medium build, stands very straight. Silver cooking pot worn as a helmet with the handle sticking out the back, grey shirt with a yellow shield shape on the chest, dark blue pants, brown boots. Serious eyebrows, proud smile.

## Must survive every art style
- Silver cooking pot worn as a helmet, handle sticking out the back
- Grey shirt with a yellow shield shape on the chest
- Dark blue pants, brown boots
- Stands very straight; serious eyebrows, proud smile

## Silhouette
Very upright medium body with a cylindrical pot on the head and its handle sticking straight out the back: a T-shape at the top in side view.

## Face
Serious, thick eyebrows, proud closed-mouth smile, chin up. Expressions to build: proud (default), noble charge (mouth open, brows down), polite concern (brows up, small mouth).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- pot helmet: `#B8BEC6`
- pot handle: `#3A3D44` (accent)
- shirt: `#8A8F98`
- shield: `#F2C230` (accent)
- pants: `#23305E`
- boots: `#7A4E2A`

## Signature props
- Pot helmet (headwear: cylinder with a rim and one long handle out the back)
- Optional wooden spoon as a sword, gear in `hand_r`

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/sir_clank/jarling.json` (standard humanoid body, kit v2; costume pieces sit over the standard body, same skeleton, actions, slots and collision as every playable character).
- **body:** `regular`, height 1.05; posture `spine_lean` -3, `head_lean` -2 (stands very straight, chin up)
- **head:** `round` 1.0, skin `#F7CFAE`; `short` hair `#4A2F23`
- **headwear:** `pot_helmet` `#B8BEC6`, handle `#3A3D44`, `handle_len` **0.9** (shortened from the kit default 1.5 so the handle reads as a saucepan handle, not a pole; it sticks straight out the back at pot height, far from the mouth)
- **top:** `tee` `#8A8F98` + `emblem` shield `#F2C230`; **bottoms:** `pants` `#23305E`; **shoes:** `chunky_boots` `#7A4E2A`
- **face:** thick serious brows `#4A2F23`. Expressions: neutral = proud (`smile`), happy = `grin`, surprised = polite concern (brows up), determined = noble charge (`o`, brows down)
- **ref action:** `kick` frame 17, noble charge (`sir_clank_kick.png`)
- **Not built:** the wooden-spoon sword (optional on his sheet; no spoon held item in the kit yet)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/sir_clank.glb`: the 3D master
- `refs/jarling/sir_clank_turnaround.png`, `sir_clank_expressions.png`, `sir_clank_kick.png`
- `refs/jarling/sir_clank_side.png`, `sir_clank_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/sir_clank_pixel.png`, `sir_clank_frames.png` (+ `.json`), `sir_clank_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/sir_clank.py` (`sir_clank()`)

- **Height:** 31 px with the outline (the 3D is about 1.16 m with the pot, so no squeezing): pot 6 rows (light lid row, 4 body rows with a highlight stripe 2 px in from the left, darker rim row), face 8, torso 7,
  pants 5, boots 3. Medium build, standing dead straight (no lean in idle).
- **Palette:** pot `#B8BEC6` (highlight row `#DDE2E8`, rim row `#8D949E`), handle `#3A3D44`, skin `#F7CFAE` (+ `#D7AE8C`),
  hair and brows `#4A2F23`, eyes `#2A1E2C` with a `#FFFFFF` highlight, mouth `#8A3A3A`, shirt `#8A8F98` (back sleeve `#6C7179`),
  shield `#F2C230`, pants `#23305E` (back leg `#1A2447`), boots `#7A4E2A` (sole `#3F2814`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions).
- **Should read as:** a boy knight with a saucepan helmet (not a chef, not a bucket)
  - pot: flat-topped silver cylinder 14 px wide and 6 rows tall (lid, 4 body rows, rim), sitting down to the brows; brown hair
    shows under it at the sides and back
  - handle: dark 5 x 2 px bar straight out the back (left in the frames) at upper-pot height, rows 3-4, far from the mouth;
    a 1 px dark stub peeks out at the left of the pot in the front form
  - face: thick serious brows (row 8, 3 px), small 1 x 2 eyes, small closed proud smile
  - grey shirt with a yellow 3 x 4 shield (pointed bottom) on the chest, navy pants, brown boots
  - spoon sword not built (optional gear)
