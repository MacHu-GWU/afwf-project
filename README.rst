
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


.. _install:

Install
------------------------------------------------------------------------------

``afwf`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install afwf

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade afwf



最佳实践中, Script Filter 的设置应该是这样的:

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

handler_id 是一个字符串, 唯一对应一个 python "handler" 函数. 所谓 "handler" 就是一个 python 函数, 接受一个 '{query}' 的字符串输入, 创建一个 Workflow 对象, 返回一些 Item.
