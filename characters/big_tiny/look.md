# Big Tiny — look

## Kaden's sheet (verbatim)
The widest, tallest body type with the smallest possible beanie perched on top. Sky blue shirt stretched over a round belly, grey pants, enormous white sneakers. Closed-eye happy smile.

## Must survive every art style
- Widest, tallest body with the smallest possible beanie perched on top
- Sky blue shirt stretched over a round belly
- Grey pants
- Enormous white sneakers
- Closed-eye happy smile

## Silhouette
The biggest Jarling: tall and wide with a round belly, a tiny beanie dot on top of the head and huge sneakers. Tall pear outline with a pip on top.

## Face
Eyes closed in happy arcs, soft wide smile. Expressions to build: content (closed-eye smile), oops-sorry (brows up, small `o`), rumbling chuckle (mouth open, eyes arcs).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- beanie: `#2E3A66`
- shirt: `#7EC8F2`
- pants: `#80848C`
- sneakers: `#F7F7F5`
- sneaker sole: `#D0D3D8` (accent)

## Signature props
- Tiny beanie (headwear, scaled down)
- No gear

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/big_tiny/jarling.json` (standard humanoid body, kit v2).
- **body:** `round`, height 1.3, width 1.5, belly 1.0: the top of the playable range on every one (the widest and tallest playable Jarling)
- **head:** `round` 1.0; skin `#D99E6E`; `buzz` hair `#4A2F23`
- **headwear:** `beanie` `#2E3A66` at `scale` 0.45, perched on the crown (hair free)
- **face:** closed-eye smile in neutral (`eye_mode` arc), soft brows. Expressions: happy = closed-eye open grin, surprised = eyes open, `o`
  (the only face with open eyes), determined = closed eyes, set mouth
- **top:** `tee` `#7EC8F2` stretched over the belly; **bottoms:** `pants` `#80848C`; **shoes:** `sneaker` `#F7F7F5`, `size` 1.35 (enormous)
- **ref action:** `cheer` frame 10
- Same skeleton, slots and gameplay collision as everyone; the size is visual only

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/big_tiny.glb`: the 3D master
- `refs/jarling/big_tiny_turnaround.png`, `big_tiny_expressions.png`, `big_tiny_cheer.png`
- `refs/jarling/big_tiny_side.png`, `big_tiny_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/big_tiny_pixel.png`, `big_tiny_frames.png` (+ `.json`), `big_tiny_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/big_tiny.py` (`big_tiny()`)

- **Height:** 32 px with the outline, the full frame (1.3 m body): beanie 2 rows above the head (its cuff row sits on the
  crown), head 11, belly 10, pants 4, sneakers 3. The widest Jarling: belly 24 px across in the front form (30 px with the arms
  and outline), 21 px in the frames, against a 12 px head.
- **Palette:** beanie `#2E3A66` with pom and cuff `#46558C`, buzz hair `#4A2F23`, skin `#D99E6E` (+ `#B97F55`), closed eyes
  `#2A1E2C`, mouth `#6A2232`, tee `#7EC8F2` (shade `#5FA9D6` under the belly curve and on the back sleeve), pants `#80848C`
  (shade `#6A6E76`), sneakers `#F7F7F5` (sole `#B9BDC4`), outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride,
  sleep0-1 (three-quarter view facing right, feet on row 30; hand at (22, 21) idle, The Hill's dig hand positions, the front arm
  resting on the belly; he fills the frame, so the jump tucks the feet up 2 px instead of lifting the body).
- **Should read as:**
  - a too-small beanie (not a hair tuft, not a button): 4 px wide, 3 rows: a 2 px light pom on top, a navy row, a light cuff
    row, perched on the crown with brown buzz hair showing 2 px either side of the cuff
  - gentle giant: a round sky-blue belly much wider than the head, shaded underneath, short grey legs
  - happy closed eyes: two `^` arcs (3 px each) in every frame, a small 4 px smile
  - enormous sneakers: white, 7 px long each with a grey sole row and a grey heel pixel
