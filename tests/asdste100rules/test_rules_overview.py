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

from src.biz.dfch.asdste100rules.models import EntryType
from src.biz.dfch.asdste100rules.rules import Rules

from .rules_file import RulesFile


class TestRulesOverview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fullname1 = Path(__file__).parent / RulesFile.ONE_ITEM
        fullname2 = Path(__file__).parent / RulesFile.TWO_ITEMS
        cls.sut = Rules(files=[fullname1, fullname2], use_builtin=False)

    def test_overview_unfiltered_returns_all_rules(self):
        result = self.sut.overview()
        self.assertEqual(3, len(result))
        self.assertEqual(["GX-1", "X1.1", "X1.2"], [item.id_ for item in result])

    def test_overview_is_brief_by_default(self):
        result = self.sut.overview()
        for item in result:
            self.assertIsNone(item.summary)

    def test_overview_full_includes_summary(self):
        result = self.sut.overview(brief=False)
        by_id = {item.id_: item for item in result}
        self.assertEqual("Summary one", by_id["X1.1"].summary)
        self.assertEqual("Summary two mentions apple", by_id["X1.2"].summary)
        self.assertEqual("Summary three", by_id["GX-1"].summary)

    def test_overview_example_count(self):
        result = self.sut.overview()
        by_id = {item.id_: item for item in result}
        # X1.1 contents: text + ste_example -> 1 example
        self.assertEqual(1, by_id["X1.1"].example_count)
        # X1.2 contents: note + nonste_example -> 1 example
        self.assertEqual(1, by_id["X1.2"].example_count)
        # GX-1 has no contents
        self.assertEqual(0, by_id["GX-1"].example_count)

    def test_overview_technical_noun_and_verb_flags_default_false(self):
        result = self.sut.overview()
        for item in result:
            self.assertFalse(item.has_technical_nouns)
            self.assertFalse(item.has_technical_verbs)

    def test_overview_note_and_text_counts(self):
        result = self.sut.overview()
        by_id = {item.id_: item for item in result}
        # X1.1 contents: text + ste_example -> 1 text, 0 notes
        self.assertEqual(1, by_id["X1.1"].text_count)
        self.assertEqual(0, by_id["X1.1"].note_count)
        # X1.2 contents: note + nonste_example -> 0 text, 1 note
        self.assertEqual(0, by_id["X1.2"].text_count)
        self.assertEqual(1, by_id["X1.2"].note_count)
        # GX-1 has no contents
        self.assertEqual(0, by_id["GX-1"].text_count)
        self.assertEqual(0, by_id["GX-1"].note_count)

    def test_overview_filtered_by_section(self):
        result = self.sut.overview(section="Test Section A")
        self.assertEqual({"X1.1", "X1.2"}, {item.id_ for item in result})

    def test_overview_filtered_by_category(self):
        result = self.sut.overview(category="Test Category B")
        self.assertEqual(["X1.2"], [item.id_ for item in result])

    def test_overview_filtered_by_type(self):
        result = self.sut.overview(type_=EntryType.RECOMMENDATION)
        self.assertEqual(["GX-1"], [item.id_ for item in result])

    def test_overview_no_match_returns_empty_list(self):
        result = self.sut.overview(section="does-not-exist")
        self.assertEqual(0, len(result))


class TestRulesOverviewBuiltin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sut = Rules()

    def test_overview_returns_all_66_builtin_rules(self):
        result = self.sut.overview()
        self.assertEqual(66, len(result))

    def test_overview_r1_5_has_technical_nouns_flag(self):
        result = self.sut.overview(section="Words", category="Technical nouns")
        self.assertGreater(len(result), 0)
        by_id = {item.id_: item for item in result}
        self.assertTrue(by_id["R1.5"].has_technical_nouns)

    def test_overview_filtered_by_type_rule_excludes_recommendations(self):
        result = self.sut.overview(type_=EntryType.RULE)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertEqual(EntryType.RULE, item.type_)

    def test_overview_filtered_by_type_recommendation(self):
        result = self.sut.overview(type_=EntryType.RECOMMENDATION)
        self.assertGreater(len(result), 0)
        for item in result:
            self.assertEqual(EntryType.RECOMMENDATION, item.type_)
            self.assertTrue(item.id_.startswith("GR-"))


if __name__ == "__main__":
    unittest.main()
