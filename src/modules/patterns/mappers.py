from __future__ import annotations

from dataclasses import dataclass

from modules.patterns.domain import Pattern, PatternCategory, Gauge, PatternDifficultyLevel, PatternId


@dataclass
class PatternFormData:
    name: str = ""
    description: str = ""
    category: str = ""
    subcategory: str = ""
    gauge_stitches: str = ""
    gauge_rows: str = ""
    has_pattern: str = ""
    pattern_language: str = ""
    author: str = ""
    difficulty_level: str = ""

    @classmethod
    def empty(cls) -> PatternFormData:
        return PatternFormData()

    @classmethod
    def from_domain(cls, pattern: Pattern) -> PatternFormData:
        return PatternFormData(
            name=pattern.name,
            description=pattern.description,
            category=pattern.category.name,
            subcategory=pattern.subcategory or "",
            gauge_stitches="" if pattern.target_gauge is None or pattern.target_gauge.stitches is None else str(pattern.target_gauge.stitches),
            gauge_rows="" if pattern.target_gauge is None or pattern.target_gauge.rows is None else str(pattern.target_gauge.rows),
            has_pattern="yes" if (pattern.pattern_language or pattern.author or pattern.difficulty_level) else "no",
            pattern_language=pattern.pattern_language or "",
            author=pattern.author or "",
            difficulty_level="" if pattern.difficulty_level is None else pattern.difficulty_level.value,
        )

    @classmethod
    def from_request_form(cls, form) -> PatternFormData:
        return PatternFormData(
            name=form.get("name", ""),
            description=form.get("description", ""),
            category=form.get("category", ""),
            subcategory=form.get("subcategory", ""),
            gauge_stitches=form.get("gauge_stitches", ""),
            gauge_rows=form.get("gauge_rows", ""),
            has_pattern=form.get("has_pattern", ""),
            pattern_language=form.get("pattern_language", ""),
            author=form.get("author", ""),
            difficulty_level=form.get("difficulty_level", ""),
        )

    def to_domain(self, pattern_id: PatternId | None = None) -> Pattern:
        stitches = self.normalize_gauge_value(self.gauge_stitches)
        rows = self.normalize_gauge_value(self.gauge_rows)
        if stitches is not None or rows is not None:
            target_gauge = Gauge(stitches=stitches, rows=rows)
        else:
            target_gauge = None

        if self.has_pattern == "no":
            pattern_language = None
            author = None
            difficulty_level = None
        else:
            pattern_language = self.pattern_language or None
            author = self.author or None
            difficulty_level = PatternDifficultyLevel(self.difficulty_level) if self.difficulty_level else None

        return Pattern(
            id=pattern_id,
            name=self.name,
            description=self.description,
            target_gauge=target_gauge,
            category=PatternCategory[self.category],
            subcategory=self.subcategory or None,
            pattern_language=pattern_language,
            author=author,
            difficulty_level=difficulty_level,
        )

    @staticmethod
    def normalize_gauge_value(raw: str) -> float | None:
        if raw == "":
            return None

        value = float(raw)
        if value <= 0:
            return None

        return value
