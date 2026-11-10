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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `regular` (soft)
- **height:** 0.9
- **leg_scale:** 0.85 (skirt covers them)
- **width / belly:** soft, no belly
- **head:** `round`, size 1.0
- **hair:** `bun`, white (Kaden's "white-bun grandma body type" is hair + skirt on the standard body, see REPORT)
- **headwear:** **new** `goggles_up` (band + two round lenses), fits over the bun's front; `down` pose for driving
- **top:** **new** `cardigan` style (open front with a button line), lavender
- **bottoms:** **new** `long_skirt` (ankle length; must not change collision or leg rig)
- **shoes:** **new** `sneakers`, yellow
- **gear:** none
- **pieces needed:** goggles (up/down), cardigan top, long_skirt, sneakers

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Bun is a 3x3 white blob on top of the head; goggles a 1-px dark band with two light-blue lens pixels. Skirt is a solid grey trapezoid to the ankles; yellow sneakers 2 px.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
