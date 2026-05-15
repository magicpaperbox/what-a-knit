from dataclasses import dataclass


@dataclass(frozen=True)
class Mass:
    grams: int

    def __post_init__(self):
        if self.grams is None:
            raise ValueError("Mass value cannot be None")

    def __str__(self):
        return f"{self.grams} g"

    def __add__(self, other: "Mass"):
        if not isinstance(other, Mass):
            return NotImplemented
        return Mass(self.grams + other.grams)

    def __radd__(self, other: int):
        if other == 0:
            return self
        return NotImplemented

    def __mul__(self, other: int | float):
        if not isinstance(other, int | float):
            return NotImplemented
        return Mass(int(self.grams * other))
