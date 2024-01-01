# -*- coding: utf-8 -*-

import sys

if sys.version_info.minor < 8:
    from cached_property import cached_property
else:
    from functools import cached_property