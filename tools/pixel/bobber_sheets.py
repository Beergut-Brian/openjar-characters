"""Bobber's read check. Run from the repo root: python3 tools/pixel/bobber_sheets.py

-> characters/bobber_read_check.png  the 3D side view, the pixel form at 1x and at The Hill's game scales (x2 in play
   today, x3 the design scale) on sky and dirt, the right-facing idle frame, the two sit_dock frames (Life of a Worm) on a
   dock plank, a 16 px silhouette, and what each part should read as (copied from yoji_sheets.py)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from px import up, silhouette, font, rgba
import bobber as Y

BG, INK, SOFT = "#F6EFE0", "#2A1E2C", "#6A5E6C"
SKY, DIRT = "#9FD3F7", "#8A5A3C"
DOCK, DOCK_D = "#8C6A4A", "#6B4F36"
READS = [
    "should read as: oversized rain hat, striped t-shirt, shorts, kid with a fishing rod (the rod is 3D gear only: "
    "no rod in the pixel frames)",
    "rain hat: yellow sou'wester, round dome, brim wider than the head, long and drooping at the back, the biggest "
    "shape (not a helmet, bowl or straw hat); sandy hair under it",
    "striped tee: teal with cream stripes on alternate rows",
    "denim shorts with light cuffs, bare legs, little brown sandals",
    "face: big round dark eyes under the brim, freckles, gap-toothed grin; nothing at the mouth",
]


def trim(im): return im.crop(im.getbbox())


def sil16(im):
    """The figure reduced to 16 px tall (nearest), as a flat silhouette."""
    f = trim(im); w = max(1, round(f.width * 16 / f.height))
    return silhouette(f.resize((w, 16), Image.NEAREST))


def read_check():
    RH = 470
    im = Image.new("RGBA", (2240, 70 + RH), rgba(BG)); d = ImageDraw.Draw(im)
    d.text((40, 14), "Bobber read check: 3D side view > pixel form > game size > 16 px silhouette", fill=INK, font=font(34))
    y = 70
    d.line((20, y, 2220, y), fill="#B9AD96", width=2)
    d.text((40, y + 8), "Bobber", fill=INK, font=font(26))
    side = Image.open("characters/bobber/refs/jarling/bobber_side.png").convert("RGBA")
    side = trim(side); k = 280 / side.height
    side = side.resize((round(side.width * k), 280), Image.LANCZOS)
    im.alpha_composite(side, (40 + (260 - side.width) // 2, y + 50)); d.text((40, y + 332 - 18), "3D side view", fill=SOFT, font=font(15))
    f = Y.bobber(); fr = Y.sheet().crop((0, 0, 32, 32))
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
    sx = 1360
    for i in (0, 1):                          # sit_dock on a dock plank, x4 (seat line = the plank top)
        sd = up(Y.outline(Y.sit_dock(i)), 4); px0 = sx + i * 140
        d.rectangle((px0, y + 50 + 24 * 4, px0 + 21 * 4 + 3, y + 50 + 24 * 4 + 14), fill=DOCK)
        d.rectangle((px0, y + 50 + 24 * 4 + 15, px0 + 21 * 4 + 3, y + 50 + 24 * 4 + 18), fill=DOCK_D)
        im.alpha_composite(sd, (px0, y + 50))
    d.text((sx, y + 332 - 18), "sit_dock 0 and 1 x4 (Life of a Worm)", fill=SOFT, font=font(15))
    s16 = sil16(f); im.alpha_composite(s16, (1650, y + 110)); im.alpha_composite(up(s16, 4), (1680, y + 62))
    s16 = sil16(fr); im.alpha_composite(s16, (1650, y + 220)); im.alpha_composite(up(s16, 4), (1680, y + 172))
    d.text((1650, y + 332 - 18), "16 px x1, x4", fill=SOFT, font=font(15))
    d.text((1800, y + 50), "should read as", fill=SOFT, font=font(15))
    ty = y + 72
    for line in READS:
        words, cur = line.split(), ""
        for w in words:                       # wrap at about 40 characters
            if len(cur) + len(w) > 40:
                d.text((1800, ty), cur, fill=INK, font=font(16)); ty += 20; cur = "   "
            cur += w + " "
        d.text((1800, ty), cur, fill=INK, font=font(16)); ty += 28
    im.convert("RGB").save("characters/bobber_read_check.png")


if __name__ == "__main__":
    read_check()
