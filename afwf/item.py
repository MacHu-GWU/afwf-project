# -*- coding: utf-8 -*-

"""
Alfred Workflow Script Filter Item module.
"""

from typing import Any, ClassVar
from pydantic import ConfigDict, Field

from .script_filter_object import ScriptFilterObject
from .constants import IconTypeEnum
from .constants import ItemTypeEnum
from .constants import ModEnum
from .constants import VarKeyEnum
from .constants import VarValueEnum



class Icon(ScriptFilterObject):
    """
    Represent an icon object in a Script Filter item.

    Ref: search ``icon : OBJECT`` in https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    # Alias kept for workflow-developer discoverability: Icon.TypeEnum
    TypeEnum: ClassVar[type[IconTypeEnum]] = IconTypeEnum

    path: str
    type: str | None = None

    @classmethod
    def from_image_file(
        cls,
        path: str,
    ) -> "Icon":
        """
        Create an Icon using a local file's path as the icon image.
        """
        return cls(path=path)


class Text(ScriptFilterObject):
    """
    Represent the ``text`` object in a Script Filter item.

    - ``copy``      — text copied to clipboard when the user presses ⌘C
    - ``largetype`` — text shown with Alfred Large Type (⌘L)

    If neither field is set Alfred falls back to using ``arg``.

    Ref: search ``text : OBJECT`` in https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    copy: str | None = None  # Alfred JSON field; shadows BaseModel.copy() intentionally
    largetype: str | None = None


T_ITEM_ACTION = str | list[str] | dict[str, Any]


class Item(ScriptFilterObject):
    """
    Data model for an Alfred Script Filter dropdown menu item.

    Field names match the Alfred JSON spec exactly.

    Ref: https://www.alfredapp.com/help/workflows/inputs/script-filter/json/

    .. note::

        **``mods`` and ``variables`` inheritance** — when a mod entry contains a
        ``variables`` key it *replaces* (not merges with) the item's ``variables``.
        An explicit ``"variables": {}`` on a mod prevents inheriting item variables.
        See :class:`~afwf.constants.ModEnum`.
    """

    # Alias kept for workflow-developer discoverability: Item.TypeEnum
    TypeEnum: ClassVar[type[ItemTypeEnum]] = ItemTypeEnum

    title: str
    subtitle: str | None = None
    arg: str | None = None
    autocomplete: str | None = None
    icon: Icon | None = None
    valid: bool = True
    uid: str | None = None
    match: str | None = None
    type: str | None = None
    mods: dict | None = None
    action: T_ITEM_ACTION | None = None
    text: Text | None = None
    quicklookurl: str | None = None
    variables: dict = Field(default_factory=dict)

    # --------------------------------------------------------------------------
    # Set attribute value
    # --------------------------------------------------------------------------
    def set_icon(
        self,
        path: str,
    ) -> "Item":
        """
        Set icon for item.
        """
        self.icon = Icon.from_image_file(path)
        return self

    def set_modifier(
        self,
        mod: str | ModEnum = ModEnum.cmd,
        subtitle: str | None = None,
        arg: str | None = None,
        valid: bool = True,
    ) -> "Item":
        """
        Add a modifier key override to this item.

        When the user holds the modifier key while actioning the item, Alfred
        uses the values defined here instead of the item's top-level fields.

        :param mod: modifier key; use :class:`~afwf.constants.ModEnum` values
        :param subtitle: alternate subtitle to display
        :param arg: alternate argument passed to the connected action
        :param valid: whether the item is actionable with this modifier
        """
        if mod not in ModEnum.get_values():
            raise ValueError(f"Invalid modifier key: {mod!r}. Use ModEnum values.")
        dct = {
            k: v
            for k, v in dict(subtitle=subtitle, arg=arg, valid=valid).items()
            if v
        }
        if self.mods is None:
            self.mods = dict()
        self.mods[mod] = dct
        return self

    # --------------------------------------------------------------------------
    # Set variables
    # --------------------------------------------------------------------------
    def _open_log_file(  # pragma: no cover
        self,
        path: str,
    ) -> "Item":
        """
        Internal use only: sets a variable to open the last error log in editor.
        """
        self.variables[VarKeyEnum._open_log_file.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum._open_log_file_path.value] = path
        return self

    def open_file(
        self,
        path: str,
    ) -> "Item":
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

    def launch_app_or_file(
        self,
        path: str,
    ) -> "Item":
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

    def reveal_file_in_finder(
        self,
        path: str,
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to reveal a file in Finder.

        Use the "Utilities -> Conditional" widget and set: if ``{var:reveal_file_in_finder}``
        is equal to "y".

        Use the "Actions -> Reveal File in Finder" widget.

        :param path: the absolute path of the file to reveal in Finder
        """
        self.variables[VarKeyEnum.reveal_file_in_finder.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.reveal_file_in_finder_path.value] = path
        return self

    def browse_in_terminal(
        self,
        path: str,
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to browse in terminal.

        Use the "Utilities -> Conditional" widget and set: if ``{var:browse_in_terminal}``
        is equal to "y".

        Use the "Actions -> Browse in Terminal" widget.
        """
        self.variables[VarKeyEnum.browse_in_terminal.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.browse_in_terminal_path.value] = path
        return self

    def browse_in_alfred(
        self,
        path: str,
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to browse in Alfred.

        Use the "Utilities -> Conditional" widget and set: if ``{var:browse_in_alfred}``
        is equal to "y".

        Use the "Actions -> Browse in Alfred" widget.
        """
        self.variables[VarKeyEnum.browse_in_alfred.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.browse_in_alfred_path.value] = path
        return self

    def open_url(
        self,
        url: str,
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to open a URL.

        Use the "Utilities -> Conditional" widget and set: if ``{var:open_url}``
        is equal to "y".

        Use the "Actions -> Open URL" widget and set: File = ``{var:open_url_arg}``

        :param url: the URL to open in browser
        """
        self.variables[VarKeyEnum.open_url.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.open_url_arg.value] = url
        return self

    def run_script(
        self,
        cmd: str,
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to run a script.

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

    def terminal_command(
        self,
        cmd: str,
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to run a terminal command.

        Use the "Utilities -> Conditional" widget and set: if ``{var:terminal_command}``
        is equal to "y".

        Use the "Actions -> Terminal Command" widget and set: Command = ``{query}``

        :param cmd: the full command to run in terminal
        """
        self.variables[VarKeyEnum.terminal_command.value] = VarValueEnum.y.value
        self.variables[VarKeyEnum.terminal_command_arg.value] = cmd
        self.arg = cmd
        return self

    def send_notification(
        self,
        title: str,
        subtitle: str = "",
    ) -> "Item":
        """
        Set variables to tell subsequence Alfred action to send a notification.

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
