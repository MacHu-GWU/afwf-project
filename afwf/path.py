# -*- coding: utf-8 -*-

"""
Frequently used paths.
"""

from pathlib import Path

dir_here = Path(__file__).absolute().parent
dir_lib = Path(dir_here.parent, "lib")

dir_home = Path.home()
dir_afwf = Path(dir_home, ".alfred-afwf")
p_last_error = Path(dir_afwf, "last-error.txt")
p_debug_log = Path(dir_afwf, "debug.txt")
