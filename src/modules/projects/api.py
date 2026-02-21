from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import Project

projects_api = Blueprint('projects', __name__, url_prefix="/projects")

@projects_api.route('')
def index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)

@projects_api.route('/<int:project_id>')
def details(project_id: int):
    project = db.get_or_404(Project, project_id)
    return render_template('projects/details.html', project=project)

@projects_api.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_project = Project(
            name=request.form['name'],
            type=request.form.get('type'),
            subtype=request.form.get('subtype'),
            tool=request.form.get('tool'),
            needle_size=request.form.get('needle_size'),
            skeins=request.form.get('skeins'),
            skeins_needed=request.form.get('skeins_needed', type=int),
            pattern_language=request.form.get('pattern_language'),
            designer=request.form.get('designer'),
            yarn_bought=request.form.get('yarn_bought'),
            difficulty=None,
            status='not started',
            completion=0,
            rating=None,
            notes=request.form.get('notes')
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(f"/projects/{new_project.id}")
    return render_template('projects/add.html')

@projects_api.route('/<int:project_id>/delete', methods=['POST'])
def delete(project_id):
    project = db.get_or_404(Project, project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect("/projects")

@projects_api.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id):
    project = db.get_or_404(Project, project_id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.type = request.form.get('type')
        project.subtype = request.form.get('subtype')
        project.tool = request.form.get('tool')
        project.needle_size = request.form.get('needle_size')
        project.skeins = request.form.get('skeins')
        project.skeins_needed = request.form.get('skeins_needed', type=int)
        project.pattern_language = request.form.get('pattern_language')
        project.designer = request.form.get('designer')
        project.yarn_bought = request.form.get('yarn_bought')
        project.difficulty = None
        project.status = 'not started'
        project.completion = 0
        project.rating = None
        project.notes = request.form.get('notes')
        db.session.commit()
        return redirect(f'/project/{project.id}')
    return render_template('projects/edit.html', project=project)
