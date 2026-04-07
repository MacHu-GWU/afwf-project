# -*- coding: utf-8 -*-

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

    def test_set_modifier_invalid_key(self):
        # invalid modifier key must raise ValueError
        item = Item(title="hello")
        try:
            item.set_modifier(mod="invalid_key")
            assert False, "expected ValueError"
        except ValueError:
            pass

    def test_set_modifier_output(self):
        # modifier appears correctly in to_script_filter output
        item = Item(title="hello")
        item.set_modifier(mod=ModEnum.cmd, subtitle="alt subtitle", arg="alt_arg")
        sf = item.to_script_filter()
        assert sf["mods"] == {"cmd": {"subtitle": "alt subtitle", "arg": "alt_arg", "valid": True}}

    def test_set_variable_method(self):
        # representative set_* method: variables are set correctly
        item = Item(title="hello")
        item.open_file(path="/tmp/file.txt")
        assert item.variables["open_file"] == "y"
        assert item.variables["open_file_path"] == "/tmp/file.txt"

    def test_run_script_sets_arg(self):
        # run_script and terminal_command also set self.arg (unlike other set_* methods)
        item = Item(title="hello")
        item.run_script(cmd="python3 /tmp/script.py")
        assert item.arg == "python3 /tmp/script.py"
        assert item.variables["run_script"] == "y"

        item2 = Item(title="hello")
        item2.terminal_command(cmd="echo hello")
        assert item2.arg == "echo hello"
        assert item2.variables["terminal_command"] == "y"


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.item",
        preview=False,
    )
