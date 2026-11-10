# CLAUDE.md — openjar-characters

This is a content library, not a Godot project. Read `README.md` for the process, then the
character you are working on.

- Never change a character's `kind`, `playable`, `default_for`, or fixed colours without Kaden's
  approval in writing (a PR comment from him counts). `player-locked` was retired 2026-11-10.
- Player colours belong to the player slot, never to a character: P1 green `#3cc24a`, P2 red
  `#e4393c`. No playable character uses either as a main colour; new ones use neither at all.
- Playable characters use the standard humanoid Jarling body (`avatar/kit`; only `build`, `height`
  0.8-1.3, `leg_scale` 0.8-1.2), with the same gameplay collision for all. Non-standard bodies are
  for non-playable residents. See README "Playable characters" and `docs/roster.md`.
- Never create a new character folder without an approved `bible.md` and `look.md` first.
- Every image in `refs/` and every `.ogg` in `voice/` gets a line in that character's `CREDITS.md`
  (tool, prompt, license). Original designs only: nothing that depicts or imitates recognisable
  characters, brands or artists.
- `characters.json` is regenerated from the folders by `tools/build_index.py`; do not hand-edit it.
- Tag a release (`v0.x.y`) whenever a character's look or voice changes; games pin to tags.
- Git LFS for images and audio (see `.gitattributes`).
- Branch per change, PR to `main`. The maker profile merges.
