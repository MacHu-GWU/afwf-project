# -*- coding: utf-8 -*-

import pytest
from afwf.enumeration import BetterEnum, StrEnum


class TestBetterEnum:
    def test(self):
        class Color(BetterEnum):
            red = 1
            green = 2

        assert Color.has_name("red") is True
        assert Color.has_name("blue") is False

        assert Color.has_value(1) is True
        assert Color.has_value(3) is False

        assert Color.to_names() == ["red", "green"]
        assert Color.to_values() == [1, 2]


class TestStrEnum:
    def test(self):
        class Color(StrEnum):
            red = "Red"
            green = "green"
            shiny_color = "shiny:color"
            none = None

        assert Color.get_by_value(Color.red.value) is Color.red
        assert Color.get_by_value(Color.green.value) is Color.green
        assert Color.get_by_value(Color.shiny_color.value) is Color.shiny_color
        assert Color.get_by_value(Color.none.value) is Color.none


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
