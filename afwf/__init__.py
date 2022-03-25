# -*- coding: utf-8 -*-

"""
Alfred Workflow Script Filter power tool.
"""

from ._version import __version__

__short_description__ = "Alfred Workflow Script Filter power tool.."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
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
    from .workflow import Workflow
except ImportError as e:
    print(e)
