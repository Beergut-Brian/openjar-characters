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
- skin: `#9FD6F0`
- antenna stalks: `#7FB9D6` (changed 2026-11-10 by the build, director's translation: was skin `#9FD6F0`; a shade darker so the stalks read against the head)
- antenna bobbles: `#FFD23F` (accent)
- headband: `#C9CED4`
- shirt yellow: `#FFD23F`
- shirt pink: `#FF7EB9`
- shirt light pink: `#FFA9D0` (added 2026-11-10 for the print's second accent, replacing the kit example's orange; tool-checked by `tools/check_colours.py`)
- shorts: `#F5F5F2`
- sandals: `#C89A63`

## Signature props
- Antennae: grown, not worn. Two antennae with yellow bobbles are a head feature (`head.features`, species; Gary's call 2026-11-10); they bob with the head's secondary motion
- Headband: worn (silver headwear, Kaden's sheet names it); the antennae rise clear above it
- Optional imaginary camera (mimed)

## Per-technique notes

### Jarling 3D (master)
Built on the standard humanoid Jarling body (`avatar/kit`) from `characters/zorp/jarling.json`; same skeleton, actions, ten equipment slots and gameplay collision as every playable character. Height 1.375 m to the bobble tops.
- **body:** `slim`, height 1.05, width 0.85, leg_scale 1.0, no belly
- **head:** `tall`, size 1.05, ears `none`; skin `#9FD6F0`; hair `none`
- **head feature:** `antennae`, count 2, stalks `#7FB9D6`, bobbles `#FFD23F`, `ball` 0.2, `length` 0.8, `spread` 28, `back` 15 (tilted outward and slightly back, never over the face; both bobbles show from the front and 3/4)
- **headwear:** `headband` `#C9CED4`
- **top:** `tee` `#FFD23F` with the `vacation` pattern: accent `#FF7EB9`, accent2 (leaves) `#FFA9D0`, flower centre `#FFD23F` (the example's orange dropped: yellow-and-pink only)
- **bottoms:** `shorts` `#F5F5F2`; **shoes:** `sandals` `#C89A63`
- **face:** eyes `round`, brows `thin`, nose `none`, mouth `o`, blush 0.5. neutral = amazed (eye_scale 1.15, `o`); happy = delighted (arc eyes, `smile`); surprised = eyes wider (eye_scale 1.35, `o`); determined = puzzled (left brow up via `brow_raise_left` 0.06, `flat` mouth)
- **ref action:** `cheer` frame 7 (both arms up), happy
- **new kit param:** `antennae.back` (deg, default 0 = old shape) in `avatar/kit/pieces_features.py` `antennae()`
- **bobbing:** each antenna has its own bone (`feat_antenna.1`, `feat_antenna.2`, children of `head`) and copies the comb's secondary bob (amount 1.6, mirrored sideways sway) in every standard action that keys it (idle, cheer...). No separate spring; games can add spring motion on those two bones.

## Refs
- `refs/jarling/`: `zorp.glb`, `zorp_turnaround.png`, `zorp_expressions.png`, `zorp_cheer.png`, `zorp_side.png`, `zorp_side_sprite.png`
- `refs/pixel/`: `zorp_pixel.png`, `zorp_frames.png`, `zorp_frames.json`, `zorp_pixel_sheet.png`

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/zorp.py` (`zorp()`)

- **Height:** 30 px drawn, 32 px with the outline (the frame limit). At true scale Zorp's head, body and legs alone already fill 32 px (1.19 m) and the antennae add about 5 px, so shortening only the stalks could not fit: the antennae keep their minimum (1 px stalks 2 px high plus 2x2 bobbles = 4 px) and head, body and legs are squeezed evenly to 26 px (head 12, shirt 6, shorts 3, legs 3, sandals 2), keeping the 3D head-to-body ratio.
- **Palette:** skin `#9FD6F0` (far side `#7FB9D6`), stalks `#7FB9D6`, bobbles `#FFD23F`, headband `#C9CED4`, shirt `#FFD23F` (far sleeve `#E8B92A`) with `#FF7EB9` and `#FFA9D0` pixels, shorts `#F5F5F2` (`#D9D9D4`), sandals `#C89A63` (far `#A57B4B`), outline and eyes `#2A1E2C`.
- **Frames:** idle0 idle1 walk0-3 jump fall side0-2 down0-2 (+ ride, sleep0-1 from `jarling_frames.sheet`), three-quarter facing right, feet centre x=16 on row 30, `HAND = (22, 21)`; hands at The Hill's POSES positions for the dig frames.
- **Should read as:**
  - two antennae with yellow bobbles growing from the head (not a hat, not horns, not ears): 1 px stalks in a V, 2x2 bobbles, part of the outline and of the 16 px silhouette
  - silver headband: one `#C9CED4` row across the head, 1 px proud of each side
  - loud holiday shirt: yellow block with scattered pink pixels, open collar
  - white shorts and sandals: white block, tan sole line with a skin-blue foot and one strap pixel
  - small amazed mouth: one 2 px dark `o`, nothing near it
