# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict


class ScriptFilterObject(BaseModel):
    """
    Base class for all objects that appear in an Alfred Script Filter JSON payload
    (e.g. ``Item``, ``Icon``, ``Text``, ``ScriptFilter``).

    Ref: https://www.alfredapp.com/help/workflows/inputs/script-filter/json/

    ---

    Alfred's JSON protocol differs from standard Python OOP serialization in
    several ways. ``to_script_filter()`` implements these rules explicitly:

    1. **``None`` → field must be absent** (not ``null``).
       Alfred interprets a missing key as "use default", not as a null value.
       Standard serialisation would emit ``"subtitle": null``; Alfred expects
       the key to simply not appear.

    2. **``False`` / ``0`` / ``""`` → must be preserved**.
       These are falsy in Python but carry real meaning in Alfred's protocol.
       Most importantly: if ``valid`` is absent Alfred defaults to ``true``,
       so ``valid=False`` *must* appear in the output. Standard OOP serialisers
       handle this correctly; a naïve ``if v:`` falsy-filter does not (bug).

    3. **Empty nested ``ScriptFilterObject`` → field must be absent**.
       A ``Text()`` with no fields set serialises to ``{}``.  Sending
       ``"text": {}`` to Alfred is noise and may confuse some versions of Alfred.
       These are omitted by calling ``to_script_filter()`` recursively and
       skipping the result when it is an empty dict.

    4. **Top-level ``dict`` field that is ``{}`` → omit**.
       e.g. ``variables: dict = {}`` on an ``Item`` means "no variables",
       which is identical to the key being absent. Alfred ignores both.

    5. **``variables: {}`` *inside* ``mods`` → must be preserved**.
       Alfred distinguishes between a mod *without* a ``variables`` key
       (inherits the item's variables) and a mod *with* ``"variables": {}``
       (explicitly clears inheritance). Therefore this rule applies only to
       the top-level fields of a ``ScriptFilterObject``, and plain ``dict``
       values are passed through as-is without recursive stripping.

    6. **``list`` fields → always preserved, even when empty**.
       ``ScriptFilter`` is required to return an ``items`` array (even ``[]``),
       so list fields are never omitted regardless of their content.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_script_filter(self) -> dict:
        """
        Serialize to an Alfred Workflow Script Filter compatible dictionary.

        See class docstring for the full set of serialization rules.
        """
        dct = {}
        for k in self.__class__.model_fields:
            v = getattr(self, k)
            # Rule 1: omit None
            if v is None:
                continue
            if isinstance(v, ScriptFilterObject):
                # Rule 3: omit empty nested objects
                serialized = v.to_script_filter()
                if serialized:
                    dct[k] = serialized
            elif isinstance(v, list):
                # Rule 6: always preserve lists; recurse into ScriptFilterObject items
                dct[k] = [
                    item.to_script_filter() if isinstance(item, ScriptFilterObject) else item
                    for item in v
                ]
            elif isinstance(v, dict) and not v:
                # Rule 4: omit empty top-level dict fields
                # Rule 5: plain dict values (e.g. mods content) are NOT recursively stripped,
                #          so "variables": {} inside mods is preserved as-is.
                continue
            else:
                # Rule 2: preserve False, 0, "", and all other non-None values
                dct[k] = v
        return dct
