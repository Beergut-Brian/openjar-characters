# Patience the Cow: voice

## Direction
Moos only, never words. A low, warm, unhurried, contented voice: a big animal that is in no hurry.
Most moos are long and a little nasal at the start ("mmm-"), opening into a round "-ooo". She is
expressive only through length and pitch: long and falling is content, rising is curious, short is
surprised, and one high, wobbly moo is the only time she panics (ballooned).

In Junk Yard Zap the game pitch-shifts her with size (grow lowers it, shrink raises it), so record at
her normal size only. Mono, 0.4 to 3 seconds, normalised to -16 LUFS, file name = cue.

## Sample lines (test reads)
1. "Mmmmoooooo." (content, falling)
2. "Mm... mooo?" (curious, rising at the end)
3. "Mmmmmooooohhh..." (the long sigh, tipped on her side)
4. "MOO-oo-oo-oo!" (wobbly and high: ballooned)

## Chatterbox voice design
A synthetic voice designed from a text description: low, warm, slow, contented, mid-low pitch, a
gentle nasal hum before each vowel, relaxed and unhurried; vocalises cow moos only, no words. No real
person's voice, no voice clone, and no imitation of any known character or performer.

Post effect: a touch of low-pass and a little room reverb (a barn), nothing else.

## Stock barks (shared cue list)
Draft lines; record after Kaden approves. Each `voice/<cue>.ogg` gets a row in `CREDITS.md`.

| Cue | Sound | When it plays |
| --- | --- | --- |
| `join` | "Mmmoo." (short, friendly) | she appears / wanders in |
| `ready` | "Mm-moo." | idle acknowledgement |
| `win` | "Mmmooo!" (two-note, up then down) | the players finish something; her `cheer` hop |
| `lose` | "Mmmoooo..." (falling) | the players fail; she does not mind |
| `oops` | "Moo?" (short, rising) | something bumps her |
| `cheer` | "Moo! Moo!" | the hop |
| `wait` | a long chew, then "mmmm" | idle, nothing happening |
| `swap_in` | "Mmoo?" | a new player looks at her |

## Yard reactions (Junk Yard Zap, one per gun; the face from `bible.md`)
| Cue | Sound | Gun / event | Face |
| --- | --- | --- | --- |
| `grow` | slow, rising "mmmMOOO" | grow (pitch drops with size) | `wide_eyed`, then `neutral` |
| `shrink` | a tiny "moo?" | shrink (pitch rises with size) | `wide_eyed` |
| `grabbed` | "Moo?!" | gravity grab | `wide_eyed` |
| `thrown` | "Moooo-oo-oof" | thrown, lands | `dizzy` |
| `tipped` | "Mmmmoooohhh..." (the long sigh) | tipped onto her side | `dizzy` (action `tipped` / `stiff`) |
| `bouncy` | a pleased low "mm-hmm-moo" | bouncy | `smug` |
| `balloon` | "MOO-oo-oo-oo!" (high, wobbly) | balloon | `panicked` |
| `frozen` | a muffled "mmf-moo" | freeze | `neutral` (she keeps chewing) |
| `glued` | "Moo." (resigned) | glue | `neutral` |
| `magnet` | "Moo?" | magnet pulls things at her | `wide_eyed` |
| `splash` | "Blub... moo." | lands in the pond | `neutral` |
| `chew` | munching, no voice | idle loop | `neutral` |
