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

"""
Shared ``Annotated`` parameter definitions for CLI sub-commands.
"""

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

from ..models import ContentType, EntryType


class ExampleKind(StrEnum):
    """The subset of `ContentType` values that count as an "example" for
    the ``examples`` command. Types such as ``text``, ``heading``,
    ``note``, ``comment`` and ``unknown`` are prose/annotations, not
    examples, and are deliberately excluded from ``--kind``.
    """

    EXAMPLE = ContentType.EXAMPLE.value
    STE_EXAMPLE = ContentType.STE_EXAMPLE.value
    NONSTE_EXAMPLE = ContentType.NONSTE_EXAMPLE.value
    NOT_RECOMMENDED = ContentType.NOT_RECOMMENDED.value


IdArg = Annotated[
    str,
    typer.Argument(
        help="The exact rule/recommendation id to search for, e.g. 'R1.1' or 'GR-8'.",
    ),
]

PatternArg = Annotated[
    str,
    typer.Argument(
        help="The regular expression pattern to search for in the rule name and summary.",
    ),
]

SearchPatternArg = Annotated[
    str,
    typer.Argument(
        help=(
            "The regular expression pattern to search for (case-insensitive), across"
            " the rule name, summary, and every content block (text, notes,"
            " examples, technical noun/verb lists, ...)."
        ),
    ),
]

SectionArg = Annotated[
    str,
    typer.Argument(
        help="The exact section name to search for, e.g. 'Words'.",
    ),
]

CategoryArg = Annotated[
    str,
    typer.Argument(
        help="The exact category name to search for, e.g. 'Technical nouns'.",
    ),
]

IdOpt = Annotated[
    str | None,
    typer.Option(
        "--id",
        "--rule-id",
        help="Only consider the rule with this exact id.",
    ),
]

SectionOpt = Annotated[
    str | None,
    typer.Option(
        "--section",
        help="Only consider rules in this exact section.",
    ),
]

CategoryOpt = Annotated[
    str | None,
    typer.Option(
        "--category",
        help="Only consider rules in this exact category.",
    ),
]

KindOpt = Annotated[
    ExampleKind | None,
    typer.Option(
        "--kind",
        "-k",
        help="Only return example content items of this type, e.g. 'ste_example'.",
    ),
]

ContentTypeOpt = Annotated[
    list[ContentType] | None,
    typer.Option(
        "--content-type",
        "-c",
        help=(
            "Only search the content of this type, e.g. 'note' or 'ste_example'."
            " Repeat for multiple types. The rule name/summary are always searched"
            " regardless of this option."
        ),
    ),
]

TypeOpt = Annotated[
    EntryType | None,
    typer.Option(
        "--type",
        "-t",
        help="Only consider entries of this exact type, e.g. 'rule' (excludes recommendations and information blocks).",
    ),
]

BriefOpt = Annotated[
    bool,
    typer.Option(
        "--brief/--full",
        help="--brief (default) omits the summary; --full includes it.",
    ),
]

UseBuiltinOpt = Annotated[
    bool,
    typer.Option(
        "--builtin/--no-builtin",
        help="Include (--builtin) or exclude (--no-builtin) the built-in ASD-STE100 Issue 9 ruleset.",
    ),
]

RulesFiles = Annotated[
    list[Path] | None,
    typer.Option(
        "--file",
        "-f",
        envvar="RULES_FILE",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help=(
            "Path to an additional JSON rules file (a single JSON array)."
            " Repeat for multiple files,"
            " e.g. ``--file a.jsonl --file b.jsonl``."
        ),
    ),
]
