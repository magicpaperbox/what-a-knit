from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from modules.units.centimeters import Centimeters
from modules.units.thickness import Thickness


class ToolKind(Enum):
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
    kind: ClassVar[ToolKind]
    id: ToolId | None

# Crochet hooks
@dataclass(frozen=True)
class ShortCrochetHook(Tool):
    kind: ClassVar[ToolKind] = ToolKind.SHORT_CROCHET_HOOK

    id: ToolId | None
    size: Thickness
    material: ToolMaterial

@dataclass(frozen=True)
class StraightTunisianCrochetHook(Tool):
    kind: ClassVar[ToolKind] = ToolKind.STRAIGHT_TUNISIAN_CROCHET_HOOK

    id: ToolId | None
    size: Thickness
    material: ToolMaterial

@dataclass(frozen=True)
class FixedCircularTunisianCrochetHook(Tool):
    kind: ClassVar[ToolKind] = ToolKind.FIXED_CIRCULAR_TUNISIAN_CROCHET_HOOK

    id: ToolId | None
    size: Thickness
    material: ToolMaterial

# Needles
@dataclass(frozen=True)
class StraightNeedles(Tool):
    kind: ClassVar[ToolKind] = ToolKind.STRAIGHT_NEEDLES

    id: ToolId | None
    size: Thickness
    length: Centimeters
    material: ToolMaterial

@dataclass(frozen=True)
class FixedCircularNeedles(Tool):
    kind: ClassVar[ToolKind] = ToolKind.FIXED_CIRCULAR_NEEDLES

    id: ToolId | None
    size: Thickness
    length: Centimeters
    material: ToolMaterial

@dataclass(frozen=True)
class InterchangeableCircularNeedleTips(Tool):
    kind: ClassVar[ToolKind] = ToolKind.INTERCHANGEABLE_CIRCULAR_NEEDLE_TIPS

    id: ToolId | None
    size: Thickness
    material: ToolMaterial

@dataclass(frozen=True)
class DoublePointedNeedles(Tool):
    kind: ClassVar[ToolKind] = ToolKind.DOUBLE_POINTED_NEEDLES

    id: ToolId | None
    size: Thickness
    material: ToolMaterial

# Needles accessories
@dataclass(frozen=True)
class Cable(Tool):
    kind: ClassVar[ToolKind] = ToolKind.CABLE

    id: ToolId | None
    length: Centimeters
    material: ToolMaterial

TOOL_CLASSES: list[type[Tool]] = [
    ShortCrochetHook,
    StraightTunisianCrochetHook,
    FixedCircularTunisianCrochetHook,
    StraightNeedles,
    FixedCircularNeedles,
    InterchangeableCircularNeedleTips,
    DoublePointedNeedles,
    Cable,
]

TOOL_CLASS_BY_KIND: dict[ToolKind, type[Tool]] = {
    tool_class.kind: tool_class
    for tool_class in TOOL_CLASSES
}

