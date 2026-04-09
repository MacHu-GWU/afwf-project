.. _Pattern-Write-Actions:

Pattern: Write Actions via Run Script
==============================================================================

A *write* Script Filter triggers a side effect when the user presses Enter —
writing a file, updating a settings store, running a shell command.  Alfred
does not call Python a second time on Enter; instead it executes a bash command
stored in the selected item's ``arg``.

The ``run_script`` pattern encodes that command *inside the Script Filter
response*, so the side-effect logic travels to Alfred as data and is executed
later by Alfred's *Run Script* widget.


The Two-Phase Architecture
------------------------------------------------------------------------------

.. code-block:: text

    Phase 1 — Script Filter (on each keystroke)
    ┌─────────────────────────────────────────────────────────────┐
    │  Python builds a command string:                            │
    │  "/path/afwf-examples write-file-request --content 'hello'" │
    │                                                             │
    │  item.run_script(cmd)  → variables["run_script"] = "y"      │
    │                          variables["run_script_arg"] = cmd  │
    │                          item.arg = cmd                     │
    └─────────────────────────────────────────────────────────────┘
                   ↓  user presses Enter
    Phase 2 — Alfred executes the command
    ┌─────────────────────────────────────────────────────────────┐
    │  Conditional (run_script=y) → Run Script widget             │
    │  Script field: {query}   (Alfred sets query = item.arg)     │
    │                                                             │
    │  Shell runs: /path/afwf-examples write-file-request ...     │
    │  Python writes the file.                                    │
    └─────────────────────────────────────────────────────────────┘

The ``*-request`` subcommands in ``cli.py`` are *not* Script Filter endpoints.
They exist solely as stable shell entry points that Alfred can invoke.


The sys.executable Trick
------------------------------------------------------------------------------

The command string must reference the CLI binary by absolute path because
Alfred's sandboxed shell does not inherit the user's ``$PATH``.  Deriving the
path from ``sys.executable`` is reliable in both dev (venv) and production
(uvx-managed) environments:

.. code-block:: python

    import sys
    from pathlib import Path

    # sys.executable = /path/to/.venv/bin/python  (dev)
    #               or /path/to/uvx-cache/python   (production)
    bin_afwf_examples = Path(sys.executable).parent / "afwf-examples"

Both ``write_file.py`` and ``set_settings.py`` use this pattern.


write-file: run_script + send_notification
------------------------------------------------------------------------------

**Keyword:** ``afwf-write-file``

**Script:** ``afwf-examples write-file --query '{query}'``

**What it does:** Shows a single confirmation item for whatever the user has
typed.  Pressing Enter writes that text to ``~/.alfred-afwf/file.txt`` and
posts a macOS notification.

.. literalinclude:: ../../../../afwf/examples/write_file.py
   :language: python

Key points:

- ``main()`` builds the command with ``_build_cmd(query)`` and attaches it via
  ``item.run_script(cmd)`` and ``item.send_notification(...)``.
- ``write_request()`` is the actual write logic.  It is separated from
  ``main()`` so it can be unit-tested directly without going through Alfred.
- The command embeds the user's input as a quoted argument:
  ``--content 'hello world'``.  The ``!r`` repr-quoting in ``_build_cmd``
  handles spaces and special characters.

**Downstream widgets** (from ``info.plist``)::

    Script Filter ──► Conditional (run_script=y) ──► Run Script {query}
                  └──► (notification is set as a variable; add Post Notification
                         widget connected after Run Script if desired)


set-settings: Two-Step Fuzzy Key Picker
------------------------------------------------------------------------------

**Keyword:** ``afwf-set-settings``

**Script:** ``afwf-examples set-settings --query '{query}'``

**What it does:** Implements a two-step UI entirely in one Script Filter:

1. **0 words** — show all valid setting keys as fuzzy-searchable items.
2. **1 word** — fuzzy-filter the key list as the user types.
3. **2+ words** — show a confirmation item; pressing Enter writes the value.

.. literalinclude:: ../../../../afwf/examples/set_settings.py
   :language: python

Key points:

- ``argumenttype: 0`` (optional) in ``info.plist`` — the query may be empty
  on first invocation.
- :class:`~afwf.query.Query` is used to branch on ``n_trimmed_parts`` (see
  :doc:`../04-QueryParser-and-Query/index`).
- The confirmation item's ``autocomplete`` field on the key items is set to
  ``sk.value + " "`` — when the user selects a key with Tab, Alfred pre-fills
  the keyword plus the chosen key and a trailing space, putting the cursor in
  the right position to type the value.
- Invalid keys (not in ``SettingsKeyEnum``) show an error item with
  ``IconFileEnum.error`` so the user gets immediate feedback.
- ``settings`` is a module-level ``_JsonSettings`` singleton backed by
  ``~/.alfred-afwf/settings.json``.

**Companion Script Filter:** ``afwf-view-settings`` (``view_settings.py``)
reads from the same store and displays all current key-value pairs.  Use it
to confirm a write was successful.

**Downstream widgets** (from ``info.plist``)::

    Script Filter ──► Conditional (run_script=y) ──► Run Script {query}


Combining run_script and send_notification
------------------------------------------------------------------------------

Both ``write_file`` and ``set_settings`` call both ``item.run_script()`` and
``item.send_notification()``.  In the ``info.plist`` the *Run Script* widget
connects forward to the *Post Notification* widget so that after the script
executes, Alfred automatically shows the notification:

.. code-block:: text

    Conditional (run_script=y)
        └──► Run Script {query}
                 └──► Post Notification
                          title:    {var:send_notification_title}
                          subtitle: {var:send_notification_subtitle}

The notification variables are set on the item in Python; Alfred carries them
through its variable inheritance from the Script Filter response all the way
to the Post Notification widget.
