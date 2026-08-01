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

"""``match`` find rules matching a regular expression pattern."""

from pathlib import Path

import typer

from ..models import Rule
from ..rules import Rules
from .args import (
    PatternArg,
    RulesFiles,
    UseBuiltinOpt,
)
from .render import print_rule_table


def match(
    pattern: PatternArg,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    Find rules matching a regular expression pattern.

    Searches the built-in ASD-STE100 Issue 9 ruleset and any additional
    JSON rules files supplied via ``--file`` for entries whose name or
    summary match *pattern* (case-insensitive regex substring search).
    """

    assert isinstance(pattern, str) and pattern.strip(), pattern

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    results: list[Rule] = rules.match(pattern)

    if not results:
        typer.echo(f"No matching rules found for '{pattern}'.")
        raise typer.Exit(code=0)

    print_rule_table(results)
