#!/usr/bin/env python3
"""Add a caption bar under a sheet render: label_sheet.py image.png "front" "3/4" "side" "back" """
import sys
from PIL import Image, ImageDraw, ImageFont

path, labels = sys.argv[1], sys.argv[2:]
im = Image.open(path).convert("RGB")
w, h = im.size
bar = 56
out = Image.new("RGB", (w, h + bar), (255, 255, 255))
out.paste(im, (0, 0))
d = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
except OSError:
    font = ImageFont.load_default()
for i, t in enumerate(labels):
    cx = (i + 0.5) * w / len(labels)
    tw = d.textlength(t, font=font)
    d.text((cx - tw / 2, h + 12), t, fill=(60, 70, 90), font=font)
out.save(path)
