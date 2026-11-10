#!/usr/bin/env python3
"""The Hill's sprite scale from a side render: sprite_side.py characters/mole/refs/jarling/mole_side.png

`<id>_side.png` (render_refs.py --only side) is 512 px per 1.2 m (Jeff with his comb). The Hill draws
Jeff 32 px tall (16 px tiles), so the sprite scale is 1/16. Writes `<id>_side_sprite.png`:
left, the render on a 16 px tile grid (x8, smooth); right, the same reduced to real sprite pixels
(x8, nearest), feet on the ground line. This is the tracing base for the 2D sprite, not the sprite.
"""
import sys
from PIL import Image, ImageDraw

SRC_PER_JARLING, SPRITE_PER_JARLING, ZOOM, TILE = 512, 32, 8, 16
for path in sys.argv[1:]:
    im = Image.open(path).convert("RGBA")
    f = SRC_PER_JARLING // SPRITE_PER_JARLING                     # 16
    pad = round(0.04 * SRC_PER_JARLING)                            # render_refs leaves this under the feet
    im = im.crop((0, 0, im.width, im.height - pad))                # feet on the bottom edge
    w = -(-im.width // (f * TILE)) * TILE; h = -(-im.height // (f * TILE)) * TILE   # whole tiles, sprite px
    big = Image.new("RGBA", (w * f, h * f), (0, 0, 0, 0))
    big.alpha_composite(im, ((w * f - im.width) // 2, h * f - im.height))
    small = big.resize((w, h), Image.BOX)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0); small.putalpha(a)
    bg = (246, 238, 222, 255)
    out = Image.new("RGBA", (2 * w * ZOOM + 3 * 24, h * ZOOM + 2 * 24), bg)
    d = ImageDraw.Draw(out)
    for k, pic in enumerate((big.resize((w * ZOOM, h * ZOOM), Image.LANCZOS), small.resize((w * ZOOM, h * ZOOM), Image.NEAREST))):
        x0, y0 = 24 + k * (w * ZOOM + 24), 24
        for gx in range(0, w + 1, TILE):
            d.line([(x0 + gx * ZOOM, y0), (x0 + gx * ZOOM, y0 + h * ZOOM)], fill=(214, 204, 186, 255))
        for gy in range(0, h + 1, TILE):
            d.line([(x0, y0 + gy * ZOOM), (x0 + w * ZOOM, y0 + gy * ZOOM)], fill=(214, 204, 186, 255))
        out.alpha_composite(pic, (x0, y0))
        d.line([(x0, y0 + h * ZOOM), (x0 + w * ZOOM, y0 + h * ZOOM)], fill=(120, 108, 96, 255), width=2)
    out.convert("RGB").save(path.replace("_side.png", "_side_sprite.png"))
    print("SPRITE", path, f"{w}x{h} sprite px")
