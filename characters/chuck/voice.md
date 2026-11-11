# Chuck — voice

## Direction (approved by Kaden, D37 a, 2026-11-11)
- Adult man, mid-40s feel, gruff mid-low voice, chest-forward. Confident, a bit too loud.
- Pace: fast and clipped; short sentences; counts and declares. Drops into a mumble when wrong ("...that was the wind").
- Texture: gravelly but friendly, a cartoon tough guy, never menacing. Grunts and huffs on effort.
- Never scary, never actually angry at a player. His outrage is at the ball, the wind, physics.
- Kid test: "the bossy funny one who's always wrong".

## Catchphrase
"Watch this!"

## Voice design (ElevenLabs v3, per the library voice pipeline, D50)
Spec: `audio-src/voices/v3-specs/chuck.json` on the producer's machine (description, performance script, catchphrase, master monologue). One design call, three takes; Kaden picks the take on Docket. No imitation of any real actor, wrestler or character.

Post effect: none.

## Stock barks (shared cue list)
File name = cue (`voice/<cue>.ogg`), each credited in `CREDITS.md`. Lines are taken from the approved bark list below and kept about plays, not a ball or a field, so they fit every game.

| Cue | Line |
| --- | --- |
| `join` | Chuck's here. Stand back. |
| `ready` | Let's do this. |
| `win` | YES. New record. Mine. |
| `lose` | Again. I wasn't ready. |
| `oops` | I meant to do that. |
| `cheer` | Go! GO! Keep GOING! |
| `wait` | *sighs* I'll be in the truck. |
| `swap_in` | Watch this. |

## Extra lines (approved list, D37; for game lanes, voiced later from the saved master)
| id | line / sound | when |
| --- | --- | --- |
| watch_this | "Watch this." | before his kick |
| stand_back | "Stand back, Jeff." | run-up starts |
| count | "One, two, three, f— seven!" | run-up (counting gone wrong) |
| hut | "HUP!" | kick |
| wind | "That one was the wind." | bad kick |
| meant_it | "I meant to do that." | falls / misses |
| ball_blame | "Bad ball. BAD ball." | ball goes nowhere |
| yell_ball | "Go! GO! Keep GOING!" | ball in flight |
| not_bad | "...not bad." | Jeff does well (grudging) |
| nod | "Mm. Yep." | his own good kick |
| fist_pump | "YES." | celebration |
| hat | "My hat!" | hat flies off |
| hat_back | "...and the hat's back." | hat lands on head |
| ugh | "Ugh." | bonked |
| stomp | (three boot stomps + huff) | idle |
| grunt | (effort grunt) | action |
| ready | "Let's do this." | round start |
| again | "Again. I wasn't ready." | restart |
| this_one | "This one. Obviously." | picks an upgrade |
| science | "It's science, Jeff." | upgrade appears |
| hi | "Chuck's here." | joins / drop-in |
| bye | "I'll be in the truck." | leaves |
| record | "New record. Mine." | best result so far |
| tiny | "...we don't talk about that one." | tiny kick |
| space | "SPACE! Told ya!" | reaches space tier |
| laugh_hold | (snort, trying not to laugh) | Jeff falls |
