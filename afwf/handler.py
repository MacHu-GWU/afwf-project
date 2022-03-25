# -*- coding: utf-8 -*-

"""

"""

import attr
from attrs_mate import AttrsClass
from .script_filter import ScriptFilter


@attr.define
class Handler(AttrsClass):
    """
    [CN]

    Handler 主要负责处理 Input Output 逻辑. 在 Alfred Workflow 的编程模型中, Input 是
    搜索框的字符串. Output 则是 Drop Down menu 所需的 Item, 以及一些 Variables, Rerun
    Setting. 这些信息被放在 :class:`~afwf.script_filter.ScriptFilter` 这个 Data
    Container 类中.

    Handler 一共有两个必须的 method.

    1. :meth:`~afwf.script_filter.ScriptFilter.lower_level_api`:
    2. :meth:`~afwf.script_filter.ScriptFilter.handler`:
    """
    id = AttrsClass.ib_str(nullable=False)

    def lower_level_api(self, **kwargs) -> ScriptFilter:
        """
        [CN]

        一个传统的 Python 函数, 可以自定义参数, 返回的是一个
        :class:`~afwf.script_filter.ScriptFilter` 对象, 里面包含了 Drop Down Menu
        所需的 Item. **最核心的逻辑将在这个函数中被处理**.
        """
        raise NotImplementedError

    def handler(self, query: str) -> ScriptFilter:
        """
        [CN]

        :meth:`~afwf.script_filter.ScriptFilter.lower_level_api` 的一个 wrapper
        函数. 只不过接收的参数是一个 query string, 也就是你在 Script Filter Widget
        里面定义的 ``python3 main.py '{handler_id} {query}'`` 中的 query 部分.

        该函数的主要工作是将 query 转化成
        :meth:`~afwf.script_filter.ScriptFilter.lower_level_api` 所需的参数.
        """
        raise NotImplementedError
