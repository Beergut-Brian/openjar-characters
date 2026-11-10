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

### Jarling 3D (master, built 2026-11-10 by the Jarlings batch 1 lane)
Params: `characters/ribbit/jarling.json`. Standard humanoid Jarling body, same skeleton, slots and gameplay collision as everyone.
- **body:** build `round`, height 0.85, leg_scale 0.85, width 1.1, belly 0.4
- **head:** `round`, size 1.05, ears none; skin `#F0BE94`; hair `none` (hood up)
- **headwear:** `animal_hood` `#2A9DB0` with `eyes` (white `#F5F5F2`, pupil `#15151A`, size 1.25, el 60, apart 30): two big frog eyes sitting on top of the hood, pupils forward; the face opening shows eyes, brows and the whole smile
- **top:** `long` `#2A9DB0` with pattern `belly_panel` `#F6D44A`; **bottoms:** `shorts` `#22336B`; **shoes:** `footies` `#F6D44A` (the bare-look frog feet)
- **face:** eyes `drop`, brows `soft`, nose `dot`, mouth `wide`; neutral = pleased (half-lidded, lid 0.45, wide flat smile); happy = mellow (closed arcs, wide smile); surprised = fly-alert (eyes wide, small `o`); determined = the calm face with brows slightly down
- **gait:** new kit param `"gait": "hop"` (`avatar/kit/pieces_gait.py`): `run` is a two-footed hop (crouch, push off, tucked in the air with the root rising 0.14, land with a squash), `idle` settles and gives a small bounce now and then. Cosmetic only: same names, lengths and loops as everyone (`run` 1-17 loop, `idle` 1-49 loop), root stays at the origin in X/Y, `kick` and `cheer` unchanged. Rig extra `jarling_gait: "hop"`.
- **ref action:** `run` frame 8 (top of the hop, both feet off the ground), neutral face
- **gear:** none

## Refs
- `refs/jarling/ribbit.glb`, `ribbit_turnaround.png`, `ribbit_expressions.png`, `ribbit_run.png` (top of the hop), `ribbit_side.png`, `ribbit_side_sprite.png`
- `refs/pixel/ribbit_pixel.png`, `ribbit_pixel_sheet.png`, `ribbit_frames.png`, `ribbit_frames.json`

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/ribbit.py` (`ribbit()`). 26 px tall drawn (28 with the outline); the 3D traces 31 px at The Hill's scale, compressed mostly in the hood so Ribbit reads small next to Jeff (32 px) and the hop fits in the frame. Palette: hoodie `#2A9DB0` (shade `#1F7F8F`), hood eyes `#F5F5F2` with pupils `#15151A`, skin `#F0BE94` (shade `#D9A27A`), belly panel and footies `#F6D44A` (shade `#D9B630`), shorts `#22336B` (shade `#18264F`), blush `#F2A08C`, outline `#2A1E2C`. Frames: idle0 idle1 (1 px settle), walk0-walk3 = a two-footed hop (crouch, push off, top of the hop lifted 4 px with feet tucked, landing squash), jump, fall, side0-side2, down0-down2, plus the shared ride and sleep rows; manifest `refs/pixel/ribbit_frames.json`. Wide flat smile: one dark 5 px line, nothing near the mouth.
- Should read as: a frog hood with two big frog eyes on top (not ears, not a bow, not goggles): two 3x3 white balls with a dark pupil, 1 px of teal between them.
- Should read as: yellow belly panel: a yellow oval block on the teal torso.
- Should read as: bare yellow frog feet (shoes): two yellow footie blocks with toe-split pixels under dark blue shorts.
