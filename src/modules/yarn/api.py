from dataclasses import dataclass

from flask import Blueprint, Response, render_template, redirect, request
from werkzeug.exceptions import abort

from modules.units.mass import Mass
from modules.units.meters import Meters
from modules.yarn.domain import (
    FiberType,
    Skein,
    SkeinId,
    Yarn,
    YarnId,
    YarnWeightCategory,
)
from modules.yarn.mappers import (
    SkeinFormData,
    YarnFormData,
)
from modules.yarn.service import YarnNotFoundError, SkeinNotFoundError, YarnService

yarn_api = Blueprint('yarn', __name__, url_prefix='/yarn')
service = YarnService()


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


def _render_yarn_form(
    form_data: YarnFormData,
    yarn_id: int | None = None,
    error: str | None = None,
):
    mode = "edit" if yarn_id else "add"
    form_action = f'/yarn/{yarn_id}/edit' if yarn_id else '/yarn/add'
    return render_template(
        'yarn/form.html',
        mode=mode,
        form_action=form_action,
        form_data=form_data,
        error=error,
        fiber_types=FiberType,
        weight_categories=YarnWeightCategory,
    )


def _render_skein_form(
    yarn: Yarn,
    form_data: SkeinFormData,
    skein_id: int | None = None,
    error: str | None = None,
):
    mode = "edit" if skein_id else "add"
    form_action = f'/yarn/skeins/{skein_id}/edit' if skein_id else f'/yarn/{yarn.id.value}/skeins/add'
    return render_template(
        'yarn/skein_form.html',
        mode=mode,
        yarn=yarn,
        form_action=form_action,
        form_data=form_data,
        error=error,
    )


@yarn_api.get('')
def index():
    yarns = service.get_all_yarns()
    return render_template('yarn/index.html', yarns=yarns)



@dataclass
class SkeinGroup:
    main_skein: Skein
    skein_ids: list[SkeinId]

    @property
    def single_skein_current_weight(self):
        return self.main_skein.current_weight

    @property
    def total_current_weight(self) -> Mass:
        return self.single_skein_current_weight * self.total_skeins

    def total_remaining_length(self, yarn: Yarn) -> Meters:
        return self.main_skein.remaining_length(yarn) * self.total_skeins

    @property
    def total_skeins(self):
        return len(self.skein_ids)

    @property
    def is_single(self):
        return self.total_skeins == 1


@dataclass
class SkeinGroups:
    groups: list[SkeinGroup]

    def is_empty(self):
        return len(self.groups) == 0

    @property
    def total_skeins(self):
        return sum(group.total_skeins for group in self.groups)

    @property
    def total_current_weight(self):
        return sum(group.total_current_weight for group in self.groups)

    def total_remaining_length(self, yarn: Yarn) -> Meters:
        return sum(group.total_remaining_length(yarn) for group in self.groups)


    @classmethod
    def from_skeins(cls, skeins: list[Skein]) -> "SkeinGroups":
        skein_weight_group: dict[Mass, list[SkeinId]] = {}
        main_skeins: dict[Mass, Skein] = {}
        skeins_groups: list[SkeinGroup] = []
        for skein in skeins:
            weight_cat = skein.current_weight
            if weight_cat not in skein_weight_group:
                skein_weight_group[weight_cat] = []
            skein_weight_group[weight_cat].append(skein.id)

            if weight_cat not in main_skeins:
                main_skeins[weight_cat] = skein

        for weight, ids_list in skein_weight_group.items():
            main_skein = main_skeins[weight]
            group_of_skeins = SkeinGroup(main_skein=main_skein, skein_ids=ids_list)
            skeins_groups.append(group_of_skeins)
        return SkeinGroups(skeins_groups)

    # @classmethod
    # def from_skeins(cls, skeins: list[Skein]) -> "SkeinGroups":
    #     skein_weight_group: dict[Mass, list[Skein]] = {}
    #     for skein in skeins:
    #         weight_cat = skein.current_weight
    #         if weight_cat not in skein_weight_group:
    #             skein_weight_group[weight_cat] = []
    #         skein_weight_group[weight_cat].append(skein)
    #
    #     skeins_groups: list[SkeinGroup] = []
    #     for weight, skeins_with_weight in skein_weight_group:
    #         main_skein = skeins_with_weight[0]
    #         ids_list = [skein.id for skein in skeins_with_weight]
    #         group_of_skeins = SkeinGroup(main_skein=main_skein, skein_ids=ids_list)
    #         skeins_groups.append(group_of_skeins)
    #     return SkeinGroups(skeins_groups)
    #

@yarn_api.get('/<int:yarn_id>')
def yarn_details(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    skeins = service.get_skeins_for_yarn(yarn.id)
    skein_groups = SkeinGroups.from_skeins(skeins)
    return render_template(
        'yarn/details.html',
        yarn=yarn,
        skein_groups=skein_groups,
    )


@yarn_api.get('/<int:yarn_id>/image')
def yarn_image(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    if yarn.image_blob is None:
        abort(404, f"Yarn id {yarn_id} doesn't have an image.")

    return Response(
        yarn.image_blob,
        mimetype=yarn.image_mime_type or 'application/octet-stream',
    )


@yarn_api.get('/add')
def create_yarn_form():
    return _render_yarn_form(YarnFormData.empty())


@yarn_api.post('/add')
def create_yarn():
    form_data = YarnFormData.from_request_form(request.form, request.files)
    try:
        yarn = form_data.to_domain()
        new_yarn = service.add_yarn(yarn)
        return redirect(f'/yarn/{new_yarn.id.value}')
    except Exception as error:
        return _render_yarn_form(form_data, error=str(error))


@yarn_api.get('/<int:yarn_id>/edit')
def edit_yarn_form(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    form_data = YarnFormData.from_domain(yarn)
    return _render_yarn_form(form_data, yarn_id=yarn_id)


@yarn_api.post('/<int:yarn_id>/edit')
def update_yarn(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    form_data = YarnFormData.from_request_form(
        request.form,
        request.files,
        existing_yarn=yarn,
    )
    try:
        updated_yarn = form_data.to_domain(yarn.id)
        service.update_yarn(updated_yarn)
        return redirect(f'/yarn/{yarn_id}')
    except Exception as error:
        return _render_yarn_form(form_data, yarn_id=yarn_id, error=str(error))


@yarn_api.post('/<int:yarn_id>/delete')
def delete_yarn(yarn_id: int):
    service.delete_yarn(YarnId(yarn_id))
    return redirect('/yarn')


@yarn_api.get('/<int:yarn_id>/skeins/add')
def create_skein_form(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    form_data = SkeinFormData.empty(current_weight=str(yarn.full_weight.grams))
    return _render_skein_form(yarn, form_data)


@yarn_api.post('/<int:yarn_id>/skeins/add')
def create_skein(yarn_id: int):
    yarn = _get_yarn_or_404(YarnId(yarn_id))
    form_data = SkeinFormData.from_request_form(request.form)
    try:
        skein = form_data.to_domain(yarn.id)
        service.add_skein(skein)
        return redirect(f'/yarn/{yarn_id}')
    except Exception as error:
        return _render_skein_form(yarn, form_data, error=str(error))

@yarn_api.post('/skeins/<int:skein_id>/add-one')
def add_one_skein(skein_id: int):
    original_skein = service.get_skein(SkeinId(skein_id))
    yarn_id = original_skein.yarn_id.value

    new_skein = Skein(
        id=None,
        yarn_id=original_skein.yarn_id,
        current_weight=original_skein.current_weight,
    )

    service.add_skein(new_skein)
    return redirect(f'/yarn/{yarn_id}')


@yarn_api.get('/skeins/<int:skein_id>/edit')
def edit_skein_form(skein_id: int):
    skein = _get_skein_or_404(SkeinId(skein_id))
    yarn = _get_yarn_or_404(skein.yarn_id)
    form_data = SkeinFormData.from_domain(skein)
    return _render_skein_form(yarn, form_data, skein_id=skein_id)


@yarn_api.post('/skeins/<int:skein_id>/edit')
def update_skein(skein_id: int):
    current_skein = _get_skein_or_404(SkeinId(skein_id))
    yarn = _get_yarn_or_404(current_skein.yarn_id)
    form_data = SkeinFormData.from_request_form(request.form)
    try:
        skein_to_update = form_data.to_domain(current_skein.yarn_id, current_skein.id)
        service.update_skein(skein_to_update)
        return redirect(f'/yarn/{skein_to_update.yarn_id.value}')
    except Exception as error:
        return _render_skein_form(yarn, form_data, skein_id=skein_id, error=str(error))


@yarn_api.post('/skeins/<int:skein_id>/delete')
def delete_skein(skein_id: int):
    yarn_id = service.delete_skein(SkeinId(skein_id))
    return redirect(f'/yarn/{yarn_id.value}')
