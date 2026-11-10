# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| refs/look_sheet.png | Python 3 + Pillow, `tools/pixel/make_sheets.py` (drawn in code, no external assets, no AI image model) | look sheet (approved by Kaden 2026-11-09, D46 a): turnaround, key poses, expressions, arc pictograms | Original work, Open Jar Games |
| `characters/residents_lineup.png` | Python 3 + Pillow, `tools/pixel/make_sheets.py` (drawn in code, no external assets, no AI image model) | lineup for scale: Jeff and Chuck pixel forms plus the four Hill residents | Original work, Open Jar Games |
| refs/jarling/gnome_foreman.glb | Blender 5.2 headless, `avatar/kit/build_jarling.py` + `avatar/kit/pieces_hill.py` (built in code, no external assets, no AI image model) | standard-body Jarling from `jarling.json`: cone hat, detachable hard hat, beard, vest, clipboard, whistle on its own bones; actions incl. march, write, salute, whistle | Original work, Open Jar Games |
| refs/jarling/gnome_foreman_turnaround.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` + `label_sheet.py` | turnaround (front, 3/4, side, back), 64 samples | Original work, Open Jar Games |
| refs/jarling/gnome_foreman_expressions.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` + `label_sheet.py` | stern, approving, sorry, hopeful, whistle (whistle cell posed at the whistle action, frame 16), 64 samples | Original work, Open Jar Games |
| refs/jarling/gnome_foreman_write.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` | action sheet: write, stern face, 64 samples | Original work, Open Jar Games |
| refs/jarling/gnome_foreman_side.png | Blender 5.2 Cycles, `avatar/kit/render_refs.py` | side view, 64 samples | Original work, Open Jar Games |
| refs/jarling/gnome_foreman_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | side render at The Hill sprite scale (tracing base) | Original work, Open Jar Games |
| `characters/residents_3d_lineup.png` | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_residents.py --only lineup` (procedural Jarling kit, no external assets, no AI image model) | Jeff, Chuck and the four Hill residents in 3D at true relative scale on one ground line (3D forms approved 2026-11-10, D49 a) | Original work, Open Jar Games |
| `characters/residents_3d_compare.png` | `avatar/kit/render_residents.py --only fronts` + Pillow `avatar/kit/compare_sheet.py` | each resident's 3D master (front, idle) beside its 3D-first pixel redraw from `tools/pixel/residents.py` | Original work, Open Jar Games |
| `characters/read_check.png` | Python 3 + Pillow, `tools/pixel/read_check.py` (3D side views from `avatar/kit/render_trace.py` / `render_refs.py`) | every library character: 3D side view, pixel form at 1x and at game scale (x2), 16 px silhouette, and what each prop should read as | Original work, Open Jar Games |
