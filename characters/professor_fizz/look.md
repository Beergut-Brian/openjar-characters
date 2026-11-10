# Professor Fizz — look

## Kaden's sheet (verbatim)
Medium build. Wild white hair standing straight up, round goggles on her forehead, white lab-coat top with a purple collar, purple pants, mismatched socks showing above black shoes. One eyebrow is a scorch mark.

## Must survive every art style
- Wild white hair standing straight up
- Round goggles on the forehead
- White lab-coat top with a purple collar
- Purple pants; mismatched socks showing above black shoes
- One eyebrow is a scorch mark

## Silhouette
Medium body under a tall spray of upright white hair, goggles as a band across the forehead, lab-coat flare at the hips. The hair is the outline.

## Face
Wide bright eyes; one normal eyebrow and one scorched (dark, jagged) eyebrow. Expressions to build: excited (open grin), idea strike (eyes wide, mouth `o`, finger up), mid-thought blank (eyes up, flat mouth).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- hair: `#F7F7F2`
- goggle rims: `#B8862E` (accent)
- goggle lens: `#9FD3E6` (accent)
- lab coat: `#F4F5F2`
- collar: `#7B3FB5` (accent)
- pants: `#5E2F94`
- sock L: `#FFB627` (accent)
- sock R: `#3FA7D6` (accent)
- shoes: `#1B1B20`
- scorch brow: `#3A2E2A` (accent)

## Signature props
- Round goggles (headwear, on forehead)
- Optional zap gun or notebook as gear in `hand_r` for cameos

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/professor_fizz/jarling.json` (standard humanoid body, kit v2).
- **body:** `regular`, height 1.0
- **head:** `round` 1.0; skin `#F7CFAE`; hair preset `upright` `#F7F7F2` (a spray of white spikes straight up: the outline)
- **goggles:** costume piece `goggles` (round, brass rims `#B8862E`, lens `#9FD3E6`) on the forehead at `height` 0.52, clear of the brows
- **face:** wide eyes, `grin`; her left brow is the `scorch_brow` extra `#3A2E2A` (jagged, with soot), the other a normal grey brow.
  Expressions: neutral = excited grin, happy = closed-eye grin, surprised = idea strike (`o`), determined = mid-thought blank (`flat`)
- **top:** `long` `#F4F5F2` with `collar` and `buttons` in `#7B3FB5` (a painted lab coat: no separate hem below the waist)
- **bottoms:** `pants` `#5E2F94`; **shoes:** `dress` `#1B1B20` with mismatched socks (left `#FFB627`, right `#3FA7D6`, `height` 0.3) worn
  over the pants cuffs so they show above the shoes
- **ref action:** `cheer` frame 10 ("For SCIENCE!")
- **Not built:** a lab coat with a real hem; zap gun / notebook (held props; wait for the held-item hold styles, not on `main` yet)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Hair a 5-px-tall white spray above the head; goggles a brass row with two light-blue dots. Lab coat white with a purple collar pixel pair; socks one orange and one blue pixel above the black shoes.

## Refs
- `refs/jarling/professor_fizz.glb`: the 3D master
- `refs/jarling/professor_fizz_turnaround.png`, `professor_fizz_expressions.png`, `professor_fizz_cheer.png`
- `refs/jarling/professor_fizz_side.png`, `professor_fizz_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/professor_fizz_pixel.png`, `professor_fizz_frames.png` (+ `.json`), `professor_fizz_pixel_sheet.png`: The Hill pixel form
