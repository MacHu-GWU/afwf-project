# -*- coding: utf-8 -*-

"""
Alfred Workflow Script Filter power tool.
"""

from ._version import __version__

__short_description__ = "A powerful framework enables fast and elegant development of Alfred Workflows in Python."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = __author__
__maintainer_email__ = __author_email__
__github_username__ = "MacHu-GWU"

try:
    from .item import (
        Icon,
        Text,
        Item,
        VarKeyEnum,
        VarValueEnum,
        ModEnum,
    )
    from .script_filter import ScriptFilter
    from .handler import Handler
    from .workflow import log_debug_info
    from .workflow import Workflow
    from .icon import IconFileEnum
    from .query import Query
    from .query import QueryParser
except ImportError as e: # pragma: no cover
    print(e)
