# -*- coding: utf-8 -*-

"""
Example: Open File
==================

**What it demonstrates**

Shows how to build a file-picker Script Filter that lets Alfred's built-in
result filtering do the work.  The handler lists every ``.py`` file in the
``examples/`` directory and attaches ``open_file`` / ``open_file_path``
variables to each item so a downstream *Open File* action can open the
selected file with the system default application.

Because **Alfred filters results** is enabled, the ``main`` function always
returns the full list and Alfred narrows it in real time as the user types —
no Python-side filtering needed.

**Alfred Workflow setup**

+---------------------------+----------------------------------------------------+
| Field                     | Value                                              |
+===========================+====================================================+
| Keyword                   | ``afwf-example-open-file`` (Argument Optional)     |
+---------------------------+----------------------------------------------------+
| Language                  | ``/bin/bash``                                      |
+---------------------------+----------------------------------------------------+
| Script                    | ``python main.py 'open_file {query}'``             |
+---------------------------+----------------------------------------------------+
| Alfred filters results    | **checked**                                        |
+---------------------------+----------------------------------------------------+

**Downstream widgets**

1. *Utilities → Conditional* — condition: ``{var:open_file}`` is equal to ``y``
2. *Actions → Open File* — File: ``{var:open_file_path}``
"""

from pathlib_mate import Path
import afwf.api as afwf


@afwf.log_error(log_file=afwf.path_enum.dir_afwf / "open_file.log")
def main() -> afwf.ScriptFilter:
    sf = afwf.ScriptFilter()
    dir_here = Path(__file__).parent
    for p in sorted(dir_here.iterdir(), key=lambda x: x.basename):
        if p.ext.lower() == ".py":
            item = afwf.Item(
                title=p.basename,
                subtitle=f"Open {p.abspath}",
                autocomplete=p.basename,
                match=p.basename,
                arg=p.abspath,
            )
            item.open_file(path=p.abspath)
            sf.items.append(item)
    return sf
