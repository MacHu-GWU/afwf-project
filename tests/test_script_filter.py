# -*- coding: utf-8 -*-

from afwf.script_filter import Item, ScriptFilter


class TestScriptFilter:
    def test_to_script_filter(self):
        sf = ScriptFilter()
        assert sf.to_script_filter() == {"items": []}

        sf.items.append(Item(title="option1"))
        assert sf.to_script_filter() == {"items": [{"title": "option1", "valid": True}]}

        sf.send_feedback()


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.script_filter", preview=False)
