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

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116

import unittest

from src.biz.dfch.asdste100rules.commands.args import ExampleKind
from src.biz.dfch.asdste100rules.models import ContentType


class TestExampleKind(unittest.TestCase):
    def test_only_the_example_content_types_are_allowed(self):
        self.assertEqual(
            {"example", "ste_example", "nonste_example", "not_recommended"},
            {kind.value for kind in ExampleKind},
        )

    def test_excludes_non_example_content_types(self):
        excluded = {
            ContentType.TEXT,
            ContentType.HEADING,
            ContentType.NOTE,
            ContentType.COMMENT,
            ContentType.UNKNOWN,
            ContentType.TECHNICAL_NOUNS,
            ContentType.TECHNICAL_VERBS,
        }
        allowed = {a.value for a in ExampleKind}
        for kind in excluded:
            self.assertNotIn(kind.value, allowed)

    def test_values_match_corresponding_content_type_values(self):
        for kind in ExampleKind:
            self.assertEqual(kind.value, ContentType(kind.value).value)


if __name__ == "__main__":
    unittest.main()
