from collections import defaultdict
from dataclasses import dataclass
from typing import Optional
from infra.db import get_db
from modules.units.mass import Mass
from modules.units.meters import Meters
from modules.yarn.domain import (
    Yarn, YarnId, YarnFiber, FiberType,
    YarnWeightCategory,
)


@dataclass
class YarnRow:
    id: int
    brand: str
    name: str
    color_shade: str
    weight_category: str
    full_weight_grams: int
    full_length_meters: float
    notes: str | None


@dataclass
class YarnFiberRow:
    id: int
    yarn_id: int
    fiber_type: str
    percentage: int


class YarnRepository:
    def _row_to_domain(self, row: YarnRow, fiber_rows: list[YarnFiberRow]) -> Yarn:
        composition = [
            YarnFiber(fiber_type=FiberType[fr.fiber_type], percentage=fr.percentage)
            for fr in fiber_rows
        ]
        return Yarn(
            id=YarnId(row.id),
            brand=row.brand,
            name=row.name,
            color_shade=row.color_shade,
            weight_category=YarnWeightCategory[row.weight_category],
            full_weight=Mass(row.full_weight_grams),
            full_length=Meters(row.full_length_meters),
            notes=row.notes,
            composition=composition,
        )

    def _get_fibers(self, yarn_id: int) -> list[YarnFiberRow]:
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM yarn_fiber WHERE yarn_id = ?', (yarn_id,)
        )
        return [YarnFiberRow(**dict(row)) for row in cursor.fetchall()]

    def _get_fibers_batch(self, yarn_ids: set[int]) -> dict[int, list[YarnFiberRow]]:
        if not yarn_ids:
            return defaultdict(list)
        db = get_db()
        placeholders = ','.join('?' for _ in yarn_ids)
        cursor = db.execute(
            f'SELECT * FROM yarn_fiber WHERE yarn_id IN ({placeholders})', tuple(yarn_ids),
        )
        result = defaultdict(list)
        for raw_row in cursor.fetchall():
            row = YarnFiberRow(**dict(raw_row))
            result[row.yarn_id].append(row)
        return result

    def _save_fibers(self, yarn_id: int, composition: list[YarnFiber]) -> None:
        db = get_db()
        db.execute('DELETE FROM yarn_fiber WHERE yarn_id = ?', (yarn_id,))
        for fiber in composition:
            db.execute(
                'INSERT INTO yarn_fiber (yarn_id, fiber_type, percentage) VALUES (?, ?, ?)',
                (yarn_id, fiber.fiber_type.name, fiber.percentage),
            )

    def get_all(self) -> list[Yarn]:
        db = get_db()
        cursor = db.execute('SELECT * FROM yarn')
        yarn_rows = [YarnRow(**dict(row)) for row in cursor.fetchall()]

        yarn_ids = {row.id for row in yarn_rows}
        fiber_rows_by_id = self._get_fibers_batch(yarn_ids)

        yarns = []
        for yarn_row in yarn_rows:
            fiber_rows = fiber_rows_by_id[yarn_row.id]
            yarn = self._row_to_domain(yarn_row, fiber_rows)
            yarns.append(yarn)
        return yarns

    def get_by_id(self, yarn_id: YarnId) -> Optional[Yarn]:
        db = get_db()
        cursor = db.execute('SELECT * FROM yarn WHERE id = ?', (yarn_id.value,))
        row = cursor.fetchone()
        if row is None:
            return None
        yarn_row = YarnRow(**dict(row))
        fiber_rows = self._get_fibers(yarn_row.id)
        return self._row_to_domain(yarn_row, fiber_rows)

    def add(self, yarn: Yarn) -> Yarn:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO yarn (
                brand, name, color_shade, weight_category, full_weight_grams, full_length_meters, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                yarn.brand, yarn.name, yarn.color_shade,
                yarn.weight_category.name,
                yarn.full_weight.grams, yarn.full_length.value,
                yarn.notes,
            ),
        )
        db.commit()
        yarn.id = YarnId(cursor.lastrowid)
        self._save_fibers(yarn.id.value, yarn.composition)
        db.commit()
        return yarn

    def update(self, yarn: Yarn) -> None:
        db = get_db()
        db.execute(
            '''UPDATE yarn SET
                brand = ?, name = ?, color_shade = ?, weight_category = ?,
                full_weight_grams = ?, full_length_meters = ?, notes = ?
            WHERE id = ?''',
            (
                yarn.brand, yarn.name, yarn.color_shade,
                yarn.weight_category.name,
                yarn.full_weight.grams, yarn.full_length.value,
                yarn.notes,
                yarn.id.value,
            ),
        )
        self._save_fibers(yarn.id.value, yarn.composition)
        db.commit()

    def delete(self, yarn_id: YarnId) -> None:
        db = get_db()
        db.execute('DELETE FROM yarn_fiber WHERE yarn_id = ?', (yarn_id.value,))
        db.execute('DELETE FROM yarn WHERE id = ?', (yarn_id.value,))
        db.commit()
