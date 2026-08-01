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

"""ContentItem model."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .content_type import ContentType


class ContentItem(BaseModel):
    """
    Represents a single block within a `Rule`'s ``contents`` list, e.g. a
    paragraph of explanatory text, a note, or an STE/non-STE example.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    type_: ContentType
    data: str
    rule_id: str | None = None
