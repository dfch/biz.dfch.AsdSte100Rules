# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Shared rendering helpers for CLI commands."""

import re

from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich import box

from ..models import ContentItem, EntryType, Rule, RuleOverview

# Colour used to highlight search-pattern matches within a cell (e.g. in
# the Section/Category/Name columns of `print_rule_table`).
_HIGHLIGHT_COLOR = "cyan"

# Colour used for the `Id` column specifically, when a `highlight_pattern`
# is given to `print_rule_table`; kept separate from `_HIGHLIGHT_COLOR` so
# it can be tuned independently of the in-cell match highlighting.
_ID_COLOR = "magenta"

# One colour per `EntryType`, applied consistently to every "Type" column
# and to the type shown in `print_rule_detail`, across every command:
# RULE is mandatory ("must"), RECOMMENDATION is advisory ("should"),
# INFORMATION is context-only prose.
_TYPE_COLOR: dict[EntryType, str] = {
    EntryType.RULE: "green",
    EntryType.RECOMMENDATION: "white",
    EntryType.INFORMATION: "yellow",
    EntryType.UNKNOWN: "white",
}


def _type_cell(type_: EntryType) -> str:
    """Return the `EntryType` value as Rich markup, coloured per `_TYPE_COLOR`."""

    color = _TYPE_COLOR.get(type_, "white")
    return f"[{color}]{escape(type_.value)}[/{color}]"


def _new_table() -> Table:
    """Return a new `Table` with the plain, uncoloured layout shared by
    every command: a rounded box with a header row, and no colour/bold
    styling on headers or cells."""

    return Table(box=box.ROUNDED, show_header=True)


def _highlight(text: str, regex: re.Pattern[str] | None) -> str:
    """Return *text* as Rich markup, with every *regex* match wrapped in
    `_HIGHLIGHT_COLOR` bold. Literal text is escaped first so any ``[``
    it contains is not misread as markup. When *regex* is `None`, the
    escaped text is returned unchanged."""

    escaped = escape(text)
    if regex is None:
        return escaped

    return regex.sub(lambda m: f"[bold {_HIGHLIGHT_COLOR}]{escape(m.group(0))}[/bold {_HIGHLIGHT_COLOR}]", escaped)


def print_rule_table(results: list[Rule], *, highlight_pattern: str | None = None) -> None:
    """Render a list of `Rule` objects as a Rich table and print it.

    Parameters
    ----------
    results:
        The list of `Rule` objects to display.
    highlight_pattern:
        When given, a regular expression (case-insensitive); every rule's
        id is coloured, and every match of the pattern within the
        `Section`, `Category`, or `Name` columns is highlighted. Intended
        for `search`/`match` results, where the caller already knows what
        pattern produced the hits.
    """

    assert isinstance(results, list), type(results)

    regex = re.compile(highlight_pattern, re.IGNORECASE) if highlight_pattern is not None else None

    table = _new_table()
    table.add_column("Id")
    table.add_column("Type")
    table.add_column("Section")
    table.add_column("Category")
    table.add_column("Name")

    for rule in results:
        id_cell = f"[bold {_ID_COLOR}]{escape(rule.id_)}[/bold {_ID_COLOR}]" if regex else rule.id_
        table.add_row(
            id_cell,
            _type_cell(rule.type_),
            _highlight(rule.section, regex),
            _highlight(rule.category, regex),
            _highlight(rule.name, regex),
        )

    console = Console()
    console.print(table)


def print_rule_detail(rule: Rule) -> None:
    """Render a single `Rule` object with its full contents.

    Parameters
    ----------
    rule:
        The `Rule` object to display.
    """

    assert isinstance(rule, Rule), type(rule)

    console = Console()
    console.print(f"{rule.id_} ({_type_cell(rule.type_)})")
    console.print(f"Ref: {rule.ref}")
    console.print(f"Section: {rule.section}")
    console.print(f"Category: {rule.category}")
    console.print(f"Name: {rule.name}")
    console.print(f"Summary: {rule.summary}")
    for content in rule.contents:
        console.print(f"({content.type_.value}) {content.data}")


def print_overview_table(results: list[RuleOverview]) -> None:
    """Render a list of `RuleOverview` objects as a Rich table and print it.

    Parameters
    ----------
    results:
        The list of `RuleOverview` objects to display.
    """

    assert isinstance(results, list), type(results)

    include_summary = any(item.summary is not None for item in results)

    table = _new_table()
    table.add_column("Id")
    table.add_column("Type")
    table.add_column("Section")
    table.add_column("Category")
    table.add_column("Name")
    table.add_column("Examples", justify="right")
    table.add_column("Notes", justify="right")
    table.add_column("Text", justify="right")
    if include_summary:
        table.add_column("Summary")

    for item in results:
        row = [
            item.id_,
            _type_cell(item.type_),
            item.section,
            item.category,
            item.name,
            str(item.example_count),
            str(item.note_count),
            str(item.text_count),
        ]
        if include_summary:
            row.append(item.summary or "")
        table.add_row(*row)

    console = Console()
    console.print(table)


def print_toc_table(
    results: list[tuple[str, str, list[str]]],
    *,
    id_types: dict[str, EntryType] | None = None,
) -> None:
    """Render a list of (section, category, ids) triples as a Rich table
    and print it.

    Parameters
    ----------
    results:
        The list of ``(section, category, ids)`` tuples to display; ``ids``
        is rendered as a single space-separated column.
    id_types:
        Optional ``id -> EntryType`` mapping; when given, each id is
        coloured per `_TYPE_COLOR`, the same scheme used for the ``Type``
        column in every other table (rule/recommendation/information).
        Ids not found in the mapping are left uncoloured.
    """

    assert isinstance(results, list), type(results)

    table = _new_table()
    table.add_column("Section")
    table.add_column("Category")
    table.add_column("Ids")

    def id_cell(id_: str) -> str:
        type_ = id_types.get(id_) if id_types is not None else None
        color = _TYPE_COLOR.get(type_) if type_ is not None else None
        return f"[{color}]{escape(id_)}[/{color}]" if color is not None else escape(id_)

    for section, category, ids in results:
        table.add_row(section, category, " ".join(id_cell(id_) for id_ in ids))

    console = Console()
    console.print(table)


def print_content_table(results: list[ContentItem]) -> None:
    """Render a list of `ContentItem` objects as a Rich table and print it.

    Parameters
    ----------
    results:
        The list of `ContentItem` objects to display.
    """

    assert isinstance(results, list), type(results)

    table = _new_table()
    table.add_column("Rule")
    table.add_column("Type")
    table.add_column("Data")

    for content in results:
        table.add_row(content.rule_id or "", content.type_.value, content.data)

    console = Console()
    console.print(table)
