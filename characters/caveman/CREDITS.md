# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| refs/look_sheet.png | Python 3 + Pillow, `tools/pixel/make_sheets.py` (drawn in code, no external assets, no AI image model) | look sheet (approved by Kaden 2026-11-09, D46 a): turnaround, key poses, expressions, arc pictograms | Original work, Open Jar Games |
| `characters/residents_lineup.png` | Python 3 + Pillow, `tools/pixel/make_sheets.py` (drawn in code, no external assets, no AI image model) | lineup for scale: Jeff and Chuck pixel forms plus the four Hill residents | Original work, Open Jar Games |
| refs/jarling/caveman.glb | Blender 5.2 headless, `avatar/kit/build_jarling.py` + `avatar/kit/pieces_hill.py` (built in code, no external assets, no AI image model) | standard-body Jarling from `jarling.json`: mane hair + beard, ice cube, one-shoulder fur tunic, cloth club; actions incl. polish, point, wave | Original work, Open Jar Games |
| refs/jarling/caveman_turnaround.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` + `label_sheet.py` | turnaround (front, 3/4, side, back), 64 samples | Original work, Open Jar Games |
| refs/jarling/caveman_expressions.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` + `label_sheet.py` | delighted, baffled, sorry, hopeful, amazed, 64 samples | Original work, Open Jar Games |
| refs/jarling/caveman_polish.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` | action sheet: polish, delighted face, 64 samples | Original work, Open Jar Games |
| refs/jarling/caveman_side.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` | side view, 64 samples | Original work, Open Jar Games |
| refs/jarling/caveman_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | side render at The Hill sprite scale (tracing base) | Original work, Open Jar Games |
| `characters/residents_3d_lineup.png` | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_residents.py --only lineup` (procedural Jarling kit, no external assets, no AI image model) | Jeff, Chuck and the four Hill residents in 3D at true relative scale on one ground line (3D forms approved 2026-11-10, D49 a) | Original work, Open Jar Games |
| `characters/residents_3d_compare.png` | `avatar/kit/render_residents.py --only fronts` + Pillow `avatar/kit/compare_sheet.py` | each resident's 3D master (front, idle) beside its 3D-first pixel redraw from `tools/pixel/residents.py` | Original work, Open Jar Games |
