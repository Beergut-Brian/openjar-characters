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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `stocky` (barrel chest)
- **height:** 0.95
- **leg_scale:** 0.8 (short legs, the minimum)
- **width / belly:** big chest, flat belly
- **head:** `round`, size 1.0
- **hair:** `buzz` under the cap
- **headwear:** `cap`, navy
- **top:** **new** `stripes_vertical` pattern on `tee` (black + white)
- **bottoms:** **new** `shorts` (shared), grey
- **shoes:** **new** `sneakers` (shared), white, with **new** `tall_socks` (white, navy band)
- **gear:** whistle on cord (costume, neck), clipboard optional
- **pieces needed:** vertical stripe pattern, shorts, sneakers, tall socks, whistle + cord

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Stripes as alternating 1-px black/white columns; cap a navy dome with a 2-px brim; whistle a single silver pixel on a yellow cord line. Socks 3 px white above the sneakers.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
