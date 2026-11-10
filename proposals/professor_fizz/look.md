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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `regular`
- **height:** 1.0
- **leg_scale:** 1.0
- **width / belly:** regular, no belly
- **head:** `round`, size 1.0
- **hair:** **new** `upright` (tall vertical spray), white; or `spiky` stretched up if the kit can scale it
- **headwear:** **new** `goggles_up` (shared with Granny Gravel), brass rims
- **top:** **new** `lab_coat` (knee-short coat over the top, purple collar)
- **bottoms:** `pants`, purple
- **shoes:** **new** `dress_shoes` (shared with Mayor Pip), black, with **new** `socks_mismatch` (one yellow-orange, one blue)
- **face extra:** scorched-brow decal (one brow)
- **gear:** zap gun or notebook in `hand_r` (optional)
- **pieces needed:** upright hair, goggles (shared), lab_coat, dress_shoes (shared), mismatched socks, scorch-brow decal

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Hair a 5-px-tall white spray above the head; goggles a brass row with two light-blue dots. Lab coat white with a purple collar pixel pair; socks one orange and one blue pixel above the black shoes.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
