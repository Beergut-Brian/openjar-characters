# Granny Gravel — look

## Kaden's sheet (verbatim)
The white-bun grandma body type. Safety goggles pushed up into her hair, lavender cardigan-style top, long grey skirt, bright yellow sneakers. Tiny smile, raised eyebrows.

## Must survive every art style
- White bun (the grandma hair)
- Safety goggles pushed up into the hair
- Lavender cardigan-style top
- Long grey skirt
- Bright yellow sneakers

## Silhouette
Round head with a tall white bun on top and goggles as a band across it, a soft cardigan torso and a long skirt that hides the legs down to bright sneakers: a bell shape topped with a bun.

## Face
Tiny smile, raised eyebrows. Expressions to build: sweet (tiny smile, brows up), gleeful driving cackle (mouth wide, eyes narrowed), innocent denial (eyes closed, little smile).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- hair (bun): `#F2F0EA`
- goggle frame: `#6E7681` (accent)
- goggle lens: `#A9D6E5` (accent)
- cardigan top: `#B9A3D9`
- skirt: `#8C8F96`
- sneakers: `#FFD93B`

## Signature props
- Safety goggles (headwear, pushed up; can be pulled down)
- Imaginary cookies are mimed: no prop

## Per-technique notes

### Jarling 3D (master)
Built 2026-11-10 from `characters/granny_gravel/jarling.json` (standard humanoid body, kit v2).
- **body:** `regular`, height 0.9, leg_scale 0.85
- **head:** `round` 1.0; skin `#F7CFAE`; hair preset `top_bun` `#F2F0EA` (white, bun on the crown)
- **goggles:** costume piece `goggles`, `safety` style, frame `#4A4F5A`, on the forehead at `height` 0.56 and `size` 0.85: pushed up into the
  white hair under the bun, well clear of the eyes and mouth
- **face:** button eyes, thin raised brows, tiny `smile`. Expressions: happy = closed-eye grin, surprised = `o`, determined = the
  behind-the-wheel cackle (open grin, brows down)
- **top:** `long` `#B9A3D9` with a `collar` (`#9C84C4`) and one row of `buttons` (cardigan); **bottoms:** `long_skirt` `#8C8F96` (length 0.85)
  over same-colour pants; **shoes:** `sneaker` `#FFD93B`
- **ref action:** `cheer` frame 10

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Bun is a 3x3 white blob on top of the head; goggles a 1-px dark band with two light-blue lens pixels. Skirt is a solid grey trapezoid to the ankles; yellow sneakers 2 px.

## Refs
- `refs/jarling/granny_gravel.glb`: the 3D master
- `refs/jarling/granny_gravel_turnaround.png`, `granny_gravel_expressions.png`, `granny_gravel_cheer.png`
- `refs/jarling/granny_gravel_side.png`, `granny_gravel_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/granny_gravel_pixel.png`, `granny_gravel_frames.png` (+ `.json`), `granny_gravel_pixel_sheet.png`: The Hill pixel form
