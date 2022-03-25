# -*- coding: utf-8 -*-

import sys
import json
from typing import Any, Type, Union, List, Tuple, Dict

import attr
from attrs_mate import AttrsClass

from .script_filter_object import ScriptFilterObject
from .item import Item


@attr.define
class ScriptFilter(ScriptFilterObject):
    items: List[Item] = Item.ib_list_of_nested()
    variables: dict = AttrsClass.ib_dict(default=None)
    rerun: float = AttrsClass.ib_float(default=0.0)

    def to_script_filter(self) -> dict:
        dct = super().to_script_filter()
        if "items" not in dct:
            dct["items"] = list()
        return dct

    def send_feedback(self):
        json.dump(self.to_script_filter(), sys.stdout, ensure_ascii=False)
        sys.stdout.flush()
