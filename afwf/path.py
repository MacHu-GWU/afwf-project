# -*- coding: utf-8 -*-

from pathlib_mate import Path

dir_home = Path.home()
dir_afwf = Path(dir_home, ".alfred-afwf")
p_last_error = Path(dir_afwf, "last-error.txt")
p_debug_log = Path(dir_afwf, "debug.txt")
