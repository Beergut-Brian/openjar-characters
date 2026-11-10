# The Mole: look

## Must survive every art style
- A pear shape: no neck, no visible legs.
- Pointy pink snout and huge pink digging claws.
- A squint: two dashes for eyes. They open as 1 px dots only when he is startled.
- Slate fur, not brown, so he reads against dirt.
- The stolen shovel held upright in both claws like a bouquet, blade up beside his head.

## Silhouette
A pear with a pointed snout at the top and two big claws wrapped round a shovel handle. Identifiable in outline alone.

## Face
Squint (neutral), happy, sorry, hopeful, startled. The nose tip is a darker pink dot.

## Fixed colours
- Fur: #56607A
- Belly: #8792AC
- Snout, claws, feet and tail: #F2A0A8
- Nose tip: #E0607A
- Shovel wood: #B07A3C
- Shovel steel: #B8C4D0
- Outline in pixel art: #2A1E2C

## Signature props
The shovel (wood handle, steel blade). It is the only prop, and it is always carried upright.

## Jarling 3D
Status of the 3D form: **proposed** (Character lane 2026-11-10, awaiting Kaden). The 2D look above is approved (D46 a). Since Kaden's 3D-first direction (2026-11-10) this model is meant to become the master for silhouette, proportions and colours, and the 2D sprites get redrawn from `refs/jarling/mole_side.png` / `mole_side_sprite.png`.
- **Body type: `critter`** (`avatar/kit/body_critter.py`), not the standard body: a pear with no neck and no visible legs cannot be made from a head-on-torso-on-legs humanoid, and the type is reusable for other small round animals. `jarling.json`: `body.type` critter, `body.height` 0.82 (about 0.9 m to the top of the head; Jeff is 1.2 m with his comb).
- Shape: two overlapping rigid blobs (head on `head`, body on `spine`) that read as one pear, widest low down. Slate fur, lighter belly oval, chunky pink snout with the darker nose tip, huge pink three-lobed digging claws on short arms, small pink feet peeking out in front, a pink tail nub. No ears.
- Face (atlas, five cells): `squint` (resting: two dashes), `happy`, `sorry`, `hopeful`, `startled` (two tiny dots).
- The shovel is part `prop` on its own bone `prop`: held upright in both claws like a bouquet, blade up beside his head on his right. Games can hide it (he gives it back).
- Bones: the shared eleven plus `prop`. Actions: `idle`, `run` (his shuffle), `cheer`, `popup` (the signature pop-up out of the ground), `bow` (the apology).
- Equipment slots: head, face, back, waist, both hands, both feet. No knees, so `knee_l/r` are reported missing and kneepads are refused.
- Files: `jarling.json`, `refs/jarling/mole.glb`, `mole_turnaround.png`, `mole_expressions.png`, `mole_bow.png`, `mole_side.png`, `mole_side_sprite.png`.
- Changes from the 2D look: in the lineup sprite his claws hang out at his sides with no shovel; the 3D rest pose is the look sheet's rule instead (shovel always carried upright in both claws). He is about three quarters of Jeff's height rather than the same 32 px. Not built: the fall-in-the-pond pose.

## 2D pixel (The Hill)
- 32 px tall including a 1 px #2A1E2C outline, on 16 px tiles, drawn on a 40 x 32 canvas.
- Must still read at 16 px: the pear body, the pink snout and the shovel blade beside his head.
- Poses: idle shuffle, pop-up from a mound, carry shovel, apologise (small bow), fall in pond.
- Expressions: squint (neutral), happy, sorry, hopeful, startled.

## Refs
`refs/look_sheet.png` (turnaround, key poses, expressions, arc pictograms) and `characters/residents_lineup.png` for scale.
