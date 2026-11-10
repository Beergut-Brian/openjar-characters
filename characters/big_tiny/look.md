# Big Tiny — look

## Kaden's sheet (verbatim)
The widest, tallest body type with the smallest possible beanie perched on top. Sky blue shirt stretched over a round belly, grey pants, enormous white sneakers. Closed-eye happy smile.

## Must survive every art style
- Widest, tallest body with the smallest possible beanie perched on top
- Sky blue shirt stretched over a round belly
- Grey pants
- Enormous white sneakers
- Closed-eye happy smile

## Silhouette
The biggest Jarling: tall and wide with a round belly, a tiny beanie dot on top of the head and huge sneakers. Tall pear outline with a pip on top.

## Face
Eyes closed in happy arcs, soft wide smile. Expressions to build: content (closed-eye smile), oops-sorry (brows up, small `o`), rumbling chuckle (mouth open, eyes arcs).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- beanie: `#2E3A66`
- shirt: `#7EC8F2`
- pants: `#80848C`
- sneakers: `#F7F7F5`
- sneaker sole: `#D0D3D8` (accent)

## Signature props
- Tiny beanie (headwear, scaled down)
- No gear

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `round` (the widest build with a belly; `puffy` is as wide but has less belly)
- **height:** 1.3 (the maximum; Kaden's "widest, tallest body type")
- **leg_scale:** 1.0
- **width / belly:** maximum width and belly the standard body allows; the round belly is the shirt stretched over it
- **head:** `round`, size 1.0
- **hair:** `buzz`
- **headwear:** `beanie` at a **small** scale (new `scale` option, about 0.4) perched on top
- **top:** `tee`, sky blue, stretched (follows the round build)
- **bottoms:** `pants`, grey
- **shoes:** **new** `sneakers` (shared) with an `oversize` flag (about 1.4x)
- **gear:** none
- **pieces needed:** beanie scale option, sneakers oversize, round build at height 1.3. Collision stays the standard shape

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Fills the full 32 px frame and is the widest sprite; the beanie is a 2x2 navy dot on top. Sneakers 4 px long each, white.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
