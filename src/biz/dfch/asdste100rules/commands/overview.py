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

"""``overview`` give a lightweight summary of the rules in the ruleset."""

from pathlib import Path

import typer

from ..models import RuleOverview
from ..rules import Rules
from .args import (
    BriefOpt,
    CategoryOpt,
    RulesFiles,
    SectionOpt,
    TypeOpt,
    UseBuiltinOpt,
)
from .render import print_overview_table


def overview(  # pylint: disable=R0913,R0917
    section: SectionOpt = None,
    category: CategoryOpt = None,
    type_: TypeOpt = None,
    brief: BriefOpt = True,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    Give a lightweight overview of the rules in the ruleset.

    Lists every rule/recommendation/information entry with its id,
    type, section, category, name, and content stats (example, note,
    and text counts), optionally scoped to an exact section, category,
    or entry type. By default (``--brief``) the summary text is
    omitted to keep the output short; use ``--full`` to include it.
    """

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    results: list[RuleOverview] = rules.overview(
        section=section,
        category=category,
        type_=type_,
        brief=brief,
    )

    if not results:
        typer.echo("No rules found for the given filters.")
        raise typer.Exit(code=0)

    print_overview_table(results)
