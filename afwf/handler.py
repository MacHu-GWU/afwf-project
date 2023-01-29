# -*- coding: utf-8 -*-

"""

"""

import typing as T

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

    你在 Script Filter 中的 Script 一栏中填写如下信息的时::

        ${path_to_python} main.py '${handler_id} ${query}'

    其行为等效于使用 ``${path_to_python}`` 的 Python 解释器, 调用跟 ``${handler_id}``
    所对应的 :class:`Handler` 类中的 ``handler(query)`` 方法.

    Handler 必须实现下面这些抽象函数.

    - :meth:`~afwf.handler.Handler.main`
    - :meth:`~afwf.handler.Handler.parse_query`
    - :meth:`~afwf.handler.Handler.encode_query`
    """

    id = AttrsClass.ib_str(nullable=False)

    def main(self, **kwargs) -> ScriptFilter:
        """
        [CN]

        用来处理 Script Filter 的具体业务逻辑的主函数. 是一个抽象函数.

        该函数必须返回一个 :class:`~afwf.script_filter.ScriptFilter` 对象, 里面包含了
        Alfred 对话框里的 Drop Down Menu 中的 :class:`~afwf.item.Item` 对象.
        """
        raise NotImplementedError

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        """
        [CN]

        一个抽象函数. 用来解析 Script Filter 传入的 query 字符串. 返回的字典要和
        :meth:`~afwf.handler.Handler.main` 中的参数一一对应.
        """
        raise NotImplementedError

    def encode_query(self, **kwargs) -> str:
        """
        [CN]

        一个抽象函数. 用来将结构化的参数编码为字符串. 该函数的参数要和
        :meth:`~afwf.handler.Handler.main` 中的参数一一对应.
        """
        raise NotImplementedError

    def handler(self, query: str) -> ScriptFilter:
        """
        [CN]

        对 :meth:`~afwf.handler.Handler.main` 进行的一层封装.
        只不过接收的参数是一个 query string, 也就是你在 Script Filter Widget
        里面定义的 ``python3 main.py '{handler_id} {query}'`` 中的 query 部分.

        该函数的主要工作是调用 :meth:`~afwf.handler.Handler.parse_query`, 将 query
        解析成结构化的参数, 然后传给 :meth:`~afwf.handler.Handler.main` 进行处理.
        """
        return self.main(**self.parse_query(query))

    def encode_run_script_command(
        self,
        bin_python: str,
        **kwargs,
    ) -> str:
        """
        将 :meth:`~afwf.handler.Handler.main` 中的参数编码为 Alfred Workflow 中的
        Run Script 的 bash command.
        """
        return f"{bin_python} main.py '{self.id} {self.encode_query(**kwargs)}'"
