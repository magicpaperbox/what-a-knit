from dataclasses import dataclass


@dataclass(frozen=True)
class Thickness:
    millimeters: float
