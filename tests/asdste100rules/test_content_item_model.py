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

from src.biz.dfch.asdste100rules.models import ContentItem, ContentType


class TestContentItemModel(unittest.TestCase):
    def test_construct(self):
        sut = ContentItem(type_=ContentType.STE_EXAMPLE, data="**Test** it.")

        self.assertEqual(ContentType.STE_EXAMPLE, sut.type_)
        self.assertEqual("**Test** it.", sut.data)

    def test_construct_heading(self):
        sut = ContentItem(type_=ContentType.HEADING, data="# Examples:")

        self.assertEqual(ContentType.HEADING, sut.type_)
        self.assertEqual("# Examples:", sut.data)

    def test_construct_example(self):
        sut = ContentItem(type_=ContentType.EXAMPLE, data="Some example.")

        self.assertEqual(ContentType.EXAMPLE, sut.type_)
        self.assertEqual("example", sut.type_.value)

    def test_construct_technical_nouns(self):
        sut = ContentItem(type_=ContentType.TECHNICAL_NOUNS, data="engine, valve")

        self.assertEqual(ContentType.TECHNICAL_NOUNS, sut.type_)
        self.assertEqual("technical_nouns", sut.type_.value)

    def test_construct_technical_verbs(self):
        sut = ContentItem(type_=ContentType.TECHNICAL_VERBS, data="open, close")

        self.assertEqual(ContentType.TECHNICAL_VERBS, sut.type_)
        self.assertEqual("technical_verbs", sut.type_.value)

    def test_removed_general_and_good_content_types_no_longer_validate(self):
        with self.assertRaises(ValidationError):
            ContentItem.model_validate({"type_": "general_example", "data": "x"})
        with self.assertRaises(ValidationError):
            ContentItem.model_validate({"type_": "good_example", "data": "x"})

    def test_rule_id_defaults_to_none(self):
        sut = ContentItem(type_=ContentType.TEXT, data="hello")

        self.assertIsNone(sut.rule_id)

    def test_construct_with_rule_id(self):
        sut = ContentItem(type_=ContentType.STE_EXAMPLE, data="**Test** it.", rule_id="R1.1")

        self.assertEqual("R1.1", sut.rule_id)

    def test_is_frozen(self):
        sut = ContentItem(type_=ContentType.TEXT, data="hello")

        with self.assertRaises(ValidationError):
            sut.data = "changed"  # type: ignore

    def test_invalid_content_type_raises(self):
        with self.assertRaises(ValidationError):
            ContentItem.model_validate({"type_": "not-a-real-type", "data": "x"})

    def test_missing_data_raises(self):
        with self.assertRaises(ValidationError):
            ContentItem.model_validate({"type_": "text"})


if __name__ == "__main__":
    unittest.main()
