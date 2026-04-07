# -*- coding: utf-8 -*-

from afwf.example_wf.handlers.source_files import handler


class TestSourceFilesHandler:
    def test_get_all_files(self):
        files = handler.get_all_files()
        # known stable files that must always exist in the afwf package
        assert "afwf/handler.py" in files
        assert "afwf/item.py" in files
        assert "afwf/script_filter.py" in files
        assert "afwf/opt/fuzzy/impl.py" in files

    def test_main_with_query(self):
        sf = handler.main(query="handler")
        titles = [item.title for item in sf.items]
        assert all("handler" in t for t in titles)
        assert "afwf/handler.py" in titles

    def test_main_empty_query_returns_all(self):
        sf_all = handler.main(query="")
        sf_files = handler.get_all_files()
        # capped at 50 but should cover everything when file count <= 50
        assert len(sf_all.items) == min(len(sf_files), 50)

    def test_main_no_match_returns_fallback_item(self):
        sf = handler.main(query="zzz_no_such_file_zzz")
        assert len(sf.items) == 1
        assert "did not match" in sf.items[0].title

    def test_parse_query(self):
        assert handler.parse_query("  handler  ") == {"query": "handler"}
        assert handler.parse_query("") == {"query": ""}

    def test_encode_query(self):
        assert handler.encode_query(query="handler") == "handler"


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.example_wf.handlers.source_files",
        preview=False,
    )
