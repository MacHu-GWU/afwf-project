# -*- coding: utf-8 -*-

"""
Alfred Workflow Script Filter protocol constants.

All special string values defined by the Alfred Script Filter JSON spec are
collected here as :class:`~enum_mate.api.BetterStrEnum` subclasses so that
workflow developers can use them without memorising raw strings.

Ref: https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
"""

from enum_mate.api import BetterStrEnum


class IconTypeEnum(BetterStrEnum):
    """
    Allowed values for ``icon.type`` in a Script Filter item.

    - ``fileicon`` — Alfred uses the file-system icon of the file at ``icon.path``
    - ``filetype``  — ``icon.path`` is treated as a UTI (e.g. ``"com.apple.rtfd"``)
    - *(omitted)*   — ``icon.path`` is a path relative to the workflow root folder

    Ref: search ``icon : OBJECT`` in the Alfred Script Filter JSON docs.
    """

    fileicon = "fileicon"
    filetype = "filetype"


class ItemTypeEnum(BetterStrEnum):
    """
    Allowed values for ``item.type`` in a Script Filter item.

    - ``file``           — Alfred treats the result as a file; checks existence before showing
    - ``file:skipcheck`` — Same as ``file`` but skips the existence check

    Ref: search ``type : STRING`` in the Alfred Script Filter JSON docs.
    """

    file = "file"
    file_skipcheck = "file:skipcheck"


class ModEnum(BetterStrEnum):
    """
    Modifier key identifiers for the ``item.mods`` object.

    Used as keys inside ``mods`` to define alternate behaviour when the user
    holds a modifier key while actioning an item.

    Note: when a mod entry contains a ``variables`` key, it **replaces** (not
    merges with) the item's ``variables``.  An empty ``"variables": {}`` on a
    mod explicitly prevents inheriting the item's variables.

    Ref: search ``mods : OBJECT`` in the Alfred Script Filter JSON docs.
    """

    cmd = "cmd"
    shift = "shift"
    alt = "alt"
    ctrl = "ctrl"
    fn = "fn"
    cmd_alt = "cmd+alt"
    cmd_ctrl = "cmd+ctrl"
    cmd_shift = "cmd+shift"


class VarKeyEnum(BetterStrEnum):
    """
    Variable key names used by this framework's built-in ``set_*`` helpers on
    :class:`~afwf.item.Item`.

    These variable names are conventions understood by the accompanying Alfred
    workflow widgets (Conditional, Open File, Run Script, etc.).
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
    Standard boolean-style variable values used by this framework's ``set_*``
    helpers. Alfred widget conditions check against these strings.
    """

    y = "y"
    n = "n"
