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


class TestRulesByCategory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file
        cls.sut = Rules(files=[fullname], use_builtin=False)

    def test_by_category_with_one_result(self):
        result = self.sut.by_category("Test Category C")
        self.assertEqual(1, len(result))
        self.assertEqual("GX-1", result[0].id_)

    def test_by_category_is_case_insensitive(self):
        result = self.sut.by_category("test category b")
        self.assertEqual(1, len(result))
        self.assertEqual("X1.2", result[0].id_)

    def test_by_category_with_zero_results(self):
        result = self.sut.by_category("does-not-exist")
        self.assertEqual(0, len(result))


class TestRulesByCategoryBuiltin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sut = Rules()

    def test_categories_returns_distinct_values(self):
        result = self.sut.categories()
        self.assertEqual(len(result), len(set(result)))
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()
