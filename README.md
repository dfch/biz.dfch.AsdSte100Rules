# biz.dfch.AsdSte100Rules

[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfch/biz.dfch.AsdSte100Rules/actions/workflows/ci.yml/badge.svg)](https://github.com/dfch/biz.dfch.AsdSte100Rules/actions/workflows/ci.yml)
[![TestPyPI version](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/biz-dfch-asdste100rules/json&label=TestPyPI&query=$.info.version&color=orange)](https://test.pypi.org/project/biz-dfch-asdste100rules/)
[![PyPI version](https://img.shields.io/badge/dynamic/json?url=https://www.pypi.org/pypi/biz-dfch-asdste100rules/json&label=PyPI&query=$.info.version&color=blue)](https://www.pypi.org/project/biz-dfch-asdste100rules/)
[![PyPI downloads](https://img.shields.io/pypi/dm/biz-dfch-asdste100rules.svg)](https://pypistats.org/packages/biz-dfch-asdste100rules)

## Table of Contents

- [Introduction](#introduction)
- [Data model](#data-model)
- [Installation](#installation)
- [Command line usage](#command-line-usage)
- [Related Projects](#related-projects)
- [Make a Release](#make-a-release)
- [License](#license)

## Introduction

This is a Python library, that implements the [ASD-STE100 Issue 9](https://www.asd-ste100.org/) rules, recommendations, and section-introduction blocks (rule sections 1-11 and the General Recommendations), as a queryable ruleset. A [`Rule`](./src/biz/dfch/asdste100rules/models/rule.py) has these properties:

* [`type_`](./src/biz/dfch/asdste100rules/models/entry_type.py), is this entry a `RULE`, a `RECOMMENDATION`, or an `INFORMATION` (section-intro) block?
* `id_`, the rule id, e.g. `R1.5` or `GR-3`
* `ref`, the page reference in the ASD-STE100 Issue 9 document
* `section`, the section name, e.g. "Words"
* `category`, the category within the section, e.g. "Technical nouns"
* `name`, the rule's short title
* `summary`, the rule's summary text
* [`contents`](./src/biz/dfch/asdste100rules/models/content_item.py), a `list` of content blocks that make up the rule's body

Each [`ContentItem`](./src/biz/dfch/asdste100rules/models/content_item.py) in `contents` has a [`type_`](./src/biz/dfch/asdste100rules/models/content_type.py) (`text`, `heading`, `note`, `comment`, `example`, `ste_example`, `nonste_example`, `not_recommended`, `technical_nouns`, or `technical_verbs`) and its `data`.

The [`Rules`](./src/biz/dfch/asdste100rules/rules.py) class is the query container over a list of `Rule` entries — loaded from the packaged built-in ASD-STE100 Issue 9 ruleset, from your own JSON file(s), or both — and offers `find`, `by_section`, `by_category`, `match`, `search`, `filter`, `examples`, `overview`, and `toc`.

[biz.dfch.AsdSte100Mcp](https://github.com/dfch/biz.dfch.AsdSte100Mcp) uses this library to expose the ruleset over MCP.

ASD-STE100: Copyright by (c) [ASD](https://www.asd-europe.org/).

I am in no way affiliated with ASD. ASD does not endorse my work.

## Data model

The built-in ASD-STE100 Issue 9 ruleset ships as a single packaged JSON file, [`data/asdste100_issue9_rules.json`](./src/biz/dfch/asdste100rules/data/asdste100_issue9_rules.json) — a pretty-printed JSON array of 66 entries (rules, recommendations, and section-introduction blocks), one object per `Rule`:

```json
{
  "type_": "rule",
  "id_": "R1.1",
  "ref": "Issue 9 page 1-1-2",
  "section": "Words",
  "category": "Which words can you use?",
  "name": "Use words that are: ...",
  "summary": "Simplified Technical English (STE) has a controlled dictionary ...",
  "contents": [
    { "type_": "text", "data": "A technical noun is a noun term ..." },
    { "type_": "example", "data": "- The word **use** is an approved verb ..." },
    { "type_": "note", "data": "In the context of ISO 1087:2019 ..." }
  ]
}
```

Loading is resilient: a malformed entry is skipped with a printed `[ERROR] entry #N: ...` message instead of raising, so one bad entry cannot break the whole ruleset.

You can point `Rules` (or any `rules` CLI command, via `--file`) at your own JSON file(s) in the same shape to extend or replace the built-in ruleset, e.g. to add company-specific rules or recommendations alongside the ASD-STE100 Issue 9 baseline.

## Installation

[biz-dfch-asdste100rules](https://pypi.org/project/biz-dfch-asdste100rules/) is on [PyPI](https://pypi.org). Create a virtual environment and install the library with `pip`:

```
pip install biz-dfch-asdste100rules
```

Or install with `uv`:

```
uv add biz-dfch-asdste100rules
```

## Command line usage

Installing the package also installs the `rules` console script:

```
uv run rules --help
```

```
Usage: rules [OPTIONS] COMMAND [ARGS]...

 Commands:
 find      Find a rule or recommendation by exact id.
 match     Find rules matching a regular expression pattern.
 section   Find rules by exact section name.
 category  Find rules by exact category name.
 examples  Find example content items across rules.
 overview  Give a lightweight overview of the rules in the ruleset.
 search    Find rules whose text matches a regular expression pattern.
 toc       List the distinct section/category pairs in the ruleset.
```

### Examples

Look up a single rule by id:

```
uv run rules find R1.5
```

List the document structure (section/category pairs and the ids they contain):

```
uv run rules toc
```

Full-text search across every rule's section, category, name, summary, and content (notes, examples, technical noun/verb lists, ...), optionally narrowed to one content type:

```
uv run rules search "technical noun" --content-type note
```

Get a lightweight overview (id, type, section, category, name, and content stats) without pulling in the rule bodies:

```
uv run rules overview --section Words
```

Collect only the STE examples for a section:

```
uv run rules examples --section Words --kind ste_example
```

Every command accepts `--file` (repeatable) to merge in your own JSON rules file(s) alongside, or instead of (`--no-builtin`), the built-in ASD-STE100 Issue 9 ruleset.

## Related Projects

This library is part of the ASD-STE100 tooling family:

* [biz.dfch.AsdSte100Vocab](https://github.com/dfch/biz.dfch.AsdSte100Vocab) — the ASD-STE100 Issue 9 vocabulary library
* [biz.dfch.AsdSte100Rules](https://github.com/dfch/biz.dfch.AsdSte100Rules) — this repo: the ASD-STE100 Issue 9 ruleset library
* [biz.dfch.AsdSte100Nlp](https://github.com/dfch/biz.dfch.AsdSte100Nlp) — WordNet-based synonym lookup for ASD-STE100 words
* [biz.dfch.AsdSte100Lookup](https://github.com/dfch/biz.dfch.AsdSte100Lookup) — an interactive CLI to look up words and rules
* [biz.dfch.AsdSte100Mcp](https://github.com/dfch/biz.dfch.AsdSte100Mcp) — an MCP server exposing vocabulary and rules lookup tools

## Make a Release

### 1. Make sure that all tests are satisfactory

Before you make the release, make sure the CI pipeline is green on the `dev` branch:

```
uv run --frozen ruff format --check
uv run --frozen ruff check
uv run --frozen pylint $(git ls-files '*.py') || true
uv run --frozen python -m unittest discover -v -s tests -t . -p "test_*.py"
```

### 2. Increase the version

Update the version in `pyproject.toml`:

```toml
version = "x.y.z"
```

### 3. Commit and push to `dev`

```
git add pyproject.toml
git commit -m "chore: bump version to vx.y.z"
git push origin dev
```

### 4. Merge `dev` into `main`

```
git checkout main
git merge dev
git push origin main
```

### 5. Create and push a version tag

This will create a binary artifact of the application and add it to the `release`.

```
export VERSION=x.y.z
git tag v${VERSION}
git push origin v${VERSION}
```

Then, select the `dev` branch to continue your work.

```
git checkout dev
```

Pushing the tag automatically triggers the `publish.yml` workflow, which will:
* build the `sdist` and `wheel` with `uv build`
    (**this step creates the artifact**)
* create a GitHub Release with auto-generated release notes
* upload the files as a release artifact
    (**this step adds the artifact to the release**)

## License

This library is licensed under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0). See [LICENSE](./LICENSE) for more information.

ASD-STE100 Simplified Technical English (Standard for Technical Documentation), Issue 9

Copyright 2025 [Aerospace, Security and Defence Industries Association of Europe (ASD)](https://www.asd-europe.org), https://www.asd-europe.org.

This library or the maintainer is not affiliated with ASD. ASD does not endorse this library or the maintainer.
