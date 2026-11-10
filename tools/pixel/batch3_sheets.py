"""Batch 3 review sheets. Run from the repo root: python3 tools/pixel/batch3_sheets.py [lineup] [read]

lineup -> characters/batch3_pixel_lineup.png  Jeff, Chuck and the six batch-3 pixel forms on one ground line
read   -> characters/batch3_read_check.png    per character: the 3D side view, the pixel form at 1x and at The
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
BATCH = [("rexy", "Rexy"), ("boxbot", "Boxbot"), ("sir_clank", "Sir Clank"), ("captain_crumbs", "Captain Crumbs"),
         ("el_burrito", "El Burrito"), ("snooze", "Snooze")]
READS = {   # the director's "should read as" line per prop
    "rexy": ["hood: an orange dinosaur hood up round the face, white felt teeth along its top edge (not a fox, not a pumpkin)",
             "spikes and tail: yellow spikes over the hood and down the back, a short tail behind (the side view is the dinosaur)",
             "mouth: a big open-mouth grin (the only thing at the mouth)", "feet: orange footies"],
    "boxbot": ["boxes: two stacked cardboard boxes, the head box no wider than the body box (not a crate, not a TV)",
               "face: the real face through a cut-out, flat calm smile", "dials: marker dials with blue and yellow buttons on the body box",
               "arms: ribbed grey dryer-hose sleeves; grey pants, blue shoes"],
    "sir_clank": ["helmet: a silver saucepan on his head, its dark handle straight out the BACK at pot height (not a chef hat, not a bucket)",
                  "handle: far from the mouth, so nothing reads as a pipe", "chest: a yellow shield on a grey shirt",
                  "stance: very upright; serious brows, proud smile"],
    "captain_crumbs": ["hat: a very tall white chef hat with a small navy badge", "eyepatch: black patch over one eye with a strap to the hat band",
                       "moustache: big brown curls lying on the face over the grin, curling up (not sticking forward: no pipe)",
                       "body: tall, round middle; white chef jacket with navy buttons, navy striped pants, black boots"],
    "el_burrito": ["mask: the whole head gold, purple trim round the eyes and mouth (not a bald head, not a helmet)",
                   "cape: purple, flaring behind", "chest: purple star on a gold shirt", "body: short and wide; white wrestling boots"],
    "snooze": ["nightcap: a long striped cap flopping to one side, white pom-pom at the tip (not a gnome hat, not a horn)",
               "eyes: always closed happy arcs", "pyjamas: light blue with white star dots", "slippers: fuzzy yellow"],
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
    d.text((40, 14), "Batch 3 pixel forms (The Hill scale: 32 px = 1.2 m, capped at the 32 px frame), with Jeff and Chuck", fill=INK, font=font(36))
    ground, x = 440, 60
    d.line((20, ground, 1900, ground), fill="#B9AD96", width=3)
    for n, s in sp:
        big = up(s, 5); im.alpha_composite(big, (x, ground - big.height + 1))
        d.text((x + 30, ground + 10), f"{n}, {trim(s).height} px", fill=INK, font=font(18)); x += big.width + 4
    d.text((40, 520), "real size x1, x2 (in play), x3 (design scale)", fill=SOFT, font=font(18))
    x = 40
    for k in (1, 2, 3):
        for n, s in sp:
            b = up(s, k); im.alpha_composite(b, (x, 720 - b.height)); x += b.width - 10 * k
        x += 60
    d.text((40, 760), "silhouettes, 16 px tall, x4 and x1", fill=SOFT, font=font(18)); x = 40
    for n, s in sp:
        b = up(sil16(s), 4); im.alpha_composite(b, (x, 870 - b.height)); x += b.width + 40
    x += 60
    for n, s in sp:
        b = sil16(s); im.alpha_composite(b, (x, 870 - b.height)); x += b.width + 10
    im.convert("RGB").save("characters/batch3_pixel_lineup.png")


def read_check():
    RH = 350
    im = Image.new("RGBA", (1920, 70 + RH * len(BATCH)), rgba(BG)); d = ImageDraw.Draw(im)
    d.text((40, 14), "Batch 3 read check: 3D side view > pixel form > game size > 16 px silhouette", fill=INK, font=font(34))
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
    im.convert("RGB").save("characters/batch3_read_check.png")


if __name__ == "__main__":
    todo = sys.argv[1:] or ["lineup", "read"]
    if "lineup" in todo: lineup()
    if "read" in todo: read_check()
