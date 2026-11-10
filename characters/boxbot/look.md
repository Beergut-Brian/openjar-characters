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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `boxy` (Kaden's "square body type")
- **height:** 0.9
- **leg_scale:** 0.9
- **width / belly:** square, no belly; the torso box sits over it
- **head:** `soft_square`, size 1.0, inside the head box
- **hair:** `none`
- **headwear:** **new** `head_box` (cardboard cube with a face cut-out; head must stay readable)
- **top:** **new** `torso_box` (cardboard box costume with marker-drawn dials and buttons)
- **sleeves:** **new** `hose_sleeves` (ribbed silver tubes over the standard arms; must bend with the arm bones)
- **bottoms:** `pants`, grey
- **shoes:** **new** `sneakers` (shared), blue
- **gear:** none
- **pieces needed:** head box with cut-out, torso box with drawn dials, ribbed hose sleeves

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Two tan rectangles stacked; face in a lighter cut-out window; two dial pixels (blue, yellow) on the torso box; arms ribbed silver (alternating light/dark pixels). Blue shoes.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
