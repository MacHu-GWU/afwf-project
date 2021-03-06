# -*- coding: utf-8 -*-

import pytest
from afwf.query import QueryParser


class TestQueryParser():
    def test_parse(self):
        qp = QueryParser(delimiter="/")
        q = qp.parse(" bucket / artifacts / / deploy.zip")
        assert q.parts == [' bucket ', ' artifacts ', ' ', ' deploy.zip']
        assert q.trimmed_parts == ['bucket', 'artifacts', 'deploy.zip']


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
