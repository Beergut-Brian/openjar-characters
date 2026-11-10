# Astro Ana — look

## Kaden's sheet (verbatim)
Medium build. Clear fishbowl helmet so the face stays visible, hair in two puffs inside it, white suit-style top with an orange chest stripe, white pants, orange moon boots. Determined grin.

## Must survive every art style
- Clear fishbowl helmet so the face stays visible
- Hair in two puffs inside the helmet
- White suit-style top with an orange chest stripe
- White pants, orange moon boots
- Determined grin

## Silhouette
Medium body with a big clear sphere around the head (two hair puffs visible inside), chunky moon boots: a bubble on a white column on two blocks.

## Face
Determined grin, focused eyes, visible through the glass. Expressions to build: determined (grin, brows down), countdown focus (set mouth), liftoff joy (open mouth, eyes wide).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- fishbowl glass (tint): `#D8EEF8`
- hair puffs: `#3B2A20`
- suit top: `#F2F4F6`
- chest stripe: `#F7941D` (accent)
- pants: `#F2F4F6`
- moon boots: `#F7941D`

## Signature props
- Fishbowl helmet: transparent; the face must stay fully readable (low-reflection glass, no tint over the face)

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `regular`
- **height:** 1.0
- **leg_scale:** 1.0
- **width / belly:** regular, no belly
- **head:** `round`, size 1.0
- **hair:** **new** `two_puffs` (two round puffs at the sides of the head), dark brown; must fit inside the helmet
- **headwear:** **new** `fishbowl_helmet` (transparent sphere, thin rim at the neck); transparency must work in every renderer the games use, with a fallback of rim-only
- **top:** **new** `spacesuit_top` (white, padded) with orange chest stripe
- **bottoms:** `pants`, white (spacesuit style)
- **shoes:** **new** `moon_boots`, orange, chunky
- **gear:** none
- **pieces needed:** fishbowl helmet (transparent), two-puffs hair, spacesuit top + stripe, moon boots

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Helmet drawn as a 1-px light-blue circle outline with one white highlight pixel; face and two dark hair puffs inside. Orange stripe and orange 3-px boots.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
