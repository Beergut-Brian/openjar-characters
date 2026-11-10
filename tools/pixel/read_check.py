#!/usr/bin/env python3
"""characters/read_check.png: does every prop read at game size? Run from the repo root:
    python3 tools/pixel/read_check.py

One row per library character: the 3D side view (refs/jarling/<id>_side.png, else the trace render
.scratch/trace/<id>_side.png), the pixel form at 1x, at The Hill's display scale (x2: 1920 x 1080
viewport, camera zoom 2, nearest filtering; x4 on a 4K TV), the prop poses at x2, a 16 px tall
silhouette, and what each prop should read as.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
import residents as R
from px import up, silhouette, font, rgba

GAME = 2
ROWS = [
    ("jeff", "Jeff", R.jeff, [], ["hard hat: a green builder's hard hat over the chicken hood",
                                  "comb: the raspberry comb poking up through the hat"]),
    ("chuck", "Chuck", R.chuck, [], ["hard hat: dark dome, red brim and ridge",
                                     "T-Rex hat: a small yellow T-Rex sticker on the front of the hard hat"]),
    ("mole", "Mole", R.mole, [("dig", lambda: R.mole("front", "dig"))],
     ["claws: big pink digging claws out at his sides (no shovel at rest)",
      "shovel: only when digging, held across him in both claws, steel blade down"]),
    ("gnome_foreman", "Gnome Foreman", R.foreman, [("whistle", lambda: R.foreman("front", "whistle"))],
     ["hard hat: a tiny white hard hat on the tip of the cone", "clipboard: a brown board with paper and lines",
      "whistle: a little yellow whistle hanging on his chest below the beard; raised only to blow it",
      "nothing near his mouth at rest (no pipe read)"]),
    ("caveman", "Caveman", R.caveman, [("wave", lambda: R.caveman("front", "wave"))],
     ["ice cube: a pale blue cube on his head with a white glint",
      "club: a cream polishing cloth tied with teal string on a wood stick"]),
    ("dragon", "Dragon", lambda: R.dragon("sit", "sleepy"), [("yawn", lambda: R.dragon("yawn"))],
     ["no props: a round purple mass, cream belly, peach tail puff", "smoke rings are a game effect (asleep pose)"]),
]


def side3d(cid):
    for p in (f"characters/{cid}/refs/jarling/{cid}_side.png", f".scratch/trace/{cid}_side.png"):
        if os.path.exists(os.path.join(ROOT, p)):
            return Image.open(os.path.join(ROOT, p)).convert("RGBA"), p
    return None, "missing"


def main():
    hs = [max(260, fn().height * GAME + 50) for _, _, fn, _, _ in ROWS]
    out = Image.new("RGBA", (1920, 90 + sum(hs) + 10 * len(hs)), rgba("#F6EFE0"))
    d = ImageDraw.Draw(out); f, sm = font(22), font(16)
    d.text((30, 14), "Read check: the 3D-first pixel forms at game size (The Hill shows sprites x2: 1920 x 1080, zoom 2)", fill="#2A1E2C", font=font(30))
    d.text((30, 54), "3D side view  |  pixel 1x  |  pixel x2 (game)  |  prop pose x2  |  16 px silhouette  |  should read as", fill="#6A5E6C", font=sm)
    y = 90
    for (cid, name, fn, extra, caps), h in zip(ROWS, hs):
        d.line((20, y - 4, 1900, y - 4), fill="#D8CDB6", width=2)
        d.text((30, y), name, fill="#2A1E2C", font=f)
        base = y + h - 30
        im, src = side3d(cid)
        x = 30
        if im:
            bb = im.getbbox(); im = im.crop(bb)
            k = min(170 / im.height, 200 / im.width); im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
            out.alpha_composite(im, (x, base - im.height))
        d.text((x, base + 6), os.path.basename(src), fill="#6A5E6C", font=font(12))
        x = 250
        sp = fn()
        out.alpha_composite(sp, (x, base - sp.height)); x += sp.width + 30
        big = up(sp, GAME); out.alpha_composite(big, (x, base - big.height)); x += big.width + 30
        for tag, efn in extra:
            e = up(efn(), GAME); out.alpha_composite(e, (x, base - e.height)); d.text((x, base + 6), tag, fill="#6A5E6C", font=sm)
            x += e.width + 30
        sil = silhouette(sp.crop(sp.getbbox()))
        sil = sil.resize((max(1, round(sil.width * 16 / sil.height)), 16), Image.NEAREST)
        out.alpha_composite(up(sil, 1), (x, base - 16)); x += sil.width + 40
        x = max(x, 1180)
        for i, c in enumerate(caps):
            d.text((x, y + 30 + i * 26), "- " + c, fill="#2A1E2C", font=font(17))
        y += h + 10
    out.convert("RGB").save(os.path.join(ROOT, "characters", "read_check.png"))
    print("wrote characters/read_check.png")


if __name__ == "__main__":
    main()
