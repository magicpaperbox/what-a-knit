from flask import request

from modules.units.centimeters import Centimeters
from tools.domain import (
    StraightNeedles,
    ToolCategory,
    ToolId,
    ToolMaterial,
    ToolType,
    ShortCrochetHook,
)

def parse_tool_from_form(tool_id: ToolId | None = None) -> ToolType:
    category = ToolCategory[request.form["type"]]
    material = ToolMaterial[request.form["material"]]

    if category == ToolCategory.SHORT_CROCHET_HOOK:
        return ShortCrochetHook(
            id=tool_id,
            category=category,
            size_mm=request.form.get("size_mm", type=float),
            material=material,
        )
    elif category == ToolCategory.STRAIGHT_NEEDLES:
        return StraightNeedles(
            id=tool_id,
            category=category,
            size_mm=request.form.get("size_mm", type=float),
            length=Centimeters(request.form.get("length", type=float)),
            material=material,
        )
    raise ValueError(f"Unsupported tool category: {category}")