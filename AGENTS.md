#biz.dfch.AsdSte100Rules Agent Instructions

## Setup

Install dependencies with `uv`. Do not use pip, poetry, or pdm.

```bash
uv sync                # runtime deps only
uv sync --extra dev    # + ruff, pylint, mypy, twine, build (needed for lint/typecheck)
uv sync --extra test   # + ruff, pylint, coverage, parameterized (subset of dev)
```

`ruff`, `pylint` and `mypy` are **not** installed by a plain `uv sync` — they live
in the `dev`/`test` optional-dependency groups in `pyproject.toml`. `uv run ruff …`
fails with "No such file or directory" until you sync one of those extras.

Python: `.python-version` pins **3.11** locally; `pyproject.toml` requires `>=3.11`
and is tested against 3.11–3.13.

## Real entry point (root `main.py` is a stale stub, ignore it)

The actual application is the Typer CLI in the installed package, not
`main.py` (which just prints "Hello from …" and is unrelated leftover
scaffolding):

```bash
uv run rules --help                                   # installed console script
uv run python -m biz.dfch.asdste100rules.cli --help   # equivalent module invocation
```

CLI commands: `find`, `match`, `search`, `section`, `category`, `examples`,
`overview`, `toc` — all in `src/biz/dfch/asdste100rules/commands/`, each a thin
wrapper around the `Rules` query class (see below), registered in `cli.py`.

CLI quirks (`src/biz/dfch/asdste100rules/cli.py`):
- Loads a `.env` at import time by walking up from the module's own directory
  first, then from the CWD; an explicit file can be passed via the global
  `--env` option (which then overrides).

## Package layout

- Src-layout: real code lives under `src/biz/dfch/asdste100rules/`, not at
  repo root. `[tool.setuptools.packages.find]` has `where = ["src"]`.
- `src/biz/` and `src/biz/dfch/` intentionally have **no** `__init__.py` —
  they are implicit PEP 420 namespace packages (`namespaces = true` in
  `pyproject.toml`). Only `.../asdste100rules/` is a regular package. Do not
  "fix" this by adding `__init__.py` to the parent dirs.
- `models/` holds the **pydantic** data model (`Rule`, `ContentItem`,
  `EntryType`, `ContentType` StrEnums) — frozen (`frozen=True`) and closed
  (`extra="forbid"`). This differs from the sibling `biz.dfch.AsdSte100Vocab`
  repo, which uses `dataclass`+`dacite`; that convention was deliberately
  **not** carried over here.
- `rules.py` defines `Rules`, the query container (`find`, `by_section`,
  `by_category`, `match`, `search`, `filter`, `examples`, `overview`, `toc`,
  `sort`, …) that all CLI commands and any future MCP-server wrapper are
  expected to call — treat it as the one public API surface, not the CLI.
  `match()` searches only `name`/`summary`; `search()` is the full-text
  variant — it also searches every `ContentItem.data` in `contents` (prose,
  notes, STE/non-STE examples, technical noun/verb lists), optionally
  restricted to specific `ContentType`s via `content_types=`. Prefer
  `search()` over `match()` for an LLM/MCP caller looking for "which rule
  covers X" without knowing section/category/id upfront. `overview()`
  returns lightweight `RuleOverview` records (id/type/section/category/name +
  example/note/text-count and technical-noun/technical-verb stats, summary
  only when `brief=False`) so a caller can survey what rules exist without
  pulling in every `Rule.contents` item. `toc()` goes one level higher,
  returning the distinct `(section, category, ids)` triples in document
  order for a quick structural outline, where `ids` lists every rule /
  recommendation / information id in that pair; the `toc` CLI command
  renders `ids` as a single space-separated column.
- `builtin_rules.py` resolves the packaged data file via
  `importlib.resources`; loading is resilient — a malformed entry is skipped
  with a printed `[ERROR] entry #N: …` message rather than raising.
- Data ships as package data:
  `src/biz/dfch/asdste100rules/data/*.json` (declared in
  `[tool.setuptools.package-data]`). The file is a single pretty-printed
  JSON array (66 entries in `asdste100_issue9_rules.json`), not one-object-
  per-line JSON Lines.
- Every source file starts with an AGPL-3.0-or-later license header + SPDX
  identifier comment; match this in new files (see any existing file under
  `src/` for the exact boilerplate).
- Python 3.11+ typing style: use `list[...]`, `dict[...]`, `X | None` — never
  `typing.List`, `typing.Optional`, `typing.Dict`.

## Tests

- No pytest config/dependency exists; CONTRIBUTING.md and the current setup
  point to **`unittest`**, not pytest.
- `tests/` mirrors the package layout (`tests/asdste100rules/`), 57 tests
  covering the pydantic models and the `Rules` container (loading, querying,
  sorting, serialization, malformed-entry resilience).
- Run with: `uv run python -m unittest discover -s tests`
- Test fixtures live alongside the tests as small JSON files
  (`test_rules_*.json`) referenced through the `RulesFile` enum in
  `tests/asdste100rules/rules_file.py` — add new fixtures there rather than
  inlining JSON strings in test bodies.

## Lint / typecheck (after `uv sync --extra dev`)

```bash
uv run ruff check .     # line-length 120, rules E, F, W
uv run pylint src       # max-line-length 120
uv run mypy src         # package ships py.typed
```
All three currently pass clean on `src/` (one pre-existing, harmless
`missing-module-docstring` pylint note on `info.py`).

## Misc

- `uv.lock` — do not edit manually.
- License: AGPL-3.0-or-later. See `CONTRIBUTING.md` for branch/PR process.
