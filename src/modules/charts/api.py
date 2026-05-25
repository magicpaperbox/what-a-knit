
from flask import render_template, Blueprint, redirect, abort, request

from modules.charts.domain import Chart, ChartId
from modules.charts.mappers import ChartFormData
from modules.charts.repository import ChartRepository
from modules.charts.service import ChartService

charts_api = Blueprint('charts', __name__, url_prefix="/charts")
repo = ChartRepository()
service = ChartService()


def _get_chart_or_404(chart_id: int) -> Chart:
    chart = repo.get_by_id(ChartId(chart_id))
    if chart is None:
        abort(404, f"Chart id {chart_id} doesn't exist.")
    return chart


def _render_chart_form(
    form_data: ChartFormData,
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
        form_data=ChartFormData.empty(),
        mode="create",
        form_action="/charts/add",
    )


@charts_api.post("/add")
def create_chart():
    form_data = ChartFormData.from_request_form(request.form)
    try:
        chart = form_data.to_domain()
        saved_chart = service.add_chart(chart)
        return redirect(f"/charts/{saved_chart.id.value}/edit")
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
    form_data = ChartFormData.from_domain(chart)
    return _render_chart_form(
        form_data=form_data,
        mode="edit",
        form_action=f"/charts/{chart_id}/edit",
        chart_id=chart_id,
    )


@charts_api.post("/<int:chart_id>/edit")
def edit_chart(chart_id: int):
    _get_chart_or_404(chart_id)
    form_data = ChartFormData.from_request_form(request.form)
    try:
        chart = form_data.to_domain(chart_id=ChartId(chart_id))
        service.update_chart(chart)
        return redirect(f"/charts/{chart_id}/edit")
    except ValueError as error:
        return _render_chart_form(
            form_data=form_data,
            mode="edit",
            form_action=f"/charts/{chart_id}/edit",
            chart_id=chart_id,
            error=str(error),
        )


@charts_api.post('/<int:chart_id>/delete')
def delete(chart_id: int):
    _get_chart_or_404(chart_id)
    repo.delete(chart_id)
    return redirect("/charts")