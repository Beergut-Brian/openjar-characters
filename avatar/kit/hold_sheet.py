#!/usr/bin/env python3
"""Lay out the hold sheet from .scratch/hold/<cell>_<view>.png (render_hold.py) -> avatar/kit/renders/hold_check.png."""
import os, re, ast
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(ROOT, "avatar", "kit", "render_hold.py")).read()
CELLS = ast.literal_eval(re.search(r"CELLS = (\{.*?\n\})", src, re.S).group(1))
def font(n):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", n)
    except OSError:
        return ImageFont.load_default(size=n)
S, PER, PAD, CAP = 360, 3, 24, 44
rows = -(-len(CELLS) // PER)
W = PER * (2 * S + PAD) + PAD
out = Image.new("RGB", (W, 80 + rows * (S + CAP + PAD)), (246, 239, 224))
d = ImageDraw.Draw(out)
d.text((PAD, 18), "Hold check: every fist closed on its grip (front and 3/4)", fill=(42, 30, 44), font=font(34))
for i, (cid, spec) in enumerate(CELLS.items()):
    x0, y0 = PAD + (i % PER) * (2 * S + PAD), 80 + (i // PER) * (S + CAP + PAD)
    for k, view in enumerate(("front", "34")):
        p = os.path.join(ROOT, ".scratch", "hold", f"{cid}_{view}.png")
        if os.path.exists(p):
            out.paste(Image.open(p).convert("RGB").resize((S, S), Image.LANCZOS), (x0 + k * S, y0))
    d.text((x0 + 4, y0 + S + 8), spec[5], fill=(42, 30, 44), font=font(19))
os.makedirs(os.path.join(ROOT, "avatar", "kit", "renders"), exist_ok=True)
out.save(os.path.join(ROOT, "avatar", "kit", "renders", "hold_check.png"))
print("wrote avatar/kit/renders/hold_check.png")
