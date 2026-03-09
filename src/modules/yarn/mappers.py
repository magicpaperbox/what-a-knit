from flask import request

from modules.units.mass import Mass
from modules.units.meters import Meters
from modules.yarn.domain import (
    Yarn, YarnFiber, FiberType, YarnWeightCategory,
    Skein, YarnId, SkeinId,
)


def parse_composition_from_form() -> list[YarnFiber]:
    fiber_types = request.form.getlist('fiber_type[]')
    percentages = request.form.getlist('percentage[]')
    fibers = []
    for ft, pct in zip(fiber_types, percentages):
        if ft and pct:
            fibers.append(YarnFiber(fiber_type=FiberType[ft], percentage=int(pct)))
    return fibers


def parse_yarn_from_form(yarn_id: YarnId | None = None) -> Yarn:
    composition = parse_composition_from_form()
    return Yarn(
        id=yarn_id,
        brand=request.form['brand'],
        name=request.form['name'],
        color_shade=request.form['color_shade'],
        weight_category=YarnWeightCategory[request.form['weight_category']],
        full_weight=Mass(int(request.form['full_weight'])),
        full_length=Meters(float(request.form['full_length'])),
        composition=composition,
    )

def parse_skein_from_form(yarn_id: YarnId, skein_id: SkeinId | None = None) -> Skein:
    return Skein(
        id=skein_id,
        yarn_id=yarn_id,
        current_weight=Mass(int(request.form['current_weight'])),
    )
