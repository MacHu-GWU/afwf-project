# -*- coding: utf-8 -*-

import json

import fire

from afwf.api import ScriptFilter


def dump_sf(sf: "ScriptFilter") -> str:
    return json.dumps(sf.to_script_filter(), indent=4)


class Command:
    def search_bookmarks(self, query: str = ""):
        from afwf.examples.search_bookmarks import main

        main(
            query=str(query)
        ).send_feedback()

    def memoize(self, query: str = ""):
        from afwf.examples.memoize import main

        main(
            query=str(query),
        ).send_feedback()

    def open_file(self):
        from afwf.examples.open_file import main

        main().send_feedback()


def main():
    fire.Fire(Command)


if __name__ == "__main__":
    main()
