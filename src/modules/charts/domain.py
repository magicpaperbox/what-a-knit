from __future__ import annotations
import enum
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ChartId:
    value: int

class ChartKind(enum.StrEnum):
    COLOR_CHART = "color"
    SYMBOL_CHART = "symbol"

    @classmethod
    def from_string(cls, value: str) -> ChartKind:
        return cls(value)

    def to_string(self) -> str:
        return self.value

@dataclass()
class Chart[CellType]:
    id: ChartId | None
    name: str
    kind: ChartKind
    cell_size: int
    cells: list[list[CellType | None]]

    @property
    def rows(self) -> int:
        return len(self.cells)

    @property
    def columns(self) -> int:
        return len(self.cells[0]) if self.cells else 0

    def validate(self) -> None:
        if not self.cells:
            raise ValueError("Chart has no cells!")

        first_row_len = len(self.cells[0])

        if first_row_len == 0:
            raise ValueError("Empty row!")

        for cell_row in self.cells:
            if len(cell_row) != first_row_len:
                raise ValueError("Length of the row is not correct")


class Symbol(enum.StrEnum):
    PURL = "purl"
    SSK = "ssk"
    K2TOG = "k2tog"
    YARN_OVER = "yarn_over"
    FRONT_MARKER = "front_marker"
    NO_STITCH = "no_stitch"

    @classmethod
    def from_string(cls, value: str) -> Symbol:
        return Symbol(value)

    def to_string(self) -> str:
        return self.value

@dataclass(frozen=True)
class Color:
    hex_value: str

    @classmethod
    def from_string(cls, value: str) -> Color:
        pattern = "#[a-f0-9]{6}"
        if not re.fullmatch(pattern, value.lower()):
            raise ValueError

        return Color(value)

    def to_string(self) -> str:
        return self.hex_value
    #
    # def __lt__(self, other):
    #     return self.hex_value < other.hex_value

class ColorChart(Chart[Color]):
    def __init__(
        self,
        id: ChartId | None,
        name: str,
        cell_size: int,
        cells: list[list[Color | None]],
    ):
        super().__init__(id, name, ChartKind.COLOR_CHART, cell_size, cells)

    def all_colors(self):
        colors = set()
        for cell_row in self.cells:
            for cell in cell_row:
                if cell is not None:
                    colors.add(cell)
        colors = list(colors)
        colors.sort(key=lambda color: color.hex_value)
        return colors


class SymbolChart(Chart[Symbol]):
    def __init__(
        self,
        id: ChartId | None,
        name: str,
        cell_size: int,
        cells: list[list[Symbol | None]],
    ):
        super().__init__(id, name, ChartKind.SYMBOL_CHART, cell_size, cells)

