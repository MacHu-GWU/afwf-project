# -*- coding: utf-8 -*-

"""
Alfred Workflow orchestration.

A :class:`Workflow` collects one or more :class:`~afwf.handler.Handler`
instances and routes Alfred's raw argument string to the right one at
runtime.

Typical project layout::

    my_workflow/
        main.py          ← calls wf.run()
        wf.py            ← creates Workflow, registers handlers
        handlers/
            search.py    ← defines Handler subclass + handler singleton

Typical ``wf.py``::

    from afwf.workflow import Workflow
    from .handlers import search

    wf = Workflow()
    wf.register(search.handler)

Typical ``main.py``::

    from .wf import wf

    if __name__ == "__main__":
        wf.run()

Alfred passes the Script Filter's argument as a single string with the
format ``"{handler_id} {query}"``.  :meth:`Workflow._run` splits on the
first space and delegates to the named handler.
"""

import sys
import traceback
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .handler import Handler
from .paths import path_enum
from .script_filter import ScriptFilter
from .item import Icon, Item
from .icon import IconFileEnum

_dir_afwf = path_enum.dir_afwf
_p_last_error = path_enum.p_last_error
_p_debug_log = path_enum.p_debug_log


def log_last_error():  # pragma: no cover
    """
    Log the last exception traceback to ``~/.alfred-afwf/last-error.txt``.
    """
    traceback_msg = traceback.format_exc()
    try:
        _p_last_error.write_text(traceback_msg, encoding="utf-8")
    except FileNotFoundError:
        _dir_afwf.mkdir(parents=True, exist_ok=True)
        _p_last_error.write_text(traceback_msg, encoding="utf-8")
    except Exception as e:
        raise e


def log_debug_info(info: str):  # pragma: no cover
    """
    Append ``info`` to ``~/.alfred-afwf/debug.txt``.

    Call this anywhere in your workflow code to leave a breadcrumb trail
    for debugging.
    """
    try:
        with _p_debug_log.open("a", encoding="utf-8") as f:
            f.write(info + "\n")
    except FileNotFoundError:
        _dir_afwf.mkdir(parents=True, exist_ok=True)
        with _p_debug_log.open("a", encoding="utf-8") as f:
            f.write(info + "\n")
    except Exception as e:
        raise e


class Workflow(BaseModel):
    """
    Top-level container that owns all handlers for one Alfred workflow.

    Each Script Filter widget in Alfred passes a single argument string with
    the format ``"{handler_id} {query}"``.  :meth:`_run` parses this string,
    looks up the handler by ``handler_id``, and delegates to
    :meth:`~afwf.handler.Handler.handler`.

    Register every handler exactly once before calling :meth:`run`:

    .. code-block:: python

        wf = Workflow()
        wf.register(search_handler)   # id="search"
        wf.register(open_handler)     # id="open"

    Alfred then dispatches based on the prefix:

    * ``"search foo"``  →  ``search_handler.handler("foo")``
    * ``"open bar"``    →  ``open_handler.handler("bar")``

    Use :meth:`_run` in unit tests (returns the :class:`~afwf.script_filter.ScriptFilter`
    object); use :meth:`run` in production (handles exceptions, exits the process).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    handlers: dict[str, Handler] = Field(default_factory=dict)

    def model_post_init(self, __context) -> None:
        pass  # reserved for future initialisation hooks

    def register(
        self,
        handler: Handler,
    ):
        """
        Register a handler with the workflow.

        :raises KeyError: if a handler with the same ``id`` is already registered.
        """
        if handler.id in self.handlers:
            raise KeyError(f"Handler {handler.id!r} is already registered.")
        self.handlers[handler.id] = handler

    def get(
        self,
        handler_id: str,
    ) -> Handler:
        """
        Look up a registered handler by its ``id``.
        """
        return self.handlers[handler_id]

    def _run(
        self,
        arg: str | None = None,
        debug: bool = False,
    ) -> ScriptFilter:
        """
        Low-level runner. Parses ``arg``, dispatches to the matching handler,
        and flushes the result to stdout.

        :param arg: ``"{handler_id} {query}"`` string.  Defaults to
            ``sys.argv[1]`` when ``None``.
        :param debug: if ``True``, logs handler_id, query, and timestamp to
            the debug log file.
        """
        if debug:  # pragma: no cover
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_debug_info(f"--- run script filter at {now} ---")

        if arg is None:  # pragma: no cover
            arg = sys.argv[1]

        if debug:  # pragma: no cover
            log_debug_info(f"received argument is: {arg!r}")

        handler_id, query = arg.split(" ", 1)

        if debug:  # pragma: no cover
            log_debug_info(f"received handler_id is: {handler_id!r}")
            log_debug_info(f"received query is: {query!r}")

        handler = self.get(handler_id)
        sf = handler.handler(query)
        sf.send_feedback()
        return sf

    def run(
        self,
        arg: str | None = None,
        debug: bool = False,
    ):  # pragma: no cover
        """
        High-level runner with built-in error handling.

        On success, exits with code 0.  On any exception, shows two error
        items in Alfred (linking to ``last-error.txt`` and ``debug.txt``),
        and exits with code 1.

        :param arg: passed through to :meth:`_run`.
        :param debug: if ``True``, logs details and persists the traceback on error.
        """
        try:
            self._run(arg=arg, debug=debug)
        except Exception as e:
            if debug:
                log_last_error()
            sf = ScriptFilter()

            item = Item(
                title=f"Error: {e}",
                subtitle=f"Open {str(_p_last_error)} to see details",
                icon=Icon.from_image_file(IconFileEnum.error),
                arg=str(_p_last_error),
            )
            item._open_log_file(path=str(_p_last_error))
            sf.items.append(item)

            item = Item(
                title="Open debug log file",
                subtitle=f"Open {str(_p_debug_log)} to see details",
                icon=Icon.from_image_file(IconFileEnum.debug),
                arg=str(_p_debug_log),
            )
            item._open_log_file(path=str(_p_debug_log))
            sf.items.append(item)

            sf.send_feedback()
            exit(1)
        exit(0)
