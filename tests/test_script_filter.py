# -*- coding: utf-8 -*-

import pytest
from afwf.script_filter import Item, ScriptFilter


class TestScriptFilter:
    def test_to_script_filter(self):
        sf = ScriptFilter()
        assert sf.to_script_filter() == {"items": []}

        sf.items.append(Item(title="option1"))
        assert sf.to_script_filter() == {"items": [{"title": "option1", "valid": True}]}

        sf.send_feedback()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
