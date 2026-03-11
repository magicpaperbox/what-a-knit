from flask import Blueprint, render_template, request, redirect
from werkzeug.exceptions import abort
from .domain import Pattern, PatternCategory, PatternId
from .repository import PatternRepository

patterns_api = Blueprint('patterns', __name__, url_prefix="/patterns")
repo = PatternRepository()

def get_pattern_or_404(pattern_id: PatternId):
    pattern = repo.get_by_id(pattern_id)
    if pattern is None:
        abort(404, f"Pattern id {pattern_id} doesn't exist.")
    return pattern


@patterns_api.route('')
def index():
    patterns = repo.get_all()
    return render_template('patterns/index.html', patterns=patterns)

@patterns_api.route('/<int:pattern_id>')
def details(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    return render_template('patterns/details.html', pattern=pattern)

@patterns_api.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_pattern = Pattern(
            id=None,
            name=request.form['name'],
            category=PatternCategory[request.form.get('category')],
            tool=request.form.get('tool'),
            gauge=request.form.get('gauge'),
            subcategory=request.form.get('subcategory'),
            tool_size=request.form.get('needle_size'),
            yarn_type=request.form.get('skeins'),
            skeins_needed=request.form.get('skeins_needed', type=int) if request.form.get('skeins_needed') else None,
            pattern_language=request.form.get('pattern_language'),
            designer=request.form.get('designer'),
            difficulty=request.form.get('difficulty'),
        )

        new_pattern = repo.add(new_pattern)
        return redirect(f"/patterns/{new_pattern.id.value}")

    subcategories_map = {}
    for category in PatternCategory:
        subcategories_map[category.name] = category.subcategories()
        
    return render_template('patterns/add.html', pattern_categories=PatternCategory, subcategories_map=subcategories_map)

@patterns_api.route('/<int:pattern_id>/delete', methods=['POST'])
def delete(pattern_id: int):
    get_pattern_or_404(PatternId(pattern_id))
    repo.delete(PatternId(pattern_id))
    return redirect("/patterns")

@patterns_api.route('/<int:pattern_id>/edit', methods=['GET', 'POST'])
def edit(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    if request.method == 'POST':
        pattern.name = request.form['name']
        pattern.category = PatternCategory[request.form.get('category')]
        pattern.subcategory = request.form.get('subcategory')
        pattern.tool = request.form.get('tool')
        pattern.tool_size = request.form.get('needle_size')
        pattern.yarn_type = request.form.get('skeins')
        pattern.skeins_needed = request.form.get('skeins_needed', type=int) if request.form.get('skeins_needed') else None
        pattern.pattern_language = request.form.get('pattern_language')
        pattern.designer = request.form.get('designer')
        pattern.yarn_bought = request.form.get('yarn_bought')
        pattern.notes = request.form.get('notes')

        repo.update(pattern)
        return redirect(f'/patterns/{pattern_id}')

    subcategories_map = {}
    for category in PatternCategory:
        subcategories_map[category.name] = category.subcategories()

    return render_template('patterns/edit.html', pattern=pattern, pattern_categories=PatternCategory, subcategories_map=subcategories_map)
