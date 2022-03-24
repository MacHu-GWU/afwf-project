# -*- coding: utf-8 -*-

import pytest
from rich import print as rprint
from afwf.item import Icon, Text, Item


class TestItem:
    def test_init(self):
        item = Item(title="hello", text=Text())
        rprint(item.to_script_filter())


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
