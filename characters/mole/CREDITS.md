# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| refs/look_sheet.png | Python 3 + Pillow, `tools/pixel/make_sheets.py` (drawn in code, no external assets, no AI image model) | look sheet (approved by Kaden 2026-11-09, D46 a): turnaround, key poses, expressions, arc pictograms | Original work, Open Jar Games |
| `characters/residents_lineup.png` | Python 3 + Pillow, `tools/pixel/make_sheets.py` (drawn in code, no external assets, no AI image model) | lineup for scale: Jeff and Chuck pixel forms plus the four Hill residents | Original work, Open Jar Games |
| jarling.json | hand-written parameters | The Mole's 3D master: body type `critter` (`avatar/kit/body_critter.py`), colours from look.md | Original work, Open Jar Games |
| refs/jarling/mole.glb | Blender 5.2.3, `avatar/kit/build_jarling.py` + `avatar/kit/body_critter.py` (procedural, no external assets, no AI image model) | 3D master: pear body, snout, claws, shovel prop; actions idle, run, cheer, popup, bow | Original work, Open Jar Games |
| refs/jarling/mole_turnaround.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py`, labelled with `avatar/kit/label_sheet.py` | front, 3/4, side, back of mole.glb | Original work, Open Jar Games |
| refs/jarling/mole_expressions.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py`, labelled with `avatar/kit/label_sheet.py` | squint, happy, sorry, hopeful, startled | Original work, Open Jar Games |
| refs/jarling/mole_bow.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py` | the apology bow at its deepest (frame 16), expression sorry | Original work, Open Jar Games |
| refs/jarling/mole_side.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py` | orthographic side view, 512 px per 1.2 m: tracing base for the 2D sprite | Original work, Open Jar Games |
| refs/jarling/mole_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | mole_side.png reduced to The Hill's sprite scale on a 16 px tile grid | Original work, Open Jar Games |
| `characters/residents_3d_lineup.png` | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_residents.py --only lineup` (procedural Jarling kit, no external assets, no AI image model) | Jeff, Chuck and the four Hill residents in 3D at true relative scale on one ground line (3D forms proposed 2026-11-10) | Original work, Open Jar Games |
| `characters/residents_3d_compare.png` | `avatar/kit/render_residents.py --only fronts` + Pillow `avatar/kit/compare_sheet.py` | each resident's 3D master (front, idle) beside its approved 2D sprite from `tools/pixel/residents.py` | Original work, Open Jar Games |
