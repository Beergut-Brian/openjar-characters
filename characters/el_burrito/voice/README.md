# el_burrito voice

- `*.ogg` (top level): stock barks, one per cue in `../voice.md`. `Audio.bark("el_burrito", "<cue>")` plays them.
- `lib/`: non-verbal sounds and extras (laughs, sighs, gasps, yawn, effort, catchphrase big and calm). `Audio.bark("el_burrito", "lib/<name>")`-style lookups or direct loads.
- `source/master.ogg`: a ~1 min varied read. New lines later come from Chatterbox with this as the clone reference (or a temporary ElevenLabs instant clone of it), so the voice never depends on a saved ElevenLabs voice.

Picked by Kaden 2026-11-10 (v3 design take 1).
