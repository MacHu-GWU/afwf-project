# -*- coding: utf-8 -*-

from pathlib_mate import Path

dir_here = Path(__file__).absolute().parent
dir_icons = Path(dir_here, "icons")
p_icon = Path(dir_here, "icon.py")

content = """
# -*- coding: utf-8 -*-

import os

dir_here = os.path.dirname(os.path.abspath(__file__))

class Icon:
""".strip()
lines = content.split("\n")

for p in dir_icons.select_file():
    name = p.basename.split("-")[0]
    file = p.basename
    line = f"    {name} = os.path.join(dir_here, \"{file}\")"
    lines.append(line)

lines.append("")

p_icon.write_text("\n".join(lines))
