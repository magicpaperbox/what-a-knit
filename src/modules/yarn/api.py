from flask import Blueprint, render_template, request, redirect
from werkzeug.exceptions import abort

from modules.yarn.domain import (
    Yarn, Skein, FiberType, YarnWeightCategory, YarnId, SkeinId,
)
from modules.yarn.mappers import parse_yarn_from_form, parse_skein_from_form
from modules.yarn.service import YarnService, YarnNotFoundError, SkeinNotFoundError

yarn_api = Blueprint('yarn', __name__, url_prefix='/yarn')
service = YarnService()

# --- Error handling ---

def _get_yarn_or_404(yarn_id: YarnId) -> Yarn:
    try:
        return service.get_yarn(yarn_id)
    except YarnNotFoundError:
        abort(404, f"Yarn id {yarn_id} doesn't exist.")


def _get_skein_or_404(skein_id: SkeinId) -> Skein:
    try:
        return service.get_skein(skein_id)
    except SkeinNotFoundError:
        abort(404, f"Skein id {skein_id} doesn't exist.")


# --- Yarn routes ---

@yarn_api.get('')
def index():
    yarns = service.get_all_yarns()
    return render_template('yarn/index.html', yarns=yarns)


@yarn_api.get('/<int:yarn_id>')
def yarn_details(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    skeins = service.get_skeins_for_yarn(yarn.id)
    return render_template(
        'yarn/details.html',
        yarn=yarn,
        skeins=skeins,
    )


@yarn_api.get('/add')
def create_yarn_form():
    return render_template(
        'yarn/add.html',
        fiber_types=FiberType,
        weight_categories=YarnWeightCategory,
    )


@yarn_api.post('/add')
def create_yarn():
    yarn = parse_yarn_from_form()
    try:
        new_yarn = service.add_yarn(yarn)
    except ValueError as e:
        return render_template(
            'yarn/add.html',
            error=str(e),
            form=request.form,
            fiber_types=FiberType,
            weight_categories=YarnWeightCategory,
        )
    return redirect(f'/yarn/{new_yarn.id.value}')


@yarn_api.get('/<int:yarn_id>/edit')
def edit_yarn_form(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    return render_template(
        'yarn/edit.html',
        yarn=yarn,
        fiber_types=FiberType,
        weight_categories=YarnWeightCategory,
    )


@yarn_api.post('/<int:yarn_id>/edit')
def update_yarn(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    updated_yarn = parse_yarn_from_form(yarn.id)
    try:
        service.update_yarn(updated_yarn)
    except ValueError as e:
        return render_template(
            'yarn/edit.html',
            yarn=yarn,
            error=str(e),
            form=request.form,
            fiber_types=FiberType,
            weight_categories=YarnWeightCategory,
        )
    return redirect(f'/yarn/{yarn_id}')


@yarn_api.post('/<int:yarn_id>/delete')
def delete_yarn(yarn_id: int):
    service.delete_yarn(YarnId(yarn_id))
    return redirect('/yarn')


# --- Skein routes ---

@yarn_api.get('/<int:yarn_id>/skeins/add')
def create_skein_form(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    return render_template(
        'yarn/add_skein.html',
        yarn=yarn,
    )


@yarn_api.post('/<int:yarn_id>/skeins/add')
def create_skein(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    skein = parse_skein_from_form(yarn.id)
    service.add_skein(skein)
    return redirect(f'/yarn/{yarn_id}')

# TODO handle error in form
@yarn_api.get('/skeins/<int:skein_id>/edit')
def edit_skein_form(skein_id: int):
    skein = _get_skein_or_404(SkeinId(skein_id))
    yarn = _get_yarn_or_404(skein.yarn_id)
    return render_template(
        'yarn/edit_skein.html',
        skein=skein,
        yarn=yarn,
    )

@yarn_api.post('/skeins/<int:skein_id>/edit')
def update_skein(skein_id: int):
    current_skein = _get_skein_or_404(SkeinId(skein_id))
    skein_to_update = parse_skein_from_form(current_skein.yarn_id, current_skein.id)
    service.update_skein(skein_to_update)
    return redirect(f'/yarn/{skein_to_update.yarn_id.value}')


@yarn_api.post('/skeins/<int:skein_id>/delete')
def delete_skein(skein_id: int):
    yarn_id = service.delete_skein(SkeinId(skein_id))
    return redirect(f'/yarn/{yarn_id.value}')