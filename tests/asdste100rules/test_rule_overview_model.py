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

from pydantic import ValidationError

from src.biz.dfch.asdste100rules.models import EntryType, RuleOverview


class TestRuleOverviewModel(unittest.TestCase):
    def test_construct_brief(self):
        sut = RuleOverview(
            id_="R1.1",
            type_=EntryType.RULE,
            section="Words",
            category="Which words can you use?",
            name="Use approved words",
            example_count=2,
            note_count=0,
            text_count=1,
            has_technical_nouns=False,
            has_technical_verbs=False,
        )

        self.assertEqual("R1.1", sut.id_)
        self.assertIsNone(sut.summary)
        self.assertEqual(2, sut.example_count)

    def test_construct_full(self):
        sut = RuleOverview(
            id_="R1.5",
            type_=EntryType.RULE,
            section="Words",
            category="Technical nouns",
            name="Technical nouns",
            summary="A technical noun is a noun term.",
            example_count=0,
            note_count=0,
            text_count=0,
            has_technical_nouns=True,
            has_technical_verbs=False,
        )

        self.assertEqual("A technical noun is a noun term.", sut.summary)
        self.assertTrue(sut.has_technical_nouns)

    def test_is_frozen(self):
        sut = RuleOverview(
            id_="R1.1",
            type_=EntryType.RULE,
            section="Words",
            category="Which words can you use?",
            name="Use approved words",
            example_count=0,
            note_count=0,
            text_count=0,
            has_technical_nouns=False,
            has_technical_verbs=False,
        )

        with self.assertRaises(ValidationError):
            sut.example_count = 5  # type: ignore

    def test_extra_field_raises(self):
        with self.assertRaises(ValidationError):
            RuleOverview.model_validate(
                {
                    "id_": "R1.1",
                    "type_": "rule",
                    "section": "Words",
                    "category": "Which words can you use?",
                    "name": "Use approved words",
                    "example_count": 0,
                    "note_count": 0,
                    "text_count": 0,
                    "has_technical_nouns": False,
                    "has_technical_verbs": False,
                    "unexpected": "field",
                }
            )

    def test_missing_required_field_raises(self):
        with self.assertRaises(ValidationError):
            RuleOverview.model_validate({"id_": "R1.1"})


if __name__ == "__main__":
    unittest.main()
