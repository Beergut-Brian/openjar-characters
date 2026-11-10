# Old Reel — look

## Kaden's sheet (verbatim)
Tall with a round belly. Tan bucket hat with a single fishing lure pinned to it, khaki vest over a cream shirt, brown pants, tall yellow rain boots. Bushy white eyebrows, sleepy smile.

## Must survive every art style
- Tan bucket hat with a single fishing lure pinned to it
- Khaki vest over a cream shirt
- Brown pants, tall yellow rain boots
- Bushy white eyebrows, sleepy smile
- Tall with a round belly

## Silhouette
Tall body with a round belly, soft bucket-hat brim all round, vest, and tall boots to the knee: a tall egg in a floppy hat.

## Face
Bushy white eyebrows over sleepy half-lidded eyes, gentle smile. Expressions to build: sleepy smile (default), almost-had-it (brows up, mouth `o`), chuckle (eyes closed, open smile).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- bucket hat: `#C8A97A`
- lure blue: `#3F8FD8` (accent)
- lure yellow: `#F2C230` (accent)
- eyebrows: `#F2F0EA` (accent)
- vest: `#A89B6E`
- shirt: `#F1E7CF`
- pants: `#6E4B30`
- rain boots: `#F6C833`

## Signature props
- Fishing lure pinned to the hat (costume piece; blue and yellow, no red)
- Optional fishing rod as gear in `hand_r` for Life of a Worm cameos

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `round`
- **height:** 1.2 (tall)
- **leg_scale:** 1.05
- **width / belly:** round belly
- **head:** `round`, size 1.0
- **hair:** `short`, white (mostly under the hat); **new** `bushy` brow style, white
- **headwear:** **new** `bucket_hat`, tan, with **new** `hat_lure` pin
- **top:** `shirt`, cream, with **new** `vest` overlay (khaki, pockets)
- **bottoms:** `pants`, brown
- **shoes:** **new** `rain_boots`, tall, yellow
- **gear:** fishing rod in `hand_r` (optional)
- **pieces needed:** bucket hat + lure, vest overlay, bushy brows, tall rain boots, fishing rod (gear)

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Bucket hat a tan block with a downturned 1-px brim on both sides and one blue lure pixel; white brow pixels; yellow boots 5 px tall.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
