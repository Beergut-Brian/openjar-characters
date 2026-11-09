#!/usr/bin/env python3
"""Regenerate characters.json from the character folders. Run from the repo root."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
out = {"version": 1, "characters": []}
for d in sorted((root / "characters").iterdir()):
    if not d.is_dir() or d.name.startswith("_"):
        continue
    bible = (d / "bible.md").read_text()
    m = re.search(r"\*\*Kind:\*\*\s*([^.]+)\.", bible)
    kind_raw = (m.group(1) if m else "universal").lower()
    kind = "player_locked" if "player-locked" in kind_raw else "universal"
    player = 0 if "player 1" in kind_raw else 1 if "player 2" in kind_raw else None
    first = re.search(r"\*\*First appears:\*\*\s*([^\n]+)", bible)
    status = bible.split("## Status")[-1].strip().splitlines()[0] if "## Status" in bible else ""
    barks = sorted(p.stem for p in (d / "voice").glob("*.ogg"))
    out["characters"].append({
        "id": d.name, "name": bible.splitlines()[0].lstrip("# ").strip(),
        "kind": kind, "player": player,
        "first_appears": first.group(1).strip() if first else None,
        "approved": "approved" in status.lower() and "not yet" not in status.lower(),
        "bible": f"characters/{d.name}/bible.md", "look": f"characters/{d.name}/look.md",
        "refs": f"characters/{d.name}/refs/", "voice": f"characters/{d.name}/voice/",
        "barks": barks,
    })
(root / "characters.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"wrote characters.json with {len(out['characters'])} characters")
