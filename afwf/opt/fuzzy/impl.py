# -*- coding: utf-8 -*-

"""
Allow filtering / sorting by fuzzy matching.

Requirements::

    fuzzywuzzy>=0.18.0,<1.0.0
"""

import typing as T
import dataclasses
import warnings

with warnings.catch_warnings():  # pragma: no cover
    warnings.simplefilter("ignore")
    try:
        from fuzzywuzzy import process

        has_fuzzywuzzy = True
    except ImportError as e:
        error = e
        has_fuzzywuzzy = False

if has_fuzzywuzzy is False:  # pragma: no cover
    warnings.warn("you have to install 'fuzzywuzzy' to use 'afwf.opt.fuzzy' feature!")
    raise error


T_ITEM = T.TypeVar("T_ITEM")


@dataclasses.dataclass
class FuzzyMatcher(T.Generic[T_ITEM]):
    """
    Fuzzywuzzy is awesome to match string. However, what if the item is not string?

    We can define a **name** for each item and use fuzzywuzzy to match the **name**.
    Then use the name to locate the original item. This class implements this pattern.

    :param _items: list of item you want to match
    :param _names: list of str of item name
    :param _mapper: the key is the name of the item, the value is the
        list of item that with the same name.

    You have to subclass this class and **implement the**
    :meth:`FuzzyMatcher.get_name` **method**. See doc string for more information.

    Don't directly use the constructor, use the ``from_items`` or ``from_mapper``
    factory method instead.

    Usage Example::

        @dataclasses.dataclass
        class Item:
            id: int
            name: str


        class ItemFuzzyMatcher(FuzzyMatcher[Item]):
            def get_name(self, item: Item) -> T.Optional[str]:
                return item.name

        items = [
            Item(id=1, name="apple and banana and cherry"),
            Item(id=2, name="alice and bob and charlie"),
        ]

        matcher = ItemFuzzyMatcher.from_items(items)
        result = matcher.match("apple", threshold=0)
        print(result)
    """

    _items: T.List[T_ITEM] = dataclasses.field(default_factory=list)
    _names: T.List[str] = dataclasses.field(default_factory=list)
    _mapper: T.Dict[str, T.List[T_ITEM]] = dataclasses.field(default_factory=dict)

    def get_name(self, item: T_ITEM) -> T.Optional[str]:  # pragma: no cover
        """
        Given an item, return the name of the item for fuzzy match.

        This method should not raise any error and always return a string or None.
        If return None, the item will be ignored (not shown in result).
        """
        raise NotImplementedError

    def _build_mapper(self):
        if self._mapper:
            self._names = list(self._mapper)
        else:
            for item in self._items:
                name = self.get_name(item)
                if name is not None:
                    self._names.append(name)
                    try:
                        self._mapper[name].append(item)
                    except:
                        self._mapper[name] = [item]

    def __post_init__(self):
        self._build_mapper()

    @classmethod
    def from_items(cls, items: T.List[T_ITEM]):
        """
        Build a FuzzyMatcher from a list of items.
        """
        return cls(_items=items)

    @classmethod
    def from_mapper(cls, name_to_item_mapper: T.Dict[str, T.List[T_ITEM]]):
        """
        Build a FuzzyMatcher from a mapper, the key should be the name of the item
        for fuzzy match.
        """
        return cls(_mapper=name_to_item_mapper)

    def match(
        self,
        name: str,
        threshold: int = 70,
        limit: int = 20,
        filter_func: T.Callable = lambda x: True,
    ) -> T.List[T_ITEM]:
        """
        Match items by name. Only return items that similarity score is greater than
        the threshold. It also uses a callable filter function to filter the result.
        The results will be sorted by the similarity score, from high to low.

        :param name: name is the search string for fuzzy match
        :param threshold: the minimal similarity score (0-100) to be considered as matched
        :param limit: the max number of matched items to return
        :param filter_func: additional filter function to filter the matched items
            it has to be a function that accept an item and return a bool
        """
        matched_name_list = process.extractBests(name, self._names, limit=limit)
        if len(matched_name_list) == 0:
            return []
        matched_name_list = list(filter(filter_func, matched_name_list))
        best_matched_name, best_matched_score = matched_name_list[0]
        if best_matched_score >= threshold:
            matched_items = list()
            for matched_name, score in matched_name_list:
                if score >= threshold:
                    matched_items.extend(self._mapper[matched_name])
            return matched_items[:limit]
        else:
            return []
