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

"""ContentType enumeration."""

from enum import StrEnum


class ContentType(StrEnum):
    """ASD-STE100 Issue 9 rule content block types (the ``contents[].type_`` field)."""

    UNKNOWN = "unknown"
    TEXT = "text"
    HEADING = "heading"
    NOTE = "note"
    COMMENT = "comment"
    EXAMPLE = "example"
    STE_EXAMPLE = "ste_example"
    NONSTE_EXAMPLE = "nonste_example"
    NOT_RECOMMENDED = "not_recommended"
    TECHNICAL_NOUNS = "technical_nouns"
    TECHNICAL_VERBS = "technical_verbs"
