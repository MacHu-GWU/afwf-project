# -*- coding: utf-8 -*-

"""

"""

import typing as T
import sys
import json
import traceback
from datetime import datetime

import attr
from attrs_mate import AttrsClass

from .handler import Handler
from .path import dir_lib, dir_afwf, p_last_error, p_debug_log
from .script_filter import ScriptFilter
from .item import Icon, Item
from .icon import IconFileEnum


def log_last_error():  # pragma: no cover
    """
    Log the last exception trace back info to ``~/.alfred-afwf/last-error.txt``
    file.
    """
    traceback_msg = traceback.format_exc()
    try:
        p_last_error.write_text(traceback_msg, encoding="utf-8")
    except FileNotFoundError:
        dir_afwf.mkdir(parents=True, exist_ok=True)
        p_last_error.write_text(traceback_msg, encoding="utf-8")
    except Exception as e:
        raise e


def log_debug_info(info: str):  # pragma: no cover
    """
    Call this function anywhere. It will append the ``info`` string to the end
    of ``~/.alfred-afwf/debug.txt`` file.
    """
    try:
        with p_debug_log.open("a", encoding="utf-8") as f:
            f.write(info + "\n")
    except FileNotFoundError:
        dir_afwf.mkdir(parents=True, exist_ok=True)
        with p_debug_log.open("a", encoding="utf-8") as f:
            f.write(info + "\n")
    except Exception as e:
        raise e


@attr.define
class Workflow(AttrsClass):
    """
    Represents an Alfred Workflow object. The workflow can register many handlers.

    Each handler will be responsible for a Script Filter implementation.

    [CN]

    表示一个 Alfred Workflow 对象. 一个 workflow 可以注册多个 handler. 每个 handler
    对应着一个 Script Filter 的实现.
    """
    handlers: T.Dict[str, Handler] = attr.ib(factory=dict)

    def __attrs_post_init__(self):
        if dir_lib.exists():
            sys.path.append(str(dir_lib))

    def register(self, handler: Handler):
        """
        Register a handler to the workflow.
        """
        if handler.id in self.handlers:
            raise KeyError
        else:
            self.handlers[handler.id] = handler

    def get(self, handler_id: str) -> Handler:
        """
        Get handler by id.
        """
        return self.handlers[handler_id]

    def _run(
        self,
        arg: T.Optional[str] = None,
        debug: bool =False,
    ) -> ScriptFilter:
        """
        Low level script filter runner. It locates the handler by ``handler_id``,
        and then call the handler to generate the script filter result, and then
        flush the result to stdout, hence you can see it in the drop-down menu.

        :param debug: flag to turn on debug.
        """
        if debug:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_debug_info(f"--- run script filter at {now} ---")

        if arg is None:
            arg = sys.argv[1]  # in format of "{handler_id} {query}"

        if debug:
            log_debug_info(f"received argument is: {arg!r}")

        handler_id, query = arg.split(" ", 1)

        if debug:
            log_debug_info(f"received handler_id is: {handler_id!r}")
            log_debug_info(f"received query is: {query!r}")

        handler = self.get(handler_id)
        sf = handler.handler(query)
        json.dump(sf.to_script_filter(), sys.stdout)
        sys.stdout.flush()
        return sf

    def run(
        self,
        arg: T.Optional[str] = None,
        debug: bool = False,
    ):
        """
        High level script filter runner.

        :param debug: flag to turn on debug.

        By default, it provides two ways to debug:

        1. Automatically log the python traceback logs to ``~/.alfred-afwf/last-error.txt``
            file.
        2. If python raises any exception, log the last Exception message as an item.
        """
        try:
            self._run(arg=arg, debug=debug)
        except Exception as e:
            if debug:
                log_last_error()
            sf = ScriptFilter()

            item = Item(
                title=f"Error: {e}",
                subtitle=f"Open {str(p_last_error)} to see details",
                icon=Icon.from_image_file(IconFileEnum.error),
                arg=str(p_last_error),
            )
            item._open_log_file(path=str(p_last_error))
            sf.items.append(item)

            item = Item(
                title=f"Open debug log file",
                subtitle=f"Open {str(p_debug_log)} to see details",
                icon=Icon.from_image_file(IconFileEnum.debug),
                arg=str(p_debug_log),
            )
            item._open_log_file(path=str(p_debug_log))
            sf.items.append(item)

            json.dump(sf.to_script_filter(), sys.stdout)
            sys.stdout.flush()
            exit(1)
        exit(0)
