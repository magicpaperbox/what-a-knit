from __future__ import annotations

from dataclasses import dataclass, field

from modules.units.mass import Mass
from modules.units.meters import Meters
from modules.yarn.domain import (
    FiberType,
    Skein,
    SkeinId,
    Yarn,
    YarnFiber,
    YarnId,
    YarnWeightCategory,
)


@dataclass(frozen=True)
class YarnFiberFormData:
    fiber_type: str = ""
    percentage: str = ""


@dataclass
class YarnFormData:
    brand: str = ""
    name: str = ""
    color_shade: str = ""
    weight_category: str = ""
    full_weight: str = ""
    full_length: str = ""
    notes: str = ""
    composition_rows: list[YarnFiberFormData] = field(default_factory=list)

    @classmethod
    def empty(cls) -> YarnFormData:
        return YarnFormData()

    @classmethod
    def from_domain(cls, yarn: Yarn) -> YarnFormData:
        return YarnFormData(
            brand=yarn.brand,
            name=yarn.name,
            color_shade=yarn.color_shade,
            weight_category=yarn.weight_category.name,
            full_weight=str(yarn.full_weight.grams),
            full_length=str(yarn.full_length.value),
            notes=yarn.notes or "",
            composition_rows=[
                YarnFiberFormData(
                    fiber_type=fiber.fiber_type.name,
                    percentage=str(fiber.percentage),
                )
                for fiber in yarn.composition
            ],
        )

    def to_domain(self, yarn_id: YarnId | None = None) -> Yarn:
        composition = []
        for row in self.composition_rows:
            if row.fiber_type and row.percentage:
                composition.append(
                    YarnFiber(
                        fiber_type=FiberType[row.fiber_type],
                        percentage=int(row.percentage),
                    )
                )

        return Yarn(
            id=yarn_id,
            brand=self.brand,
            name=self.name,
            color_shade=self.color_shade,
            weight_category=YarnWeightCategory[self.weight_category],
            full_weight=Mass(int(self.full_weight)),
            full_length=Meters(float(self.full_length)),
            notes=self.notes or None,
            composition=composition,
        )

    @classmethod
    def from_request_form(cls, form) -> YarnFormData:
        def composition_rows_from_request() -> list[YarnFiberFormData]:
            fiber_types = form.getlist('fiber_type[]')
            percentages = form.getlist('percentage[]')
            row_count = max(len(fiber_types), len(percentages))
            rows = []
            for index in range(row_count):
                fiber_type = fiber_types[index] if index < len(fiber_types) else ""
                percentage = percentages[index] if index < len(percentages) else ""
                rows.append(
                    YarnFiberFormData(
                        fiber_type=fiber_type,
                        percentage=percentage,
                    )
                )
            return rows

        return YarnFormData(
            brand=form.get('brand', ''),
            name=form.get('name', ''),
            color_shade=form.get('color_shade', ''),
            weight_category=form.get('weight_category', ''),
            full_weight=form.get('full_weight', ''),
            full_length=form.get('full_length', ''),
            notes=form.get('notes', ''),
            composition_rows=composition_rows_from_request(),
        )


@dataclass
class SkeinFormData:
    current_weight: str = ""

    @classmethod
    def empty(cls, current_weight: str = "") -> SkeinFormData:
        return SkeinFormData(current_weight=current_weight)

    @classmethod
    def from_domain(cls, skein: Skein) -> SkeinFormData:
        return SkeinFormData(current_weight=str(skein.current_weight.grams))

    def to_domain(self, yarn_id: YarnId, skein_id: SkeinId | None = None) -> Skein:
        return Skein(
            id=skein_id,
            yarn_id=yarn_id,
            current_weight=Mass(int(self.current_weight)),
        )

    @classmethod
    def from_request_form(cls, form) -> SkeinFormData:
        return SkeinFormData(
            current_weight=form.get('current_weight', ''),
        )
