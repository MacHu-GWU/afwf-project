# -*- coding: utf-8 -*-

import sys
import json

from pydantic import Field

from .script_filter_object import ScriptFilterObject
from .item import Item


class ScriptFilter(ScriptFilterObject):
    """
    The script filter return object that flush out to standard out.

    :param items: list of items object that for drop down menu
    :param variables: session level variables. items also has item level
        variables, this feature won't be used for 99% of the time
    :param rerun: 0.1 ~ 5.0 if available, the script will only be re-run
        if the script filter is still active and the user hasn't changed
        the state of the filter by typing and triggering a re-run.

    Usage example::

        >>> import afwf.api as afwf
        >>> sf = afwf.ScriptFilter()
        >>> sf.items.append(afwf.Item(title="my title"))
        >>> sf.send_feedback()

    Ref:

    - https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    items: list[Item] = Field(default_factory=list)
    variables: dict | None = None
    rerun: float | None = None

    def send_feedback(self):
        """
        Flush script filter object JSON to standard output.
        """
        json.dump(
            self.to_script_filter(),
            sys.stdout,
            ensure_ascii=False,
        )
        sys.stdout.flush()
