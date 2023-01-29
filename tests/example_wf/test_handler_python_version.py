# -*- coding: utf-8 -*-

import pytest
from afwf.example_wf.handlers.python_version import handler


class TestHandler:
    def test_get_all_python_version(self):
        versions = handler.get_all_python_version()
        assert "2.7.8" in versions
        assert "3.6.15" in versions
        assert "3.7.13" in versions
        assert "3.8.13" in versions
        assert "3.9.9" in versions


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])