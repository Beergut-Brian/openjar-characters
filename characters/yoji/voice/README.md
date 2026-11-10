# yoji voice

No audio yet: Gary generates it from `../voice.md` (Southern US male, 30s; 8 barks; catchphrase "YEEHAW! TOUCHDOWN!" is the `win` bark).
Layout when it lands, same as the other characters:

- `*.ogg` (top level): stock barks, one per cue in `../voice.md`. `Audio.bark("yoji", "<cue>")` plays them.
- `lib/`: non-verbal sounds and extras (laughs, gasps, effort, catchphrase big and calm).
- `source/master.ogg`: a ~1 min varied read, the clone reference for later lines.

Every `.ogg` gets a row in `../CREDITS.md`.
