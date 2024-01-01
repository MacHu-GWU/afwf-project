# -*- coding: utf-8 -*-

"""
Allow filtering / sorting Alfred Items by fuzzy matching.

Requirements::

    fuzzywuzzy>=0.18.0,<1.0.0
"""

import typing as T
import attr

from ..fuzzy.api import FuzzyMatcher
from ...item import Item as Item_


FUZZY_MATCH_NAME_VAR_KEY = "fuzzy_match_name"


@attr.define
class Item(Item_):
    """
    Enhance the original :class:`alfred.item.Item` class to allow fuzzy matching.
    """

    def set_fuzzy_match_name(self, name: str) -> "Item":
        """
        Store the string of name in the alfred item variables. it is used for
        fuzzy matching and sorting.
        """
        self.variables[FUZZY_MATCH_NAME_VAR_KEY] = name
        return self

    @property
    def fuzzy_match_name(self) -> T.Optional[str]:
        """
        Get the string for fuzzy matching.
        """
        return self.variables.get(FUZZY_MATCH_NAME_VAR_KEY)


class FuzzyItemMatcher(FuzzyMatcher[Item]):
    """
    Fuzzy matcher for :class:`Item`.
    """

    def get_name(self, item: Item) -> T.Optional[str]:
        """
        Given an item, return the name of the item for fuzzy match.
        """
        return item.variables.get(FUZZY_MATCH_NAME_VAR_KEY)
