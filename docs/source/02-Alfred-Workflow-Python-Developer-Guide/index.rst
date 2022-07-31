Alfred Workflow Python Developer Guide
==============================================================================

.. _script-filter-s-script:

Script Filter's script
------------------------------------------------------------------------------
当你输入 keyword + query 后, 后台实际调用的是一条 bash command 命令. 那么这个 bash command 命令应该是什么样子的呢?

我们考虑一个简单的功能, 输入 ``repo {query}``, 功能是搜索你自己的 GitHub 账户下所有 public repo, 根据 query 来 filter 出相关的 repo. 我们直接上结论:

.. code-block:: bash

    # 具体的例子
    ~/.pyenv/versions/3.8.11/bin/python main.py 'search_my_public_repo {query}'

    # 抽象的例子
    {path_to_python_interpreter} main.py '{handler_id} {query}'

说明:

- 这里的 ``{path_to_python_interpreter}`` 是你的 Python 解释器, Mac 12.3 之前自带 Python2, 之后移除了 Python2 只保留了 Python3, 前面这段你可以用来自定义是用哪个 Python 解释器. 你可以用系统自带的 ``/usr/bin/python`` 或是你自己用 pyenv 或是 homebrew 安装的 Python. 我建议使用 pyenv 安装自己想要的 Python 版本.
- **非常重要**, ``{handler_id}`` 决定了具体使用 ``main.py`` 里面的哪个 Python 函数来处理这个 Query. 这么设计的原因是, 通常你希望用一套代码库, 一套 Python 依赖来构建你的 Workflow, 而你的 Workflow 中可能有很多个不同的函数用来处理不同的 Query, 那么你如何告诉你的 Script Filter 该具体使用哪个逻辑来处理这个 Query 呢? 所以在你给 main.py 的参数中永远只有一个, 而这个参数第一个空格之前的永远是 handler_id, 而后面的才是真正的 query. 这样可以让你把复杂的逻辑都交给代码来处理, 而不是在 Alfred Workflow Script Filter 的 menu 中处理.


Script Filter's Configuration
------------------------------------------------------------------------------
当你再 Alfred Workflow 中创建了一个 ``Script Filter`` 的控件后, 会出现一个菜单对这个控件进行配置. 如何配置这个菜单呢?

.. image:: ./script-filter-configuration.png

- Keyword: 没什么好说的
- with space: 勾选, 除非你不需要 query
- Argument Optional: 选这个, 具体的逻辑在代码中处理
- Language: ``/bin/bash``
- with input as {query}: 选这个
- Run behavior
    - Queue mode: 选 Terminate previous script
    - Query delay:
        - 选 Immediately after each character typed, 除非你的处理逻辑耗时很长, 并且你的 query 一般都是很长要打很多次字.
        - 勾选 Always run immediately for first typed arg character
    - Argument:
        - 选 Automatically trim irrelevant arg whitespaces
        - 不勾选 Don't set argv when query is empty
- Alfred filters results: 不要勾线, filter 的功能在你的代码中处理
- Escaping: 只勾选 Double Quotes, Backslashes
- Script: ``{path_to_python_interpreter} main.py '{handler_id} {query}'`` 详情请参考 :ref:`script-filter-s-script`


Send Returned Items to Alfred
------------------------------------------------------------------------------
根据 :ref:`script-filter-programming-model`, 我们知道 Alfred Workflow 的本质就是 输入一个 ``query`` 返回一堆 ``item`` JSON 对象. 那么在 Python 中我们根据 query 计算出一堆 items 的 JSON 对象后, 我们如何将其发送给 Alfred 呢?

请参考下面的代码, 核心的代码其实只有 2 行. 你在计算出想要展示的 items 后, 你要把这些 items 放在一个 Alfred 所规定的 Script Filter Output 的 dict 对象中. 然后将这个对象用 json 序列化并写入 system standard output buffer 中. 也就是 ``json.dump(script_filter_output, sys.stdout)`` 这一行. 由于 Alfred 会监听 ``sys.stdout``, 你如果将 buffer 中的数据刷新到内存, 就会被 Alfred 所捕捉到并显示出来. 具体做法就是 ``sys.stdout.flush()``

.. code-block:: python

    import sys
    import json

    script_filter_output = {
        "items": [
            {"title": "item 1"},
            {"title": "item 2"},
        ]
    }

    json.dump(script_filter_output, sys.stdout)
    sys.stdout.flush()
