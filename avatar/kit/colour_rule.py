"""The player-colour rule (README "Playable characters", rule 1). Pure Python, no Blender.

P1 green and P2 red belong to the player slots. A playable character's MAIN colours (skin, hair,
headwear, top, bottoms, shoes in jarling.json) must sit at least PLAYER_DE_MIN (CIE Delta E 2000)
away from both, so a green alien uses a clearly different green, never P1's.
Used by jarling_kit.py, tools/check_colours.py and godot/run_tests.sh.
"""
import math

PLAYER_GREEN = "#3CC24A"
PLAYER_RED = "#E4393C"

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def srgb_to_lin(c):
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

def _lab(h):
    r, g, b = srgb_to_lin(hex_rgb(h))
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b)
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)

def delta_e2000(h1, h2):
    """CIE Delta E 2000 between two hex colours (sRGB, D65)."""
    return de2000_lab(_lab(h1), _lab(h2))

def de2000_lab(lab1, lab2):
    """CIE Delta E 2000 between two CIELAB colours."""
    L1, a1, b1 = lab1; L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cm = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if C1p > 1e-9 else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if C2p > 1e-9 else 0.0
    dL, dC = L2 - L1, C2p - C1p
    if C1p * C2p < 1e-9:
        dh = 0.0
    else:
        dh = h2p - h1p
        if dh > 180: dh -= 360
        elif dh < -180: dh += 360
    dH = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh) / 2)
    Lm, Cpm = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p < 1e-9:
        hm = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hm = (h1p + h2p) / 2
    else:
        hm = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hm - 30)) + 0.24 * math.cos(math.radians(2 * hm))
         + 0.32 * math.cos(math.radians(3 * hm + 6)) - 0.20 * math.cos(math.radians(4 * hm - 63)))
    dth = 30 * math.exp(-((hm - 275) / 25) ** 2)
    Rc = 2 * math.sqrt(Cpm ** 7 / (Cpm ** 7 + 25.0 ** 7))
    Sl = 1 + 0.015 * (Lm - 50) ** 2 / math.sqrt(20 + (Lm - 50) ** 2)
    Sc = 1 + 0.045 * Cpm
    Sh = 1 + 0.015 * Cpm * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dL / Sl) ** 2 + (dC / Sc) ** 2 + (dH / Sh) ** 2 + Rt * (dC / Sc) * (dH / Sh))

PLAYER_DE_MIN = 20.0   # a playable character's main colours must be at least this far from P1 green and P2 red

def main_colours(P):
    """The six main colours of a character's params (the ones the player-colour rule checks)."""
    o = P.get("outfit", {})
    m = {"skin": P.get("skin"), "hair": P.get("hair", {}).get("color"), "headwear": P.get("headwear", {}).get("color")}
    for part in ("top", "bottoms", "shoes"):
        m[part] = o.get(part, {}).get("color")
    return {k: v for k, v in m.items() if isinstance(v, str) and v.startswith("#")}

def player_colour_clashes(P, limit=PLAYER_DE_MIN):
    """[(part, colour, player, deltaE)] for every main colour closer than `limit` to a player colour."""
    out = []
    for part, col in main_colours(P).items():
        for who, pc in (("P1", PLAYER_GREEN), ("P2", PLAYER_RED)):
            d = delta_e2000(col, pc)
            if d < limit:
                out.append((part, col, who, round(d, 1)))
    return out
