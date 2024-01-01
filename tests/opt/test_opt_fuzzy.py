# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from afwf.opt.fuzzy.impl import Fuzzy


@dataclasses.dataclass
class Item:
    id: int
    name: str


class FuzzyItem(Fuzzy[Item]):
    def get_name(self, item: Item) -> T.Optional[str]:
        return item.name


class TestFuzzy:
    def test(self):
        # --- prepare data
        items = [
            Item(id=1, name="apple and banana and cherry"),
            Item(id=2, name="alice and bob and charlie"),
        ]
        fuzzy = FuzzyItem.from_items(items)

        # --- match
        assert fuzzy.match("apple", threshold=0)[0].id == 1
        assert fuzzy.match("banana", threshold=0)[0].id == 1
        assert fuzzy.match("cherry", threshold=0)[0].id == 1
        assert fuzzy.match("alice", threshold=0)[0].id == 2
        assert fuzzy.match("bob", threshold=0)[0].id == 2
        assert fuzzy.match("charlie", threshold=0)[0].id == 2

        # type hint auto complete test
        results = fuzzy.match("apple", threshold=0)
        assert len(results) == 1

        # --- sort
        assert fuzzy.sort("apple", threshold=0)[0].id == 1
        assert fuzzy.sort("banana", threshold=0)[0].id == 1
        assert fuzzy.sort("cherry", threshold=0)[0].id == 1
        assert fuzzy.sort("alice", threshold=0)[0].id == 2
        assert fuzzy.sort("bob", threshold=0)[0].id == 2
        assert fuzzy.sort("charlie", threshold=0)[0].id == 2

        results = fuzzy.sort("bob", threshold=0)
        assert len(results) == 2


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.opt.fuzzy", preview=False)
