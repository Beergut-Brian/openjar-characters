# CLAUDE.md — openjar-characters

This is a content library, not a Godot project. Read `README.md` for the process, then the
character you are working on.

- Never change a character's `kind`, `player`, or fixed colours without Kaden's approval in writing
  (a PR comment from him counts).
- Never create a new character folder without an approved `bible.md` and `look.md` first.
- Every image in `refs/` and every `.ogg` in `voice/` gets a line in that character's `CREDITS.md`
  (tool, prompt, license). Original designs only: nothing that depicts or imitates recognisable
  characters, brands or artists.
- `characters.json` is regenerated from the folders by `tools/build_index.py`; do not hand-edit it.
- Tag a release (`v0.x.y`) whenever a character's look or voice changes; games pin to tags.
- Git LFS for images and audio (see `.gitattributes`).
- Branch per change, PR to `main`. The maker profile merges.
