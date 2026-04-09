.. _Item-Variables-Conditional-Widget:

Item Variables and Alfred's Conditional Widget
==============================================================================

Alfred's Script Filter returns a list of items. When the user selects one and
presses Enter, Alfred does not call Python again — it passes the item's ``arg``
and ``variables`` to the next widget in the workflow graph.

``afwf`` exploits this mechanism to let Python code declare the *intended
follow-up action* directly on each item, while keeping the workflow graph
(the Alfred UI) completely static. The Conditional widget reads the variables
and routes to the correct downstream action widget.


The Core Pattern
------------------------------------------------------------------------------

Every ``set_*`` helper on :class:`~afwf.item.Item` writes a pair of variables:

- a **flag** key set to ``"y"`` — the Conditional widget checks this
- a **payload** key holding the data the downstream action widget needs

.. code-block:: python

    item = Item(title="Open Python docs")
    item.open_url("https://docs.python.org/")

    # item.variables is now:
    # {
    #     "open_url":     "y",
    #     "open_url_arg": "https://docs.python.org/",
    # }

The Alfred Conditional widget is configured once with a branch for each
possible flag. At runtime it reads ``{var:open_url}``, finds ``"y"``, and
routes to the *Open URL* widget that reads ``{var:open_url_arg}``.
No Python code runs at this stage — Alfred handles the action entirely.


Variable Reference
------------------------------------------------------------------------------

The following table lists every flag/payload pair defined in
:class:`~afwf.constants.VarKeyEnum`, the ``Item`` method that sets them, and
the Alfred widget that consumes them.

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - ``Item`` method
     - Flag key
     - Payload key
     - Alfred widget
   * - ``open_url(url)``
     - ``open_url``
     - ``open_url_arg``
     - *Actions → Open URL*; URL field: ``{var:open_url_arg}``
   * - ``open_file(path)``
     - ``open_file``
     - ``open_file_path``
     - *Actions → Open File*; File: ``{var:open_file_path}``
   * - ``launch_app_or_file(path)``
     - ``launch_app_or_file``
     - ``launch_app_or_file_path``
     - *Actions → Launch Apps / Files*
   * - ``reveal_file_in_finder(path)``
     - ``reveal_file_in_finder``
     - ``reveal_file_in_finder_path``
     - *Actions → Reveal File in Finder*
   * - ``browse_in_terminal(path)``
     - ``browse_in_terminal``
     - ``browse_in_terminal_path``
     - *Actions → Browse in Terminal*
   * - ``browse_in_alfred(path)``
     - ``browse_in_alfred``
     - ``browse_in_alfred_path``
     - *Actions → Browse in Alfred*
   * - ``run_script(cmd)``
     - ``run_script``
     - ``run_script_arg``
     - *Actions → Run Script*; Script: ``{query}``; also sets ``item.arg``
   * - ``terminal_command(cmd)``
     - ``terminal_command``
     - ``terminal_command_arg``
     - *Actions → Terminal Command*; Command: ``{query}``; also sets ``item.arg``
   * - ``send_notification(title, subtitle)``
     - ``send_notification``
     - ``send_notification_title`` / ``send_notification_subtitle``
     - *Outputs → Post Notification*

.. note::

   ``run_script()`` and ``terminal_command()`` also set ``item.arg`` to the
   command string. Alfred passes ``arg`` as ``{query}`` into the connected
   *Run Script* / *Terminal Command* widget, so the command reaches the widget
   through both the variable and the arg.


Configuring the Conditional Widget
------------------------------------------------------------------------------

In Alfred's workflow editor, add a *Utilities → Conditional* widget and connect
the Script Filter to it. Add one condition branch per action type your Script
Filter uses:

.. code-block:: text

    if  {var:open_url}              is equal to    y   →  Open URL widget
    if  {var:open_file}             is equal to    y   →  Open File widget
    if  {var:run_script}            is equal to    y   →  Run Script widget
    if  {var:send_notification}     is equal to    y   →  Post Notification widget

Each downstream widget reads from the corresponding payload variable:

- *Open URL* — URL field: ``{var:open_url_arg}``
- *Open File* — File field: ``{var:open_file_path}``
- *Run Script* — Script field: ``{query}`` (Alfred copies ``item.arg`` here)
- *Post Notification* — Title: ``{var:send_notification_title}``; Subtitle: ``{var:send_notification_subtitle}``


Combining Multiple Actions
------------------------------------------------------------------------------

An item can set more than one action pair. Alfred evaluates the Conditional
branches in order — the *first* matching branch wins. Arrange branches so
the most specific checks come first.

A common combination is ``run_script`` + ``send_notification``: the script
runs, then Alfred shows a notification to confirm completion.

.. code-block:: python

    item = Item(title="Write file and notify")
    item.run_script("/path/to/.venv/bin/afwf-examples write-file-request --content 'hello'")
    item.send_notification(title="File written", subtitle="success")

    # item.variables:
    # {
    #     "run_script":                  "y",
    #     "run_script_arg":              "/path/to/...",
    #     "send_notification":           "y",
    #     "send_notification_title":     "File written",
    #     "send_notification_subtitle":  "success",
    # }

For this to work, the Conditional widget must have branches for *both*
``run_script`` and ``send_notification``, and the *Run Script* widget must
connect forward to the *Post Notification* widget.


Modifier Key Overrides
------------------------------------------------------------------------------

:meth:`~afwf.item.Item.set_modifier` adds an entry to ``item.mods`` so that
holding a modifier key (e.g. ``⌘``) shows an alternate subtitle and passes
a different ``arg``.

By default a mod entry inherits the item's ``variables``. To prevent
inheritance — for example, so that ``⌘ + Enter`` does something completely
different — pass an explicit ``variables={}`` inside the mod dict.

See :class:`~afwf.constants.ModEnum` for the full list of supported modifier
key combinations.


Why This Design
------------------------------------------------------------------------------

Keeping the workflow graph static has a concrete advantage: the Alfred UI
does not need to change when new behaviour is added. Adding a new action type
only requires:

1. A new ``VarKeyEnum`` / ``VarValueEnum`` pair in ``constants.py``
2. A new ``set_*`` method on ``Item``
3. A new branch in the Conditional widget (one-time, in Alfred's UI)

All existing Script Filters that do not set the new variable are unaffected.
