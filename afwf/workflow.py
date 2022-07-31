# -*- coding: utf-8 -*-

"""
"""

import sys
import json
import traceback
from datetime import datetime
from typing import Dict

import attr
from attrs_mate import AttrsClass

from .handler import Handler
from .path import dir_lib, dir_afwf, p_last_error, p_debug_log
from .script_filter import ScriptFilter
from .item import Icon, Item
from .icon import Icons


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
    """
    handlers: Dict[str, Handler] = attr.ib(factory=dict)

    def __attrs_post_init__(self):
        if dir_lib.exists():
            sys.path.append(str(dir_lib))

    def register(self, handler: Handler):
        """
        """
        if handler.id in self.handlers:
            raise KeyError
        else:
            self.handlers[handler.id] = handler

    def get(self, handler_id: str) -> Handler:
        """
        """
        return self.handlers[handler_id]

    def _run(
        self,
        debug=False,
    ):
        """
        Low level script filter runner
        """
        if debug:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_debug_info(f"--- run script filter at {now} ---")

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

    def run(
        self,
        debug=False,
    ):
        """
        High level script filter runner.

        :param debug:

        By default, it provides two way to debug:

        1. Automatically log the python trace back logs to ``~/.alfred-afwf/last-error.txt``
            file.
        2. If python raises any exception, log the last Exception message as an item.
        """
        try:
            self._run(debug=debug)
        except Exception as e:
            if debug:
                log_last_error()
            sf = ScriptFilter()
            item = Item(
                title=f"Error: ",
                subtitle=f"Open {str(p_last_error)} to see details",
                icon=Icon.from_image_file(Icons.error),
                arg=str(p_last_error),
            )
            item.open_file(path=str(p_last_error))
            sf.items.append(item)
            json.dump(sf.to_script_filter(), sys.stdout)
            sys.stdout.flush()
            exit(1)
        exit(0)
