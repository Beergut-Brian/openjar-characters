# Open Jar Games — character library

The recurring cast of Open Jar Games. Every game pulls characters from here; no game invents a
recurring character on its own. Rendered in each game's own technique, but always the same character.

| Character | Playable | Role | One line |
| --- | --- | --- | --- |
| [Jeff](characters/jeff/bible.md) | **yes**, P1 default | kicker in Spaceballs | Fun-loving hippy in a chicken costume, jeans, barefoot |
| [Chuck](characters/chuck/bible.md) | **yes**, P2 default | kicker in Spaceballs | T-Rex trucker hat, black tie-dye, jeans, cowboy boots. Personality: proposed, awaiting Kaden |
| [Astro Ana](characters/astro_ana/bible.md) | **yes** (proposed, playtest build) | kicker in Spaceballs | Mission-ready astronaut in a clear fishbowl helmet, two hair puffs, orange moon boots |
| [Coach Whistle](characters/coach_whistle/bible.md) | **yes** (proposed, playtest build) | kicker in Spaceballs | Barrel-chested coach in referee stripes, navy cap, whistle on a cord |
| [Ribbit](characters/ribbit/bible.md) | **yes** (proposed, playtest build) | kicker in Spaceballs | Small, round and calm in a teal frog hoodie with eyes on the hood; hops |
| [Zorp](characters/zorp/bible.md) | **yes** (proposed, playtest build) | kicker in Spaceballs | Light-blue alien tourist with two antennae and a loud holiday shirt |
| [Big Tiny](characters/big_tiny/bible.md) | **yes** (proposed, playtest build) | gentle giant in Junk Yard Zap | The widest, tallest Jarling under the smallest beanie; closed-eye smile, enormous white sneakers |
| [Foreman Dot](characters/foreman_dot/bible.md) | **yes** (proposed, playtest build) | site lead in The Hill | Short, stocky human site lead; yellow hard hat sitting low, orange hi-vis shirt. Not the Gnome Foreman |
| [Granny Gravel](characters/granny_gravel/bible.md) | **yes** (proposed, playtest build) | steamroller driver in The Hill | White bun with safety goggles pushed up into it, lavender cardigan, long skirt, yellow sneakers |
| [Lampy](characters/lampy/bible.md) | **yes** (proposed, playtest build) | tunnel guide in The Hill | Tall and thin under a white miner's helmet whose headlamp is a real light |
| [Bloom](characters/bloom/bible.md) | **yes** (proposed, playtest build) | gardener in Life of a Worm | Short and soft under a huge floppy straw sun hat with one flower; pink tee, muddy knees, purple clogs |
| [Old Reel](characters/old_reel/bible.md) | **yes** (proposed, playtest build) | the worm's fisherman nemesis in Life of a Worm | Tall and round under a tan bucket hat with one lure; bushy white brows, khaki vest, tall yellow rain boots |
| [Mayor Pip](characters/mayor_pip/bible.md) | **yes** (proposed, playtest build) | mayor of Hillville in The Hill | The smallest Jarling under a top hat nearly half his height; gold sash |
| [Professor Fizz](characters/professor_fizz/bible.md) | **yes** (proposed, playtest build) | inventor in Junk Yard Zap | Wild white hair straight up, goggles on her forehead, lab coat, one scorch-mark eyebrow |
| [Scrap](characters/scrap/bible.md) | **yes** (proposed, playtest build) | junkyard kid in Junk Yard Zap | Small kid in a colander helmet, patched yellow shirt, one orange shoe and one purple |
| [Boxbot](characters/boxbot/bible.md) | **yes** (proposed, playtest build) | universal silly, any game | Kid in a cardboard-box robot costume: head box with a face cut-out, dial-drawn body box, dryer-hose arms |
| [Captain Crumbs](characters/captain_crumbs/bible.md) | **yes** (proposed, playtest build) | universal silly, any game | Tall pirate-ish chef: very tall chef hat, eyepatch, curly moustache, round middle |
| [El Burrito](characters/el_burrito/bible.md) | **yes** (proposed, playtest build) | universal silly, any game | Short, wide masked wrestler in gold and purple with a cape |
| [Rexy](characters/rexy/bible.md) | **yes** (proposed, playtest build) | universal silly, any game | Small kid in an orange dino onesie: felt-teeth hood, yellow back spikes, short tail |
| [Sir Clank](characters/sir_clank/bible.md) | **yes** (proposed, playtest build) | universal silly, any game | Very upright boy knight with a saucepan helmet (handle out the back) and a yellow shield on his shirt |
| [Snooze](characters/snooze/bible.md) | **yes** (proposed, playtest build) | universal silly, any game | Slouchy sleepyhead in star pyjamas and a long floppy nightcap; eyes always closed |
| [The Mole](characters/mole/bible.md) | no (resident) | shovel thief, then Lost & Found, in The Hill | Nearsighted, polite shovel thief who apologises to boulders |
| [The Gnome Foreman](characters/gnome_foreman/bible.md) | no (resident) | foreman, then Gnome Village, in The Hill | Tiny, serious, clipboard in hand; passes everything |
| [The Caveman](characters/caveman/bible.md) | no (resident) | museum keeper in The Hill | Delighted by everything modern, polishes treasures, one ice cube on his head |
| [The Dragon](characters/dragon/bible.md) | no (resident) | landmark (Dragon Perch) in The Hill | Huge, sleepy, huggable, snores smoke rings |

The nineteen marked *proposed, playtest build* are from Kaden's sheets of 2026-11-10 (Jarlings batch 1: Spaceballs; batch 2: Junk Yard Zap and The Hill; batch 3: the universal sillies; batch 4: Life of a Worm, Bloom and Old Reel): built so he can playtest the chooser, not yet signed off.

**Alt forms.** A look.md section `## Alt form: <name>` is an approved per-game variant (listed in
`characters.json` as `alt_forms`). Jeff and Chuck have `the-hill pixel` (hard hat, 32 px), shown in
`characters/residents_lineup.png`; sprite code in `tools/pixel/`.

**Kinds.** Every character is `universal`: any game can use them in any role. The old
`player-locked` kind (Jeff always P1, Chuck always P2) was retired by Kaden on 2026-11-10 with the
character chooser; the index still has `kind`/`player` fields for old readers, always `universal`/`null`.

## Playable characters (the roster)

Players pick who they are in every game's start menu and in the launcher (see
[`docs/roster.md`](docs/roster.md)). Only **playable** characters can be picked. Each bible's header
says `**Playable:** true|false`, `**Default for:** none|1|2` and `**Body:** standard|critter|giant` (the body types are in [`avatar/README.md`](avatar/README.md)); the index lists
the playable ids in display order under `roster` (defaults first). Today: Jeff (P1 default) and
Chuck (P2 default), then Astro Ana, Coach Whistle, Ribbit and Zorp (batch 1, proposed; lineups
`characters/batch1_lineup.png`, `characters/batch1_pixel_lineup.png`, read check `characters/batch1_read_check.png`),
then Big Tiny, Foreman Dot, Granny Gravel, Lampy, Mayor Pip, Professor Fizz and Scrap (batch 2, proposed; lineups
`characters/batch2_lineup.png`, `characters/batch2_pixel_lineup.png`, read check `characters/batch2_read_check.png`),
then Boxbot, Captain Crumbs, El Burrito, Rexy, Sir Clank and Snooze (batch 3, the universal sillies, proposed; lineups
`characters/batch3_lineup.png`, `characters/batch3_pixel_lineup.png`, read check `characters/batch3_read_check.png`), then Bloom and Old Reel (batch 4, proposed; lineups `characters/batch4_lineup.png`,
`characters/batch4_pixel_lineup.png`, read check `characters/batch4_read_check.png`). The index sorts the non-default playables by id, so batch order is not kept in `roster`.
The Hill residents (Mole, Gnome Foreman, Caveman, Dragon) are not playable.

**3D-first (Kaden, 2026-11-10).** A character is designed as a Jarling first; every other style is
derived from that 3D master. The four Hill residents were drawn 2D-first, so their 3D masters were
backfilled and then matched to the approved sprites (status: **approved**, Kaden 2026-11-10, D49 a
with the Gnome whistle fix); their Hill pixel forms are now traced from the 3D
(`tools/pixel/retrace.sh`). Gnome Foreman and Caveman use the standard body with new kit pieces;
the Mole uses the `critter` body type and the Dragon the `giant` body type. All six in 3D:
`characters/residents_3d_lineup.png`; 3D beside the pixel redraw: `characters/residents_3d_compare.png`;
every prop at game size: `characters/read_check.png`; everyone holding things:
`avatar/kit/renders/hold_check.png` ([`avatar/README.md`](avatar/README.md) "Holding items").

Rules for every playable character (checked by `godot/run_tests.sh`):

1. **Player colours belong to the player slot, never to a character.** P1 green `#3cc24a` and P2
   red `#e4393c` are for rings, arrows, glows and HUD around whoever you play. No playable character
   uses either as a main colour (skin, hair, headwear, top, bottoms, shoes in `jarling.json`): each
   main **outfit** colour (headwear, top, bottoms, shoes) must be at least CIE ΔE2000 20 from both,
   and skin and hair at least ΔE2000 10 (`tools/check_colours.py`; Gary's call 2026-11-10: the
   sheet rule is about the main outfit colour, so natural tones such as sienna skin `#A0522D` and
   auburn hair `#A34E25` pass, while a skin close to P1 green still fails). So a green
   alien uses a clearly different green such as lime `#D4F25A`, mint `#A8F0D0` or olive `#7C8A2E`. And
   new playable characters use neither anywhere. Jeff's green accents and Chuck's red accents are
   from their approved looks and stay until Kaden says otherwise (a look change needs him).
2. **Standard humanoid Jarling body.** A playable character is built on `avatar/kit` and changes
   only `body.build` (`slim`, `regular`, `stocky`, `round`, `boxy`, `puffy`), `body.height`
   (**0.8 to 1.3**), `body.leg_scale` (**0.8 to 1.2**), `body.width` (**0.75 to 1.5**, skinny to
   very round) and `body.belly` (**0 to 1**); species features such as antennae, horns and pointy
   ears are `head.features`, not hats ([`docs/kit-v2.md`](docs/kit-v2.md)). Same skeleton, actions (`idle`, `run`,
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

Fifteen of Kaden's 19 sheets (2026-11-10) wait here: `docs/jarlings-19.md`. The four Spaceballs ones (Coach Whistle, Zorp,
Ribbit, Astro Ana) were moved to `characters/` on 2026-11-10 as a playtest build: Kaden wrote the sheets and asked to playtest
the chooser with them; their Status stays "Proposed" until he signs off. The four Hill residents were approved by Kaden on
2026-11-09 (D46 a) and promoted.
Twelve of Kaden's 19 sheets (2026-11-10) wait here: `docs/jarlings-19.md` (the four Spaceballs ones are with the batch 1 lane on its own branch). The seven Junk Yard Zap and Hill ones (Professor Fizz, Scrap, Big Tiny, Foreman Dot, Granny Gravel,
Mayor Pip, Lampy) were moved to `characters/` on 2026-11-10 as a playtest build: Kaden wrote the sheets and asked to playtest
the chooser with them; their Status stays "Proposed" until he signs off. The four Hill residents were approved by Kaden on 2026-11-09 (D46 a) and promoted.

## Consuming from a game

```gdscript
var lib := JSON.parse_string(FileAccess.get_file_as_string("res://addons/openjar/characters/characters.json"))
var roster: Array = lib.roster                 # ["jeff", "chuck", ...], chooser order
var p1: String = lib.defaults.P1               # "jeff" when nothing was picked yet
```

Full contract (picks file, launch args, fallbacks): [`docs/roster.md`](docs/roster.md).

Stock barks: `Audio.bark("jeff", "yay")` resolves to `characters/jeff/voice/yay.ogg`.
