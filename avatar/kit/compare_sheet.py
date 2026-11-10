#!/usr/bin/env python3
"""characters/residents_3d_compare.png: each Hill resident's 3D master (front, idle) beside its approved
2D sprite. Run from the repo root after `render_residents.py --only fronts`:  python3 avatar/kit/compare_sheet.py
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "pixel"))
from PIL import Image, ImageDraw, ImageFont
import residents as R

CAST = [("mole", "The Mole", R.mole), ("gnome_foreman", "The Gnome Foreman", R.foreman),
        ("caveman", "The Caveman", R.caveman), ("dragon", "The Dragon", R.dragon)]
BG, INK, SUB = (246, 239, 224, 255), (42, 30, 44, 255), (110, 100, 96, 255)
PW, PH, BOX = 960, 540, 400      # panel size, picture box
def font(n):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", n)
    except OSError:
        return ImageFont.load_default(size=n)

def fit(im, box, nearest=False):
    im = im.crop(im.getbbox())
    if nearest:
        k = max(1, min(box // im.width, box // im.height))
        return im.resize((im.width * k, im.height * k), Image.NEAREST)
    k = min(box / im.width, box / im.height)
    return im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)

out = Image.new("RGBA", (PW * 2, PH * 2 + 70), BG)
d = ImageDraw.Draw(out)
d.text((40, 16), "The Hill residents: 3D master (proposed) beside the approved 2D sprite", fill=INK, font=font(34))
for i, (cid, title, fn) in enumerate(CAST):
    x0, y0 = (i % 2) * PW, 70 + (i // 2) * PH
    d.text((x0 + 40, y0 + 8), title, fill=INK, font=font(26))
    base = y0 + 60 + BOX
    pics = [(fit(Image.open(os.path.join(ROOT, ".scratch", "fronts", f"{cid}.png")).convert("RGBA"), BOX), "3D master (Jarling kit)"),
            (fit(fn().convert("RGBA"), BOX, nearest=True), "2D sprite (approved, The Hill)")]
    for k, (pic, cap) in enumerate(pics):
        cx = x0 + 40 + BOX // 2 + k * (BOX + 60)
        out.alpha_composite(pic, (cx - pic.width // 2, base - pic.height))
        d.text((cx - d.textlength(cap, font=font(18)) / 2, base + 12), cap, fill=SUB, font=font(18))
    d.line([(x0 + 30, base + 2), (x0 + PW - 30, base + 2)], fill=(190, 178, 160, 255), width=2)
out.convert("RGB").save(os.path.join(ROOT, "characters", "residents_3d_compare.png"))
print("wrote characters/residents_3d_compare.png")
