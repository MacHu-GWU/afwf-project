# -*- coding: utf-8 -*-

import pytest
from afwf.workflow import Item, Workflow


class TestWorkflow:
    def test_to_script_filter(self):
        wf = Workflow()
        assert wf.to_script_filter() == {"items": []}

        wf.items.append(Item(title="option1"))
        assert wf.to_script_filter() == {
            "items": [
                {"title": "option1", "valid": True}
            ]
        }


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
