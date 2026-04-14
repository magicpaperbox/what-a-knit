from dataclasses import dataclass


@dataclass(frozen=True)
class Meters:
    value: float

    def __str__(self):
        return f"{self.value:g} m"