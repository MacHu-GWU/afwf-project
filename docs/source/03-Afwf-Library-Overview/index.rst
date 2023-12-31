``afwf`` Framework Overview
==============================================================================


Summary
------------------------------------------------------------------------------
这篇文档的目标读者是想用 `afwf <https://github.com/MacHu-GWU/afwf-project>`_ 库来开发 Alfred Workflow 的开发者.


Design Philosophy
------------------------------------------------------------------------------
本框架的设计理念是, 极简, 易用, 可插拔, 可扩展. 重点解决的是开发 Workflow 中的痛点. 而把其他业务相关的问题交给开发者自己解决. 例如原来的 alfred-workflow 项目中就带有了太多的组件, 包括 HTTP client, Cache 等. 这些本可以用第三方库 requests 或是 diskcache 来更好的解决. 所以本库只提供了核心的功能, 专注于提供一个接近 Python 原生的开发体验, 而把具体的业务逻辑交给开发者自己去实现.


Important Concepts and Class
------------------------------------------------------------------------------
以下几个类是 Alfred Workflow 开发的核心.

- :class:`afwf.item.Item`: 代表着 drop down menu 里的一个 item. 它避免了手写 JSON 容易出错的问题, 并且提供了一些方法能通过 `variables <https://www.alfredapp.com/help/workflows/advanced/variables/>`_ 来跟后续的 Widget 互动 (例如在浏览器中打开 URL, 打开文件, 执行命令等).
- :class:`afwf.script_filter.ScriptFilter`: 代表着 ScriptFilter 对象. 本质上是一个容器, 包含了一堆 items, variables. 用于生成最终的 JSON. 它管理了最终给用户要展示的 items.
- :class:`afwf.handler.Handler`: 用于处理命令行的输入. 其包含两个抽象函数. :meth:`afwf.handler.Handler.main` 实现了你的具体业务逻辑, 输入可以是任何参数组合, 输出必须是一个 :class:`afwf.script_filter.ScriptFilter` 对象. 这个函数可以被单元测试, 而无需真正运行 Alfred. 另一个则是 :meth:`afwf.handler.Handler.handler`, 它只有一个输入 ``query``, 是你命令行输入的字符串, 而它仅仅是将 query 解析成具体的参数, 然后传给 :meth:`afwf.handler.Handler.main`.
- :class:`afwf.workflow.Workflow`: 代表着 Workflow 对象. 本质上是一个 Handler 的容器, 可以根据命令行输入中的 handler_id 定位到不同的 Handler 对象, 然后运行不同的逻辑. 它提供了一个 :meth:`afwf.workflow.Workflow.run` 方法, 用于运行整个 Workflow. 其中包含了异常处理, 日志记录等功能.

此外本框架还提供了下面的 API 帮助你开发:

- :class:`afwf.workflow.log_debug_info`: 用于将 debug 信息写入到日志文件.
- :class:`afwf.icon.IconFileEnum`: 对框架自带的 Icon 文件的枚举.
- :class:`afwf.item.Icon`: 代表着 item 的 icon.
- :class:`afwf.item.Text`: 代表着你在 CMD + C 复制的字符串, 或是 CMD + L 显示的大型文本.
- :class:`afwf.item.VarKeyEnum`: 一些该框架内使用的 Variable key 的枚举.
- :class:`afwf.item.VarValueEnum`: 一些该框架内使用的 Variable value 的枚举.
- :class:`afwf.item.ModEnum`: 对 modifier key 的枚举.
- :class:`afwf.query.Query`: 一个方便你处理 query string 的类.
- :class:`afwf.query.QueryParser`: 一个能解析 query string 的类.


How to use this Framework
------------------------------------------------------------------------------
我提供了一个用该框架写的 `Demo Workflow <https://github.com/MacHu-GWU/afwf_example-project>`_. 它涵盖了如何实现 query 到 item 的输入输出, 如何处理错误, 如何利用缓存, 如何打开 URL, 打开文件, 对文件进行读写等常见操作. 请详细阅读 ``afwf_example`` 项目文档, 你可以参考它来学习如何使用 ``afwf`` 框架.


What's Next?
------------------------------------------------------------------------------
如果你花了一点时间已经学会了如何使用 ``afwf`` 框架, 我建议你可以进入下一章了解一些 ``afwf`` 框架的其他功能.
