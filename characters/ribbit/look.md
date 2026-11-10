# Ribbit — look

## Kaden's sheet (verbatim)
Small and round. Teal frog hoodie with the hood up, two big frog eyes on top of the hood, yellow belly panel, dark blue shorts, bare-look yellow shoes. Wide, flat, pleased smile.

## Must survive every art style
- Teal frog hoodie with the hood up
- Two big frog eyes on top of the hood
- Yellow belly panel
- Dark blue shorts, bare-look yellow shoes
- Small and round; wide, flat, pleased smile

## Silhouette
Small round body with a hood whose two big frog eyes stick up like bumps: a round blob with two balls on top.

## Face
Wide flat pleased smile, calm half-lidded eyes. Expressions to build: pleased (flat wide smile), fly-alert (eyes wide, head turned), mellow (eyes closed, smile).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- frog hoodie: `#2A9DB0`
- hood eyes: `#F5F5F2` (accent)
- hood pupils: `#15151A` (accent)
- belly panel: `#F6D44A`
- shorts: `#22336B`
- shoes: `#F6D44A`

## Signature props
- Frog hoodie hood (headwear) with two big frog eyes
- No gear

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `round`
- **height:** 0.85 (small)
- **leg_scale:** 0.85
- **width / belly:** round, with a belly (the yellow panel sits on it)
- **head:** `round`, size 1.05
- **hair:** `none` (hood up)
- **headwear:** **new** `frog_hood` (hood up, two big frog eyes on top: white with black pupils)
- **top:** **new** `hoodie` style, teal, with **new** `belly_panel` (yellow)
- **bottoms:** **new** `shorts` (shared), dark blue
- **shoes:** **new** `bare_look` shoes (toe-shaped, yellow): a shoe piece, not barefoot
- **motion:** **new** `hop` gait layer on `run` (cosmetic; same speed and collision)
- **gear:** none
- **pieces needed:** frog_hood with eyes, hoodie top, belly panel, shorts, bare-look shoes, hop gait layer

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Two 2x2 white frog-eye bumps on top of the teal hood, each with a black pupil pixel. Yellow belly block. Walk cycle is a hop (2 frames).

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
