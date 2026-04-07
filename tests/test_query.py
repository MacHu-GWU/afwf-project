# -*- coding: utf-8 -*-

from afwf.query import Query, QueryParser


class TestQueryParser:
    def test_parse(self):
        qp = QueryParser.from_delimiter("/")
        q = qp.parse(" bucket / artifacts / / deploy.zip")
        assert q.parts == [" bucket ", " artifacts ", " ", " deploy.zip"]
        assert q.trimmed_parts == ["bucket", "artifacts", "deploy.zip"]
        assert q.n_parts == 4
        assert q.n_trimmed_parts == 3

        qp = QueryParser.from_delimiter([" ", "-", "_"])
        q = qp.parse(" a b-c d_e f-g_h ")
        assert q.parts == ["", "a", "b", "c", "d", "e", "f", "g", "h", ""]
        assert q.trimmed_parts == list("abcdefgh")
        assert q.n_parts == 10
        assert q.n_trimmed_parts == 8

    def test_default_constructor(self):
        # QueryParser() with no args splits on single space
        qp = QueryParser()
        q = qp.parse("hello world")
        assert q.trimmed_parts == ["hello", "world"]

    def test_underscore_containing_delimiter(self):
        # multi-char delimiter that contains "_" is handled before non-underscore ones
        qp = QueryParser.from_delimiter("__")
        q = qp.parse("foo__bar__baz")
        assert q.trimmed_parts == ["foo", "bar", "baz"]


class TestQuery:
    def test_from_str(self):
        q = Query.from_str("  a   b   c  ")
        assert q.trimmed_parts == list("abc")
        assert q.n_trimmed_parts == 3
        assert (
            q.n_parts == 11
        )  # 2 leading + "a" + 3 middle + "b" + 3 middle + "c" + 2 trailing spaces

    def test_empty_string(self):
        q = Query.from_str("")
        assert q.parts == [""]
        assert q.trimmed_parts == []
        assert q.n_parts == 1
        assert q.n_trimmed_parts == 0

    def test_from_str_custom_parser(self):
        qp = QueryParser.from_delimiter("::")
        q = Query.from_str("a::b::c", parser=qp)
        assert q.trimmed_parts == ["a", "b", "c"]
        assert q.n_trimmed_parts == 3


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf.query",
        preview=False,
    )
