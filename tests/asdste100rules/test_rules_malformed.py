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


class TestRulesMalformed(unittest.TestCase):
    def test_malformed_entry_is_skipped_not_raised(self):
        """A single malformed entry must not prevent the rest of the file
        from loading; it is skipped and reported via `print`."""

        rules_file = RulesFile.MALFORMED
        fullname = Path(__file__).parent / rules_file

        sut = Rules(files=[fullname], use_builtin=False)

        self.assertEqual(1, len(sut))
        self.assertEqual("X9.1", sut[0].id_)


if __name__ == "__main__":
    unittest.main()
