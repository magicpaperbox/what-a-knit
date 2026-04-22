import json
from dataclasses import dataclass

from infra.db import get_db
from modules.charts.domain import Chart


@dataclass
class ChartRow:
    id: int
    name: str
    rows: int
    columns: int
    cell_size: int
    cells_json: str
    created_at: str
    updated_at: str


class ChartRepository:
    def _row_to_domain(self, row: ChartRow) -> Chart:
        return Chart(
            id=row.id,
            name=row.name,
            rows=row.rows,
            columns=row.columns,
            cell_size=row.cell_size,
            cells=json.loads(row.cells_json),
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def get_all(self) -> list[Chart]:
        db = get_db()
        cursor = db.execute(
            """
            SELECT * FROM chart
            ORDER BY updated_at DESC, id DESC
            """
        )
        return [self._row_to_domain(ChartRow(**dict(row))) for row in cursor.fetchall()]

    def get_by_id(self, chart_id: int) -> Chart | None:
        db = get_db()
        cursor = db.execute("SELECT * FROM chart WHERE id = ?", (chart_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_domain(ChartRow(**dict(row)))

    def add(self, chart: Chart) -> Chart:
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO chart (name, rows, columns, cell_size, cells_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                chart.name,
                chart.rows,
                chart.columns,
                chart.cell_size,
                json.dumps(chart.cells),
            ),
        )
        db.commit()
        chart.id = cursor.lastrowid
        return self.get_by_id(chart.id)

    def update(self, chart: Chart) -> Chart:
        db = get_db()
        db.execute(
            """
            UPDATE chart
            SET name = ?, rows = ?, columns = ?, cell_size = ?, cells_json = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                chart.name,
                chart.rows,
                chart.columns,
                chart.cell_size,
                json.dumps(chart.cells),
                chart.id,
            ),
        )
        db.commit()
        return self.get_by_id(chart.id)
