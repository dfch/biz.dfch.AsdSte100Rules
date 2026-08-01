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

"""RuleOverview model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .entry_type import EntryType


class RuleOverview(BaseModel):
    """
    A lightweight summary of a single `Rule`, intended to give a caller
    (e.g. an LLM driving an MCP server) a cheap overview of what rules
    exist without shipping every `Rule.contents` item.

    See `Rules.overview` for how instances of this model are produced.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id_: str
    type_: EntryType
    section: str
    category: str
    name: str
    summary: str | None = None
    example_count: int
    note_count: int
    text_count: int
    has_technical_nouns: bool
    has_technical_verbs: bool
