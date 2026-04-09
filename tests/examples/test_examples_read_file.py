# -*- coding: utf-8 -*-

import pytest

import afwf.examples.read_file as mod


class TestMain:
    def test_file_exists_shows_content(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        p.write_text("hello world")
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main()
        assert len(sf.items) == 1
        assert sf.items[0].subtitle == "hello world"
        assert str(p) in sf.items[0].title

    def test_file_missing_shows_error_item(self, tmp_path, monkeypatch):
        p = tmp_path / "missing.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main()
        assert len(sf.items) == 1
        assert "does not exist" in sf.items[0].title

    def test_file_missing_item_has_error_icon(self, tmp_path, monkeypatch):
        p = tmp_path / "missing.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main()
        item = sf.items[0]
        assert item.icon is not None
        assert "error" in str(item.icon.path).lower()


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.examples.read_file",
        preview=False,
    )
