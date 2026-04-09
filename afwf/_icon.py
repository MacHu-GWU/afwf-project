# -*- coding: utf-8 -*-

"""
Run this script to generate ``icon.py`` file.

Do this if you update the ``icons`` folder.
"""

from pathlib import Path

dir_here = Path(__file__).absolute().parent
dir_icons = dir_here / "icons"
p_icon = dir_here / "icon.py"

content = """
# -*- coding: utf-8 -*-

\"\"\"
Enumerate all built-in ICON images.
\"\"\"

import os

dir_icons = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

class IconFileEnum:
    \"\"\"
    List of built-in icon files.
    \"\"\"
""".strip()
lines = content.split("\n")

for p in sorted(dir_icons.glob("*.png")):
    name = p.name[:-7].replace("-", "_")
    file = p.name
    line = f"    {name} = os.path.join(dir_icons, \"{file}\")"
    lines.append(line)

lines.append("")

p_icon.write_text("\n".join(lines))
