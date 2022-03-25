# -*- coding: utf-8 -*-

"""

"""

import attr
from attrs_mate import AttrsClass


@attr.define
class ScriptFilterObject(AttrsClass):
    """
    [CN]

    根据 Alfred 的 `官方文档 <https://www.alfredapp.com/help/workflows/inputs/script-filter/json/>`_
    Script Filter 是一个 JSON 的数据结构. 但这个 JSON 数据结构与 Python OOP 的序列化接口
    有差别. OOP 序列化接口是为了能从 JSON 中还原 object. 而 Script Filter 接口是为
    Alfred 服务的. 例如 OOP 中如果一个 attribute 的值为 None, 那么序列化后还是需要保留
    这个值. Script Filter 中如果一个 attribute 被解读为 Omit, 这个 attribute 就彻底
    不应该存在, 不然会出现歧义. 所以 ScriptFilterObject 是一种特殊的对象, 同时提供了
    OOP 序列化接口 和 Script Filter 序列化接口.
    """

    def to_script_filter(self) -> dict:
        """
        Convert object to Alfred Workflow Script Filter friendly dictionary.
        """
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
