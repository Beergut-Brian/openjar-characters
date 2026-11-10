#!/usr/bin/env python3
"""Regenerate characters.json from the character folders. Run from the repo root.

Reads each bible's header line:
  **Kind:** universal. **Playable:** true. **Default for:** 1 (...). **Body:** standard. **First appears:** ...
Deterministic: rerunning it on unchanged folders writes the same bytes.
"""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent


def field(bible, name):
    m = re.search(r"\*\*" + re.escape(name) + r":\*\*\s*([^.\n]+)\.", bible)
    return m.group(1).strip() if m else None


def entry(d, base, extra=None):
    bible = (d / "bible.md").read_text()
    kind_raw = (field(bible, "Kind") or "universal").lower()
    kind = "player_locked" if "player-locked" in kind_raw else "universal"
    player = 0 if "player 1" in kind_raw else 1 if "player 2" in kind_raw else None
    playable = (field(bible, "Playable") or "false").lower().startswith("true")
    dm = re.match(r"([12])\b", field(bible, "Default for") or "")
    default_for = int(dm.group(1)) if dm and playable else None
    body_type = (field(bible, "Body") or "standard").lower().split()[0]
    first = re.search(r"\*\*First appears:\*\*\s*([^\n]+)", bible)
    status = bible.split("## Status")[-1].strip().splitlines()[0] if "## Status" in bible else ""
    barks = sorted(p.stem for p in (d / "voice").glob("*.ogg"))
    look = (d / "look.md").read_text() if (d / "look.md").exists() else ""
    alt_forms = re.findall(r"^## Alt form:\s*([^(\n]+?)\s*(?:\(|$)", look, re.M)
    rel = f"{base}/{d.name}"
    glb = f"{rel}/refs/jarling/{d.name}.glb"
    params = f"{rel}/jarling.json"
    # pixel form: an alt form whose name says "pixel" and whose text names its sprite source
    pixel = None
    for sec in re.split(r"^## ", look, flags=re.M)[1:]:
        head = sec.splitlines()[0]
        if head.lower().startswith("alt form:") and "pixel" in head.lower():
            src = re.search(r"Sprite source:\s*`([^`]+)`\s*\(`(\w+)\(\)`\)", sec)
            pixel = {"alt_form": re.sub(r"^alt form:\s*|\s*\(.*$|:.*$", "", head, flags=re.I).strip(),
                     "source": src.group(1) if src else None,
                     "function": src.group(2) if src else None}
            break
    e = {
        "id": d.name, "name": bible.splitlines()[0].lstrip("# ").strip(),
        "kind": kind, "player": player,
        "playable": playable, "default_for": default_for, "body_type": body_type,
        "first_appears": first.group(1).strip() if first else None,
        "approved": "approved" in status.lower() and "not yet" not in status.lower(),
        "bible": f"{rel}/bible.md", "look": f"{rel}/look.md",
        "refs": f"{rel}/refs/", "voice": f"{rel}/voice/",
        "model_3d": glb if (root / glb).exists() else None,
        "jarling_params": params if (root / params).exists() else None,
        "pixel": pixel,
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


def roster(chars):
    """Playable ids in display order: P1 default, P2 default, then the rest by id."""
    play = [c for c in chars if c["playable"]]
    return [c["id"] for c in sorted(play, key=lambda c: (c["default_for"] or 9, c["id"]))]


out = {"version": 1, "characters": scan("characters")}
out["roster"] = roster(out["characters"])
out["defaults"] = {f"P{c['default_for']}": c["id"] for c in out["characters"] if c["default_for"]}
out["proposed"] = scan("proposals", {"status": "proposed"})
(root / "characters.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"wrote characters.json with {len(out['characters'])} characters "
      f"(roster {', '.join(out['roster'])}), {len(out['proposed'])} proposed")
