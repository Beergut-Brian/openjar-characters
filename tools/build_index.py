#!/usr/bin/env python3
"""Regenerate characters.json from the character folders. Run from the repo root."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
def entry(d, base, extra=None):
    bible = (d / "bible.md").read_text()
    m = re.search(r"\*\*Kind:\*\*\s*([^.]+)\.", bible)
    kind_raw = (m.group(1) if m else "universal").lower()
    kind = "player_locked" if "player-locked" in kind_raw else "universal"
    player = 0 if "player 1" in kind_raw else 1 if "player 2" in kind_raw else None
    first = re.search(r"\*\*First appears:\*\*\s*([^\n]+)", bible)
    status = bible.split("## Status")[-1].strip().splitlines()[0] if "## Status" in bible else ""
    barks = sorted(p.stem for p in (d / "voice").glob("*.ogg"))
    look = (d / "look.md").read_text() if (d / "look.md").exists() else ""
    alt_forms = re.findall(r"^## Alt form:\s*([^(\n]+?)\s*(?:\(|$)", look, re.M)
    e = {
        "id": d.name, "name": bible.splitlines()[0].lstrip("# ").strip(),
        "kind": kind, "player": player,
        "first_appears": first.group(1).strip() if first else None,
        "approved": "approved" in status.lower() and "not yet" not in status.lower(),
        "bible": f"{base}/{d.name}/bible.md", "look": f"{base}/{d.name}/look.md",
        "refs": f"{base}/{d.name}/refs/", "voice": f"{base}/{d.name}/voice/",
        "barks": barks,
        "alt_forms": alt_forms,
    }
    if extra:
        e.update(extra)
    return e


def scan(base, extra=None):
    folder = root / base
    if not folder.is_dir():
        return []
    return [entry(d, base, extra) for d in sorted(folder.iterdir())
            if d.is_dir() and not d.name.startswith("_")]


out = {"version": 1, "characters": scan("characters")}
out["proposed"] = scan("proposals", {"status": "proposed"})
(root / "characters.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"wrote characters.json with {len(out['characters'])} characters, {len(out['proposed'])} proposed")
