# -*- coding: utf-8 -*-

import afwf.api as afwf


def test():
    _ = afwf.Icon
    _ = afwf.Text
    _ = afwf.Item
    _ = afwf.VarKeyEnum
    _ = afwf.VarValueEnum
    _ = afwf.ModEnum

    _ = afwf.ScriptFilter
    _ = afwf.IconFileEnum
    _ = afwf.Query
    _ = afwf.QueryParser


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.api",
        preview=False,
    )
