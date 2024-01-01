# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import afwf.api as afwf

    _ = afwf.Icon
    _ = afwf.Text
    _ = afwf.Item
    _ = afwf.VarKeyEnum
    _ = afwf.VarValueEnum
    _ = afwf.ModEnum

    _ = afwf.ScriptFilter
    _ = afwf.Handler
    _ = afwf.log_debug_info
    _ = afwf.Workflow
    _ = afwf.IconFileEnum
    _ = afwf.Query
    _ = afwf.QueryParser

    _ = afwf.TypedCache
    _ = afwf.FuzzyMatcher
    _ = afwf.FuzzyItem
    _ = afwf.FuzzyItemMatcher


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.api", preview=False)
