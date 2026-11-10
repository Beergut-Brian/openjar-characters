# Lampy — look

## Kaden's sheet (verbatim)
Tall and thin. White miner's helmet with a big round headlamp, dusty teal overalls-style top, brown pants, dirt smudge on one cheek, grey boots. Wide curious eyes.

## Must survive every art style
- White miner's helmet with a big round headlamp
- Dusty teal overalls-style top
- Brown pants, grey boots
- Dirt smudge on one cheek
- Tall and thin; wide curious eyes

## Silhouette
Tall, thin column topped by a white helmet with a big round lamp sticking out front; long legs. Reads like a lit match.

## Face
Wide, round curious eyes, small mouth, a dirt smudge on one cheek (left). Expressions to build: curious (eyes wide), wonder gasp (mouth `o`, brows up), shy smile (eyes half-lidded, small smile).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- miner's helmet: `#F1F1EC`
- headlamp lens: `#FFE9A8` (accent)
- overalls top: `#3F8A99`
- pants: `#7A5536`
- cheek smudge: `#6B5A4A` (accent)
- boots: `#7B7F86`

## Signature props
- Headlamp on the helmet: a real light (emissive lens + a spot light in 3D; the light can be toggled by the game)
- A rock (gear, `hand_r`) for idle and win

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `slim`
- **height:** 1.25 (tall)
- **leg_scale:** 1.15
- **width / belly:** thin, no belly
- **head:** `round`, size 1.0
- **hair:** `short`, under the helmet
- **headwear:** **new** `miner_helmet` (white dome, front lamp housing with an emissive lens and an optional spot light, light on by default only in dark scenes)
- **top:** **new** `overalls_top` (bib and straps), dusty teal
- **bottoms:** `pants`, brown
- **shoes:** `boots`, grey
- **face extra:** cheek `smudge` decal on one cheek
- **gear:** rock in `hand_r` (optional)
- **pieces needed:** miner_helmet + headlamp light, overalls_top, cheek smudge decal, rock (gear)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Helmet a white dome with a 2x2 pale-yellow lamp pixel at the front; in dark areas a light cone sprite in front of the lamp. Smudge one brown pixel on the cheek. Tallest of the Hillville four at 32 px.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
