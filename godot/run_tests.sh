#!/usr/bin/env bash
# Copy the Jarling + gear glbs into the test project, import, run the equipment tests.
#   godot/run_tests.sh            -> prints results, exit 1 on failure
set -euo pipefail
cd "$(dirname "$0")"
rm -rf _lib && mkdir -p _lib/characters _lib/gear
cp ../characters/*/refs/jarling/*.glb _lib/characters/
cp ../avatar/gear/*.glb ../avatar/gear/*.json _lib/gear/
# three generic Jarlings with other builds (stocky + cap, slim + skirt, round + afro), if Blender is here
if command -v blender >/dev/null; then
  for s in 4 10 11; do
    blender -b --factory-startup -P ../avatar/kit/build_jarling.py -- --seed $s --out "$PWD/_lib/characters/generic$s.glb" >/dev/null 2>&1
  done
fi
godot --headless --path . --import >/dev/null 2>&1 || true
timeout 300 godot --headless --path . -s res://tests/test_equipment.gd 2>&1 | grep -v "^Godot Engine\|^$"
exit "${PIPESTATUS[0]}"
