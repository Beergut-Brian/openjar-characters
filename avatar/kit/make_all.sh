#!/usr/bin/env bash
# Rebuild every Jarling deliverable from source. Run from the repo root.
set -euo pipefail
B="blender -b --factory-startup"
K=avatar/kit
for c in jeff chuck; do
  out=characters/$c/refs/jarling
  $B -P $K/build_jarling.py -- --params characters/$c/jarling.json --out $out/$c.glb
  $B -P $K/render_refs.py -- --params characters/$c/jarling.json --outdir $out --samples ${REF_SAMPLES:-64}
  python3 $K/label_sheet.py $out/${c}_turnaround.png front "3/4" side back
  python3 $K/label_sheet.py $out/${c}_expressions.png neutral happy surprised determined
done
$B -P $K/render_scenes.py -- --outdir $K/renders --only lineup --samples ${REF_SAMPLES:-64}
$B -P $K/render_scenes.py -- --outdir $K/renders --only mock --samples ${MOCK_SAMPLES:-128}
