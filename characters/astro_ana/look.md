# Astro Ana — look

## Kaden's sheet (verbatim)
Medium build. Clear fishbowl helmet so the face stays visible, hair in two puffs inside it, white suit-style top with an orange chest stripe, white pants, orange moon boots. Determined grin.

## Must survive every art style
- Clear fishbowl helmet so the face stays visible
- Hair in two puffs inside the helmet
- White suit-style top with an orange chest stripe
- White pants, orange moon boots
- Determined grin

## Silhouette
Medium body with a big clear sphere around the head (two hair puffs visible inside), chunky moon boots: a bubble on a white column on two blocks.

## Face
Determined grin, focused eyes, visible through the glass. Expressions to build: determined (grin, brows down), countdown focus (set mouth), liftoff joy (open mouth, eyes wide).

## Fixed colours
Checked against the player colours with CIEDE2000 (`docs/jarlings-19.md`): every value below is at
least ΔE00 20 from P1 green `#3cc24a` and P2 red `#e4393c`. Skin tone is not fixed by the sheet; the kit lane picks one and runs the same check.
- fishbowl glass (tint): `#D8EEF8`
- hair puffs: `#3B2A20`
- suit top: `#F2F4F6`
- chest stripe: `#F7941D` (accent)
- pants: `#F2F4F6`
- moon boots: `#F7941D`

## Signature props
- Fishbowl helmet: transparent; the face must stay fully readable (low-reflection glass, no tint over the face)

## Per-technique notes

### Jarling 3D (master, built)
Built on the standard humanoid Jarling body (`avatar/kit`) from `jarling.json`:
- **body:** `build` regular, `height` 1.0 (no leg_scale / width / belly change)
- **head:** `round`, size 1.0, round ears; skin `#BF8150`
- **face:** eyes `lash`, brows `arched` `#2A1A14`, mouth `grin_top`, brows slightly down (neutral = determined grin).
  Expressions: neutral = determined grin; happy = liftoff joy (open `grin`, eyes wide, brows up); surprised = `o`;
  determined = countdown focus (`set` mouth, brows down, lids lowered)
- **hair:** preset `puffs` `#3B2A20` (two round puffs at the upper sides, fully inside the bowl)
- **headwear:** `fishbowl`, tint `#D8EEF8`, alpha 0.14, collar `#F2F4F6`, `collar_accent` `#F7941D`. Kit change
  (`avatar/kit/pieces_headwear.py`, `fishbowl`): chunky lip torus at the neck (`collar_size`), optional orange
  band (`collar_accent`), a light-blue edge (`rim` `#8FC7E8`, `rim_alpha`, `rim_power`) that exists only in the
  Blender/Cycles renders (Layer Weight on a CYCLES output; the exported glTF material stays a plain alpha-blended
  tint: alphaMode BLEND, baseColorFactor alpha 0.14, roughness 0.03), and a bigger glint streak high on the upper left
  (`highlight_alpha`, `highlight_size`). In a game the bowl's edge comes from the engine's reflections; add a
  fresnel rim in the game's shader if it reads too faint there.
- **top:** `long` `#F2F4F6` with `hstripe` `#F7941D` across the chest; **bottoms:** `pants` `#F2F4F6`;
  **shoes:** `moon_boots` `#F7941D`, sole `#F2F4F6`
- **ref_action:** `kick` frame 17 (follow-through), expression determined

## Refs
- `refs/jarling/`: `astro_ana.glb`, `astro_ana_turnaround.png`, `astro_ana_expressions.png`, `astro_ana_kick.png`,
  `astro_ana_side.png`, `astro_ana_side_sprite.png` (Blender kit renders)
- `refs/pixel/`: `astro_ana_pixel.png`, `astro_ana_frames.png`, `astro_ana_frames.json`, `astro_ana_pixel_sheet.png`
- Colours: all Fixed colours used as listed; the pixel form adds the ring `#8FC7E8`, white `#FFFFFF` and shades
  `#9E6740` (skin), `#C9D1DA` (suit), `#D2741A` (boots).

## Alt form: the-hill pixel: proposed
Sprite source: `tools/pixel/astro_ana.py` (`astro_ana()`)

- **Height:** 30 px drawn, 32 px with the outline. Body below the collar at true scale (traced from
  `astro_ana_side_sprite.png`: boots + legs 9 px, torso 8 px); the 3D head + bowl would be 3 px taller than the
  frame, so the head is drawn 2 px shorter and the bowl's clearance above the hair is 1 px of glass.
- **Palette:** skin `#BF8150` (shade `#9E6740`), hair `#3B2A20`, suit `#F2F4F6` (shade `#C9D1DA`), orange
  `#F7941D` (shade `#D2741A`), glass `#D8EEF8`, ring `#8FC7E8`, white `#FFFFFF`, outline `#2A1E2C`.
- **Frames:** front form (40 x 32); 32 x 32 three-quarter frames facing right: idle0 idle1 walk0-3 jump fall
  side0-2 down0-2, plus ride and sleep from `jarling_frames.sheet`; hand at (22, 21).
- Should read as: a clear glass fishbowl space helmet (not a hood, not a halo, not a bubble of hair): an opaque
  pixel bowl, 1 px light-blue ring inside the outline, pale glass fill, white glint at the upper left, white collar
  row with an orange pixel at the neck.
- Should read as: two hair puffs inside the helmet (dark 3 px puffs at the upper sides, 1 px of glass between puff and ring).
- Should read as: orange moon boots (3 px orange with a white sole row).
- Should read as: a white suit with an orange chest stripe (1 px row); a determined grin (corners up, white teeth).
