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

"""``category`` find rules by exact category name."""

from pathlib import Path

import typer

from ..models import Rule
from ..rules import Rules
from .args import (
    CategoryArg,
    RulesFiles,
    UseBuiltinOpt,
)
from .render import print_rule_table


def category(
    category_: CategoryArg,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    Find rules by exact category name.

    Searches the built-in ASD-STE100 Issue 9 ruleset and any additional
    JSON rules files supplied via ``--file`` for entries whose category
    exactly matches *category_* (case-insensitive).
    """

    assert isinstance(category_, str) and category_.strip(), category_

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    results: list[Rule] = rules.by_category(category_)

    if not results:
        typer.echo(f"No rules found for category '{category_}'.")
        raise typer.Exit(code=0)

    print_rule_table(results)
