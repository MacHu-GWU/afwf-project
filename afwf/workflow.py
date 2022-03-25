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
from .path import dir_afwf, p_last_error, p_debug_log
from .script_filter import ScriptFilter
from .item import Icon, Item
from .icon import IconEnum


def log_last_error():  # pragma: no cover
    """
    Log the last exception trace back info to ``~/.alfred-afwf/last-error.txt``
    file.
    """
    traceback_msg = traceback.format_exc()
    try:
        p_last_error.write_text(traceback_msg)
    except FileNotFoundError:
        dir_afwf.mkdir_if_not_exists()
        p_last_error.write_text(traceback_msg)
    except Exception as e:
        raise e


def log_debug_info(info: str):  # pragma: no cover
    """
    Call this function anywhere. It will append the ``info`` string to the end
    of ``~/.alfred-afwf/debug.txt`` file.
    """
    try:
        with p_debug_log.open("a") as f:
            f.write(info + "\n")
    except FileNotFoundError:
        dir_afwf.mkdir_if_not_exists()
        with p_debug_log.open("a") as f:
            f.write(info + "\n")
    except Exception as e:
        raise e


@attr.define
class Workflow(AttrsClass):
    """
    dai
    """
    handlers: Dict[str, Handler] = attr.ib(factory=dict)

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
        if debug:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_debug_info(f"--- run script filter at {now} ---")

        arg = sys.argv[1]  # "{handler_id} {query}"

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
        try:
            self._run(debug=debug)
        except Exception as e:
            log_last_error()
            sf = ScriptFilter()
            log_debug_info(IconEnum.error)
            item = Item(
                title=f"Error: ",
                subtitle=f"Open {p_last_error.abspath} to see details",
                icon=Icon(path=IconEnum.error, type=Icon.TypeEnum.filetype.value),
                arg=p_last_error.abspath,
            )
            item.open_file(path=p_last_error.abspath)
            sf.items.append(item)
            json.dump(sf.to_script_filter(), sys.stdout)
            sys.stdout.flush()
            exit(1)
        exit(0)
