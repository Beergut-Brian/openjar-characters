# The roster: who players can be

Design: the character chooser plan (Kaden, 2026-11-10). Every game's start menu (the template's
Showtime lobby) and the launcher's join/ready step let each player pick a character. Only
**playable** characters can be picked; world residents (Mole, Gnome Foreman, Caveman, Dragon; the proposed
cow, body `quadruped`) never appear. Rules every playable character follows: README "Playable characters".

## 1. Reading the roster

Games consume this repo as a submodule at `addons/openjar/characters/`, pinned to a tag. Read
`characters.json` from that pinned copy:

| Key | Meaning |
| --- | --- |
| `roster` | playable ids in chooser order: the P1 default, the P2 default, then the rest by id |
| `defaults` | `{"P1": "jeff", "P2": "chuck"}`: who a slot starts as when nothing was picked |
| `player_colours` | `{"P1": "#3cc24a", "P2": "#e4393c"}`: the slot's ring/arrow/glow/HUD colour, whoever is picked |
| `body_types.standard` | the kit params a playable body may use and their limits |
| `characters[i].playable` | `true` only for roster members |
| `characters[i].default_for` | `1`, `2` or `null` |
| `characters[i].body_type` | `"standard"` for every playable character |
| `characters[i].model_3d` | the 3D master, `characters/<id>/refs/jarling/<id>.glb` (or `null`) |
| `characters[i].jarling_params` | `characters/<id>/jarling.json` (or `null`) |
| `characters[i].pixel` | `{"alt_form", "source", "function"}`: the pixel form and its sprite code, e.g. `tools/pixel/residents.py`, `jeff` (or `null`) |
| `characters[i].voice` / `barks` | voice folder and the stock bark names in it (empty until recorded; fall back to a generic set) |

Paths are relative to the repo root (prefix them with `res://addons/openjar/characters/`). The
chooser cycles `roster`; a 3D game spawns `model_3d`, The Hill draws the `pixel` form. Because
every playable character is a standard Jarling, gear, animations and collision need no per-character
code. Use one collision shape for all of them.

```gdscript
const LIB := "res://addons/openjar/characters/"
var lib: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(LIB + "characters.json"))
var by_id := {}
for c in lib.characters: by_id[c.id] = c
func scene_for(id: String) -> PackedScene: return load(LIB + by_id[id].model_3d)
```

## 2. The shared picks file

Picks are remembered across every game and the launcher in one file **outside** any game's own
save folder:

- Path: `<OS data dir>/openjar/players.json`. Linux `~/.local/share/openjar/players.json`
  (`$XDG_DATA_HOME/openjar/` when set), Windows `%APPDATA%\openjar\players.json`, macOS
  `~/Library/Application Support/openjar/players.json`. Godot: not `user://` (that is per game);
  build it from `OS.get_data_dir()` + `/openjar/players.json`.
- Shape: keyed by the launcher's **save profile** id, then **player slot**:

```json
{
  "p1": {"P1": "jeff", "P2": "chuck"},
  "p2": {"P1": "chuck", "P2": "jeff"}
}
```

- **Read** on start (the template's `Roster` autoload; the launcher). **Write** the moment a pick
  changes, not on quit: read the file, change only your profile's slot, write it back whole
  (write to `players.json.tmp`, then rename, so a crash never leaves half a file).
- Keep keys you don't know (other profiles, future slots `P3`, `P4`).

## 3. Launch args

When the launcher starts a game it passes the current picks:

```
--p1-char=<id> --p2-char=<id>
```

(Godot: in `OS.get_cmdline_user_args()` after `--`, or `OS.get_cmdline_args()`.) They win over the
file, so a game still gets the right picks if the file is missing or unwritable. A pick made in the
game is still written to the file.

## 4. Resolving a slot's character

In this order, taking the first that is **in this game's pinned `roster`**:

1. `--pN-char` launch arg
2. `players.json[<profile>][PN]`
3. `defaults.PN`
4. the first `roster` id not taken by the other player

Unknown, removed or non-playable ids (an id from a newer library, a resident, a typo) are skipped,
never an error. The same character twice is not allowed: if both slots resolve to the same id, P2
moves to the next free roster id. While cycling, the other player's pick shows as taken and is
skipped.

## 5. How a new character joins the roster

1. Approved `bible.md` and `look.md` (README "Process for a new character"). Header:
   `**Kind:** universal. **Playable:** false. **Default for:** none. **Body:** standard.`
2. **3D master first**: `jarling.json` on the standard body (only `build`, `height` 0.8-1.3,
   `leg_scale` 0.8-1.2, `width` 0.75-1.5, `belly` 0-1; outfit main colours ΔE2000 >= 20 from both player colours, skin and hair >= 10 (`tools/check_colours.py <file>`); no player green/red anywhere), built to `refs/jarling/<id>.glb`, with
   turnaround and expression renders. Credits in `CREDITS.md`.
3. **Pixel form** for The Hill, traced from the 3D side view: a `## Alt form: the-hill pixel`
   section in `look.md` with `Sprite source: \`tools/pixel/<file>.py\` (\`<id>()\`)`.
   From batch 1 on, each playable character has its own `tools/pixel/<id>.py` following
   `tools/pixel/jarling_frames.py`: `<id>()` is the front form (40 x 32 canvas, 32 px = 1.2 m, feet on
   the bottom row, 1 px `#2A1E2C` outline; this is what a game's `sync_characters.sh` vendors as
   `pixel.png`), and `sheet()` is a 128 x 224 sheet of 32 x 32 frames facing right in The Hill's
   player layout (rows idle, walk, air, dig_side, dig_down, ride, sleep; pivot 16,32), also saved as
   `refs/pixel/<id>_frames.png` + `<id>_frames.json`. Check that every prop still reads at game size
   (`tools/pixel/batch1_sheets.py read` is the pattern).
4. **Voice set** in `voice/` (bark `.ogg`s, each credited).
5. Once Kaden approves: set `**Playable:** true`, run `tools/build_index.py`, run
   `godot/run_tests.sh` (must end `RESULT: PASS`), PR, tag a release. Games see the new character
   when they bump their pin.

`default_for` stays with Jeff (1) and Chuck (2) unless Kaden says otherwise.
