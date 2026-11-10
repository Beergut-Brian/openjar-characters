# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md, prompts.md | Text, Character writing lane (Claude Code) | Kaden's sheet text kept verbatim where marked; the rest drafted from it | Original work, Open Jar Games |
| jarling.json | Hand-written parameter file for the Jarlings kit | Derived from characters/astro_ana/look.md | Original work, Open Jar Games |
| refs/jarling/astro_ana.glb | Blender 5.2.3 script `avatar/kit/build_jarling.py` (Jarlings kit, procedural, no external assets) | Built from characters/astro_ana/jarling.json | Original work, Open Jar Games |
| refs/jarling/astro_ana_turnaround.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py`, caption by `label_sheet.py` (Pillow) | Front, 3/4, side, back; idle frame 1 | Original work, Open Jar Games |
| refs/jarling/astro_ana_expressions.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py`, caption by `label_sheet.py` (Pillow) | Neutral, happy, surprised, determined (face atlas cells) | Original work, Open Jar Games |
| refs/jarling/astro_ana_kick.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | `kick` action, frame 17 (follow-through), expression determined | Original work, Open Jar Games |
| refs/jarling/astro_ana_side.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | Side view at The Hill's scale (512 px per 1.2 m), transparent background | Original work, Open Jar Games |
| refs/jarling/astro_ana_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | The side render reduced to sprite pixels on a 16 px tile grid (tracing base) | Original work, Open Jar Games |
| refs/pixel/astro_ana_pixel.png | Python 3 + Pillow, `tools/pixel/astro_ana.py` (drawn in code, no external assets, no AI image model) | Front form, 40 x 32 native | Original work, Open Jar Games |
| refs/pixel/astro_ana_frames.png | Python 3 + Pillow, `tools/pixel/astro_ana.py` (drawn in code, no external assets, no AI image model) | The Hill player sheet, 128 x 224 native | Original work, Open Jar Games |
| refs/pixel/astro_ana_frames.json | Python 3, `tools/pixel/astro_ana.py` | Frame manifest (`jarling_frames.manifest`) | Original work, Open Jar Games |
| refs/pixel/astro_ana_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/astro_ana.py` (drawn in code, no external assets, no AI image model) | Review sheet: front x8, frames x4, front 1x/2x, 16 px silhouette | Original work, Open Jar Games |
