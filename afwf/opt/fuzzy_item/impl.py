# -*- coding: utf-8 -*-

"""
Allow filtering / sorting Alfred Items by fuzzy matching.

Requirements::

    rapidfuzz>=3.0.0,<4.0.0
"""

try:
    from typing import Self
except ImportError:  # python < 3.11
    from typing_extensions import Self

from ..fuzzy.api import FuzzyMatcher
from ...item import Item as Item_


FUZZY_MATCH_NAME_VAR_KEY = "fuzzy_match_name"


class Item(Item_):
    """
    Enhance the original :class:`~afwf.item.Item` class to allow fuzzy matching.

    The fuzzy match name is stored in ``variables[FUZZY_MATCH_NAME_VAR_KEY]`` so
    it travels with the item through Alfred's variable inheritance mechanism.

    Example::

        item = Item(title="Alfred Handler")
        item.set_fuzzy_match_name("Alfred Handler")
        # item.fuzzy_match_name == "Alfred Handler"
    """

    def set_fuzzy_match_name(self, name: str) -> Self:
        """
        Store *name* in the item's variables for later fuzzy matching.
        """
        self.variables[FUZZY_MATCH_NAME_VAR_KEY] = name
        return self

    @property
    def fuzzy_match_name(self) -> str | None:
        """
        Return the name stored for fuzzy matching, or ``None`` if not set.
        """
        return self.variables.get(FUZZY_MATCH_NAME_VAR_KEY)


class FuzzyItemMatcher(FuzzyMatcher[Item]):
    """
    Fuzzy matcher for :class:`Item`.
    """

    def get_name(self, item: Item) -> str | None:
        """
        Return the fuzzy-match name stored on *item*.
        """
        return item.variables.get(FUZZY_MATCH_NAME_VAR_KEY)
