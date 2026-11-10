"""Run from the repo root: python3 tools/pixel/make_sheets.py  -> five 1920x1080 PNGs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import px, residents as R
from px import up, silhouette, font, bubble, rgba

BG = "#F6EFE0"
FACT = {"mole": R.mole, "foreman": R.foreman, "caveman": R.caveman}
SW = {
    "mole": [("fur", "#56607A"), ("belly", "#8792AC"), ("snout/claws", "#F2A0A8"), ("nose tip", "#E0607A"),
             ("shovel wood", "#B07A3C"), ("steel", "#B8C4D0"), ("outline", "#2A1E2C")],
    "foreman": [("cone hat", "#1E9AA0"), ("hard hat", "#F4F1E6"), ("beard", "#EDE6D6"), ("vest", "#F7932F"),
                ("skin", "#E8B48C"), ("nose", "#E59A86"), ("boots", "#4A3B3B"), ("clipboard", "#B07A3C"),
                ("paper", "#FFFDF4"), ("whistle", "#FFD23F"), ("outline", "#2A1E2C")],
    "caveman": [("hair/beard", "#7A4A2A"), ("skin", "#D99A6C"), ("tunic", "#D9A441"), ("spots", "#7C4E24"),
                ("ice cube", "#BFE6F5"), ("cloth", "#F3EAD2"), ("string", "#1E9AA0"), ("outline", "#2A1E2C")],
    "dragon": [("body", "#A88BE0"), ("shade", "#8C6FC8"), ("belly/horns", "#FFF0C9"), ("wings/puff", "#FFB37A"),
               ("cheeks", "#F7A6C0"), ("smoke", "#C9C4D4"), ("outline", "#2A1E2C")],
}
TITLE = {"mole": "The Mole", "foreman": "The Gnome Foreman", "caveman": "The Caveman", "dragon": "The Dragon"}
DEED = {"mole": px.ic_shovel, "foreman": px.ic_wall, "caveman": px.ic_ice, "dragon": px.ic_snore}
OUTD = {"mole": "characters/mole", "foreman": "characters/gnome_foreman", "caveman": "characters/caveman",
        "dragon": "characters/dragon"}


def canvas():
    im = Image.new("RGBA", (1920, 1080), rgba(BG)); return im, ImageDraw.Draw(im)


def paste(im, sp, x, y): im.alpha_composite(sp, (x, y))


def red(im, f):
    """Integer nearest-neighbour reduction (used only to fit big dragon art into bubbles)."""
    return im if f == 1 else im.resize((im.width // f, im.height // f), Image.NEAREST)


def swatches(d, name, x, y, per=8):
    f = font(15); dx = 72 if len(SW[name]) > 8 and per > 8 else 100
    for i, (n, c) in enumerate(SW[name]):
        cx, cy = x + (i % per) * dx, y + (i // per) * 100
        d.rectangle((cx, cy, cx + 48, cy + 40), fill=c, outline="#2A1E2C", width=2)
        d.text((cx, cy + 44), c, fill="#2A1E2C", font=f); d.text((cx, cy + 62), n, fill="#6A5E6C", font=f)


def heads_row(im, d, name, x, y, k, gap):
    f = font(18)
    for i, e in enumerate(R.EXPRS[name]):
        h = up(R.head(name, e), k); paste(im, h, x + i * gap, y)
        d.text((x + i * gap, y + h.height + 6), e, fill="#2A1E2C", font=f)


def bubbles(im, d, name, x, y, k=4):
    kind = {"foreman": "foreman"}.get(name, name)
    fct = 4 if name == "dragon" else 1
    hd = lambda e: red(R.head(name, e), fct)
    nuis = {"mole": R.mole("front", "popup", "startled"), "foreman": R.foreman("front", "whistle"),
            "caveman": R.caveman("front", "wave", "delighted"), "dragon": red(R.dragon("asleep"), 4)}[name]
    deed, arrow, plus = DEED[name](), px.ic_arrow(), px.ic_plus()
    ruin, home, gift = px.ic_home(kind, False), px.ic_home(kind, True), px.ic_gift(kind)
    blocks = px.ic_blocks()
    rows = [[deed, nuis], [deed, hd("sorry"), arrow, ruin, hd("hopeful")], [ruin, plus, blocks, arrow, home, gift]]
    caps = ["encounter", "arrival", "fix-up"]
    f = font(26); cx = x
    for items, cap in zip(rows, caps):
        w = sum(i.width for i in items) + 4 * (len(items) - 1) + 12
        h = max(i.height for i in items) + 8
        b = bubble(w, h, 0.15, k); px_ = cx
        ix = 6
        for it in items:
            iy = 4 + (h - 8 - it.height) // 2 + 1
            b.alpha_composite(up(it, k), (ix * k, iy * k)); ix += it.width + 4
        im.alpha_composite(b, (px_, y)); d.text((px_ + 8, y + b.height + 6), cap, fill="#2A1E2C", font=f)
        cx += b.width + 50
    return cx


def lines(d, x, y, t, size=44):
    d.text((x, y), t, fill="#2A1E2C", font=font(size))


def sheet(name):
    im, d = canvas(); lines(d, 40, 14, TITLE[name] + " (3D-first redraw, 2026-11-10: traced from the 3D master, hand-cleaned)", 40)
    sm = font(18)
    if name != "dragon":
        F = FACT[name]; views = [F(v, "idle", R.EXPRS[name][0]) for v in ("front", "side", "back")]
        for i, v in enumerate(views):
            paste(im, up(v, 8), 40 + i * 340, 90); d.text((40 + i * 340, 350), ("front", "side", "back")[i], fill="#2A1E2C", font=sm)
        d.rounded_rectangle((1090, 90, 1880, 340), 12, outline="#B9AD96", width=3, fill="#FBF7EC")
        d.text((1104, 98), "real size x1 / x2", fill="#6A5E6C", font=sm)
        for i, v in enumerate(views):
            paste(im, up(v, 2), 1104 + i * 100, 130); paste(im, v, 1104 + i * 100 + 20, 250)
        poses = {"mole": ("idle", "dig", "popup"), "foreman": ("idle", "whistle", "hat_in_hands"),
                 "caveman": ("idle", "polish", "wave")}[name]
        for i, p in enumerate(poses):
            paste(im, up(F("front", p, R.EXPRS[name][0 if p != "whistle" else 4]), 8), 40 + i * 340, 400)
            d.text((40 + i * 340, 660), p, fill="#2A1E2C", font=sm)
        k = max(1, 150 // R.HEAD_BOX[name][2] + 0)
        bx = R.HEAD_BOX[name]; k = 150 // (bx[2] - bx[0])
        heads_row(im, d, name, 1090, 400, k, 160)
        swatches(d, name, 1090, 580, 8 if name != 'foreman' else 11)
        bubbles(im, d, name, 40, 750)
    else:
        paste(im, up(R.dragon("sit", "sleepy"), 3), 20, 70); sit_bottom = 70 + 336
        paste(im, up(R.jeff(), 3), 410, sit_bottom - 96); d.text((410, sit_bottom + 4), "Jeff, 32 px", fill="#2A1E2C", font=sm)
        paste(im, up(R.dragon("yawn"), 3), 520, 70)
        paste(im, up(R.dragon("asleep"), 3), 910, sit_bottom - 216)
        for i, v in enumerate(("side", "back")):
            paste(im, R.dragon("sit", "sleepy", v), 1440 + i * 140, sit_bottom - 112)
        d.text((1440, sit_bottom + 4), "side, back x1", fill="#2A1E2C", font=sm)
        d.text((910, sit_bottom + 30), "asleep: hand-drawn (no curled pose in 3D)", fill="#6A5E6C", font=sm)
        for t, x in (("sit", 20), ("yawn", 520), ("asleep", 910)):
            d.text((x, 20), t, fill="#6A5E6C", font=sm) if False else d.text((x, sit_bottom + 4), t, fill="#2A1E2C", font=sm)
        heads_row(im, d, "dragon", 20, 450, 2, 220)
        swatches(d, "dragon", 1160, 450, 4)
        bubbles(im, d, "dragon", 40, 760)
    p = OUTD[name] + "/refs"; os.makedirs(p, exist_ok=True)
    im.convert("RGB").save(p + "/look_sheet.png")


def lineup():
    im, d = canvas(); lines(d, 40, 14, "The Hill: residents lineup (3D-first redraw, 2026-11-10; one scale: 32 px = 1.2 m, Dragon 3.5 players)", 36)
    sp = [("Jeff", R.jeff()), ("Chuck", R.chuck()), ("Mole", R.mole()), ("Foreman", R.foreman()),
          ("Caveman", R.caveman()), ("Dragon", R.dragon("sit", "sleepy"))]
    ground, x, f = 690, 40, font(24)
    d.line((20, ground, 1900, ground), fill="#B9AD96", width=3)
    for n, s in sp:
        big = up(s, 5); paste(im, big, x, ground - big.height + 1); d.text((x + big.width // 2 - 40, ground + 10), n, fill="#2A1E2C", font=f)
        x += big.width + (10 if s.width == 40 else 0)
    d.text((40, 790), "silhouettes x2", fill="#6A5E6C", font=font(18)); d.text((1000, 790), "real size x1", fill="#6A5E6C", font=font(18))
    x, g2, g1 = 40, 1040, 1040
    for n, s in sp:
        sil = up(silhouette(s), 2); paste(im, sil, x, g2 - sil.height); x += sil.width + 16
    x = 1000
    for n, s in sp:
        sil = silhouette(s); paste(im, sil, x, g1 - sil.height); x += sil.width + 10
    im.convert("RGB").save("characters/residents_lineup.png")


if __name__ == "__main__":
    for n in ("mole", "foreman", "caveman", "dragon"):
        sheet(n)
    lineup()
