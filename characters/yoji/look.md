# Yoji — look

## Kaden's sheet (verbatim, 2026-11-10)
- Hair: "short hair", and a hat on top
- Hat: "a cowboy hat"
- Shirt: "football jersey", "number 55", team "The Champions"
- Pants: none, "just underwear on"
- Shoes: "black and blue" basketball shoes (ours are unbranded original high-tops, no logos)
- Face: yes

## Must survive every art style
- Tan cowboy hat: wide brim curled up at the sides, pinched crown, worn level on top of short brown hair
- Navy football jersey with shoulder pads, gold trim, a big white **55** front and back
- White boxer shorts with small navy stars and a waistband: clearly underwear, as a gag (never rude)
- Bare legs
- Black-and-blue high-top basketball shoes with white soles, no logos
- A huge happy grin

## Silhouette
A wide-brimmed hat on a big round head, broad padded shoulders over a stocky torso, a short puff of boxers, then bare legs down to chunky high-tops. Wide at the top (brim + pads), narrow in the middle (bare legs), chunky at the feet.

## Face
Big friendly grin, thick brows, round bright eyes. Expressions: neutral = grin; happy = arc eyes, open yell-grin (touchdown!); surprised = round "o"; determined = game face, brows down, set grin.

## Fixed colours
Checked against the player colours with CIEDE2000 (`avatar/kit/colour_rule.py`, `tools/check_colours.py`): every outfit main colour is at least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`, skin and hair at least 10. Lowest: hair `#6B4A2E` 27.7 from P2. No adjustment was needed; all values are the producer's starting picks from the sheet.

| Part | Colour | ΔE00 vs P1 / P2 |
| --- | --- | --- |
| cowboy hat | `#C8955A` | 38.0 / 29.3 |
| hat band | `#5A3A22` (accent) | 56.8 / 30.2 |
| hair | `#6B4A2E` | 51.1 / 27.7 |
| skin | `#E8B48A` | 40.2 / 30.9 |
| jersey | `#1F3A6B` navy | 65.2 / 45.7 |
| jersey trim | `#F2B632` gold (accent) | 36.8 / 42.8 |
| number 55, lettering | `#F7F7F5` (accent) | 33.4 / 44.2 |
| boxer shorts | `#F7F7F5` with stars `#1F3A6B` | 33.4 / 44.2 |
| high-tops | `#1A1A1E` black, panels `#2A6FD6` blue, soles + laces `#F7F7F5` | 61.0 / 43.8, 59.6 / 44.9 |

## Lettering
"55" (front and back) and "CHAMPIONS" (upper back) live only in the 3D jersey texture and the pixel art, never as gameplay UI text. The team name is "The Champions"; only "CHAMPIONS" fits on the back.

## Signature props
- The cowboy hat. Also available as head-slot gear `avatar/gear/cowboy_hat` for any Jarling.

## Per-technique notes

### Jarling 3D
Built 2026-11-10 from `characters/yoji/jarling.json` (standard humanoid body, kit v2).
- **body:** `stocky`, height 1.0, leg_scale 1.0, width 1.15, belly 0.25
- **head:** `round`, skin `#E8B48A`; `short` hair `#6B4A2E` tucked under the hat (shows at the sides and back)
- **headwear:** new kit piece `cowboy_hat` (`avatar/kit/pieces_headwear.py`): tan `#C8955A`, band `#5A3A22`, brim_width 0.8, crown_height 1.1,
  fit 0.45 (brim sits 0.45 R above the head centre, about 1.8 R wide each side), tilt 0 (level). Wide brim curled up at the sides,
  cattleman crown with front pinches and a centre crease. It is the `headwear` body part. The same shape is head-slot gear
  `avatar/gear/cowboy_hat` (replaces `headwear`), so any Jarling can wear it.
- **top:** `tee` navy `#1F3A6B` with the new `jersey` pattern (gold `#F2B632` collar and outline, white `#F7F7F5` "55" front and back,
  "CHAMPIONS" across the upper back; letters drawn in code from a 5x7 block font), plus the new `shoulder_pads` costume piece
  (navy, gold sleeve stripes, white hem)
- **bottoms:** new `boxers` style (shorter and puffier than shorts, gold waistband) white `#F7F7F5` with `stars` navy `#1F3A6B`
  (count 34, size 2.0); bare legs below
- **shoes:** new `high_tops` style: black `#1A1A1E`, blue `#2A6FD6` collar and panels, white sole and laces, no logos
- **ref action:** `cheer` frame 13, happy face (the touchdown cheer; the standard cheer, arms up)
- Weak spots: the side view only catches the edge of the "55"; a short strip of bare leg shows between boxers and high-tops.

## Refs
- `refs/jarling/yoji.glb`: the 3D master (idle, run, kick, cheer; ten slots)
- `refs/jarling/yoji_turnaround.png`, `yoji_expressions.png`, `yoji_cheer.png`
- `refs/jarling/yoji_side.png`, `yoji_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/yoji_pixel.png`, `yoji_frames.png` (+ `.json`), `yoji_pixel_sheet.png`: The Hill pixel form
- `../yoji_read_check.png` (read check), `../yoji_lineup.png` (Jeff, Chuck and Yoji at true scale)

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/yoji.py` (`yoji()`)

- **Height:** 32 px with the outline (1.0 m body plus the tall cowboy hat, traced from `refs/jarling/yoji_side_sprite.png`,
  capped at the frame): hat 5 rows (trapezoid crown 3 rows with a 1 px pinch notch on top + band row, 1 long flat brim row with the tips turned up 1 px), head 8-9
  rows, jersey 7-8 rows (shoulder pads on the top rows, gold hem), navy-gold waistband + 2 rows of boxers, 2 rows of bare
  legs, high-tops 4 rows (blue collar, 2 black rows, white sole).
- **Palette:** hat `#C8955A` (+ `#A6763F`), band `#5A3A22`, hair and brows `#6B4A2E`, skin `#E8B48A` (+ `#C8936B`), jersey
  `#1F3A6B` (+ `#162B52`), trim `#F2B632`, number and boxers `#F7F7F5` (+ `#D6D8DE`), stars `#1F3A6B`, shoes `#1A1A1E`
  with `#2A6FD6`, soles `#F7F7F5`, mouth `#6A2232`, outline `#2A1E2C`. Every pixel colour is at least ΔE00 24 from P1
  `#3cc24a` and P2 `#e4393c`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride, sleep0-1
  (three-quarter view facing right, feet on row 30, hand at (22, 21) idle).
- **Should read as:**
  - a tan cowboy hat (not horns, not a bucket hat, not a sombrero, not a helmet): one long flat brim row, the widest thing
    on the figure and clearly wider than the head on both sides, tips turned up only 1 px; a trapezoid crown (narrower on
    top) with a single 1 px pinch notch in the top middle; the band row; short brown hair under it at the back and as a
    fringe. At 16 px the silhouette is a flat brim line with a crown on it
  - a navy football jersey 55: broad shoulder pads (the widest part of the body), gold sleeve stripes and hem, a white
    3 x 5 "55" on the front form (a white "5" on the side of the jersey in the frames)
  - boxer shorts: white with navy star pixels and a navy-and-gold waistband, then bare skin legs
  - high-tops: black with a blue collar above the ankle, a blue stripe, white soles
  - a big grin with a white row of teeth, thick brown brows, round dark eyes
