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
    from .api import Icon
    from .api import Text
    from .api import Item
    from .api import VarKeyEnum
    from .api import VarValueEnum
    from .api import ModEnum
    from .api import ScriptFilter
    from .api import Handler
    from .api import log_debug_info
    from .api import Workflow
    from .api import IconFileEnum
    from .api import Query
    from .api import QueryParser
except ImportError as e:  # pragma: no cover
    print(e)
