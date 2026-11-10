# The 19 new Jarlings (Kaden's sheets, 2026-11-10)

Status: **proposed**. Text drafts in `proposals/<id>/` (README "Proposals"). Batch 2 (2026-11-10): the three Junk Yard Zap
Jarlings (`professor_fizz`, `scrap`, `big_tiny`) and the four Hill ones (`foreman_dot`, `granny_gravel`, `mayor_pip`, `lampy`) are
built and live in `characters/<id>/` as a playtest build (`Playable: true`, Status still proposed).
Kaden's Look, Personality, Voice and sample lines are kept verbatim in each `look.md`, `bible.md`,
`voice.md`. All are `kind: universal`, `Body: standard`, planned playable (header says
`Playable: false` until each is complete and Kaden approves, per `docs/roster.md` step 5).

Standard body only: `build` in slim/regular/stocky/round/boxy/puffy, `height` 0.8-1.3, `leg_scale`
0.8-1.2, head shape from the kit's `HEAD_SHAPES`. Same gameplay collision for all.

## Roster table

Palette swatches are the main colours (skin when fixed, hair, headwear, top, bottoms, shoes); each
`look.md` lists accents too.

| id | Name | Home game | Body (build, height, legs, head) | Key pieces | Main palette |
| --- | --- | --- | --- | --- | --- |
| `foreman_dot` | Foreman Dot | The Hill / Hillville | stocky, h 0.85, legs 0.85, head round, size 1.0 | hard_hat (low fit), hivis_stripe, chunky boots, clipboard | `#F5C518` `#F28A1E` `#1F2D4F` `#7A4E2A` |
| `granny_gravel` | Granny Gravel | The Hill / Hillville | regular, h 0.9, legs 0.85, head round, size 1.0 | goggles (up/down), cardigan top, long_skirt, sneakers | `#F2F0EA` `#B9A3D9` `#8C8F96` `#FFD93B` |
| `mayor_pip` | Mayor Pip | The Hill / Hillville | slim, h 0.8, legs 0.8, head round, size 1.0 | top_hat (tall), sash, dress_shoes, collared shirt, ribbon scissors (gear) | `#1C1C22` `#A8CFF0` `#7D8088` `#15151A` |
| `lampy` | Lampy | The Hill / Hillville | slim, h 1.25, legs 1.15, head round, size 1.0 | miner_helmet + headlamp light, overalls_top, cheek smudge decal, rock (gear) | `#F1F1EC` `#3F8A99` `#7A5536` `#7B7F86` |
| `professor_fizz` | Professor Fizz | Junk Yard Zap | regular, h 1.0, legs 1.0, head round, size 1.0 | upright hair, goggles (shared), lab_coat, dress_shoes (shared), mismatched socks, scorch-brow decal | `#F7F7F2` `#F4F5F2` `#5E2F94` `#1B1B20` |
| `scrap` | Scrap | Junk Yard Zap | regular, h 0.85, legs 0.85, head round, size 1.05 | colander, shirt patches, shorts, sneakers with per-foot colour, freckles decal, gap-tooth grin | `#B9BEC4` `#F2C230` `#3E6DB5` `#F28C28` `#8A4FC4` |
| `big_tiny` | Big Tiny | Junk Yard Zap | round, h 1.3, legs 1.0, head round, size 1.0 | beanie scale option, sneakers oversize, round build at height 1.3 | `#2E3A66` `#7EC8F2` `#80848C` `#F7F7F5` |
| `coach_whistle` | Coach Whistle | Spaceballs | stocky, h 0.95, legs 0.8, head round, size 1.0 | vertical stripe pattern, shorts, sneakers, tall socks, whistle + cord | `#1E2B4D` `#1A1A1E` `#F5F5F2` `#8A8E96` `#F7F7F5` |
| `zorp` | Zorp | Spaceballs | slim, h 1.05, legs 1.0, head tall, size 1.05 | antennae (on headband), vacation shirt print, shorts, sandals, tall head shape | `#9FD6F0` `#C9CED4` `#FFD23F` `#FF7EB9` `#F5F5F2` `#C89A63` |
| `ribbit` | Ribbit | Spaceballs | round, h 0.85, legs 0.85, head round, size 1.05 | frog_hood with eyes, hoodie top, belly panel, shorts, bare-look shoes, hop gait layer | `#2A9DB0` `#F6D44A` `#22336B` |
| `astro_ana` | Astro Ana | Spaceballs | regular, h 1.0, legs 1.0, head round, size 1.0 | fishbowl helmet (transparent), two-puffs hair, spacesuit top + stripe, moon boots | `#D8EEF8` `#3B2A20` `#F2F4F6` `#F7941D` |
| `old_reel` | Old Reel | Life of a Worm | round, h 1.2, legs 1.05, head round, size 1.0 | bucket hat + lure, vest overlay, bushy brows, tall rain boots, fishing rod (gear) | `#C8A97A` `#A89B6E` `#F1E7CF` `#6E4B30` `#F6C833` |
| `bloom` | Bloom | Life of a Worm | puffy, h 0.85, legs 0.85, head round, size 1.0 | floppy sun hat + flower, knee skirt, mud-knee decals, clogs, watering can (gear) | `#E3C27A` `#F7A8CB` `#5B7FB8` `#8A4FC4` |
| `sir_clank` | Sir Clank | any (universal silly) | regular, h 1.05, legs 1.0, head round, size 1.0 | pot helmet, shield emblem, spoon sword (gear) | `#B8BEC6` `#8A8F98` `#23305E` `#7A4E2A` |
| `rexy` | Rexy | any (universal silly) | round, h 0.8, legs 0.8, head round, size 1.05 | dino hood + teeth, onesie, footies, back spikes, short tail | `#F7941D` |
| `boxbot` | Boxbot | any (universal silly) | boxy, h 0.9, legs 0.9, head soft_square, size 1.0 | head box with cut-out, torso box with drawn dials, ribbed hose sleeves | `#C49A6C` `#C0C4CA` `#80848C` `#3B6FD1` |
| `el_burrito` | El Burrito | any (universal silly) | stocky, h 0.85, legs 0.85, head round, size 1.0 | full-head mask, star emblem, cape, shorts, tall wrestling boots | `#E0B12E` `#6B2FA8` `#F5F5F2` |
| `snooze` | Snooze | any (universal silly) | regular, h 1.0, legs 0.95, head round, size 1.0 | floppy nightcap, pajama top + pants with star print, fuzzy slippers, closed-eye face lock | `#6F7FD8` `#F5F5F2` `#A9D4F2` `#FFD95A` |
| `captain_crumbs` | Captain Crumbs | any (universal silly) | round, h 1.2, legs 1.0, head round, size 1.0 | chef hat + badge, eyepatch, curly moustache, chef jacket, striped pants, flour decal/particle | `#F7F7F2` `#1F2D55` `#18181C` `#4A3324` |

## Pieces the kit must provide (union)

"New" means not in `avatar/kit/jarling_kit.py` today (it has headwear `cap`, `beanie`, `headband`,
`trucker`, `chicken_hood`; shoes `boots`, `barefoot`; hair `short`, `bun`, `buzz`, `bob`, `spiky`,
...). Names are suggestions for the kit lane; shared pieces are listed once.

| Piece | Used by |
| --- | --- |
| antennae | `zorp` |
| back spikes | `rexy` |
| bare-look shoes | `ribbit` |
| beanie scale option | `big_tiny` |
| belly panel | `ribbit` |
| bucket hat | `old_reel` |
| bushy brows | `old_reel` |
| cape | `el_burrito` |
| cardigan top | `granny_gravel` |
| cheek smudge decal | `lampy` |
| chef hat | `captain_crumbs` |
| chef jacket | `captain_crumbs` |
| chunky boots | `foreman_dot` |
| clipboard | `foreman_dot` |
| clogs | `bloom` |
| closed-eye face lock | `snooze` |
| colander | `scrap` |
| collared shirt | `mayor_pip` |
| curly moustache | `captain_crumbs` |
| dino hood | `rexy` |
| dress shoes | `mayor_pip`, `professor_fizz` |
| eyepatch | `captain_crumbs` |
| fishbowl helmet | `astro_ana` |
| fishing rod | `old_reel` |
| floppy nightcap | `snooze` |
| floppy sun hat | `bloom` |
| flour decal/particle | `captain_crumbs` |
| footies | `rexy` |
| freckles decal | `scrap` |
| frog hood | `ribbit` |
| full-head mask | `el_burrito` |
| fuzzy slippers | `snooze` |
| gap-tooth grin | `scrap` |
| goggles | `granny_gravel`, `professor_fizz` |
| hard hat | `foreman_dot` |
| head box | `boxbot` |
| hivis stripe | `foreman_dot` |
| hoodie top | `ribbit` |
| hop gait layer | `ribbit` |
| lab coat | `professor_fizz` |
| miner helmet | `lampy` |
| mismatched socks | `professor_fizz` |
| moon boots | `astro_ana` |
| mud-knee decals | `bloom` |
| onesie | `rexy` |
| overalls top | `lampy` |
| pajama top + pants | `snooze` |
| pot helmet | `sir_clank` |
| ribbed hose sleeves | `boxbot` |
| ribbon scissors | `mayor_pip` |
| rock | `lampy` |
| sandals | `zorp` |
| sash | `mayor_pip` |
| scorch-brow decal | `professor_fizz` |
| shield emblem | `sir_clank` |
| shirt patches | `scrap` |
| short tail | `rexy` |
| shorts | `scrap`, `coach_whistle`, `zorp`, `ribbit`, `el_burrito` |
| skirt (knee) | `bloom` |
| skirt (long) | `granny_gravel` |
| sneakers | `granny_gravel`, `scrap`, `coach_whistle`, `boxbot` |
| sneakers (oversize flag) | `big_tiny` |
| spacesuit top | `astro_ana` |
| spoon sword | `sir_clank` |
| star emblem | `el_burrito` |
| tall rain boots | `old_reel` |
| tall socks | `coach_whistle` |
| tall wrestling boots | `el_burrito` |
| top hat | `mayor_pip` |
| torso box | `boxbot` |
| two-puffs hair | `astro_ana` |
| upright hair | `professor_fizz` |
| vacation shirt print | `zorp` |
| vertical stripes | `coach_whistle`, `captain_crumbs` |
| vest overlay | `old_reel` |
| watering can | `bloom` |
| whistle | `coach_whistle` |

Also needed across the set: per-foot shoe colour (Scrap), a headwear `scale` option (Big Tiny's tiny
beanie), a `sit_low` headwear offset (Foreman Dot), transparent headwear with a rim-only fallback
(Astro Ana), a cosmetic `hop` gait layer on `run` (Ribbit), closed-eye lock for every expression
(Snooze), sway/jiggle bones for floppy hats, antennae, nightcap and cape, an emissive headlamp with
an optional spot light (Lampy), and a flour-puff particle (Captain Crumbs).

## Colour check (CIEDE2000 against the player colours)

Script: `.scratch/colour_check.py` (sRGB D65 to CIELAB, CIEDE2000, checked against Sharma et al.
test pairs). Threshold: every colour, main or accent, at least ΔE00 20 from P1 green `#3cc24a` and
P2 red `#e4393c` (CLAUDE.md: new playable characters use neither at all). Skin tones are not fixed
by the sheets except Zorp's; the kit lane runs the same check on its picks.

| id | role | hex | main | ΔE00 vs P1 #3cc24a | ΔE00 vs P2 #e4393c | ok |
| --- | --- | --- | --- | --- | --- | --- |
| foreman_dot | hard hat | `#F5C518` | yes | 33.9 | 49.2 | yes |
| foreman_dot | shirt | `#F28A1E` | yes | 50.8 | 28.1 | yes |
| foreman_dot | hi-vis stripe | `#F4F4F0` | accent | 32.7 | 44.1 | yes |
| foreman_dot | pants | `#1F2D4F` | yes | 64.9 | 45.6 | yes |
| foreman_dot | boots | `#7A4E2A` | yes | 51.5 | 25.3 | yes |
| granny_gravel | hair (bun) | `#F2F0EA` | yes | 32.3 | 43.4 | yes |
| granny_gravel | goggle frame | `#6E7681` | accent | 38.9 | 33.4 | yes |
| granny_gravel | goggle lens | `#A9D6E5` | accent | 36.6 | 54.9 | yes |
| granny_gravel | cardigan top | `#B9A3D9` | yes | 46.1 | 36.7 | yes |
| granny_gravel | skirt | `#8C8F96` | yes | 33.3 | 31.4 | yes |
| granny_gravel | sneakers | `#FFD93B` | yes | 32.3 | 53.0 | yes |
| mayor_pip | top hat | `#1C1C22` | yes | 61.2 | 43.7 | yes |
| mayor_pip | hat band | `#D4A82A` | accent | 32.5 | 42.7 | yes |
| mayor_pip | shirt | `#A8CFF0` | yes | 43.7 | 50.5 | yes |
| mayor_pip | sash | `#D4A82A` | accent | 32.5 | 42.7 | yes |
| mayor_pip | pants | `#7D8088` | yes | 35.5 | 30.8 | yes |
| mayor_pip | shoes | `#15151A` | yes | 62.4 | 45.1 | yes |
| lampy | miner's helmet | `#F1F1EC` | yes | 32.1 | 43.9 | yes |
| lampy | headlamp lens | `#FFE9A8` | accent | 30.2 | 48.1 | yes |
| lampy | overalls top | `#3F8A99` | yes | 37.7 | 58.1 | yes |
| lampy | pants | `#7A5536` | yes | 48.0 | 25.4 | yes |
| lampy | cheek smudge | `#6B5A4A` | accent | 42.7 | 28.1 | yes |
| lampy | boots | `#7B7F86` | yes | 35.3 | 31.1 | yes |
| professor_fizz | hair | `#F7F7F2` | yes | 32.8 | 44.8 | yes |
| professor_fizz | goggle rims | `#B8862E` | accent | 37.3 | 32.8 | yes |
| professor_fizz | goggle lens | `#9FD3E6` | accent | 38.1 | 56.3 | yes |
| professor_fizz | lab coat | `#F4F5F2` | yes | 32.8 | 44.4 | yes |
| professor_fizz | collar | `#7B3FB5` | accent | 61.8 | 38.1 | yes |
| professor_fizz | pants | `#5E2F94` | yes | 66.3 | 40.4 | yes |
| professor_fizz | sock L | `#FFB627` | accent | 40.2 | 41.9 | yes |
| professor_fizz | sock R | `#3FA7D6` | accent | 47.6 | 57.2 | yes |
| professor_fizz | shoes | `#1B1B20` | yes | 61.1 | 43.8 | yes |
| professor_fizz | scorch brow | `#3A2E2A` | accent | 57.9 | 35.8 | yes |
| scrap | colander helmet | `#B9BEC4` | yes | 32.1 | 37.6 | yes |
| scrap | shirt | `#F2C230` | yes | 33.7 | 47.4 | yes |
| scrap | patch tan | `#D9B38C` | accent | 35.1 | 32.4 | yes |
| scrap | patch blue | `#5A8FD0` | accent | 52.0 | 45.6 | yes |
| scrap | shorts | `#3E6DB5` | yes | 56.6 | 43.8 | yes |
| scrap | shoe L | `#F28C28` | yes | 50.5 | 27.9 | yes |
| scrap | shoe R | `#8A4FC4` | yes | 58.9 | 36.8 | yes |
| scrap | freckles | `#C8936A` | accent | 41.3 | 24.9 | yes |
| big_tiny | beanie | `#2E3A66` | yes | 63.6 | 43.5 | yes |
| big_tiny | shirt | `#7EC8F2` | yes | 46.0 | 56.8 | yes |
| big_tiny | pants | `#80848C` | yes | 35.0 | 31.4 | yes |
| big_tiny | sneakers | `#F7F7F5` | yes | 33.4 | 44.2 | yes |
| big_tiny | sneaker sole | `#D0D3D8` | accent | 32.8 | 39.9 | yes |
| coach_whistle | cap | `#1E2B4D` | yes | 65.3 | 45.7 | yes |
| coach_whistle | shirt stripe black | `#1A1A1E` | yes | 61.0 | 43.8 | yes |
| coach_whistle | shirt stripe white | `#F5F5F2` | yes | 33.0 | 44.1 | yes |
| coach_whistle | whistle | `#C9CED4` | accent | 33.0 | 39.9 | yes |
| coach_whistle | cord | `#F2C230` | accent | 33.7 | 47.4 | yes |
| coach_whistle | shorts | `#8A8E96` | yes | 33.9 | 31.9 | yes |
| coach_whistle | sneakers + socks | `#F7F7F5` | yes | 33.4 | 44.2 | yes |
| coach_whistle | sock band | `#1E2B4D` | accent | 65.3 | 45.7 | yes |
| zorp | skin + antennae | `#9FD6F0` | yes | 41.2 | 56.4 | yes |
| zorp | antenna bobbles | `#FFD23F` | accent | 33.5 | 50.3 | yes |
| zorp | headband | `#C9CED4` | yes | 33.0 | 39.9 | yes |
| zorp | shirt yellow | `#FFD23F` | yes | 33.5 | 50.3 | yes |
| zorp | shirt pink | `#FF7EB9` | yes | 79.5 | 26.4 | yes |
| zorp | shorts | `#F5F5F2` | yes | 33.0 | 44.1 | yes |
| zorp | sandals | `#C89A63` | yes | 36.4 | 30.2 | yes |
| ribbit | frog hoodie | `#2A9DB0` | yes | 37.2 | 65.7 | yes |
| ribbit | hood eyes | `#F5F5F2` | accent | 33.0 | 44.1 | yes |
| ribbit | hood pupils | `#15151A` | accent | 62.4 | 45.1 | yes |
| ribbit | belly panel | `#F6D44A` | yes | 30.8 | 51.6 | yes |
| ribbit | shorts | `#22336B` | yes | 66.9 | 45.5 | yes |
| ribbit | shoes | `#F6D44A` | yes | 30.8 | 51.6 | yes |
| astro_ana | fishbowl glass (tint) | `#D8EEF8` | yes | 36.9 | 50.1 | yes |
| astro_ana | hair puffs | `#3B2A20` | yes | 58.9 | 35.8 | yes |
| astro_ana | suit top | `#F2F4F6` | yes | 34.4 | 44.1 | yes |
| astro_ana | chest stripe | `#F7941D` | accent | 48.5 | 31.3 | yes |
| astro_ana | pants | `#F2F4F6` | yes | 34.4 | 44.1 | yes |
| astro_ana | moon boots | `#F7941D` | yes | 48.5 | 31.3 | yes |
| old_reel | bucket hat | `#C8A97A` | yes | 31.1 | 34.0 | yes |
| old_reel | lure blue | `#3F8FD8` | accent | 54.0 | 48.2 | yes |
| old_reel | lure yellow | `#F2C230` | accent | 33.7 | 47.4 | yes |
| old_reel | eyebrows | `#F2F0EA` | accent | 32.3 | 43.4 | yes |
| old_reel | vest | `#A89B6E` | yes | 25.1 | 37.1 | yes |
| old_reel | shirt | `#F1E7CF` | yes | 30.4 | 43.5 | yes |
| old_reel | pants | `#6E4B30` | yes | 51.4 | 26.7 | yes |
| old_reel | rain boots | `#F6C833` | yes | 33.4 | 48.8 | yes |
| bloom | straw sun hat | `#E3C27A` | yes | 30.3 | 41.8 | yes |
| bloom | flower petals | `#8E9BF0` | accent | 52.6 | 42.5 | yes |
| bloom | flower centre | `#FFD23F` | accent | 33.5 | 50.3 | yes |
| bloom | shirt | `#F7A8CB` | yes | 67.9 | 30.7 | yes |
| bloom | skirt | `#5B7FB8` | yes | 51.4 | 42.5 | yes |
| bloom | mud | `#6B4A33` | accent | 51.9 | 26.7 | yes |
| bloom | clogs | `#8A4FC4` | yes | 58.9 | 36.8 | yes |
| bloom | cheeks | `#F4A3B4` | accent | 63.9 | 26.4 | yes |
| sir_clank | pot helmet | `#B8BEC6` | yes | 33.1 | 38.2 | yes |
| sir_clank | pot handle | `#3A3D44` | accent | 54.1 | 38.1 | yes |
| sir_clank | shirt | `#8A8F98` | yes | 34.3 | 32.5 | yes |
| sir_clank | shield | `#F2C230` | accent | 33.7 | 47.4 | yes |
| sir_clank | pants | `#23305E` | yes | 66.1 | 45.2 | yes |
| sir_clank | boots | `#7A4E2A` | yes | 51.5 | 25.3 | yes |
| rexy | dino onesie | `#F7941D` | yes | 48.5 | 31.3 | yes |
| rexy | felt teeth | `#F7F7F2` | accent | 32.8 | 44.8 | yes |
| rexy | back spikes | `#FFD23F` | accent | 33.5 | 50.3 | yes |
| rexy | footies | `#F7941D` | yes | 48.5 | 31.3 | yes |
| boxbot | cardboard box | `#C49A6C` | yes | 36.0 | 29.2 | yes |
| boxbot | marker lines | `#2A2A30` | accent | 58.0 | 40.7 | yes |
| boxbot | button blue | `#3B6FD1` | accent | 58.8 | 44.0 | yes |
| boxbot | button yellow | `#F2C230` | accent | 33.7 | 47.4 | yes |
| boxbot | dryer-hose arms | `#C0C4CA` | yes | 32.4 | 38.1 | yes |
| boxbot | pants | `#80848C` | yes | 35.0 | 31.4 | yes |
| boxbot | shoes | `#3B6FD1` | yes | 58.8 | 44.0 | yes |
| el_burrito | mask | `#E0B12E` | yes | 33.2 | 43.9 | yes |
| el_burrito | mask trim + star | `#6B2FA8` | accent | 65.5 | 40.0 | yes |
| el_burrito | cape | `#6B2FA8` | yes | 65.5 | 40.0 | yes |
| el_burrito | shirt | `#E0B12E` | yes | 33.2 | 43.9 | yes |
| el_burrito | shorts | `#6B2FA8` | yes | 65.5 | 40.0 | yes |
| el_burrito | boots | `#F5F5F2` | yes | 33.0 | 44.1 | yes |
| snooze | nightcap stripe A | `#6F7FD8` | yes | 54.8 | 41.1 | yes |
| snooze | nightcap stripe B + pom | `#F5F5F2` | yes | 33.0 | 44.1 | yes |
| snooze | pajamas | `#A9D4F2` | yes | 42.9 | 52.3 | yes |
| snooze | pajama stars | `#FFFFFF` | accent | 34.7 | 45.0 | yes |
| snooze | slippers | `#FFD95A` | yes | 32.1 | 50.7 | yes |
| captain_crumbs | chef hat | `#F7F7F2` | yes | 32.8 | 44.8 | yes |
| captain_crumbs | badge | `#1F2D55` | accent | 65.9 | 45.7 | yes |
| captain_crumbs | eyepatch | `#18181C` | accent | 61.4 | 44.3 | yes |
| captain_crumbs | chef jacket | `#F7F7F2` | yes | 32.8 | 44.8 | yes |
| captain_crumbs | buttons | `#1F2D55` | accent | 65.9 | 45.7 | yes |
| captain_crumbs | pants stripe navy | `#1F2D55` | yes | 65.9 | 45.7 | yes |
| captain_crumbs | pants stripe white | `#F7F7F2` | yes | 32.8 | 44.8 | yes |
| captain_crumbs | boots | `#18181C` | yes | 61.4 | 44.3 | yes |
| captain_crumbs | moustache | `#4A3324` | yes | 57.6 | 32.9 | yes |
