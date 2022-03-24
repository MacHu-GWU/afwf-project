# -*- coding: utf-8 -*-

import attr
from attrs_mate import AttrsClass


@attr.define
class ScriptFilterObject(AttrsClass):
    def to_script_filter(self) -> dict:
        dct = dict()
        for k, v in attr.asdict(self, recurse=False).items():
            if v:
                if isinstance(v, ScriptFilterObject):
                    v1 = v.to_script_filter()
                    if v1:
                        dct[k] = v1
                elif isinstance(v, list):
                    lst = list()
                    for i in v:
                        if isinstance(i, ScriptFilterObject):
                            lst.append(i.to_script_filter())
                        else:
                            lst.append(i)
                    dct[k] = lst
                else:
                    dct[k] = v
        return dct
