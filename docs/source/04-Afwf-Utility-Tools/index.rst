``afwf`` Utility Tools
==============================================================================
``afwf`` 自带了一些开发 Workflow 时常用到的工具. 和 Alfred 官放的 Python 包不同的是, 官放倾向于自己从 0 只用标准库造一个轮子, 而 ``afwf`` 倾向于使用成熟的第三方库.


Cache
------------------------------------------------------------------------------
一个基于 `diskcache <https://pypi.org/project/diskcache/>`_ 的磁盘缓存工具. 详细使用说明可以参考单元测试:

.. literalinclude:: ../../../tests/opt/test_cache.py
   :language: python


Fuzzy Item
------------------------------------------------------------------------------
一个基于 `fuzzywuzzy <https://pypi.org/project/fuzzywuzzy/>`_ 的模糊搜索工具, 用于对 items 进行模糊搜索, 排序. 详细使用说明可以参考单元测试:

.. literalinclude:: ../../../tests/opt/test_opt_fuzzy_item.py
   :language: python
