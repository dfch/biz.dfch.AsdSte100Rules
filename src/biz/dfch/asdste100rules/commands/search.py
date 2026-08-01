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

"""``search`` find rules whose text (section, category, name, summary, or any content block) matches a pattern."""

from pathlib import Path

import typer

from ..models import Rule
from ..rules import Rules
from .args import (
    ContentTypeOpt,
    RulesFiles,
    SearchPatternArg,
    UseBuiltinOpt,
)
from .render import print_rule_table


def search(
    pattern: SearchPatternArg,
    content_type: ContentTypeOpt = None,
    use_builtin: UseBuiltinOpt = True,
    files: RulesFiles = None,
) -> None:
    """
    Find rules whose text matches a regular expression pattern.

    Unlike ``match``, which only looks at the rule name and summary, this
    searches every text a rule carries: section, category, name, summary,
    and the data of every content block (explanatory text, notes,
    STE/non-STE examples, technical noun/verb lists, ...). Use
    ``--content-type`` to narrow the content search to specific block
    types.
    """

    assert isinstance(pattern, str) and pattern.strip(), pattern

    extra_files: list[Path] = files if files is not None else []

    rules = Rules(
        use_builtin=use_builtin,
        files=extra_files,
    )

    results: list[Rule] = rules.search(pattern, content_types=content_type)

    if not results:
        typer.echo(f"No matching rules found for '{pattern}'.")
        raise typer.Exit(code=0)

    print_rule_table(results, highlight_pattern=pattern)
