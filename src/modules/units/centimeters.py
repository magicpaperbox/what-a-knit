from dataclasses import dataclass


@dataclass(frozen=True)
class Centimeters:
    value: float

    def __post_init__(self):
        if self.value is None:
            raise ValueError("Centimeters value cannot be None")

    def __str__(self):
        return f"{self.value:g} cm"