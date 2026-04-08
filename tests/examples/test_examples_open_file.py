# -*- coding: utf-8 -*-

import pytest

from afwf.examples.open_file import main


class TestMain:
    def test_returns_script_filter_with_py_files(self):
        sf = main(query="")
        assert len(sf.items) > 0
        for item in sf.items:
            assert item.title.endswith(".py")

    def test_items_have_correct_fields(self):
        sf = main(query="")
        item = sf.items[0]
        assert item.subtitle.startswith("Open ")
        assert item.autocomplete == item.title
        assert item.match == item.title
        assert item.arg.endswith(".py")

    def test_open_file_variable_set(self):
        sf = main(query="")
        item = sf.items[0]
        # open_file sets the afwf variables on the item
        assert "open_file" in item.variables
        assert item.variables["open_file"] == "y"
        assert "open_file_path" in item.variables
        assert item.variables["open_file_path"].endswith(".py")

    def test_open_file_py_is_listed(self):
        sf = main(query="")
        titles = [item.title for item in sf.items]
        assert "open_file.py" in titles

    def test_items_sorted_by_name(self):
        sf = main(query="")
        titles = [item.title for item in sf.items]
        assert titles == sorted(titles)

    def test_error_query_raises_and_logs(self, tmp_path):
        import afwf.examples.open_file as mod
        from afwf.decorator import log_error
        from pathlib_mate import Path

        log_file = tmp_path / "open_file.log"

        def _raise(query: str):
            raise ValueError("simulated error")

        patched_main = log_error(log_file=log_file)(_raise)

        with pytest.raises(ValueError, match="simulated error"):
            patched_main(query="anything")

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "ValueError" in content


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.examples.open_file",
        preview=False,
    )
