from flask import Blueprint, render_template, redirect, request
from werkzeug.exceptions import abort

from use_cases.delete_pattern_use_case import DeletePatternUseCase
from modules.patterns.domain import PatternCategory, PatternId, PatternDifficultyLevel
from modules.patterns.mappers import PatternFormData
from modules.patterns.repository import PatternRepository
from modules.projects.repository import ProjectRepository

patterns_api = Blueprint('patterns', __name__, url_prefix="/patterns")
repo = PatternRepository()
delete_pattern_use_case = DeletePatternUseCase(ProjectRepository(), repo)

def get_pattern_or_404(pattern_id: PatternId):
    pattern = repo.get_by_id(pattern_id)
    if pattern is None:
        abort(404, f"Pattern id {pattern_id} doesn't exist.")
    return pattern


@patterns_api.get('')
def index():
    patterns = repo.get_all()
    return render_template('patterns/index.html', patterns=patterns)

@patterns_api.get('/<int:pattern_id>')
def details(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    return render_template('patterns/details.html', pattern=pattern)


def _render_pattern_form(
    template_name: str,
    form_data: PatternFormData,
    pattern_id: int | None = None,
    error: str | None = None,
):
    subcategories_map = {}
    for category in PatternCategory:
        subcategories_map[category.name] = category.subcategories()
    mode = "edit" if pattern_id else "add"
    form_action = f"/patterns/{pattern_id}/edit" if pattern_id else "/patterns/add"
    return render_template(
        template_name,
        mode=mode,
        form_action=form_action,
        form_data=form_data,
        pattern_id=pattern_id,
        error=error,
        pattern_categories=PatternCategory,
        subcategories_map=subcategories_map,
        difficulty_levels=PatternDifficultyLevel,
    )


@patterns_api.get('/add')
def create_pattern_form():
    return _render_pattern_form("patterns/add.html", PatternFormData.empty())

@patterns_api.post('/add')
def create_pattern():
    form_data = PatternFormData.from_request_form(request.form)
    try:
        new_pattern = form_data.to_domain()
        new_pattern = repo.add(new_pattern)
        return redirect(f"/patterns/{new_pattern.id.value}")
    except Exception as error:
        return _render_pattern_form("patterns/add.html", form_data, error=str(error))

@patterns_api.post('/<int:pattern_id>/delete')
def delete(pattern_id: int):
    get_pattern_or_404(PatternId(pattern_id))
    delete_pattern_use_case.delete_pattern(PatternId(pattern_id))
    return redirect("/patterns")

@patterns_api.get('/<int:pattern_id>/edit')
def edit_pattern_form(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    form_data = PatternFormData.from_domain(pattern)
    return _render_pattern_form("patterns/edit.html", form_data, pattern_id=pattern_id)

@patterns_api.post('/<int:pattern_id>/edit')
def edit_pattern(pattern_id: int):
    get_pattern_or_404(PatternId(pattern_id))
    form_data = PatternFormData.from_request_form(request.form)
    try:
        edited_pattern = form_data.to_domain(PatternId(pattern_id))
        repo.update(edited_pattern)
        return redirect(f'/patterns/{pattern_id}')
    except Exception as error:
        return _render_pattern_form("patterns/edit.html", form_data, pattern_id=pattern_id, error=str(error))
