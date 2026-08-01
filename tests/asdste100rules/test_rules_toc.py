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


class TestRulesToc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fullname1 = Path(__file__).parent / RulesFile.ONE_ITEM
        fullname2 = Path(__file__).parent / RulesFile.TWO_ITEMS
        cls.sut = Rules(files=[fullname1, fullname2], use_builtin=False)

    def test_toc_unfiltered_returns_distinct_pairs_in_document_order(self):
        result = self.sut.toc()
        # GX-1 (Test Section B / Test Category C), X1.1 (Test Section A /
        # Test Category A), X1.2 (Test Section A / Test Category B) --
        # natural sort id order is GX-1, X1.1, X1.2.
        self.assertEqual(
            [
                ("Test Section B", "Test Category C", ["GX-1"]),
                ("Test Section A", "Test Category A", ["X1.1"]),
                ("Test Section A", "Test Category B", ["X1.2"]),
            ],
            result,
        )

    def test_toc_filtered_by_section(self):
        result = self.sut.toc(section="Test Section A")
        self.assertEqual(
            [
                ("Test Section A", "Test Category A", ["X1.1"]),
                ("Test Section A", "Test Category B", ["X1.2"]),
            ],
            result,
        )

    def test_toc_no_match_returns_empty_list(self):
        result = self.sut.toc(section="does-not-exist")
        self.assertEqual([], result)

    def test_toc_is_case_insensitive(self):
        result = self.sut.toc(section="test section a")
        self.assertEqual(2, len(result))

    def test_toc_ids_list_the_items_in_each_pair(self):
        result = self.sut.toc()
        ids_by_pair = {(section, category): ids for section, category, ids in result}
        self.assertEqual(["GX-1"], ids_by_pair[("Test Section B", "Test Category C")])
        self.assertEqual(["X1.1"], ids_by_pair[("Test Section A", "Test Category A")])
        self.assertEqual(["X1.2"], ids_by_pair[("Test Section A", "Test Category B")])


class TestRulesTocBuiltin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sut = Rules()

    def test_toc_returns_a_pair_per_distinct_section_category_combination(self):
        result = self.sut.toc()
        self.assertGreater(len(result), 0)
        # Every rule's (section, category) must appear exactly once.
        pairs = [(section, category) for section, category, _ in result]
        self.assertEqual(len(pairs), len(set(pairs)))

    def test_toc_ids_cover_every_item_exactly_once(self):
        result = self.sut.toc()
        all_ids = [id_ for _, _, ids in result for id_ in ids]
        self.assertEqual(len(all_ids), len(set(all_ids)))
        self.assertEqual({rule.id_ for rule in self.sut}, set(all_ids))

    def test_toc_sections_match_the_sections_method(self):
        result = self.sut.toc()
        sections_in_toc = {section for section, _, _ in result}
        self.assertEqual(set(self.sut.sections()), sections_in_toc)

    def test_toc_filtered_by_section(self):
        result = self.sut.toc(section="Words")
        self.assertGreater(len(result), 0)
        for section, _, ids in result:
            self.assertEqual("Words", section)
            self.assertGreater(len(ids), 0)


if __name__ == "__main__":
    unittest.main()
