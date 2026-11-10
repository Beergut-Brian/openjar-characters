# Patience the Cow: look

Body type `quadruped` (avatar/kit/body_quadruped.py), its first character. Designed 3D-first: the
Jarling below is the master for silhouette, proportions and colours; the pixel form is traced from it.

## Must survive every art style
- A white barrel body on four short stub legs with dark hooves, black patches, a tufted tail.
- A big round Jarling head low on the front, with a wide pink muzzle and two nostrils.
- One black patch over her right eye (on your left as you look at her), two short cream horns, side ears with pink insides.
- Heavy-lidded, slightly smug resting eyes with two lashes.

## Silhouette
Horizontal: about 1.5 times as long as she is tall, head at the front as high as the top of her back.
About the height of a standard Jarling (1.07 m to the top of her head, 1.56 m nose to tail).
Reads as "cow" from the side at 16 px: four legs, a head with a snout, a tail with a tuft.

## Face
Standard face atlas on the front of the head, six expressions (the yard's reaction list): `neutral`
(half-lidded, small smile: her resting face), `happy` (closed arcs, smile, blush), `wide_eyed`
(raised brows, small "o"), `dizzy` (spirals, wobbly mouth), `smug` (heavy lids, one brow up, smirk),
`panicked` (tiny pupils, worried brows, open mouth, sweat drop). The mouth and nostrils are drawn on
the muzzle. Strokes over the face patch get a white rim so they read on black.

## Fixed colours
- Coat (head, legs, body): #F4F1EA
- Patches, tail tuft: #2B2B33
- Muzzle and inner ears: #F2B8C0
- Nostrils: #B85C70
- Horns: #E8CF9A
- Hooves: #4A3B3B
- Eyes and lines: #2A1E2C; outline in pixel art: #2A1E2C
- Not playable, so the player-colour rule does not bind her, but her main colours keep clear of both
  anyway (Delta E 2000 from P1 green / P2 red): coat 32.5 / 43.4, patches 58.4 / 40.7, muzzle 56.0 / 29.9,
  horns 29.6 / 42.0, hooves 57.2 / 32.5. The nostrils (15.4 from P2) are a two-pixel detail.

## Signature props
None of her own. She carries things in her mouth (slot `mouth`, hold style `in_mouth`): the proof item
is the pail (`avatar/gear/pail`). Gear on head, face, back and waist fits (hat, sunglasses, a balloon
tie on her back, a belt as a girth strap).

## Jarling 3D
`jarling.json` in this folder. Body `height` 0.95, `length` 1.0, `girth` 0.27, `width` 0.98, `leg` 0.24,
`head` 0.22. Coat pattern `patches` with five placed patches; snout `muzzle`; ears `side`; horns `nubs`
(a body feature, part `feature_horns`, never a hat); hooves; tail `tuft`.
Actions: `idle` (chew, tail flick), `run` (trot), `cheer` (hop), `tipped` (on her side, legs out),
`stiff` (the same legs-out pose without the roll, for a physics body that has rolled over by itself),
`graze`, `sit`.

## 2D pixel (The Hill)
Traced from the 3D master with `avatar/kit/render_trace.py --params proposals/cow/jarling.json` and
`tools/pixel/cow.py` (majority vote per pixel on the fixed palette, a small hand-clean for the eye and
nostril pixels, the 1 px outline). True scale: 29 px tall on a 48 x 32 frame (Jeff with his comb is
32 px). Poses: side, front, back, trot (2 frames), graze, tipped, panicked; plus 16 px versions.
Sprites: `refs/pixel/`. Sheet: `refs/cow_pixel_sheet.png`.

## Refs
- `refs/jarling/cow.glb`: the 3D master (Godot-ready)
- `refs/jarling/cow_turnaround.png`, `cow_expressions.png`, `cow_tipped.png`, `cow_actions.png`, `cow_side.png`, `cow_side_sprite.png`
- `refs/cow_pixel_sheet.png`, `refs/pixel/*.png`
- `refs/cow_read_check.png`: 16 px, x1/x2/x4, and tiny to giant at Junk Yard Zap's grow/shrink steps
