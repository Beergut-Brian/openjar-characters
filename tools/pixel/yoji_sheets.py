"""Yoji's read check. Run from the repo root: python3 tools/pixel/yoji_sheets.py

-> characters/yoji_read_check.png  the 3D side view, the pixel form at 1x and at The Hill's game scales (x2 in play
   today, x3 the design scale) on sky and dirt, the right-facing idle frame, a 16 px silhouette, and what each part
   should read as (the read-check half of batch4_sheets.py, for one character)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from px import up, silhouette, font, rgba
import yoji as Y

BG, INK, SOFT = "#F6EFE0", "#2A1E2C", "#6A5E6C"
SKY, DIRT = "#9FD3F7", "#8A5A3C"
READS = [
    "cowboy hat: tan, a long flat brim, the widest thing, tips up 1 px; trapezoid crown with a 1 px pinch on top "
    "(not horns, bucket hat, sombrero or helmet); brown hair under it",
    "football jersey 55: navy, broad shoulder pads, gold stripes and hem, white 55 on the front",
    "boxer shorts: white with navy stars and a navy-gold waistband, then bare legs",
    "high-tops: black, blue collar above the ankle, white soles",
    "face: a big grin, teeth showing",
]


def trim(im): return im.crop(im.getbbox())


def sil16(im):
    """The figure reduced to 16 px tall (nearest), as a flat silhouette."""
    f = trim(im); w = max(1, round(f.width * 16 / f.height))
    return silhouette(f.resize((w, 16), Image.NEAREST))


def read_check():
    RH = 420
    im = Image.new("RGBA", (1920, 70 + RH), rgba(BG)); d = ImageDraw.Draw(im)
    d.text((40, 14), "Yoji read check: 3D side view > pixel form > game size > 16 px silhouette", fill=INK, font=font(34))
    y = 70
    d.line((20, y, 1900, y), fill="#B9AD96", width=2)
    d.text((40, y + 8), "Yoji", fill=INK, font=font(26))
    side = Image.open("characters/yoji/refs/jarling/yoji_side.png").convert("RGBA")
    side = trim(side); k = 280 / side.height
    side = side.resize((round(side.width * k), 280), Image.LANCZOS)
    im.alpha_composite(side, (40 + (260 - side.width) // 2, y + 50)); d.text((40, y + 332 - 18), "3D side view", fill=SOFT, font=font(15))
    f = Y.yoji(); fr = Y.sheet().crop((0, 0, 32, 32))
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
    d.text((1530, y + 50), "should read as", fill=SOFT, font=font(15))
    ty = y + 72
    for line in READS:
        words, cur = line.split(), ""
        for w in words:                       # wrap at about 40 characters
            if len(cur) + len(w) > 40:
                d.text((1530, ty), cur, fill=INK, font=font(16)); ty += 20; cur = "   "
            cur += w + " "
        d.text((1530, ty), cur, fill=INK, font=font(16)); ty += 28
    im.convert("RGB").save("characters/yoji_read_check.png")


if __name__ == "__main__":
    read_check()
