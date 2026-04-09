# -*- coding: utf-8 -*-

"""
Example: Set Settings
=====================

**What it demonstrates**

Shows a two-step fuzzy-picker pattern for writing to a persistent key-value
store, and how to bind the Enter key to an arbitrary Python action via Alfred's
*Run Script* widget (the same technique as ``write_file.py``).

The Script Filter behaves differently depending on how many words the user has
typed:

- **0 words** — list all valid setting keys as fuzzy-searchable items.
- **1 word (key only)** — fuzzy-match the typed prefix against the key list.
- **2 words (key + value)** — show a single confirmation item; pressing Enter
  triggers a dynamically built CLI command that writes the value:

  .. code-block::

      /path/to/.venv/bin/afwf-examples set-settings-request --key username --value alice

  The ``set-settings-request`` sub-command is **not** a Script Filter endpoint.
  It exists solely as a CLI entry point for the run_script action, analogous to
  ``write-file-request`` in ``write_file.py``.
"""

import sys
from pathlib import Path

import afwf.api as afwf
import afwf.opt.fuzzy_item.api as fuzzy_item

from afwf.examples.settings import settings, SettingsKeyEnum


def _all_key_items() -> list[fuzzy_item.Item]:
    """Return one fuzzy item per setting key."""
    items = []
    for sk in SettingsKeyEnum:
        item = fuzzy_item.Item(
            title=sk.value,
            subtitle=f"set {sk.value} to ...",
            autocomplete=sk.value + " ",
        )
        item.set_fuzzy_match_name(sk.value)
        items.append(item)
    return items


def _build_cmd(key: str, value: str) -> str:
    """Build the shell command Alfred's *Run Script* widget will execute.

    See ``write_file.py`` for a detailed explanation of this pattern.
    The binary is derived from ``sys.executable`` so it works reliably inside
    Alfred's sandboxed shell environment.
    """
    bin_afwf_examples = Path(sys.executable).parent / "afwf-examples"
    return f"{bin_afwf_examples} set-settings-request --key {key!r} --value {value!r}"


def set_settings_request(key: str, value: str) -> None:
    """Write *value* for *key* into the settings store.

    This function is **not** called by Alfred's Script Filter directly.
    It is the target of the dynamically built CLI command produced by
    :func:`_build_cmd`, executed by Alfred via a *Run Script* widget when
    the user confirms a key=value pair.
    """
    settings[key] = value


@afwf.log_error(log_file=afwf.path_enum.dir_afwf / "set_settings.log")
def main(query: str) -> afwf.ScriptFilter:
    sf = afwf.ScriptFilter()
    q = afwf.Query.from_str(query)

    if q.n_trimmed_parts == 0:
        # No input yet — show all keys.
        sf.items.extend(_all_key_items())

    elif q.n_trimmed_parts == 1:
        # One word typed — fuzzy-filter the key list.
        key = q.trimmed_parts[0]
        all_items = _all_key_items()
        matcher = fuzzy_item.FuzzyItemMatcher.from_items(all_items)
        matched = matcher.match(key, threshold=0)
        sf.items.extend(matched if matched else all_items)

    else:
        # Two+ words — treat first as key, rest joined as value.
        key = q.trimmed_parts[0]
        value = " ".join(q.trimmed_parts[1:])
        if key in SettingsKeyEnum.__members__:
            item = afwf.Item(
                title=f"Set settings.{key} = {value!r}",
            )
            item.run_script(_build_cmd(key, value))
            item.send_notification(title=f"Set settings.{key} = {value!r}")
            sf.items.append(item)
        else:
            item = afwf.Item(title=f"{key!r} is not a valid settings key")
            item.set_icon(afwf.IconFileEnum.error)
            sf.items.append(item)

    return sf
