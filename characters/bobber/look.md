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
