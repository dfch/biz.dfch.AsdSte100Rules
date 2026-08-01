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

from src.biz.dfch.asdste100rules.models import ContentItem, ContentType, EntryType, Rule


class TestRuleModel(unittest.TestCase):
    def test_construct_minimal_rule(self):
        sut = Rule(
            type_=EntryType.RULE,
            id_="R1.1",
            ref="ref",
            section="Words",
            category="cat",
            name="name",
            summary="summary",
        )

        self.assertEqual(EntryType.RULE, sut.type_)
        self.assertEqual("R1.1", sut.id_)
        self.assertEqual([], sut.contents)

    def test_construct_with_contents(self):
        sut = Rule(
            type_=EntryType.RULE,
            id_="R1.1",
            ref="ref",
            section="Words",
            category="cat",
            name="name",
            summary="summary",
            contents=[ContentItem(type_=ContentType.TEXT, data="hello")],
        )

        self.assertEqual(1, len(sut.contents))
        self.assertEqual(ContentType.TEXT, sut.contents[0].type_)

    def test_is_frozen(self):
        sut = Rule(
            type_=EntryType.RULE,
            id_="R1.1",
            ref="ref",
            section="Words",
            category="cat",
            name="name",
            summary="summary",
        )

        with self.assertRaises(ValidationError):
            sut.id_ = "R1.2"  # type: ignore

    def test_missing_required_field_raises(self):
        with self.assertRaises(ValidationError):
            Rule.model_validate(
                {
                    "type_": "rule",
                    "id_": "R1.1",
                    # missing ref, section, category, name, summary
                }
            )

    def test_unknown_field_raises(self):
        with self.assertRaises(ValidationError):
            Rule.model_validate(
                {
                    "type_": "rule",
                    "id_": "R1.1",
                    "ref": "ref",
                    "section": "Words",
                    "category": "cat",
                    "name": "name",
                    "summary": "summary",
                    "contents": [],
                    "unexpected_field": "boom",
                }
            )

    def test_invalid_entry_type_raises(self):
        with self.assertRaises(ValidationError):
            Rule.model_validate(
                {
                    "type_": "not-a-real-type",
                    "id_": "R1.1",
                    "ref": "ref",
                    "section": "Words",
                    "category": "cat",
                    "name": "name",
                    "summary": "summary",
                    "contents": [],
                }
            )

    def test_model_dump_roundtrip(self):
        sut = Rule(
            type_=EntryType.RECOMMENDATION,
            id_="GR-1",
            ref="ref",
            section="Writing Practices",
            category="General recommendations",
            name="name",
            summary="summary",
            contents=[ContentItem(type_=ContentType.NOTE, data="a note")],
        )

        dumped = sut.model_dump(mode="json")
        restored = Rule.model_validate(dumped)

        self.assertEqual(sut, restored)


if __name__ == "__main__":
    unittest.main()
