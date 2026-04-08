# -*- coding: utf-8 -*-

import pytest

from afwf.examples.search_bookmarks import main


class TestMain:
    def test_empty_query_returns_all(self):
        sf = main(query="")
        assert len(sf.items) == 20

    def test_query_returns_filtered_results(self):
        sf = main(query="python")
        titles = [item.title for item in sf.items]
        assert "Python" in titles

    def test_query_no_match_returns_all(self):
        sf = main(query="zzz_no_match_zzz")
        assert len(sf.items) == 20

    def test_error_query_raises_and_logs(self, tmp_path):
        log_file = tmp_path / "test_error.log"

        # re-decorate the unwrapped function with a tmp log path
        # so we don't write to the real ~/.alfred-afwf during tests
        import afwf.examples.search_bookmarks as mod
        from afwf.decorator import log_error

        patched_main = log_error(log_file=log_file)(mod.main.__wrapped__)

        with pytest.raises(ValueError, match="simulated Python error"):
            patched_main(query="error")

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "ValueError" in content
        assert "simulated Python error" in content


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.examples.search_bookmarks",
        preview=False,
    )
