from flask import Blueprint, render_template, request, redirect
from werkzeug.exceptions import abort
from .domain import Project, ProjectId
from .repository import ProjectRepository

projects_api = Blueprint('projects', __name__, url_prefix="/projects")
repo = ProjectRepository()

def get_project_or_404(project_id: ProjectId):
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
    project = get_project_or_404(ProjectId(project_id))
    return render_template('projects/details.html', project=project)

@projects_api.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_project = Project(
            id=None,
            name=request.form['name'],
            my_tool_size=request.form.get('my_tool_size'),
            my_gauge=request.form.get('my_gauge'),
            yarn_bought=request.form.get('yarn_bought'),
            notes=request.form.get('notes')
        )

        new_project = repo.add(new_project)
        return redirect(f"/projects/{new_project.id.value}")

    return render_template('projects/add.html')

@projects_api.route('/<int:project_id>/delete', methods=['POST'])
def delete(project_id: int):
    get_project_or_404(ProjectId(project_id))
    repo.delete(ProjectId(project_id))
    return redirect("/projects")

@projects_api.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id: int):
    project = get_project_or_404(ProjectId(project_id))
    if request.method == 'POST':
        project.name = request.form['name']
        project.my_tool_size = request.form.get('my_tool_size')
        project.my_gauge = request.form.get('my_gauge')
        project.yarn_bought = request.form.get('yarn_bought')
        project.notes = request.form.get('notes')

        repo.update(project)
        return redirect(f'/projects/{project_id}')

    return render_template('projects/edit.html', project=project)
