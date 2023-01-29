# -*- coding: utf-8 -*-

import typing as T
import sys
import json

import attr
from attrs_mate import AttrsClass

from .script_filter_object import ScriptFilterObject
from .item import Item


@attr.define
class ScriptFilter(ScriptFilterObject):
    """
    The script filter return object that flush out to standard out.

    :param items: list of items object that for drop down menu
    :param variables: session level variables. items also has item level
        variables, this feature won't be used for 99% of the time
    :param rerun: 0.1 ~ 5.0 if available, the script will only be re-run
        if the script filter is still active and the user hasn't changed
        the state of the filter by typing and triggering a re-run.

    Ref:

    - https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """
    items: T.List[Item] = Item.ib_list_of_nested()
    variables: dict = AttrsClass.ib_dict(default=None)
    rerun: float = AttrsClass.ib_float(default=None)

    def to_script_filter(self) -> dict:
        dct = super(ScriptFilter, self).to_script_filter()
        if "items" not in dct:
            dct["items"] = list()
        return dct

    def send_feedback(self):
        """
        Flush script filter object to standard output.
        """
        json.dump(self.to_script_filter(), sys.stdout, ensure_ascii=False)
        sys.stdout.flush()
