from dataclasses import dataclass


ChartCell = str | None


@dataclass(frozen=True)
class ChartId:
    value: int

@dataclass
class Chart:
    name: str
    rows: int
    columns: int
    cell_size: int
    cells: list[list[ChartCell]]
    id: ChartId | None = None
    created_at: str | None = None
    updated_at: str | None = None
