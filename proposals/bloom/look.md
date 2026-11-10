# Bloom — look

## Kaden's sheet (verbatim)
Short with a soft, rounded build. Huge floppy straw sun hat with one flower on the brim, pink shirt, denim-blue skirt with muddy knees below it, purple garden clogs. Rosy cheeks, gentle smile.

## Must survive every art style
- Huge floppy straw sun hat with one flower on the brim
- Pink shirt
- Denim-blue skirt with muddy knees below it
- Purple garden clogs
- Short, soft, rounded; rosy cheeks, gentle smile

## Silhouette
Short soft body under a very wide floppy hat brim (wider than the shoulders), skirt, chunky clogs. A mushroom outline.

## Face
Rosy cheeks, gentle smile, soft eyes. Expressions to build: gentle smile (default), encouraging (eyes arcs, open smile), humming (eyes closed, small `o`).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- straw sun hat: `#E3C27A`
- flower petals: `#8E9BF0` (accent)
- flower centre: `#FFD23F` (accent)
- shirt: `#F7A8CB`
- skirt: `#5B7FB8`
- mud: `#6B4A33` (accent)
- clogs: `#8A4FC4`
- cheeks: `#F4A3B4` (accent)

## Signature props
- Straw sun hat with one flower (periwinkle petals, yellow centre) on the brim
- Optional small watering can as gear in `hand_r`

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `puffy` (soft and rounded)
- **height:** 0.85 (short)
- **leg_scale:** 0.85
- **width / belly:** soft, slight belly
- **head:** `round`, size 1.0
- **hair:** `bob`, colour left to the kit lane (not fixed by the sheet)
- **headwear:** **new** `sun_hat`, floppy wide brim (soft-body or sway bone), with **new** `hat_flower`
- **top:** `tee`, pink
- **bottoms:** **new** `skirt` (knee length), denim blue; **new** `mud_knees` decals below
- **shoes:** **new** `clogs`, purple
- **face extra:** rosy cheeks (blush up, in `#F4A3B4`, not player red)
- **gear:** watering can in `hand_r` (optional)
- **pieces needed:** floppy sun hat + flower, knee skirt, mud-knee decals, clogs, watering can (gear)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Hat brim 2 px wider than the body on each side, straw colour, one periwinkle flower pixel with a yellow centre. Pink top, blue skirt, two brown mud pixels on the knees, purple clogs.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
