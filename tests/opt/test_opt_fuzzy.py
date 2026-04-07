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

    def test_get_name_returns_none(self):
        # items whose get_name() returns None are silently skipped
        class NullableMatcher(FuzzyMatcher[Item]):
            def get_name(self, item: Item) -> T.Optional[str]:
                return None if item.id == 99 else item.name

        item_skip = Item(id=99, name="should be ignored")
        item_keep = Item(id=1, name="apple and banana")
        fuzzy = NullableMatcher.from_items([item_skip, item_keep])
        assert 99 not in [i.id for i in fuzzy.match("apple", threshold=0)]
        assert fuzzy.match("apple", threshold=0)[0].id == 1

    def test_threshold_filtering(self):
        # items below threshold are excluded; only high-score matches survive
        item1 = Item(id=1, name="apple")
        item2 = Item(id=2, name="zzzzz")
        fuzzy = FuzzyItemMatcher.from_items([item1, item2])
        results = fuzzy.match("apple", threshold=80)
        ids = [i.id for i in results]
        assert 1 in ids
        assert 2 not in ids

    def test_limit(self):
        # limit caps the number of returned items
        items = [Item(id=i, name=f"item {i}") for i in range(10)]
        fuzzy = FuzzyItemMatcher.from_items(items)
        assert len(fuzzy.match("item", threshold=0, limit=3)) <= 3

    def test_filter_func(self):
        # filter_func can exclude matches that would otherwise pass threshold
        item1 = Item(id=1, name="apple and banana")
        item2 = Item(id=2, name="apple and cherry")
        fuzzy = FuzzyItemMatcher.from_items([item1, item2])
        results = fuzzy.match(
            "apple",
            threshold=0,
            filter_func=lambda t: "banana" in t[0],
        )
        assert all(i.id == 1 for i in results)

    def test_duplicate_names(self):
        # multiple items sharing the same name are all returned
        item_a = Item(id=1, name="apple")
        item_b = Item(id=2, name="apple")
        fuzzy = FuzzyItemMatcher.from_items([item_a, item_b])
        results = fuzzy.match("apple", threshold=0)
        assert {i.id for i in results} == {1, 2}


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.opt.fuzzy.impl",
        preview=False,
    )
