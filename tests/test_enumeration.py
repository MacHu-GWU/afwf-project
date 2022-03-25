# -*- coding: utf-8 -*-

import pytest
from afwf.enumeration import BetterEnum


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


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
