#!/usr/bin/env bash
# Index + roster + equipment tests.
#   godot/run_tests.sh            -> prints results, last line "RESULT: PASS|FAIL", exit 1 on failure
# 1. tools/build_index.py is rerun: characters.json must not change (index up to date, deterministic).
# 2. test_roster.gd: roster, defaults, player-colour rule, standard-body rule (README "Playable characters").
# 3. test_equipment.gd: gear on Jeff, Chuck and generic Jarlings.
# 4. test_bodies.gd: per-body-type contract (bones, actions, expressions, slots, gear) for every character with a model.
# 5. Kit v2: tools/check_colours.py (Delta E 2000 player-colour rule: outfit >= 20, skin and hair >= 10), avatar/kit/check_kit_v2.py (width/belly limits,
#    slots follow the surface, features as parts; needs Blender) and test_kit_v2.gd (gear on the widest and skinniest body).
set -uo pipefail
cd "$(dirname "$0")"
status=0

echo "index: rerun tools/build_index.py"
mkdir -p ../.scratch
cp ../characters.json ../.scratch/characters.before.json
(cd .. && python3 tools/build_index.py) | sed 's/^/  /'
if cmp -s ../characters.json ../.scratch/characters.before.json; then
  echo "  ok   rerunning the index changes nothing"
else
  echo "  FAIL rerunning the index changed characters.json (it was stale or is not deterministic):"
  diff ../.scratch/characters.before.json ../characters.json | head -20
  status=1
fi

rm -rf _lib && mkdir -p _lib/characters _lib/gear _lib/params
cp ../characters.json _lib/characters.json
cp ../characters/*/refs/jarling/*.glb _lib/characters/
for p in ../characters/*/jarling.json; do cp "$p" "_lib/params/$(basename "$(dirname "$p")").json"; done
cp ../avatar/gear/*.glb ../avatar/gear/*.json _lib/gear/
# three generic Jarlings with other builds (stocky + cap, slim + skirt, round + afro), if Blender is here
if command -v blender >/dev/null; then
  for s in 4 10 11; do
    blender -b --factory-startup -P ../avatar/kit/build_jarling.py -- --seed $s --out "$PWD/_lib/characters/generic$s.glb" >/dev/null 2>&1
  done
fi
echo "colour rule: tools/check_colours.py"
(cd .. && python3 tools/check_colours.py --self-test && python3 tools/check_colours.py) || status=1
mkdir -p _lib/kit_v2
cp tests/kit_v2/gear_*.json ../avatar/gear/hat.glb _lib/kit_v2/   # test-only helmets with hides_features
if command -v blender >/dev/null; then
  echo "kit v2: avatar/kit/check_kit_v2.py"
  blender -b --factory-startup -P ../avatar/kit/check_kit_v2.py 2>&1 | grep -E "^  (ok|FAIL)|^\\[kit|^KIT_V2_CHECK" > ../.scratch/check_kit_v2.out
  cat ../.scratch/check_kit_v2.out
  grep -q "^KIT_V2_CHECK PASS" ../.scratch/check_kit_v2.out || { echo "  FAIL check_kit_v2.py did not pass"; status=1; }
  for p in tests/kit_v2/v2_*.json; do
    blender -b --factory-startup -P ../avatar/kit/build_jarling.py -- --params "$p" --out "$PWD/_lib/kit_v2/$(basename "$p" .json).glb" >/dev/null 2>&1
  done
  for p in ../avatar/kit/examples/sheets/*.json; do   # the 19 sheet examples: each must build and be a standard Jarling
    blender -b --factory-startup -P ../avatar/kit/build_jarling.py -- --params "$p" --out "$PWD/_lib/kit_v2/sheet_$(basename "$p" .json).glb" >/dev/null 2>&1
    (cd .. && python3 tools/check_colours.py "avatar/kit/examples/sheets/$(basename "$p")") || status=1
  done
else
  echo "  FAIL blender not found: kit v2 checks need it"; status=1
fi
godot --headless --path . --import >/dev/null 2>&1 || true
for t in test_roster test_equipment test_bodies test_kit_v2; do
  timeout 300 godot --headless --path . -s "res://tests/$t.gd" 2>&1 | grep -v "^Godot Engine\|^$"
  rc=${PIPESTATUS[0]}
  [ "$rc" -eq 0 ] || { echo "  ($t exited $rc)"; status=1; }
done
echo "RESULT: $([ $status -eq 0 ] && echo PASS || echo FAIL)"
exit $status
