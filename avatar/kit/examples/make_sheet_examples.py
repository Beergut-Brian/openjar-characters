#!/usr/bin/env python3
"""Starting-point params for Kaden's 19 Jarling sheets (2026-11-10): proof that kit v2 can build
each one. NOT characters: the batch lanes write the real `characters/<id>/jarling.json` (they may
start from these). Run from the repo root: python3 avatar/kit/examples/make_sheet_examples.py
Writes avatar/kit/examples/sheets/<id>.json and docs/sheets-coverage.md's table rows.
"""
import json, pathlib
here = pathlib.Path(__file__).resolve().parent
SK = ["#F7CFAE", "#EFBB90", "#D99E6E", "#BF8150", "#7A4A2C", "#F0BE94"]

def J(id, name, skin, body, head=None, face=None, hair=None, headwear=None, top=None, bottoms=None, shoes=None, costume=None, **kw):
    d = {"id": id, "name": name, "notes": "Kit v2 example for the sheet, not an approved look.",
         "head": head or {"shape": "round", "size": 1.0, "ears": "round"}, "skin": skin, "face": face or {},
         "hair": hair or {"style": "none"}, "headwear": headwear or {"type": "none"}, "body": body,
         "outfit": {"top": top, "bottoms": bottoms, "shoes": shoes}, "costume": costume or []}
    d.update(kw)
    return d

S = [
 J("foreman_dot", "Foreman Dot", SK[2], {"build": "stocky", "height": 0.85, "leg_scale": 0.85, "width": 1.1},
   face={"eyes": "round", "brows": "thick", "brow_color": "#4A2F23", "mouth": "grin_top", "eye_y": -0.10},
   hair={"style": "bob", "color": "#4A2F23"}, headwear={"type": "hard_hat", "color": "#F5C518", "fit": 0.22, "tilt_deg": 8},
   top={"style": "tee", "color": "#F28A1E", "pattern": {"type": "hstripe", "accent": "#FFFFFF", "edge": "#C9CED4"}},
   bottoms={"style": "pants", "color": "#1F2D4F"}, shoes={"style": "chunky_boots", "color": "#7A4E2A"}),
 J("granny_gravel", "Granny Gravel", SK[0], {"build": "regular", "height": 0.9, "leg_scale": 0.85},
   face={"eyes": "button", "brows": "thin", "brow_color": "#B9B4AE", "brow_raise": 0.05, "mouth": "smile", "mouth_width": 0.6},
   hair={"style": "top_bun", "color": "#F2F0EA"},
   top={"style": "long", "color": "#B9A3D9", "pattern": {"type": "buttons", "accent": "#F2F0EA", "rows": 1}},
   bottoms={"style": "pants", "color": "#8C8F96"}, shoes={"style": "sneaker", "color": "#FFD93B"},
   costume=[{"piece": "long_skirt", "color": "#8C8F96", "length": 0.85}, {"piece": "goggles", "pos": "forehead", "style": "safety", "color": "#4A4F5A"}]),
 J("mayor_pip", "Mayor Pip", SK[1], {"build": "slim", "height": 0.8, "leg_scale": 0.8, "width": 0.9},
   face={"eyes": "button", "brows": "arched", "brow_color": "#4A2F23", "brow_raise": 0.04, "mouth": "set", "lid": 0.2},
   hair={"style": "short", "color": "#4A2F23"}, headwear={"type": "top_hat", "color": "#1C1C22", "band": "#D9B23A", "height": 2.3, "scale": 1.12},
   top={"style": "long", "color": "#A8CFF0"}, bottoms={"style": "pants", "color": "#7D8088"}, shoes={"style": "dress", "color": "#15151A"},
   costume=[{"piece": "sash", "color": "#D9B23A", "side": "R"}]),
 J("lampy", "Lampy", SK[1], {"build": "slim", "height": 1.25, "leg_scale": 1.15, "width": 0.8},
   face={"eyes": "round", "brows": "thin", "nose": "dot", "mouth": "smile", "expressions": {"neutral": {"eye_scale": 1.2}}, "extras": [{"type": "smudge", "side": "R"}]},
   hair={"style": "short", "color": "#7A4B2A"}, headwear={"type": "miner_helmet", "color": "#F1F1EC"},
   top={"style": "tee", "color": "#3F8A99", "pattern": {"type": "bib", "accent": "#35778A"}}, bottoms={"style": "pants", "color": "#7A5536"},
   shoes={"style": "chunky_boots", "color": "#7B7F86", "sole": "#4A4D55"}),
 J("professor_fizz", "Professor Fizz", SK[0], {"build": "regular", "height": 1.0},
   face={"eyes": "wide", "brows": "arched", "brow_color": "#8A8F99", "brow_skip": "L", "mouth": "grin", "extras": [{"type": "scorch_brow", "side": "L"}]},
   hair={"style": "upright", "color": "#F7F7F2"},
   top={"style": "long", "color": "#F4F5F2", "pattern": [{"type": "collar", "accent": "#5E2F94"}, {"type": "buttons", "accent": "#5E2F94"}]},
   bottoms={"style": "shorts", "color": "#5E2F94"},
   shoes={"style": "dress", "color": "#1B1B20", "socks": {"color_l": "#FF9A2E", "color_r": "#5CC6F2", "height": 0.45}},
   costume=[{"piece": "goggles", "pos": "forehead", "style": "round", "color": "#6B4A2A"}]),
 J("scrap", "Scrap", SK[5], {"build": "regular", "height": 0.85, "leg_scale": 0.85}, head={"shape": "round", "size": 1.05, "ears": "round"},
   face={"eyes": "drop", "brows": "soft", "brow_color": "#7A3A1A", "mouth": "grin_gap", "extras": ["freckles_big"], "eye_y": -0.09},
   hair={"style": "short", "color": "#B5651D"}, headwear={"type": "colander", "color": "#B9BEC4"},
   top={"style": "tee", "color": "#F2C230", "pattern": {"type": "patches", "accent": "#E8873D", "accent2": "#5B8FD6"}},
   bottoms={"style": "shorts", "color": "#3E6DB5"}, shoes={"style": "sneaker", "color": "#F28C28", "color_r": "#8A4FC4"}),
 J("big_tiny", "Big Tiny", SK[2], {"build": "round", "height": 1.3, "width": 1.5, "belly": 1.0},
   face={"eyes": "drop", "brows": "soft", "mouth": "smile", "expressions": {"neutral": {"eye_mode": "arc"}}},
   hair={"style": "buzz", "color": "#4A2F23"}, headwear={"type": "beanie", "color": "#2E3A66", "scale": 0.45, "hair": "free"},
   top={"style": "tee", "color": "#7EC8F2"}, bottoms={"style": "pants", "color": "#80848C"}, shoes={"style": "sneaker", "color": "#F7F7F5", "size": 1.35}),
 J("coach_whistle", "Coach Whistle", SK[2], {"build": "stocky", "height": 0.95, "leg_scale": 0.8, "width": 1.15, "belly": 0.25},
   face={"eyes": "round", "brows": "thick", "brow_color": "#3A2418", "nose": "bump", "mouth": "yell", "blush": 0.4},
   hair={"style": "buzz", "color": "#3A2418"}, headwear={"type": "cap", "color": "#1E2B4D", "brim": "#1E2B4D", "tilt_deg": 8},
   top={"style": "tee", "color": "#F5F5F2", "sleeve": "#1A1A1E", "pattern": {"type": "vstripes", "accent": "#1A1A1E", "count": 12}},
   bottoms={"style": "shorts", "color": "#8A8E96"},
   shoes={"style": "sneaker", "color": "#F7F7F5", "socks": {"color": "#F7F7F5", "height": 0.5, "cuff": "#1E2B4D"}},
   costume=[{"piece": "whistle_cord", "color": "#C9CED4", "cord": "#1E2B4D"}]),
 J("zorp", "Zorp", "#9FD6F0", {"build": "slim", "height": 1.05, "width": 0.85},
   head={"shape": "tall", "size": 1.05, "ears": "none", "features": [{"type": "antennae", "count": 2, "color": "#7FB9D6", "tip": "#FFD23F"}]},
   face={"eyes": "round", "brows": "thin", "nose": "none", "mouth": "o", "blush": 0.5, "expressions": {"neutral": {"eye_scale": 1.15}}},
   headwear={"type": "headband", "color": "#C9CED4"},
   top={"style": "tee", "color": "#FFD23F", "pattern": {"type": "vacation", "accent": "#FF7EB9", "accent2": "#FF9A2E"}},
   bottoms={"style": "shorts", "color": "#F5F5F2"}, shoes={"style": "sandals", "color": "#C89A63"}),
 J("ribbit", "Ribbit", SK[5], {"build": "round", "height": 0.85, "leg_scale": 0.85, "width": 1.1, "belly": 0.4},
   head={"shape": "round", "size": 1.05, "ears": "none"}, face={"eyes": "drop", "brows": "soft", "nose": "dot", "mouth": "wide", "blush": 0.5},
   headwear={"type": "animal_hood", "color": "#2A9DB0", "eyes": {"color": "#FFFFFF", "pupil": "#1B1B20", "size": 1.0}},
   top={"style": "long", "color": "#2A9DB0", "pattern": {"type": "belly_panel", "accent": "#F6D44A"}},
   bottoms={"style": "shorts", "color": "#22336B"}, shoes={"style": "footies", "color": "#F6D44A"}),
 J("astro_ana", "Astro Ana", SK[3], {"build": "regular", "height": 1.0},
   face={"eyes": "lash", "brows": "arched", "brow_color": "#2A1A14", "mouth": "grin_top", "blush": 0.4, "lid": 0.12, "lid_tilt": 0.2, "brow_tilt": 0.2},
   hair={"style": "puffs", "color": "#3B2A20"}, headwear={"type": "fishbowl", "collar": "#F2F4F6"},
   top={"style": "long", "color": "#F2F4F6", "pattern": {"type": "hstripe", "accent": "#F7941D", "v": 0.62, "width": 0.10}},
   bottoms={"style": "pants", "color": "#F2F4F6"}, shoes={"style": "moon_boots", "color": "#F7941D", "sole": "#F2F4F6"}),
 J("old_reel", "Old Reel", SK[1], {"build": "round", "height": 1.2, "leg_scale": 1.05, "width": 1.1, "belly": 0.7},
   face={"eyes": "drop", "brows": "bushy", "brow_color": "#F1EEE8", "mouth": "smile", "lid": 0.45, "eye_y": -0.08},
   hair={"style": "buzz", "color": "#E8E4DC"}, headwear={"type": "bucket_hat", "color": "#C8A97A", "lure": "#F28C28"},
   top={"style": "long", "color": "#F1E7CF", "pattern": {"type": "vest", "accent": "#A89B6E"}}, bottoms={"style": "pants", "color": "#6E4B30"},
   shoes={"style": "rain_boots", "color": "#F6C833"}),
 J("bloom", "Bloom", SK[3], {"build": "puffy", "height": 0.85, "leg_scale": 0.85, "width": 1.1, "belly": 0.2},
   face={"eyes": "lash", "brows": "soft", "brow_color": "#3A2418", "mouth": "smile", "blush": 0.9, "eye_y": -0.09},
   hair={"style": "bob", "color": "#3A2418"}, headwear={"type": "sun_hat", "color": "#E3C27A", "band": "#F7A8CB", "flower": "#F7A8CB"},
   top={"style": "tee", "color": "#F7A8CB"}, bottoms={"style": "shorts", "color": "#5B7FB8"}, shoes={"style": "clogs", "color": "#8A4FC4"},
   costume=[{"piece": "long_skirt", "color": "#5B7FB8", "length": 0.35, "mud": "#6B4A2E"}]),
 J("sir_clank", "Sir Clank", SK[0], {"build": "regular", "height": 1.05},
   face={"eyes": "round", "brows": "thick", "brow_color": "#4A2F23", "brow_tilt": 0.25, "mouth": "grin", "eye_y": -0.09},
   hair={"style": "short", "color": "#4A2F23"}, headwear={"type": "pot_helmet", "color": "#B8BEC6"},
   top={"style": "tee", "color": "#8A8F98", "pattern": {"type": "emblem", "shape": "shield", "accent": "#F2C230"}},
   bottoms={"style": "pants", "color": "#23305E"}, shoes={"style": "chunky_boots", "color": "#7A4E2A"},
   posture={"spine_lean": -3, "head_lean": -2}),
 J("rexy", "Rexy", SK[5], {"build": "round", "height": 0.8, "leg_scale": 0.8}, head={"shape": "round", "size": 1.05, "ears": "none"},
   face={"eyes": "round", "brows": "soft", "mouth": "yell"},
   headwear={"type": "animal_hood", "color": "#F7941D", "teeth": "#FFFFFF", "spikes": "#FFD23F"},
   top={"style": "costume", "color": "#F7941D"}, bottoms={"style": "pants", "color": "#F7941D"}, shoes={"style": "footies", "color": "#F7941D"},
   costume=[{"piece": "back_spikes", "color": "#FFD23F"}, {"piece": "dino_tail", "color": "#F7941D", "spikes": "#FFD23F"}]),
 J("boxbot", "Boxbot", SK[1], {"build": "boxy", "height": 0.9, "leg_scale": 0.9}, head={"shape": "soft_square", "size": 1.0, "ears": "none"},
   face={"eyes": "button", "brows": "none", "nose": "none", "mouth": "flat", "blush": 0.2},
   headwear={"type": "box_head", "color": "#C49A6C"},
   top={"style": "long", "color": "#C0C4CA"}, bottoms={"style": "pants", "color": "#80848C"}, shoes={"style": "sneaker", "color": "#3B6FD1"},
   costume=[{"piece": "box_torso", "color": "#C49A6C", "accent": "#3B6FD1"}, {"piece": "hose_arms", "color": "#C0C4CA"}]),
 J("el_burrito", "El Burrito", SK[2], {"build": "stocky", "height": 0.85, "leg_scale": 0.85, "width": 1.3, "belly": 0.35},
   head={"shape": "round", "size": 1.0, "ears": "none"},
   face={"eyes": "round", "brows": "none", "nose": "none", "mouth": "grin_top", "blush": 0, "extras": [{"type": "mask", "color": "#E0B12E", "trim": "#6B2FA8"}]},
   top={"style": "tee", "color": "#E0B12E", "pattern": {"type": "emblem", "shape": "star", "accent": "#6B2FA8"}},
   bottoms={"style": "shorts", "color": "#6B2FA8"}, shoes={"style": "wrestling_boots", "color": "#F5F5F2", "lace": "#6B2FA8"},
   costume=[{"piece": "cape", "color": "#6B2FA8", "trim": "#E0B12E"}]),
 J("snooze", "Snooze", SK[0], {"build": "regular", "height": 1.0, "leg_scale": 0.95},
   face={"eyes": "drop", "brows": "soft", "mouth": "smile", "expressions": {"neutral": {"eye_mode": "arc"}, "surprised": {"eye_mode": "arc"}, "determined": {"eye_mode": "arc"}}},
   hair={"style": "short", "color": "#7A4B2A"}, headwear={"type": "nightcap", "color": "#6F7FD8", "stripe": "#F5F5F2", "pom": "#F5F5F2"},
   top={"style": "long", "color": "#A9D4F2", "pattern": {"type": "stars", "accent": "#FFFFFF"}},
   bottoms={"style": "pants", "color": "#A9D4F2", "pattern": {"type": "stars", "accent": "#FFFFFF"}}, shoes={"style": "slippers", "color": "#FFD95A"},
   posture={"spine_lean": 7, "head_lean": 4}),
 J("captain_crumbs", "Captain Crumbs", SK[2], {"build": "round", "height": 1.2, "width": 1.15, "belly": 0.6},
   face={"eyes": "round", "brows": "thick", "brow_color": "#4A3324", "mouth": "grin_top"},
   hair={"style": "short", "color": "#4A3324"}, headwear={"type": "chef_hat", "color": "#F7F7F2", "badge": "#1F2D55"},
   top={"style": "long", "color": "#F7F7F2", "pattern": {"type": "buttons", "accent": "#1F2D55", "rows": 2}},
   bottoms={"style": "pants", "color": "#1F2D55", "pattern": {"type": "vstripes", "accent": "#F7F7F2"}}, shoes={"style": "chunky_boots", "color": "#18181C"},
   costume=[{"piece": "eyepatch", "side": "L"}, {"piece": "moustache", "style": "curly", "color": "#4A3324"}]),
]
out = here / "sheets"
out.mkdir(exist_ok=True)
for d in S:
    (out / f"{d['id']}.json").write_text(json.dumps(d, indent=1) + "\n")
print(f"wrote {len(S)} sheet examples to {out}")

# ------------------------------------------------------------------ docs/sheets-coverage.md
NOTES = {   # id: (what the sheet asks that is covered by something other than a kit piece, what is NOT built)
 "foreman_dot": ("Hard hat 'slightly too low' = `fit` 0.22 with `face.eye_y` lowered. Clipboard prop exists (`clipboard`, pieces_hill).", ""),
 "granny_gravel": ("'Cardigan-style' = long sleeves + `buttons` row. Goggles 'pushed up into her hair' = `goggles` pos forehead. Cackle face = an expression for the batch lane.", ""),
 "mayor_pip": ("Hat 'nearly half his height' = `top_hat` height 2.3, scale 1.12. Smallest body = slim, height 0.8, width 0.9.", "Ribbon scissors prop (docs/jarlings-19.md lists it as gear): not built."),
 "lampy": ("Headlamp is a real spot light in the glb (`<id>_headlamp`, Godot imports a light under the head attachment) plus a glowing lens. 'Overalls-style top' = `bib` pattern.", "Rock prop (gear): not built."),
 "professor_fizz": ("Lab coat = white long top + `collar` + `buttons`; it is a painted coat, not a separate coat with tails. Mismatched socks = `shoes.socks.color_l/_r` (shorts so they show). Scorch brow = `scorch_brow` + `brow_skip`.", "A real lab coat hem below the waist: not built."),
 "scrap": ("One orange, one purple shoe = `shoes.color` + `color_r`. Gap-toothed grin = mouth `grin_gap`. 'A little sticky' is personality only.", ""),
 "big_tiny": ("Widest and tallest = round, width 1.5, belly 1.0, height 1.3. Smallest beanie = `beanie` scale 0.45. Enormous sneakers = `shoes.size` 1.35.", ""),
 "coach_whistle": ("Barrel chest, short legs = stocky, width 1.15, leg_scale 0.8. Tall socks = `shoes.socks` height 0.5. Mid-yell = mouth `yell`.", "Whistle blast is audio (voice lane)."),
 "zorp": ("Antennae are a head feature (Gary's call), with a `headband` under them as the sheet draws; any hat still fits on top. Slightly taller head = shape tall, size 1.05.", ""),
 "ribbit": ("Hood up with eyes on top = `animal_hood` eyes. Yellow belly = `belly_panel`. 'Bare-look yellow shoes' = `footies`.", "Hop gait (an extra action): not built; idle/run/kick/cheer are the standard ones."),
 "astro_ana": ("Clear helmet = `fishbowl` (hair mode free, so the puffs stay). Two puffs = hair preset `puffs`. Chest stripe = `hstripe`.", "In Blender renders the bowl is very faint (glint + collar read); raise `headwear.alpha` or add a rim shader in-game. Radio crackle is audio."),
 "old_reel": ("Vest over a shirt = `vest` pattern (painted, with pockets). Bushy white brows = brows bushy + white `brow_color`. Tall with a round belly = round, height 1.2, belly 0.7.", "Fishing rod prop (gear): not built."),
 "bloom": ("Skirt with muddy knees = `long_skirt` length 0.35 + `mud`. Rosy cheeks = blush 0.9. Soft rounded = puffy, width 1.1.", "Watering can prop (gear): not built."),
 "sir_clank": ("Handle sticks out the back = `pot_helmet`. Shield = `emblem` shape shield. Stands very straight = posture.", "Spoon sword prop (gear): not built. Bow action: not built."),
 "rexy": ("Onesie = top style costume + same-colour pants + `footies`. Hood teeth and spikes = `animal_hood` teeth/spikes; back spikes and tail are costume pieces (tail is the part `tail`, a cape or jetpack hides it).", ""),
 "boxbot": ("Square body = boxy. Head box with face cut-out = `box_head`; torso box with drawn dials = `box_torso`; dryer-hose arms = `hose_arms`.", ""),
 "el_burrito": ("Mask covering the head = face extra `mask` (the whole head takes the mask colour; ears none). Cape = costume `cape` (part `cape`; the gear cape also works). Short and wide = stocky, width 1.3.", "Pose actions: not built."),
 "snooze": ("Eyes permanently closed = `eye_mode` arc in every expression. Slouch = posture. Pom-pom flops on its own bob bone.", "Yawn expression/action: not built."),
 "captain_crumbs": ("Chef jacket = long top + `buttons` rows 2. Striped pants = bottoms `vstripes`. Eyepatch and curly moustache are separable parts.", "The skull-and-spoon badge is a plain round badge (`chef_hat.badge`), not a drawn skull and spoon. Flour dusting: use `smudge` in a light colour, or particles in-game."),
}
HOME = {"foreman_dot": "The Hill", "granny_gravel": "The Hill", "mayor_pip": "The Hill", "lampy": "The Hill", "professor_fizz": "Junk Yard Zap",
        "scrap": "Junk Yard Zap", "big_tiny": "Junk Yard Zap", "coach_whistle": "Spaceballs", "zorp": "Spaceballs", "ribbit": "Spaceballs",
        "astro_ana": "Spaceballs", "old_reel": "Life of a Worm", "bloom": "Life of a Worm"}

def pat(d):
    p = d.get("pattern")
    if not p:
        return []
    return [(x if isinstance(x, str) else x["type"]) for x in (p if isinstance(p, list) else [p])]

def row(d):
    b = d["body"]; o = d["outfit"]
    body = ", ".join(f"{k} {v}" for k, v in b.items())
    head = f"{d['head'].get('shape', 'round')} {d['head'].get('size', 1.0)}"
    feats = [f["type"] for f in d["head"].get("features", [])]
    pieces = []
    if feats: pieces.append("features: " + ", ".join(f"`{x}`" for x in feats))
    if d["headwear"]["type"] != "none": pieces.append(f"headwear `{d['headwear']['type']}`")
    if d["hair"]["style"] != "none": pieces.append(f"hair `{d['hair']['style']}`")
    pp = pat(o["top"]) 
    pieces.append(f"top {o['top']['style']}" + (" + " + ", ".join(f"`{x}`" for x in pp) if pp else ""))
    pb = pat(o["bottoms"])
    pieces.append(f"bottoms {o['bottoms']['style']}" + (" + " + ", ".join(f"`{x}`" for x in pb) if pb else ""))
    sh = o["shoes"]
    extra = [k for k in ("socks", "size", "color_r", "color_l") if k in sh]
    pieces.append(f"shoes `{sh['style']}`" + (f" ({', '.join(extra)})" if extra else ""))
    if d["costume"]: pieces.append("costume " + ", ".join(f"`{c['piece']}`" for c in d["costume"]))
    fx = [(e if isinstance(e, str) else e["type"]) for e in d["face"].get("extras", [])]
    face = f"mouth `{d['face'].get('mouth', 'smile')}`" + (", extras " + ", ".join(f"`{x}`" for x in fx) if fx else "")
    pieces.append("face: " + face)
    how, missing = NOTES[d["id"]]
    return f"| [{d['name']}](../avatar/kit/examples/sheets/{d['id']}.json) | {HOME.get(d['id'], 'universal')} | {body}; head {head}; skin `{d['skin']}` | {'; '.join(pieces)} | {how} | {missing or 'nothing'} |"

doc = f"""# Sheets coverage: Kaden's 19 Jarlings on kit v2

Generated by `avatar/kit/examples/make_sheet_examples.py` (2026-11-10). Each row links a complete,
buildable params file in `avatar/kit/examples/sheets/`: a **starting point for the batch lanes, not
an approved look** (skin tones, exact hexes and faces are placeholders where the sheet is silent).
All 19 build to a `.glb` with the standard skeleton, were rendered front and back and looked at,
and pass the player-colour rule (`tools/check_colours.py`). Piece params: [`kit-v2.md`](kit-v2.md).

Build one: `blender -b --factory-startup -P avatar/kit/build_jarling.py -- --params avatar/kit/examples/sheets/zorp.json --out out/zorp.glb`

| Sheet | Home | Body params | Pieces | How the sheet's details are met | Not built |
| --- | --- | --- | --- | --- | --- |
""" + "\n".join(row(d) for d in S) + """

## Gear or kit piece?

- **Kit pieces (part of the character's own model):** every headwear type, pattern, shoe style and
  costume piece above. Headwear is the separable part `headwear` (an equipped hat hides it; with
  `"separate": true` it is the detachable `<id>_hat` object); goggles, eyepatch, moustache, cape and
  tail are their own separable parts, so a game can hide or detach them.
- **Equipment gear (`avatar/gear`, comes off, any Jarling can wear it):** unchanged starter set. No
  new gear items were made in this lane; hand props that the sheets imply (scissors, rock, rod,
  watering can, spoon sword) are listed as not built.
- **Species features** (`head.features`): antennae (Zorp). Horns, pointy ears and fins exist for
  later characters.

## Not built, all sheets

Hand props (ribbon scissors, rock, fishing rod, watering can, spoon sword), extra actions (hop,
bow, poses, yawn), the drawn skull-and-spoon on the chef badge, a lab coat with a real hem. No
sheet is blocked by these: each example reads as its sheet without them.
"""
(here.parent.parent.parent / "docs" / "sheets-coverage.md").write_text(doc)
print("wrote docs/sheets-coverage.md")
