from dataclasses import dataclass
from enum import Enum
from typing import Union

from modules.units.centimeters import Centimeters

class ToolCategory(Enum):
    SHORT_CROCHET_HOOK = "short crochet hook"
    STRAIGHT_TUNISIAN_CROCHET_HOOK = "straight tunisian crochet hook"
    FIXED_CIRCULAR_TUNISIAN_CROCHET_HOOK = "fixed circular tunisian crochet hook"
    STRAIGHT_NEEDLES = "straight needles"
    FIXED_CIRCULAR_NEEDLES = "fixed circular needles"
    INTERCHANGEABLE_CIRCULAR_NEEDLE_TIPS = "interchangeable circular needle tips"
    DOUBLE_POINTED_NEEDLES = "double pointed needles"
    CABLE = "cable"


class ToolMaterial(Enum):
    WOOD = "wood"
    METAL = "metal"
    PLASTIC = "plastic"
    BAMBOO = "bamboo"
    NYLON_WIRE = "nylon wire"


@dataclass(frozen=True)
class ToolId:
    value: int

class Tool:
    id: ToolId | None

# Crochet hooks
@dataclass(frozen=True)
class ShortCrochetHook(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    material: ToolMaterial

@dataclass(frozen=True)
class StraightTunisianCrochetHook(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    material: ToolMaterial

@dataclass(frozen=True)
class FixedCircularTunisianCrochetHook(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    material: ToolMaterial

# Needles
@dataclass(frozen=True)
class StraightNeedles(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    length: Centimeters
    material: ToolMaterial

@dataclass(frozen=True)
class FixedCircularNeedles(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    length: Centimeters
    material: ToolMaterial

@dataclass(frozen=True)
class InterchangeableCircularNeedleTips(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    material: ToolMaterial

@dataclass(frozen=True)
class DoublePointedNeedles(Tool):
    id: ToolId | None
    category: ToolCategory
    size_mm: float
    material: ToolMaterial

# Needles accessories
@dataclass(frozen=True)
class Cable(Tool):
    id: ToolId | None
    category: ToolCategory
    length: Centimeters
    material: ToolMaterial

ToolType = Union[
    ShortCrochetHook,
    StraightTunisianCrochetHook,
    FixedCircularTunisianCrochetHook,
    StraightNeedles,
    FixedCircularNeedles,
    InterchangeableCircularNeedleTips,
    DoublePointedNeedles,
    Cable,
]