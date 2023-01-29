# -*- coding: utf-8 -*-

import pytest
from afwf.example_wf import wf


class TestWorkflow:
    def test(self):
        sf = wf._run(arg="python_version 2.7")
        for item in sf.items:
            assert "2.7" in item.title


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])