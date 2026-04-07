from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import abort

from use_cases.delete_pattern_use_case import DeletePatternUseCase
from modules.patterns.domain import PatternCategory, PatternId, PatternDifficultyLevel
from modules.patterns.mappers import parse_pattern_from_form
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

@patterns_api.get('/add')
def create_pattern_form():
    subcategories_map = {}
    for category in PatternCategory:
        subcategories_map[category.name] = category.subcategories()

    return render_template('patterns/add.html', pattern_categories=PatternCategory, subcategories_map=subcategories_map, difficulty_levels=PatternDifficultyLevel)

@patterns_api.post('/add')
def create_pattern():
    new_pattern = parse_pattern_from_form()
    new_pattern = repo.add(new_pattern)
    return redirect(f"/patterns/{new_pattern.id.value}")

@patterns_api.post('/<int:pattern_id>/delete')
def delete(pattern_id: int):
    get_pattern_or_404(PatternId(pattern_id))
    delete_pattern_use_case.delete_pattern(PatternId(pattern_id))
    return redirect("/patterns")

@patterns_api.get('/<int:pattern_id>/edit')
def edit_pattern_form(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    subcategories_map = {}
    for category in PatternCategory:
        subcategories_map[category.name] = category.subcategories()

    return render_template(
        'patterns/edit.html',
        pattern=pattern,
        pattern_categories=PatternCategory,
        subcategories_map=subcategories_map,
        difficulty_levels=PatternDifficultyLevel
    )

@patterns_api.post('/<int:pattern_id>/edit')
def edit_pattern(pattern_id: int):
    get_pattern_or_404(PatternId(pattern_id))

    edited_pattern = parse_pattern_from_form()
    edited_pattern.id = PatternId(pattern_id)

    repo.update(edited_pattern)
    return redirect(f'/patterns/{pattern_id}')