# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md, prompts.md | Text, Character writing lane (Claude Code) | Kaden's sheet text kept verbatim where marked; the rest drafted from it | Original work, Open Jar Games |
| jarling.json | Hand-written parameter file for the Jarlings kit | Derived from characters/zorp/look.md | Original work, Open Jar Games |
| refs/jarling/zorp.glb | Blender 5.2.3 script `avatar/kit/build_jarling.py` (Jarlings kit, procedural, no external assets) | Built from characters/zorp/jarling.json | Original work, Open Jar Games |
| refs/jarling/zorp_turnaround.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py`, caption by `label_sheet.py` (Pillow) | Front, 3/4, side, back; idle frame 1 | Original work, Open Jar Games |
| refs/jarling/zorp_expressions.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py`, caption by `label_sheet.py` (Pillow) | Neutral (amazed), happy (delighted), surprised, determined (puzzled) (face atlas cells) | Original work, Open Jar Games |
| refs/jarling/zorp_cheer.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | `cheer` action, frame 7 (both arms up), happy | Original work, Open Jar Games |
| refs/jarling/zorp_side.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | Side view at The Hill's tracing scale (512 px per 1.2 m) | Original work, Open Jar Games |
| refs/jarling/zorp_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | zorp_side.png on the 16 px tile grid and reduced to sprite pixels (tracing base) | Original work, Open Jar Games |
| refs/pixel/zorp_pixel.png | Python 3 + Pillow, `tools/pixel/zorp.py` (drawn in code, no external assets, no AI image model) | Front form, native 40 x 32 | Original work, Open Jar Games |
| refs/pixel/zorp_frames.png | Python 3 + Pillow, `tools/pixel/zorp.py` | The Hill player sheet, native 128 x 224 | Original work, Open Jar Games |
| refs/pixel/zorp_frames.json | Python 3, `tools/pixel/zorp.py` (`jarling_frames.manifest`) | Frame layout, pivot and hand position | Original work, Open Jar Games |
| refs/pixel/zorp_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/zorp.py` | Review sheet: front x8, frames x4, front 1x and x2, 16 px silhouette x4 | Original work, Open Jar Games |
