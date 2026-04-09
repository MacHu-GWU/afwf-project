# -*- coding: utf-8 -*-

import afwf.examples.set_settings as mod
from afwf.examples.settings import SettingsKeyEnum, _JsonSettings


def _patch_settings(tmp_path, monkeypatch):
    import afwf.examples.settings as settings_mod

    patched = _JsonSettings(tmp_path / "settings.json")
    monkeypatch.setattr(settings_mod, "settings", patched)
    monkeypatch.setattr(mod, "settings", patched)
    return patched


class TestSetSettingsRequest:
    def test_writes_value(self, tmp_path, monkeypatch):
        patched = _patch_settings(tmp_path, monkeypatch)
        mod.set_settings_request("username", "alice")
        assert patched["username"] == "alice"

    def test_overwrites_value(self, tmp_path, monkeypatch):
        patched = _patch_settings(tmp_path, monkeypatch)
        mod.set_settings_request("username", "alice")
        mod.set_settings_request("username", "bob")
        assert patched["username"] == "bob"


class TestMain:
    def test_no_query_returns_all_keys(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="")
        assert len(sf.items) == len(SettingsKeyEnum)

    def test_one_word_fuzzy_filters_keys(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="user")
        titles = [item.title for item in sf.items]
        assert "username" in titles

    def test_valid_key_value_shows_confirmation(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="username alice")
        assert len(sf.items) == 1
        assert "username" in sf.items[0].title
        assert "alice" in sf.items[0].title

    def test_valid_key_value_sets_run_script(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="username alice")
        item = sf.items[0]
        assert item.variables.get("run_script") == "y"
        assert "set-settings-request" in item.arg
        assert "username" in item.arg
        assert "alice" in item.arg

    def test_valid_key_value_sets_notification(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="username alice")
        item = sf.items[0]
        assert item.variables.get("send_notification") == "y"

    def test_invalid_key_shows_error_item(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="badkey somevalue")
        assert len(sf.items) == 1
        assert "not a valid settings key" in sf.items[0].title

    def test_invalid_key_has_error_icon(self, tmp_path, monkeypatch):
        _patch_settings(tmp_path, monkeypatch)
        sf = mod.main(query="badkey somevalue")
        item = sf.items[0]
        assert item.icon is not None
        assert "error" in str(item.icon.path).lower()


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.examples.set_settings",
        preview=False,
    )
