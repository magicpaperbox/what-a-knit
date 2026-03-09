from dataclasses import dataclass
from typing import Optional
from infra.db import get_db
from modules.units.mass import Mass
from modules.yarn.domain import Skein, SkeinId, YarnId


@dataclass
class SkeinRow:
    id: int
    yarn_id: int
    current_weight_grams: int


class SkeinRepository:
    def _row_to_domain(self, row: SkeinRow) -> Skein:
        return Skein(
            id=SkeinId(row.id),
            yarn_id=YarnId(row.yarn_id),
            current_weight=Mass(row.current_weight_grams),
        )

    def get_all(self) -> list[Skein]:
        db = get_db()
        cursor = db.execute('SELECT * FROM skein')
        return [self._row_to_domain(SkeinRow(**dict(row))) for row in cursor.fetchall()]

    def get_by_id(self, skein_id: SkeinId) -> Optional[Skein]:
        db = get_db()
        cursor = db.execute('SELECT * FROM skein WHERE id = ?', (skein_id.value,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_domain(SkeinRow(**dict(row)))

    def get_by_yarn_id(self, yarn_id: YarnId) -> list[Skein]:
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM skein WHERE yarn_id = ?', (yarn_id.value,)
        )
        return [self._row_to_domain(SkeinRow(**dict(row))) for row in cursor.fetchall()]

    def add(self, skein: Skein) -> Skein:
        db = get_db()
        cursor = db.execute(
            'INSERT INTO skein (yarn_id, current_weight_grams) VALUES (?, ?)',
            (skein.yarn_id.value, skein.current_weight.grams),
        )
        db.commit()
        skein.id = SkeinId(cursor.lastrowid)
        return skein

    def update(self, skein: Skein) -> None:
        db = get_db()
        db.execute(
            'UPDATE skein SET current_weight_grams = ? WHERE id = ?',
            (skein.current_weight.grams, skein.id.value),
        )
        db.commit()

    def delete(self, skein_id: SkeinId) -> None:
        db = get_db()
        db.execute('DELETE FROM skein WHERE id = ?', (skein_id.value,))
        db.commit()
