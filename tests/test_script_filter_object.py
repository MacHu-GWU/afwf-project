# -*- coding: utf-8 -*-

import typing as T

import attr
from attrs_mate import AttrsClass

from afwf.script_filter_object import ScriptFilterObject


@attr.define
class Profile(ScriptFilterObject):
    firstname: str = AttrsClass.ib_str(default=None)
    lastname: str = AttrsClass.ib_str(default=None)
    ssn: str = AttrsClass.ib_str(default=None)


@attr.define
class Degree(ScriptFilterObject):
    name: str = AttrsClass.ib_str(default=None)
    year: int = AttrsClass.ib_int(default=None)


@attr.define
class People(ScriptFilterObject):
    id: int = AttrsClass.ib_int(default=None)
    profile: Profile = Profile.ib_nested(default=None)
    degrees: T.List[Degree] = Degree.ib_list(default=None)


class TestScriptFilterObject:
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

    run_cov_test(__file__, "afwf.script_filter_object", preview=False)
