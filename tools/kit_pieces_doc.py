#!/usr/bin/env python3
"""Regenerate the piece tables in docs/kit-v2.md from the kit plug-ins' module docstrings.

    python3 tools/kit_pieces_doc.py        (run from the repo root; no Blender needed)

Each `avatar/kit/pieces_*.py` docstring lists its pieces as `  name   params...` lines under a
heading line ending in ":"; this turns them into tables between the PIECES markers.
"""
import ast, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
out = []
for f in ("pieces_features.py", "pieces_headwear.py", "pieces_outfit.py", "pieces_hill.py"):
    doc = ast.get_docstring(ast.parse((root / "avatar" / "kit" / f).read_text())) or ""
    out.append(f"### `avatar/kit/{f}`\n")
    table = False
    for line in doc.splitlines():
        m = re.match(r"^  ([a-z_0-9]+)\s{2,}(.*)$", line)
        cont = re.match(r"^\s{6,}(\S.*)$", line)
        if m:
            if not table:
                out.append("| Name | Params (defaults) |\n| --- | --- |")
                table = True
            out.append(f"| `{m.group(1)}` | {m.group(2).replace('|', '/')} |")
        elif cont and table:
            out[-1] = out[-1][:-2] + " " + cont.group(1).replace("|", "/") + " |"
        else:
            table = False
            if line.strip():
                # names listed inline (hill pieces, presets, mouths) get backticks so they are findable
                out.append("\n" + re.sub(r"`", "`", line.strip()) + "\n")
    out.append("")
p = root / "docs" / "kit-v2.md"
s = p.read_text()
a, b = "<!-- PIECES:START (tools/kit_pieces_doc.py) -->", "<!-- PIECES:END -->"
s = s[:s.index(a) + len(a)] + "\n" + "\n".join(out) + "\n" + s[s.index(b):]
p.write_text(s)
print("docs/kit-v2.md piece tables regenerated")
