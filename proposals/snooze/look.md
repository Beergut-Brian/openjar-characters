# Snooze — look

## Kaden's sheet (verbatim)
Medium, slightly slouched. Long striped nightcap with a pom-pom that flops to one side, light blue pajamas with white stars, fuzzy yellow slippers. Eyes permanently closed in happy arcs.

## Must survive every art style
- Long striped nightcap with a pom-pom that flops to one side
- Light blue pajamas with white stars
- Fuzzy yellow slippers
- Medium, slightly slouched
- Eyes permanently closed in happy arcs

## Silhouette
Medium slouched body with a long cone nightcap flopping over to one side, pom-pom hanging at shoulder height. The droop is the outline.

## Face
Eyes always closed in happy arcs (never open). Expressions to build: content (closed arcs, small smile), yawn (mouth big `o`, eyes squeezed), snore (mouth slightly open).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- nightcap stripe A: `#6F7FD8`
- nightcap stripe B + pom: `#F5F5F2`
- pajamas: `#A9D4F2`
- pajama stars: `#FFFFFF` (accent)
- slippers: `#FFD95A`

## Signature props
- Nightcap (headwear: long cone, flops to one side, pom-pom tip, sway bones)
- No gear

## Per-technique notes

### Jarling 3D (master, built by the kit lane from this sheet)
Standard humanoid Jarling body (`avatar/kit`): only `build`, `height` (0.8-1.3) and `leg_scale` (0.8-1.2) change; same skeleton, actions, ten equipment slots and the same gameplay collision as every playable character.
- **build:** `regular`
- **height:** 1.0
- **leg_scale:** 0.95
- **width / belly:** regular, soft
- **head:** `round`, size 1.0
- **hair:** `short`, colour left to the kit lane
- **headwear:** **new** `nightcap` (long striped cone, floppy, pom-pom; sway bones)
- **top:** **new** `pajama_top` (button front), light blue with white star print
- **bottoms:** **new** `pajama_pants`, same print
- **shoes:** **new** `fuzzy_slippers`, yellow
- **posture:** slouch: spine lean about 8, head lean about -6
- **face:** eyes locked to closed arcs in every expression
- **gear:** none
- **pieces needed:** floppy nightcap, pajama top + pants with star print, fuzzy slippers, closed-eye face lock

### 2D pixel (The Hill)
32 px tall at Jeff's scale (stage 1), side-on like `characters/residents_lineup.png`; traced from the 3D side view once it exists. Nightcap stripes alternate periwinkle/white pixels and flop down one side; a white pom-pom pixel pair at shoulder height. Light blue pajamas with scattered white star pixels; yellow slippers.

## Refs
`refs/`: none yet. The kit lane builds the 3D master and renders after Kaden approves this sheet.
