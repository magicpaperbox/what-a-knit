from flask import request
from datetime import date

from modules.patterns.domain import Gauge, PatternId
from modules.projects.domain import Project, ProjectStatus


def parse_project_from_form() -> Project:
    stitches = request.form.get('gauge_stitches', type=float)
    rows = request.form.get('gauge_rows', type=float)
    if stitches is not None or rows is not None:
        actual_gauge=Gauge(stitches=stitches, rows=rows)
    else:
        actual_gauge = None

    start_date=request.form['start_date']
    if start_date == "":
        start_date = None
    else:
        start_date = date.fromisoformat(request.form['start_date'])
    end_date=request.form['end_date']
    if end_date == "":
        end_date = None
    else:
        end_date = date.fromisoformat(request.form['end_date'])

    pattern_ids = []
    pattern_ids_form = request.form.getlist('pattern_id', type=int)
    for pattern_id in pattern_ids_form:
        pattern_id = PatternId(pattern_id)
        pattern_ids.append(pattern_id)



    return Project(
        id=None,
        name=request.form['name'],
        status=ProjectStatus[request.form['status']],
        progress_percent=request.form.get('progress_percent', type=int),
        pattern_ids=pattern_ids,
        actual_gauge=actual_gauge,
        start_date=start_date,
        end_date=end_date,
        rating=request.form.get('rating', type=int),
        notes=request.form['notes'],

    )
