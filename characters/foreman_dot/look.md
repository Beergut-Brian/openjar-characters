# Foreman Dot — look

## Kaden's sheet (verbatim)
Short and stocky. Yellow hard hat sitting slightly too low, orange shirt with one white hi-vis stripe, navy pants, chunky brown boots. Confident open-mouth smile.

## Must survive every art style
- Yellow hard hat sitting slightly too low, brim nearly over the eyes
- Orange shirt with one white hi-vis stripe across the chest
- Navy pants, chunky brown boots
- Short and stocky; confident open-mouth smile under the brim

## Silhouette
Short, wide stocky block with a low, dome hard hat that sits down over the brow line; chunky boots widen the base. A squat triangle-on-a-dome outline.

## Face
Eyes half under the brim, big open-mouth smile. Expressions to build: confident (default open grin), barking an order (mouth wide, brows down), delighted (eyes arc, grin), startled (worm; eyes wide, mouth `o`).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- hard hat: `#F5C518`
- shirt: `#F28A1E`
- hi-vis stripe: `#F4F4F0` (accent)
- pants: `#1F2D4F`
- boots: `#7A4E2A`

## Signature props
- Hard hat (sits low; can be nudged up)
- Optional clipboard in `hand_l` for cameos (gear, not part of the body)

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `stocky`
- **height:** 0.85 (short)
- **leg_scale:** 0.85
- **width / belly:** wide shoulders, flat belly: build stocky, no extra belly
- **head:** `round`, size 1.0
- **hair:** `short`, mostly hidden
- **headwear:** **new** `hard_hat` (dome + brim), with a `sit_low` offset so the brim sits at the brow; same piece Jeff and Chuck's the-hill alt forms use, if the kit lane shares it
- **top:** `tee` style, orange, with one horizontal white `hivis_stripe` (new costume piece)
- **bottoms:** `pants`, navy
- **shoes:** `boots`, chunky variant (new `chunky` size flag)
- **gear:** clipboard in `hand_l` (optional)
- **pieces needed:** hard_hat (low fit), hivis_stripe, chunky boots, clipboard

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. The hard hat is a 3-px-tall yellow dome with the brim one px above the eye line; the white stripe is a single row across the orange shirt. Must read at 16 px: yellow dome + orange block.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
