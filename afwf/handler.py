# -*- coding: utf-8 -*-

import attr
from attrs_mate import AttrsClass
from .script_filter import ScriptFilter


@attr.define
class Handler(AttrsClass):
    id = AttrsClass.ib_str(nullable=False)

    def lower_level_api(self, **kwargs) -> ScriptFilter:
        raise NotImplementedError

    def handler(self, query: str) -> ScriptFilter:
        raise NotImplementedError
