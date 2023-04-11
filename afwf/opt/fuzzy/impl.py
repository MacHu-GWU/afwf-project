# -*- coding: utf-8 -*-

"""
Allow filtering / sorting by fuzzy matching.
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


ITEM = T.TypeVar("ITEM")


@dataclasses.dataclass
class Fuzzy(T.Generic[ITEM]):
    """
    Fuzzywuzzy is awesome to match string. However, what if the item is not string?

    We can define a name for each item and use fuzzywuzzy to match the name.
    Then use the name to locate the original item. This class implements this pattern.

    :param _items: list of item you want to match
    :param _names: list of str of item name
    :param _mapper: the key is the name of the item, the value is the
        list of item that with the same name.

    You have to subclass this class and implement the :meth:`Fuzzy.get_name`
     method. See doc string for more information.

    Don't directly use the constructor, use the ``from_items`` or ``from_mapper``
    factory method instead.
    """

    _items: T.List[ITEM] = dataclasses.field(default_factory=list)
    _names: T.List[str] = dataclasses.field(default_factory=list)
    _mapper: T.Dict[str, T.List[ITEM]] = dataclasses.field(default_factory=dict)

    def get_name(self, item: ITEM) -> T.Optional[str]:
        """
        Given an item, return the item of the entity for fuzzy match.

        This method should not raise any error and always return a string or None.
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
    def from_items(cls, items: T.List[ITEM]):
        return cls(_items=items)

    @classmethod
    def from_mapper(cls, name_to_item_mapper: T.Dict[str, T.List[ITEM]]):
        return cls(_mapper=name_to_item_mapper)

    def match(
        self,
        name: str,
        threshold: int = 0,
    ) -> T.List[ITEM]:
        """
        Find the best matched list of items. Only highest score is returned.
        """
        tp = process.extractOne(
            query=name,
            choices=self._names,
            score_cutoff=threshold,
        )
        if tp is None:
            return []
        else:
            return self._mapper[tp[0]]

    def sort(
        self,
        name: str,
        threshold: int = 0,
        limit: int = 20,
    ) -> T.List[ITEM]:
        """
        Sort items by the match score.
        """
        matched_name_list = process.extractBests(
            query=name,
            choices=self._names,
            score_cutoff=threshold,
            limit=limit,
        )
        results = list()
        for matched_name, matched_score in matched_name_list:
            results.extend(self._mapper[matched_name])
        return results
