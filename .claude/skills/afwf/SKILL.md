---
name: afwf
description: Guide for building Alfred workflow Python packages using the afwf SDK. Use when creating, modifying, or debugging afwf-based Alfred workflows — Script Filters, CLI entry points, fuzzy matching, disk caching, write actions, testing, or deployment.
---

# afwf — Alfred Workflow Python SDK

`afwf` lets you build Alfred Script Filter workflows in Python. The core idea: write Python functions that return a `ScriptFilter` object, expose them as a CLI via `fire`, and call the CLI from Alfred's Script field.

---

## Architecture: Three Layers

```
Layer 1 — Python logic (my_pkg/your_module.py)
  Your package name is whatever you choose (e.g. my_pkg).
  afwf is just the SDK you import — not the name of your package.
  Pure functions. main(query) → ScriptFilter. No Alfred dependency. Unit-testable.

Layer 2 — CLI entry point (cli.py → your-cli-name)
  fire.Fire(Command) exposes each main() as a subcommand.
  Alfred's Script field calls this binary.

Layer 3 — Alfred workflow config (info.plist)
  Keywords, Script Filter nodes, Conditional branches, action widgets.
  Static — never changes when Python logic changes.
```

`pyproject.toml` declares the entry point:
```toml
[project.scripts]
my-workflow = "my_pkg.cli:main"
```

`cli.py`:
```python
import fire
from my_pkg import search_items, write_item

class Command:
    def search_items(self, query: str = ""):
        search_items.main(query=query).send_feedback()

    def write_item_request(self, content: str):
        # Called by Alfred's Run Script widget, not a Script Filter
        write_item.write_request(content)

def main():
    fire.Fire(Command)
```

Alfred Script field (dev): `.venv/bin/my-workflow search-items --query '{query}'`
Alfred Script field (prod): `~/.local/bin/uvx --from my-pkg==1.0.0 my-workflow search-items --query '{query}'`

---

## Core Classes

```python
import afwf.api as afwf

# Build a response
sf = afwf.ScriptFilter()
item = afwf.Item(title="My Result", subtitle="Details here")
sf.items.append(item)
sf.send_feedback()   # dumps JSON to stdout → Alfred reads it
```

| Class | Purpose |
|---|---|
| `ScriptFilter` | Top-level response; holds `items` list; `send_feedback()` dumps JSON |
| `Item` | One row in Alfred's dropdown; has `title`, `subtitle`, `arg`, `icon`, `match`, `autocomplete`, `valid`, `variables`, `mods` |
| `Icon` | `{"type": "fileicon"/"filetype", "path": "..."}` |
| `Text` | `{"copy": "...", "largetype": "..."}` |

### Bundled Icons

```python
from afwf.api import IconFileEnum
item.icon = afwf.Icon(path=IconFileEnum.error)     # error state
item.icon = afwf.Icon(path=IconFileEnum.search)    # search
item.icon = afwf.Icon(path=IconFileEnum.folder)    # folder
# ~50 bundled PNGs available in IconFileEnum
```

---

## Serialization Rules

`to_script_filter()` serializes correctly for Alfred's protocol (not a plain `model_dump()`):

| Python value | Output |
|---|---|
| `None` | Field **omitted** (Alfred treats missing = use default) |
| `False` / `0` / `""` | **Preserved** (e.g. `valid=False` must appear) |
| Nested `ScriptFilterObject` → `{}` | Field **omitted** |
| Top-level `dict` that is `{}` | Field **omitted** |
| `dict` nested inside another `dict` (e.g. inside `mods`) | **Passed through** unchanged |
| `list` (any length, including `[]`) | **Always preserved** (`items: []` required) |

---

## Item Actions — Conditional Widget Pattern

Python declares the *intended follow-up action* via `item.set_*` helpers. Each helper writes a flag/payload variable pair. Alfred's Conditional widget reads the flag and routes to the correct downstream widget.

```python
# Opens URL in browser
item.open_url("https://example.com")
# → variables: {"open_url": "y", "open_url_arg": "https://example.com"}

# Opens file
item.open_file(path="/path/to/file.py")
# → variables: {"open_file": "y", "open_file_path": "/path/to/file.py"}

# Runs a shell command (also sets item.arg = cmd)
item.run_script("/path/to/bin/my-workflow write-item-request --content 'hello'")
# → variables: {"run_script": "y", "run_script_arg": "..."}

# Shows macOS notification
item.send_notification(title="Done", subtitle="File written")
# → variables: {"send_notification": "y", "send_notification_title": "Done", ...}

# Other helpers
item.launch_app_or_file(path=...)
item.reveal_file_in_finder(path=...)
item.browse_in_terminal(path=...)
item.browse_in_alfred(path=...)
item.terminal_command(cmd=...)
```

**Alfred Conditional widget config** (set up once in Alfred UI):
```
if {var:open_url}          = y  →  Open URL widget        (URL: {var:open_url_arg})
if {var:open_file}         = y  →  Open File widget       (File: {var:open_file_path})
if {var:run_script}        = y  →  Run Script widget      (Script: {query})
if {var:send_notification} = y  →  Post Notification      (Title: {var:send_notification_title})
```

**Combining actions** (run_script + send_notification is common):
```python
item.run_script(cmd)
item.send_notification(title="Done", subtitle="success")
# In Alfred: Run Script widget → connect forward to → Post Notification widget
```

**The `sys.executable` trick** for write actions (Alfred's shell has no $PATH):
```python
import sys
from pathlib import Path
bin_cli = Path(sys.executable).parent / "my-workflow"
cmd = f"{bin_cli} write-item-request --content {content!r}"
item.run_script(cmd)
```

---

## QueryParser — Multi-Step Interactions

Alfred passes one raw query string. Parse it to branch on token count:

```python
import afwf.api as afwf

q = afwf.Query.from_str("username alice")
q.trimmed_parts    # ["username", "alice"]
q.n_trimmed_parts  # 2

# Custom delimiter
parser = afwf.QueryParser.from_delimiter("/")
q = parser.parse("2026/04/08")
q.trimmed_parts    # ["2026", "04", "08"]
```

**Standard two-step pattern** (e.g. pick key → enter value):
```python
def main(query: str) -> afwf.ScriptFilter:
    q = afwf.Query.from_str(query)

    if q.n_trimmed_parts == 0:
        # Show all options
        return build_all_items()

    elif q.n_trimmed_parts == 1:
        # Fuzzy-filter options
        return fuzzy_filter(q.trimmed_parts[0])

    else:
        # key + value → show confirmation item with run_script
        key = q.trimmed_parts[0]
        value = " ".join(q.trimmed_parts[1:])
        return build_confirmation(key, value)
```

---

## log_error Decorator

Alfred silently swallows Python exceptions. `log_error` writes the traceback to disk:

```python
import afwf.api as afwf

@afwf.log_error()   # writes to ~/.alfred-afwf/error.log
def main(query: str) -> afwf.ScriptFilter:
    ...

# Custom log file per Script Filter:
@afwf.log_error(log_file="~/.alfred-afwf/search_bookmarks.log")
def main(query: str) -> afwf.ScriptFilter:
    ...
```

Log format: `[YYYY-MM-DD HH:MM:SS]` + traceback + separator line. Uses `RotatingFileHandler` (500 KB × 3 files by default). Transparent on the happy path — zero overhead.

---

## Fuzzy Matching (`afwf[fuzzy]`)

Install: `pip install "afwf[fuzzy]"` or `uv add "afwf[fuzzy]"`

### opt.fuzzy_item — For Alfred Items (most common)

```python
import afwf.opt.fuzzy_item.api as fuzzy_item

# Build items with a fuzzy match name stored in variables
item = fuzzy_item.Item(title="Alfred App", subtitle="https://alfredapp.com/")
item.set_fuzzy_match_name("Alfred App")

# Match against a query
matcher = fuzzy_item.FuzzyItemMatcher.from_items(items)
matched = matcher.match("alfred", threshold=70, limit=20)
# Falls back gracefully: if no match, return full list
return afwf.ScriptFilter(items=matched if matched else items)
```

### opt.fuzzy — Generic (for domain objects)

```python
from afwf.opt.fuzzy.api import FuzzyMatcher
import dataclasses

@dataclasses.dataclass
class Bookmark:
    title: str
    url: str

class BookmarkMatcher(FuzzyMatcher[Bookmark]):
    def get_name(self, item: Bookmark) -> str | None:
        return item.title  # None = exclude from index

matcher = BookmarkMatcher.from_items(bookmarks)
results = matcher.match("alfred", threshold=0)
```

`match()` params: `threshold=70` (0–100), `limit=20`, `filter_func=lambda x: True`.

---

## Typed Disk Cache (`afwf[cache]`)

Install: `pip install "afwf[cache]"` or `uv add "afwf[cache]"`

Alfred runs Script Filters on every keystroke. Cache expensive operations:

```python
from afwf.opt.cache.api import TypedCache
from afwf.paths import path_enum

# Module-level singleton — persists on disk between Alfred invocations
cache = TypedCache(path_enum.dir_afwf / ".cache")  # ~/.alfred-afwf/.cache

@cache.typed_memoize(expire=60)   # TTL in seconds
def fetch_data(query: str) -> list[str]:
    # expensive: network call, disk scan, etc.
    ...

# In main():
def main(query: str) -> afwf.ScriptFilter:
    data = fetch_data(query)   # cached after first call
    ...
```

`typed_memoize` params: `expire=None` (never), `tag=None` (for bulk eviction), `typed=False`. Preserves type hints unlike plain `diskcache.memoize`.

Cache invalidation: `cache.clear()` / `cache.evict(tag="my_tag")` / `cache.delete(key)`

---

## Patterns

### Read-Only Script Filter (Python-side fuzzy filtering)

```python
# search_bookmarks.py
import afwf.api as afwf
import afwf.opt.fuzzy_item.api as fuzzy_item
from afwf.api import IconFileEnum

BOOKMARKS = [
    {"title": "Python", "url": "https://python.org/"},
    # ...
]

@afwf.log_error()
def main(query: str) -> afwf.ScriptFilter:
    items = []
    for bm in BOOKMARKS:
        item = fuzzy_item.Item(title=bm["title"], subtitle=bm["url"])
        item.set_fuzzy_match_name(bm["title"])
        item.open_url(bm["url"])
        items.append(item)

    if query:
        matcher = fuzzy_item.FuzzyItemMatcher.from_items(items)
        matched = matcher.match(query, threshold=0)
        items = matched if matched else items

    return afwf.ScriptFilter(items=items)
```

Alfred Script field: `my-workflow search-bookmarks --query '{query}'`  
`argumenttype: 1` (required) in plist.

### Read-Only Script Filter (Alfred-side filtering)

```python
# open_file.py — runs once; Alfred filters client-side
@afwf.log_error()
def main() -> afwf.ScriptFilter:
    sf = afwf.ScriptFilter()
    for p in sorted(Path("examples/").glob("*.py")):
        item = afwf.Item(title=p.name, subtitle=f"Open {p.name}")
        item.match = p.name          # Alfred filters on this
        item.autocomplete = p.name   # Tab completion
        item.open_file(path=str(p.resolve()))
        sf.items.append(item)
    return sf
```

Alfred Script field: `my-workflow open-file` (no query arg)  
`argumenttype: 2` (no argument) + `alfredfiltersresults: true` in plist.

### Write Action (run_script + send_notification)

```python
# write_file.py
import sys
from pathlib import Path
import afwf.api as afwf

path_file = Path.home() / ".alfred-afwf" / "file.txt"

def _build_cmd(content: str) -> str:
    bin_cli = Path(sys.executable).parent / "my-workflow"
    return f"{bin_cli} write-file-request --content {content!r}"

@afwf.log_error()
def main(query: str) -> afwf.ScriptFilter:
    item = afwf.Item(title=f"Write: {query}", subtitle=str(path_file))
    item.run_script(_build_cmd(query))
    item.send_notification(title="File written", subtitle=query)
    return afwf.ScriptFilter(items=[item])

def write_request(content: str) -> None:
    """Called by Alfred's Run Script widget — separate from main()."""
    path_file.parent.mkdir(parents=True, exist_ok=True)
    path_file.write_text(content)
```

`cli.py` exposes both as separate subcommands. Alfred workflow graph:
```
Script Filter → Conditional (run_script=y) → Run Script {query}
                                                  └→ Post Notification
```

### Conditional Item Display (file-not-found error state)

```python
@afwf.log_error()
def main() -> afwf.ScriptFilter:
    if not path_file.exists():
        item = afwf.Item(
            title=f"{path_file} does not exist",
            icon=afwf.Icon(path=IconFileEnum.error),
        )
    else:
        content = path_file.read_text()
        item = afwf.Item(title=str(path_file), subtitle=content)
    return afwf.ScriptFilter(items=[item])
```

---

## Testing

All tests run with plain `pytest` — no Alfred needed.

### Pattern 1: Standalone file with coverage

```python
# tests/test_search_bookmarks.py
class TestMain:
    def test_empty_query_returns_all(self):
        sf = main(query="")
        assert len(sf.items) == 20

    def test_query_filters_results(self):
        sf = main(query="python")
        assert any("Python" in item.title for item in sf.items)

if __name__ == "__main__":
    from afwf.tests import run_cov_test
    run_cov_test(__file__, "my_pkg.search_bookmarks", preview=False)
```

Run: `python tests/test_search_bookmarks.py` → runs pytest + coverage for that module only.

### Pattern 2: Monkeypatching module-level state

```python
import my_pkg.write_file as mod

def test_creates_file(self, tmp_path, monkeypatch):
    p = tmp_path / "file.txt"
    monkeypatch.setattr(mod, "path_file", p)   # patch on module object
    mod.write_request("hello")
    assert p.read_text() == "hello"
```

For settings singletons imported at module load time, patch **both** the source module and the importing module:
```python
monkeypatch.setattr(settings_mod, "settings", patched)
monkeypatch.setattr(mod, "settings", patched)          # also patch the import
```

For cache + memoized functions (decorator applied at import time):
```python
mod.cache = TypedCache(tmp_path / ".cache")
mod._get_value = mod.cache.typed_memoize(expire=5)(lambda key: random.randint(1, 1000))
```

### Pattern 3: Testing log_error via `__wrapped__`

```python
def test_error_writes_log(self, tmp_path):
    from afwf.decorator import log_error

    log_file = tmp_path / "test.log"
    patched_main = log_error(log_file=log_file)(main.__wrapped__)  # unwrap, re-decorate

    with pytest.raises(ValueError, match="simulated Python error"):
        patched_main(query="error")

    assert "ValueError" in log_file.read_text()
```

### Pattern 4: Assert on model, not serialized JSON

```python
# Good
item = sf.items[0]
assert item.variables["run_script"] == "y"
assert "write-file-request" in item.arg

# Avoid — brittle
assert '"run_script": "y"' in json.dumps(sf.to_script_filter())
```

**Don't test:** Alfred widget routing, `to_script_filter()` output format, `uvx` invocation.

---

## Deployment

### Dev (local venv)

Alfred Script field: `.venv/bin/my-workflow search-items --query '{query}'`

### Production (uvx)

```bash
~/.local/bin/uvx --from "my-pkg[fuzzy,cache]==1.0.1" \
    my-workflow search-items --query '{query}'
```

`uvx` downloads, caches, and runs the pinned version — no virtualenv to manage. Latency is negligible after the first call (cached in `~/.cache/uv/`).

### Release checklist

1. Bump version in `_version.py`
2. Run `mise run cov` (full test suite)
3. `uv build && uv publish`
4. Update `script` field in Alfred's plist for each Script Filter
5. Re-export `.alfredworkflow` bundle if distributing to users

### `info.plist` key fields for Script Filter nodes

```xml
<key>keyword</key><string>my-search</string>
<key>script</key><string>.venv/bin/my-workflow search-items --query '{query}'</string>
<key>argumenttype</key><integer>1</integer>  <!-- 0=optional 1=required 2=none -->
<key>alfredfiltersresults</key><false/>       <!-- false=Python filters, true=Alfred filters -->
```

Keep `info.plist` in repo with **dev** paths. Production paths only live in Alfred's installed copy.

---

## Quick Reference

```python
import afwf.api as afwf
from afwf.api import IconFileEnum

# Minimal Script Filter
@afwf.log_error()
def main(query: str) -> afwf.ScriptFilter:
    item = afwf.Item(title="Hello", subtitle=query)
    item.open_url("https://example.com")
    return afwf.ScriptFilter(items=[item])

# In CLI: main(query=query).send_feedback()
```

| Need | Use |
|---|---|
| Return items to Alfred | `ScriptFilter(items=[...]).send_feedback()` |
| Open URL on Enter | `item.open_url(url)` |
| Open file on Enter | `item.open_file(path=...)` |
| Run shell command on Enter | `item.run_script(cmd)` + `sys.executable` trick |
| Notify on Enter | `item.send_notification(title, subtitle)` |
| Fuzzy filter items | `FuzzyItemMatcher.from_items(items).match(query)` |
| Cache slow calls | `@cache.typed_memoize(expire=60)` |
| Parse multi-token query | `Query.from_str(query).n_trimmed_parts` |
| Log errors to disk | `@afwf.log_error(log_file="...")` |
| Error icon | `afwf.Icon(path=IconFileEnum.error)` |