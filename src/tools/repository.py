from dataclasses import dataclass

from infra.db import get_db
from modules.units.centimeters import Centimeters
from tools.domain import ToolId, StraightNeedles, ToolCategory, ToolMaterial, ShortCrochetHook


@dataclass
class ToolRow:
    id: int
    category: str
    size_mm: float | None
    length_cm: float | None
    material: str

class ToolsRepository:
    def _row_to_domain(self, tool_row: ToolRow):
        category = ToolCategory[tool_row.category]

        if category == ToolCategory.SHORT_CROCHET_HOOK:
            return ShortCrochetHook(
                id=ToolId(tool_row.id),
                category=category,
                size_mm=tool_row.size_mm,
                material=ToolMaterial[tool_row.material]
            )
        elif category == ToolCategory.STRAIGHT_NEEDLES:
            return StraightNeedles(
                id=ToolId(tool_row.id),
                category=category,
                size_mm=tool_row.size_mm,
                length=Centimeters(tool_row.length_cm),
                material=ToolMaterial[tool_row.material]
            )

        raise ValueError(f"Unsupported tool category: {category}")

    def add(self, tool):
        if isinstance(tool, ShortCrochetHook):
            return self.add_short_crochet_hook(tool)

        if isinstance(tool, StraightNeedles):
            return self.add_straight_needles(tool)

        raise ValueError(f"Unsupported tool type: {type(tool)}")

    def add_short_crochet_hook(self, tool: ShortCrochetHook) -> ShortCrochetHook:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO tool (
            category, size_mm, material)
            VALUES (?, ?, ?)''',
            (
            tool.category.name,
            tool.size_mm,
            tool.material.name,
            )
        )
        db.commit()
        return ShortCrochetHook(
            id=ToolId(cursor.lastrowid),
            category=tool.category,
            size_mm=tool.size_mm,
            material=tool.material,
        )

    def add_straight_needles(self, tool: StraightNeedles) -> StraightNeedles:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO tool (
            category, size_mm, length_cm, material)
            VALUES (?, ?, ?, ?)''',
            (
            tool.category.name,
            tool.size_mm,
            tool.length.value,
            tool.material.name,
            )
        )
        db.commit()
        return StraightNeedles(
            id=ToolId(cursor.lastrowid),
            category=tool.category,
            size_mm=tool.size_mm,
            length=tool.length,
            material=tool.material,
        )




    def get_all(self) -> list[StraightNeedles]:
        db = get_db()
        cursor = db.execute('SELECT * FROM tool')

        tools = []
        for row in cursor.fetchall():
            tool_row = ToolRow(**dict(row))
            tool = self._row_to_domain(tool_row)
            tools.append(tool)

        return tools