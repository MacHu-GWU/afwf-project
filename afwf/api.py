# -*- coding: utf-8 -*-

"""
Usage::

    import afwf.api as afwf
"""

from .item import Icon
from .item import Text
from .item import Item
from .item import VarKeyEnum
from .item import VarValueEnum
from .item import ModEnum
from .script_filter import ScriptFilter
from .handler import Handler
from .workflow import log_debug_info
from .workflow import Workflow
from .icon import IconFileEnum
from .query import Query
from .query import QueryParser

try:
    from .opt.cache.api import TypedCache
except ImportError:  # pragma: no cover
    pass

try:
    from .opt.fuzzy.api import FuzzyMatcher
except ImportError:  # pragma: no cover
    pass

try:
    from .opt.fuzzy_item.api import Item as FuzzyItem
    from .opt.fuzzy_item.api import FuzzyItemMatcher
except ImportError:  # pragma: no cover
    pass
