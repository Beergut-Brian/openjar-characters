# Sir Clank — look

## Kaden's sheet (verbatim)
Medium build, stands very straight. Silver cooking pot worn as a helmet with the handle sticking out the back, grey shirt with a yellow shield shape on the chest, dark blue pants, brown boots. Serious eyebrows, proud smile.

## Must survive every art style
- Silver cooking pot worn as a helmet, handle sticking out the back
- Grey shirt with a yellow shield shape on the chest
- Dark blue pants, brown boots
- Stands very straight; serious eyebrows, proud smile

## Silhouette
Very upright medium body with a cylindrical pot on the head and its handle sticking straight out the back: a T-shape at the top in side view.

## Face
Serious, thick eyebrows, proud closed-mouth smile, chin up. Expressions to build: proud (default), noble charge (mouth open, brows down), polite concern (brows up, small mouth).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- pot helmet: `#B8BEC6`
- pot handle: `#3A3D44` (accent)
- shirt: `#8A8F98`
- shield: `#F2C230` (accent)
- pants: `#23305E`
- boots: `#7A4E2A`

## Signature props
- Pot helmet (headwear: cylinder with a rim and one long handle out the back)
- Optional wooden spoon as a sword, gear in `hand_r`

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `regular`
- **height:** 1.05
- **leg_scale:** 1.0
- **width / belly:** regular, no belly
- **head:** `round`, size 1.0
- **hair:** `short` under the pot
- **headwear:** **new** `pot_helmet` (silver cylinder, sits to the brow; long handle out the back)
- **top:** `tee`, grey, with **new** `shield_emblem` (yellow)
- **bottoms:** `pants`, dark blue
- **shoes:** `boots`, brown
- **posture:** very straight: spine lean 0, chin up
- **gear:** wooden spoon sword in `hand_r` (optional)
- **pieces needed:** pot helmet, shield emblem, spoon sword (gear)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Pot a 6x3 silver block with a 1-px darker rim and a 3-px handle sticking out the back in the side view. Yellow shield 3x3 on the grey chest.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
