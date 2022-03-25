# -*- coding: utf-8 -*-

import json
from typing import Any, Type, Union, List, Tuple, Dict

import attr
from attr import validators as vs
from attrs_mate import AttrsClass

from .enumeration import BetterEnum
from .script_filter_object import ScriptFilterObject


@attr.define
class Icon(ScriptFilterObject):
    """
    """
    class TypeEnum(BetterEnum):
        fileicon = "fileicon"
        filetype = "filetype"

    path: str = AttrsClass.ib_str()
    type: str = attr.field(
        validator=vs.optional(vs.in_(TypeEnum.to_values())),
        default=None,
    )


class VarKeyEnum(BetterEnum):
    open_file = "open_file"
    open_file_path = "open_file_path"
    launch_app_or_file = "launch_app_or_file"
    launch_app_or_file_path = "launch_app_or_file_path"
    reveal_file_in_finder = "reveal_file_in_finder"
    reveal_file_in_finder_path = "reveal_file_in_finder_path"
    browse_in_terminal = "browse_in_terminal"
    browse_in_terminal_path = "browse_in_terminal_path"
    browse_in_alfred = "browse_in_alfred"
    browse_in_alfred_path = "browse_in_alfred_path"
    action_in_alfred = "action_in_alfred"
    file_buffer = "file_buffer"
    default_web_search = "default_web_search"
    open_url = "open_url"
    open_url_arg = "open_url_arg"
    system_command = "system_command"
    itunes_command = "itunes_command"
    run_script = "run_script"
    run_script_arg = "run_script_arg"
    run_ns_apple_script = "run_ns_apple_script"
    run_ns_apple_script_arg = "run_ns_apple_script_arg"
    terminal_command = "terminal_command"
    terminal_command_arg = "terminal_command_arg"


class VarValueEnum(BetterEnum):
    y = "y"
    n = "n"


@attr.define
class Text(ScriptFilterObject):
    copy: str = AttrsClass.ib_str(default=None)
    largetype: str = AttrsClass.ib_str(default=None)


class ModEnum(BetterEnum):
    cmd = "cmd"
    shift = "shift"
    alt = "alt"
    ctrl = "ctrl"
    fn = "fn"


@attr.define
class Item(ScriptFilterObject):
    """
    Ref: https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    class TypeEnum(BetterEnum):
        file = "file"
        file_skipcheck = "file:skipcheck"

    title: str = AttrsClass.ib_str()
    subtitle: str = AttrsClass.ib_str(default=None)
    arg: str = AttrsClass.ib_str(default=None)
    autocomplete: str = AttrsClass.ib_str(default=None)
    icon: Icon = Icon.ib_nested(default=None)
    valid: bool = AttrsClass.ib_bool(default=True)
    uid: str = AttrsClass.ib_str(default=None)
    match: str = AttrsClass.ib_str(default=None)
    type: str = attr.field(
        validator=vs.optional(vs.in_(TypeEnum.to_values())),
        default=None,
    )
    mods: dict = AttrsClass.ib_dict(default=None)
    action: Union[str, List[str], Dict[str, Any]] = attr.ib(default=None)
    text: Text = Text.ib_nested(default=None)
    quicklookurl: str = AttrsClass.ib_str(default=None)
    variables: dict = AttrsClass.ib_dict(default=None)

    def open_file(self, path: str):
        self.variables[VarKeyEnum.open_file] = VarValueEnum.y
        self.variables[VarKeyEnum.open_file_path] = path

    def launch_app_or_file(self, path: str):
        self.variables[VarKeyEnum.launch_app_or_file] = VarValueEnum.y
        self.variables[VarKeyEnum.launch_app_or_file_path] = path

    def reveal_file_in_finder(self, path: str):
        self.variables[VarKeyEnum.reveal_file_in_finder] = VarValueEnum.y
        self.variables[VarKeyEnum.reveal_file_in_finder_path] = path

    def browse_in_terminal(self, path: str):
        self.variables[VarKeyEnum.browse_in_terminal] = VarValueEnum.y
        self.variables[VarKeyEnum.browse_in_terminal_path] = path

    def browse_in_alfred(self, path: str):
        self.variables[VarKeyEnum.browse_in_alfred] = VarValueEnum.y
        self.variables[VarKeyEnum.browse_in_alfred_path] = path

    def open_url(self, path: str):
        self.variables[VarKeyEnum.open_url] = VarValueEnum.y
        self.variables[VarKeyEnum.open_url_arg] = path

    def run_script(self, path: str):
        self.variables[VarKeyEnum.run_script] = VarValueEnum.y
        self.variables[VarKeyEnum.run_script_arg] = path

    def terminal_command(self, path: str):
        self.variables[VarKeyEnum.terminal_command] = VarValueEnum.y
        self.variables[VarKeyEnum.terminal_command_arg] = path

    def add_modifier(
        self,
        mod: str,
        subtitle: subtitle = None,
        arg: str = None,
        valid: bool = True,
    ):
        if mod not in ModEnum.to_values():
            raise ValueError
        dct = {
            k: v
            for k, v in dict(
                subtitle=subtitle,
                arg=arg,
                valid=valid,
            ).items()
            if v
        }
        if self.mods is None:
            self.mods = dict()
        self.mods[mod] = dct
