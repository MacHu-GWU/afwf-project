# -*- coding: utf-8 -*-

"""
Example: Write File
===================

**What it demonstrates**

Shows how to trigger an arbitrary Python action when the user presses Enter,
using Alfred's *Run Script* widget.  The Script Filter builds an item whose
``arg`` is a shell command; when selected, Alfred passes that command to a
*Run Script* widget which executes it.

The write logic lives in :func:`write_request` — a plain function that writes
the query text into ``file.txt``.  The CLI exposes it as the
``write-file-request`` sub-command so that the generated shell command looks
like::

    afwf-examples write-file-request --content 'hello world'

Use ``read_file`` to verify the written content afterwards.
"""

import shutil
import sys

import afwf.api as afwf
from afwf.paths import path_enum

path_file = path_enum.dir_afwf / "file.txt"


def write_request(content: str) -> None:
    """Write *content* to ``file.txt`` under the afwf home directory."""
    path_file.parent.mkdir(parents=True, exist_ok=True)
    path_file.write_text(content)


def _build_cmd(content: str) -> str:
    """Return the shell command Alfred's Run Script widget will execute."""
    bin_afwf_examples = shutil.which("afwf-examples") or f"{sys.executable} -m afwf.examples.cli"
    return f"{bin_afwf_examples} write-file-request --content {content!r}"


@afwf.log_error(log_file=path_enum.dir_afwf / "write_file.log")
def main(query: str) -> afwf.ScriptFilter:
    sf = afwf.ScriptFilter()
    item = afwf.Item(
        title=f"Write {query!r} to {path_file}",
    )
    item.run_script(_build_cmd(query))
    item.send_notification(
        title=f"Write {query!r} to {path_file}",
        subtitle="success",
    )
    sf.items.append(item)
    return sf
