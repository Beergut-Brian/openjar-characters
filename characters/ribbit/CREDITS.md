# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md, prompts.md | Text, Character writing lane (Claude Code) | Kaden's sheet text kept verbatim where marked; the rest drafted from it | Original work, Open Jar Games |
| jarling.json | Hand-written parameter file for the Jarlings kit | Derived from characters/ribbit/look.md (Kaden's sheet 2026-11-10) | Original work, Open Jar Games |
| refs/jarling/ribbit.glb | Blender 5.2.3 script `avatar/kit/build_jarling.py` (Jarlings kit, procedural, no external assets) | Built from characters/ribbit/jarling.json; hop gait from `avatar/kit/pieces_gait.py` | Original work, Open Jar Games |
| refs/jarling/ribbit_turnaround.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py`, caption by `label_sheet.py` (Pillow) | Front, 3/4, side, back; idle frame 1 | Original work, Open Jar Games |
| refs/jarling/ribbit_expressions.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py`, caption by `label_sheet.py` (Pillow) | Neutral, happy, surprised, determined (face atlas cells) | Original work, Open Jar Games |
| refs/jarling/ribbit_run.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | `run` action (hop), frame 8 (top of the hop), neutral face | Original work, Open Jar Games |
| refs/jarling/ribbit_side.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` `--only side` | Side view at The Hill's sprite scale (512 px per 1.2 m) | Original work, Open Jar Games |
| refs/jarling/ribbit_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | Side render reduced to The Hill's sprite pixels (tracing base) | Original work, Open Jar Games |
| refs/pixel/ribbit_pixel.png | Python 3 + Pillow, `tools/pixel/ribbit.py` (drawn in code, no external assets, no AI image model) | Front pixel form, 40 x 32 | Original work, Open Jar Games |
| refs/pixel/ribbit_frames.png | Python 3 + Pillow, `tools/pixel/ribbit.py` (drawn in code, no external assets, no AI image model) | The Hill player sheet, 128 x 224 (hop walk row) | Original work, Open Jar Games |
| refs/pixel/ribbit_frames.json | Python 3 + Pillow, `tools/pixel/ribbit.py` (drawn in code, no external assets, no AI image model) | Frame manifest (`jarling_frames.manifest`) | Original work, Open Jar Games |
| refs/pixel/ribbit_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/ribbit.py` (drawn in code, no external assets, no AI image model) | Review sheet: front x8, frame sheet x4, front x1 and x2, 16 px silhouette x4 | Original work, Open Jar Games |
