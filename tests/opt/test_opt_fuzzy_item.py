# -*- coding: utf-8 -*-

from afwf.opt.fuzzy_item import Item, FuzzyItem


class TestFuzzyItem:
    def test(self):
        items = [
            Item(title="1").set_fuzzy_match_name("apple and banana and cherry"),
            Item(title="2").set_fuzzy_match_name("alice and bob and charlie"),
        ]

        fuzzy = FuzzyItem.from_items(items)
        res = fuzzy.match(name="bob")
        assert len(res) == 1
        assert res[0].title == "2"

        res = fuzzy.match(name="this is invalid", threshold=95)
        assert len(res) == 0

        fuzzy = FuzzyItem.from_mapper({item.fuzzy_match_name: [item,] for item in items})
        res = fuzzy.sort(name="bob")
        assert len(res) == 2
        assert res[0].title == "2"
        assert res[1].title == "1"


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.opt.fuzzy_item", preview=False)
