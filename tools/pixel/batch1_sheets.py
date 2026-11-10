"""Batch 1 review sheets. Run from the repo root: python3 tools/pixel/batch1_sheets.py [lineup] [read]

lineup -> characters/batch1_pixel_lineup.png  Jeff, Chuck and the four batch-1 pixel forms on one ground line
read   -> characters/batch1_read_check.png    per character: the 3D side view, the pixel form at 1x and at The
          Hill's game scales (x2 in play today, x3 the design scale) on sky and dirt, the right-facing idle frame,
          a 16 px silhouette, and what each prop should read as
"""
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import residents as R
from px import up, silhouette, font, rgba

BG, INK, SOFT = "#F6EFE0", "#2A1E2C", "#6A5E6C"
SKY, DIRT = "#9FD3F7", "#8A5A3C"
BATCH = [("zorp", "Zorp"), ("coach_whistle", "Coach Whistle"), ("astro_ana", "Astro Ana"), ("ribbit", "Ribbit")]
READS = {   # the director's "should read as" line per prop
    "zorp": ["antennae: two stalks with yellow bobbles growing from the head (not a hat, horns or ears)",
             "headband: a thin silver band", "shirt: loud yellow-and-pink holiday shirt", "skin: light blue alien"],
    "coach_whistle": ["whistle: a referee's whistle hanging on a yellow cord at the chest (not a pipe, not a medal)",
                      "cap: navy baseball cap", "shirt: black-and-white referee stripes", "socks: tall white socks, short legs"],
    "astro_ana": ["helmet: a clear glass fishbowl (not a hood, a halo or hair)", "hair: two puffs inside the glass",
                  "stripe: orange chest stripe on a white suit", "boots: chunky orange moon boots"],
    "ribbit": ["hood: a frog hood with two big frog eyes on top (not ears, a bow or goggles)",
               "belly: yellow belly panel", "feet: bare-look yellow frog shoes", "mouth: wide flat pleased smile"],
}


def mod(cid): return importlib.import_module(cid)
def front(cid): return getattr(mod(cid), cid)()
def trim(im): return im.crop(im.getbbox())


def sil16(im):
    """The figure reduced to 16 px tall (nearest), as a flat silhouette."""
    f = trim(im); w = max(1, round(f.width * 16 / f.height))
    return silhouette(f.resize((w, 16), Image.NEAREST))


def lineup():
    sp = [("Jeff", R.jeff()), ("Chuck", R.chuck())] + [(n, front(c)) for c, n in BATCH]
    im = Image.new("RGBA", (1920, 900), rgba(BG)); d = ImageDraw.Draw(im)
    d.text((40, 14), "Batch 1 pixel forms (The Hill scale: 32 px = 1.2 m), with Jeff and Chuck", fill=INK, font=font(36))
    ground, x = 440, 60
    d.line((20, ground, 1900, ground), fill="#B9AD96", width=3)
    for n, s in sp:
        big = up(s, 8); im.alpha_composite(big, (x, ground - big.height + 1))
        d.text((x + 40, ground + 10), f"{n}, {trim(s).height} px", fill=INK, font=font(22)); x += big.width - 10
    d.text((40, 520), "real size x1, x2 (in play), x3 (design scale)", fill=SOFT, font=font(18))
    x = 40
    for k in (1, 2, 3):
        for n, s in sp:
            b = up(s, k); im.alpha_composite(b, (x, 720 - b.height)); x += b.width + 4
        x += 40
    d.text((40, 760), "silhouettes, 16 px tall, x4", fill=SOFT, font=font(18)); x = 40
    for n, s in sp:
        b = up(sil16(s), 4); im.alpha_composite(b, (x, 870 - b.height)); x += b.width + 40
    im.convert("RGB").save("characters/batch1_pixel_lineup.png")


def read_check():
    RH = 350
    im = Image.new("RGBA", (1920, 70 + RH * len(BATCH)), rgba(BG)); d = ImageDraw.Draw(im)
    d.text((40, 14), "Batch 1 read check: 3D side view > pixel form > game size > 16 px silhouette", fill=INK, font=font(34))
    for i, (cid, name) in enumerate(BATCH):
        y = 70 + i * RH
        d.line((20, y, 1900, y), fill="#B9AD96", width=2)
        d.text((40, y + 8), name, fill=INK, font=font(26))
        side = Image.open(f"characters/{cid}/refs/jarling/{cid}_side.png").convert("RGBA")
        side = trim(side); k = 280 / side.height
        side = side.resize((round(side.width * k), 280), Image.LANCZOS)
        im.alpha_composite(side, (40 + (260 - side.width) // 2, y + 50)); d.text((40, y + 332 - 18), "3D side view", fill=SOFT, font=font(15))
        f = front(cid); fr = mod(cid).sheet().crop((0, 0, 32, 32))
        big = up(f, 8); im.alpha_composite(big, (320, y + 60)); d.text((320, y + 332 - 18), "pixel form x8", fill=SOFT, font=font(15))
        big = up(fr, 8); im.alpha_composite(big, (640, y + 60)); d.text((640, y + 332 - 18), "idle frame (faces right) x8", fill=SOFT, font=font(15))
        for bi, (bgc, lab) in enumerate(((SKY, "on sky"), (DIRT, "on dirt"))):
            bx, by = 920, y + 50 + bi * 140
            d.rectangle((bx, by, bx + 420, by + 126), fill=bgc)
            x = bx + 10
            for k2 in (1, 2, 3):
                for s in (f, fr):
                    b = up(trim(s), k2); im.alpha_composite(b, (x, by + 116 - b.height)); x += b.width + 10
                x += 14
            d.text((bx + 4, by + 2), f"{lab}: x1, x2 (in play), x3", fill=INK if bi == 0 else "#FFFDF4", font=font(14))
        s16 = sil16(f); im.alpha_composite(s16, (1370, y + 110)); im.alpha_composite(up(s16, 4), (1400, y + 62))
        s16 = sil16(fr); im.alpha_composite(s16, (1370, y + 220)); im.alpha_composite(up(s16, 4), (1400, y + 172))
        d.text((1370, y + 332 - 18), "16 px silhouette x1, x4", fill=SOFT, font=font(15))
        d.text((1500, y + 50), "should read as", fill=SOFT, font=font(15))
        ty = y + 72
        for line in READS[cid]:
            words, cur = line.split(), ""
            for w in words:                       # wrap at about 44 characters
                if len(cur) + len(w) > 44:
                    d.text((1500, ty), cur, fill=INK, font=font(16)); ty += 20; cur = "   "
                cur += w + " "
            d.text((1500, ty), cur, fill=INK, font=font(16)); ty += 28
    im.convert("RGB").save("characters/batch1_read_check.png")


if __name__ == "__main__":
    todo = sys.argv[1:] or ["lineup", "read"]
    if "lineup" in todo: lineup()
    if "read" in todo: read_check()
