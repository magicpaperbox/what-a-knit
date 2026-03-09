from dataclasses import dataclass


@dataclass(frozen=True)
class Mass:
    grams: int

    def __str__(self):
        return f"{self.grams} g"
