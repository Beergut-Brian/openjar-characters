# Open Jar Games — character library

The recurring cast of Open Jar Games. Every game pulls characters from here; no game invents a
recurring character on its own. Rendered in each game's own technique, but always the same character.

| Character | Kind | Role | One line |
| --- | --- | --- | --- |
| [Jeff](characters/jeff/bible.md) | player-locked, **P1 (green)** | kicker in Spaceballs | Fun-loving hippy in a chicken costume, jeans, barefoot |
| [Chuck](characters/chuck/bible.md) | player-locked, **P2 (red)** | kicker in Spaceballs | T-Rex trucker hat, black tie-dye, jeans, cowboy boots. Personality: proposed, awaiting Kaden |
| [The Mole](characters/mole/bible.md) | universal | shovel thief, then Lost & Found, in The Hill | Nearsighted, polite shovel thief who apologises to boulders |
| [The Gnome Foreman](characters/gnome_foreman/bible.md) | universal | foreman, then Gnome Village, in The Hill | Tiny, serious, clipboard in hand; passes everything |
| [The Caveman](characters/caveman/bible.md) | universal | museum keeper in The Hill | Delighted by everything modern, polishes treasures, one ice cube on his head |
| [The Dragon](characters/dragon/bible.md) | universal | landmark (Dragon Perch) in The Hill | Huge, sleepy, huggable, snores smoke rings |

**Alt forms.** A look.md section `## Alt form: <name>` is an approved per-game variant (listed in
`characters.json` as `alt_forms`). Jeff and Chuck have `the-hill pixel` (hard hat, 32 px), shown in
`characters/residents_lineup.png`; sprite code in `tools/pixel/`.

**Kinds.** `universal` characters can be used by any game in any role. `player-locked` characters
belong to one player side forever (Jeff is always P1, Chuck is always P2) and carry that player's
colour in their costume accents. The Reviewer lane rejects a game that puts a player-locked
character on the wrong side.

## Layout

```
characters.json              machine-readable index (games read this)
characters/<name>/bible.md   who they are: personality, how they talk, signature move, fears, relationships
characters/<name>/look.md    silhouette rules, fixed colours, costume pieces that survive every art style
characters/<name>/refs/      reference sheet: front/side/back, 3 expressions, 1 action pose; per-technique renders
characters/<name>/voice/     Chatterbox voice profile, seed clips, 20-30 pre-rendered stock barks (.ogg), prompt
characters/<name>/prompts.md ComfyUI / image-to-mesh prompt packs per technique
characters/_template/        copy this to start a new character
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
for c in lib.characters:
    if c.kind == "player_locked" and c.player != my_player: continue
```

Stock barks: `Audio.bark("jeff", "yay")` resolves to `characters/jeff/voice/yay.ogg`.
