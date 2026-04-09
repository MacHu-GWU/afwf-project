# -*- coding: utf-8 -*-

import pytest

import afwf.examples.write_file as mod


class TestWriteRequest:
    def test_creates_file_with_content(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        mod.write_request("hello world")
        assert p.read_text() == "hello world"

    def test_overwrites_existing_content(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        p.write_text("old content")
        monkeypatch.setattr(mod, "path_file", p)

        mod.write_request("new content")
        assert p.read_text() == "new content"

    def test_creates_parent_dirs(self, tmp_path, monkeypatch):
        p = tmp_path / "nested" / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        mod.write_request("data")
        assert p.exists()


class TestMain:
    def test_returns_one_item(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main(query="test content")
        assert len(sf.items) == 1

    def test_item_title_contains_query(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main(query="my text")
        assert "my text" in sf.items[0].title

    def test_item_run_script_variable_set(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main(query="some content")
        item = sf.items[0]
        assert "run_script" in item.variables
        assert item.variables["run_script"] == "y"

    def test_item_send_notification_variable_set(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main(query="some content")
        item = sf.items[0]
        assert "send_notification" in item.variables
        assert item.variables["send_notification"] == "y"

    def test_cmd_contains_content(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)

        sf = mod.main(query="my text")
        item = sf.items[0]
        assert "write-file-request" in item.arg
        assert "my text" in item.arg


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.examples.write_file",
        preview=False,
    )
