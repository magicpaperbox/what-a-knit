from dataclasses import dataclass

from modules.charts.domain import Chart, ChartId, ChartKind, SymbolChart, Symbol, ColorChart, Color
import json


@dataclass
class ChartFormData:
    name: str = ""
    rows: str = "12"
    columns: str = "12"
    cell_size: str = "32"
    cells_json: str = ""
    kind: str = "symbol"

    @classmethod
    def from_request_form(cls, form) -> "ChartFormData":
        return cls(
            name=form.get("name", "").strip(),
            rows=form.get("rows", "12").strip(),
            columns=form.get("columns", "12").strip(),
            cell_size=form.get("cell_size", "32").strip(),
            cells_json=form.get("cells_json", "").strip(),
            kind=form.get("kind", "").strip()
        )

    @classmethod
    def empty(cls) -> "ChartFormData":
        cells = [[None for _ in range(12)] for _ in range(12)]
        return cls(
            name="",
            rows="12",
            columns="12",
            cell_size="32",
            cells_json=json.dumps(cells),
            kind="symbol",
        )

    @classmethod
    def from_domain(cls, chart: Chart) -> "ChartFormData":
        string_cells = []
        for row in chart.cells:
            string_row = []
            for cell in row:
                if cell is not None:
                    string_row.append(cell.to_string())
                else:
                    string_row.append(None)
            string_cells.append(string_row)
        return cls(
            name=chart.name,
            rows=str(chart.rows),
            columns=str(chart.columns),
            cell_size=str(chart.cell_size),
            cells_json=json.dumps(string_cells),
            kind=chart.kind.to_string()
        )


    def to_domain(self, chart_id: ChartId | None = None) -> Chart:
        if not self.name:
            raise ValueError("Chart name is required.")

        cell_size = self._parse_int_field(self.cell_size, "Box size", 10, 80)

        try:
            raw_cells = json.loads(self.cells_json) if self.cells_json else []
        except json.JSONDecodeError:
            raise ValueError("Chart data is invalid.")

        if not isinstance(raw_cells, list):
            raise ValueError("Raw cells are not a list!")

        chart_kind = ChartKind.from_string(self.kind)
        if chart_kind == ChartKind.SYMBOL_CHART:
            mapped_rows = []
            for raw_row in raw_cells:
                if not isinstance(raw_row, list):
                    raise ValueError("raw_row is not a list!")
                mapped_row = [
                    Symbol.from_string(cell) if cell is not None else None
                    for cell in raw_row
                ]
                mapped_rows.append(mapped_row)
            return SymbolChart(
                id=chart_id,
                name=self.name,
                cell_size=cell_size,
                cells=mapped_rows,
            )
        elif chart_kind == ChartKind.COLOR_CHART:
            mapped_rows = []
            for raw_row in raw_cells:
                if not isinstance(raw_row, list):
                    raise ValueError("raw_row is not a list!")
                mapped_row = [
                    Color.from_string(cell) if cell is not None else None
                    for cell in raw_row
                ]
                mapped_rows.append(mapped_row)
            return ColorChart(
                id=chart_id,
                name=self.name,
                cell_size=cell_size,
                cells=mapped_rows,
            )
        else:
            raise ValueError("Unknown chart type!")


    def _parse_int_field(self, raw_value: str, label: str, min_value: int, max_value: int) -> int:
        try:
            parsed_value = int(raw_value)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must be a whole number.")

        if not min_value <= parsed_value <= max_value:
            raise ValueError(f"{label} must be between {min_value} and {max_value}.")

        return parsed_value

