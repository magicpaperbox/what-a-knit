import dataclasses
from dataclasses import dataclass
from typing import Optional

from infra.db import get_db
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
    ToolKind,
    ToolMaterial,
)


@dataclass
class ToolRow:
    id: int | None
    kind: str
    size_mm: float | None
    length_cm: float | None
    material: str


class ToolsRepository:
    def _row_to_domain(self, tool_row: ToolRow) -> Tool:
        kind = ToolKind[tool_row.kind]
        tool_id = ToolId(tool_row.id) if tool_row.id is not None else None

        if kind == ToolKind.SHORT_CROCHET_HOOK:
            return ShortCrochetHook(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.STRAIGHT_TUNISIAN_CROCHET_HOOK:
            return StraightTunisianCrochetHook(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.FIXED_CIRCULAR_TUNISIAN_CROCHET_HOOK:
            return FixedCircularTunisianCrochetHook(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.STRAIGHT_NEEDLES:
            return StraightNeedles(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                length=Centimeters(tool_row.length_cm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.FIXED_CIRCULAR_NEEDLES:
            return FixedCircularNeedles(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                length=Centimeters(tool_row.length_cm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.INTERCHANGEABLE_CIRCULAR_NEEDLE_TIPS:
            return InterchangeableCircularNeedleTips(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.DOUBLE_POINTED_NEEDLES:
            return DoublePointedNeedles(
                id=tool_id,
                size=Thickness(tool_row.size_mm),
                material=ToolMaterial[tool_row.material]
            )
        if kind == ToolKind.CABLE:
            return Cable(
                id=tool_id,
                length=Centimeters(tool_row.length_cm),
                material=ToolMaterial[tool_row.material]
            )

        raise ValueError(f"Unsupported tool kind: {kind}")

    def _domain_to_row(self, tool: Tool) -> ToolRow:
        tool_id = tool.id.value if tool.id else None

        if isinstance(tool, ShortCrochetHook):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=None,
                material=tool.material.name,
            )

        if isinstance(tool, StraightTunisianCrochetHook):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=None,
                material=tool.material.name,
            )

        if isinstance(tool, FixedCircularTunisianCrochetHook):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=None,
                material=tool.material.name,
            )

        if isinstance(tool, StraightNeedles):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=tool.length.value,
                material=tool.material.name,
            )

        if isinstance(tool, FixedCircularNeedles):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=tool.length.value,
                material=tool.material.name,
            )

        if isinstance(tool, InterchangeableCircularNeedleTips):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=None,
                material=tool.material.name,
            )

        if isinstance(tool, DoublePointedNeedles):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=tool.size.millimeters,
                length_cm=None,
                material=tool.material.name,
            )

        if isinstance(tool, Cable):
            return ToolRow(
                id=tool_id,
                kind=tool.kind.name,
                size_mm=None,
                length_cm=tool.length.value,
                material=tool.material.name,
            )

        raise ValueError(f"Unsupported tool type: {type(tool)}")


    def add(self, tool: Tool) -> Tool:
        row = self._domain_to_row(tool)
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO tool (
            kind, size_mm, length_cm, material)
            VALUES (?, ?, ?, ?)''',
            (
            row.kind,
            row.size_mm,
            row.length_cm,
            row.material,
            )
        )
        db.commit()
        tool_id = ToolId(cursor.lastrowid)
        return dataclasses.replace(tool, id=tool_id)

    def update(self, tool: Tool) -> None:
        row = self._domain_to_row(tool)
        db = get_db()
        db.execute(
            '''UPDATE tool
            SET kind = ?, size_mm = ?, length_cm = ?, material = ?
            WHERE id = ?''',
            (
                row.kind,
                row.size_mm,
                row.length_cm,
                row.material,
                row.id,
            )
        )
        db.commit()

    def delete(self, tool_id: ToolId) -> None:
        db = get_db()
        db.execute('DELETE FROM tool WHERE id = ?', (tool_id.value,))
        db.commit()

    def get_all(self) -> list[Tool]:
        db = get_db()
        cursor = db.execute('SELECT * FROM tool')

        tools = []
        for row in cursor.fetchall():
            tool_row = ToolRow(**dict(row))
            tool = self._row_to_domain(tool_row)
            tools.append(tool)

        return tools

    def get_by_id(self, tool_id: ToolId) -> Optional[Tool]:
        db = get_db()
        cursor = db.execute('SELECT * FROM tool WHERE id = ?', (tool_id.value,))
        row = cursor.fetchone()

        if row is None:
            return None

        tool_row = ToolRow(**dict(row))
        return self._row_to_domain(tool_row)
