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

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `round` (small and round in the onesie)
- **height:** 0.8 (kid)
- **leg_scale:** 0.8
- **width / belly:** slightly round
- **head:** `round`, size 1.05
- **hair:** `none` (hood up)
- **headwear:** **new** `dino_hood` with felt-teeth rim
- **top:** **new** `onesie` (one piece top + bottoms), orange
- **bottoms:** part of the onesie (same colour)
- **shoes:** **new** `footies` (onesie feet), orange
- **costume:** **new** `back_spikes` (yellow row) and **new** `short_tail` (on the `back`/`waist` area; cosmetic, no collision)
- **gear:** none
- **pieces needed:** dino hood + teeth, onesie, footies, back spikes, short tail

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Orange body, hood edge a row of alternating white tooth pixels around the face; 3 to 4 yellow spike pixels down the back and a 2-px tail. About 25 px tall (kid).

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
