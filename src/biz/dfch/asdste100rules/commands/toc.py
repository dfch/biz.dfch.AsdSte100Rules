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

"""``toc`` list the distinct section/category pairs in the ruleset."""

from pathlib import Path

import typer

from ..rules import Rules
from .args import (
    RulesFiles,
    SectionOpt,
    UseBuiltinOpt,
)
from .render import print_toc_table


def toc(
    section: SectionOpt = None,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    List the distinct section/category pairs in the ruleset.

    Gives a table-of-contents style outline of the ruleset's structure
    (Section | Category), without any per-rule detail, optionally
    scoped to an exact section.
    """

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    results: list[tuple[str, str, list[str]]] = rules.toc(section=section)

    if not results:
        typer.echo("No sections/categories found for the given filters.")
        raise typer.Exit(code=0)

    id_types = {rule.id_: rule.type_ for rule in rules}
    print_toc_table(results, id_types=id_types)
