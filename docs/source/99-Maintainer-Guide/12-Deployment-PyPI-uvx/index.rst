.. _Deployment-PyPI-uvx:

Deployment: PyPI and uvx
==============================================================================

Once workflow logic is stable, publishing it as a PyPI package makes
distribution trivial.  Alfred users install the workflow once and upgrade by
changing a single version string — no virtualenv management, no ``pip install``,
no per-machine setup.


Why uvx
------------------------------------------------------------------------------

``uvx`` (part of `uv <https://docs.astral.sh/uv/>`_) downloads a package from
PyPI, caches it in ``~/.cache/uv/``, and runs the requested entry point — all
in one command.  From the workflow's perspective it behaves like a normal
binary:

.. code-block:: bash

    ~/.local/bin/uvx --from afwf==1.0.1 \
        afwf-examples search-bookmarks --query '{query}'

On the first call ``uvx`` downloads ``afwf==1.0.1`` and its dependencies.
Subsequent calls reuse the cache — the latency added to Alfred invocations is
negligible after the first run.

The version pin (``afwf==1.0.1``) guarantees that every machine runs the same
code.  Rolling back to a previous version is a one-line change in Alfred's
Script field.


Package Entry Point
------------------------------------------------------------------------------

The entry point is declared in ``pyproject.toml``:

.. code-block:: toml

    [project.scripts]
    afwf-examples = "afwf.examples.cli:main"

``uvx --from afwf`` makes ``afwf-examples`` available as a command for the
duration of that invocation.  No installation into ``/usr/local/bin`` or
``~/.local/bin`` occurs.

If your workflow uses optional extras (fuzzy matching, disk cache), declare
them in the ``uvx`` call:

.. code-block:: bash

    ~/.local/bin/uvx --from "afwf[fuzzy,cache]==1.0.1" \
        afwf-examples search-bookmarks --query '{query}'


Release Checklist
------------------------------------------------------------------------------

1. **Bump the version** in ``afwf/_version.py`` and confirm ``pyproject.toml``
   reads from it (or update both if they are separate).

2. **Update ``release-history.rst``** with the change summary for the new version.

3. **Run the full test suite** to confirm nothing is broken:

   .. code-block:: bash

       mise run cov

4. **Build and publish** to PyPI.  The project uses the standard ``uv`` workflow:

   .. code-block:: bash

       uv build
       uv publish

   CI (``mise run publish`` or the GitHub Actions workflow) automates this on
   tag push.

5. **Update the Script field** in Alfred's workflow for each Script Filter that
   needs the new version:

   .. code-block:: bash

       # Before
       ~/.local/bin/uvx --from afwf==1.0.0 afwf-examples search-bookmarks --query '{query}'

       # After
       ~/.local/bin/uvx --from afwf==1.0.1 afwf-examples search-bookmarks --query '{query}'

   This change goes into ``info.plist`` in the ``script`` field of each
   affected Script Filter node.  Commit it so the repo stays in sync with
   the released version.

6. **Export and redistribute** the updated ``info.plist`` as a new
   ``.alfredworkflow`` bundle if you distribute the workflow to other users.


Dev vs Production Side by Side
------------------------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Aspect
     - Dev (local venv)
     - Production (uvx)
   * - Script field
     - ``.venv/bin/afwf-examples search-bookmarks --query '{query}'``
     - ``uvx --from afwf==1.0.1 afwf-examples search-bookmarks --query '{query}'``
   * - Python environment
     - Project's ``.venv``
     - uvx cache (``~/.cache/uv/``)
   * - Code changes
     - Immediate (no reinstall needed)
     - Requires new PyPI release + version bump
   * - ``sys.executable``
     - ``.venv/bin/python``
     - uvx-managed interpreter; ``../afwf-examples`` still resolves correctly
   * - Extras
     - Installed via ``mise run inst``
     - ``uvx --from "afwf[fuzzy,cache]==..."``


Keeping info.plist in Sync
------------------------------------------------------------------------------

``info.plist`` in the repository should always reflect the *dev* invocation
paths so that cloning the repo and running ``mise run inst`` gives a working
workflow immediately.  The production ``uvx`` paths live only in Alfred's
installed copy of the workflow, updated manually when a new release is
published.

A useful convention: keep a comment or a separate ``info.plist.production``
snippet in the repo documenting the production script strings, so that
updating Alfred after a release is a straightforward find-and-replace.
