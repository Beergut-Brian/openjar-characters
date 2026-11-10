"""Gaits: cosmetic replacements for a standard Jarling's `run` and `idle` (params `"gait"`).

Gaits:  `hop` (Ribbit): `run` is a two-footed hop (crouch, push off, tucked in the air, land with
a squash); `idle` breathes and now and then settles and gives a small bounce.

Same action names, lengths and loop flags as the standard set (`run` 16 frames, `idle` 48 frames),
root stays at the origin in X/Y (vertical motion only: the game moves the character), `kick` and
`cheer` unchanged. Without `"gait"` nothing here runs.
"""
import jarling_kit as kit


def _base(B, extra=None):
    po = B.P.get("posture", {})
    sl, hl, ao = po.get("spine_lean", 0.0), po.get("head_lean", 0.0), po.get("arm_out", 0.0)
    p = {"spine": {"lean": sl}, "head": {"lean": hl}, "arm.L": {"out": ao + 4}, "arm.R": {"out": ao + 4}}
    for k, v in (extra or {}).items():
        cur = dict(p.get(k, {}))
        for kk, vv in v.items():
            cur[kk] = cur.get(kk, 0.0) + vv if not isinstance(vv, tuple) else vv
        p[k] = cur
    return p


def _both(d):
    """Same entry on both sides (two-footed: legs, feet and arms move together)."""
    out = {}
    for k, v in d.items():
        if k.endswith(".*"):
            out[k[:-2] + ".L"] = dict(v); out[k[:-2] + ".R"] = dict(v)
        else:
            out[k] = v
    return out


def hop_run(B):
    crouch = _both({"root": {"scale": (1.08, 1.08, 0.86)}, "spine": {"lean": 20}, "head": {"lean": -14},
                    "leg.*": {"swing": 8}, "foot.*": {"point": -10}, "arm.*": {"swing": -35, "out": 10}, "comb": {"lean": -12}})
    push = _both({"root": {"loc": (0, 0, 0.05), "scale": (0.95, 0.95, 1.08)}, "spine": {"lean": 6}, "head": {"lean": -6},
                  "leg.*": {"swing": -12}, "foot.*": {"point": 35}, "arm.*": {"swing": 40, "out": 18}, "comb": {"lean": 10}})
    top = _both({"root": {"loc": (0, 0, 0.14)}, "spine": {"lean": 10}, "head": {"lean": -8},
                 "leg.*": {"swing": 30}, "foot.*": {"point": 18}, "arm.*": {"swing": 20, "out": 32}, "comb": {"lean": 14}})
    fall = _both({"root": {"loc": (0, 0, 0.06), "scale": (0.98, 0.98, 1.03)}, "spine": {"lean": 8}, "head": {"lean": -6},
                  "leg.*": {"swing": 10}, "foot.*": {"point": -6}, "arm.*": {"swing": -5, "out": 24}, "comb": {"lean": -6}})
    land = _both({"root": {"scale": (1.1, 1.1, 0.84)}, "spine": {"lean": 22}, "head": {"lean": -16},
                  "leg.*": {"swing": 6}, "foot.*": {"point": -12}, "arm.*": {"swing": -25, "out": 20}, "comb": {"lean": -16}})
    return [(1, _base(B, crouch)), (4, _base(B, push)), (8, _base(B, top)), (12, _base(B, fall)),
            (14, _base(B, land)), (17, _base(B, crouch))]


def hop_idle(B):
    rest = _base(B, {"comb": {"tilt": 6}})
    breathe = _base(B, {"spine": {"scale": (1.02, 1.02, 1.03)}, "head": {"lean": -2.5, "scale": (0.98, 0.98, 0.97)},
                        "arm.L": {"out": 3}, "arm.R": {"out": 3}, "comb": {"tilt": -6}})
    settle = _base(B, _both({"root": {"scale": (1.06, 1.06, 0.91)}, "spine": {"lean": 8}, "head": {"lean": -6},
                             "foot.*": {"point": -6}, "arm.*": {"out": 6}, "comb": {"lean": -10}}))
    bounce = _base(B, _both({"root": {"loc": (0, 0, 0.03), "scale": (0.97, 0.97, 1.04)}, "head": {"lean": -3},
                             "foot.*": {"point": 14}, "arm.*": {"out": 10}, "comb": {"lean": 12}}))
    resettle = _base(B, {"root": {"scale": (1.03, 1.03, 0.95)}, "spine": {"lean": 4}, "comb": {"lean": -6}})
    return [(1, rest), (13, breathe), (25, rest), (31, settle), (35, bounce), (39, resettle), (44, rest), (49, rest)]


# gait name -> fn(builder) -> {action name: [(frame, pose), ...]} replacing those standard actions
kit.GAITS.update({"hop": lambda B: {"run": hop_run(B), "idle": hop_idle(B)}})
