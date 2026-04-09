# -*- coding: utf-8 -*-

import afwf.examples.view_settings as mod
from afwf.examples.settings import SettingsKeyEnum


class TestMain:
    def test_returns_one_item_per_key(self, tmp_path, monkeypatch):
        import afwf.examples.settings as settings_mod
        from afwf.examples.settings import _JsonSettings

        patched = _JsonSettings(tmp_path / "settings.json")
        monkeypatch.setattr(settings_mod, "settings", patched)
        monkeypatch.setattr(mod, "settings", patched)

        sf = mod.main()
        assert len(sf.items) == len(SettingsKeyEnum)

    def test_item_title_shows_key_and_value(self, tmp_path, monkeypatch):
        import afwf.examples.settings as settings_mod
        from afwf.examples.settings import _JsonSettings

        patched = _JsonSettings(tmp_path / "settings.json")
        patched["username"] = "alice"
        monkeypatch.setattr(settings_mod, "settings", patched)
        monkeypatch.setattr(mod, "settings", patched)

        sf = mod.main()
        titles = [item.title for item in sf.items]
        assert any("username" in t and "alice" in t for t in titles)

    def test_item_subtitle_shows_path(self, tmp_path, monkeypatch):
        import afwf.examples.settings as settings_mod
        from afwf.examples.settings import _JsonSettings

        patched = _JsonSettings(tmp_path / "settings.json")
        monkeypatch.setattr(settings_mod, "settings", patched)
        monkeypatch.setattr(mod, "settings", patched)
        monkeypatch.setattr(mod, "path_settings_json", tmp_path / "settings.json")

        sf = mod.main()
        assert all(str(tmp_path / "settings.json") in item.subtitle for item in sf.items)

    def test_missing_value_shows_none(self, tmp_path, monkeypatch):
        import afwf.examples.settings as settings_mod
        from afwf.examples.settings import _JsonSettings

        patched = _JsonSettings(tmp_path / "settings.json")
        monkeypatch.setattr(settings_mod, "settings", patched)
        monkeypatch.setattr(mod, "settings", patched)

        sf = mod.main()
        assert any("None" in item.title for item in sf.items)


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.examples.view_settings",
        preview=False,
    )
