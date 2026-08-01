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

"""``examples`` find content items (examples, notes, ...) across rules."""

from pathlib import Path

import typer

from ..models import ContentItem, ContentType
from ..rules import Rules
from .args import (
    CategoryOpt,
    ExampleKind,
    IdOpt,
    KindOpt,
    RulesFiles,
    SectionOpt,
    UseBuiltinOpt,
)
from .render import print_content_table

# The `ContentType` values that count as an "example" when `--kind` is
# not given; `text`, `heading`, `note`, `comment`, and `unknown` are
# prose/annotations, not examples, and are excluded by default.
_EXAMPLE_KINDS = frozenset(ExampleKind)


def examples(  # pylint: disable=R0913,R0917
    id_: IdOpt = None,
    section: SectionOpt = None,
    category: CategoryOpt = None,
    kind: KindOpt = None,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    Find example content items across rules.

    Searches the built-in ASD-STE100 Issue 9 ruleset and any additional
    JSON rules files supplied via ``--file`` for example content items,
    optionally scoped to an exact rule id (``--id``/``--rule-id``),
    section, or category, and optionally narrowed to one example kind
    (``--kind ste_example``).

    Only ``example``, ``ste_example`` and ``nonste_example``
    content items are considered examples; prose/annotation types such
    as ``text``, ``heading``, ``note``, ``comment`` and ``unknown`` are
    never returned by this command.
    """

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    if kind is not None:
        results: list[ContentItem] = rules.examples(
            id_=id_,
            section=section,
            category=category,
            kind=ContentType(kind.value),
        )
    else:
        results = [
            item for item in rules.examples(id_=id_, section=section, category=category) if item.type_ in _EXAMPLE_KINDS
        ]

    if not results:
        typer.echo("No content items found for the given filters.")
        raise typer.Exit(code=0)

    print_content_table(results)
