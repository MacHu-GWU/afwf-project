# -*- coding: utf-8 -*-

from pathlib import Path

from afwf.opt.cache.impl import TypedCache

dir_cache = Path(__file__).absolute().parent.joinpath(".cache")

cache = TypedCache(str(dir_cache))


class Dog:
    def __init__(self):
        self.bark_count = 0

    @cache.typed_memoize(expire=10)
    def bark(self, say: str):
        _ = say
        self.bark_count += 1


def test():
    cache.clear()
    dog = Dog()
    dog.bark("woof")
    dog.bark("woof")
    dog.bark("woof")
    dog.bark("ruff")
    dog.bark("ruff")
    dog.bark("ruff")
    dog.bark("ruff")
    dog.bark("ruff")
    assert dog.bark_count == 2


if __name__ == "__main__":
    from afwf.tests import run_cov_test

    run_cov_test(__file__, "afwf.opt.cache", preview=False)
