Script Filter Input
===================

The Script Filter input is one of the most powerful workflow objects, allowing you to populate Alfred's results with your own custom items.

![JSON Example](json-example.png)

Note: Both the JSON and the legacy XML Output Formats are available as examples within Alfred's Workflow preferences. Select the \[+\] button > Getting Started and choose "Script Filter Output" to install the workflow.

Take a look at [the JSON Format page for more details](/help/workflows/inputs/script-filter/json/).

Jump to:

*   [Configuring the Script Filter](#config)
*   [Script Behaviour](#behaviour)
*   [Alfred Filtering Results](#alfred-filters-results)
*   [Useful Resources](#resources)

* * *

Configuring the Script Filter
-----------------------------

Script Filters are configured like any other workflow input in that they require a keyword, title and icon.

![Keyword Configuration](json-format.png)

The placeholder title and subtitle is displayed in Alfred's results until the Script Filter keyword is matched or the Script Filter is run. When the Script Filter is first run, the subtext is replaced by the "Please Wait" subtext which gives the user feedback while waiting for the initial returned result items.

Placeholder text is no longer required, but is recommended. The placeholder title and subtitle appear until you start typing your actual search query text. Without a placeholder, your filter will still work, but will not appear until you start typing your search query text.

The keyword works [much like any other keyword](/help/workflows/advanced/keywords/) throughout Alfred, it allows him to know when you want to run your Script Filter.

### Keyword argument types

There are some subtle nuances regarding the keyword argument types which are worth understanding as it can help get the most out of your filter.

#### Argument Required

The Placeholder text and subtext are shown until the user types an argument. The script is not run until an argument is present. Once an argument is typed, the "Please Wait" subtext is shown until the initial script results are returned.

#### Argument Optional

The script is run immediately on the keyword matching, with the placeholder text and "Please Wait" subtext being shown until the initial script results are returned.

#### No Argument

The script is run immediately on keyword matching with the placeholder text and "Please Wait" subtext being shown until the initial script results are returned. If an argument is typed, Alfred no longer sees this Script Filter as relevant and any related results are removed from Alfred.

* * *

XML Output Format
-----------------

The [XML version](/help/workflows/inputs/script-filter/xml/) is available for legacy, but new workflows should use the [JSON format](/help/workflows/inputs/script-filter/json/) instead.

* * *

Script Behaviour
----------------

You can control the script execution behaviour when using a Script Filter input, including the queueing mode, queueing delay and trimming of whitespaces in arguments. You'll find this under the "Run Behaviour" button.

![Script Behaviour](script-behaviour-options.png)

### Queue Mode

The options for the 'Queue Mode' are self explanatory, you can either wait until the previous script finishes before running the script again with the latest argument, or you can terminate the currently running script and run a new instance of the script with the latest argument.

You can experiment to see which mode suits your script better. As a general rule, if you have a slow script, it may be better to use the 'terminate' option. If you have a script which needs to finish each time and is quite fast, then use the 'queue' option.

### Queue Delay

This option allows you tweak the behaviour of when a script is queued (or run). It allows you to hold back from running the script if the user is currently typing, which is beneficial if your script is slow or uses a web API. It can also prevent flooding.

If you select the Automatic option, Alfred profiles how fast the user is typing and tries to only run the script when the user has stopped typing.

Unless you have a reason not to, it's recommended that you select "Always run immediately for first typed arg character" as this may make your script input perceptually faster to the user.

### Argument Whitespaces Trimming

This option allows you to tell Alfred whether the whitespaces in your arg should be trimmed. By default, the option is set to trim irrelevant spaces to prevent a script from being re-run unnecessarily if there are multiple spaces.

If the spaces are significant and should be retained as part of your argument, use the "Don't trim arg spaces, as they are significant" option instead.

* * *

Alfred Filters Results
----------------------

You can choose to run the script once, and allow Alfred to filter the results from all results returned by the script.

This is a highly efficient way to return results fast as Alfred handles the filtering, rather than running the script multiple times as additional characters are typed and the search is refined.

### Match Mode

You can set the match mode Alfred uses to filter the results from the configuration cog to the right of the "Alfred Filters Results" checkbox. These modes pair well with the "[match](/help/workflows/inputs/script-filter/json/#match)" property in the [Script Filter JSON output](/help/workflows/inputs/script-filter/json/).

![Match Mode](match-mode.png)

Where phrase means the title or match property, the match modes are:

#### Exact from start or whitespace

The default behaviour for filtering. Results match if the search term is an exact match from a word boundary in the phrase.

e.g. "My Family Photos" will match with the queries "My Family Photos", "Family Photos", "Photos".

#### Exact from start

The most strict matching mode. Results match if they are an exact match from the beginning of the phrase.

e.g. "My Family Photos" will match with the queries "My Family Photos", "My Family".

#### Word matching - Any order

Loose matching. Matches words in the phrase in any order.

e.g. "My Family Photos" will match with the queries "My Family Photos", "Photos Family", "Ph Fa".

#### Word matching - Sequential

Loose matching. Matches words in the phrase if they appear in the written order.

e.g. "My Family Photos" will match with the queries "My Family Photos", "My Photos", "Fa Ph".

* * *

Useful Resources
----------------

*   The script runs (language, escaping, script) in the same way as a [Run Script](/help/workflows/actions/run-script/) action.
*   You'll find additional information and useful discussion relating to workflows on the [Alfred forum](https://www.alfredforum.com)
*   [Github](http://github.com) provides hosting suitable for your workflows