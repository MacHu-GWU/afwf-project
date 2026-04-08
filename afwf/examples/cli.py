# -*- coding: utf-8 -*-

import json

import fire

from afwf.api import ScriptFilter


def dump_sf(sf: "ScriptFilter") -> str:
    return json.dumps(sf.to_script_filter(), indent=4)


class Command:
    def search_bookmarks(self, query: str = ""):
        from afwf.examples.search_bookmarks import main

        print(dump_sf(main(query)))


def main():
    fire.Fire(Command)


if __name__ == "__main__":
    main()
