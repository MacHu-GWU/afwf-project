# Alfred Workflow Python Development in the uvx Era

The cleanest way to ship Alfred Workflows in Python today.

---

## The Core Idea

Stop bundling a virtualenv inside your workflow folder. Instead:

1. **Publish your workflow logic as a normal Python package on PyPI.**
2. **Expose every Script Filter as a CLI subcommand** (one subcommand = one Script Filter widget).
3. **Call it from Alfred using `uvx`** — no installation, no PATH hacks, version-pinned.

```
~/.local/bin/uvx your-package@1.2.3 subcommand --query '{query}'
```

That single line is the entire Alfred script. `uvx` downloads, caches, and runs the right version automatically. Upgrading means bumping the version number in Alfred — nothing else.

---

## Why uvx

| Old way | uvx way |
|---|---|
| Hardcode `.venv/bin/python` path in Alfred | `~/.local/bin/uvx pkg@version cmd` |
| Breaks when venv moves or Python upgrades | Always works, self-contained |
| Each machine needs manual setup | Zero setup — uvx caches on first run |
| Version drift between machines | Version pinned in the Alfred script itself |

---

## Project Structure

```
your-workflow-project/
├── your_package/
│   ├── __init__.py
│   ├── cli.py          ← fire CLI, one method per Script Filter
│   └── handlers/
│       └── open_url.py ← afwf Handler (or skip and inline the logic)
├── pyproject.toml      ← exposes the CLI as a script entry point
└── ...
```

The handler layer is optional. For simple Script Filters you can inline everything directly in `cli.py`.

---

## The Stack

- **[afwf](https://github.com/MacHu-GWU/afwf-project)** — builds the Script Filter JSON (`Item`, `ScriptFilter`, `Handler`)
- **[fire](https://github.com/google/python-fire)** — turns a Python class into a CLI with zero boilerplate
- **[uv](https://github.com/astral-sh/uv) / uvx** — runs the CLI directly from PyPI, no install needed

---

## Step 1 — Write the Handler

```python
# your_package/handlers/open_url.py
from afwf.handler import Handler
from afwf.script_filter import ScriptFilter
from afwf.item import Item


class OpenUrlHandler(Handler):
    def parse_query(self, query: str) -> dict:
        return {}                    # no-argument Script Filter

    def encode_query(self, **kwargs) -> str:
        return ""

    def main(self) -> ScriptFilter:
        sf = ScriptFilter()
        for title, url in [
            ("Alfred App", "https://www.alfredapp.com/"),
            ("Python",     "https://www.python.org/"),
            ("GitHub",     "https://github.com/"),
        ]:
            item = Item(title=title, subtitle=f"open {url}", arg=url)
            item.open_url(url=url)
            sf.items.append(item)
        return sf


handler = OpenUrlHandler(id="open_url")
```

---

## Step 2 — Wire It to a CLI

```python
# your_package/cli.py
import json


class Command:
    def open_url(self, query: str = ""):
        from your_package.handlers.open_url import handler
        sf = handler.handler(query)
        print(json.dumps(sf.to_script_filter()))


def main():
    import fire
    fire.Fire(Command)
```

Each method on `Command` = one Script Filter subcommand. Adding a new Script Filter means adding one method.

---

## Step 3 — Expose the Entry Point

```toml
# pyproject.toml
[project.scripts]
your-package = "your_package.cli:main"

[project.dependencies]
dependencies = [
    "afwf>=1.0.1,<2.0.0",
    "fire>=0.7.0,<1.0.0",
]
```

Publish to PyPI:

```bash
uv build && uv publish
```

---

## Step 4 — Configure Alfred

In the Script Filter widget:

| Field | Value |
|---|---|
| Language | `/bin/zsh` |
| with input as | `{query}` |
| Script | `~/.local/bin/uvx your-package@1.2.3 open_url --query '{query}'` |
| Alfred filters results | unchecked (filter in Python) |

That's the entire Alfred configuration. No workflow folder, no venv, no `main.py`.

---

## Upgrading

1. Bump the version in `pyproject.toml`, publish.
2. Change `@1.2.3` → `@1.2.4` in the Alfred Script field.

Done. No other changes needed anywhere.

---

## Fuzzy Filtering Inside the Handler

If you want Alfred-style fuzzy search, filter inside `main()` before building items:

```python
def main(self, query: str) -> ScriptFilter:
    candidates = get_all_items()
    results = [c for c in candidates if query.lower() in c.lower()] if query else candidates
    sf = ScriptFilter()
    for r in results[:50]:
        sf.items.append(Item(title=r, arg=r))
    return sf
```

Or use `afwf`'s optional fuzzy module (`afwf.opt.fuzzy`) for ranked matching.

---

## Testing Without Alfred

```bash
# install locally
uv pip install -e .

# run like Alfred would
your-package open_url --query "git"

# or pin-test against a published version
~/.local/bin/uvx your-package@1.2.3 open_url --query "git"
```

What you see in the terminal is exactly what Alfred receives.
