from dataclasses import dataclass
from enum import Enum, auto, StrEnum
from typing import Optional

from modules.units.centimeters import Centimeters
from modules.units.mass import Mass
from modules.units.meters import Meters
from modules.yarn.domain import YarnWeightCategory

class PatternDifficultyLevel(StrEnum):
    BEGINNER = auto()
    INTERMEDIATE = auto()
    ADVANCED = auto()
    EXPERT = auto()

class PatternCategory(Enum):
    SWEATER = "sweater"
    CARDIGAN = "cardigan"
    BLOUSE = "blouse"
    VEST = "vest"
    DRESS = "dress"
    SKIRT = "skirt"
    PANTS = "pants"
    SOCKS = "socks"
    GLOVES = "gloves"
    HAT = "hat"
    SCARF = "scarf"
    BAG = "bag"
    ACCESSORIES = "accessories"
    PLUSHIES = "plushies"


    def subcategories(self) -> list[str]:
        global _SUBCATEGORY_MAPPING
        return _SUBCATEGORY_MAPPING.get(self, [])

_SUBCATEGORY_MAPPING = {
    PatternCategory.SWEATER: ["raglan", "yoke", "set-in sleeve", "top-down", "bottom-up", "flat", "steek"],
    PatternCategory.CARDIGAN: ["raglan", "yoke", "set-in sleeve", "top-down", "bottom-up", "flat", "steek"],
    PatternCategory.VEST: ["raglan", "yoke", "top-down", "bottom-up", "flat", "slipover"],
    PatternCategory.BLOUSE: ["raglan", "yoke", "set-in sleeve", "top-down", "bottom-up", "flat", "long-sleeve", "short-sleeve"],
    PatternCategory.SOCKS: ["heel-flap", "short-row", "afterthought", "toe-up", "cuff-down", "leg-warmers"],
    PatternCategory.PANTS: ["flat", "in-round", "afterthought", "top-down", "bottom-up", "tights"],
    PatternCategory.SKIRT: ["mini", "midi", "maxi"],
    PatternCategory.DRESS: ["mini", "midi", "maxi"],
    PatternCategory.HAT: ["beanie", "beret", "balaclava", "bonnet"],
    PatternCategory.SCARF: ["shawl", "cowl", "triangular", "crescent", "hood", "collar"],
    PatternCategory.GLOVES: ["mittens", "classic", "fingerless"],
    PatternCategory.ACCESSORIES: ["pillow", "blanket", "rug", "towel", "washcloth", "pot-holder", "basket", "keychain", "case", "christmas", "decoratives"],
    PatternCategory.BAG: ["shopper", "shoulder-bag", "hand-bag", "backpack"],
    PatternCategory.PLUSHIES: ["animals", "food", "others"]
}

@dataclass(frozen=True)
class Gauge:
    stitches: float | None
    rows: float | None
    width: Centimeters = Centimeters(10.0)
    height: Centimeters = Centimeters(10.0)
    #TODO validate stitches or rows are provided

@dataclass(frozen=True)
class PatternId:
    value: int

@dataclass(frozen=True)
class PatternRequirements:
    possible_yarn_weights: list[YarnWeightCategory]
    allow_multicolor: bool = False
    total_weight: Optional[Mass] = None
    total_length: Optional[Meters] = None

@dataclass
class Pattern:
    id: Optional[PatternId]
    name: str
    description: str
    # requirements: PatternRequirements

    target_gauge: Optional[Gauge]

    category: PatternCategory
    subcategory: Optional[str]

    pattern_language: Optional[str]
    author: Optional[str]
    difficulty_level: Optional[PatternDifficultyLevel]
    # charts: list[Chart] = field(default_factory=list)
