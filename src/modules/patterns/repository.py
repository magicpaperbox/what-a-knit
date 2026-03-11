from dataclasses import dataclass
from typing import Optional
from infra.db import get_db
from modules.patterns.domain import Pattern, PatternId, PatternCategory


@dataclass
class PatternRow:
    id: int
    name: str
    category: str
    tool: str
    gauge: str
    subcategory: Optional[str]
    tool_size: Optional[list[str]]
    yarn_type: Optional[str]
    skeins_needed: Optional[int]
    pattern_language: Optional[str]
    designer: Optional[str]
    difficulty: Optional[int]


class PatternRepository:
    def _row_to_domain(self, row: PatternRow) -> Pattern:
        return Pattern(
            id=PatternId(row.id),
            name=row.name,
            category=PatternCategory(row.category),
            tool=row.tool,
            gauge=row.gauge,
            subcategory=row.subcategory,
            tool_size=row.tool_size,
            yarn_type=row.yarn_type,
            skeins_needed=row.skeins_needed,
            pattern_language=row.pattern_language,
            designer=row.designer,
            difficulty=row.difficulty
        )

    def get_all(self) -> list[Pattern]:
        db = get_db()
        cursor = db.execute('SELECT * FROM pattern')
        rows = cursor.fetchall()
        
        patterns = []
        for row in rows:
            pattern_row = PatternRow(**dict(row))
            patterns.append(self._row_to_domain(pattern_row))
        return patterns

    def get_by_id(self, pattern_id: PatternId) -> Optional[Pattern]:
        db = get_db()
        cursor = db.execute('SELECT * FROM pattern WHERE id = ?', (pattern_id.value,))
        row = cursor.fetchone()

        if row is None:
            return None
        
        pattern_row = PatternRow(**dict(row))
        return self._row_to_domain(pattern_row)

    def add(self, pattern: Pattern) -> Pattern:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO pattern (
                name, category, tool, gauge, subcategory, tool_size, yarn_type, 
                skeins_needed, pattern_language, designer, 
                difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                pattern.name, pattern.category.value, pattern.tool, pattern.gauge, pattern.subcategory,
                pattern.tool_size, pattern.yarn_type, pattern.skeins_needed,
                pattern.pattern_language, pattern.designer, pattern.difficulty
            )
        )
        db.commit()
        pattern.id = PatternId(cursor.lastrowid)
        return pattern

    def update(self, pattern: Pattern) -> None:
        db = get_db()
        db.execute(
            '''UPDATE pattern SET 
                name = ?, category = ?, tool = ?, gauge = ?, subcategory = ?, tool_size = ?, 
                yarn_type = ?, skeins_needed = ?, pattern_language = ?, 
                designer = ?, difficulty = ?
            WHERE id = ?''',
            (
                pattern.name, pattern.category.value, pattern.tool, pattern.gauge, pattern.subcategory,
                pattern.tool_size, pattern.yarn_type, pattern.skeins_needed,
                pattern.pattern_language, pattern.designer, pattern.difficulty, pattern.id.value
            )
        )
        db.commit()

    def delete(self, pattern_id: PatternId) -> None:
        db = get_db()
        db.execute('DELETE FROM pattern WHERE id = ?', (pattern_id.value,))
        db.commit()
