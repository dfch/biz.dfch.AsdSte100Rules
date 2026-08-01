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

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as metadata_version


@dataclass
class Info:
    """Program information."""

    name = "biz.dfch.AsdSte100Rules"
    try:
        version = metadata_version("biz-dfch-asdste100rules")
    except PackageNotFoundError:
        version = "unknown"
    description = f"{name}, v{version}. The ASD-STE100 (Simplified Technical English) Issue 9 rules."
    epilog = (
        "Copyright 2025-2026 Ronald Rink, d-fens GmbH, "
        "https://github.com/dfch/biz.dfch.AsdSte100Rules"
        ". "
        "Licensed under AGPLv3."
        "\n\n\n\n"
        "ASD-STE100 Simplified Technical English "
        "(Standard for Technical Documentation), Issue 9"
        "\n\n"
        "Copyright 2025 Aerospace, Security and Defence "
        "Industries Association of Europe (ASD)"
        ", "
        "https://www.asd-europe.org"
        "."
    )
