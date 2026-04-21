.. _afwf-Introduction:

afwf Introduction
==============================================================================

``afwf`` is a Python framework for building Alfred Workflows. It covers three things:

- **A typed API for Script Filter output** — build drop-down items and script filter responses as Python objects, not raw dicts.
- **A uvx-based deployment model** — ship your workflow as a PyPI package, invoke it from Alfred with a single ``uvx`` line. No virtualenv to babysit.
- **Optional workflow utilities** — fuzzy ranking, disk caching, and other primitives that come up in nearly every workflow.


Quick Example
------------------------------------------------------------------------------

A Script Filter that fuzzy-ranks bookmarks against the user's query:

.. code-block:: python

    from afwf.api import ScriptFilter
    from afwf.opt.fuzzy_item.api import Item, FuzzyItemMatcher

    BOOKMARKS = [
        ("Alfred App",     "https://www.alfredapp.com/"),
        ("Python",         "https://www.python.org/"),
        ("GitHub",         "https://github.com/"),
        ("Stack Overflow", "https://stackoverflow.com/"),
    ]

    def search_bookmarks(query: str = "") -> ScriptFilter:
        items = [
            Item(title=title, subtitle=url, arg=url).set_fuzzy_match_name(title)
            for title, url in BOOKMARKS
        ]
        if query.strip():
            items = FuzzyItemMatcher.from_items(items).match(query, threshold=0) or items
        sf = ScriptFilter()
        sf.items.extend(items)
        return sf

The Alfred Script field:

.. code-block:: bash

    ~/.local/bin/uvx your-workflow@1.0.0 search-bookmarks --query '{query}'

That's it. No ``main.py``, no hardcoded interpreter path, no per-machine setup.


The Typed Script Filter API
------------------------------------------------------------------------------

Alfred's Script Filter speaks JSON. Writing that JSON by hand is fragile — a typo in a key name produces no error, just a silently broken workflow. ``afwf`` gives you a proper Python API instead.

**Item**

.. code-block:: python

    from afwf.api import Item

    item = (
        Item(
            title="Alfred Documentation",
            subtitle="Open in browser",
            arg="https://www.alfredapp.com/help/",
        )
        .open_url("https://www.alfredapp.com/help/")          # Enter → open URL
        .add_modifier(mod="cmd", subtitle="Copy URL", arg="https://www.alfredapp.com/help/")
    )

``Item`` covers the full `Alfred Script Filter JSON spec <https://www.alfredapp.com/help/workflows/inputs/script-filter/json/>`_ — title, subtitle, arg, uid, icon, modifiers, variables, and more. Methods are chainable.

**ScriptFilter**

.. code-block:: python

    from afwf.api import ScriptFilter

    sf = ScriptFilter()
    sf.items.append(item)

    sf.to_script_filter()   # → dict, useful in unit tests
    sf.send_feedback()      # → writes JSON to stdout, picked up by Alfred


The uvx Deployment Model
------------------------------------------------------------------------------

The old workflow deployment story is painful:

- A virtualenv lives inside the workflow directory, bloating it with tens of MB of packages.
- The Python interpreter path is hardcoded in Alfred's Script field.
- That path breaks whenever the venv moves, Python upgrades, or you switch machines.
- Every new machine needs the same manual setup.

The ``uvx`` model cuts all of this out. Publish your workflow logic to PyPI, then point Alfred at it:

.. code-block:: bash

    ~/.local/bin/uvx your-package@1.0.0 subcommand --query '{query}'

``uvx`` resolves, downloads, and caches the exact version on first run. Nothing to install. Nothing to configure. Upgrading is a one-character change in Alfred's Script field.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Before
     - With uvx
   * - Hardcoded ``.venv/bin/python`` in Alfred
     - ``uvx pkg@version subcommand``
   * - Breaks on Python upgrade or venv move
     - Self-contained, always works
   * - Manual setup on every machine
     - Zero setup — cached on first run
   * - Version drift across machines
     - Version pinned in the Script field

See :doc:`../12-uvx-Deployment-Model/index` for the full walkthrough.


Optional Utilities
------------------------------------------------------------------------------

**Fuzzy ranking** (``afwf.opt.fuzzy_item``)

Sort a list of Items by relevance to a query string. Built on `rapidfuzz <https://pypi.org/project/rapidfuzz/>`_.

.. code-block:: python

    from afwf.opt.fuzzy_item.api import Item, FuzzyItemMatcher

    items = [Item(title=t).set_fuzzy_match_name(t) for t in ["Alfred", "Python", "GitHub"]]
    results = FuzzyItemMatcher.from_items(items).match("pyth", threshold=0)
    # → [Item("Python"), ...]

**Disk cache** (``afwf.opt.cache``)

Persist expensive results — API responses, filesystem scans — between Alfred invocations. Built on `diskcache <https://pypi.org/project/diskcache/>`_.


Programmatic Access to Alfred and Your Project
------------------------------------------------------------------------------

``afwf`` also exposes the Alfred runtime environment and your project layout as first-class Python objects,
so scripts, build tools, and tests can navigate paths without hardcoding anything.

**AlfredPreferences** — the Alfred preferences folder

.. code-block:: python

    from afwf.api import AlfredPreferences

    prefs = AlfredPreferences()
    prefs.dir_alfred_preferences   # Path to Alfred.alfredpreferences
    prefs.dir_workflows            # …/workflows/

    # iterate every installed workflow
    for wf in prefs.list_workflows():
        print(wf.name, wf.bundle_id, wf.version)

    # look up one workflow by its UUID
    wf = prefs.get_workflow("76458317-5B0A-40E7-A328-DC6C900EC1B9")

``AlfredPreferences`` reads ``~/Library/Application Support/Alfred/prefs.json`` to locate the
active preferences folder (which may live on a sync drive), so it works regardless of where
Alfred is configured to store its data.

**AlfredWorkflow** — a single workflow directory

.. code-block:: python

    from afwf.api import AlfredWorkflow
    from pathlib import Path

    wf = AlfredWorkflow(dir_workflow=Path("…/workflows/user.workflow.<UUID>"))

    wf.workflow_id     # UUID string extracted from the folder name
    wf.name            # human-readable name from info.plist
    wf.bundle_id       # reverse-DNS bundle id, e.g. "MacHu-GWU.my-workflow"
    wf.version         # version string, e.g. "1.0.0"
    wf.description     # short description
    wf.created_by      # author
    wf.web_address     # homepage / repo URL
    wf.disabled        # bool — is the workflow currently disabled?

All attributes are lazy: ``info.plist`` is only parsed on first access.

**AfwfProject** — binds your source repo to its deployed workflow folder

.. code-block:: python

    from afwf.api import AlfredPreferences, AfwfProject
    from pathlib import Path

    prefs = AlfredPreferences()
    wf = prefs.get_workflow("76458317-5B0A-40E7-A328-DC6C900EC1B9")

    proj = AfwfProject(
        dir_project_root=Path("~/my-workflow"),
        alfred_workflow=wf,
    )

    # source-side paths
    proj.package_name              # from [project] name in pyproject.toml
    proj.dir_package               # <root>/<package_name>/
    proj.path_project_info_plist   # info.plist checked into VCS
    proj.path_project_icon_png     # icon.png checked into VCS

    # workflow-side paths
    proj.alfred_workflow.dir_workflow   # the live Alfred folder
    proj.alfred_workflow.path_info_plist

``AfwfProject`` is useful in build scripts that sync ``info.plist`` / ``icon.png`` between the
Alfred folder and the git repo, or that inspect the deployed version before publishing to PyPI.
