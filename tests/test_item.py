# -*- coding: utf-8 -*-

import pytest
from rich import print as rprint
from afwf.item import Icon, Text, Item


class TestIcon:
    def test_init(self):
        icon = Icon(path="/tmp/log.txt", type=Icon.TypeEnum.filetype.value)
        assert icon.to_script_filter() == {"path": "/tmp/log.txt", "type": "filetype"}


class TestItem:
    def test_init(self):
        item = Item(title="hello", text=Text())
        assert item.to_script_filter() == {"title": "hello", "valid": True}


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
