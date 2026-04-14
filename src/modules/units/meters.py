from dataclasses import dataclass


@dataclass(frozen=True)
class Meters:
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError("Meters value cannot be None")

    def __str__(self):
        return f"{self.value:g} m"