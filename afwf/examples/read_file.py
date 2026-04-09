# -*- coding: utf-8 -*-

"""
Example: Read File
==================

**What it demonstrates**

Shows how to build a Script Filter that reads the content of a file and
displays it as an Alfred item.  This example is designed to work alongside
``write_file.py``: use ``write_file`` to write text into ``file.txt``, then
use ``read_file`` to confirm the content was saved correctly.

If the file does not exist yet, an error item (with the error icon) is shown
instead.
"""

import afwf.api as afwf
from afwf.paths import path_enum

path_file = path_enum.dir_afwf / "file.txt"


@afwf.log_error(log_file=path_enum.dir_afwf / "read_file.log")
def main() -> afwf.ScriptFilter:
    sf = afwf.ScriptFilter()
    if path_file.exists():
        content = path_file.read_text()
        item = afwf.Item(
            title=f"content of {path_file} is",
            subtitle=content,
        )
    else:
        item = afwf.Item(
            title=f"{path_file} does not exist!",
        )
        item.set_icon(afwf.IconFileEnum.error)

    sf.items.append(item)
    return sf
