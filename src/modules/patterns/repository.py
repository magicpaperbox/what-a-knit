from dataclasses import dataclass
from typing import Optional

from infra.db import get_db
from modules.patterns.domain import Pattern, PatternId, PatternCategory, Gauge, PatternDifficultyLevel
from modules.units.centimeters import Centimeters


@dataclass
class GaugeRow:
    id: int
    pattern_id: int
    stitches: float | None
    rows: float | None
    width_cm: float
    height_cm: float


@dataclass
class PatternRow:
    id: int
    name: str
    description: str
    category: str
    subcategory: Optional[str]
    pattern_language: Optional[str]
    author: Optional[str]
    difficulty_level: Optional[str]


class PatternRepository:
    def _row_to_domain(self, pattern_row: PatternRow, gauge_row: GaugeRow | None) -> Pattern:
        if gauge_row:
            gauge = Gauge(
                float(gauge_row.stitches) if gauge_row.stitches is not None else None,
                float(gauge_row.rows) if gauge_row.rows is not None else None,
                width=Centimeters(gauge_row.width_cm) if gauge_row.width_cm is not None else None,
                height=Centimeters(gauge_row.height_cm) if gauge_row.height_cm is not None else None
            )
        else:
            gauge = None
        return Pattern(
            id=PatternId(pattern_row.id),
            name=pattern_row.name,
            description=pattern_row.description,
            # requirements=PatternRequirements(row.requirements),
            target_gauge=gauge,
            category=PatternCategory[pattern_row.category],
            subcategory=pattern_row.subcategory,
            pattern_language=pattern_row.pattern_language,
            author=pattern_row.author,
            difficulty_level=PatternDifficultyLevel(pattern_row.difficulty_level) if pattern_row.difficulty_level is not None else None
        )

    def _get_gauge(self, pattern_id: int) -> GaugeRow | None:
        if not pattern_id:
            return None
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM pattern_gauge WHERE pattern_id = ?', (pattern_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return GaugeRow(**dict(row))


    def _get_gauge_batch(self, pattern_ids: set[int]) -> dict[int, GaugeRow]:
        if not pattern_ids:
            return {}
        db = get_db()
        placeholders = ','.join('?' for _ in pattern_ids)
        cursor = db.execute(
            f'SELECT * FROM pattern_gauge WHERE pattern_id IN ({placeholders})', tuple(pattern_ids),
        )
        result = {}
        for raw_row in cursor.fetchall():
            row = GaugeRow(**dict(raw_row))
            result[row.pattern_id] = row
        return result

    def get_all(self) -> list[Pattern]:
        db = get_db()
        cursor = db.execute('SELECT * FROM pattern')

        pattern_rows = [PatternRow(**dict(row)) for row in cursor.fetchall()]
        pattern_ids = {row.id for row in pattern_rows}
        gauge_rows_by_id = self._get_gauge_batch(pattern_ids)

        patterns = []
        for pattern_row in pattern_rows:
            gauge_row = gauge_rows_by_id.get(pattern_row.id)
            gauge = self._row_to_domain(pattern_row, gauge_row)
            patterns.append(gauge)
        return patterns

    def get_by_id(self, pattern_id: PatternId) -> Optional[Pattern]:
        db = get_db()
        cursor = db.execute('SELECT * FROM pattern WHERE id = ?', (pattern_id.value,))
        row = cursor.fetchone()

        if row is None:
            return None

        pattern_row = PatternRow(**dict(row))
        gauge_row = self._get_gauge(pattern_row.id)

        return self._row_to_domain(pattern_row, gauge_row)

    def _save_gauge(self, gauge: Gauge, pattern_id: int) -> None:
        db = get_db()
        db.execute(
            '''INSERT INTO pattern_gauge (pattern_id, stitches, rows, width_cm, height_cm) VALUES (?, ?, ?, ?, ?)''',
            (pattern_id, gauge.stitches, gauge.rows, gauge.width.value, gauge.height.value)
        )


    def add(self, pattern: Pattern) -> Pattern:
        if pattern.difficulty_level:
            difficulty = pattern.difficulty_level.value
        else:
            difficulty = None
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO pattern (
                name, description, category, subcategory, pattern_language, author, difficulty_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                pattern.name, pattern.description, pattern.category.name, pattern.subcategory,
                pattern.pattern_language, pattern.author, difficulty
            )
        )
        pattern.id = PatternId(cursor.lastrowid)
        if pattern.target_gauge:
            self._save_gauge(pattern.target_gauge, pattern.id.value)
        db.commit()
        return pattern

    def update(self, pattern: Pattern) -> None:
        if pattern.difficulty_level:
            difficulty = pattern.difficulty_level.value
        else:
            difficulty = None
        db = get_db()
        db.execute(
            '''UPDATE pattern SET 
                name = ?, description = ?, category = ?, subcategory = ?, pattern_language = ?, 
                author = ?, difficulty_level = ?
            WHERE id = ?''',
            (
                pattern.name, pattern.description, pattern.category.name, pattern.subcategory,
                pattern.pattern_language, pattern.author, difficulty, pattern.id.value
            )
        )
        db.execute('DELETE FROM pattern_gauge WHERE pattern_id = ?', (pattern.id.value,))
        if pattern.target_gauge:
            self._save_gauge(pattern.target_gauge, pattern.id.value)
        db.commit()

    def delete(self, pattern_id: PatternId) -> None:
        db = get_db()
        db.execute('DELETE FROM pattern_gauge WHERE pattern_id = ?', (pattern_id.value,))
        db.execute('DELETE FROM pattern WHERE id = ?', (pattern_id.value,))
        db.commit()


