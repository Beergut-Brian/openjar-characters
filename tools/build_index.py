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
out["defaults"] = {f"P{c['default_for']}": c["id"] for c in sorted(out["characters"], key=lambda c: c["default_for"] or 9) if c["default_for"]}
# The rules every playable character follows (README "Playable characters"); tests and games read these.
out["player_colours"] = {"P1": "#3cc24a", "P2": "#e4393c"}
# Main outfit colours (headwear, top, bottoms, shoes) must be at least this far (CIE Delta E 2000) from both;
# skin and hair need the smaller distance (natural tones pass).
out["player_colour_min_delta_e"] = 20.0
out["player_colour_min_delta_e_skin_hair"] = 10.0
SLOTS = ["head", "face", "back", "hand_l", "hand_r", "waist", "knee_l", "knee_r", "foot_l", "foot_r"]
BONES = ["root", "spine", "head", "arm.L", "arm.R", "hand.L", "hand.R", "leg.L", "leg.R", "foot.L", "foot.R"]
NO_KNEES = [s for s in SLOTS if not s.startswith("knee_")]
out["body_types"] = {
    "standard": {
        "rig": "avatar/kit (Jarling humanoid)", "params": ["build", "height", "leg_scale", "width", "belly"],
        "builds": ["slim", "regular", "stocky", "round", "boxy", "puffy"],
        "height": [0.8, 1.3], "leg_scale": [0.8, 1.2], "width": [0.75, 1.5], "belly": [0.0, 1.0],
        "features": ["antennae", "horns", "pointy_ears", "fins"],
        "bones": BONES, "actions": ["idle", "run", "kick", "cheer"], "loops": ["idle", "run", "cheer"],
        "slots": SLOTS, "playable": True},
    "critter": {
        "rig": "avatar/kit/body_critter.py (small no-neck animal)",
        "bones": BONES + ["prop"], "actions": ["idle", "run", "cheer", "popup", "bow", "dig"],
        "loops": ["idle", "run", "cheer"], "slots": NO_KNEES, "playable": False},
    "giant": {
        "rig": "avatar/kit/body_giant.py (huge sitting creature)",
        "bones": BONES + ["tail.1", "tail.2", "tail.3", "wing.L", "wing.R"],
        "actions": ["idle", "run", "cheer", "yawn", "wave", "flap", "sleep"],
        "loops": ["idle", "run", "cheer", "flap", "sleep"], "slots": NO_KNEES, "playable": False},
    "quadruped": {
        "rig": "avatar/kit/body_quadruped.py (four-legged farm animal or pet; arm/hand = front legs and hooves, leg/foot = hind)",
        "params": ["height", "length", "girth", "width", "leg", "head"],
        "bones": BONES + ["tail.1", "tail.2"],
        "actions": ["idle", "run", "cheer", "tipped", "stiff", "graze", "sit"],
        "loops": ["idle", "run", "cheer", "tipped", "stiff", "graze", "sit"],
        "slots": ["head", "face", "back", "waist", "mouth"], "hold_styles": ["in_mouth"], "playable": False}}
out["proposed"] = scan("proposals", {"status": "proposed"})
(root / "characters.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"wrote characters.json with {len(out['characters'])} characters "
      f"(roster {', '.join(out['roster'])}), {len(out['proposed'])} proposed")
