# -*- coding: utf-8 -*-

import pytest
from afwf.example_wf import wf
from afwf.example_wf.handlers import source_files


class TestWorkflow:
    def test_run_dispatch(self):
        # end-to-end: _run parses the arg, routes to the handler, returns ScriptFilter
        sf = wf._run(arg="source_files handler")
        assert len(sf.items) > 0
        assert all("handler" in item.title for item in sf.items)

    def test_register_duplicate_raises(self):
        with pytest.raises(KeyError):
            wf.register(source_files.handler)


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.example_wf.handlers.wf",
        preview=False,
    )
