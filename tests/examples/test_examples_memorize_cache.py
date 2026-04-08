# -*- coding: utf-8 -*-

import pytest

from afwf.examples.memorize_cache import main, _get_value


class TestGetValue:
    def test_returns_int_in_range(self, tmp_path):
        # patch cache dir so tests don't pollute ~/.alfred-afwf/.cache
        import afwf.examples.memorize_cache as mod
        from afwf.opt.cache.api import TypedCache

        mod.cache = TypedCache(tmp_path / ".cache")
        mod._get_value = mod.cache.typed_memoize(tag="memorize_cache", expire=5)(
            lambda key: __import__("random").randint(1, 1000)
        )

        value = mod._get_value("test_key")
        assert isinstance(value, int)
        assert 1 <= value <= 1000

    def test_same_key_returns_cached_value(self, tmp_path):
        import afwf.examples.memorize_cache as mod
        from afwf.opt.cache.api import TypedCache

        mod.cache = TypedCache(tmp_path / ".cache")
        mod._get_value = mod.cache.typed_memoize(tag="memorize_cache", expire=5)(
            lambda key: __import__("random").randint(1, 1000)
        )

        v1 = mod._get_value("same_key")
        v2 = mod._get_value("same_key")
        assert v1 == v2

    def test_different_keys_may_differ(self, tmp_path):
        import afwf.examples.memorize_cache as mod
        from afwf.opt.cache.api import TypedCache

        mod.cache = TypedCache(tmp_path / ".cache")
        # use a deterministic function so the test is stable
        mod._get_value = mod.cache.typed_memoize(tag="memorize_cache", expire=5)(
            lambda key: len(key)
        )

        assert mod._get_value("a") != mod._get_value("bb")


class TestMain:
    def test_returns_script_filter_with_one_item(self, tmp_path):
        import afwf.examples.memorize_cache as mod
        from afwf.opt.cache.api import TypedCache

        mod.cache = TypedCache(tmp_path / ".cache")
        mod._get_value = mod.cache.typed_memoize(tag="memorize_cache", expire=5)(
            lambda key: __import__("random").randint(1, 1000)
        )

        sf = main(query="hello")
        assert len(sf.items) == 1
        assert sf.items[0].title.startswith("value is ")

    def test_title_contains_integer(self, tmp_path):
        import afwf.examples.memorize_cache as mod
        from afwf.opt.cache.api import TypedCache

        mod.cache = TypedCache(tmp_path / ".cache")
        mod._get_value = mod.cache.typed_memoize(tag="memorize_cache", expire=5)(
            lambda key: 42
        )

        sf = main(query="any")
        assert sf.items[0].title == "value is 42"

    def test_error_query_raises_and_logs(self, tmp_path):
        import afwf.examples.memorize_cache as mod
        from afwf.decorator import log_error

        log_file = tmp_path / "memorize_cache.log"
        patched_main = log_error(log_file=log_file)(main.__wrapped__)

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
        "afwf.examples.memorize_cache",
        preview=False,
    )
