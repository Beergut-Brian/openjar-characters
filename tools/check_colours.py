#!/usr/bin/env python3
"""Player-colour rule check (CIE Delta E 2000). Run from the repo root.

    tools/check_colours.py                      # every playable character in characters.json
    tools/check_colours.py path/to/jarling.json # any params file (a proposal, a draft)
    tools/check_colours.py --self-test          # the Delta E maths against published reference pairs
    tools/check_colours.py --suggest "#3CC24A"  # show a colour's distance to both player colours

A main outfit colour (headwear, top, bottoms, shoes) closer than Delta E 20 to P1 green #3cc24a or
P2 red #e4393c fails; skin and hair fail under Delta E 10 (natural tones pass, a player-green skin does not). Prints "  ok   ..." / "  FAIL ..." lines; exit 1 on any failure.
"""
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "avatar" / "kit"))
import colour_rule as cr

REF = [  # Sharma, Wu, Dalal (2005) test pairs: Lab1, Lab2, Delta E 2000
    ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
    ((50.0, 3.1571, -77.2803), (50.0, 0.0, -82.7485), 2.8615),
    ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492),
    ((50.0, 2.5, 0.0), (61.0, -5.0, 29.0), 22.8977),
    ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
    ((63.0109, -31.0961, -5.8663), (62.8187, -29.7946, -4.0864), 1.2630),
    ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
]

def line(ok, what):
    print(("  ok   " if ok else "  FAIL ") + what)
    return ok

def check_params(P, label):
    bad = cr.player_colour_clashes(P)
    main = cr.main_colours(P)
    near = min(((cr.delta_e2000(c, pc) - cr.limit_for(k), cr.delta_e2000(c, pc), k, c, who) for k, c in main.items() for who, pc in (("P1", cr.PLAYER_GREEN), ("P2", cr.PLAYER_RED))), default=None)
    msg = f"[{label}] outfit colours keep Delta E >= {cr.PLAYER_DE_MIN:.0f}, skin and hair >= {cr.SKIN_HAIR_DE_MIN:.0f}, from both player colours"
    if near:
        msg += f" (tightest: {near[2]} {near[3]} is {near[1]:.1f} from {near[4]}, needs {cr.limit_for(near[2]):.0f})"
    if bad:
        msg += " " + "; ".join(f"{part} {col} is {d} from {who}" for part, col, who, d in bad)
    return line(not bad, msg)

def main(argv):
    ok = True
    if "--suggest" in argv:
        c = argv[argv.index("--suggest") + 1]
        print(f"{c}: Delta E {cr.delta_e2000(c, cr.PLAYER_GREEN):.1f} from P1 green, {cr.delta_e2000(c, cr.PLAYER_RED):.1f} from P2 red (outfit needs >= {cr.PLAYER_DE_MIN:.0f}, skin/hair >= {cr.SKIN_HAIR_DE_MIN:.0f})")
        return 0
    if "--self-test" in argv:
        for l1, l2, want in REF:
            got = cr.de2000_lab(l1, l2)
            ok &= line(abs(got - want) < 5e-4, f"Delta E 2000 reference pair {l1} / {l2}: {got:.4f} (published {want:.4f})")
        ok &= line(cr.delta_e2000(cr.PLAYER_GREEN, cr.PLAYER_GREEN) == 0.0, "a colour is 0 from itself")
        ok &= line(bool(cr.player_colour_clashes({"skin": "#3CC24A"})) and bool(cr.player_colour_clashes({"skin": "#41BD50"})), "P1 green and a near-P1 green skin are refused")
        ok &= line(bool(cr.player_colour_clashes({"outfit": {"top": {"color": "#E03A3A"}}})), "a near-P2 red top is refused")
        ok &= line(not cr.player_colour_clashes({"skin": "#D4F25A"}) and not cr.player_colour_clashes({"skin": "#A8F0D0"}) and not cr.player_colour_clashes({"skin": "#7C8A2E"}),
                   "lime #D4F25A, mint #A8F0D0 and olive #7C8A2E skins pass")
        ok &= line(not cr.player_colour_clashes({"skin": "#9FD6F0", "hair": {"color": "#8A5CC9"}, "headwear": {"color": "#A9B0B8"}}), "blue, purple and grey pass")
        ok &= line(not cr.player_colour_clashes({"skin": "#A0522D", "hair": {"color": "#A34E25"}}), "natural tones pass as skin and hair: sienna skin #A0522D, auburn hair #A34E25")
        ok &= line(bool(cr.player_colour_clashes({"outfit": {"top": {"color": "#A0522D"}}})) and bool(cr.player_colour_clashes({"headwear": {"color": "#A34E25"}})),
                   "the same two colours are refused as a main outfit colour (top, headwear)")
        ok &= line(bool(cr.player_colour_clashes({"skin": "#4FCB5C"})) and bool(cr.player_colour_clashes({"hair": {"color": "#DD4245"}})), "a neon-green skin near P1 and red hair near P2 are still refused")
        return 0 if ok else 1
    files = [a for a in argv if not a.startswith("--")]
    if files:
        for f in files:
            ok &= check_params(json.load(open(f)), f)
    else:
        idx = json.load(open(root / "characters.json"))
        for c in idx["characters"]:
            if c["playable"] and c.get("jarling_params"):
                ok &= check_params(json.load(open(root / c["jarling_params"])), c["id"])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
