# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-08-01

### Fixed

- Ship the missing `py.typed` marker file (PEP 561) so that consumers of
  this package get proper type information instead of mypy reporting
  `Skipping analyzing "biz.dfch.asdste100rules": module is installed, but
  missing library stubs or py.typed marker [import-untyped]`.

## [0.1.0] - 2026-08-01

### Added

- Pydantic data model (`Rule`, `ContentItem`, `EntryType`, `ContentType`,
  `RuleOverview`) for the ASD-STE100 Issue 9 rules, recommendations, and
  section-introduction blocks.
- Built-in ASD-STE100 Issue 9 ruleset, packaged as JSON data (66 entries),
  with a loader that skips a malformed entry and prints an error instead
  of raising.
- `Rules` query container with `find`, `by_section`, `by_category`,
  `match`, `search`, `filter`, `examples`, `overview`, and `toc`.
- `rules` console script (Typer CLI) with `find`, `match`, `search`,
  `section`, `category`, `examples`, `overview`, and `toc` commands.
- README with an Introduction, a Data model section, Installation
  instructions, and CLI usage examples.
- NOTICE file with the project license header and third-party license
  notices for `pydantic`, `python-dotenv`, and `typer`.
- GitHub Actions CI workflow (`ruff`, `pylint`, `unittest` across Python
  3.11, 3.12, and 3.13), a publish workflow, a dependabot configuration,
  and issue templates.

### Fixed

- CI: pass the matrix Python version to every `uv run --frozen` step, so
  it does not fall back to the `.python-version` pin and silently lose
  the dev dependencies.

[Unreleased]: https://github.com/dfch/biz.dfch.AsdSte100Rules/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/dfch/biz.dfch.AsdSte100Rules/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dfch/biz.dfch.AsdSte100Rules/releases/tag/v0.1.0

