# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import afwf

    _ = afwf.Icon
    _ = afwf.Text
    _ = afwf.Item
    _ = afwf.VarKeyEnum
    _ = afwf.VarValueEnum
    _ = afwf.ModEnum


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
