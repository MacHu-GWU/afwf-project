# Project Guide for AI Assistants

This document guides AI assistants on how to navigate and work with this project.

## What is afwf

`afwf` is a Python SDK for building [Alfred](https://www.alfredapp.com/) workflows on macOS — it lets developers write Script Filter handlers in Python using an OOP API instead of hand-crafting JSON.

## Core Modules

### Script Filter JSON Protocol

Alfred Script Filters communicate via a [JSON protocol](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/). These modules implement it:

| Module | Key Class | Purpose |
|---|---|---|
| `afwf/script_filter_object.py` | `ScriptFilterObject` | Pydantic base class; `to_script_filter()` serialises to Alfred-compatible dict (handles None-omission, False-preservation, empty-object rules) |
| `afwf/item.py` | `Icon`, `Text`, `Item` | Alfred dropdown item model; `Item` has fluent `set_*` helpers (`open_url`, `run_script`, `open_file`, `send_notification`, etc.) that set workflow variable pairs |
| `afwf/script_filter.py` | `ScriptFilter` | Top-level response object; holds `items` list; `send_feedback()` dumps JSON to stdout |

### Constants & Icons

| Module | Key Class | Purpose |
|---|---|---|
| `afwf/constants.py` | `IconTypeEnum`, `ItemTypeEnum`, `ModEnum`, `VarKeyEnum`, `VarValueEnum` | All Alfred protocol string constants; `VarKeyEnum` defines the variable key names used by `Item.set_*` helpers |
| `afwf/icon.py` | `IconFileEnum` | Paths to ~50 bundled PNG icons (search, folder, star, git, error, …) |

### Optional Utilities (`afwf/opt/`)

| Module | Key Class | Purpose |
|---|---|---|
| `afwf/opt/cache/` | `TypedCache` | `diskcache`-backed disk cache with type-hint-safe `typed_memoize()` decorator; extra dep `afwf[cache]` |
| `afwf/opt/fuzzy/` | `FuzzyMatcher` | Generic fuzzy matcher over any item type using `rapidfuzz`; subclass and implement `get_name()`; extra dep `afwf[fuzzy]` |
| `afwf/opt/fuzzy_item/` | `Item`, `FuzzyItemMatcher` | `Item` subclass that stores a fuzzy-match name in `variables`; `FuzzyItemMatcher` wires it to `FuzzyMatcher` |

## Deployment Pattern (Best Practice)

Publish your workflow logic as a Python package on PyPI, expose it as a CLI using [fire](https://github.com/google-deepmind/python-fire), then invoke it from Alfred's Script Filter via `uvx`.

**Package structure:**
- `pyproject.toml` declares the CLI entry point, e.g. `afwf-examples = "afwf.examples.cli:main"`
- `afwf/examples/cli.py` — `fire.Fire(Command)` wrapping subcommands
- Each subcommand (e.g. `search_bookmarks`) calls `main(query=...).send_feedback()`

**Script Filter command:**

- Dev/local: `~/Documents/GitHub/afwf-project/.venv/bin/afwf-examples search-bookmarks --query '{query}'`
- Production (uvx): `~/.local/bin/uvx --from afwf==1.0.1 afwf-examples search-bookmarks --query '{query}'`

## Examples (`afwf/examples/`)

Demonstrate common workflow patterns. Each example has a corresponding test under `tests/examples/`.

- `search_bookmarks.py` — fuzzy search over a static list; items open URL via `item.open_url()`
- `memoize.py` — disk-cached handler using `afwf.opt.cache`; demonstrates `typed_memoize`
- `open_file.py` — open a file via `item.open_file()`
- `handlers/` — handler-style examples (open_url, open_file, write_file, set_settings, …)

**Workflow definition** for all examples is exported in `example.info.plist` (Alfred plist format, checked into repo).

## Project Overview

**What this project does:** Read `README.rst` for project description and purpose.

**Project type:** Python package

## Core Configuration Files

### Tool & Dependency Management
- `mise.toml` - Task runner and tool version management (Python 3.12, uv, claude)
- `pyproject.toml` - Python dependencies and package metadata
- `.venv/` - Virtual environment directory (created by uv)

Use `mise ls python --current` to see the exact Python version in use.

### CI/CD & Testing
- `.github/workflows/main.yml` - GitHub Actions CI workflow
- `codecov.yml` + `.coveragerc` - Code coverage reporting (codecov.io)
- `.readthedocs.yml` - Documentation hosting (readthedocs.org)

### Documentation
- `docs/source/` - Sphinx documentation source files
- `docs/source/conf.py` - Sphinx configuration

## Development Workflow

### Task Management
List all available tasks:
```bash
mise tasks ls
```

Run a specific task:
```bash
mise run ${task_name}
```

**Key tasks:**
- `inst` - Install all dependencies using uv (fast package manager)
- `cov` - Run unit tests with coverage report
- `build-doc` - Build Sphinx documentation

For complete task reference, run `mise run list-tasks` to generate `.claude/mise-tasks.md`.

### Testing Philosophy
This project uses **pytest** with a special pattern that allows running individual test files as standalone scripts.

**Example:** See `tests/test_api.py` - the `if __name__ == "__main__":` block demonstrates this pattern. It runs pytest as a subprocess with coverage tracking for the specific module, enabling quick isolated testing during development.

## Working with This Project

**Approach:**
1. Don't load entire files unnecessarily - read specific files only when needed
2. Use task commands (`mise run`) instead of direct tool invocation
3. Follow the testing pattern when creating new test files
4. Reference configuration files for specific settings rather than assuming defaults

**Tools in use:**
- **mise-en-place** - Development tool management
- **uv** - Fast Python package management
- **pytest** - Unit testing framework
- **sphinx** - Documentation generation
