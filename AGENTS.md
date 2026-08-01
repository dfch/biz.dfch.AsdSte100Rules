#biz.dfch.AsdSte100Rules Agent Instructions

## Setup

Install dependencies with `uv`. Do not use pip, poetry, or pdm.

```bash
uv sync
```

The project uses Python 3.13 as declared in `.python-version` and `pyproject.toml`.

## Running the code

```bash
python main.py
```

Or with uv:

```bash
uv run python main.py
```

## Tooling status

- No tests exist yet. CONTRIBUTING.md mentions pytest, coverage, and unittest, but the project has no test files or pytest configuration in `pyproject.toml`.
- No lint, typecheck, formatter, or mypy configuration exists.
- Add tooling config (pytest, ruff, mypy) as needed and update this file.

## Structure

Only two source files:

- `main.py` — Entry point with a stub `main()` function.
- `pyproject.toml` — Project declaration. Requires Python >= 3.13. No dependencies declared yet.

Lockfile: `uv.lock` (do not edit manually).

## Contributing

See `CONTRIBUTING.md` for clone, branch, and pull request process. License: AGPL-3.0.
