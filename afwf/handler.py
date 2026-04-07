# -*- coding: utf-8 -*-

"""
Alfred workflow handler module.
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from .vendor.better_pathlib import temp_cwd
from .script_filter import ScriptFilter

import subprocess


class Handler(BaseModel):
    """
    A Handler owns the business logic for one Alfred Script Filter widget.

    A workflow typically contains several Script Filter widgets, each mapped to
    one ``Handler`` instance via a unique string ``id``.  The Script Filter's
    *Script* field should be set to::

        /path/to/python main.py '{handler_id} {query}'

    When Alfred runs that command, ``main.py`` looks up the handler by its
    ``id``, then calls :meth:`handler` with the raw query string.

    **Execution flow**::

        Alfred types → Script Filter runs main.py
            └─ handler(query)
                  ├─ parse_query(query)  →  {"keyword": "foo", "arg": "bar"}
                  └─ main(keyword="foo", arg="bar")  →  ScriptFilter

    **Abstract methods to implement**

    You must subclass ``Handler`` and implement three methods that form a
    matched triple:

    - :meth:`parse_query`   — raw query string  →  kwargs dict
    - :meth:`main`          — kwargs dict        →  ScriptFilter
    - :meth:`encode_query`  — kwargs dict        →  raw query string  *(inverse of parse_query)*

    Example::

        class MyHandler(Handler):
            def parse_query(self, query: str) -> dict:
                # "python hello" → {"lang": "python", "keyword": "hello"}
                parts = query.strip().split(maxsplit=1)
                return {"lang": parts[0], "keyword": parts[1] if len(parts) > 1 else ""}

            def encode_query(self, lang: str, keyword: str) -> str:
                return f"{lang} {keyword}"

            def main(self, lang: str, keyword: str) -> ScriptFilter:
                sf = ScriptFilter()
                sf.items.append(Item(title=f"[{lang}] {keyword}"))
                return sf

        handler = MyHandler(id="my_handler")
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str

    def main(self, **kwargs) -> ScriptFilter:  # pragma: no cover
        """
        Core business logic. **Must be overridden.**

        Receives the structured parameters produced by :meth:`parse_query` and
        returns a :class:`~afwf.script_filter.ScriptFilter` whose ``items``
        list populates the Alfred dropdown.

        Design intent: keep this method free of Alfred-specific I/O so it can
        be unit-tested directly::

            sf = handler.main(keyword="hello")
            assert sf.items[0].title == "hello"

        :param kwargs: keyword arguments matching :meth:`parse_query`'s return value.
        :return: :class:`~afwf.script_filter.ScriptFilter` to send to Alfred.
        """
        raise NotImplementedError

    def parse_query(self, query: str) -> dict[str, Any]:  # pragma: no cover
        """
        Parse the raw Alfred query string into structured keyword arguments.
        **Must be overridden.**

        The returned dict's keys must match the parameter names of :meth:`main`.
        Even for an empty query string, all expected keys must be present.

        :param query: the raw query string Alfred appends after the keyword,
            e.g. ``"python hello"`` when the user types ``myworkflow python hello``.
        :return: dict of kwargs to pass directly to :meth:`main`.
        """
        raise NotImplementedError

    def encode_query(self, **kwargs) -> str:  # pragma: no cover
        """
        Encode structured parameters back into a query string.
        **Must be overridden.**

        This is the inverse of :meth:`parse_query`.  It is used by
        :meth:`encode_run_script_command` to build the bash command string
        that Alfred's "Run Script" action will execute.

        :param kwargs: keyword arguments matching :meth:`main`'s signature.
        :return: query string that :meth:`parse_query` would parse back to the
            same kwargs.
        """
        raise NotImplementedError

    def handler(self, query: str) -> ScriptFilter:  # pragma: no cover
        """
        Entry point called by ``main.py``.

        Chains :meth:`parse_query` → :meth:`main` so that ``main.py`` only
        needs to call ``handler.handler(query)`` without knowing the internal
        parameter structure.

        :param query: raw query string from Alfred.
        :return: :class:`~afwf.script_filter.ScriptFilter` ready to send.
        """
        return self.main(**self.parse_query(query))

    def encode_run_script_command(
        self,
        bin_python: str | Path,
        **kwargs,
    ) -> str:  # pragma: no cover
        """
        Build the bash command string for Alfred's "Run Script" action.

        Use this when pressing Enter should trigger a Python function rather
        than a built-in Alfred action.  Set the item's ``arg`` to the string
        this method returns, then wire it to a "Run Script" widget.

        Example::

            cmd = handler.encode_run_script_command(
                bin_python="/usr/bin/python3",
                lang="python",
                keyword="hello",
            )
            # → "/usr/bin/python3 main.py 'my_handler python hello'"
            item.run_script(cmd=cmd)

        :param bin_python: absolute path to the Python interpreter used by the
            workflow (e.g. ``sys.executable`` or a virtualenv path).
        :param kwargs: keyword arguments forwarded to :meth:`encode_query`.
        :return: bash command string that Alfred will execute.
        """
        return f"{bin_python} main.py '{self.id} {self.encode_query(**kwargs)}'"

    def run_script_command(
        self,
        bin_python: str | Path,
        dir_workflow: str | Path,
        query: str,
        verbose: bool = False,
    ) -> str | None:  # pragma: no cover
        """
        Simulate Alfred executing the Script Filter and return its JSON output.

        Useful for debugging when the Alfred UI behaves unexpectedly — runs the
        same subprocess command that Alfred would run, from the workflow
        directory, and captures stdout.

        Example::

            output = handler.run_script_command(
                bin_python="/usr/bin/python3",
                dir_workflow="/path/to/workflow",
                query="python hello",
                verbose=True,
            )
            # prints the command and the raw JSON Alfred would receive

        :param bin_python: absolute path to the Python interpreter.
        :param dir_workflow: absolute path to the workflow directory
            (``…/Alfred.alfredpreferences/workflows/user.workflow.XXXX``).
        :param query: the query string as if typed in Alfred.
        :param verbose: if ``True``, prints the command and JSON response.
        :return: the JSON string Alfred would receive, or ``None`` on no output.
        """
        args = [str(bin_python), "main.py", f"{self.id} {query}"]
        if verbose:
            print(f"run: {bin_python} main.py '{self.id} {query}'")

        with temp_cwd(dir_workflow):
            res = subprocess.run(args, capture_output=True, check=True)
            response = res.stdout.decode("utf-8")
            if verbose:
                print(response)

        return response
