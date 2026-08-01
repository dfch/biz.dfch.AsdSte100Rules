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

"""Rules class."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Callable, Iterator

from pydantic import ValidationError

from .builtin_rules import BuiltInRules
from .models import ContentItem, ContentType, EntryType, Rule, RuleOverview

# The `ContentType` values that count as an "example" for
# `Rules.overview`'s `example_count`; prose/annotation types such as
# `text`, `heading`, `note`, `comment`, `unknown`, `technical_nouns` and
# `technical_verbs` are not counted here (the latter two get their own
# `has_technical_nouns`/`has_technical_verbs` flags instead).
_EXAMPLE_CONTENT_TYPES = frozenset(
    {
        ContentType.EXAMPLE,
        ContentType.STE_EXAMPLE,
        ContentType.NONSTE_EXAMPLE,
        ContentType.NOT_RECOMMENDED,
    }
)


class Rules:  # pylint: disable=R0904
    """Queryable collection of ASD-STE100 Issue 9 rules, recommendations, and information blocks."""

    _files: list[Path]
    _items: list[Rule]
    _predicate: Callable[[Rule], bool]

    def __init__(
        self,
        *,
        files: list[Path] | None = None,
        use_builtin: bool = True,
        predicate: Callable[[Rule], bool] | None = None,
    ) -> None:
        """Instantiates a ruleset object."""

        if files is None:
            files = []
        assert isinstance(files, list), type(files)
        assert isinstance(use_builtin, bool), type(use_builtin)
        if predicate is not None:
            assert callable(predicate), type(predicate)
            self._predicate = predicate
        else:
            self._predicate = lambda _: True

        self._items = []
        self._files = []

        if use_builtin:
            self._files.append(BuiltInRules.STE100_RULES.value)

        self._files.extend(files)
        for file in self._files:
            assert isinstance(file, Path), type(file)
            if not file.exists():
                raise FileNotFoundError(file)

            rules = Rules.read_json_file(
                file,
                predicate=self._predicate,
            )
            self._items.extend(rules)

        self.sort(key=self._default_sort_key)

    @staticmethod
    def read_json_text(
        value: str,
    ) -> list[Rule]:
        """
        Read `Rule` entries from a JSON array string.

        Each element is validated individually so that a single malformed
        entry does not prevent the rest of the document from loading; any
        entry that fails validation is skipped and reported via ``print``.
        """

        assert isinstance(value, str), type(value)

        raw = json.loads(value)
        assert isinstance(raw, list), type(raw)

        result: list[Rule] = []
        for idx, item in enumerate(raw):
            try:
                rule = Rule.model_validate(item)
                result.append(Rules._with_rule_id(rule))
            except ValidationError as ex:  # pylint: disable=W0718
                print(f"[ERROR] entry #{idx}: '{ex}'.")

        return result

    @staticmethod
    def _with_rule_id(rule: Rule) -> Rule:
        """Return a copy of `rule` whose `contents` items carry a
        `ContentItem.rule_id` back-reference to `rule.id_`.

        The source data does not embed the rule id on each content item,
        so it is stamped on after validation. Both `Rule` and
        `ContentItem` are frozen, hence `model_copy(update=...)`.
        """

        contents = [content.model_copy(update={"rule_id": rule.id_}) for content in rule.contents]
        return rule.model_copy(update={"contents": contents})

    @staticmethod
    def read_json_file(
        fullname: Path,
        predicate: Callable[[Rule], bool] | None = None,
    ) -> list[Rule]:
        """Read `Rule` entries from a JSON file (a single JSON array)."""

        assert isinstance(fullname, Path), type(fullname)
        assert fullname.exists(), fullname
        if predicate is not None:
            assert callable(predicate), type(predicate)

        text = fullname.read_text(encoding="utf-8")
        result = Rules.read_json_text(text)

        if predicate is not None:
            result = [rule for rule in result if predicate(rule)]

        return result

    def __len__(self) -> int:
        """Return the number of items in the ruleset."""
        return len(self._items)

    def __iter__(self) -> Iterator[Rule]:
        """Return an iterator over items in the ruleset."""
        return iter(self._items)

    def __getitem__(self, index: int) -> Rule:
        """Return a `Rule` by its index."""
        return self._items[index]

    def __delitem__(self, index: int) -> None:
        """Remove a `Rule` item from the ruleset by its index."""
        del self._items[index]

    def append(self, rule: Rule) -> None:
        """Add a single `Rule` item to the ruleset."""

        assert isinstance(rule, Rule), type(rule)

        self._items.append(rule)

    def extend(self, rules: list[Rule]) -> None:
        """Add multiple `Rule` items to the ruleset."""

        assert isinstance(rules, list), type(rules)

        self._items.extend(rules)

    def remove(self, rule: Rule) -> None:
        """Remove a `Rule` item from the ruleset by object."""

        assert isinstance(rule, Rule), type(rule)

        self._items.remove(rule)

    def clear(self) -> Rules:
        """Remove all `Rule` items from the ruleset."""

        self._items.clear()
        return self

    def pop(self, index: int = -1) -> Rule:
        """Remove and return a `Rule` item from the ruleset by its index."""

        return self._items.pop(index)

    def find(self, id_: str) -> list[Rule]:
        """
        Search for rules in the ruleset by exact id.

        Parameters
        ----------
        id_:
            The rule/recommendation id to search for (e.g. ``"R1.1"`` or
            ``"GR-8"``), matched case-insensitively.

        Returns
        -------
        list[Rule]
            A list of matching `Rule` objects.
        """

        assert isinstance(id_, str), type(id_)

        search_term = id_.lower()
        return [item for item in self._items if search_term == item.id_.lower()]

    def by_section(self, section: str) -> list[Rule]:
        """
        Search for rules in the ruleset by exact section name (case-insensitive).

        Parameters
        ----------
        section:
            The section name to search for, e.g. ``"Words"``.

        Returns
        -------
        list[Rule]
            A list of matching `Rule` objects.
        """

        assert isinstance(section, str), type(section)

        search_term = section.lower()
        return [item for item in self._items if search_term == item.section.lower()]

    def by_category(self, category: str) -> list[Rule]:
        """
        Search for rules in the ruleset by exact category name (case-insensitive).

        Parameters
        ----------
        category:
            The category name to search for, e.g. ``"Technical nouns"``.

        Returns
        -------
        list[Rule]
            A list of matching `Rule` objects.
        """

        assert isinstance(category, str), type(category)

        search_term = category.lower()
        return [item for item in self._items if search_term == item.category.lower()]

    def match(self, pattern: str) -> list[Rule]:
        """
        Search for rules in the ruleset using a regular expression.

        The pattern is matched (case-insensitively) against both the
        ``name`` and the ``summary`` of each rule.

        Parameters
        ----------
        pattern:
            The regular expression pattern to search for.

        Returns
        -------
        list[Rule]
            A list of matching `Rule` objects.
        """

        assert isinstance(pattern, str), type(pattern)

        regex = re.compile(pattern, re.IGNORECASE)
        return [item for item in self._items if regex.search(item.name) or regex.search(item.summary)]

    def search(self, pattern: str, *, content_types: list[ContentType] | None = None) -> list[Rule]:
        """
        Full-text search for rules using a regular expression.

        Unlike `match`, which only looks at `name` and `summary`, this
        searches every text a rule carries: `section`, `category`, `name`,
        `summary`, and the `data` of every `ContentItem` in `contents` --
        i.e. explanatory text, notes, STE/non-STE examples, technical
        noun/verb lists, and so on. Useful for an LLM-driven writer/checker
        that needs to find "what rule governs passive voice" or "where
        does STE100 mention abbreviations", without knowing the
        section/category/id upfront.

        Parameters
        ----------
        pattern:
            The regular expression pattern to search for (case-insensitive).
        content_types:
            When given, only the `data` of `ContentItem` entries whose
            `type_` is in this list is searched (`section`, `category`,
            `name`, and `summary` are always searched regardless). Use
            this to narrow the search to, e.g., only `ContentType.NOTE`
            or `ContentType.STE_EXAMPLE` content.

        Returns
        -------
        list[Rule]
            A list of matching `Rule` objects, in document order.
        """

        assert isinstance(pattern, str), type(pattern)
        if content_types is not None:
            assert isinstance(content_types, list), type(content_types)

        regex = re.compile(pattern, re.IGNORECASE)
        allowed_types = set(content_types) if content_types is not None else None

        def matches(item: Rule) -> bool:
            if (
                regex.search(item.section)
                or regex.search(item.category)
                or regex.search(item.name)
                or regex.search(item.summary)
            ):
                return True
            for content in item.contents:
                if allowed_types is not None and content.type_ not in allowed_types:
                    continue
                if regex.search(content.data):
                    return True
            return False

        return [item for item in self._items if matches(item)]

    def filter(self, predicate: Callable[[Rule], bool]) -> list[Rule]:
        """
        Search for rules in the ruleset using a predicate function.

        Parameters
        ----------
        predicate:
            A function that takes a `Rule` and returns `True` if it should
            be included in the result.

        Returns
        -------
        list[Rule]
            A list of `Rule` objects for which the predicate returned `True`.
        """

        assert callable(predicate), type(predicate)

        return [item for item in self._items if predicate(item)]

    def sections(self) -> list[str]:
        """Return the distinct section names, in first-seen order."""

        seen: dict[str, None] = {}
        for item in self._items:
            seen.setdefault(item.section, None)
        return list(seen)

    def categories(self) -> list[str]:
        """Return the distinct category names, in first-seen order."""

        seen: dict[str, None] = {}
        for item in self._items:
            seen.setdefault(item.category, None)
        return list(seen)

    def toc(self, *, section: str | None = None) -> list[tuple[str, str, list[str]]]:
        """
        Return the distinct (section, category) pairs, in first-seen order.

        Gives a table-of-contents style outline of the ruleset's
        structure, without any per-rule detail; useful for a caller
        (e.g. an LLM driving an MCP server) that wants to see which
        sections and categories exist before drilling into `overview`,
        `by_section`, or `by_category` for a specific one.

        Parameters
        ----------
        section:
            When given, only consider rules in this exact section
            (case-insensitive).

        Returns
        -------
        list[tuple[str, str, list[str]]]
            One ``(section, category, ids)`` tuple per distinct pair, in
            first-seen document order, where ``ids`` lists the ids of
            every rule/recommendation/information item in that
            (section, category), in document order.
        """

        if section is not None:
            assert isinstance(section, str), type(section)

        rules = self._items
        if section is not None:
            rules = [rule for rule in rules if rule.section.lower() == section.lower()]

        ids_by_pair: dict[tuple[str, str], list[str]] = {}
        for item in rules:
            ids_by_pair.setdefault((item.section, item.category), []).append(item.id_)
        return [(section_, category, ids) for (section_, category), ids in ids_by_pair.items()]

    def examples(
        self,
        *,
        id_: str | None = None,
        section: str | None = None,
        category: str | None = None,
        kind: ContentType | None = None,
    ) -> list[ContentItem]:
        """
        Return content items across rules, optionally scoped and filtered.

        Parameters
        ----------
        id_:
            When given, only consider the rule with this exact id
            (case-insensitive).
        section:
            When given, only consider rules in this exact section
            (case-insensitive).
        category:
            When given, only consider rules in this exact category
            (case-insensitive).
        kind:
            When given, only return content items of this `ContentType`
            (e.g. `ContentType.STE_EXAMPLE`).

        Returns
        -------
        list[ContentItem]
            A list of matching `ContentItem` objects, in document order.
        """

        if id_ is not None:
            assert isinstance(id_, str), type(id_)
        if section is not None:
            assert isinstance(section, str), type(section)
        if category is not None:
            assert isinstance(category, str), type(category)
        if kind is not None:
            assert isinstance(kind, ContentType), type(kind)

        rules = self._items
        if id_ is not None:
            rules = [rule for rule in rules if rule.id_.lower() == id_.lower()]
        if section is not None:
            rules = [rule for rule in rules if rule.section.lower() == section.lower()]
        if category is not None:
            rules = [rule for rule in rules if rule.category.lower() == category.lower()]

        result: list[ContentItem] = []
        for rule in rules:
            for content in rule.contents:
                if kind is None or content.type_ == kind:
                    result.append(content)

        return result

    def overview(
        self,
        *,
        section: str | None = None,
        category: str | None = None,
        type_: EntryType | None = None,
        brief: bool = True,
    ) -> list[RuleOverview]:
        """
        Return a lightweight, per-rule overview of the ruleset.

        Intended for a caller (e.g. an LLM driving an MCP server) that
        needs a cheap, low-token summary of what rules exist before
        drilling into `find` or `examples` for a specific rule; each
        result carries only the rule's id, type, section, category,
        name, and (optionally) summary, plus counts/flags about its
        content items rather than the content items themselves.

        Parameters
        ----------
        section:
            When given, only consider rules in this exact section
            (case-insensitive).
        category:
            When given, only consider rules in this exact category
            (case-insensitive).
        type_:
            When given, only consider rules of this exact `EntryType`
            (e.g. `EntryType.RULE`, to exclude recommendations and
            informational blocks).
        brief:
            When `True` (default), omit `RuleOverview.summary` to keep
            the payload small. When `False`, include the full summary.

        Returns
        -------
        list[RuleOverview]
            One `RuleOverview` per matching `Rule`, in the ruleset's
            current order (natural id order by default).
        """

        if section is not None:
            assert isinstance(section, str), type(section)
        if category is not None:
            assert isinstance(category, str), type(category)
        if type_ is not None:
            assert isinstance(type_, EntryType), type(type_)
        assert isinstance(brief, bool), type(brief)

        rules = self._items
        if section is not None:
            rules = [rule for rule in rules if rule.section.lower() == section.lower()]
        if category is not None:
            rules = [rule for rule in rules if rule.category.lower() == category.lower()]
        if type_ is not None:
            rules = [rule for rule in rules if rule.type_ == type_]

        result: list[RuleOverview] = []
        for rule in rules:
            example_count = sum(1 for content in rule.contents if content.type_ in _EXAMPLE_CONTENT_TYPES)
            note_count = sum(1 for content in rule.contents if content.type_ == ContentType.NOTE)
            text_count = sum(1 for content in rule.contents if content.type_ == ContentType.TEXT)
            has_technical_nouns = any(content.type_ == ContentType.TECHNICAL_NOUNS for content in rule.contents)
            has_technical_verbs = any(content.type_ == ContentType.TECHNICAL_VERBS for content in rule.contents)

            result.append(
                RuleOverview(
                    id_=rule.id_,
                    type_=rule.type_,
                    section=rule.section,
                    category=rule.category,
                    name=rule.name,
                    summary=None if brief else rule.summary,
                    example_count=example_count,
                    note_count=note_count,
                    text_count=text_count,
                    has_technical_nouns=has_technical_nouns,
                    has_technical_verbs=has_technical_verbs,
                )
            )

        return result

    @staticmethod
    def _natural_sort_key(value: str) -> tuple:
        """
        Split `value` into digit/non-digit chunks for natural sort order,
        e.g. so that ``"R1.10"`` sorts after ``"R1.9"`` instead of before it.

        Each chunk is tagged with a type discriminator so chunks of
        different types never get compared directly (which would raise
        ``TypeError``).
        """

        chunks = [chunk for chunk in re.split(r"(\d+)", value) if chunk != ""]
        return tuple((0, int(chunk)) if chunk.isdigit() else (1, chunk.lower()) for chunk in chunks)

    @staticmethod
    def _default_sort_key(rule: Rule) -> tuple:
        """Default sort key is natural order of the rule id_."""

        return Rules._natural_sort_key(rule.id_)

    def sort(self, *, key: Callable[[Rule], Any] | None = None, reverse: bool = False) -> None:
        """
        Sort the `Rule` items in the ruleset.

        If you do not define `key`, then the result of the sort is by
        natural order of the rule id.
        """

        if key is None:
            key = Rules._default_sort_key
        assert callable(key), type(key)
        assert isinstance(reverse, bool)

        self._items.sort(key=key, reverse=reverse)

    def as_dict(self) -> list[dict]:
        """
        Serialise the ruleset to a list of dictionaries.

        Each element in the returned list is a plain :class:`dict`
        representing one `Rule`, with all enum values resolved to their
        string representations. The result is suitable for use with
        third-party libraries that expect plain mappings (e.g. pandas,
        rich, REST serialisers).

        Returns
        -------
        list[dict]
            One dict per `Rule`.
        """

        return [rule.model_dump(mode="json") for rule in self._items]

    def write_json_text(self) -> str:
        """
        Serialise the ruleset to a single pretty-printed JSON array string.

        Returns
        -------
        str
            A JSON-encoded string representing the whole ruleset.
        """

        return json.dumps(self.as_dict(), indent=4, ensure_ascii=False)

    def write_json_file(
        self,
        path: Path,
        *,
        overwrite: bool = False,
        encoding: str = "utf-8",
        create_parents: bool = False,
    ) -> int:
        """
        Write the ruleset to a JSON file (a single JSON array).

        Parameters
        ----------
        path:
            Destination file path.
        overwrite:
            When ``False`` (default) raise ``FileExistsError`` if *path*
            already exists.
        encoding:
            File encoding (default ``"utf-8"``).
        create_parents:
            When ``True`` create any missing parent directories.

        Returns
        -------
        int
            Number of rules written.
        """

        assert isinstance(path, Path), type(path)
        assert isinstance(overwrite, bool), type(overwrite)
        assert isinstance(encoding, str), type(encoding)
        assert isinstance(create_parents, bool), type(create_parents)

        if path.exists() and not overwrite:
            raise FileExistsError(path)

        if create_parents:
            path.parent.mkdir(parents=True, exist_ok=True)

        text = self.write_json_text()
        with open(path, "w", encoding=encoding) as f:
            f.write(text)

        return len(self._items)
