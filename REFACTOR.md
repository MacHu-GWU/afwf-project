# Refactor Plan

## Progress

| # | File | Task | Status |
|---|------|------|--------|
| 1 | `pyproject.toml` | Add `fuzzy`/`cache` opt groups, drop `fuzzywuzzy`, keep `attrs` until done | ⬜ Pending |
| 2 | `opt/fuzzy/impl.py` | Replace `fuzzywuzzy` → `rapidfuzz`, fix 3-tuple unpack | ⬜ Pending |
| 3 | `query.py` | `attrs` → `pydantic BaseModel` | ⬜ Pending |
| 4 | `script_filter_object.py` | `attrs` → `pydantic BaseModel`, update `to_script_filter()` | ⬜ Pending |
| 4a | `test_script_filter_object.py` | Remove `@attr.define` + `AttrsClass.ib_*` (required small edit) | ⬜ Pending |
| 5 | `item.py` | `attrs` → `pydantic`, `Literal` for enum validation | ⬜ Pending |
| 6 | `script_filter.py` | `attrs` → `pydantic` | ⬜ Pending |
| 7 | `handler.py` | `attrs` → `pydantic` | ⬜ Pending |
| 8 | `workflow.py` | `attrs` → `pydantic`, `__attrs_post_init__` → `model_post_init` | ⬜ Pending |
| 9 | `opt/fuzzy_item/impl.py` | Remove `@attr.define` from `Item` subclass | ⬜ Pending |
| 10 | all | Remove all `attrs`/`attrs_mate` imports, drop from deps | ⬜ Pending |

> Status: ⬜ Pending · 🔄 In Progress · ✅ Done · ❌ Blocked

---

Target: Alfred 5.7, Python ≥ 3.10

Goals:
- Replace `attrs` + `attrs_mate` → `pydantic v2`
- Replace `fuzzywuzzy` → `rapidfuzz`
- Move optional deps into `pyproject.toml` opt groups
- Minimize test changes (only `test_script_filter_object.py` needs small edits)

---

## Dependency Graph

```
script_filter_object.py   ← attrs base (BLOCKER: test uses @attr.define on subclass)
  └── item.py             ← attrs
        └── script_filter.py ← attrs
              ├── handler.py  ← attrs
              │     └── workflow.py ← attrs
              └── opt/fuzzy_item/impl.py ← @attr.define subclass of Item

query.py                  ← attrs (test is behavior-only, easy)
opt/fuzzy/impl.py         ← fuzzywuzzy (no attrs, just dataclasses)
opt/cache/impl.py         ← diskcache (no attrs, already clean)
```

---

## Step 1 — `pyproject.toml` deps

```toml
[project]
dependencies = [
    "pydantic>=2.0.0,<3.0.0",
    # remove: attrs, attrs_mate
]

[project.optional-dependencies]
fuzzy = [
    "rapidfuzz>=3.0.0,<4.0.0",
]
cache = [
    "diskcache>=5.6.3,<6.0.0",
]
dev = [
    "rich>=13.8.1,<14.0.0",
    "pathlib-mate>=1.3.2,<2.0.0",
    "rapidfuzz>=3.14.1,<4.0.0",
    "diskcache>=5.6.3,<6.0.0",
]
```

Remove `fuzzywuzzy` entirely. Keep `attrs`/`attrs_mate` in deps until all source files are migrated.

---

## Step 2 — `afwf/opt/fuzzy/impl.py` (fuzzywuzzy → rapidfuzz)

No attrs involvement. Change:

```python
# Before
from fuzzywuzzy import process
matched_name_list = process.extractBests(name, self._names, limit=limit)
best_matched_name, best_matched_score = matched_name_list[0]
for matched_name, score in matched_name_list:
    ...

# After — rapidfuzz returns (string, score, index) 3-tuple
from rapidfuzz import process
matched_name_list = process.extractBests(name, self._names, limit=limit)
best_matched_name, best_matched_score, _ = matched_name_list[0]
for matched_name, score, _ in matched_name_list:
    ...
```

Also remove the `has_fuzzywuzzy` try/except guard, replace with `rapidfuzz` import (always available as opt dep).

**Test impact**: `test_opt_fuzzy.py` — no changes needed, behavior is identical.

---

## Step 3 — `afwf/query.py` (attrs → pydantic)

```python
# Before
@attrs.define
class Query(AttrsClass):
    raw: str = AttrsClass.ib_str(nullable=False)
    parts: T.List[str] = AttrsClass.ib_list_of_str(nullable=False)
    trimmed_parts: T.List[str] = AttrsClass.ib_list_of_str(nullable=False)

# After
from pydantic import BaseModel

class Query(BaseModel):
    raw: str
    parts: T.List[str]
    trimmed_parts: T.List[str]
    # classmethod from_str and properties n_parts/n_trimmed_parts unchanged
```

**Test impact**: `test_query.py` — no changes needed.

---

## Step 4 — `afwf/script_filter_object.py` (attrs → pydantic)

This is the core change. Key decision: `to_script_filter()` filters **falsy** values (not just None).

```python
# Before
import attrs
from attrs_mate import AttrsClass

@attrs.define
class ScriptFilterObject(AttrsClass):
    def to_script_filter(self) -> dict:
        dct = dict()
        for k, v in attrs.asdict(self, recurse=False).items():
            if v: ...

# After
from pydantic import BaseModel

class ScriptFilterObject(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    def to_script_filter(self) -> dict:
        dct = dict()
        for k in self.model_fields:
            v = getattr(self, k)
            if v:
                if isinstance(v, ScriptFilterObject):
                    v1 = v.to_script_filter()
                    if v1:
                        dct[k] = v1
                elif isinstance(v, list):
                    lst = []
                    for i in v:
                        if isinstance(i, ScriptFilterObject):
                            lst.append(i.to_script_filter())
                        else:
                            lst.append(i)
                    dct[k] = lst
                else:
                    dct[k] = v
        return dct
```

**Test impact**: `test_script_filter_object.py` — **requires small edits**:

```python
# Before (in test file)
import attr
from attrs_mate import AttrsClass

@attr.define
class Profile(ScriptFilterObject):
    firstname: str = AttrsClass.ib_str(default=None)
    lastname: str = AttrsClass.ib_str(default=None)
    ssn: str = AttrsClass.ib_str(default=None)

@attr.define
class Degree(ScriptFilterObject):
    name: str = AttrsClass.ib_str(default=None)
    year: int = AttrsClass.ib_int(default=None)

@attr.define
class People(ScriptFilterObject):
    id: int = AttrsClass.ib_int(default=None)
    profile: Profile = Profile.ib_nested(default=None)
    degrees: T.List[Degree] = Degree.ib_list(default=None)

# After (minimal diff)
import typing as T
from afwf.script_filter_object import ScriptFilterObject

class Profile(ScriptFilterObject):
    firstname: T.Optional[str] = None
    lastname: T.Optional[str] = None
    ssn: T.Optional[str] = None

class Degree(ScriptFilterObject):
    name: T.Optional[str] = None
    year: T.Optional[int] = None

class People(ScriptFilterObject):
    id: T.Optional[int] = None
    profile: T.Optional[Profile] = None
    degrees: T.Optional[T.List[Degree]] = None
```

This is the **only required test change** in the entire refactor.

---

## Step 5 — `afwf/item.py` (attrs → pydantic)

```python
# Before
@attrs.define
class Icon(ScriptFilterObject):
    path: str = AttrsClass.ib_str()
    type: str = attrs.field(validator=vs.optional(vs.in_(TypeEnum.get_values())), default=None)

@attrs.define
class Item(ScriptFilterObject):
    title: str = AttrsClass.ib_str()
    subtitle: str = AttrsClass.ib_str(default=None)
    icon: Icon = Icon.ib_nested(default=None)
    valid: bool = AttrsClass.ib_bool(default=True)
    variables: dict = AttrsClass.ib_dict(factory=dict)
    type: str = attrs.field(validator=vs.optional(vs.in_(TypeEnum.get_values())), default=None)
    ...

# After
from typing import Optional, Literal
from pydantic import Field, field_validator

class Icon(ScriptFilterObject):
    path: str
    type: Optional[Literal["fileicon", "filetype"]] = None

class Item(ScriptFilterObject):
    title: str
    subtitle: Optional[str] = None
    icon: Optional[Icon] = None
    valid: bool = True
    variables: dict = Field(default_factory=dict)
    type: Optional[Literal["file", "file:skipcheck"]] = None
    mods: Optional[dict] = None
    action: Optional[T_ITEM_ACTION] = None
    text: Optional[Text] = None
    ...
```

Note: `Literal` replaces the `vs.in_()` validators — cleaner and more IDE-friendly.

**Test impact**: `test_item.py` — no changes needed.

---

## Step 6 — `afwf/script_filter.py` (attrs → pydantic)

```python
# Before
@attrs.define
class ScriptFilter(ScriptFilterObject):
    items: T.List[Item] = Item.ib_list_of_nested()
    variables: dict = AttrsClass.ib_dict(default=None)
    rerun: float = AttrsClass.ib_float(default=None)

# After
class ScriptFilter(ScriptFilterObject):
    items: T.List[Item] = Field(default_factory=list)
    variables: Optional[dict] = None
    rerun: Optional[float] = None
```

**Test impact**: `test_script_filter.py` — no changes needed.

---

## Step 7 — `afwf/handler.py` (attrs → pydantic)

```python
# Before
@attrs.define
class Handler(AttrsClass):
    id = AttrsClass.ib_str(nullable=False)

# After
class Handler(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    id: str
    # all methods unchanged
```

No test for this file directly.

---

## Step 8 — `afwf/workflow.py` (attrs → pydantic)

```python
# Before
@attrs.define
class Workflow(AttrsClass):
    handlers: T.Dict[str, Handler] = attrs.field(factory=dict)

    def __attrs_post_init__(self):
        if dir_lib.exists():
            sys.path.append(str(dir_lib))

# After
class Workflow(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    handlers: T.Dict[str, Handler] = Field(default_factory=dict)

    def model_post_init(self, __context) -> None:
        if dir_lib.exists():
            sys.path.append(str(dir_lib))
    # all other methods unchanged
```

---

## Step 9 — `afwf/opt/fuzzy_item/impl.py` (remove @attr.define)

```python
# Before
@attr.define
class Item(Item_):
    ...

# After — pydantic subclass needs no decorator
class Item(Item_):
    ...
```

**Test impact**: `test_opt_fuzzy_item.py` — no changes needed.

---

## Step 10 — Cleanup

- Remove `attrs`, `attrs_mate` from `pyproject.toml` `[project.dependencies]`
- Remove all `import attr`, `import attrs`, `from attrs_mate import AttrsClass` across codebase
- Remove `opt/cache` and `opt/fuzzy` guard try/except import patterns — replace with clean imports (deps are guaranteed by opt groups)

---

## Summary Table

| Step | File | Change | Test Change? |
|------|------|--------|-------------|
| 1 | `pyproject.toml` | add rapidfuzz/cache opt groups, drop fuzzywuzzy | — |
| 2 | `opt/fuzzy/impl.py` | fuzzywuzzy → rapidfuzz, unpack 3-tuple | No |
| 3 | `query.py` | attrs → pydantic BaseModel | No |
| 4 | `script_filter_object.py` | attrs → pydantic BaseModel | **Yes (small)** |
| 5 | `item.py` | attrs → pydantic, Literal for enum validation | No |
| 6 | `script_filter.py` | attrs → pydantic | No |
| 7 | `handler.py` | attrs → pydantic | No |
| 8 | `workflow.py` | attrs → pydantic, post_init hook | No |
| 9 | `opt/fuzzy_item/impl.py` | remove @attr.define | No |
| 10 | all | remove attrs/attrs_mate imports | — |
