from __future__ import annotations
import enum
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ChartId:
    value: int

class ChartKind(enum.StrEnum):
    ColorChart = enum.auto()
    SymbolChart = enum.auto()

    @classmethod
    def from_string(cls, value: str) -> ChartKind:
        return cls(value)

    def to_string(self) -> str:
        return self.value


class Chart[CellType]:
    def __init__(
        self,
        id: ChartId | None,
        name: str,
        kind: ChartKind,
        cell_size: int,
        cells: list[list[CellType | None]],
    ):
        self.id = id
        self.name = name
        self.kind = kind
        self.cell_size = cell_size
        self.cells = cells

    @property
    def rows(self) -> int:
        return len(self.cells)

    @property
    def columns(self) -> int:
        return len(self.cells[0]) if self.cells else 0

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

@dataclass
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

class ColorChart(Chart[Color]):
    def __init__(
        self,
        id: ChartId | None,
        name: str,
        cell_size: int,
        cells: list[list[Color | None]],
    ):
        super().__init__(id, name, ChartKind.ColorChart, cell_size, cells)

class SymbolChart(Chart[Symbol]):
    def __init__(
        self,
        id: ChartId | None,
        name: str,
        cell_size: int,
        cells: list[list[Symbol | None]],
    ):
        super().__init__(id, name, ChartKind.SymbolChart, cell_size, cells)
