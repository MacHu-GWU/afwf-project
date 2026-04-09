.. _Example-Workflow-Architecture:

The afwf Example Workflow: Architecture and Development Model
==============================================================================

The ``afwf`` library ships a complete, runnable Alfred workflow that
demonstrates every pattern covered in the next four documents.  This document
explains the architecture of that example workflow and the development model
behind it.

Install the workflow from the repo root to follow along interactively:

.. code-block:: text

    afwf-dev.alfredworkflow   ← double-click to install in Alfred

The source of truth is the plain-text plist file alongside it:

.. code-block:: text

    info.plist   ← human-readable XML; captures everything the Alfred UI shows


The Three-Layer Development Model
------------------------------------------------------------------------------

``afwf``-based workflows are built in three independent layers:

.. code-block:: text

    ┌─────────────────────────────────────────────────────────┐
    │  Layer 1 — Python logic                                 │
    │  afwf/examples/*.py                                     │
    │  Pure functions; no Alfred dependency.                  │
    │  Unit-tested in isolation.                              │
    ├─────────────────────────────────────────────────────────┤
    │  Layer 2 — CLI entry point                              │
    │  afwf/examples/cli.py  →  afwf-examples                 │
    │  fire.Fire(Command) exposes each main() as a subcommand │
    │  Alfred calls this binary from its Script field.        │
    ├─────────────────────────────────────────────────────────┤
    │  Layer 3 — Alfred workflow config                       │
    │  info.plist                                             │
    │  Declares keywords, Script Filter nodes, Conditional    │
    │  branches, and action widgets.  Static; never changes   │
    │  when Python logic changes.                             │
    └─────────────────────────────────────────────────────────┘

This separation means:

- Python logic is testable with plain ``pytest`` — no Alfred needed.
- Adding a new feature only changes Python code; the workflow graph is untouched.
- Deploying a new version is a version bump in PyPI; Alfred users upgrade via ``uvx``.


The CLI Entry Point
------------------------------------------------------------------------------

``pyproject.toml`` declares ``afwf-examples`` as a console script entry point:

.. code-block:: toml

    [project.scripts]
    afwf-examples = "afwf.examples.cli:main"

``afwf/examples/cli.py`` wraps every Python ``main()`` function as a
``fire.Fire`` subcommand:

.. literalinclude:: ../../../../afwf/examples/cli.py
   :language: python

Each subcommand maps directly to one Script Filter keyword in Alfred.  The
``*-request`` subcommands (``write-file-request``, ``set-settings-request``)
are *not* Script Filter endpoints — they are CLI-only entry points called by
Alfred's *Run Script* widget (see :doc:`../10-Pattern-Write-Actions/index`).


Two Invocation Modes
------------------------------------------------------------------------------

The ``script`` field in each Script Filter node has two forms depending on
the deployment context:

**Dev / local** — uses the project's virtual environment directly.
This is what ``info.plist`` contains in the repo:

.. code-block:: bash

    /Users/sanhehu/Documents/GitHub/afwf-project/.venv/bin/afwf-examples \
        search-bookmarks --query '{query}'

**Production** — calls the package via ``uvx``, which downloads, caches, and
runs the pinned version without any pre-installed virtualenv:

.. code-block:: bash

    ~/.local/bin/uvx --from afwf==1.0.1 \
        afwf-examples search-bookmarks --query '{query}'

The only thing that changes between the two modes is the binary path.
The subcommand name and arguments are identical.


info.plist Structure
------------------------------------------------------------------------------

Alfred stores the entire workflow definition in a single plist file.
Understanding its structure makes it possible to inspect or edit the workflow
without opening Alfred's GUI (where screenshots lose detail).

**Top-level keys**

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Key
     - Content
   * - ``objects``
     - Array of all nodes (Script Filters, Conditionals, action widgets)
   * - ``connections``
     - Dict mapping source node UID → list of wired destination UIDs
   * - ``uidata``
     - Dict mapping node UID → ``{xpos, ypos}`` (visual canvas positions only)
   * - ``name``
     - Workflow display name (``"afwf dev"``)
   * - ``bundleid``
     - Unique reverse-DNS identifier (``"MacHu-GWU.afwf-dev"``)

**A Script Filter node**

Each entry in ``objects`` with ``type = alfred.workflow.input.scriptfilter``
has a ``config`` dict.  The fields that matter most:

.. code-block:: xml

    <key>keyword</key>
    <string>afwf-search-bookmarks</string>          <!-- Alfred trigger keyword -->

    <key>script</key>
    <string>.venv/bin/afwf-examples search-bookmarks --query '{query}'</string>

    <key>argumenttype</key>
    <integer>1</integer>    <!-- 0=optional  1=required  2=no argument -->

    <key>withspace</key>
    <true/>                 <!-- keyword must be followed by a space before firing -->

    <key>alfredfiltersresults</key>
    <false/>                <!-- false = Script Filter handles filtering in Python
                                 true  = Alfred filters the returned list client-side -->

**Connections**

The ``connections`` dict is keyed by the *source* node's UID.  Each value is
an array of destination objects.  A ``sourceoutputuid`` of
``4D36294E-9A14-49FB-A0F4-62E21227E74D`` in a Conditional node means "the
matching (``y``) branch output":

.. code-block:: xml

    <key>2219C90E-2659-4B5A-BDB1-B1A0375C5501</key>   <!-- Conditional: open_url=y -->
    <array>
        <dict>
            <key>destinationuid</key>
            <string>2FE6CFA4-74F5-41A7-A2CA-43A4D999A92D</string>   <!-- Open URL widget -->
            <key>sourceoutputuid</key>
            <string>4D36294E-9A14-49FB-A0F4-62E21227E74D</string>   <!-- "y" branch output -->
        </dict>
    </array>


The Shared Downstream Widget Pattern
------------------------------------------------------------------------------

The example workflow has six Script Filter triggers but only a small set of
Conditional + action widget pairs, shared across triggers:

.. code-block:: text

    afwf-search-bookmarks ──┐
                            ├──► Conditional (open_url=y)    ──► Open URL
                            ├──► Conditional (open_file=y)   ──► Open File  ◄──── afwf-open-file
                            └──► Conditional (_open_log_file=y) ──► Open File (log)

    afwf-write-file ────────┐
    afwf-set-settings ──────┴──► Conditional (run_script=y)  ──► Run Script

    afwf-memoize         (read-only; no downstream action widget)
    afwf-read-file       (read-only; no downstream action widget)
    afwf-view-settings   (read-only; no downstream action widget)

Multiple Script Filter triggers wire to the *same* Conditional node.  Alfred
evaluates the variables on the selected item and routes correctly regardless
of which trigger produced it.  This keeps the workflow graph small and avoids
duplicating widget configuration.

Adding a new action type requires adding one Conditional branch and one action
widget — once — and then any number of Script Filters can use it immediately
by setting the appropriate variable pair on their items.
