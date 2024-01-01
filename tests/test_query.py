# -*- coding: utf-8 -*-

from afwf.query import Query, QueryParser


class TestQueryParser:
    def test_parse(self):
        qp = QueryParser(delimiter="/")
        q = qp.parse(" bucket / artifacts / / deploy.zip")
        assert q.parts == [" bucket ", " artifacts ", " ", " deploy.zip"]
        assert q.trimmed_parts == ["bucket", "artifacts", "deploy.zip"]
        assert q.n_parts == 4
        assert q.n_trimmed_parts == 3

        qp = QueryParser(delimiter=[" ", "-", "_"])
        q = qp.parse(" a b-c d_e f-g_h ")
        assert q.parts == ["", "a", "b", "c", "d", "e", "f", "g", "h", ""]
        assert q.trimmed_parts == list("abcdefgh")
        assert q.n_parts == 10
        assert q.n_trimmed_parts == 8


class TestQuery:
    def test_from_str(self):
        q = Query.from_str("  a   b   c  ")
        assert q.trimmed_parts == list("abc")
        assert q.n_trimmed_parts == 3


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.query", preview=False)
