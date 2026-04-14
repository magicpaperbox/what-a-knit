from flask import Blueprint, render_template, redirect, request, abort

from modules.patterns.domain import Pattern
from modules.patterns.repository import PatternRepository
from modules.projects.domain import ProjectId, ProjectStatus
from modules.projects.mappers import ProjectFormData
from modules.projects.repository import ProjectRepository

projects_api = Blueprint('projects', __name__, url_prefix="/projects")
repo = ProjectRepository()
pattern_repo = PatternRepository()


def _get_project_or_404(project_id: ProjectId):
    project = repo.get_by_id(project_id)
    if project is None:
        abort(404, f"Project id {project_id} doesn't exist.")
    return project


def _patterns_to_dicts(patterns: list[Pattern]) -> list[dict]:
    return [{"id": pattern.id.value, "name": pattern.name} for pattern in patterns]


def _render_project_form(
    form_data: ProjectFormData,
    available_patterns: list[Pattern],
    project_id: int | None = None,
    error: str | None = None,
):
    mode = "edit" if project_id else "add"
    form_action = f'/projects/{project_id}/edit' if project_id else '/projects/add'
    return render_template(
        'projects/form.html',
        mode=mode,
        form_action=form_action,
        form_data=form_data,
        error=error,
        status=ProjectStatus,
        patterns_dicts=_patterns_to_dicts(available_patterns),
        initial_selected_patterns=form_data.selected_patterns_to_dicts(),
    )


@projects_api.get('')
def index():
    projects = repo.get_all()
    return render_template('projects/index.html', projects=projects)


@projects_api.get('/<int:project_id>')
def details(project_id: int):
    project = _get_project_or_404(ProjectId(project_id))
    patterns = pattern_repo.get_by_ids(project.pattern_ids)
    return render_template('projects/details.html', project=project, patterns=patterns)


@projects_api.get('/add')
def create_project_form():
    available_patterns = pattern_repo.get_all()
    return _render_project_form(ProjectFormData.empty(), available_patterns)


@projects_api.post('/add')
def create_project():
    available_patterns = pattern_repo.get_all()
    form_data = ProjectFormData.from_request_form(request.form, available_patterns)
    try:
        new_project = form_data.to_domain()
        new_project.normalize()
        new_project = repo.add(new_project)
        return redirect(f"/projects/{new_project.id.value}")
    except Exception as error:
        return _render_project_form(form_data, available_patterns, error=str(error))


@projects_api.post('/<int:project_id>/delete')
def delete(project_id: int):
    _get_project_or_404(ProjectId(project_id))
    repo.delete(ProjectId(project_id))
    return redirect("/projects")


@projects_api.get('/<int:project_id>/edit')
def edit_project_form(project_id: int):
    project = _get_project_or_404(ProjectId(project_id))
    available_patterns = pattern_repo.get_all()
    selected_patterns = pattern_repo.get_by_ids(project.pattern_ids)
    form_data = ProjectFormData.from_domain(project, selected_patterns)
    return _render_project_form(form_data, available_patterns, project_id=project_id)


@projects_api.post('/<int:project_id>/edit')
def edit_project(project_id: int):
    _get_project_or_404(ProjectId(project_id))
    available_patterns = pattern_repo.get_all()
    form_data = ProjectFormData.from_request_form(request.form, available_patterns)
    try:
        edited_project = form_data.to_domain(ProjectId(project_id))
        edited_project.normalize()
        repo.update(edited_project)
        return redirect(f'/projects/{project_id}')
    except Exception as error:
        return _render_project_form(form_data, available_patterns, project_id=project_id, error=str(error))
