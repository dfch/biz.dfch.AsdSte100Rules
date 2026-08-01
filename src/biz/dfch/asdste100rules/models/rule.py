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

"""Rule model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .content_item import ContentItem
from .entry_type import EntryType


class Rule(BaseModel):
    """
    Represents a single entry of the ASD-STE100 Issue 9 rules: a rule, a
    recommendation, or an informational (section-intro) block.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    type_: EntryType
    id_: str
    ref: str
    section: str
    category: str
    name: str
    summary: str
    contents: list[ContentItem] = Field(default_factory=list)
