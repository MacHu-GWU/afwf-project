# -*- coding: utf-8 -*-

import pytest
from rich import print as rprint
from afwf.item import Icon, Text, ModEnum, Item
from afwf.icon import IconFileEnum


class TestIcon:
    def test_init(self):
        icon = Icon(path="/tmp/log.txt", type=Icon.TypeEnum.filetype.value)
        assert icon.to_script_filter() == {"path": "/tmp/log.txt", "type": "filetype"}


class TestItem:
    def test_init(self):
        item = Item(title="hello", text=Text())
        assert item.to_script_filter() == {"title": "hello", "valid": True}

        item.set_icon(path=IconFileEnum.debug)
        item.set_modifier(mod=ModEnum.cmd.value)
        item.open_file(path=IconFileEnum.debug)
        item.launch_app_or_file(path=IconFileEnum.debug)
        item.reveal_file_in_finder(path=IconFileEnum.debug)
        item.browse_in_terminal(path=IconFileEnum.debug)
        item.browse_in_alfred(path=IconFileEnum.debug)
        item.open_url(url="https://www.google.com")
        item.run_script(cmd="/path/to/script.py")
        item.terminal_command(cmd="echo hello")
        item.send_notification(title="hello")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
