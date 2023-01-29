# -*- coding: utf-8 -*-

from typing import Any, Union, List, Dict

import attr
from attr import validators as vs
from attrs_mate import AttrsClass

from .enumeration import BetterEnum
from .script_filter_object import ScriptFilterObject


@attr.define
class Icon(ScriptFilterObject):
    """ """

    class TypeEnum(BetterEnum):
        fileicon = "fileicon"
        filetype = "filetype"

    path: str = AttrsClass.ib_str()
    type: str = attr.field(
        validator=vs.optional(vs.in_(TypeEnum.to_values())),
        default=None,
    )

    @classmethod
    def from_image_file(cls, path: str) -> "Icon":
        """
        Create an Icon object that using a file on local file system as an icon.
        """
        return cls(path=path)


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
    send_notification = "send_notification"
    send_notification_title = "send_notification_title"
    send_notification_subtitle = "send_notification_subtitle"

    _open_log_file = "_open_log_file"
    _open_log_file_path = "_open_log_file_path"


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
    Data model for alfred dropdown menu items.

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
    variables: dict = AttrsClass.ib_dict(factory=dict)

    # --------------------------------------------------------------------------
    # Set attribute value
    # --------------------------------------------------------------------------
    def set_icon(self, path: str) -> "Item":
        self.icon = Icon.from_image_file(path)
        return self

    def set_modifier(
        self,
        mod: str = ModEnum.cmd.value,
        subtitle: subtitle = None,
        arg: str = None,
        valid: bool = True,
    ) -> "Item":
        """
        Add modifier to item. Modifier allow you to return different title,
        subtitle and argument in Alfred drop down menu item when you hit a
        modifier key.

        :param mode: the modifier key
        """
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
        return self

    # --------------------------------------------------------------------------
    # Set variables
    # --------------------------------------------------------------------------
    def _open_log_file(self, path: str):
        """
        This is a special variable that will open the last error file in the editor.
        It is for internal implementation only, not for public API.
        """
        self.variables[VarKeyEnum._open_log_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum._open_log_file_path.value] = path

    def open_file(self, path: str):
        """
        Set variables to tell subsequence Alfred action to open a file.

        Use the "Utilities -> Conditional" widget and set: if ``{var:open_file}``
        is equal to "y".

        Use the "Actions -> Open File" widget and set: File: ``{var:open_file_path}``
        """
        self.variables[VarKeyEnum.open_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.open_file_path.value] = path

    def launch_app_or_file(self, path: str):
        self.variables[VarKeyEnum.launch_app_or_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.launch_app_or_file_path.value] = path

    def reveal_file_in_finder(self, path: str):
        self.variables[VarKeyEnum.reveal_file_in_finder.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.reveal_file_in_finder_path.value] = path

    def browse_in_terminal(self, path: str):
        self.variables[VarKeyEnum.browse_in_terminal.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.browse_in_terminal_path.value] = path

    def browse_in_alfred(self, path: str):
        self.variables[VarKeyEnum.browse_in_alfred.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.browse_in_alfred_path.value] = path

    def open_url(self, url: str):
        """
        Set variables to tell subsequence Alfred action to open url.

        Use the "Utilities -> Conditional" widget and set: if ``{var:open_url}``
        is equal to "y".

        Use the "Actions -> Open URL" widget and set:

        - File = ``{var:open_url_arg}``
        """
        self.variables[VarKeyEnum.open_url.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.open_url_arg.value] = url

    def run_script(self, cmd: str):
        """
        Set variables to tell subsequence Alfred action to run script.

        Use the "Utilities -> Conditional" widget and set: if ``{var:run_script}``
        is equal to "y".

        Use the "Actions -> Run Script" widget and set:

        - Language = ``/bin/bash``
        - "with input as {query}"
        - running instances = "Sequentially"
        - Script = ``{query}``
        """
        self.variables[VarKeyEnum.run_script.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.run_script_arg.value] = cmd

    def terminal_command(self, cmd: str):
        self.variables[VarKeyEnum.terminal_command.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.terminal_command_arg.value] = cmd

    def send_notification(self, title: str, subtitle: str = ""):
        """
        Set variables to tell subsequence Alfred action to send notification.

        Use the "Utilities -> Conditional" widget and set: if ``{var:send_notification}``
        is equal to "y".

        Use the "Outputs -> Post Notification" widget and set:

        - Title = ``{var:send_notification_title}``
        - Subtitle = ``{var:send_notification_subtitle}``
        """
        self.variables[VarKeyEnum.send_notification.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.send_notification_title.value] = title
        self.variables[VarKeyEnum.send_notification_subtitle.value] = subtitle
