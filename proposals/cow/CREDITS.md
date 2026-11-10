# Asset credits

| File | Tool / source | Prompt or notes | License |
| --- | --- | --- | --- |
| bible.md, look.md, voice.md | Text, Character lane (Claude Code) | written from D52 a and the Junk Yard Zap / The Hill design docs | Original work, Open Jar Games |
| jarling.json | hand-written parameters | the cow's 3D master: body type `quadruped` (`avatar/kit/body_quadruped.py`), colours from look.md | Original work, Open Jar Games |
| refs/jarling/cow.glb | Blender 5.2.3, `avatar/kit/build_jarling.py` + `avatar/kit/body_quadruped.py` (procedural, no external assets, no AI image model) | 3D master: barrel body, Jarling head with face atlas, muzzle, side ears, horn nubs, hooves, tufted tail; actions idle, run, cheer, tipped, stiff, graze, sit | Original work, Open Jar Games |
| refs/jarling/cow_turnaround.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py`, labelled with `avatar/kit/label_sheet.py` | front, 3/4, side, back of cow.glb | Original work, Open Jar Games |
| refs/jarling/cow_expressions.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py`, labelled with `avatar/kit/label_sheet.py` | neutral, happy, wide_eyed, dizzy, smug, panicked | Original work, Open Jar Games |
| refs/jarling/cow_tipped.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py` (`ref_action`) | tipped onto her side, dizzy | Original work, Open Jar Games |
| refs/jarling/cow_actions.png | Blender 5.2.3 Cycles, `avatar/kit/render_quadruped.py --only actions` (captions in Pillow); the pail is `avatar/gear/pail` on the mouth slot | trot, hop, tipped, stiff, graze, sit, idle with the pail | Original work, Open Jar Games |
| refs/jarling/cow_side.png | Blender 5.2.3 Cycles, `avatar/kit/render_refs.py` | orthographic side view, 512 px per 1.2 m: tracing base for the 2D sprite | Original work, Open Jar Games |
| refs/jarling/cow_side_sprite.png | Python 3 + Pillow, `avatar/kit/sprite_side.py` | cow_side.png reduced to The Hill's sprite scale on a 16 px tile grid | Original work, Open Jar Games |
| refs/pixel/*.png | Python 3 + Pillow, `tools/pixel/cow.py` from `avatar/kit/render_trace.py --params proposals/cow/jarling.json` flat renders (no AI image model) | pixel form traced from the 3D master: side, front, back, trot x2, graze, tipped, panicked, and 16 px versions | Original work, Open Jar Games |
| refs/cow_pixel_sheet.png | Python 3 + Pillow, `tools/pixel/cow.py` | every pixel pose at x6 on The Hill's 16 px grid | Original work, Open Jar Games |
| refs/cow_read_check.png | Python 3 + Pillow, `tools/pixel/cow.py` (pixel Jeff from `tools/pixel/residents.py`); the 3D strip from `avatar/kit/render_quadruped.py --only scale` (Blender 5.2.3 Cycles) | read check: x1/x2/x4, 16 px tall and silhouette, Junk Yard Zap grow/shrink steps beside Jeff | Original work, Open Jar Games |

No audio in `voice/` yet. Add one row per `.ogg` when the barks are recorded.
