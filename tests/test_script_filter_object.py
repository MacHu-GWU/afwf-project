# -*- coding: utf-8 -*-

from afwf.script_filter_object import ScriptFilterObject


class Profile(ScriptFilterObject):
    firstname: str | None = None
    lastname: str | None = None
    ssn: str | None = None


class Degree(ScriptFilterObject):
    name: str | None = None
    year: int | None = None


class People(ScriptFilterObject):
    id: int | None = None
    profile: Profile | None = None
    degrees: list[Degree] | None = None


class Widget(ScriptFilterObject):
    # used to test falsy-but-non-None values (Rule 2) and plain dict passthrough (Rule 5)
    valid: bool = True
    score: int = 0
    mods: dict | None = None
    tags: list[str] | None = None
    meta: dict | None = None


class TestScriptFilterObject:
    def test_falsy_primitives_preserved(self):
        # Rule 2: False and 0 must appear in output even though they are falsy
        w = Widget(valid=False, score=0)
        result = w.to_script_filter()
        assert result["valid"] is False
        assert result["score"] == 0

    def test_empty_dict_field_omitted(self):
        # Rule 4: a top-level dict field that is {} is omitted
        w = Widget(meta={})
        assert "meta" not in w.to_script_filter()

    def test_nonempty_dict_field_preserved_with_nested_empty(self):
        # Rule 5: plain dict values are NOT recursively stripped —
        # "variables": {} inside mods has special meaning in Alfred
        # (prevents inheritance of item variables) and must be preserved.
        w = Widget(mods={"cmd": {"variables": {}}})
        result = w.to_script_filter()
        assert result["mods"] == {"cmd": {"variables": {}}}

    def test_empty_list_preserved(self):
        # Rule 6: empty lists are always kept
        w = Widget(tags=[])
        assert w.to_script_filter()["tags"] == []

    def test_empty_nested_object_omitted(self):
        # Rule 3: a nested ScriptFilterObject that serialises to {} is omitted
        people = People(id=1, profile=Profile())
        assert "profile" not in people.to_script_filter()

    def test(self):
        profile = Profile(
            firstname="David",
            lastname="John",
            ssn="123-45-6789",
        )
        degree1 = Degree(name="Bachelor", year=2004)
        degree2 = Degree(name="Master", year=2006)
        people = People(
            id=1,
            profile=profile,
            degrees=[degree1, degree2],
        )
        assert people.to_script_filter() == {
            "id": 1,
            "profile": {"firstname": "David", "lastname": "John", "ssn": "123-45-6789"},
            "degrees": [
                {"name": "Bachelor", "year": 2004},
                {"name": "Master", "year": 2006},
            ],
        }

        profile = Profile()
        degree1 = Degree()
        degree2 = Degree()
        people = People(id=1)

        assert profile.to_script_filter() == {}
        assert degree1.to_script_filter() == {}
        assert degree2.to_script_filter() == {}
        assert people.to_script_filter() == {"id": 1}


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.script_filter_object",
        preview=False,
    )
