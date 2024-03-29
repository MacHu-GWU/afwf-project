# -*- coding: utf-8 -*-

"""
Alfred Workflow Script Filter Item module.
"""

import typing as T

import attrs
from attrs import validators as vs
from attrs_mate import AttrsClass
from .vendor.better_enum import BetterStrEnum

from .script_filter_object import ScriptFilterObject


@attrs.define
class Icon(ScriptFilterObject):
    """
    represent an icon object in script filter item.

    Reference:

    - Search ``icon : OBJECT (optional)`` in https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    class TypeEnum(BetterStrEnum):
        fileicon = "fileicon"
        filetype = "filetype"

    # fmt: off
    path: str = AttrsClass.ib_str()
    type: str = attrs.field(validator=vs.optional(vs.in_(TypeEnum.get_values())), default=None)
    # fmt: on

    @classmethod
    def from_image_file(cls, path: str) -> "Icon":
        """
        Create an Icon object that using a file on local file system as an icon.
        """
        return cls(path=path)


class VarKeyEnum(BetterStrEnum):
    """
    List of available variable keys in this framework.
    """

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


class VarValueEnum(BetterStrEnum):
    """
    List of available variable values in this framework.
    """

    y = "y"
    n = "n"


@attrs.define
class Text(ScriptFilterObject):
    """
    Represent a text object in script filter item.

    Reference:

    - Search ``text : OBJECT (optional)`` in https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    copy: str = AttrsClass.ib_str(default=None)
    largetype: str = AttrsClass.ib_str(default=None)


class ModEnum(BetterStrEnum):
    """
    List of available modifier keys. Hit enter with the modifier key can lead
    to different behavior.

    Reference:

    - Search ``mods : OBJECT (optional)`` in https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    cmd = "cmd"
    shift = "shift"
    alt = "alt"
    ctrl = "ctrl"
    fn = "fn"
    cmd_alt = "cmd+alt"
    cmd_ctrl = "cmd+ctrl"
    cmd_shift = "cmd+shift"


T_ITEM_ACTION = T.Union[str, T.List[str], T.Dict[str, T.Any]]


@attrs.define
class Item(ScriptFilterObject):
    """
    Data model for alfred dropdown menu items.

    .. note::

        Please make sure the attribute name is exactly the same as the field name
        in the following document.

    Ref: https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    class TypeEnum(BetterStrEnum):
        file = "file"
        file_skipcheck = "file:skipcheck"

    # fmt: off
    title: str = AttrsClass.ib_str()
    subtitle: str = AttrsClass.ib_str(default=None)
    arg: str = AttrsClass.ib_str(default=None)
    autocomplete: str = AttrsClass.ib_str(default=None)
    icon: Icon = Icon.ib_nested(default=None)
    valid: bool = AttrsClass.ib_bool(default=True)
    uid: str = AttrsClass.ib_str(default=None)
    match: str = AttrsClass.ib_str(default=None)
    type: str = attrs.field(validator=vs.optional(vs.in_(TypeEnum.get_values())), default=None)
    mods: dict = AttrsClass.ib_dict(default=None)
    action: T_ITEM_ACTION = attrs.field(default=None)
    text: Text = Text.ib_nested(default=None)
    quicklookurl: str = AttrsClass.ib_str(default=None)
    variables: dict = AttrsClass.ib_dict(factory=dict)
    # fmt: on

    # --------------------------------------------------------------------------
    # Set attribute value
    # --------------------------------------------------------------------------
    def set_icon(self, path: str) -> "Item":
        """
        Set icon for item.
        """
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
        :param subtitle: the subtitle you want to display
        :param arg: the argument passed to subsequence action
        :param valid: whether the item is valid
        """
        if mod not in ModEnum.get_values():
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
    def _open_log_file(self, path: str) -> "Item":  # pragma: no cover
        """
        This is a special variable that will open the last error file in the editor.
        It is for internal implementation only, not for public API.
        """
        self.variables[VarKeyEnum._open_log_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum._open_log_file_path.value] = path
        return self

    def open_file(self, path: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to open a file.

        Use the "Utilities -> Conditional" widget and set: if ``{var:open_file}``
        is equal to "y".

        Use the "Actions -> Open File" widget and set: File: ``{var:open_file_path}``

        :param path: the absolute path of the file to open
        """
        self.variables[VarKeyEnum.open_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.open_file_path.value] = path
        return self

    def launch_app_or_file(self, path: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to launch an app or file.

        Use the "Utilities -> Conditional" widget and set: if ``{var:launch_app_or_file}``
        is equal to "y".

        Use the "Actions -> Launch Apps / Files" widget.

        :param path: the absolute path of the file or app to launch
        """
        self.variables[VarKeyEnum.launch_app_or_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.launch_app_or_file_path.value] = path
        return self

    def reveal_file_in_finder(self, path: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to launch an app or file.

        Use the "Utilities -> Conditional" widget and set: if ``{var:reveal_file_in_finder}``
        is equal to "y".

        Use the "Actions -> Reveal File in Finder" widget.

        :param path: the absolute path of the file to reveal in Finder
        """
        self.variables[VarKeyEnum.reveal_file_in_finder.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.reveal_file_in_finder_path.value] = path
        return self

    def browse_in_terminal(self, path: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to browse in terminal.

        Use the "Utilities -> Conditional" widget and set: if ``{var:browse_in_terminal}``
        is equal to "y".

        Use the "Actions -> Browse in Terminal" widget.
        """
        self.variables[VarKeyEnum.browse_in_terminal.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.browse_in_terminal_path.value] = path
        return self

    def browse_in_alfred(self, path: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to browse in Alfred.

        Use the "Utilities -> Conditional" widget and set: if ``{var:browse_in_alfred}``
        is equal to "y".

        Use the "Actions -> Browse in Alfred" widget.
        """
        self.variables[VarKeyEnum.browse_in_alfred.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.browse_in_alfred_path.value] = path
        return self

    def open_url(self, url: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to open url.

        Use the "Utilities -> Conditional" widget and set: if ``{var:open_url}``
        is equal to "y".

        Use the "Actions -> Open URL" widget and set:

        - File = ``{var:open_url_arg}``

        :param url: the url to open in browser
        """
        self.variables[VarKeyEnum.open_url.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.open_url_arg.value] = url
        return self

    def run_script(self, cmd: str) -> "Item":
        """
        Set variables to tell subsequence Alfred action to run script.

        Use the "Utilities -> Conditional" widget and set: if ``{var:run_script}``
        is equal to "y".

        Use the "Actions -> Run Script" widget and set:

        - Language = ``/bin/bash``
        - "with input as {query}"
        - running instances = "Sequentially"
        - Script = ``{query}``

        :param cmd: the full command to run, for example ``python3 /path/to/test.py``
        """
        self.variables[VarKeyEnum.run_script.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.run_script_arg.value] = cmd
        self.arg = cmd
        return self

    def terminal_command(self, cmd: str) -> "Item":
        """
        Use the "Utilities -> Conditional" widget and set: if ``{var:terminal_command}``
        is equal to "y".

        Use the "Actions -> Terminal Command" widget and set:

        - Command = ``{query}``

        :param cmd: the full command to run in terminal, for example ``python3 /path/to/test.py``
        """
        self.variables[VarKeyEnum.terminal_command.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.terminal_command_arg.value] = cmd
        self.arg = cmd
        return self

    def send_notification(self, title: str, subtitle: str = "") -> "Item":
        """
        Set variables to tell subsequence Alfred action to send notification.

        Use the "Utilities -> Conditional" widget and set: if ``{var:send_notification}``
        is equal to "y".

        Use the "Outputs -> Post Notification" widget and set:

        - Title = ``{var:send_notification_title}``
        - Subtitle = ``{var:send_notification_subtitle}``

        :param title: the title of the notification
        :param subtitle: the subtitle of the notification
        """
        self.variables[VarKeyEnum.send_notification.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.send_notification_title.value] = title
        self.variables[VarKeyEnum.send_notification_subtitle.value] = subtitle
        return self
