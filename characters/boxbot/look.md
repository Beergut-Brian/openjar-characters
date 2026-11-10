# Boxbot — look

## Kaden's sheet (verbatim)
Square body type. Cardboard box over the torso with drawn-on dials and buttons, smaller box on the head with a face cut-out, dryer-hose arms, grey pants, blue shoes. Calm, flat smile.

## Must survive every art style
- Cardboard box over the torso with drawn-on dials and buttons
- Smaller box on the head with a face cut-out
- Dryer-hose arms
- Grey pants, blue shoes
- Square body; calm, flat smile

## Silhouette
Two stacked boxes, a bigger one on the body and a smaller one on the head, with ribbed hose arms: all right angles.

## Face
Seen through the cut-out: calm, flat smile, steady eyes. Expressions to build: flat smile (default), processing (eyes up, flat mouth), secret delight (real grin, quickly hidden).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- cardboard box: `#C49A6C`
- marker lines: `#2A2A30` (accent)
- button blue: `#3B6FD1` (accent)
- button yellow: `#F2C230` (accent)
- dryer-hose arms: `#C0C4CA`
- pants: `#80848C`
- shoes: `#3B6FD1`

## Signature props
- Head box (headwear; face cut-out so the real face is visible)
- Torso box (costume over the torso) with drawn dials and buttons
- Dryer-hose sleeves (costume over the arms; the arms are the standard arms)

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/boxbot/jarling.json` (standard humanoid body, kit v2; costume pieces sit over the standard body, same skeleton, actions, slots and collision as every playable character).
- **body:** `boxy`, height 0.9, leg_scale 0.9; the boxes are costume over the standard body
- **head:** `soft_square` **0.8** (smaller than the kit sheet's 1.0 so the head box comes out no wider than the body box, as his sheet says "smaller box on the head"); skin `#EFBB90`, no hair
- **headwear:** `box_head` `#C49A6C`, scale 0.92, face cut-out (the real face shows through)
- **costume:** `box_torso` `#C49A6C` with drawn dials and `#3B6FD1` buttons, `hose_arms` `#C0C4CA` (ribbed sleeves over the standard arms)
- **top:** `long` `#C0C4CA`; **bottoms:** `pants` `#80848C`; **shoes:** `sneaker` `#3B6FD1`
- **face:** button eyes, `flat` mouth, no brows/nose. Expressions: neutral = flat smile, happy = secret delight (`grin_top`), surprised = processing (wide eyes, flat mouth), determined = half-lidded flat
- **ref action:** `cheer` frame 10, happy (`boxbot_cheer.png`)
- **3D size:** 0.96 m tall. Deviation: the head box is about as wide as the body box (the kit's `box_torso` has no size option), not clearly smaller

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/boxbot.glb`: the 3D master
- `refs/jarling/boxbot_turnaround.png`, `boxbot_expressions.png`, `boxbot_cheer.png`
- `refs/jarling/boxbot_side.png`, `boxbot_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/boxbot_pixel.png`, `boxbot_frames.png` (+ `.json`), `boxbot_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/boxbot.py` (`boxbot()`)

- **Height:** 27 px with the outline (the 3D is about 0.98 m, 26-27 px at true scale, no squeeze): head box 10 rows,
  torso box 8, pants 6, shoes 3. Head box 10 px wide, torso box 12 px (the head is the smaller box).
- **Palette:** box `#C49A6C` (shade `#A47C52`), tape `#E6CFA0`, marker lines and face dots `#2A2A30`, dials blue `#3B6FD1`
  and yellow `#F2C230`, skin `#EFBB90` (+ `#CF9A70`), hose `#C0C4CA` (rib shade `#9A9EA6`), pants `#80848C` (back leg `#63676F`),
  shoes `#3B6FD1` (sole `#2C54A0`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions).
- **Should read as:**
  - a kid in a cardboard-box robot costume (not a crate, not a TV): two stacked tan boxes, a pale tape strip on the top row
    of the head box, shaded left column and bottom row on each box
  - real face in a cut-out: 6 x 6 skin window (5 x 6 in the frames), two 1 px dot eyes, a flat 3-4 px line mouth (calm smile)
  - drawn-on torso: blue and yellow dial pixels between marker dots, a marker line below
  - ribbed dryer-hose arms: 2 px sleeves with alternating light and dark rows, skin mitten hands
  - grey pants, blue shoes with a darker sole
