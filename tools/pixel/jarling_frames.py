"""Shared rules for the playable Jarlings' pixel forms (The Hill). Pillow only.

A playable character's pixel form lives in `tools/pixel/<id>.py`:
  <id>()            the front form, native size on a 40 x 32 canvas, feet on the bottom row, 1 px outline
                    (what `characters.json` `pixel.function` names and a game's sync script vendors)
  frame(name)       one unoutlined 32 x 32 frame facing right, feet centre at the pivot (16, 32), for
                    idle0 idle1 walk0..walk3 jump fall side0..side2 down0..down2 (`eyes_shut=True` for sleep)
  sheet()           the 128 x 224 sheet in The Hill's player layout (jarling_frames.sheet(frame))
Scale: The Hill draws 1.2 m (Jeff with his comb) 32 px tall, so a figure is round(metres * 32 / 1.2) px
tall, traced from `refs/jarling/<id>_side_sprite.png`; nothing may be taller than 32 px (the frame).
Outline `px.OUT` (#2A1E2C), flat colours from the character's look.md, no anti-aliasing.
"""
from PIL import Image
from px import outline, OUT

W, H = 40, 32            # front form canvas, same as residents.py
FW, FH = 32, 32          # one frame of The Hill's player sheet; pivot (16, 32)
PX_PER_M = 32 / 1.2
ROWS = [("idle", ["idle0", "idle1"], 2), ("walk", ["walk0", "walk1", "walk2", "walk3"], 8),
        ("air", ["jump", "fall"], 0), ("dig_side", ["side0", "side1", "side2"], 10),
        ("dig_down", ["down0", "down1", "down2"], 10), ("ride", ["ride"], 0), ("sleep", ["sleep0", "sleep1"], 2)]
FRAMES = [f for _, fs, _ in ROWS for f in fs if f != "ride" and not f.startswith("sleep")]
CLEAR = (0, 0, 0, 0)


def px_tall(metres):
    return min(FH, round(metres * PX_PER_M))


def fin(im, w=W, h=H):
    """Outline a drawn figure and stand it on the bottom row of a w x h canvas (x kept as drawn)."""
    im = outline(im.im if hasattr(im, "im") else im)
    bb = im.getbbox()
    assert bb and bb[3] - bb[1] <= h and bb[0] >= 0 and bb[2] <= w, f"figure {bb} does not fit {w}x{h}"
    out = Image.new("RGBA", (w, h), CLEAR)
    out.paste(im.crop((0, bb[1], w, bb[3])), (0, h - (bb[3] - bb[1])))
    return out


def sheet(frame):
    """128 x 224: rows idle(2) walk(4) air(jump, fall) dig_side(3) dig_down(3) ride(1) sleep(2), as The Hill's players.
    `frame(name, eyes_shut=False)` returns an unoutlined 32 x 32 RGBA frame with a clear 1 px border.
    ride = the top 14 rows of the idle figure at the frame top (the vehicle hides the rest);
    sleep = the idle figure lying down, head to the right, eyes shut; sleep1 lifts the chest 1 px."""
    out = Image.new("RGBA", (4 * FW, len(ROWS) * FH), CLEAR)
    for ri, (_, names, _) in enumerate(ROWS):
        for fi, n in enumerate(names):
            if n == "ride":
                body = frame("idle0"); top = body.getbbox()[1]
                im = Image.new("RGBA", (FW, FH), CLEAR)
                im.alpha_composite(body.crop((0, top, FW, top + 14)), (0, 1))
            elif n.startswith("sleep"):
                body = frame("idle0", eyes_shut=True)
                lying = body.rotate(-90, expand=True); lying = lying.crop(lying.getbbox())
                im = Image.new("RGBA", (FW, FH), CLEAR)
                im.alpha_composite(lying, ((FW - lying.width) // 2, FH - 1 - lying.height - (1 if n == "sleep1" else 0)))
                if n == "sleep1":      # breathing: the whole figure rises 1 px, a ground row keeps the feet line
                    im.alpha_composite(lying.crop((0, lying.height - 1, lying.width, lying.height)), ((FW - lying.width) // 2, FH - 2))
            else:
                im = frame(n)
            assert im.size == (FW, FH), n
            im = outline(im)
            out.alpha_composite(im, (fi * FW, ri * FH))
    return out


def manifest(hand=(23, 22)):
    rows = {name: {"row": i, "frames": len(fs), "fps": fps} for i, (name, fs, fps) in enumerate(ROWS)}
    rows["air"]["names"] = ["jump", "fall"]
    return {"frame": [FW, FH], "pivot": [16, 32], "facing": "right", "hand": list(hand), "rows": rows}
