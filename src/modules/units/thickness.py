from dataclasses import dataclass


@dataclass(frozen=True)
class Thickness:
    millimeters: float

    def __post_init__(self):
        if self.millimeters is None:
            raise ValueError("Thickness value cannot be None")

    def __str__(self):
        return f"{self.millimeters:g} mm"