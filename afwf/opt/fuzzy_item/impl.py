# -*- coding: utf-8 -*-

"""
Allow filtering / sorting Alfred Items by fuzzy matching.
"""

import typing as T
import attr
from ..fuzzy import Fuzzy
from ...item import Item as Item_


FUZZY_MATCH_NAME_VAR_KEY = "fuzzy_match_name"


@attr.define
class Item(Item_):
    def set_fuzzy_match_name(self, name: str) -> "Item":
        """
        Store the string of name in the alfred item variables. it is used for
        fuzzy matching and sorting.
        """
        self.variables[FUZZY_MATCH_NAME_VAR_KEY] = name
        return self

    @property
    def fuzzy_match_name(self) -> T.Optional[str]:
        return self.variables.get(FUZZY_MATCH_NAME_VAR_KEY)


class FuzzyItem(Fuzzy[Item]):
    def get_name(self, item: Item) -> T.Optional[str]:
        return item.variables.get(FUZZY_MATCH_NAME_VAR_KEY)
