
.. image:: https://readthedocs.org/projects/afwf/badge/?version=latest
    :target: https://afwf.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/afwf-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/afwf-project/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf-project

.. image:: https://img.shields.io/pypi/v/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/pypi/l/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/pypi/pyversions/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://afwf.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://afwf.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://afwf.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/afwf#files


Welcome to ``afwf`` Documentation
==============================================================================

Alfred Workflow Script Filter power tool.


Summary
------------------------------------------------------------------------------
`Alfred 官方的 Python 包 <https://www.deanishe.net/alfred-workflow/>`_ 已经 5 年没有更新了, 而且只支持 Python2.7, 不支持 Python3. 因为 2.7 已经在 2020 年 1 月 1 日停止更新, 而且 MacOS 2021 年起操作系统内就不带 Python2.7 了, 所以这导致以前使用了官方包的 Workflow 对新 Mac 不再兼容. 并且由于兼容性和历史包袱的原因, 官方的 Python 包内置了太多本应由第三方库提供的功能, 例如 HTTP request, 缓存 等等, 而为了兼容性只能在垃圾代码上堆叠垃圾代码. 于是我就萌生了自己造一个极简的轮子的想法.

这个项目的目的是提供了用 Python 编写 Alfred Workflow 中需要用到的 Script Filter 的数据模型, 以及一套基于超大型内部企业项目 (我是 AWS 内部官方的 AWS Alfred Workflow 的作者) 经验总结出的一套开发 Python Alfred Workflow 的最佳实践. 解决了 Workflow 中的控件太多, 测试不易等问题.


.. _install:

Install
------------------------------------------------------------------------------
``afwf`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install afwf

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade afwf


Best Practice
------------------------------------------------------------------------------
**Script Filter 控件的设置**

最佳实践中, Script Filter 的设置应该是这样的

- with space: checked
- Language: /bin/bash
- with input as {query}
- run behavior:
    - Queue Mode: Terminate previous script
    - Queue Delay: Immediately after each character typed
    - Always run immediately for first typed arg character: checked
    - Argument: Automatically trim irrelevant arg whitespaces
    - Don't set argv when query is empty: unchecked
- Escaping: double quotes, backslashes

然后 Script 里这么写:

.. code-block:: bash

    /path/to/python main.py 'handler_id {query}'

这里 ``/path/to/python`` 是你想要使用的 Python 解释器的路径, 你可以用 `pyenv <https://github.com/pyenv/pyenv>`_ 安装任何你想要的 Python 版本, 甚至是已经不再更新的 Python2.7.

而 main.py 则是一个入口, 它的内容和本项目中的 main.py 应该类似, 里面没有真正的业务逻辑. 真正的业务逻辑在 ``from my_project import wf`` 中的 Workflow 对象里.

而 handler_id 是一个字符串, 唯一对应一个 Python "handler" 函数. 所谓 "handler" 就是一个 python 函数, 接受一个 '{query}' 的字符串输入, 创建一个 Workflow 对象, 返回一些 Item. 简单来说就是一个功能. 这种方式能让开发者将多个不同的 handler 绑定到一个 Workflow 上, 并且实现互相调用. 由于 handler 的本质是 Python 函数, 所以是很容易测试的.

具体例子请参考 `example_wf <./afwf/example_wf>`_ 这个示例项目.
