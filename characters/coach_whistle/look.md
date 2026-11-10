# Coach Whistle — look

## Kaden's sheet (verbatim)
Barrel-chested with short legs. Navy cap, black-and-white vertical striped shirt, silver whistle on a cord, grey shorts, white sneakers with tall socks. Permanently mid-yell with a happy face.

## Must survive every art style
- Navy cap
- Black-and-white vertical striped shirt
- Silver whistle on a cord
- Grey shorts, white sneakers with tall socks
- Barrel chest on short legs; permanently mid-yell with a happy face

## Silhouette
Barrel torso on short legs under a curved cap brim; vertical stripes; tall socks make the short legs read. Like a striped drum on sticks.

## Face
Mouth always open mid-yell but happy (brows up, eyes bright). Expressions to build: pep-yell (wide open mouth, eyes bright), whistle blow (cheeks puffed, whistle in mouth), proud (closed-eye grin).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- cap: `#1E2B4D`
- shirt stripe black: `#1A1A1E`
- shirt stripe white: `#F5F5F2`
- whistle: `#C9CED4` (accent)
- cord: `#F2C230` (accent)
- shorts: `#8A8E96`
- sneakers + socks: `#F7F7F5`
- sock band: `#1E2B4D` (accent)

## Signature props
- Silver whistle on a yellow cord (costume piece around the neck; whistle can move to the mouth for the blast)
- Optional clipboard in `hand_l` (shared with Foreman Dot)

## Per-technique notes

### Jarling 3D
Built 2026-11-10 from `characters/coach_whistle/jarling.json` (standard humanoid body, kit v2).
- **body:** `stocky`, height 0.95, leg_scale 0.8, width 1.15, belly 0.1 (0.25 made the belly read bigger than the chest in the side view)
- **head:** `round` 1.0, round ears; skin `#D99E6E`; `buzz` hair `#3A2418` under a navy `cap` `#1E2B4D` (tilt 8)
- **face:** round eyes, thick brows raised (`brow_raise` 0.08, `brow_tilt` -0.25), nose `bump`, mouth `yell`, blush 0.4.
  Expressions: neutral = pep yell, eyes bright; happy = proud closed-eye grin (arc eyes, yell); surprised = wide eyes, `o`;
  determined = yell with brows down a little.
- **top:** `tee` `#F5F5F2` with `vstripes` `#1A1A1E` (count 10, so a black stripe sits behind the whistle), black sleeves
- **bottoms:** `shorts` `#8A8E96`; **shoes:** `sneaker` `#F7F7F5` with tall socks (white, height 0.5, navy cuff `#1E2B4D`)
- **costume:** `whistle_cord`, whistle `#C9CED4`, cord `#F2C230`, `size` 1.5. New kit param: `size` on `whistle_cord`
  (`avatar/kit/pieces_outfit.py`, default 1.0 = the old look) scales the whistle, not the cord. It hangs at mid-chest on the
  sternum, on top of the shirt, and sticks out in the side view.
- **ref action:** `cheer` frame 10, happy face.
- The whistle stays on the cord in every action. The "whistle blow" face/pose (whistle in the mouth, cheeks puffed) waits for
  the held-item hold styles; no clipboard in this build (held items belong to that lane).

## Refs
- `refs/jarling/coach_whistle.glb`: the 3D master
- `refs/jarling/coach_whistle_turnaround.png`, `coach_whistle_expressions.png`, `coach_whistle_cheer.png`
- `refs/jarling/coach_whistle_side.png`, `coach_whistle_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/coach_whistle_pixel.png`, `coach_whistle_frames.png` (+ `.json`), `coach_whistle_pixel_sheet.png`: The Hill pixel form

Fixed colours: unchanged. Added for the 3D: skin `#D99E6E`, hair and brows `#3A2418`. Pixel shades added: skin `#B97F55`,
cap light `#34477A`, shorts `#6F737B`, sneaker sole `#B9BDC4`, whistle shade `#7D848D`, mouth `#6A2232` / `#F2848C`.

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/coach_whistle.py` (`coach_whistle()`)

- **Height:** 29 px with the cap (1.12 m, traced from `coach_whistle_side_sprite.png`): cap 5 rows, face 8, barrel torso 9,
  shorts 2, navy cuff 1, white socks 2, sneakers 2. The barrel torso is 14 px wide, wider than the 12 px head.
- **Palette:** cap `#1E2B4D` (+ `#34477A`), stripes `#1A1A1E` / `#F5F5F2`, whistle `#C9CED4` (+ `#7D848D`), cord `#F2C230`,
  shorts `#8A8E96` (+ `#6F737B`), sneakers and socks `#F7F7F5` (sole `#B9BDC4`), sock cuff `#1E2B4D`, skin `#D99E6E` (+ `#B97F55`),
  hair `#3A2418`, mouth `#6A2232` with tongue `#F2848C`, outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions).
- **Should read as:**
  - a referee's whistle hanging on a yellow cord at the chest (not a pipe, not a medal): a 2 x 2 silver block with a darker
    mouthpiece pixel on a dark patch at the bottom of a yellow cord V, 6 rows below the mouth, in every frame
  - navy baseball cap: navy dome with a 2 px brim to the right (a brim to both sides in the front form)
  - referee stripes: alternating 1 px black / white columns on the torso
  - tall white socks: white socks with a navy cuff row above white sneakers on short legs
  - mid-yell happy face: a small dark open mouth block with a tongue row inside, nothing sticking out of it
