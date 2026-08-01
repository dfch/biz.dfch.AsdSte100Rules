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

from pathlib import Path
import unittest

from src.biz.dfch.asdste100rules.rules import Rules

from .rules_file import RulesFile


class TestRulesMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file
        cls.sut = Rules(files=[fullname], use_builtin=False)

    def test_match_on_name(self):
        result = self.sut.match("mentions banana")
        self.assertEqual(1, len(result))
        self.assertEqual("GX-1", result[0].id_)

    def test_match_on_summary(self):
        result = self.sut.match("apple")
        self.assertEqual(1, len(result))
        self.assertEqual("X1.2", result[0].id_)

    def test_match_is_case_insensitive(self):
        result = self.sut.match("BANANA")
        self.assertEqual(1, len(result))

    def test_match_with_zero_results(self):
        result = self.sut.match("[0-9]{5}")
        self.assertEqual(0, len(result))

    def test_filter(self):
        result = self.sut.filter(lambda rule: rule.id_.startswith("GX"))
        self.assertEqual(1, len(result))
        self.assertEqual("GX-1", result[0].id_)


if __name__ == "__main__":
    unittest.main()
