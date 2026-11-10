#!/usr/bin/env bash
# Index + roster + equipment tests.
#   godot/run_tests.sh            -> prints results, last line "RESULT: PASS|FAIL", exit 1 on failure
# 1. tools/build_index.py is rerun: characters.json must not change (index up to date, deterministic).
# 2. test_roster.gd: roster, defaults, player-colour rule, standard-body rule (README "Playable characters").
# 3. test_equipment.gd: gear on Jeff, Chuck and generic Jarlings.
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
godot --headless --path . --import >/dev/null 2>&1 || true
for t in test_roster test_equipment; do
  timeout 300 godot --headless --path . -s "res://tests/$t.gd" 2>&1 | grep -v "^Godot Engine\|^$"
  rc=${PIPESTATUS[0]}
  [ "$rc" -eq 0 ] || { echo "  ($t exited $rc)"; status=1; }
done
echo "RESULT: $([ $status -eq 0 ] && echo PASS || echo FAIL)"
exit $status
