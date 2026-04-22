from dataclasses import dataclass


ChartCell = str | None


@dataclass
class Chart:
    name: str
    rows: int
    columns: int
    cell_size: int
    cells: list[list[ChartCell]]
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
