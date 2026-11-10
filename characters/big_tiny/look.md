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
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Fills the full 32 px frame and is the widest sprite; the beanie is a 2x2 navy dot on top. Sneakers 4 px long each, white.

## Refs
- `refs/jarling/big_tiny.glb`: the 3D master
- `refs/jarling/big_tiny_turnaround.png`, `big_tiny_expressions.png`, `big_tiny_cheer.png`
- `refs/jarling/big_tiny_side.png`, `big_tiny_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/big_tiny_pixel.png`, `big_tiny_frames.png` (+ `.json`), `big_tiny_pixel_sheet.png`: The Hill pixel form
