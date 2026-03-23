from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import abort
from .domain import ProjectId, ProjectStatus
from .mappers import parse_project_from_form
from .repository import ProjectRepository

projects_api = Blueprint('projects', __name__, url_prefix="/projects")
repo = ProjectRepository()

def get_project_or_404(project_id: ProjectId):
    project = repo.get_by_id(project_id)
    if project is None:
        abort(404, f"Project id {project_id} doesn't exist.")
    return project


@projects_api.get('')
def index():
    projects = repo.get_all()
    return render_template('projects/index.html', projects=projects)

@projects_api.get('/<int:project_id>')
def details(project_id: int):
    project = get_project_or_404(ProjectId(project_id))
    return render_template('projects/details.html', project=project)

@projects_api.get('/add')
def create_project_form():
    return render_template('projects/add.html', status=ProjectStatus)

@projects_api.post('/add')
def create_project():
    new_project = parse_project_from_form()
    new_project = repo.add(new_project)
    return redirect(f"/projects/{new_project.id.value}")


@projects_api.post('/<int:project_id>/delete')
def delete(project_id: int):
    get_project_or_404(ProjectId(project_id))
    repo.delete(ProjectId(project_id))
    return redirect("/projects")

@projects_api.get('/<int:project_id>/edit')
def edit_project_form(project_id: int):
    project = get_project_or_404(ProjectId(project_id))
    return render_template('projects/edit.html', project=project, status=ProjectStatus)


@projects_api.post('/<int:project_id>/edit')
def edit_project(project_id: int):
    get_project_or_404(ProjectId(project_id))
    edited_project = parse_project_from_form()
    edited_project.id = ProjectId(project_id)

    repo.update(edited_project)
    return redirect(f'/projects/{project_id}')

