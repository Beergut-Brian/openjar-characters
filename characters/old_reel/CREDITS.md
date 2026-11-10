# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md, prompts.md | Text, Character writing lane (Claude Code) | Kaden's sheet text kept verbatim where marked; the rest drafted from it | Original work, Open Jar Games |
| jarling.json | Hand-written parameter file for the Jarlings kit | Derived from characters/old_reel/look.md | Original work, Open Jar Games |
| refs/jarling/old_reel.glb | Blender 5.2.3 script `avatar/kit/build_jarling.py` (Jarlings kit, procedural, no external assets) | Built from characters/old_reel/jarling.json | Original work, Open Jar Games |
| refs/jarling/old_reel_turnaround.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | Front, 3/4, side, back; idle frame 1 | Original work, Open Jar Games |
| refs/jarling/old_reel_expressions.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | Neutral, happy, surprised, determined (face atlas cells) | Original work, Open Jar Games |
| refs/jarling/old_reel_idle.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | `idle` frame 1 holding the fishing rod gear (`avatar/gear/fishing_rod.glb`), yaw 28 | Original work, Open Jar Games |
| refs/jarling/old_reel_hold.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_hold.py --adhoc old_reel:fishing_rod:idle:1` | Grip check: fist closes on the cork handle | Original work, Open Jar Games |
| refs/jarling/old_reel_side.png | Blender 5.2.3 Cycles (CPU) via `avatar/kit/render_refs.py` | Orthographic side view, transparent (tracing base for 2D) | Original work, Open Jar Games |
| refs/jarling/old_reel_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | The side view at The Hill's sprite scale | Original work, Open Jar Games |
| refs/pixel/old_reel_pixel.png | Python 3 + Pillow, `tools/pixel/old_reel.py` (drawn in code, no external assets, no AI image model) | Front pixel form, native 40 x 32 | Original work, Open Jar Games |
| refs/pixel/old_reel_frames.png | Python 3 + Pillow, `tools/pixel/old_reel.py` (drawn in code, no external assets, no AI image model) | The Hill player sheet, native 128 x 224 | Original work, Open Jar Games |
| refs/pixel/old_reel_frames.json | Python 3 + Pillow, `tools/pixel/old_reel.py` (drawn in code, no external assets, no AI image model) | Frame manifest for the sheet (`jarling_frames.manifest`) | Original work, Open Jar Games |
| refs/pixel/old_reel_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/old_reel.py` (drawn in code, no external assets, no AI image model) | Review sheet: front x8, frames x4, front 1x/2x, 16 px silhouette x4 | Original work, Open Jar Games |

No audio in `voice/` yet. Add one row per file when it is made.
