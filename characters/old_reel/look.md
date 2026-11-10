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

### Jarling 3D (master, as built)
Built 2026-11-10 from `characters/old_reel/jarling.json` (standard humanoid body, kit v2).
- **body:** `round`, height 1.2, leg_scale 1.05, width 1.1, belly 0.7 (a tall egg in a floppy hat)
- **head:** `round` 1.0; skin `#E0A882`; `buzz` hair `#F2F0EA` mostly under the hat; `bushy` brows `#F2F0EA`
- **headwear:** `bucket_hat` `#C8A97A` (fit 0.55 so the brows clear the brim) with one `lure` `#3F8FD8` pinned at the hat side. The kit lure
  takes one colour, so the sheet's yellow `#F2C230` is not modelled in 3D (it is a pixel in the 2D form)
- **face:** sleepy half-lidded eyes (lid 0.45), `smile`. Kit expression slots: neutral = sleepy smile, happy = chuckle (eyes closed, open
  smile), surprised = almost-had-it (`o`, brows up), determined = set mouth, brows tilted
- **top:** `long` shirt `#F1E7CF` with the `vest` pattern `#A89B6E`; **bottoms:** `shorts` `#6E4B30` tucked into tall boots (the kit's
  `pants` poke brown patches through the boot shaft); **shoes:** `rain_boots` `#F6C833`, height 0.30 (to the knee)
- **ref action:** `idle` frame 1 holding the `fishing_rod` gear (one_hand_raised), seen from yaw 28; `refs/jarling/old_reel_hold.png` is the grip check
- **gear:** `fishing_rod` (cork handle, reel, line to a blue/yellow bobber) in `avatar/gear`

### 2D pixel (The Hill)
See "Alt form: the-hill pixel" below (as built).

## Refs
- `refs/jarling/old_reel.glb`: the 3D master
- `refs/jarling/old_reel_turnaround.png`, `old_reel_expressions.png`, `old_reel_idle.png` (with the fishing rod), `old_reel_hold.png`
- `refs/jarling/old_reel_side.png`, `old_reel_side_sprite.png`: side view and its sprite-scale tracing base
- `refs/pixel/old_reel_pixel.png`, `old_reel_frames.png` (+ `.json`), `old_reel_pixel_sheet.png`: The Hill pixel form

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/old_reel.py` (`old_reel()`)

- **Height:** 32 px with the outline (1.28 m in 3D, squeezed to the frame): hat dome 4 rows + 1 brim row (tips turned down 1 px at
  both ends), face 8 rows, round vest torso 8 rows, 2 rows of pants, yellow boots 5 rows plus a dark sole row.
- **Palette:** hat `#C8A97A` (band `#A88C5E`), lure `#3F8FD8` with a `#F2C230` tip pixel, brows and hair `#F2F0EA`, skin `#E0A882`
  (+ `#C08A64`), shirt `#F1E7CF`, vest `#A89B6E` (+ `#8A7F58`), pants `#6E4B30`, boots `#F6C833` (+ `#C79F1E`, sole `#6B5316`),
  mouth `#6A2232`, outline `#2A1E2C`.
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride, sleep0-1
  (three-quarter view facing right, feet on row 30, hand at (22, 21) idle). No rod in the pixel frames.
- **Should read as:**
  - a soft tan bucket hat (not a helmet, not hair): a 4-row dome, a brim row wider than the head, 1 px turned down at each tip
  - one fishing lure: a 2 px blue block with a yellow pixel on the hat band at the side (not an ear, not a badge on the face)
  - bushy white brows over sleepy eyes: 3-4 white pixels above 1-row half-closed eyes with a shaded lid pixel (not a visor)
  - a gentle smile, nothing at the mouth (no pipe)
  - tall and round: a khaki vest with a cream strip, belly bulging 1 px, brown pants, tall yellow boots that read as rain boots
