# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from afwf.opt.fuzzy.impl import FuzzyMatcher


@dataclasses.dataclass
class Item:
    id: int
    name: str

    def special_method(self):
        pass


class FuzzyItemMatcher(FuzzyMatcher[Item]):
    def get_name(self, item: Item) -> T.Optional[str]:
        return item.name


class TestFuzzy:
    def test(self):
        # --- prepare data
        item1 = Item(id=1, name="apple and banana and cherry")
        item2 = Item(id=2, name="alice and bob and charlie")
        items = [item1, item2]
        item_mapper = {item1.name: [item1], item2.name: [item2]}

        # --- match
        fuzzy = FuzzyItemMatcher.from_items(items)
        assert fuzzy.match("apple", threshold=0)[0].id == 1
        assert fuzzy.match("banana", threshold=0)[0].id == 1
        assert fuzzy.match("cherry", threshold=0)[0].id == 1
        assert fuzzy.match("alice", threshold=0)[0].id == 2
        assert fuzzy.match("bob", threshold=0)[0].id == 2
        assert fuzzy.match("charlie", threshold=0)[0].id == 2
        assert len(fuzzy.match("2e8de47b8d5981a06a3f71c06e51a841", threshold=70)) == 0

        # type hint auto complete test
        fuzzy = FuzzyItemMatcher.from_mapper(item_mapper)
        results = fuzzy.match("apple", threshold=0)
        results[0].special_method()  # type hint should work here

        # edge case
        fuzzy = FuzzyItemMatcher.from_mapper({})
        assert len(fuzzy.match("hello")) == 0


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.opt.fuzzy.impl", preview=False)
