#!/usr/bin/env bash
# Re-trace the Hill residents' pixel forms from the 3D masters, in one go. Run from anywhere:
#   tools/pixel/retrace.sh            (all: Blender trace renders, reduce, sheets, read check)
#   tools/pixel/retrace.sh --no-render (skip Blender, reuse .scratch/trace/*.png)
# 1. avatar/kit/render_trace.py -> .scratch/trace/<id>[_<pose>]_<view>.png (flat colour, 512 px per 1.2 m)
# 2. tools/pixel/trace3d.py     -> tools/pixel/traced.py (palette-snapped sprite bases, no Blender needed)
# 3. tools/pixel/make_sheets.py -> characters/<id>/refs/look_sheet.png, characters/residents_lineup.png
# 4. tools/pixel/read_check.py  -> characters/read_check.png
set -euo pipefail
cd "$(dirname "$0")/../.."
T="blender -b --factory-startup -P avatar/kit/render_trace.py --"
run() { echo "== trace $*"; local log; log=$($T "$@" 2>&1) || true; grep -E "^TRACE" <<<"$log" || { grep -E "Traceback|Error" -A3 <<<"$log" | head; echo "render failed: $*"; return 1; }; }
if [ "${1:-}" != "--no-render" ]; then
  for c in mole gnome_foreman caveman dragon; do run --char "$c"; done
  run --char gnome_foreman --views front,side --expression whistle --tag whistle
  run --char mole --views front --action popup --frame 12 --expression startled --tag popup
  run --char mole --views front --action dig --frame 9 --gear shovel --tag dig || echo "mole dig skipped"
  run --char caveman --views front --action polish --frame 13 --tag polish
  run --char caveman --views front --action wave --frame 10 --tag wave
  run --char dragon --views front --action yawn --frame 34 --expression yawn --tag yawn
  run --char jeff --views side
  run --char chuck --views side
fi
python3 tools/pixel/trace3d.py
python3 tools/pixel/make_sheets.py
python3 tools/pixel/read_check.py
echo "retrace done"
