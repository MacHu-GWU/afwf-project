# -*- coding: utf-8 -*-

"""
Run this script to generate ``icon.py`` file.

Do this if you update the ``icons`` folder.
"""

from pathlib_mate import Path

dir_here = Path(__file__).absolute().parent
dir_icons = Path(dir_here, "icons")
p_icon = Path(dir_here, "icon.py")

content = """
# -*- coding: utf-8 -*-

\"\"\"
Enumerate all built-in ICON images.
\"\"\"

import os

dir_icons = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

class IconFileEnum:
""".strip()
lines = content.split("\n")

for p in dir_icons.select_by_ext(".png"):
    name = p.basename.split("-")[0]
    file = p.basename
    line = f"    {name} = os.path.join(dir_icons, \"{file}\")"
    lines.append(line)

lines.append("")

p_icon.write_text("\n".join(lines))
