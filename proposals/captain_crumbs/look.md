# Captain Crumbs — look

## Kaden's sheet (verbatim)
Tall with a round middle. Tall white chef hat with a small skull-and-spoon badge, black eyepatch, white chef jacket with navy buttons, navy striped pants, black boots. Big curly moustache over a grin.

## Must survive every art style
- Tall white chef hat with a small skull-and-spoon badge
- Black eyepatch
- White chef jacket with navy buttons
- Navy striped pants, black boots
- Big curly moustache over a grin; tall with a round middle; usually dusted in flour

## Silhouette
Tall body with a round middle under a very tall puffed chef hat; curly moustache. A tall exclamation mark with a puffy top.

## Face
Eyepatch over one eye (left), big curly moustache, broad grin. Expressions to build: hearty grin (default), "arrr" growl (mouth open, brow down), laughing (eye closed, head back).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- chef hat: `#F7F7F2`
- badge: `#1F2D55` (accent)
- eyepatch: `#18181C` (accent)
- chef jacket: `#F7F7F2`
- buttons: `#1F2D55` (accent)
- pants stripe navy: `#1F2D55`
- pants stripe white: `#F7F7F2`
- boots: `#18181C`
- moustache: `#4A3324`

## Signature props
- Chef hat with skull-and-spoon badge (headwear)
- Eyepatch (face slot)
- Optional wooden spoon in `hand_r`
- Flour-puff particle on claps (effect, not a mesh)

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `round`
- **height:** 1.2 (tall)
- **leg_scale:** 1.0
- **width / belly:** round middle
- **head:** `round`, size 1.0
- **hair:** `short`; **new** `curly_moustache` facial hair (dark brown, not fixed by the sheet beyond "big curly")
- **headwear:** **new** `chef_hat` (tall puffed toque) with **new** `skull_spoon_badge`
- **face:** **new** `eyepatch` (on the `face` slot)
- **top:** **new** `chef_jacket` (double-breasted, navy buttons), white
- **bottoms:** `pants` with **new** `stripes_vertical` (shared with Coach Whistle) navy + white
- **shoes:** `boots`, black
- **extra:** flour dusting texture/decal and flour-puff particle
- **gear:** wooden spoon in `hand_r` (optional)
- **pieces needed:** chef hat + badge, eyepatch, curly moustache, chef jacket, striped pants, flour decal/particle

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Chef hat 6 px tall white puff with a navy badge pixel; black eyepatch pixel and strap line; dark curly moustache 3 px wide; navy/white striped pants.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
