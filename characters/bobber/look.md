# Bobber — look

## Brief (Kaden's Life of a Worm brief 2026-11-10; look from the approved bible, D89)
"The grandson is named Bobber. He is a new Jarling." Look proposal from `bible.md`: kid build, too-big yellow rain hat matching
Grandpa's boots, striped teal-and-cream t-shirt, rolled-up denim shorts, bare feet or tiny sandals, gap-toothed grin, big round
eyes, freckles, a short kid's fishing rod with a sandwich on the hook.

## Must survive every art style
- A yellow rain hat (sou'wester) a size too big: brim low over the brow, long at the back, but the eyes still show
- Horizontal teal-and-cream striped t-shirt
- Rolled-up denim shorts (lighter cuffs), little brown sandals, bare legs
- Gap-toothed grin, big round eyes, freckles
- Small: about six, the shortest Jarling on the dock (height 0.85, standard body)
- Prop (Life of a Worm): a short kid's fishing rod with a sandwich (not a lure, not a fish) on the hook

## Silhouette
A small kid under a big round rain hat whose brim flares out behind: hat, head, short striped body, short legs. The hat is the
biggest shape; next to Old Reel he comes up to about Grandpa's belly.

## Face
Big round eyes, freckles across the nose and cheeks, a gap-toothed grin. Expressions: neutral = gap-toothed grin; happy = big
open grin (the fist pump); surprised = round "o" (it was true!); determined = **the squint** (one eye shut, one narrowed, lips
pressed: weighing whether a grown-up is lying). "Nuh-uh" = the squint with arms crossed.

## Fixed colours
Checked against the player colours with CIEDE2000 (`tools/check_colours.py`, `avatar/kit/colour_rule.py`): every outfit main
colour is at least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`, skin and hair at least 10. The bible's teal `#2FA7A0`
is the tightest at 25.4 from P1 and passes, so **no adjustment was needed**: the bible's picks are kept as they are. Skin, hair,
cuffs, sandals and the rod colours are the character lane's picks (not fixed by the bible) and pass too.

| Part | Colour | ΔE00 vs P1 / P2 |
| --- | --- | --- |
| rain hat | `#F6C833` (Grandpa's boots) | 33.4 / 48.8 |
| t-shirt | `#2FA7A0` teal | 25.4 / 59.6 |
| t-shirt stripes | `#F1E7CF` cream (accent) | 30.4 / 43.5 |
| shorts | `#3D5A88` denim | 56.3 / 42.6 |
| shorts cuffs | `#5873A0` light denim (accent) | 50.4 / 40.7 |
| sandals | `#9A6A3C` | 43.9 / 23.7 |
| skin | `#F0B488` | 42.8 / 30.3 |
| hair | `#8A5A34` sandy brown | 48.7 / 22.9 |
| kid rod | `#6FA8DC` blue, cream reel `#F1E7CF` (gear) | 48.6 / 49.0 |
| sandwich | bread `#E8C48A`, crust `#C08A4E`, cheese `#F2C94C` (gear) | 32.4 / 39.1, -, 32.0 / 47.9 |

No green lettuce and nothing red in the sandwich, so it never reads as a player colour.

## Signature props
- The rain hat. Also head-slot gear `avatar/gear/rain_hat` for any Jarling.
- The kid's rod with a sandwich on the hook: hand gear `avatar/gear/kid_rod` (`hand_r`), Life of a Worm.

## Per-technique notes

### Jarling 3D
See "Jarling 3D (as built)" below.

### 2D pixel (The Hill / Life of a Worm)
See "Alt form: the-hill pixel" below.

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/bobber.py` (`bobber()`)

- **Height:** 31 px with the outline (0.85 m kid body, 22 rows to the top of the head, plus the oversized sou'wester, traced
  from `refs/jarling/bobber_side_sprite.png`): rain hat 7 rows (round dome crown 6 rows + 1 brim row much wider than the
  head, the back brim drooping 4 rows lower behind the neck), head 7 rows (sandy hair under the brim, big round dark eyes,
  freckles, gap-toothed grin), striped tee 7 rows, denim shorts 2 rows + a light cuff row, bare legs, little sandals 2 rows
  (strap over the foot, sole).
- **Palette:** hat `#F6C833` (+ `#C79F1E`, white shine `#F7F7F5`), hair and freckles `#8A5A34`, skin `#F0B488`
  (+ `#D0926A`), tee `#2FA7A0` (+ `#23807B`), stripes `#F1E7CF` (+ `#D3C7AA`), shorts `#3D5A88` (+ `#2E4670`), cuffs
  `#5873A0`, sandals `#9A6A3C` (+ `#7A5230`), teeth `#F7F7F5`, mouth `#6A2232`, outline `#2A1E2C`. Every pixel colour is at
  least ΔE00 22.9 from P2 `#e4393c` and 25.4 from P1 `#3cc24a` (the teal; its shade is darker, not greener).
- **Frames:** front form (40 x 32) and the 128 x 224 player sheet: idle0-1, walk0-3, jump, fall, side0-2, down0-2, ride, sleep0-1
  (three-quarter view facing right, feet on row 30, hand at (19, 21) idle). Life of a Worm cutscene: `sit_dock(0|1)`, 32 x 48,
  sitting on the dock edge facing right, seat line on row 24 (mid-height), dock edge at x 21 (seat point (21, 24)), knees bent
  over the edge, shins and sandals dangling below the seat, the feet swinging between the two frames
  (`refs/pixel/bobber_sit_dock.png`, both frames side by side). No rod in the pixel frames (the kid rod is 3D gear only).
- **Should read as:**
  - an oversized yellow sou'wester rain hat (not a helmet, a bowl or a straw hat): a round dome crown with a shine, one brim
    row clearly wider than the head on both sides, the back brim long and drooping down behind the neck; the biggest shape on
    the figure. Sandy brown hair peeks out under it at the back and as a fringe. No chin tie
  - big round dark eyes (with a white glint) under the brim, freckle pixels, a gap-toothed grin (white teeth with a 1 px gap);
    nothing at the mouth that could read as a pipe or cigarette
  - a teal t-shirt with cream stripes on alternate rows (striped sleeves too)
  - denim shorts with a lighter cuff row, bare legs, little brown sandals
  - a small kid: at 16 px the silhouette is a big hat on a short body
