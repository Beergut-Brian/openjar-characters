# Asset credits

Design: Kaden's sheet 2026-11-10.

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md, prompts.md | Text, Character director lane (Claude Code) | Kaden's sheet text kept verbatim where marked; the rest drafted from it and the producer's starting picks | Original work, Open Jar Games |
| refs/pixel/yoji_pixel.png | Python 3 + Pillow, `tools/pixel/yoji.py` (drawn in code, no external assets, no AI image model) | Front pixel form, native 40 x 32 | Original work, Open Jar Games |
| refs/pixel/yoji_frames.png | Python 3 + Pillow, `tools/pixel/yoji.py` (drawn in code, no external assets, no AI image model) | The Hill player sheet, native 128 x 224 | Original work, Open Jar Games |
| refs/pixel/yoji_frames.json | Python 3 + Pillow, `tools/pixel/yoji.py` (drawn in code, no external assets, no AI image model) | Frame manifest for the sheet (`jarling_frames.manifest`) | Original work, Open Jar Games |
| refs/pixel/yoji_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/yoji.py` (drawn in code, no external assets, no AI image model) | Review sheet: front x8, frames x4, front 1x/2x, 16 px silhouette x4 | Original work, Open Jar Games |
| ../yoji_read_check.png | Python 3 + Pillow, `tools/pixel/yoji_sheets.py` (pixel art drawn in code; the 3D side view is `refs/jarling/yoji_side.png`) | Read check: 3D side view, pixel form x8, idle frame x8, x1/x2/x3 on sky and dirt, 16 px silhouettes, should-read-as notes | Original work, Open Jar Games |
| jarling.json, refs/jarling/yoji.glb | Blender 5.2.3 bmesh, `avatar/kit/build_jarling.py` (kit pieces `cowboy_hat`, `jersey`, `boxers`, `high_tops`, `shoulder_pads`, all made in code) | 3D master from look.md; no external assets, no AI image model | Original work, Open Jar Games |
| refs/jarling/yoji_turnaround.png, yoji_expressions.png, yoji_cheer.png, yoji_side.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py` (64 samples) + `avatar/kit/label_sheet.py` | Turnaround, four expressions, cheer (happy, frame 13), orthographic side view | Original work, Open Jar Games |
| refs/jarling/yoji_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | The side view at The Hill's sprite scale (tracing base) | Original work, Open Jar Games |
