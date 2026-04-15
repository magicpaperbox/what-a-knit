from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from modules.units.mass import Mass
from modules.units.meters import Meters


class YarnWeightCategory(Enum):
    LACE = "Lace"
    FINGERING = "Fingering"
    SPORT = "Sport"
    DK = "DK"
    WORSTED = "Worsted"
    ARAN = "Aran"
    BULKY = "Bulky"

class FiberType(Enum):
    WOOL = "Wool"
    MERINO = "Merino"
    ALPACA = "Alpaca"
    MOHAIR = "Mohair"
    CASHMERE = "Cashmere"
    COTTON = "Cotton"
    LINEN = "Linen"
    SILK = "Silk"
    ACRYLIC = "Acrylic"
    POLYAMIDE = "Polyamide"
    POLYESTER = "Polyester"
    BAMBOO = "Bamboo"


@dataclass(frozen=True)
class YarnFiber:
    fiber_type: FiberType
    percentage: int


@dataclass(frozen=True)
class YarnId:
    value: int


@dataclass
class Yarn:
    id: Optional[YarnId]
    brand: str
    name: str
    color_shade: str
    weight_category: YarnWeightCategory
    full_weight: Mass
    full_length: Meters
    notes: Optional[str] = None
    composition: list[YarnFiber] = field(default_factory=list)

    def validate(self) -> None:
        if not self.composition:
            return
        total = sum(f.percentage for f in self.composition)
        if total > 100:
            raise ValueError(f"Composition percentages sum to {total}%, cannot exceed 100%.")


@dataclass(frozen=True)
class SkeinId:
    value: int


@dataclass
class Skein:
    id: Optional[SkeinId]
    yarn_id: YarnId
    current_weight: Mass

    def remaining_length(self, yarn: Yarn) -> Meters:
        if yarn.full_weight.grams == 0:
            return Meters(0)
        ratio = self.current_weight.grams / yarn.full_weight.grams
        return Meters(round(yarn.full_length.value * ratio, 1))

    def validate(self, yarn: Yarn) -> None:
        if self.current_weight.grams > yarn.full_weight.grams:
            raise ValueError(
                f"Skein weight exceeds yarn weight ({self.current_weight}) > ({yarn.full_weight})"
            )
