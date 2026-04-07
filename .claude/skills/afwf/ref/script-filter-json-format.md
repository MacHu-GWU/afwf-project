Script Filter JSON Format
=========================

We recommend JSON as the preferred format to return results into Alfred from a Script Filter.

Example JSON Format:

    {"items": [
        {
            "uid": "desktop",
            "type": "file",
            "title": "Desktop",
            "subtitle": "~/Desktop",
            "arg": "~/Desktop",
            "autocomplete": "Desktop",
            "icon": {
                "type": "fileicon",
                "path": "~/Desktop"
            }
        }
    ]}

A Script Filter is required to return an items array of zero or more `item`s. Each `item` describes a result row displayed in Alfred. The three obvious elements are the ones you see in an Alfred result row - `title`, `subtitle` and `icon`.

* * *

Properties
----------

Alfred uses the following properties within each `item` in the `items` array:

* * *

### uid : STRING (optional)

A unique identifier for the item. It allows Alfred to learn about the item for subsequent sorting and ordering of the user's actioned results.

It is important that you use the same UID throughout subsequent executions of your script to take advantage of Alfred's knowledge and sorting. To show results in the order you return them from your script, [exclude the UID field or use `skipknowledge: true`](#uid).

* * *

### title : STRING

The title displayed in the result row. There are no options for this element and it is essential that this element is populated.

`"title": "Desktop"`

* * *

### subtitle : STRING (optional)

The subtitle displayed in the result row.

`"subtitle": "~/Desktop"`

* * *

### arg : STRING | ARRAY (recommended)

The argument which is passed through the workflow to the connected output action.

`"arg": "~/Desktop"`

While optional, it's highly recommended that you populate `arg` as it's the string which is passed to your connected output actions. If excluded, you won't know which result item the user has selected.

It is also possible to pass multiple arguments via an array of strings:

`"arg": ["~/Desktop", "~/Pictures"]`

* * *

### icon : OBJECT (optional)

The icon displayed in the result row. `path` is relative to the workflow's root folder:

    "icon": {
        "path": "./custom_icon.png"
    }

The optional `type` key alters this behaviour. Setting it to `fileicon` will tell Alfred to get the file icon for the specified path.

    "icon": {
        "type": "fileicon",
        "path": "~/Desktop"
    }

`filetype` is similar but takes a file UTI (Uniform Type Identifier) as the `path`.

    "icon": {
        "type": "filetype",
        "path": "com.apple.rtfd"
    }

* * *

### valid : true | false (optional, default = true)

If the item is valid or not. If an `item` is valid then Alfred will action it when the user presses return. If the `item` is not valid, Alfred will do nothing. This allows you to intelligently prevent Alfred from actioning a result based on the current `{query}` passed into your script.

If you exclude the `valid` attribute, Alfred assumes your `item` is valid.

* * *

### match : STRING (optional)

The `match` field enables you to define what Alfred matches against when the workflow is set to "Alfred Filters Results". If `match` is present, it fully replaces matching on the `title` property.

    "match": "my family photos"

The `match` field is always treated as case insensitive, and intelligently treated as diacritic insensitive. If the search query contains a diacritic, the match becomes diacritic sensitive.

This option pairs well with the "[Alfred Filters Results](/help/workflows/inputs/script-filter/#alfred-filters-results)" Match Mode option.

* * *

### autocomplete : STRING (recommended)

An optional but recommended string you can provide to populate into Alfred's search field if the user auto-complete's the selected result (⇥ by default).

If the `item` is set to `"valid": false`, the auto-complete text is populated into Alfred's search field when the user actions the result.

* * *

### type : "default" | "file" | "file:skipcheck" (optional, default = "default")

By specifying `"type": "file"`, Alfred treats your result as a file on your system. This allows the user to perform actions on the file like they can with Alfred's standard file filters.

When returning files, Alfred will check if they exist before presenting that result to the user. This has a very small performance implication but makes results as predictable as possible. If you would like Alfred to skip this check because you are certain the files you are returning exist, use `"type": "file:skipcheck"`.

* * *

### mods : OBJECT (optional)

The mod element gives you control over how the modifier keys react. It can alter the looks of a result (e.g. `subtitle`, `icon`) and output a different `arg` or [session variables](#variables).

    "mods": {
        "alt": {
            "valid": true,
            "arg": "alfredapp.com/powerpack/",
            "subtitle": "https://www.alfredapp.com/powerpack/"
        },
        "cmd": {
            "valid": true,
            "arg": "alfredapp.com/shop/",
            "subtitle": "https://www.alfredapp.com/shop/"
        },
        "cmd+alt": {
            "valid": true,
            "arg": "alfredapp.com/blog/",
            "subtitle": "https://www.alfredapp.com/blog/"
        }
    }

Valid modifiers include `cmd` (⌘), `alt` (⌥), `ctrl` (⌃), `shift` (⇧), `fn`, and any combination through the use of `+`. For example: `cmd + alt` only activates when both keys are pressed.

* * *

### action : OBJECT | ARRAY | STRING (optional)

This element defines the Universal Action items used when actioning the result, and overrides the `arg` being used for actioning. The `action` key can take a string or array for simple types, and the content type will automatically be derived by Alfred to file, url, or text.

Single Item:

    "action": "Alfred is Great"

Multiple Items:

    "action": ["Alfred is Great", "I use him all day long"]

For control over the content type of the action, you can use an object with typed keys:

    "action": {
      "text": ["one", "two", "three"],
      "url": "https://www.alfredapp.com",
      "file": "~/Desktop",
      "auto": "~/Pictures"
    }

See [Universal Actions](/help/features/universal-actions/) for more information.

* * *

### text : OBJECT (optional)

Defines the text the user will get when copying the selected result row with ⌘C or displaying large type with ⌘L.

    "text": {
        "copy": "https://www.alfredapp.com/ (text here to copy)",
        "largetype": "https://www.alfredapp.com/ (text here for large type)"
    }

If these are not defined, you will inherit Alfred's standard behaviour where the arg is copied to the Clipboard or used for Large Type.

* * *

### quicklookurl : STRING (optional)

A Quick Look URL which will be visible if the user uses the Quick Look feature within Alfred (tapping shift, or ⌘Y). `quicklookurl` will also accept a file path, both absolute and relative to home using ~/.

    "quicklookurl": "https://www.alfredapp.com/"

If absent, Alfred will attempt to use `arg` as the quicklook URL.

* * *

Variables / Session Variables
=============================

Variables within a `variables` object will be passed out of the script filter and remain accessible throughout the current session as environment variables.

In addition, they are passed back in when the script reruns within the same session. This can be used for managing state between runs as the user types input or when the script is set to re-run after an interval.

    {
        "variables": {
            "fruit": "banana",
            "vegetable": "carrot"
        },
        "items": [
            ...
        ]
    }

See the built in "Advanced Script Filter" getting started guide for more info, and to see this in practice.

Item Variables
--------------

Individual `item` objects can have `variables` which are passed out of the Script Filter object if the associated result item is selected in Alfred's results list. `variables` set within an `item` will override any JSON session variables of the same name.

It is also possible to add a `variables` object for each `mod` in the `item` object, allowing you to differentiate when a mod result is selected within your workflow. Note that when setting a `variables` object on a `mod`, this replaces the `item` variables, and doesn't inherit from them, allowing maximum flexibility.

When a `mod` doesn't contain a `variables` object, it will assume the `item` variables. To prevent this, add an empty `variables` object: `"variables": {}`.

* * *

Rerunning script filters automatically
======================================

Scripts can be set to re-run automatically after an interval using the `rerun` key with a value from 0.1 to 5.0 seconds. The script will only be re-run if the script filter is still active and the user hasn't changed the state of the filter by typing and triggering a re-run.

    {
        "rerun": 1,
        "items": [
            ...
        ]
    }

See the built in "Advanced Script Filter" getting started guide for more info, and to see this in practice.

* * *

Caching script filters automatically
====================================

New in Alfred 5.5

Scripts which take a while to return can cache results so users see data sooner on subsequent runs. The Script Filter presents the results from the previous run when caching is active and hasn't expired. Because the script won't execute when loading cached data, we recommend this option only be used with "[Alfred filters results](/help/workflows/inputs/script-filter/#alfred-filters-results)".

Time to live for cached data is defined as a number of seconds between 5 and 86400 (i.e. 24 hours).

    {
        "cache": {
            "seconds": 3600
        },
        "items": [
            ...
        ]
    }

Caches are marked as stale - and thus purged, causing the script to rerun when called - by:

*   Editing the Script Filter object.
*   Clicking `Flush` in the [debugger](/help/workflows/advanced/debugger/).
*   Reloading the workflow.
*   Reloading Alfred's cache (by typing `reload` into Alfred).
*   Restarting Alfred (e.g. after opening at login following a macOS reboot).

The first three act on a specific workflow, while the bottom two affect all of them.

The optional `loosereload` key asks the Script Filter to try to show any cached data first. If it's determined to be stale, the script runs in the background and replaces results with the new data when it becomes available.

    {
        "cache": {
            "seconds": 3600,
            "loosereload": true
        },
        "items": [
            ...
        ]
    }

* * *

Result Ordering and the UID
===========================

Alfred learns to prioritise `item` results like he learns any other, meaning the order in which your workflow results are presented will be based on Alfred's knowledge (using the `item` UID) and not the order your script returns the `item`s.

To have Alfred present the `item`s in the exact sequence you define, **exclude the UID attribute**. For example:

    {"items": [
        {
            "type": "file",
            "title": "Desktop",
            "subtitle": "~/Desktop",
            "arg": "~/Desktop",
            "autocomplete": "Desktop",
            "icon": {
                "type": "fileicon",
                "path": "~/Desktop"
            }
        }
    ]}

New in Alfred 5

Alternatively, set the optional `skipknowledge` key to `true`:

    {
        "skipknowledge": true,
        "items": [
            ...
        ]
    }

This preserves the given item order while allowing Alfred to retain knowledge of your items, like your current selection during a [re-run](#rerun).

> Note: _`skipknowledge` prevents the creation of new knowledge but does not ignore what Alfred already learned._ In other words, by adding and removing `skipknowledge` you may generate _local_ ordering which does not exactly match the order of your items.
> 
> Knowledge is retained _per object_. Replace the object with a duplicate to force reset the ordering.

* * *

An Example
==========

For a working example of the JSON format, Add the Getting Started > Script Filter Output workflow from the + button within Alfred's Workflow preferences.