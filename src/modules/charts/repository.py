import json
from collections.abc import Callable
from dataclasses import dataclass

from infra.db import get_db
from modules.charts.domain import Chart, ChartId, ChartKind, ColorChart, SymbolChart, Color, Symbol


@dataclass
class ChartRow:
    id: int
    kind: str
    name: str
    cell_size: int
    cells_json: str

def _convert_cells[A, B](raw_rows: list[list[A]], create: Callable[[A], B]) -> list[list[B]]:
    mapped_rows = []
    for raw_row in raw_rows:
        mapped_row = [
            create(raw_cell) if raw_cell is not None else None
            for raw_cell in raw_row
        ]
        mapped_rows.append(mapped_row)
    return mapped_rows

class ChartRepository:
    def _row_to_domain(self, row: ChartRow) -> Chart:
        kind = ChartKind.from_string(row.kind)
        id = ChartId(row.id)
        raw_cell_rows = json.loads(row.cells_json)
        if kind == ChartKind.COLOR_CHART:
            return ColorChart(
                id=id,
                name=row.name,
                cell_size=row.cell_size,
                cells=_convert_cells(raw_cell_rows, Color.from_string),
            )
        if kind == ChartKind.SYMBOL_CHART:
            return SymbolChart(
                id=id,
                name=row.name,
                cell_size=row.cell_size,
                cells=_convert_cells(raw_cell_rows, Symbol.from_string),
            )
        raise ValueError(f"Unsupported kind: {kind}")

    def _domain_to_row(self, chart: Chart) -> ChartRow:
        string_cells = _convert_cells(chart.cells, lambda cell: cell.to_string())
        return ChartRow(
            id=chart.id.value if chart.id else None,
            kind=chart.kind.to_string(),
            name=chart.name,
            cell_size=chart.cell_size,
            cells_json=json.dumps(string_cells)
        )


    def get_all(self) -> list[Chart]:
        db = get_db()
        cursor = db.execute(
            """
            SELECT * FROM chart
            """
        )
        return [self._row_to_domain(ChartRow(**dict(row))) for row in cursor.fetchall()]

    def get_by_id(self, chart_id: ChartId) -> Chart | None:
        db = get_db()
        cursor = db.execute("SELECT * FROM chart WHERE id = ?", (chart_id.value,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_domain(ChartRow(**dict(row)))

    def add(self, chart: Chart) -> Chart:
        row = self._domain_to_row(chart)
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO chart (kind, name, cell_size, cells_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                row.kind,
                row.name,
                row.cell_size,
                row.cells_json,
            ),
        )
        db.commit()
        chart.id = ChartId(cursor.lastrowid)
        return self.get_by_id(chart.id)

    def update(self, chart: Chart) -> Chart:
        row = self._domain_to_row(chart)
        db = get_db()
        db.execute(
            """
            UPDATE chart
            SET kind = ?, name = ?, cell_size = ?, cells_json = ?
            WHERE id = ?
            """,
            (
                row.kind,
                row.name,
                row.cell_size,
                row.cells_json,
                row.id,
            ),
        )
        db.commit()
        return self.get_by_id(chart.id)


    def delete(self, chart_id: int) -> None:
        db = get_db()
        db.execute('DELETE FROM chart WHERE id = ?', (chart_id,))
        db.commit()