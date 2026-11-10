"""Pixel sprites for the Hill residents (Pillow only). 3D-first redraw, 2026-11-10.

The Mole, the Gnome Foreman, the Caveman and the Dragon (sitting) are TRACED from their 3D masters:
`traced.py` holds the palette-snapped fill (tools/pixel/trace3d.py from avatar/kit/render_trace.py;
re-run everything with tools/pixel/retrace.sh). Each function below then HAND-CLEANS the traced base
with the explicit pixel edits listed in it (faces, the whistle, the clipboard lines, the ice-cube
glint, the club's string...), placed from anchors found in the base (snout, nose, face, eyes), so a
re-trace keeps them in place. Then the 1 px #2A1E2C outline. Jeff and Chuck are hand-drawn (approved).
The Dragon's curled-asleep pose stays hand-drawn: the 3D master has no curled pose.
"""
from PIL import Image
from px import Spr, OUT, rgba, PAPER, mirror
import traced as TR

W, H = 40, 32
TEAR, SWEAT, BLUSH = "#8FD3F4", "#8FD3F4", "#F7A6C0"
WHITE = "#FFFFFF"
EXPRS = {
    "mole": ["squint", "happy", "sorry", "hopeful", "startled"],
    "foreman": ["stern", "approving", "sorry", "hopeful", "whistle"],
    "caveman": ["delighted", "baffled", "sorry", "hopeful", "amazed"],
    "dragon": ["sleepy", "yawn", "happy", "sorry", "hopeful"],
}


def fin(s, w=W, h=H):
    """Outline, then stand the figure on the bottom row of the w x h canvas (feet on the ground line).
    Every resident fits the frame; the Mole is shorter than 32 px (true 3D scale)."""
    im = s.done()
    bb = im.getbbox()
    assert bb and bb[3] - bb[1] <= h and bb[0] >= 0 and bb[2] <= w, f"bbox {bb}"
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im.crop((0, bb[1], w, bb[3])), (0, h - (bb[3] - bb[1])))
    return out


def drop(s, x, y):
    s.px(SWEAT, (x, y), (x, y + 1), (x + 1, y + 1)); s.px(SWEAT, (x, y + 2))


# ---------------------------------------------------------------- traced bases + anchors
def base(key, cid, flip=False):
    """A Spr holding the traced fill `key` (no outline). Side views are mirrored to face screen-right."""
    rows, pal = TR.BASES[key], TR.PAL[cid]
    s = Spr(len(rows[0]), len(rows))
    pix = s.im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                pix[x, y] = rgba(pal[ch])
    if flip:
        s.im.paste(mirror(s.im))
    return s


def find(s, col, box=None):
    """Pixels of colour `col` (inside box x0, y0, x1, y1 inclusive)."""
    c, pix = rgba(col), s.im.load()
    x0, y0, x1, y1 = box or (0, 0, s.im.width - 1, s.im.height - 1)
    return [(x, y) for y in range(max(0, y0), min(s.im.height, y1 + 1))
            for x in range(max(0, x0), min(s.im.width, x1 + 1)) if pix[x, y] == c]


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def top_row(s):
    return s.im.getbbox()[1]


def recolour(s, pts, col):
    s.px(col, *pts)


# ---------------------------------------------------------------- the Mole
SLATE, BELLY, PINK, NOSE, WOOD, STEEL, DIRT, DIRT2 = (
    "#56607A", "#8792AC", "#F2A0A8", "#E0607A", "#B07A3C", "#B8C4D0", "#8A5A3C", "#6E4528")


def mole_face(s, ex, sx0, sy0, sx1, sy1):
    """Snout box (sx0..sx1, sy0..sy1). Eyes: 2 px marks just above the snout's outer edges; mouth under it."""
    ey, my, cx = sy0 - 1, sy1 + 1, (sx0 + sx1) // 2
    eye = {"squint": [(-1, 0), (0, 0)], "happy": [(-1, 0), (0, -1)], "sorry": [(-1, -1), (0, 0)],
           "hopeful": [(0, 0), (0, -1)], "startled": [(0, 0)]}[ex]
    for x, d in ((sx0, 1), (sx1, -1)):
        s.px(OUT, *[(x + dx * d, ey + dy) for dx, dy in eye])
        if ex == "hopeful":
            s.px(WHITE, (x - d, ey - 1))
        if ex == "startled":
            s.px(WHITE, (x - d, ey), (x, ey - 1))
    m = {"squint": [(cx, my), (cx + 1, my)],
         "happy": [(cx - 1, my), (cx, my + 1), (cx + 1, my + 1), (cx + 2, my)],
         "sorry": [(cx - 1, my + 1), (cx, my), (cx + 1, my), (cx + 2, my + 1)],
         "hopeful": [(cx, my), (cx + 1, my)],
         "startled": [(cx, my), (cx + 1, my), (cx, my + 1), (cx + 1, my + 1)]}[ex]
    s.px(OUT, *m)
    if ex in ("happy", "hopeful"):
        s.px(PINK, (sx0 - 2, sy0 + 1), (sx1 + 2, sy0 + 1))
    if ex in ("sorry", "startled"):
        drop(s, sx1 + 4, ey - 3)


def mole(view="front", pose="idle", expr="squint"):
    """Front/side/back; poses idle (claws out, no shovel), dig (shovel two-handed; `bouquet` is the old
    name), popup (out of a dirt mound). Traced at true 3D scale: about 24 px tall."""
    pose = "dig" if pose == "bouquet" else pose
    key = f"mole_{pose}_front" if view == "front" and pose in ("popup", "dig") else f"mole_{view}"
    s = base(key, "mole", flip=view == "side")
    t = top_row(s)
    snout = find(s, PINK, (0, t, W - 1, t + 7))
    if view == "front" and snout:
        sx0, sy0, sx1, sy1 = bbox(snout)
        cx = (sx0 + sx1) // 2
        s.px(NOSE, (cx, sy0 + 1), (cx + 1, sy0 + 1))                   # hand: nose tip (lost at 1/16)
        mole_face(s, expr, sx0, sy0, sx1, sy1)
        if pose == "dig":                                              # hand: the shovel, redrawn from the traced blade
            st = find(s, STEEL)
            if st:
                bx0, by0, bx1, by1 = bbox(st)
                body = find(s, SLATE); _, _, _, gy = bbox(body)
                s.px(SLATE, *[p for p in st + find(s, WOOD) if p[0] <= bx0 + 1])
                s.px(SLATE, *[p for p in find(s, PINK, (0, sy1 + 3, bx0 - 1, s.im.height - 1))])
                s.l([(sx0 - 6, by0 - 4), (bx0 + 1, by0 + 1)], WOOD)    # handle across him, claw to blade
                s.px(PINK, (sx0 - 7, by0 - 4), (sx0 - 6, by0 - 3), (sx0 - 7, by0 - 3))
                s.p([(bx0 + 1, by0), (bx0 + 5, by0), (bx0 + 5, by0 + 3), (bx0 + 3, by0 + 5), (bx0 + 1, by0 + 3)], STEEL)
                s.px(WHITE, (bx0 + 2, by0 + 1), (bx0 + 2, by0 + 2))
                s.px(PINK, (bx0 - 1, by0 + 1), (bx0, by0 + 1), (bx0, by0 + 2))
    elif view == "side" and snout:
        sx0, sy0, sx1, sy1 = bbox(snout)
        s.px(NOSE, (sx1, sy0 + 1))
        s.px(OUT, (sx0 - 2, sy0 - 1), (sx0 - 3, sy0 - 1) if expr == "squint" else (sx0 - 2, sy0 - 2))
    if pose == "popup":                                                # hand: the mound he pops out of
        g = s.im.height - H                                            # rows of headroom above the frame
        s.e(4, 25 + g, 36, 40 + g, DIRT); s.e(3, 24 + g, 12, 31 + g, DIRT); s.e(28, 24 + g, 37, 31 + g, DIRT)
        s.cut(0, H - 1 + g, W - 1, s.im.height - 1)
        s.px(DIRT2, *[(x, y + g) for x, y in ((8, 28), (10, 27), (20, 28), (31, 29), (28, 27), (14, 29), (5, 29), (24, 29))])
    return fin(s)


# ---------------------------------------------------------------- the Gnome Foreman
TEAL, HARD, BEARD, VEST, CREAM, SKIN, FNOSE, BOOT, YEL = (
    "#1E9AA0", "#F4F1E6", "#EDE6D6", "#F7932F", "#F4F1E6", "#E8B48C", "#E59A86", "#4A3B3B", "#FFD23F")


def _gnome_eyes(s, e, lx, rx, ey):
    for x, d in ((lx, 1), (rx, -1)):                                   # d points to the nose
        if e == "approving":                                           # closed, smiling eyes
            s.px(OUT, (x - 1, ey), (x, ey - 1), (x + 1, ey))
        elif e == "hopeful":
            s.px(OUT, (x, ey)); s.px(WHITE, (x - d, ey))
        elif e == "whistle":
            s.px(OUT, (x - d, ey), (x, ey))
        else:
            s.px(OUT, (x, ey))
        if e == "stern":                                               # brows down at the nose
            s.px(BEARD, (x - d, ey - 1), (x, ey - 1), (x + d, ey))
        elif e == "sorry":                                             # brows up at the nose
            s.px(BEARD, (x - d, ey), (x, ey - 1), (x + d, ey - 1))
        else:
            s.px(BEARD, (x - d, ey - 2 if e == "approving" else ey - 1), (x, ey - 2 if e == "approving" else ey - 1))


def foreman(view="front", pose="idle", expr=None):
    """Front/side/back; poses idle (clipboard, whistle hanging on his chest), whistle (raised to the mouth,
    blowing), hat_in_hands. Traced at 32 px (1.23 m with the cone: true scale)."""
    expr = expr or ("whistle" if pose == "whistle" else "stern")
    blowing = pose == "whistle" or expr == "whistle"
    key = "gnome_foreman_whistle_" + view if blowing and view in ("front", "side") else "gnome_foreman_" + view
    s = base(key, "gnome_foreman", flip=view == "side")
    nose = find(s, FNOSE)
    if view == "front" and nose:
        nx0, ny0, nx1, ny1 = bbox(nose)
        nx1 = max(nx1, nx0 + 1)
        s.r(nx0, ny0, nx1, ny0 + 1, FNOSE)                             # hand: round 2 x 2 nose
        _gnome_eyes(s, expr, nx0 - 2, nx1 + 2, ny0)
        if expr in ("approving", "hopeful", "sorry"):
            s.px(FNOSE, (nx0 - 3, ny0 + 1), (nx1 + 3, ny0 + 1))         # rosy cheeks
        if expr == "sorry":
            drop(s, nx1 + 7, ny0 - 3)
    elif view == "side" and nose:
        nx0, ny0, nx1, ny1 = bbox(nose)
        s.r(nx0, ny0, nx1 + 1, ny0 + 1, FNOSE)
        s.px(OUT, (nx0 - 2, ny0)); s.px(BEARD, (nx0 - 3, ny0 - 1), (nx0 - 2, ny0 - 1))
    t = top_row(s)
    hat = find(s, HARD, (0, t, W - 1, t + 5))
    if hat:                                                            # hand: the tiny hard hat, a clean dome + brim on the cone tip
        for p in hat:
            s.cut(*p, *p)
        cone = find(s, TEAL); ct = min(p[1] for p in cone)
        tip = [p[0] for p in cone if p[1] == ct]; c = (min(tip) + max(tip)) // 2
        if pose != "hat_in_hands":
            s.r(c - 1, ct - 2, c + 1, ct - 2, HARD); s.r(c - 2, ct - 1, c + 2, ct - 1, HARD); s.r(c - 3, ct, c + 3, ct, HARD)
    # the whistle: always hand-placed. Clear what the trace made of it, then draw it.
    recolour(s, find(s, YEL), VEST)
    beard = find(s, BEARD, (0, t + 12, W - 1, s.im.height - 1))
    if blowing and view == "front":
        # raised to his mouth, held in his hand at the beard's edge, with a blast of sound lines
        # at his mouth, pointing at us (a round yellow end), hand under it, a blast of sound lines
        nx0, ny0, nx1, ny1 = bbox(find(s, FNOSE))
        wy = ny0 + 2
        s.px(YEL, (nx0, wy), (nx0 + 1, wy), (nx0, wy + 1), (nx0 + 1, wy + 1)); s.px(OUT, (nx0 + 1, wy + 1))
        s.px(SKIN, (nx0 - 1, wy + 2), (nx0, wy + 2), (nx0 + 1, wy + 2), (nx0 + 2, wy + 2))
        bx = max(p[0] for p in find(s, BEARD)) + 2
        for p in ((bx, wy - 3), (bx + 1, wy - 4), (bx + 1, wy), (bx + 2, wy), (bx + 3, wy), (bx, wy + 3), (bx + 1, wy + 4)):
            s.px(YEL, p)
    elif view == "front" and beard and pose != "hat_in_hands":
        bx0, by0, bx1, by1 = bbox(beard)
        tip = [p[0] for p in beard if p[1] == by1]
        cx = (min(tip) + max(tip)) // 2
        # hangs on its cord BELOW the beard, centred on the chest: cord V, barrel, ring
        s.px(WOOD, (cx - 1, by1 + 1), (cx + 2, by1 + 1))
        s.px(YEL, (cx, by1 + 2), (cx + 1, by1 + 2), (cx, by1 + 3)); s.px(OUT, (cx + 1, by1 + 3))
    elif view == "side" and beard and not blowing:
        bx0, by0, bx1, by1 = bbox(beard)
        s.px(YEL, (bx1, by1 + 2), (bx1, by1 + 3))
    # the clipboard: paper with two written lines and the cream clip
    paper = find(s, PAPER)
    if paper and pose != "hat_in_hands":
        px0, py0, px1, py1 = bbox(paper)
        s.r(px0 - 1, py0 - 1, px1 + 1, py1 + 1, WOOD); s.r(px0, py0, px1, py1, PAPER)
        s.px(CREAM, ((px0 + px1) // 2, py0 - 1))
        for y in range(py0 + 1, py1, 2):
            s.px(WOOD, *[(x, y) for x in range(px0, px1)])
    if pose == "hat_in_hands" and view == "front":
        vest = find(s, VEST)
        vx0, vy0, vx1, vy1 = bbox(vest)
        s.cut(0, vy0 - 4, vx0 - 1, s.im.height - 1); s.cut(vx1 + 1, vy0 - 4, W - 1, s.im.height - 1)
        cx = (vx0 + vx1) // 2
        s.r(vx0 - 1, vy0 + 2, vx0, vy0 + 4, VEST); s.r(vx1, vy0 + 2, vx1 + 1, vy0 + 4, VEST)
        s.e(cx - 4, vy0 + 1, cx + 4, vy0 + 7, OUT); s.e(cx - 3, vy0 + 2, cx + 3, vy0 + 6, HARD)
        s.r(cx - 5, vy0 + 5, cx + 5, vy0 + 6, OUT); s.r(cx - 4, vy0 + 5, cx + 4, vy0 + 5, HARD)
        s.px(SKIN, (cx - 5, vy0 + 4), (cx + 5, vy0 + 4))
    return fin(s)


# ---------------------------------------------------------------- the Caveman
HAIR, CSKIN, TUN, SPOT, ICE, CLOTH, STR = "#7A4A2A", "#D99A6C", "#D9A441", "#7C4E24", "#BFE6F5", "#F3EAD2", "#1E9AA0"


def cave_face(s, ex, cx, fy):
    """Face centred on column cx; fy = the eyes' top row. Eyes 2 x 2 at cx-3 and cx+2, brows above, mouth below."""
    lx, rx, my = cx - 3, cx + 2, fy + 2
    for x, d in ((lx, -1), (rx, 1)):                                   # d points away from the middle
        xo = x + (1 if d == 1 else 0); xi = x + (0 if d == 1 else 1)  # outer / inner column
        if ex == "delighted":
            s.r(x, fy, x + 1, fy + 1, OUT); s.px(WHITE, (xo, fy))
        elif ex == "hopeful":
            s.r(x, fy, x + 1, fy + 1, OUT); s.px(WHITE, (xo, fy), (xi, fy))
        elif ex == "amazed":
            s.r(x, fy, x + 1, fy + 1, WHITE); s.px(OUT, (xi, fy + 1))
        elif ex == "baffled":
            if d == -1:
                s.r(x, fy, x + 1, fy + 1, WHITE); s.px(OUT, (xi, fy + 1))
            else:
                s.px(OUT, (x, fy + 1), (x + 1, fy + 1))
        elif ex == "sorry":
            s.px(OUT, (x, fy + 1), (x + 1, fy + 1))
        by = fy - 1
        if ex == "sorry":
            s.px(HAIR, (xi, by - 1), (xo, by))
        elif ex in ("amazed", "hopeful") or (ex == "baffled" and d == -1):
            s.px(HAIR, (x, by - 1), (x + 1, by - 1))
        else:
            s.px(HAIR, (x, by), (x + 1, by))
    m = {"delighted": [(cx - 1, my), (cx + 1, my)], "baffled": [(cx, my), (cx + 1, my)],
         "sorry": [(cx - 1, my), (cx, my), (cx + 1, my)], "hopeful": [(cx, my)], "amazed": [(cx - 1, my), (cx, my)]}[ex]
    s.px(OUT, *m)
    if ex == "delighted":
        s.px(WHITE, (cx, my))
    if ex in ("delighted", "sorry"):
        s.px(BLUSH, (lx - 1, fy + 2), (rx + 2, fy + 2))
    if ex == "sorry":
        drop(s, rx + 6, fy - 3)
    if ex == "hopeful":
        s.px("#FFD86B", (lx - 6, fy - 4), (lx - 7, fy - 4), (lx - 5, fy - 4), (lx - 6, fy - 5), (lx - 6, fy - 3))


def caveman(view="front", pose="idle", expr="delighted"):
    """Front/side/back; poses idle (cloth club up in his hand), polish, wave. Traced at 32 px (1.21 m: true scale)."""
    key = f"caveman_{pose}_front" if view == "front" and pose in ("polish", "wave") else f"caveman_{view}"
    s = base(key, "caveman", flip=view == "side")
    ice = find(s, ICE)
    if ice:                                                            # hand: the ice cube's glint
        ix0, iy0, ix1, iy1 = bbox(ice)
        s.px(WHITE, (ix0 + 1, iy0 + 2), (ix0 + 2, iy0 + 1))
    cloth = find(s, CLOTH)
    if cloth:                                                          # hand: the teal string round the cloth
        cx0, cy0, cx1, cy1 = bbox(cloth)
        tie = cy1 if pose != "polish" else cy0
        s.px(STR, *[p for p in cloth if p[1] == tie])
    if view == "front":
        hair = find(s, HAIR); hx0, hy0, hx1, hy1 = bbox(hair)
        face = [p for p in find(s, CSKIN, (hx0, hy0, hx1, hy1)) + find(s, OUT, (hx0, hy0, hx1, hy1))
                + find(s, WHITE, (hx0 + 2, hy0 + 4, hx1, hy1))
                if p[1] < hy0 + (hy1 - hy0) * 0.6]
        if face:
            fx0, fy0, fx1, fy1 = bbox(face)
            rows = {}
            for x, y in face:
                rows.setdefault(y, []).append(x)
            wide = max(rows, key=lambda y: len(rows[y]))
            s.px(CSKIN, *[p for p in face])                            # clear the traced eyes, redraw by hand
            cx = (min(rows[wide]) + max(rows[wide]) + 1) // 2
            cave_face(s, expr, cx, wide + 1)
    return fin(s)


# ---------------------------------------------------------------- Jeff and Chuck (pixel form)
JYEL, JOR, GRN, JEANS, COMB = "#FFD84D", "#F7932F", "#3CC24A", "#3B5BA5", "#D63384"
RED = "#E4393C"


def jeff(view="front"):
    s = Spr(W, H)
    s.r(19, 1, 21, 4, COMB); s.px(COMB, (18, 3), (22, 3))
    s.e(12, 3, 28, 20, JYEL)
    s.e(12, 2, 28, 10, GRN); s.r(12, 6, 28, 8, GRN); s.r(10, 9, 30, 10, GRN)
    s.r(19, 1, 21, 5, COMB)
    s.e(10, 14, 30, 28, JYEL)
    s.p([(11, 25), (29, 25), (31, 30), (9, 30)], JEANS); s.r(11, 25, 29, 25, JEANS)
    s.cut(19, 27, 21, 30)
    s.r(9, 29, 18, 30, JOR); s.r(22, 29, 31, 30, JOR)
    s.e(4, 15, 11, 25, JYEL); s.e(29, 15, 36, 25, JYEL); s.px(GRN, (5, 24), (6, 24), (7, 24), (33, 24), (34, 24), (35, 24), (4, 23), (36, 23))
    s.p([(18, 13), (22, 13), (20, 17)], JOR)
    s.px(OUT, (16, 12), (24, 12), (16, 11), (24, 11))
    return fin(s)


def chuck(view="front"):
    s = Spr(W, H)
    s.e(12, 8, 28, 21, "#E8B48C")
    s.e(12, 1, 28, 12, "#2B2B33"); s.r(12, 7, 28, 10, "#2B2B33")
    s.r(10, 10, 30, 11, RED); s.r(19, 1, 21, 7, RED)
    s.px("#FFD84D", (18, 5), (19, 5), (20, 5), (19, 6), (21, 6), (18, 7))
    s.px(OUT, (16, 14), (24, 14), (16, 13), (24, 13), (18, 18), (19, 19), (20, 19), (21, 19), (22, 18))
    s.r(10, 20, 30, 26, "#1E1E26"); s.px(RED, (15, 22), (16, 21), (17, 21), (18, 22), (17, 23), (16, 23))
    s.r(5, 21, 9, 26, "#1E1E26"); s.r(31, 21, 35, 26, "#1E1E26"); s.r(5, 27, 8, 27, "#E8B48C"); s.r(32, 27, 35, 27, "#E8B48C")
    s.r(12, 27, 19, 28, JEANS); s.r(21, 27, 28, 28, JEANS); s.r(12, 29, 19, 30, "#8A5A2B"); s.r(21, 29, 28, 30, "#8A5A2B")
    s.r(10, 26, 30, 27, JEANS)
    return fin(s)


# ---------------------------------------------------------------- the Dragon
LIL, SHADE, DCREAM, PEACH, CHEEK, SMOKE = "#A88BE0", "#8C6FC8", "#FFF0C9", "#FFB37A", "#F7A6C0", "#C9C4D4"
STRIPE = "#F0DAA6"


def _ring(s, x0, y0, x1, y1, w, c):
    s.e(x0, y0, x1, y1, c)
    s.cut_e = None
    s.d.ellipse((x0 + w, y0 + w, x1 - w, y1 - w), fill=(0, 0, 0, 0))


def _tail(s, pts, r, c):
    for x, y in pts:
        s.e(x - r, y - r, x + r, y + r, c)


def _dface(s, ex, cx, ey, dx=19):
    """Face centred on cx; eyes at y=ey."""
    for sx, d in ((cx - dx, 1), (cx + dx, -1)):
        if ex == "sleepy" or ex == "sorry":
            s.e(sx - 7, ey - 5, sx + 7, ey + 5, OUT); s.r(sx - 8, ey - 6, sx + 8, ey - 1, LIL)
            s.px("#FFFFFF", (sx - 3, ey + 1), (sx - 2, ey + 1))
            s.r(sx - 7, ey - 2, sx + 7, ey - 1, SHADE)
        elif ex == "hopeful":
            s.e(sx - 6, ey - 6, sx + 6, ey + 6, OUT); s.r(sx - 3, ey - 4, sx - 1, ey - 2, "#FFFFFF"); s.px("#FFFFFF", (sx + 2, ey + 2))
        elif ex in ("yawn",):
            s.arc((sx - 7, ey - 4, sx + 7, ey + 6), 200, 340, OUT); s.arc((sx - 7, ey - 5, sx + 7, ey + 5), 200, 340, OUT)
        elif ex == "happy":
            s.arc((sx - 7, ey - 2, sx + 7, ey + 10), 200, 340, OUT); s.arc((sx - 7, ey - 3, sx + 7, ey + 9), 200, 340, OUT)
    if ex in ("sorry", "hopeful"):
        for sx, d in ((cx - dx, 1), (cx + dx, -1)):
            for i in range(9):
                s.px(SHADE, (sx - 8 + i if d == 1 else sx - 8 + i, ey - 11 + (i // 3 if ex == "sorry" else 0) * (1 if d == 1 else 1) if False else ey - 12 + (-(i // 3) if (ex == "sorry") == (d == 1) else (i // 3)) + (2 if ex == "sorry" else 0)))
    s.e(cx - 12, ey + 7, cx - 2, ey + 14, CHEEK) if False else None
    s.e(cx - dx - 12, ey + 6, cx - dx + 4, ey + 17, CHEEK); s.e(cx + dx - 4, ey + 6, cx + dx + 12, ey + 17, CHEEK)
    s.r(cx - 4, ey + 8, cx - 3, ey + 9, OUT); s.r(cx + 3, ey + 8, cx + 4, ey + 9, OUT)
    my = ey + 14
    if ex == "yawn":
        s.e(cx - 12, my - 6, cx + 12, my + 20, OUT); s.e(cx - 8, my + 8, cx + 8, my + 19, CHEEK)
    elif ex == "happy":
        s.arc((cx - 9, my - 8, cx + 9, my + 4), 20, 160, OUT); s.arc((cx - 9, my - 9, cx + 9, my + 3), 20, 160, OUT)
    elif ex == "sorry":
        s.arc((cx - 7, my, cx + 7, my + 8), 200, 340, OUT); s.arc((cx - 7, my - 1, cx + 7, my + 7), 200, 340, OUT)
    elif ex == "hopeful":
        s.arc((cx - 6, my - 6, cx + 6, my + 2), 20, 160, OUT)
    else:
        s.arc((cx - 5, my - 5, cx + 5, my + 1), 20, 160, OUT)
    if ex == "sorry":
        drop(s, cx + dx + 14, ey - 8); s.px(SWEAT, (cx + dx + 14, ey - 9), (cx + dx + 14, ey - 10))


def dragon_asleep():
    """Curled asleep: hand-drawn (the 3D master has no curled pose; its `sleep` is a sitting nap)."""
    if True:
        s = Spr(160, 72)
        _tail(s, [(146, 52), (140, 62), (125, 64), (108, 64), (92, 62), (84, 58)], 7, LIL)
        s.e(14, 12, 150, 70, SHADE); s.e(12, 10, 146, 66, LIL)
        s.e(60, 30, 125, 66, DCREAM)
        for x in (72, 86, 100, 114):
            s.arc((x, 32, x + 28, 66), 190, 250, STRIPE)
        for x in (50, 72, 94, 116):
            s.e(x, 3, x + 14, 15, PEACH)
        s.e(110, 12, 140, 28, PEACH)
        s.e(4, 24, 70, 70, LIL); s.e(7, 20, 22, 36, DCREAM); s.e(34, 20, 49, 36, DCREAM)
        s.e(6, 40, 20, 54, CHEEK); s.e(50, 40, 64, 54, CHEEK)
        for sx in (25, 49):
            s.arc((sx - 9, 36, sx + 9, 52), 20, 160, OUT); s.arc((sx - 9, 37, sx + 9, 53), 20, 160, OUT)
        s.arc((29, 50, 41, 60), 20, 160, OUT); s.px(OUT, (34, 47), (36, 47))
        s.e(76, 52, 90, 66, "#4FD6E0"); s.r(79, 54, 81, 56, "#FFFFFF")
        _tail(s, [(78, 64), (70, 62)], 0, LIL); s.e(60, 54, 76, 68, PEACH)
        _ring(s, 6, 1, 30, 15, 5, SMOKE); _ring(s, 34, 4, 48, 12, 3, SMOKE)
        im = s.done()
        out = Image.new("RGBA", (160, 72), (0, 0, 0, 0)); out.paste(im, (0, 0)); return out


def _dragon_face(s, ex):
    """Hand-clean the traced sleepy face into expression `ex` (eyes and mouth found in the base)."""
    t = top_row(s); bb = s.im.getbbox(); cx = (bb[0] + bb[2]) // 2
    lids = find(s, SHADE, (0, t, s.im.width - 1, t + 45))
    if not lids:
        return
    ey0 = min(p[1] for p in lids)
    eyes = [p for p in find(s, OUT, (0, ey0, s.im.width - 1, ey0 + 14)) + find(s, WHITE, (0, ey0, s.im.width - 1, ey0 + 14)) + lids]
    ey1 = max(p[1] for p in eyes)
    L = bbox([p for p in eyes if p[0] < cx]); R = bbox([p for p in eyes if p[0] >= cx])
    below = sorted({p[1] for p in find(s, OUT, (cx - 9, ey1 + 1, cx + 9, ey1 + 22))})
    groups = []
    for y in below:
        if groups and y == groups[-1][-1] + 1:
            groups[-1].append(y)
        else:
            groups.append([y])
    mouth = groups[1] if len(groups) > 1 else []
    my = mouth[0] if mouth else ey1 + 12
    s.px(LIL, *eyes)
    if mouth:
        s.px(LIL, *find(s, OUT, (cx - 9, mouth[0], cx + 9, mouth[-1])))
    for (x0, y0, x1, y1), d in ((L, 1), (R, -1)):
        ecx, ecy = (x0 + x1) // 2, (y0 + y1) // 2 + 2
        if ex == "sleepy":                                             # the traced look, redrawn crisp
            s.e(ecx - 7, ecy - 5, ecx + 7, ecy + 4, OUT); s.r(ecx - 8, ecy - 6, ecx + 8, ecy - 1, SHADE)
            s.px(WHITE, (ecx - 3 * d, ecy + 1), (ecx - 2 * d, ecy + 1))
        elif ex == "sorry":
            s.e(ecx - 7, ecy - 5, ecx + 7, ecy + 4, OUT); s.r(ecx - 8, ecy - 6, ecx + 8, ecy - 1, SHADE)
            s.px(WHITE, (ecx - 3 * d, ecy + 1))
            for i in range(8):                                         # worried brows, up at the middle
                s.px(SHADE, (ecx - 4 * d + i * d, ecy - 9 - i // 3), (ecx - 4 * d + i * d, ecy - 10 - i // 3))
        elif ex == "hopeful":
            s.e(ecx - 6, ecy - 6, ecx + 6, ecy + 6, OUT); s.r(ecx - 3, ecy - 4, ecx - 1, ecy - 2, WHITE); s.px(WHITE, (ecx + 2, ecy + 2))
        elif ex == "happy":
            for k in (0, 1):
                s.arc((ecx - 7, ecy - 3 + k, ecx + 7, ecy + 9 + k), 200, 340, OUT)
    if ex == "happy":
        for k in (0, 1):
            s.arc((cx - 9, my - 9 + k, cx + 9, my + 3 + k), 20, 160, OUT)
    elif ex == "sorry":
        for k in (0, 1):
            s.arc((cx - 7, my + k, cx + 7, my + 8 + k), 200, 340, OUT)
        drop(s, R[2] + 6, ey0 - 2); s.px(SWEAT, (R[2] + 6, ey0 - 3))
    elif ex == "hopeful":
        s.arc((cx - 6, my - 6, cx + 6, my + 2), 20, 160, OUT)
    else:
        s.arc((cx - 5, my - 5, cx + 5, my + 1), 20, 160, OUT)


def dragon(pose="sit", expr="sleepy", view="front"):
    """Poses sit (traced, 112 px = 3.5 players), yawn (traced from the 3D `yawn`), asleep (hand-drawn,
    160 x 72). Views front/side/back for sit."""
    if pose == "asleep":
        return dragon_asleep()
    yawn = pose == "yawn" or expr == "yawn"
    key = "dragon_yawn_front" if yawn and view == "front" else f"dragon_{view}"
    s = base(key, "dragon", flip=view == "side")
    if view == "front" and not yawn:
        _dragon_face(s, expr)
    return fin(s, 128, 112)


# ---------------------------------------------------------------- heads
def _head_box(name):
    """Head crop for the bubbles and the expression rows, found from the traced front base."""
    if name in ("jeff", "chuck"):
        return (8, 0, 32, 22)
    im = {"mole": lambda: mole(), "foreman": lambda: foreman(), "caveman": lambda: caveman(),
          "dragon": lambda: dragon("sit", "sleepy")}[name]()
    x0, y0, x1, y1 = im.getbbox()
    if name == "dragon":
        return (x0 + 4, y0, x1 - 4, y0 + 66)
    h = {"mole": 10, "foreman": 23, "caveman": 21}[name]
    cx = (x0 + x1) // 2 if name != "foreman" else (lambda b: (b[0] + b[2]) // 2)(im.crop((0, y0, im.width, y0 + 20)).getbbox())
    half = {"mole": 7, "foreman": 9, "caveman": 13}[name]
    return (max(0, cx - half), y0, min(im.width, cx + half + 1), y0 + h)


HEAD_BOX = {n: _head_box(n) for n in ("mole", "foreman", "caveman", "jeff", "chuck", "dragon")}


def head(name, expr=None):
    if name == "dragon":
        im = dragon("sit", expr or "sleepy")
    elif name in ("jeff", "chuck"):
        im = {"jeff": jeff, "chuck": chuck}[name]()
    else:
        im = {"mole": mole, "foreman": foreman, "caveman": caveman}[name]("front", "idle", expr or EXPRS[name][0])
    return im.crop(HEAD_BOX[name])
