# Asset credits

Design: Kaden's Life of a Worm brief 2026-11-10 (bible approved, Docket D89).

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md, prompts.md | Text, Character director lane (Claude Code) | Drafted from the approved bible; colours checked with `tools/check_colours.py` | Original work, Open Jar Games |
| refs/pixel/bobber_pixel.png | Python 3 + Pillow, `tools/pixel/bobber.py` (drawn in code, no external assets, no AI image model) | Front pixel form, native 40 x 32 | Original work, Open Jar Games |
| refs/pixel/bobber_frames.png | Python 3 + Pillow, `tools/pixel/bobber.py` (drawn in code, no external assets, no AI image model) | The Hill player sheet, native 128 x 224 | Original work, Open Jar Games |
| refs/pixel/bobber_frames.json | Python 3 + Pillow, `tools/pixel/bobber.py` (drawn in code, no external assets, no AI image model) | Frame manifest for the sheet (`jarling_frames.manifest`) | Original work, Open Jar Games |
| refs/pixel/bobber_sit_dock.png | Python 3 + Pillow, `tools/pixel/bobber.py` (drawn in code, no external assets, no AI image model) | Life of a Worm sitting-on-the-dock pose, frames 0 and 1 side by side, native 64 x 48 | Original work, Open Jar Games |
| refs/pixel/bobber_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/bobber.py` (drawn in code, no external assets, no AI image model) | Review sheet: front x8, frames x4, front 1x/2x, 16 px silhouette x4, sit_dock x4 | Original work, Open Jar Games |
| ../bobber_read_check.png | Python 3 + Pillow, `tools/pixel/bobber_sheets.py` (pixel art drawn in code; the 3D side view is `refs/jarling/bobber_side.png`) | Read check: 3D side view, pixel form x8, idle frame x8, x1/x2/x3 on sky and dirt, sit_dock x4 on a plank, 16 px silhouettes, should-read-as notes | Original work, Open Jar Games |
| jarling.json, refs/jarling/bobber.glb | Blender 5.2.3 bmesh, `avatar/kit/build_jarling.py` (new kit pieces `rain_hat`, `hstripes`, shorts `cuff`, face `wink`, all made in code) | 3D master from look.md; no external assets, no AI image model | Original work, Open Jar Games |
| refs/jarling/bobber_turnaround.png, bobber_side.png, bobber_expressions.png, bobber_cheer.png | Blender 5.2.3 Cycles CPU, `avatar/kit/render_refs.py` (48 samples) + `avatar/kit/label_sheet.py` | Turnaround, side view, four expressions, cheer with the kid rod (happy, frame 13, yaw -50) | Original work, Open Jar Games |
| refs/jarling/bobber_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | The side view at sprite scale (tracing base) | Original work, Open Jar Games |
| refs/jarling/bobber_hold.png | Blender 5.2.3 Cycles CPU, `avatar/kit/render_hold.py --adhoc` (24 samples), joined with Pillow + `label_sheet.py` | Kid rod held in idle, cheer, run (front, 3/4); fist-to-grip check | Original work, Open Jar Games |
| ../bobber_lineup.png | Blender 5.2.3 Cycles CPU, `avatar/kit/render_range.py --lineup` (32 samples) + `label_sheet.py` | Jeff, Chuck, Old Reel and Bobber at true scale on one ground line | Original work, Open Jar Games |
