from dataclasses import fields

from flask import request

from modules.units.centimeters import Centimeters
from modules.units.thickness import Thickness
from tools.domain import (
    Cable,
    DoublePointedNeedles,
    FixedCircularNeedles,
    FixedCircularTunisianCrochetHook,
    InterchangeableCircularNeedleTips,
    ShortCrochetHook,
    StraightNeedles,
    StraightTunisianCrochetHook,
    Tool,
    ToolId,
    TOOL_CLASS_BY_KIND,
    ToolKind,
    ToolMaterial,
)


def _parse_size() -> Thickness:
    size = request.form.get("size", type=float)
    if size is None:
        raise ValueError("Size is required for this tool type")
    return Thickness(size)


def _parse_length() -> Centimeters:
    length = request.form.get("length", type=float)
    if length is None:
        raise ValueError("Length is required for this tool type")
    return Centimeters(length)


def _reject_size() -> None:
    if request.form.get("size"):
        raise ValueError("Size not supported for this tool type")


def _reject_length() -> None:
    if request.form.get("length"):
        raise ValueError("Length not supported for this tool type")


def parse_tool_from_form(tool_id: ToolId | None = None) -> Tool:
    kind = ToolKind[request.form["kind"]]
    material = ToolMaterial[request.form["material"]]

    if kind == ToolKind.SHORT_CROCHET_HOOK:
        _reject_length()
        return ShortCrochetHook(
            id=tool_id,
            size=_parse_size(),
            material=material,
        )
    if kind == ToolKind.STRAIGHT_TUNISIAN_CROCHET_HOOK:
        _reject_length()
        return StraightTunisianCrochetHook(
            id=tool_id,
            size=_parse_size(),
            material=material,
        )
    if kind == ToolKind.FIXED_CIRCULAR_TUNISIAN_CROCHET_HOOK:
        _reject_length()
        return FixedCircularTunisianCrochetHook(
            id=tool_id,
            size=_parse_size(),
            material=material,
        )
    if kind == ToolKind.STRAIGHT_NEEDLES:
        return StraightNeedles(
            id=tool_id,
            size=_parse_size(),
            length=_parse_length(),
            material=material,
        )
    if kind == ToolKind.FIXED_CIRCULAR_NEEDLES:
        return FixedCircularNeedles(
            id=tool_id,
            size=_parse_size(),
            length=_parse_length(),
            material=material,
        )
    if kind == ToolKind.INTERCHANGEABLE_CIRCULAR_NEEDLE_TIPS:
        _reject_length()
        return InterchangeableCircularNeedleTips(
            id=tool_id,
            size=_parse_size(),
            material=material,
        )
    if kind == ToolKind.DOUBLE_POINTED_NEEDLES:
        _reject_length()
        return DoublePointedNeedles(
            id=tool_id,
            size=_parse_size(),
            material=material,
        )
    if kind == ToolKind.CABLE:
        _reject_size()
        return Cable(
            id=tool_id,
            length=_parse_length(),
            material=material,
        )

    raise ValueError(f"Unsupported tool kind: {kind}")


def tool_kinds_with_field(field_name: str) -> list[str]:
    result = []

    for kind, tool_class in TOOL_CLASS_BY_KIND.items():
        field_names = {field.name for field in fields(tool_class)}
        if field_name in field_names:
            result.append(kind.name)

    return result
