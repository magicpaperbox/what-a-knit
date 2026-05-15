from dataclasses import dataclass


@dataclass(frozen=True)
class Meters:
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError("Meters value cannot be None")

    def __str__(self):
        return f"{self.value:g} m"

    def __add__(self, other: "Meters"):
        if not isinstance(other, Meters):
            return NotImplemented
        return Meters(self.value + other.value)

    def __radd__(self, other: int):
        if other == 0:
            return self
        return NotImplemented

    def __mul__(self, other: int | float):
        if not isinstance(other, int | float):
            return NotImplemented
        return Meters(self.value * other)
