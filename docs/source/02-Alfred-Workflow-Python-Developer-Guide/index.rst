Alfred Workflow Python Developer Guide
==============================================================================


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



如何把 Python 中的数据发送给 Alfred Workflow?

- 参考这段 Alfred 作者的代码: https://github.com/deanishe/alfred-workflow/blob/master/workflow/workflow.py#L2176
- 参考 Script Filter 的编程模型: https://www.alfredapp.com/help/workflows/inputs/script-filter/json/