# -*- coding: utf-8 -*-

"""
Alfred workflow handler module.
"""

import typing as T
import subprocess
from pathlib import Path

import attrs
from attrs_mate import AttrsClass
from .vendor.better_pathlib import temp_cwd

from .script_filter import ScriptFilter


@attrs.define
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

    Handler 必须实现下面这些抽象方法.

    - :meth:`~afwf.handler.Handler.main`
    - :meth:`~afwf.handler.Handler.parse_query`
    - :meth:`~afwf.handler.Handler.encode_query`
    """

    id = AttrsClass.ib_str(nullable=False)

    def main(self, **kwargs) -> ScriptFilter:  # pragma: no cover
        """
        [CN]

        用来处理 Script Filter 的具体业务逻辑的主方法. 是一个抽象方法. 你需要 override 这个方法
        并给予具体的实现.

        该方法可以接收任何自定义的参数, 并必须返回一个 :class:`~afwf.script_filter.ScriptFilter` 对象,
        里面包含了Alfred 对话框里的 Drop Down Menu 中的 :class:`~afwf.item.Item` 对象.

        在设计上, 这个方法应该着眼于核心业务逻辑, 并且可以被单元测试充分覆盖. 在单元测试中,
        你可以调用这个方法传入各种可能得参数组合, 并返回一个 :class:`~afwf.script_filter.ScriptFilter`,
        然后检查里面的 items 是否符合预期.
        """
        raise NotImplementedError

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:  # pragma: no cover
        """
        [CN]

        一个抽象方法. 用来解析 Script Filter 传入的 query 字符串. 返回的字典要和
        :meth:`~afwf.handler.Handler.main` 中的参数一一对应. 注意, 即使是空字符串,
        返回的字典也必须包含所有的参数.

        :param query: 你在 Alfred Workflow UI 中跟在 keyword 之后的 query 字符串.

        :return: 一个字典, 它和 :meth:`~afwf.handler.Handler.main` 中的参数一一对应.
        """
        raise NotImplementedError

    def encode_query(self, **kwargs) -> str:  # pragma: no cover
        """
        [CN]

        一个抽象方法. 用来将结构化的参数编码为字符串. 该方法的参数要和
        :meth:`~afwf.handler.Handler.main` 中的参数一一对应.
        """
        raise NotImplementedError

    def handler(self, query: str) -> ScriptFilter:  # pragma: no cover
        """
        [CN]

        该方法对 :meth:`~afwf.handler.Handler.main` 进行的一层封装.
        只不过接收的参数是一个 query string, 也就是你在 Script Filter Widget
        里面定义的 ``/usr/bin/python3 main.py '{handler_id} {query}'`` 中的 query 部分.

        该方法的主要工作是调用 :meth:`~afwf.handler.Handler.parse_query`, 将 query
        解析成结构化的参数, 然后传给 :meth:`~afwf.handler.Handler.main` 进行处理.

        :param query: 你在 Alfred Workflow UI 中跟在 keyword 之后的 query 字符串.

        :return: :class:`~afwf.script_filter.ScriptFilter` 对象.
        """
        return self.main(**self.parse_query(query))

    def encode_run_script_command(
        self,
        bin_python: T.Union[str, Path, T.Any],
        **kwargs,
    ) -> str:  # pragma: no cover
        """
        将 :meth:`~afwf.handler.Handler.main` 中的参数编码为 Alfred Workflow 中的
        Run Script 的 bash command. 当你定义按下 Enter 后所对应的行为是执行某个复杂的
        Python 函数的时候, 该方法就可以将 bash command 编码为 arg, 并传给 "Run Script" action.

        :param bin_python: 运行 Alfred Workflow 所用的 Python 解释器的绝对路径.

        :return: Alfred Workflow 中的 Script Filter 底层实际执行的 bash command 命令.
        """
        return f"{bin_python} main.py '{self.id} {self.encode_query(**kwargs)}'"

    def run_script_command(
        self,
        bin_python: T.Union[str, Path, T.Any],
        dir_workflow: T.Union[str, Path, T.Any],
        query: str,
        verbose: bool = False,
    ) -> T.Optional[str]:  # pragma: no cover
        """
        模拟 Alfred Workflow UI 中的行为. 执行 UI 界面底层对应的 ``Script``.
        当 UI 工作不符合预期时, 可以用这个方法 debug, 执行底层的 Python 代码.

        :param bin_python: 运行 Alfred Workflow 所用的 Python 解释器的绝对路径.
        :param dir_workflow: Alfred Workflow 中
            ``/path/to/Alfred.alfredpreferences/workflows/user.workflow.ABCD1234-A1B2-C3D4-E5F6-A1B2C3D4E5F6``
            这个目录的绝对路径.
        :param query: 你在 Alfred UI 中输入的 query 内容.
        :param verbose: 是否打印出执行的 bash command.

        :return: Alfred Workflow 中的 Script Filter 底层实际执行的 bash command 命令
            所返回的 JSON 字符串. 如果是 None 则表示该命令没有返回值.
        """
        args = [
            f"{bin_python}",
            "main.py",
            f"{self.id} {query}",
        ]
        cmd = f"{bin_python} main.py '{self.id} {query}'"
        if verbose:
            print(f"run: {cmd}")

        with temp_cwd(dir_workflow):
            res = subprocess.run(args, capture_output=True, check=True)
            response = res.stdout.decode("utf-8")
            if verbose:
                print(response)

        return response
