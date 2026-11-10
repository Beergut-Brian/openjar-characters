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
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/professor_fizz.glb`: the 3D master
- `refs/jarling/professor_fizz_turnaround.png`, `professor_fizz_expressions.png`, `professor_fizz_cheer.png`
- `refs/jarling/professor_fizz_side.png`, `professor_fizz_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/professor_fizz_pixel.png`, `professor_fizz_frames.png` (+ `.json`), `professor_fizz_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/professor_fizz.py` (`professor_fizz()`)

- **Height:** 32 px with the outline (the 3D at true scale is 36 px with the hair, squeezed to the 32 px frame): hair spray
  5 rows + crown 1, head 10 (hair/goggles on the forehead rows 7-9, one skin row, brow row, eyes 2, grin 2, chin 1),
  lab coat 8, pants 3 (waist band + 2), sock 1, shoes 2.
- **Palette:** hair `#F7F7F2` (+ `#D9D9D2`), goggles brass `#B8862E` with lens `#9FD3E6` (+ glint `#E6F5FA`), skin `#F7CFAE`
  (+ `#DDAE8C`), scorched brow `#3A2E2A`, eyes `#2A1E2C` with a `#FFFFFF` catch-light, grin `#6A2232`, lab coat `#F4F5F2`
  (+ `#D5D8D6`), collar V and buttons `#7B3FB5`, pants `#5E2F94` (+ `#4A2478`), socks `#FFB627` (her left) / `#3FA7D6`
  (her right), shoes `#1B1B20` (+ toe glint `#44444E`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions; jump
  tucks the feet without lifting the body, since the hair already reaches row 1).
- **Should read as:**
  - mad-scientist hair straight up (not a crown, not a chef hat): 5 uneven spikes in the front form (4 in the frames), each a
    1 px tip over a 2 px shaft shaded on its left, tips on rows 1-4, the outer ones leaning out, 1 px gaps down to the crown;
    white hair also covers the back and side of the head down to the ear in the frames
  - round goggles pushed up on the forehead (not glasses, not a second pair of eyes): a brass row across the forehead with
    two 2 x 2 light-blue lenses in brass rings (front); one ringed lens at the front right with the brass strap row going
    back through the hair (frames); a full skin row between the goggles and the eyes
  - one scorched eyebrow: 3 dark `#3A2E2A` pixels with a 1 px break over her left eye only (image right in the front form,
    the near eye in the frames), no brow over the other eye
  - excited grin: a 4 px dark mouth row over a 2 px row, nothing poking out of it
  - white lab coat with a purple collar: white top with a purple V (skin inside), purple button pixels, long white sleeves
    with a grey shade, skin hands
  - mismatched socks: one sock row each, orange on her left leg and blue on her right, above black shoes (front form and
    every walk frame: near leg orange, far leg blue)
