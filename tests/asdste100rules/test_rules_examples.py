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

from src.biz.dfch.asdste100rules.models import ContentType
from src.biz.dfch.asdste100rules.rules import Rules

from .rules_file import RulesFile


class TestRulesExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fullname1 = Path(__file__).parent / RulesFile.ONE_ITEM
        fullname2 = Path(__file__).parent / RulesFile.TWO_ITEMS
        cls.sut = Rules(files=[fullname1, fullname2], use_builtin=False)

    def test_examples_unfiltered_returns_all_content_items(self):
        result = self.sut.examples()
        # X1.1: text + ste_example, X1.2: note + nonste_example, GX-1: none
        self.assertEqual(4, len(result))

    def test_examples_filtered_by_kind(self):
        result = self.sut.examples(kind=ContentType.STE_EXAMPLE)
        self.assertEqual(1, len(result))
        self.assertEqual("STE one", result[0].data)

    def test_examples_filtered_by_id(self):
        result = self.sut.examples(id_="X1.2")
        self.assertEqual(2, len(result))
        kinds = {content.type_ for content in result}
        self.assertEqual({ContentType.NOTE, ContentType.NONSTE_EXAMPLE}, kinds)

    def test_examples_carry_their_rule_id(self):
        result = self.sut.examples()
        rule_ids = {content.rule_id for content in result}
        self.assertEqual({"X1.1", "X1.2"}, rule_ids)
        for content in self.sut.examples(id_="X1.2"):
            self.assertEqual("X1.2", content.rule_id)

    def test_examples_filtered_by_section(self):
        result = self.sut.examples(section="Test Section A")
        # X1.1 and X1.2 are both in "Test Section A"
        self.assertEqual(4, len(result))

    def test_examples_filtered_by_category(self):
        result = self.sut.examples(category="Test Category C")
        self.assertEqual(0, len(result))

    def test_examples_no_match_returns_empty_list(self):
        result = self.sut.examples(id_="does-not-exist")
        self.assertEqual(0, len(result))


class TestRulesExamplesBuiltin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sut = Rules()

    def test_examples_for_r1_2_has_ste_examples(self):
        result = self.sut.examples(id_="R1.2", kind=ContentType.STE_EXAMPLE)
        self.assertGreater(len(result), 0)
        for content in result:
            self.assertEqual(ContentType.STE_EXAMPLE, content.type_)

    def test_examples_filtered_by_heading_start_with_hash(self):
        result = self.sut.examples(kind=ContentType.HEADING)
        self.assertGreater(len(result), 0)
        for content in result:
            self.assertEqual(ContentType.HEADING, content.type_)
            self.assertTrue(content.data.startswith("#"))

    def test_examples_filtered_by_example(self):
        result = self.sut.examples(kind=ContentType.EXAMPLE)
        self.assertGreater(len(result), 0)
        for content in result:
            self.assertEqual(ContentType.EXAMPLE, content.type_)

    def test_examples_filtered_by_technical_nouns(self):
        result = self.sut.examples(kind=ContentType.TECHNICAL_NOUNS)
        self.assertGreater(len(result), 0)
        for content in result:
            self.assertEqual(ContentType.TECHNICAL_NOUNS, content.type_)

    def test_examples_filtered_by_technical_verbs(self):
        result = self.sut.examples(kind=ContentType.TECHNICAL_VERBS)
        self.assertGreater(len(result), 0)
        for content in result:
            self.assertEqual(ContentType.TECHNICAL_VERBS, content.type_)


if __name__ == "__main__":
    unittest.main()
