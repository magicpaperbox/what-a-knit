import json

from flask import render_template, Blueprint, redirect, request, abort

from modules.charts.domain import Chart
from modules.charts.repository import ChartRepository

charts_api = Blueprint('charts', __name__, url_prefix="/charts")
repo = ChartRepository()


ALLOWED_SYMBOL_IDS = {
    "purl",
    "ssk",
    "k2tog",
    "yarn_over",
    "front_marker",
    "no_stitch",
}


def _parse_int_field(raw_value: str, label: str, min_value: int, max_value: int) -> int:
    try:
        parsed_value = int(raw_value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a whole number.")

    if not min_value <= parsed_value <= max_value:
        raise ValueError(f"{label} must be between {min_value} and {max_value}.")

    return parsed_value


def _normalize_cells(raw_cells: object, rows: int, columns: int) -> list[list[str | None]]:
    normalized_cells = []

    for row_index in range(rows):
        source_row = []
        if isinstance(raw_cells, list) and row_index < len(raw_cells) and isinstance(raw_cells[row_index], list):
            source_row = raw_cells[row_index]

        normalized_row = []
        for column_index in range(columns):
            source_value = source_row[column_index] if column_index < len(source_row) else None
            normalized_row.append(source_value if source_value in ALLOWED_SYMBOL_IDS else None)

        normalized_cells.append(normalized_row)

    return normalized_cells


def _chart_to_form_data(chart: Chart | None = None) -> dict:
    if chart is None:
        cells = [[None for _ in range(12)] for _ in range(12)]
        return {
            "name": "",
            "rows": "12",
            "columns": "12",
            "cell_size": "32",
            "cells_json": json.dumps(cells),
        }

    return {
        "name": chart.name,
        "rows": str(chart.rows),
        "columns": str(chart.columns),
        "cell_size": str(chart.cell_size),
        "cells_json": json.dumps(chart.cells),
    }


def _form_data_from_request() -> dict:
    return {
        "name": request.form.get("name", "").strip(),
        "rows": request.form.get("rows", "12").strip(),
        "columns": request.form.get("columns", "12").strip(),
        "cell_size": request.form.get("cell_size", "32").strip(),
        "cells_json": request.form.get("cells_data", "").strip(),
    }


def _form_data_to_chart(form_data: dict, chart_id: int | None = None) -> Chart:
    name = form_data["name"]
    if not name:
        raise ValueError("Chart name is required.")

    rows = _parse_int_field(form_data["rows"], "Rows", 1, 200)
    columns = _parse_int_field(form_data["columns"], "Columns", 1, 200)
    cell_size = _parse_int_field(form_data["cell_size"], "Box size", 10, 80)

    try:
        raw_cells = json.loads(form_data["cells_json"]) if form_data["cells_json"] else []
    except json.JSONDecodeError:
        raise ValueError("Chart data is invalid.")

    return Chart(
        id=chart_id,
        name=name,
        rows=rows,
        columns=columns,
        cell_size=cell_size,
        cells=_normalize_cells(raw_cells, rows, columns),
    )


def _get_chart_or_404(chart_id: int) -> Chart:
    chart = repo.get_by_id(chart_id)
    if chart is None:
        abort(404, f"Chart id {chart_id} doesn't exist.")
    return chart


def _render_chart_form(
    form_data: dict,
    mode: str,
    form_action: str,
    chart_id: int | None = None,
    error: str | None = None,
):
    saved_charts = repo.get_all()
    return render_template(
        "charts/create_chart.html",
        form_data=form_data,
        mode=mode,
        form_action=form_action,
        chart_id=chart_id,
        error=error,
        saved_charts=saved_charts,
    )


@charts_api.get("")
def create_chart_form():
    return _render_chart_form(
        form_data=_chart_to_form_data(),
        mode="create",
        form_action="/charts/add",
    )


@charts_api.post("/add")
def create_chart():
    form_data = _form_data_from_request()
    try:
        chart = _form_data_to_chart(form_data)
        saved_chart = repo.add(chart)
        return redirect(f"/charts/{saved_chart.id}/edit")
    except ValueError as error:
        return _render_chart_form(
            form_data=form_data,
            mode="create",
            form_action="/charts/add",
            error=str(error),
        )


@charts_api.get("/<int:chart_id>/edit")
def edit_chart_form(chart_id: int):
    chart = _get_chart_or_404(chart_id)
    return _render_chart_form(
        form_data=_chart_to_form_data(chart),
        mode="edit",
        form_action=f"/charts/{chart_id}/edit",
        chart_id=chart_id,
    )


@charts_api.post("/<int:chart_id>/edit")
def edit_chart(chart_id: int):
    _get_chart_or_404(chart_id)
    form_data = _form_data_from_request()
    try:
        chart = _form_data_to_chart(form_data, chart_id=chart_id)
        repo.update(chart)
        return redirect(f"/charts/{chart_id}/edit")
    except ValueError as error:
        return _render_chart_form(
            form_data=form_data,
            mode="edit",
            form_action=f"/charts/{chart_id}/edit",
            chart_id=chart_id,
            error=str(error),
        )
