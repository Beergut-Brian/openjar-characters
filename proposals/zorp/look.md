# Zorp — look

## Kaden's sheet (verbatim)
Slim with a slightly taller head. Light blue skin, headband with two bobbing antennae, loud yellow-and-pink vacation shirt, white shorts, sandals. Big round eyes and a small amazed mouth.

## Must survive every art style
- Light blue skin
- Headband with two bobbing antennae
- Loud yellow-and-pink vacation shirt
- White shorts, sandals
- Slim with a slightly taller head; big round eyes and a small amazed mouth

## Silhouette
Slim body with a taller egg-ish head and two antennae with bobbles sticking up from a headband; boxy loud shirt. The antennae are the outline.

## Face
Big round eyes, small `o` amazed mouth. Expressions to build: amazed (eyes wide, `o`), delighted (eyes arcs, small smile), puzzled (one brow up, flat mouth).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Zorp's skin is fixed by the sheet: light blue (below).
- skin + antennae: `#9FD6F0`
- antenna bobbles: `#FFD23F` (accent)
- headband: `#C9CED4`
- shirt yellow: `#FFD23F`
- shirt pink: `#FF7EB9`
- shorts: `#F5F5F2`
- sandals: `#C89A63`

## Signature props
- Antennae on a headband: Kaden says "headband with two bobbing antennae", so the antennae are mounted on headwear, not grown (see REPORT); they bob with secondary motion
- Optional imaginary camera (mimed)

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `slim`
- **height:** 1.05
- **leg_scale:** 1.0
- **width / belly:** slim, no belly
- **head:** `tall`, size 1.05 (Kaden's "slightly taller head"; uses the kit's existing head shape, not a body change)
- **skin:** light blue `#9FD6F0` (fixed; Zorp is the one playable with a fixed non-human skin)
- **hair:** `none`
- **headwear:** `headband` (silver) with **new** `antennae` add-on: two stalks with yellow bobbles, jiggle bones or spring motion. If Kaden prefers them as a body feature, they move to the head mesh (one flag)
- **top:** **new** `vacation_shirt` (open collar, short sleeves, loud yellow + pink print)
- **bottoms:** **new** `shorts` (shared), white
- **shoes:** **new** `sandals`
- **gear:** none
- **pieces needed:** antennae (on headband), vacation shirt print, shorts, sandals, tall head shape

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Antennae two 1-px stalks with yellow tip pixels, 4 px above the head; shirt a yellow block with pink dots. Light blue skin.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
