from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.exceptions import abort
from .domain import Project
from .repository import ProjectRepository

projects_api = Blueprint('projects', __name__, url_prefix="/projects")
repo = ProjectRepository()

def get_project_or_404(project_id: int):
    project = repo.get_by_id(project_id)
    if project is None:
        abort(404, f"Project id {project_id} doesn't exist.")
    return project

@projects_api.route('')
def index():
    projects = repo.get_all()
    return render_template('projects/index.html', projects=projects)

@projects_api.route('/<int:project_id>')
def details(project_id: int):
    project = get_project_or_404(project_id)
    return render_template('projects/details.html', project=project)

@projects_api.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # tworzymy obiekt domenowy najpierw w pamięci komputera z danych od usera (nie wpada jeszcze do bazy!)
        new_project = Project(
            name=request.form['name'],
            type=request.form.get('type'),
            subtype=request.form.get('subtype'),
            tool=request.form.get('tool'),
            needle_size=request.form.get('needle_size'),
            skeins=request.form.get('skeins'),
            skeins_needed=request.form.get('skeins_needed', type=int) if request.form.get('skeins_needed') else None,
            pattern_language=request.form.get('pattern_language'),
            designer=request.form.get('designer'),
            yarn_bought=request.form.get('yarn_bought'),
            notes=request.form.get('notes')
        )
        
        # teraz delegujemy zadanie jego fizycznego zapisu do Repozytorium 
        new_project = repo.add(new_project)
        return redirect(f"/projects/{new_project.id}")
        
    return render_template('projects/add.html')

@projects_api.route('/<int:project_id>/delete', methods=['POST'])
def delete(project_id: int):
    # używamy pomocniczej metody, żeby upewnić się, czy na pewno projekt istnieje
    get_project_or_404(project_id)
    repo.delete(project_id)
    return redirect("/projects")

@projects_api.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id: int):
    project = get_project_or_404(project_id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.category = request.form.get('type')
        project.subcategory = request.form.get('subtype')
        project.tool = request.form.get('tool')
        project.tool_size = request.form.get('needle_size')
        project.skeins = request.form.get('skeins')
        project.skeins_needed = request.form.get('skeins_needed', type=int) if request.form.get('skeins_needed') else None
        project.pattern_language = request.form.get('pattern_language')
        project.designer = request.form.get('designer')
        project.yarn_bought = request.form.get('yarn_bought')
        project.notes = request.form.get('notes')
        
        # wywołujemy update w Repozytorium - przekaże to wprost jako query do dazy
        repo.update(project)
        return redirect(f'/projects/{project_id}')

    return render_template('projects/edit.html', project=project)
