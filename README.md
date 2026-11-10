# Open Jar Games — character library

The recurring cast of Open Jar Games. Every game pulls characters from here; no game invents a
recurring character on its own. Rendered in each game's own technique, but always the same character.

| Character | Playable | Role | One line |
| --- | --- | --- | --- |
| [Jeff](characters/jeff/bible.md) | **yes**, P1 default | kicker in Spaceballs | Fun-loving hippy in a chicken costume, jeans, barefoot |
| [Chuck](characters/chuck/bible.md) | **yes**, P2 default | kicker in Spaceballs | T-Rex trucker hat, black tie-dye, jeans, cowboy boots. Personality: proposed, awaiting Kaden |
| [The Mole](characters/mole/bible.md) | no (resident) | shovel thief, then Lost & Found, in The Hill | Nearsighted, polite shovel thief who apologises to boulders |
| [The Gnome Foreman](characters/gnome_foreman/bible.md) | no (resident) | foreman, then Gnome Village, in The Hill | Tiny, serious, clipboard in hand; passes everything |
| [The Caveman](characters/caveman/bible.md) | no (resident) | museum keeper in The Hill | Delighted by everything modern, polishes treasures, one ice cube on his head |
| [The Dragon](characters/dragon/bible.md) | no (resident) | landmark (Dragon Perch) in The Hill | Huge, sleepy, huggable, snores smoke rings |

All six are `kind: universal`.

**Alt forms.** A look.md section `## Alt form: <name>` is an approved per-game variant (listed in
`characters.json` as `alt_forms`). Jeff and Chuck have `the-hill pixel` (hard hat, 32 px), shown in
`characters/residents_lineup.png`; sprite code in `tools/pixel/`.

**Kinds.** Every character is `universal`: any game can use them in any role. The old
`player-locked` kind (Jeff always P1, Chuck always P2) was retired by Kaden on 2026-11-10 with the
character chooser; the index still has `kind`/`player` fields for old readers, always `universal`/`null`.

## Playable characters (the roster)

Players pick who they are in every game's start menu and in the launcher (see
[`docs/roster.md`](docs/roster.md)). Only **playable** characters can be picked. Each bible's header
says `**Playable:** true|false`, `**Default for:** none|1|2` and `**Body:** standard`; the index lists
the playable ids in display order under `roster` (defaults first). Today: Jeff (P1 default) and
Chuck (P2 default). The Hill residents (Mole, Gnome Foreman, Caveman, Dragon) are not playable.

Rules for every playable character (checked by `godot/run_tests.sh`):

1. **Player colours belong to the player slot, never to a character.** P1 green `#3cc24a` and P2
   red `#e4393c` are for rings, arrows, glows and HUD around whoever you play. No playable character
   uses either as a main colour (skin, hair, headwear, top, bottoms, shoes in `jarling.json`), and
   new playable characters use neither anywhere. Jeff's green accents and Chuck's red accents are
   from their approved looks and stay until Kaden says otherwise (a look change needs him).
2. **Standard humanoid Jarling body.** A playable character is built on `avatar/kit` and changes
   only `body.build` (`slim`, `regular`, `stocky`, `round`, `boxy`, `puffy`), `body.height`
   (**0.8 to 1.3**) and `body.leg_scale` (**0.8 to 1.2**). Same skeleton, actions (`idle`, `run`,
   `kick`, `cheer`, ...) and ten equipment slots, so every game's animations, gear and chooser work
   with no per-game work. Non-standard body types (`**Body:** <other>`) are for non-playable
   residents only. The limits are also in `characters.json` under `body_types.standard`.
3. **Same gameplay collision for everyone.** Size is visual only: a game uses one collision shape
   for every playable character, never one sized from the model, so a pick never changes difficulty.
4. **Complete before playable:** a 3D master (`refs/jarling/<id>.glb` + `jarling.json`), a pixel
   form (a `## Alt form: <name> pixel` section in `look.md` naming its sprite source), and a voice
   folder. Then `playable: true`, once Kaden approves.

## Layout

```
characters.json              machine-readable index (games read this)
characters/<name>/bible.md   who they are: personality, how they talk, signature move, fears, relationships
characters/<name>/look.md    silhouette rules, fixed colours, costume pieces that survive every art style
characters/<name>/refs/      reference sheet: front/side/back, 3 expressions, 1 action pose; per-technique renders
characters/<name>/voice/     Chatterbox voice profile, seed clips, 20-30 pre-rendered stock barks (.ogg), prompt
characters/<name>/prompts.md ComfyUI / image-to-mesh prompt packs per technique
characters/_template/        copy this to start a new character
docs/roster.md               the roster contract: picks file, launch args, joining the roster
```

## Process for a new character

1. Anyone proposes: a name and a one-line pitch (Kaden, the maker profile, or a game's design sprint).
2. The maker profile drafts `bible.md` and `look.md`.
3. **Kaden approves or edits** the bible and look. Nothing visual is made before this.
4. A short-lived Character lane (Claude Code session in this repo) produces the reference sheet,
   voice profile, stock barks and prompt pack on a branch, then opens a PR. The maker profile merges.
5. Games consume this repo as a git submodule at `addons/openjar/characters/`, pinned to a tag.
6. When a game renders a character in a new technique, the render goes back into `refs/` by PR.

## Proposals

Drafts awaiting Kaden live in `proposals/<id>/` and are listed under `proposed` in `characters.json`
(never under `characters`, so games do not see them). Once Kaden approves one, promote it with
`git mv proposals/<id> characters/<id>`, set the bible's `## Status` to "Approved by Kaden <date>" (the
index reads `approved` from it), then run `tools/build_index.py`.

None right now. The four Hill residents were approved by Kaden on 2026-11-09 (D46 a) and promoted.

## Consuming from a game

```gdscript
var lib := JSON.parse_string(FileAccess.get_file_as_string("res://addons/openjar/characters/characters.json"))
var roster: Array = lib.roster                 # ["jeff", "chuck", ...], chooser order
var p1: String = lib.defaults.P1               # "jeff" when nothing was picked yet
```

Full contract (picks file, launch args, fallbacks): [`docs/roster.md`](docs/roster.md).

Stock barks: `Audio.bark("jeff", "yay")` resolves to `characters/jeff/voice/yay.ogg`.
