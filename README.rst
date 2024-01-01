
.. image:: https://readthedocs.org/projects/afwf/badge/?version=latest
    :target: https://afwf.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/afwf-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/afwf-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf-project

.. image:: https://img.shields.io/pypi/v/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/pypi/l/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/pypi/pyversions/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/afwf-project/blob/main/release-history.rst

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
A powerful framework enables fast and elegant development of Alfred Workflows in Python.

📔 See `Full Documentation HERE <https://afwf.readthedocs.io/index.html>`_.


Project Background
------------------------------------------------------------------------------
`Alfred 官方的 Python 包 <https://www.deanishe.net/alfred-workflow/>`_ 已经 5 年没有更新了, 而且只支持 Python2.7, 不支持 Python3. 因为 2.7 已经在 2020 年 1 月 1 日停止更新, 而且 MacOS 2021 年起操作系统内就不带 Python2.7 了, 所以这导致以前使用了官方包的 Workflow 对新 Mac 不再兼容. 并且由于兼容性和历史包袱的原因, 官方的 Python 包内置了太多本应由第三方库提供的功能, 例如 HTTP request, 缓存 等等, 而为了兼容性只能在垃圾代码上堆叠垃圾代码. 于是我就萌生了自己造一个轮子的想法.

我个人同时维护着 10 多个垂直领域的 Alfred Workflow, 早期我的源代码中包含了很多跟业务逻辑无关, 只用于和 Alfred 整合, 自动化测试, 以及元编程的代码. 这些代码在多个项目中有很多重复. 于是我认为有必要讲这些功能抽象出来, 将其封装为一个框架, 以便于在多个项目中复用, 于是就有了这个项目.

这个项目的目的是提供了用 Python 编写 Alfred Workflow 中需要用到的 Script Filter 的数据模型, 以及一套基于超大型内部企业项目 (我是 AWS 内部官方的 AWS Alfred Workflow 的作者) 经验总结出的一套开发 Python Alfred Workflow 的框架, 包含了项目生命周期中的开发, 测试, 发布, 快速迭代等最佳实践, 解决了 Workflow 中的控件太多, 测试不易等问题.

另外, 这个项目提供了互联网领域常用的图标, 你可以 `在这里预览 <https://github.com/MacHu-GWU/afwf-project/blob/main/preview-icons.rst>`_.


Related Projects
------------------------------------------------------------------------------
- `cookiecutter-afwf <https://github.com/MacHu-GWU/cookiecutter-afwf>`_: 一个 Python Alfred Workflow 的项目模板. 我的所有的 Alfred Workflow 的项目都是基于这个模板, 自动生成所需要的所有代码的. 使得我可以专注于项目的业务逻辑, 而不是运维.
- `afwf_example-project <https://github.com/MacHu-GWU/afwf_example-project>`_: 一个使用 ``cookiecutter-afwf`` 生成的示例项目. 可以用来学习如何使用 ``cookiecutter-afwf`` 模版来快速开发 Alfred Workflow.


.. _install:

Install
------------------------------------------------------------------------------
``afwf`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install afwf

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade afwf
