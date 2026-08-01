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

import json
from pathlib import Path
import unittest

from src.biz.dfch.asdste100rules.models import Rule
from src.biz.dfch.asdste100rules.rules import Rules

from .rules_file import RulesFile


class TestRules(unittest.TestCase):
    def test_load_builtin(self):

        sut = Rules(use_builtin=True)
        self.assertIsNotNone(sut)
        self.assertGreater(len(sut), 0)

    def test_load_nothing(self):

        expected = 0

        sut = Rules(use_builtin=False)
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_default_params(self):
        """Initialize `Rules` with default parameters."""

        sut = Rules()
        self.assertIsNotNone(sut)
        self.assertGreater(len(sut), 0)

    def test_load_custom_rules_file(self):

        rules_file = RulesFile.ONE_ITEM
        fullname = Path(__file__).parent / rules_file

        expected = 1

        sut = Rules(files=[fullname], use_builtin=False)
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_non_existent_rules_file_throws(self):

        rules_file = RulesFile.NON_EXISTENT_FILE
        fullname = Path(__file__).parent / rules_file

        with self.assertRaises(FileNotFoundError) as ex:
            _ = Rules(files=[fullname])
        self.assertIsNotNone(ex)
        self.assertIsNotNone(ex.exception)
        self.assertTrue(rules_file in str(ex.exception), str(ex.exception))

    def test_load_multiple_rules_files(self):

        rules_file1 = RulesFile.ONE_ITEM
        fullname1 = Path(__file__).parent / rules_file1
        rules_file2 = RulesFile.TWO_ITEMS
        fullname2 = Path(__file__).parent / rules_file2

        expected = 3

        sut = Rules(files=[fullname1, fullname2], use_builtin=False)
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_with_predicate(self):

        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file

        def predicate(rule: Rule) -> bool:
            return rule.id_ == "GX-1"

        expected = 1

        sut = Rules(files=[fullname], use_builtin=False, predicate=predicate)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_load_all_filter_all(self):

        def predicate(_: Rule) -> bool:
            return False

        expected = 0

        sut = Rules(use_builtin=True, predicate=predicate)
        self.assertIsNotNone(sut)
        result = len(sut)

        self.assertEqual(expected, result)

    def test_iterate(self):

        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file

        expected = 2

        sut = Rules(files=[fullname], use_builtin=False)

        result = len(sut)
        self.assertEqual(expected, result)

        count = 0
        for _ in sut:
            count += 1

        self.assertEqual(expected, count)

    def test_index(self):

        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)

        item = sut[0]
        self.assertIsNotNone(item)

        with self.assertRaises(IndexError):
            _ = sut[42]

    def test_pop(self):

        rules_file = RulesFile.ONE_ITEM
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)

        item = sut.pop()
        self.assertIsNotNone(item)
        self.assertEqual("X1.1", item.id_)

        self.assertEqual(0, len(sut))

        with self.assertRaises(IndexError):
            _ = sut.pop()

    def test_del(self):

        rules_file = RulesFile.ONE_ITEM
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)
        self.assertEqual(1, len(sut))

        del sut[0]

        self.assertEqual(0, len(sut))

        with self.assertRaises(IndexError):
            del sut[42]

    def test_append_extend_remove(self):

        rules_file = RulesFile.ONE_ITEM
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)
        item = sut[0]

        sut.clear()
        self.assertEqual(0, len(sut))

        sut.append(item)
        self.assertEqual(1, len(sut))

        sut.extend([item, item])
        self.assertEqual(3, len(sut))

        sut.remove(item)
        self.assertEqual(2, len(sut))

    def test_append_throws(self):

        sut = Rules(use_builtin=False)

        with self.assertRaises(AssertionError):
            sut.append(None)  # type: ignore

    def test_sort_default_is_natural_order(self):

        rules_file = RulesFile.NATURAL_SORT
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)

        ids = [rule.id_ for rule in sut]
        self.assertEqual(["X1.2", "X1.9", "X1.10"], ids)

    def test_sort_reverse(self):

        rules_file = RulesFile.NATURAL_SORT
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)
        sut.sort(reverse=True)

        ids = [rule.id_ for rule in sut]
        self.assertEqual(["X1.10", "X1.9", "X1.2"], ids)

    def test_sort_custom_key(self):

        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)
        sut.sort(key=lambda rule: rule.type_.value)

        result = [rule.type_.value for rule in sut]
        self.assertEqual(sorted(result), result)

    def test_as_dict(self):

        rules_file = RulesFile.ONE_ITEM
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)
        result = sut.as_dict()

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], dict)
        self.assertEqual("X1.1", result[0]["id_"])
        self.assertEqual("rule", result[0]["type_"])

    def test_write_json_text_roundtrip(self):

        rules_file = RulesFile.TWO_ITEMS
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)
        text = sut.write_json_text()

        parsed = json.loads(text)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(sut), len(parsed))

        roundtrip = Rules.read_json_text(text)
        self.assertEqual(len(sut), len(roundtrip))
        for original, result in zip(sut, roundtrip):
            self.assertEqual(original, result)

    def test_write_json_file(self):

        rules_file = RulesFile.ONE_ITEM
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)

        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "out.json"
            written = sut.write_json_file(target)

            self.assertEqual(1, written)
            self.assertTrue(target.exists())

            with self.assertRaises(FileExistsError):
                sut.write_json_file(target)

            written_again = sut.write_json_file(target, overwrite=True)
            self.assertEqual(1, written_again)


if __name__ == "__main__":
    unittest.main()
