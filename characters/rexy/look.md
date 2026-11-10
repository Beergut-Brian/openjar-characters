# Rexy — look

## Kaden's sheet (verbatim)
Small kid body type. Orange dino onesie with the hood up, white felt teeth along the hood edge, a row of yellow spikes down the back, short tail, orange footies. Face peeks out with a huge open-mouth grin.

## Must survive every art style
- Orange dino onesie with the hood up
- White felt teeth along the hood edge
- A row of yellow spikes down the back, short tail
- Orange footies
- Small kid body; face peeks out with a huge open-mouth grin

## Silhouette
Small round-hooded kid shape with a jagged row of spikes down the back and a short tail: the side view is the dinosaur.

## Face
Huge open-mouth grin framed by the hood's felt teeth. Expressions to build: roar (mouth wide, brows down), grin (default), pout (small frown, brief).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- dino onesie: `#F7941D`
- felt teeth: `#F7F7F2` (accent)
- back spikes: `#FFD23F` (accent)
- footies: `#F7941D`

## Signature props
- Dino hood with felt teeth (headwear)
- Spikes and tail are part of the onesie costume (not body features; they are clothing)

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/rexy/jarling.json` (standard humanoid body, kit v2; costume pieces sit over the standard body, same skeleton, actions, slots and collision as every playable character).
- **body:** `round`, height 0.8, leg_scale 0.8 (small kid); the onesie is a costume over the standard body
- **head:** `round` 1.05, no ears, skin `#F0BE94`; no hair (hood up)
- **headwear:** `animal_hood` `#F7941D` with white felt teeth `#FFFFFF` round the face opening and a yellow spike `#FFD23F` crest
- **top:** `costume` `#F7941D`; **bottoms:** `pants` `#F7941D`; **shoes:** `footies` `#F7941D` (one orange onesie)
- **costume:** `back_spikes` `#FFD23F`, `dino_tail` `#F7941D` with yellow spikes (cosmetic, no collision)
- **face:** round eyes, `yell` open-mouth grin. Expressions: neutral/happy = grin (`yell`), surprised = roar (brows down, wide mouth), determined = pout (`frown`, brows up)
- **ref action:** `kick` frame 17, roar face (`rexy_kick.png`)
- **3D size:** 1.15 m tall with the hood spikes (body h 0.8)

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/rexy.glb`: the 3D master
- `refs/jarling/rexy_turnaround.png`, `rexy_expressions.png`, `rexy_kick.png`
- `refs/jarling/rexy_side.png`, `rexy_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/rexy_pixel.png`, `rexy_frames.png` (+ `.json`), `rexy_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/rexy.py` (`rexy()`)

- **Height:** 31 px with the outline (the 3D is 1.15 m with the hood spikes, about 31 px at true scale): spikes 2 rows, round hood
  13 rows with the face opening inside, short torso 9, short legs 5 with footies. Small kid, big head.
- **Palette:** onesie, hood and footies `#F7941D` (shade `#D2780F`), spikes `#FFD23F`, felt teeth `#F7F7F2`, skin `#F0BE94`
  (+ `#D09C72`), eyes `#2A1E2C` with a `#FFFFFF` highlight, mouth `#6A2232`, tongue `#E8708A`, outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions).
- **Should read as:**
  - a kid in a dinosaur onesie (not a fox or a pumpkin): yellow spikes in a row over the hood and down the back, a short
    orange tail with yellow spikes sticking out behind at the left (a sliver beside the legs in the front form)
  - hood up: a big round orange hood with an oval skin face opening, 3 white felt-teeth pixels along its top edge
  - huge open-mouth grin: `#6A2232` mouth with a pink tongue, nothing else at the mouth
  - round eyes: 2 x 2 dark eyes with a white highlight pixel (the far eye 1 x 2 in the frames)
  - small and short-legged: 9 px torso, 5-row legs into orange footies with a shaded sole
