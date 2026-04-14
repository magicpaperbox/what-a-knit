from dataclasses import dataclass


@dataclass(frozen=True)
class Centimeters:
    value: float


    def __str__(self):
        return f"{self.value:g} cm"