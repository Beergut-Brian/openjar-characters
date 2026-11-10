# Yoji — look

## Kaden's sheet (verbatim, 2026-11-10)
- Hair: "short hair", and a hat on top
- Hat: "a cowboy hat"
- Shirt: "football jersey", "number 55", team "The Champions"
- Pants: none, "just underwear on"
- Shoes: "black and blue" basketball shoes (ours are unbranded original high-tops, no logos)
- Face: yes

## Must survive every art style
- Tan cowboy hat: wide brim curled up at the sides, pinched crown, worn level on top of short brown hair
- Navy football jersey with shoulder pads, gold trim, a big white **55** front and back
- White boxer shorts with small navy stars and a waistband: clearly underwear, as a gag (never rude)
- Bare legs
- Black-and-blue high-top basketball shoes with white soles, no logos
- A huge happy grin

## Silhouette
A wide-brimmed hat on a big round head, broad padded shoulders over a stocky torso, a short puff of boxers, then bare legs down to chunky high-tops. Wide at the top (brim + pads), narrow in the middle (bare legs), chunky at the feet.

## Face
Big friendly grin, thick brows, round bright eyes. Expressions: neutral = grin; happy = arc eyes, open yell-grin (touchdown!); surprised = round "o"; determined = game face, brows down, set grin.

## Fixed colours
Checked against the player colours with CIEDE2000 (`avatar/kit/colour_rule.py`, `tools/check_colours.py`): every outfit main colour is at least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`, skin and hair at least 10. Lowest: hair `#6B4A2E` 27.7 from P2. No adjustment was needed; all values are the producer's starting picks from the sheet.

| Part | Colour | ΔE00 vs P1 / P2 |
| --- | --- | --- |
| cowboy hat | `#C8955A` | 38.0 / 29.3 |
| hat band | `#5A3A22` (accent) | 56.8 / 30.2 |
| hair | `#6B4A2E` | 51.1 / 27.7 |
| skin | `#E8B48A` | 40.2 / 30.9 |
| jersey | `#1F3A6B` navy | 65.2 / 45.7 |
| jersey trim | `#F2B632` gold (accent) | 36.8 / 42.8 |
| number 55, lettering | `#F7F7F5` (accent) | 33.4 / 44.2 |
| boxer shorts | `#F7F7F5` with stars `#1F3A6B` | 33.4 / 44.2 |
| high-tops | `#1A1A1E` black, panels `#2A6FD6` blue, soles + laces `#F7F7F5` | 61.0 / 43.8, 59.6 / 44.9 |

## Lettering
"55" (front and back) and "CHAMPIONS" (upper back) live only in the 3D jersey texture and the pixel art, never as gameplay UI text. The team name is "The Champions"; only "CHAMPIONS" fits on the back.

## Signature props
- The cowboy hat. Also available as head-slot gear `avatar/gear/cowboy_hat` for any Jarling.
