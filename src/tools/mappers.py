from __future__ import annotations

from dataclasses import dataclass, fields

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


def tool_kinds_with_field(field_name: str) -> list[str]:
    result = []

    for kind, tool_class in TOOL_CLASS_BY_KIND.items():
        field_names = {field.name for field in fields(tool_class)}
        if field_name in field_names:
            result.append(kind.name)

    return result


@dataclass
class ToolFormData:
    kind: str = ""
    size: str = ""
    length: str = ""
    material: str = ""

    @classmethod
    def empty(cls) -> ToolFormData:
        return ToolFormData()

    @classmethod
    def from_request_form(cls, form) -> ToolFormData:
        return ToolFormData(
            kind=form.get("kind", ""),
            size=form.get("size", ""),
            length=form.get("length", ""),
            material=form.get("material", ""),
        )

    @classmethod
    def from_domain(cls, tool: Tool) -> ToolFormData:
        size = ""
        if hasattr(tool, "size"):
            size = str(tool.size.millimeters)

        length = ""
        if hasattr(tool, "length"):
            length = str(tool.length.value)

        return ToolFormData(
            kind=tool.kind.name,
            size=size,
            length=length,
            material=tool.material.name,
        )

    def _parse_size(self) -> Thickness:
        if not self.size:
            raise ValueError("Size is required for this tool type")
        return Thickness(float(self.size))

    def _parse_length(self) -> Centimeters:
        if not self.length:
            raise ValueError("Length is required for this tool type")
        return Centimeters(float(self.length))

    def _reject_size(self) -> None:
        if self.size:
            raise ValueError("Size not supported for this tool type")

    def _reject_length(self) -> None:
        if self.length:
            raise ValueError("Length not supported for this tool type")

    def to_domain(self, tool_id: ToolId | None = None) -> Tool:
        kind = ToolKind[self.kind]
        material = ToolMaterial[self.material]

        if kind == ToolKind.SHORT_CROCHET_HOOK:
            self._reject_length()
            return ShortCrochetHook(
                id=tool_id,
                size=self._parse_size(),
                material=material,
            )
        if kind == ToolKind.STRAIGHT_TUNISIAN_CROCHET_HOOK:
            self._reject_length()
            return StraightTunisianCrochetHook(
                id=tool_id,
                size=self._parse_size(),
                material=material,
            )
        if kind == ToolKind.FIXED_CIRCULAR_TUNISIAN_CROCHET_HOOK:
            self._reject_length()
            return FixedCircularTunisianCrochetHook(
                id=tool_id,
                size=self._parse_size(),
                material=material,
            )
        if kind == ToolKind.STRAIGHT_NEEDLES:
            return StraightNeedles(
                id=tool_id,
                size=self._parse_size(),
                length=self._parse_length(),
                material=material,
            )
        if kind == ToolKind.FIXED_CIRCULAR_NEEDLES:
            return FixedCircularNeedles(
                id=tool_id,
                size=self._parse_size(),
                length=self._parse_length(),
                material=material,
            )
        if kind == ToolKind.INTERCHANGEABLE_CIRCULAR_NEEDLE_TIPS:
            self._reject_length()
            return InterchangeableCircularNeedleTips(
                id=tool_id,
                size=self._parse_size(),
                material=material,
            )
        if kind == ToolKind.DOUBLE_POINTED_NEEDLES:
            self._reject_length()
            return DoublePointedNeedles(
                id=tool_id,
                size=self._parse_size(),
                material=material,
            )
        if kind == ToolKind.CABLE:
            self._reject_size()
            return Cable(
                id=tool_id,
                length=self._parse_length(),
                material=material,
            )

        raise ValueError(f"Unsupported tool kind: {kind}")
