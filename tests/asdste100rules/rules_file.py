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

"""Test file definitions."""

from enum import StrEnum


class RulesFile(StrEnum):
    """Definitions for test rules fixture files."""

    NON_EXISTENT_FILE = "this-rules-file-does-not-exist.json"
    ONE_ITEM = "test_rules_list1.json"
    TWO_ITEMS = "test_rules_list2.json"
    NATURAL_SORT = "test_rules_natural_sort.json"
    MALFORMED = "test_rules_malformed.json"
