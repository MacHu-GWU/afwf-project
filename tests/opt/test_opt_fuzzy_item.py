# -*- coding: utf-8 -*-

from afwf.opt.fuzzy_item.impl import Item, FuzzyItemMatcher


class TestFuzzyItemMatcher:
    def test(self):
        items = [
            Item(title="1").set_fuzzy_match_name("apple and banana and cherry"),
            Item(title="2").set_fuzzy_match_name("alice and bob and charlie"),
        ]

        fuzzy = FuzzyItemMatcher.from_items(items)
        res = fuzzy.match(name="alice bob")
        assert len(res) == 1
        assert res[0].title == "2"

        res = fuzzy.match(name="this is invalid", threshold=95)
        assert len(res) == 0


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.opt.fuzzy_item.impl", preview=False)
