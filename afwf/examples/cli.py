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

    def read_file(self):
        from afwf.examples.read_file import main

        main().send_feedback()

    def write_file(self, query: str = ""):
        from afwf.examples.write_file import main

        main(query=str(query)).send_feedback()

    def write_file_request(self, content: str = ""):
        from afwf.examples.write_file import write_request

        write_request(content=str(content))

    def view_settings(self):
        from afwf.examples.view_settings import main

        main().send_feedback()

    def set_settings(self, query: str = ""):
        from afwf.examples.set_settings import main

        main(query=str(query)).send_feedback()

    def set_settings_request(self, key: str = "", value: str = ""):
        from afwf.examples.set_settings import set_settings_request

        set_settings_request(key=str(key), value=str(value))


def main():
    fire.Fire(Command)


if __name__ == "__main__":
    main()
