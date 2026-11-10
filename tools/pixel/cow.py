#!/usr/bin/env python3
"""The cow's pixel form (proposal), traced from her 3D master, and her read check. Run from the repo root:

    for v in ...: blender ... avatar/kit/render_trace.py -- --params proposals/cow/jarling.json ...   (see RETRACE)
    python3 tools/pixel/cow.py

Same reduction as tools/pixel/trace3d.py (majority vote per sprite pixel after snapping to the fixed
palette, 512 px per 1.2 m in, Jeff = 32 px out), then a small hand-clean (CLEAN: eye and nostril
pixels the reduction drops at this size) and the library's 1 px outline. Writes:
  proposals/cow/refs/pixel/cow_<pose>.png      native-size sprites (outline included)
  proposals/cow/refs/cow_pixel_sheet.png       every pose at x6, on The Hill's 16 px tile grid
  proposals/cow/refs/cow_read_check.png        read check: 16 px tall, x1/x2/x4, tiny and giant (Junk Yard Zap
                                               grow/shrink steps, 1.3 per step, 4 each way), 3D beside Jeff
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
import trace3d as T3
from px import outline, up, silhouette, font, rgba, OUT

RETRACE = [  # render_trace.py arguments (after --params proposals/cow/jarling.json)
    "--views front,side,back",
    "--views front --action tipped --frame 1 --expression dizzy --tag tipped",
    "--views side --action run --frame 1 --expression happy --tag trot1",
    "--views side --action run --frame 5 --expression happy --tag trot2",
    "--views side --action graze --frame 1 --tag graze",
    "--views front --action idle --frame 1 --expression panicked --tag panicked",
]
CID = "cow"
T3.PAL[CID] = {"w": "#F4F1EA", "k": "#2B2B33", "p": "#F2B8C0", "n": "#B85C70", "h": "#E8CF9A", "f": "#4A3B3B",
               "o": OUT, "W": "#FFFFFF"}
T3.SCALE[CID] = "true"            # 1.07 m: 29 px at true scale (Jeff with his comb, 1.2 m, is 32 px)
T3.CANVAS[CID] = (48, 32)
POSES = [("", "side"), ("", "front"), ("", "back"), ("trot1", "side"), ("trot2", "side"), ("graze", "side"),
         ("tipped", "front"), ("panicked", "front")]
OUTDIR = os.path.join(ROOT, "proposals", "cow", "refs")


def sprite(rows, pal):
    h, w = len(rows), len(rows[0])
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                im.putpixel((x, y), rgba(pal[ch]))
    # trim empty rows at the top (HEADROOM) but keep the frame width
    bb = im.getbbox()
    return im.crop((0, max(0, bb[1] - 1), w, h)) if bb else im


def clean(name, rows):
    """Hand-clean: at 29 px the eye is under a pixel and the vote drops it; put it back."""
    rows = [list(r) for r in rows]
    def put(x, y, ch):
        if 0 <= y < len(rows) and 0 <= x < len(rows[0]) and rows[y][x] != ".":
            rows[y][x] = ch
    def find(ch):
        """The muzzle: the bottom-most run of rows holding ch (the pink inner ears sit higher up)."""
        pts = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == ch]
        if not pts:
            return []
        ys = {y for _x, y in pts}; top = bot = max(ys)
        while top - 1 in ys:
            top -= 1
        return [(x, y) for x, y in pts if top <= y <= bot]
    if name.endswith("_side") and "graze" not in name:
        mz = find("p")
        if mz:                                    # the eye: up and behind the muzzle's top corner (she faces left)
            for y, r in enumerate(rows):          # an eye pixel on the silhouette edge merges with the outline
                for x, c in enumerate(r):
                    if c == "o" and (x == 0 or r[x - 1] == "." or x + 1 == len(r) or r[x + 1] == "."):
                        r[x] = "w"
            top = min(y for _x, y in mz)
            xs = [x for x, y in mz if y == top]
            put(max(xs) + 2, top - 2, "o")
            put(min(x for x, y in mz if y == top + 1) + 1, top + 1, "n")
    if name.endswith("_front") and "tipped" not in name:
        mz = find("p")
        if mz:
            top = min(y for _x, y in mz); xs = [x for x, y in mz if y == top]
            cx = (min(xs) + max(xs)) // 2
            put(cx - 2, top + 1, "n"); put(cx + 2, top + 1, "n")
    for y, r in enumerate(rows):                  # an eye on the face patch gets a coat-coloured rim (as in 3D)
        for x, c in enumerate(r):
            if c == "o":
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, -1)):
                    if 0 <= y + dy < len(rows) and 0 <= x + dx < len(r) and rows[y + dy][x + dx] == "k":
                        rows[y + dy][x + dx] = "w"
    return ["".join(r) for r in rows]


def build():
    s, tgt = T3.scale_for(CID)
    out = {}
    for tag, view in POSES:
        key, rows = T3.reduce(CID, tag, view, s)
        rows = clean(key, rows)
        out[key] = outline(sprite(rows, T3.PAL[CID]))
    small = {}
    s16 = s * 14 / (tgt - 2)                     # 16 px tall with the outline
    T3.CANVAS[CID] = (28, 18)
    for tag, view in (("", "side"), ("", "front"), ("tipped", "front")):
        key, rows = T3.reduce(CID, tag, view, s16)
        small[key] = outline(sprite(rows, T3.PAL[CID]))
    return out, small, tgt


def tiles(im, k, tile=16):
    """x k on a light tile grid, feet on the bottom line."""
    w, h = -(-im.width // tile) * tile, -(-im.height // tile) * tile
    bg = Image.new("RGBA", (w * k, h * k), (246, 238, 222, 255))
    d = ImageDraw.Draw(bg)
    for gx in range(0, w + 1, tile):
        d.line([(gx * k, 0), (gx * k, h * k)], fill=(214, 204, 186, 255))
    for gy in range(0, h + 1, tile):
        d.line([(0, gy * k), (w * k, gy * k)], fill=(214, 204, 186, 255))
    bg.alpha_composite(up(im, k), ((w - im.width) // 2 * k, (h - im.height) * k))
    return bg


def main():
    os.makedirs(os.path.join(OUTDIR, "pixel"), exist_ok=True)
    sp, small, tgt = build()
    for k, im in sp.items():
        im.save(os.path.join(OUTDIR, "pixel", f"{k}.png"))
    for k, im in small.items():
        im.save(os.path.join(OUTDIR, "pixel", f"{k}_16px.png"))
    f = font(18); fb = font(22)
    # pixel sheet: every pose x6
    labels = {"cow_side": "side (idle)", "cow_front": "front", "cow_back": "back", "cow_trot1_side": "trot f1",
              "cow_trot2_side": "trot f5", "cow_graze_side": "graze", "cow_tipped_front": "tipped", "cow_panicked_front": "panicked"}
    K = 6
    cells = [(labels[k], tiles(im, K)) for k, im in sp.items()]
    cw = max(c.width for _l, c in cells) + 24; ch = max(c.height for _l, c in cells) + 44
    sheet = Image.new("RGBA", (4 * cw + 24, 2 * ch + 70), (255, 253, 244, 255))
    d = ImageDraw.Draw(sheet)
    d.text((24, 16), f"Cow (proposal): pixel form traced from the 3D master, {tgt} px tall at The Hill's scale (Jeff = 32 px), x{K}", fill=rgba(OUT), font=fb)
    for i, (l, c) in enumerate(cells):
        x, y = 24 + (i % 4) * cw, 60 + (i // 4) * ch
        sheet.alpha_composite(c, (x, y + ch - 44 - c.height))
        d.text((x, y + ch - 36), l, fill=rgba(OUT), font=f)
    sheet.convert("RGB").save(os.path.join(OUTDIR, "cow_pixel_sheet.png"))
    # read check
    jeff = None
    for cand in ("characters/jeff/refs/pixel/jeff_side.png", "characters/jeff/refs/jeff_side_sprite.png"):
        if os.path.exists(os.path.join(ROOT, cand)):
            jeff = cand
    W = 1900
    rc = Image.new("RGBA", (W, 1500), (255, 253, 244, 255))
    d = ImageDraw.Draw(rc)
    d.text((24, 14), "Cow (proposal): read check. Does she read as a cow, and as herself, at game size?", fill=rgba(OUT), font=fb)
    y = 56
    d.text((24, y), "1. Sprite at 1x, x2 (The Hill on a 1080p TV) and x4 (4K)", fill=rgba(OUT), font=f); y += 30
    x = 24
    for k in (1, 2, 4):
        for key in ("cow_side", "cow_front", "cow_tipped_front"):
            im = up(sp[key], k); rc.alpha_composite(im, (x, y + 4 * 32 - im.height)); x += im.width + 18
        x += 30
    y += 4 * 32 + 26
    d.text((24, y), "2. At 16 px tall (a far-away cow), x1 and x4, and as a flat silhouette x4", fill=rgba(OUT), font=f); y += 30
    x = 24
    for key, im in small.items():
        rc.alpha_composite(im, (x, y + 72 - im.height)); x += im.width + 14
    x += 30
    for key, im in small.items():
        im4 = up(im, 4); rc.alpha_composite(im4, (x, y + 72 - im4.height)); x += im4.width + 18
    x += 20
    for key, im in small.items():
        im4 = up(silhouette(im), 4); rc.alpha_composite(im4, (x, y + 72 - im4.height)); x += im4.width + 18
    y += 72 + 30
    d.text((24, y), "3. Junk Yard Zap grow/shrink: 1.3 per step, 4 steps each way (-4 = x0.35, +4 = x2.86), pixel form x2 beside Jeff (32 px)",
           fill=rgba(OUT), font=f); y += 30
    x = 24; base = y + 2 * 96
    import residents
    jim = residents.jeff("front")
    for st in (-4, -2, 0, 2, 4):
        kf = 1.3 ** st
        im = sp["cow_side"]
        im = im.resize((max(1, round(im.width * kf)), max(1, round(im.height * kf))), Image.NEAREST)
        im = up(im, 2)
        if jim:
            j2 = up(jim, 2); rc.alpha_composite(j2, (x, base - j2.height)); x += j2.width + 6
        rc.alpha_composite(im, (x, base - im.height))
        d.text((x, base + 6), f"step {st:+d} (x{kf:.2f})", fill=rgba(OUT), font=f)
        x += max(im.width, 120) + 40
    y = base + 40
    s3 = os.path.join(ROOT, ".scratch", "quad", "cow_scale.png")
    if os.path.exists(s3):
        d.text((24, y), "4. The 3D master at the same steps beside Jeff (render_quadruped.py --only scale)", fill=rgba(OUT), font=f); y += 30
        im = Image.open(s3).convert("RGBA"); im = im.crop((0, round(im.height * 0.22), im.width, round(im.height * 0.80))); im = im.resize((W - 48, round(im.height * (W - 48) / im.width)), Image.LANCZOS)
        rc.alpha_composite(im, (24, y)); y += im.height + 20
    rc = rc.crop((0, 0, W, y + 10))
    rc.convert("RGB").save(os.path.join(OUTDIR, "cow_read_check.png"))
    print("COW_PIXEL", {k: im.size for k, im in sp.items()}, "16px", {k: im.size for k, im in small.items()})


if __name__ == "__main__":
    main()
