# -*- coding: utf-8 -*-

from diskcache import Cache
from pathlib_mate import Path

dir_home = Path.home()
dir_afwf = Path(dir_home, ".alfred-afwf")
dir_cache = Path(dir_afwf, ".cache")

dir_afwf.mkdir_if_not_exists()

cache = Cache(dir_cache.abspath)
