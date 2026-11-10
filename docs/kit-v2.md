# Jarlings kit v2: one standard body for every sheet

Kit v2 (2026-11-10) lets the standard humanoid Jarling be fat or skinny, any skin colour, with
species features (antennae, horns, pointy ears, fins) and data-driven hair, and adds the headwear,
patterns, shoes, props and face extras that Kaden's 19 sheets need. Everything is still one
skeleton, the same four actions, the same ten equipment slots and the same gameplay collision.
Sheet-by-sheet params: [`sheets-coverage.md`](sheets-coverage.md).

Everything below is a key in a character's `jarling.json`. Unknown names raise a clear error at
build time. Build and look:

```
blender -b --factory-startup -P avatar/kit/build_jarling.py -- --params my.json --out out/my.glb
blender -b --factory-startup -P avatar/kit/render_refs.py   -- --params my.json --outdir out
blender -b --factory-startup -P avatar/kit/render_range.py  -- --lineup a.json,b.json --out out/x.png
python3 tools/check_colours.py my.json
```

## 1. Fat and skinny: `body.width`, `body.belly`

| Key | Range | What it does |
| --- | --- | --- |
| `body.build` | slim, regular, stocky, round, boxy, puffy | the base shape (unchanged) |
| `body.height` | 0.8 .. 1.3 | unchanged |
| `body.leg_scale` | 0.8 .. 1.2 | unchanged |
| `body.width` | **0.75 .. 1.5** (default 1.0) | multiplies the torso width; limbs thicken or thin with it (45% as much) |
| `body.belly` | **0 .. 1** (default: the build's own) | a soft ball belly: wider in the middle and pushed forward |

Out-of-range values are refused (`ValueError`). The bones do not change height and `root`, `spine`,
`head` do not move at all; arm and leg bones only shift sideways with the body, so every action
plays as before. The hands hang clear of the belly. Equipment slots are measured from the built
surface, so the waist, back, knee, hand and foot fit scales follow the body and the starter gear fits
the skinniest and the widest Jarling (`avatar/kit/renders/kit_v2_range.png`; tested in Godot).
Gameplay collision stays the same for everyone: width is visual only.

Skinniest = `{"build": "slim", "width": 0.75}`; widest = `{"build": "round", "width": 1.5, "belly": 1.0}`.

## 2. Any skin colour, and the player-colour rule

`skin` takes any hex. For skins outside the human range (blue, green, purple, grey; decided by hue
and saturation, `kit.is_fantasy_skin`) the blush, face lines and default brows are derived from the
skin so the face still reads. Human skins keep the original colours exactly (Jeff and Chuck are
unchanged). Overrides: `face.blush_color`, `face.line_color`, `face.brow_color`.

**The rule** (`avatar/kit/colour_rule.py`, `tools/check_colours.py`, run by `godot/run_tests.sh`):
a playable character's main **outfit** colours (headwear, top, bottoms, shoes) must be at least
**CIE ΔE2000 20** from P1 green `#3cc24a` and P2 red `#e4393c`; **skin and hair need ΔE2000 10**
(Gary's call, 2026-11-10: Kaden's sheet rule is about the main outfit colour; at 20 the check refused
natural tones such as sienna skin `#A0522D` and auburn hair `#A34E25`, both 16.3 from P2 red. At 10
every natural tone passes and a skin near P1 green, e.g. `#4FCB5C` at 2.9, still fails). The
distances below are against the outfit limit of 20; as a skin, anything from 10 up passes. A green alien uses a clearly
different green. Greens that pass: lime `#D4F25A` (20.8), mint `#A8F0D0` (21.7), pale mint
`#B8F5D8` (23.3), sea `#7FD9C4` (21.5), olive `#7C8A2E` (20.5), dark olive `#6E7A2A` (24.8), teal
`#2A9DB0` (37.2). Greens that fail: `#B6E33B` (17.0), `#8FE3B0` (15.8), forest `#2E8B3A` (16.9).
Check any colour with `tools/check_colours.py --suggest "#RRGGBB"`.

## 3. Head features: `head.features`

Antennae, horns, pointy ears and fins belong to the species, not to a hat (Gary's call,
2026-11-10), so the character can still wear any hat or helmet on top.

```json
"head": {"ears": "none", "features": [{"type": "antennae", "count": 2, "tip": "#FFD23F"}]}
```

- Each feature is its own skinned part `<id>_part_feature_<type>` (extras `jarling_part`), listed in
  the rig extras `jarling_features`, on its own bones under `head` (`feat_antenna.1`, `feat_horn.1`,
  `feat_ear.L`, `feat_fin.1`). Antennae, ears and fins get the same soft secondary bob as Jeff's comb
  in every standard action; horns are rigid.
- In Godot: `JarlingEquipment.features()` lists them. A hat leaves them visible (antennae poke out
  of the bucket hat). A closed helmet that cannot fit them says so in its gear JSON:
  `"hides_features": ["antennae"]` or `true` for all; they come back when it is taken off.
- Clothing-like headwear (hard hat, top hat, hoods, fishbowl ...) stays `headwear`.

## 4. Hair: styles, presets and pieces

`hair.style` is a scalp cap (`short`, `buzz`, `bob`, `sleek`, `swoop`, `curly`, `afro`, `mane`,
`spiky`, `bun`, `ponytail`, `long`, `none`) or a preset (`puffs`, `top_bun`, `upright`, `pigtails`,
`mohawk`, `tuft_top`). `hair.pieces` adds buns, puffs, tufts, spikes and tails anywhere:

```json
"hair": {"style": "sleek", "color": "#3B2A20",
         "pieces": [{"type": "puff", "at": [38, 95], "size": 0.32, "mirror": true}]}
```

`at` is `[elevation°, azimuth°]` on the head (azimuth 0 = front, 90 = the character's left, 180 =
back); sizes are in head radii. Under headwear the hat type decides: `tuck` (default: the cap is
clamped under the hat and pieces are dropped unless a piece has `"keep": true`), `free` (fishbowl:
hair untouched), `hide` (hoods, box head). Override per character with `headwear.hair`. Hat gear
fit ignores hair pieces (it follows the scalp), so a tall hairdo can poke through an equipped hat.

## 5. Other new keys in the core

| Key | What |
| --- | --- |
| `outfit.top.pattern`, `outfit.bottoms.pattern` | a pattern name, a layer dict or a list of layers (tables below); `top.sleeve` sets the sleeve colour |
| `outfit.shoes.color_l` / `color_r` (also `sole_`, `style_`) | mismatched shoes |
| `outfit.shoes.size` | scales the finished shoes (1.35 = enormous sneakers) |
| `outfit.shoes.socks` | `{"color", "color_l", "color_r", "height" 0..1 of the leg, "cuff"}`: tall or mismatched socks |
| `headwear.scale` on `beanie` | 0.45 = the smallest beanie perched on the crown |
| `face.extras` | drawn face details (table below) |
| `face.mouth_width` | scales the mouth |
| `face.expressions.neutral` | overrides for the resting face, e.g. `{"eye_mode": "arc"}` for eyes closed in happy arcs |

For plug-in authors: `kit.HEADWEAR`, `HEADWEAR_OPTS`, `COSTUME`, `SHOES`, `PATTERNS`, `FACE_EXTRAS`,
`MOUTH_DRAW`, `FEATURES`, `HAIR_PIECES`, `HAIR_PRESETS`; `Builder.torso_point(t, th)` (follows width
and belly), `add_bob_bone`, `mats.glass`, `mats.emit`, `lamps` (a real spot light on the head bone,
exported in the glb). Any `pieces_*.py` next to the kit is loaded automatically.

## 6. Pieces

Generated from the plug-ins' docstrings by `tools/kit_pieces_doc.py` (`godot/run_tests.sh` fails if
a registered piece is missing here).

<!-- PIECES:START (tools/kit_pieces_doc.py) -->
### `avatar/kit/pieces_features.py`


Kit v2: head features, data-driven hair pieces, hair presets, face extras and extra mouths.


Head features (`head.features`: list of dicts; body features of the species, NOT hats, so any hat


or helmet still goes on top; each is the part `<id>_part_feature_<type>` on its own bones under `head`):

| Name | Params (defaults) |
| --- | --- |
| `antennae` | count 2 (1..4), color (default: darker skin), tip (default: color), length 0.75 (x R), spread 30 (deg from straight up), ball 0.15 (x R), thickness 0.035 (x R), back 0 (deg the stalks lean toward the back of the head) |
| `horns` | style "nub"/"curved", count 2 (1 = one centre horn), color "#F1E7CF", size 1.0 |
| `pointy_ears` | color (default: skin), length 0.55 (x R), up 0.5 (how much they point up); replace the round ears |
| `fins` | count 1/3 (centre crest, plus one each side), color (default: darker skin), size 1.0 |

Hair pieces (`hair.pieces`: list; every piece takes `at` [elevation deg, azimuth deg] with azimuth


0 = front, 90 = the character's left, 180 = back; `size` (x R); `color` (default hair colour);


`mirror` true = also at -azimuth; `keep` true = stays when a hat tucks the hair):

| Name | Params (defaults) |
| --- | --- |
| `puff` | round puff / bun: size 0.32, squash 1.0 (height factor), out 0.55 (how far it sits out) |
| `bun` | same as puff (size 0.36) |
| `tuft` | short soft lock: size 0.2, length 0.45, dir "out"/"up"/[x,y,z] |
| `spike` | pointed lock: size 0.2, length 0.7, dir "out"/"up"/[x,y,z], lean 0.25 (outward lean when "up") |
| `tail` | hanging pony/pig tail: size 0.22, length 0.8 |

Hair presets (`hair.style`): puffs (two side puffs), top_bun, upright (wild hair straight up),


pigtails, mohawk, tuft_top; plus every cap style of the core (short, buzz, bob, sleek, ...).


Face extras (`face.extras`: list of names or dicts, drawn into the face atlas):

| Name | Params (defaults) |
| --- | --- |
| `smudge` | side "L"/"R" (the character's), color "#6B5A4A", size 1.0: dirt / flour smudge on a cheek |
| `scorch_brow` | side "L"/"R", color "#2A2420": that eyebrow is a sooty scorch mark |
| `mask` | color, trim, full-head wrestling mask: whole head in `color`, skin shows in eye and mouth openings edged in `trim` (use head.ears "none") |
| `freckles_big` | color (default darker skin): bolder freckles across the cheeks and nose |

Mouths (`face.mouth`, besides the core's smile, grin, grin_top, grin_two, o, smirk, set, grit, flat, frown, none):

| Name | Params (defaults) |
| --- | --- |
| `grin_gap` | open grin with a gap between the front teeth |
| `yell` | wide open happy shout |
| `wide` | wide, flat, pleased smile |

### `avatar/kit/pieces_headwear.py`


Kit v2 headwear and head accessories for the standard Jarling body.


All sizes are multiples of the head radius R, so every piece fits every head size and shape.


Colours default to neutral toy colours (never the player colours). Hats built with `place_parts`


take `separate` (true: on the detachable `<id>_hat` object), `tilt_deg` (positive lowers the front)


and `fit` (height of the hat base above the head centre, in R: lower sits lower on the brow).


Headwear (`headwear.type`; hair mode in HEADWEAR_OPTS):

| Name | Params (defaults) |
| --- | --- |
| `animal_hood` | color="#2BB3A3", inner=<color darker>, opening_deg=52, eyes=None {"color": "#FFFFFF", "pupil": "#1B1B20", "size": 1.0, "el": 50, "apart": 34}, teeth=None (colour), teeth_n=6, teeth_span=110, spikes=None (colour), spike_n=6, ears=None (colour); hair hide |
| `fishbowl` | tint="#CFE8FF", alpha=0.07, scale=1.0, collar="#F4F4F0", collar_size=1.0, collar_accent=None (colour), rim="#8FC7E8" (None: off), rim_alpha=0.55, rim_power=0.35, highlight=True, highlight_alpha=0.7, highlight_size=1.0; hair free |
| `hard_hat` | color="#FFC93C", fit=0.30, tilt_deg=6, separate=False; hair tuck |
| `top_hat` | color="#2A2A33", band="#7E57C2", height=1.6 (R), scale=1.0, tilt_deg=0, separate=False; hair tuck |
| `miner_helmet` | color="#F4F4F0", lamp="#3A3A46", light="#FFF2C0", glow=6.0, lamp_size=1.0, watts=30, spot_deg=55, fit=0.28, tilt_deg=0, separate=False; hair tuck |
| `colander` | color="#C8CDD3", holes="#3A3F48", fit=0.25, tilt_deg=4, separate=False; hair tuck |
| `pot_helmet` | color="#B9C0C8", handle="#2A2A33", handle_len=1.5 (R), height=1.0, fit=0.18, tilt_deg=0, separate=False; hair tuck |
| `nightcap` | color="#3E7BEA", stripe="#F4F4F0", pom=<stripe>, stripes=6, side="L", length=1.0, bob=1.0; hair tuck |
| `chef_hat` | color="#FBFBF7", band=<color>, badge=None (colour), height=1.0, fit=0.32, tilt_deg=0, separate=False; hair tuck |
| `bucket_hat` | color="#C9B48A", band=<color darker>, brim=0.55 (R), lure=None (colour), lure_deg=50, fit=0.40, tilt_deg=0, separate=False; hair tuck |
| `sun_hat` | color="#E9C97A", band="#E86FA6", brim=1.3 (R), waves=7, flower=None (colour), flower_mid="#FFD23F", flower_deg=40, fit=0.40, tilt_deg=0, separate=False; hair tuck |
| `cowboy_hat` | color="#C8955A", band="#5A3A22", brim_width=0.80 (R), curl=1.0 (side curl-up), crown_height=1.0 (R), pinch=1.0, crease=1.0, fit=0.45, tilt_deg=0, separate=False; hair tuck |
| `box_head` | color="#C49A6C", tape="#E6CFA0", scale=1.0, hole_w=0.64 (R), tilt_deg=0, separate=False; hair hide |

Costume pieces on the head (`costume[]`, each its own separable part named after the piece):

| Name | Params (defaults) |
| --- | --- |
| `goggles` | pos="forehead"/"eyes", style="round"/"safety", color="#4A4F5A", strap=<color darker>, lens="#9FD8F0" (see-through over the eyes), size=1.0, height=0.40 (forehead) |
| `eyepatch` | side="L"/"R" (L = the character's left, +X), color="#1B1B20", strap="#1B1B20", size=1.0 |
| `moustache` | style="curly"/"bushy", color=<hair colour or "#4A2F23">, size=1.0, height=<between nose and mouth> |

### `avatar/kit/pieces_outfit.py`


Kit v2 outfit pieces for the standard Jarling body: shirt/trouser patterns, shoes, costume pieces.


Patterns (`outfit.top.pattern` / `outfit.bottoms.pattern`, a name, a layer dict or a list of layers;


a layer inherits `color`/`accent` from the top/bottoms dict):

| Name | Params (defaults) |
| --- | --- |
| `vstripes` | accent "#1A1A1E", count 12 (top) / 8 (bottoms), offset 0.0 (turns, 0.5 = stripe edge at the front) |
| `vacation` | accent "#FF6F91" (flowers), accent2 "#2FA88A" (leaves), center "#FFE066", count 14, seed 7, size 1.0 |
| `hstripe` | accent "#F2F2EE", v 0.58, width 0.10, edge null (thin edge lines colour, e.g. silver on hi-vis) |
| `stars` | accent "#FFE066", count 26 (top) / 14 (bottoms), size 1.0, seed 3 |
| `patches` | accent "#E8A33D", accent2 "#5B8FD6", stitch null (default darker accent), count 3 (2 or 3) |
| `emblem` | shape "star" ("shield"/"star"/"circle"), accent "#FFD23F", size 0.13 (half height in V), v 0.62, rim null, inner null |
| `buttons` | accent "#2A2F5A", rows 1 (1 or 2), count 5, line null (rows 1: darker centre line, default shade of color) |
| `vest` | accent "#5A4A8C" (vest), open 0.10 (front strip half width in U), pockets true, trim null |
| `collar` | accent "#8A5CC9", depth 0.34 (how far the V comes down, in V), width 0.07, inner null (colour inside the V) |
| `bib` | accent "#3E6FB0", top 0.66 (V), width 0.22 (half width in U), button "#F2D16B" |
| `belly_panel` | accent "#FFE38A", v 0.42, width 0.22 (half width in U), height 0.34 (half height in V), soft 0.02 |
| `dials` | accent "#FF9F1C", line "#2A2A33", size 1.35 |
| `jersey` | accent "#F2B632" (collar band), number "55" (digits), number_color "#F7F7F5", outline null (thin number edge colour; null = accent), front true, back true, size 0.36 (number height in V), v 0.56, v_back 0.50, text null (block letters across the upper back, A-Z 0-9 and space), text_v 0.83, text_size 0.065, aspect 0.62 (glyph width squash: the torso texture is wider than tall) |

Shoes (`outfit.shoes.style`; `color` is per side, `size`/`socks` are the core's):

| Name | Params (defaults) |
| --- | --- |
| `sandals` | color "#8B5A2B" (straps; the sole is a darker shade), foot_size 1.0; the foot is B.skin |
| `moon_boots` | color "#D9DCE3", sole "#7C808A", rings 2 |
| `rain_boots` | color "#FFD23F", sole "#2A2A33", height 0.20 (top of the shaft, m above ground) |
| `clogs` | color "#4FB3A9", sole null (darker color), strap true |
| `slippers` | color "#F2B8C6" |
| `dress` | color "#2A2A33", sole null |
| `footies` | color = the shoes colour (match the onesie) |
| `wrestling_boots` | color "#2A3A8C", lace "#F7F7F5", sole null, height 0.235 |
| `chunky_boots` | color "#8B5A2B", sole "#3A3330", cap null (toe cap, default darker color) |
| `high_tops` | color "#1A1A1E" (upper), accent "#2A6FD6" (side panel, collar, heel stripe), sole "#F7F7F5", lace "#F7F7F5", height 0.15 (top of the collar, m above ground) |

Costume (`costume: [{"piece": name, ...}]`):

| Name | Params (defaults) |
| --- | --- |
| `whistle_cord` | color "#FFD23F" (whistle), cord "#2A6FD6", t 0.56 (height on the torso), x 0.0 (turn off centre, radians), size 1.0 (whistle scale; Coach Whistle uses 1.5) |
| `sash` | color "#C8A2F0", side "L" (the shoulder it goes over), width 0.17 (in torso height) |
| `cape` | (part "cape") color "#7A2E8C", trim "#F2D16B", length 1.0 (1 = knee height), flare 0.3 |
| `back_spikes` | color "#2FA88A", count 5, size 1.0 |
| `dino_tail` | (part "tail") color "#5FB85A", spikes null (colour: adds soft spikes along the top), length 1.0 |
| `box_torso` | color "#C49A6C", accent "#FF9F1C" (dial fills), line "#3A2A1E" (marker) |
| `hose_arms` | color "#B8BCC4", rings 9 |
| `shoulder_pads` | color <top colour> (the pads under the shirt), size 1.0, stripes null (colour: two rings round each short sleeve), hem null (colour: sleeve hem ring); part of the top, on the spine bone, so raised arms swing out from under them |
| `long_skirt` | color "#6A5ACD", length 1.0 (0 = just below the hips, 1 = the ankles), flare 1.0, mud null (colour) |

The `whistle` piece in pieces_hill.py sits at a fixed depth (made for the beard), use `whistle_cord` on other bodies.


### `avatar/kit/pieces_hill.py`


Kit pieces for The Hill's people (standard body): the Gnome Foreman and the Caveman.


Headwear: `cone_hat` (teal cone + detachable tiny hard hat), `ice_cube`.


Costume:  `gnome_beard`, `vest_stripes`, `clipboard` (part `prop`), `whistle`,


`mane_beard`, `fur_tunic`, `cloth_club` (part `prop`).


Actions:  `march`, `write`, `salute`, `whistle` (gnome); `polish`, `point`, `wave` (caveman).


<!-- PIECES:END -->

## Gait

`"gait"` (top level, optional) swaps a standard Jarling's `run` and `idle` for a cosmetic variant, registered
in `kit.GAITS` by `avatar/kit/pieces_gait.py`. `"hop"` (Ribbit): `run` is a two-footed hop (crouch, push off,
tucked in the air with the root rising, land with a squash) and `idle` settles and gives a small bounce now and
then. Same action names, frame ranges and loop flags as the standard set (`run` 1-17, `idle` 1-49), the root
only moves vertically (the game moves the character), `kick` and `cheer` are unchanged, and the rig gets the
extra `jarling_gait`. Gameplay and collision never change. Without `"gait"` every action is exactly as before.
