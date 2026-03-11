from dataclasses import dataclass
from enum import Enum
from typing import Optional

from modules.yarn.domain import YarnWeightCategory


class PatternCategory(Enum):
    SWEATER = "Sweater"
    CARDIGAN = "Cardigan"
    BLOUSE = "Blouse"
    VEST = "Vest"
    DRESS = "Dress"
    SKIRT = "Skirt"
    PANTS = "Pants"
    SOCKS = "Socks"
    GLOVES = "Gloves"
    HAT = "Hat"
    SCARF = "Scarf"
    BAG = "Bag"
    ACCESSORIES = "Accessories"
    PLUSHIES = "Plushies"

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
class PatternId:
    value: int

@dataclass
class Pattern:
    id: Optional[PatternId]
    name: str
    tool: str
    gauge: str
    category: PatternCategory
    subcategory: Optional[str]
    tool_size: Optional[list[str]]
    yarn_type: Optional[YarnWeightCategory]
    skeins_needed: Optional[int]
    pattern_language: Optional[str]
    designer: Optional[str]
    difficulty: Optional[int]
