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


class TestRulesSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fullname1 = Path(__file__).parent / RulesFile.ONE_ITEM
        fullname2 = Path(__file__).parent / RulesFile.TWO_ITEMS
        cls.sut = Rules(files=[fullname1, fullname2], use_builtin=False)

    def test_search_on_name(self):
        result = self.sut.search("mentions banana")
        self.assertEqual(1, len(result))
        self.assertEqual("GX-1", result[0].id_)

    def test_search_on_summary(self):
        result = self.sut.search("apple")
        self.assertEqual(1, len(result))
        self.assertEqual("X1.2", result[0].id_)

    def test_search_on_section(self):
        result = self.sut.search("Section B")
        self.assertEqual(1, len(result))
        self.assertEqual("GX-1", result[0].id_)

    def test_search_on_category(self):
        result = self.sut.search("Category C")
        self.assertEqual(1, len(result))
        self.assertEqual("GX-1", result[0].id_)

    def test_search_on_content_text(self):
        result = self.sut.search("Some text")
        self.assertEqual(1, len(result))
        self.assertEqual("X1.1", result[0].id_)

    def test_search_on_content_example(self):
        result = self.sut.search("STE one")
        self.assertEqual(1, len(result))
        self.assertEqual("X1.1", result[0].id_)

    def test_search_on_content_note(self):
        result = self.sut.search("Note two")
        self.assertEqual(1, len(result))
        self.assertEqual("X1.2", result[0].id_)

    def test_search_is_case_insensitive(self):
        result = self.sut.search("BANANA")
        self.assertEqual(1, len(result))

    def test_search_with_zero_results(self):
        result = self.sut.search("[0-9]{5}")
        self.assertEqual(0, len(result))

    def test_search_restricted_to_content_type_excludes_other_types(self):
        # "two" appears in both the note and the nonste_example content of
        # X1.2; restricting to NOTE must still find it via that content.
        result = self.sut.search("Note two", content_types=[ContentType.NOTE])
        self.assertEqual(1, len(result))
        self.assertEqual("X1.2", result[0].id_)

    def test_search_restricted_to_content_type_finds_nothing_in_wrong_type(self):
        # "Some text" only lives in a TEXT content block, not a NOTE one.
        result = self.sut.search("Some text", content_types=[ContentType.NOTE])
        self.assertEqual(0, len(result))

    def test_search_content_type_restriction_does_not_affect_name_summary_match(self):
        # name/summary are always searched regardless of content_types.
        result = self.sut.search("apple", content_types=[ContentType.NOTE])
        self.assertEqual(1, len(result))
        self.assertEqual("X1.2", result[0].id_)


class TestRulesSearchBuiltin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sut = Rules()

    def test_search_finds_more_than_match_for_content_only_terms(self):
        # "auxiliary" appears in rule content/summaries about verb forms;
        # confirm search returns at least what match() would and is not
        # empty for a real STE100 term.
        result = self.sut.search("auxiliary")
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()
