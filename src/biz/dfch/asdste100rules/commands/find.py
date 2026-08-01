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

"""``find`` find a rule or recommendation by exact id."""

from pathlib import Path

import typer

from ..models import Rule
from ..rules import Rules
from .args import (
    IdArg,
    RulesFiles,
    UseBuiltinOpt,
)
from .render import print_rule_detail


def find(
    id_: IdArg,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    Find a rule or recommendation by exact id.

    Searches the built-in ASD-STE100 Issue 9 ruleset and any additional
    JSON rules files supplied via ``--file`` for entries whose id
    exactly matches *id_* (case-insensitive).
    """

    assert isinstance(id_, str) and id_.strip(), id_

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    results: list[Rule] = rules.find(id_)

    if not results:
        typer.echo(f"No rule found for id '{id_}'.")
        raise typer.Exit(code=0)

    for rule in results:
        print_rule_detail(rule)
