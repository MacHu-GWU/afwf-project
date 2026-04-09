# -*- coding: utf-8 -*-

"""
Example: Write File
===================

**What it demonstrates**

Shows how to bind the Enter key in a Script Filter to an arbitrary Python
action via Alfred's *Run Script* widget.

When the user types text in the ``write-file`` Script Filter and presses
Enter, Alfred does **not** call Python directly — it executes whatever bash
command is stored in the selected item's ``arg``.  We therefore construct that
command string dynamically inside :func:`_build_cmd`, encoding the user's
input into it so Alfred can hand it back to us as a CLI invocation.

The actual write logic lives in :func:`write_request`.  The CLI exposes it as
the ``write-file-request`` sub-command.  That sub-command is **not** a Script
Filter endpoint — it is never called by Alfred's keyword trigger.  It exists
solely as a stable shell entry point that the dynamically built command can
call when Alfred fires the *Run Script* action::

    /path/to/.venv/bin/afwf-examples write-file-request --content 'hello'

Use ``read_file`` to verify the written content afterwards.
"""

import sys
from pathlib import Path

import afwf.api as afwf
from afwf.paths import path_enum

path_file = path_enum.dir_afwf / "file.txt"


def write_request(content: str) -> None:
    """Write *content* to ``file.txt`` under the afwf home directory.

    This function is **not** invoked by Alfred's Script Filter directly.
    It is the target of the dynamically built CLI command produced by
    :func:`_build_cmd`, which Alfred executes via a *Run Script* widget
    when the user presses Enter on the ``write-file`` item.
    """
    path_file.parent.mkdir(parents=True, exist_ok=True)
    path_file.write_text(content)


def _build_cmd(content: str) -> str:
    """Build the shell command that Alfred's *Run Script* widget will execute.

    When the user presses Enter, Alfred runs the bash command stored in the
    item's ``arg``.  We construct that command here, embedding ``content`` so
    Alfred can pass it back to :func:`write_request` via the CLI.

    The ``write-file-request`` sub-command is not a Script Filter endpoint —
    it is a thin CLI wrapper around :func:`write_request` that exists only to
    give Alfred a runnable command.

    We derive the CLI binary path from ``sys.executable`` (e.g.
    ``/path/to/.venv/bin/python`` → ``/path/to/.venv/bin/afwf-examples``)
    rather than relying on PATH lookup, which is unreliable inside Alfred's
    sandboxed shell environment.
    """
    # sys.executable is e.g. /path/to/.venv/bin/python; the CLI lives beside it.
    bin_afwf_examples = Path(sys.executable).parent / "afwf-examples"
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
