from dataclasses import dataclass


@dataclass(frozen=True)
class Mass:
    grams: int

    def __post_init__(self):
        if self.grams is None:
            raise ValueError("Mass value cannot be None")

    def __str__(self):
        return f"{self.grams} g"
