# -*- coding: utf-8 -*-

"""
Example: View Settings
======================

**What it demonstrates**

Shows how to read from a persistent key-value store and display all entries as
Alfred items.  Each item shows one setting key and its current value.  This
example is designed to work alongside ``set_settings.py``: use
``set_settings`` to write a value, then open ``view_settings`` to confirm it
was saved.
"""

import afwf.api as afwf

from afwf.examples.settings import path_settings_json, settings, SettingsKeyEnum


@afwf.log_error(log_file=afwf.path_enum.dir_afwf / "view_settings.log")
def main() -> afwf.ScriptFilter:
    sf = afwf.ScriptFilter()
    for settings_key in SettingsKeyEnum:
        value = settings.get(settings_key.value)
        item = afwf.Item(
            title=f"settings.{settings_key.value} = {value!r}",
            subtitle=f"settings are stored at {path_settings_json}",
        )
        sf.items.append(item)
    return sf
