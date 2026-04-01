from collections import defaultdict
from dataclasses import dataclass
from typing import Optional
from infra.db import get_db
from modules.patterns.domain import PatternId
from modules.projects.domain import Gauge, Project, ProjectId, ProjectStatus
from datetime import date

from modules.units.centimeters import Centimeters

@dataclass
class ProjectGaugeRow:
    id: int
    project_id: int
    stitches: float | None
    rows: float | None
    width_cm: float
    height_cm: float

@dataclass
class ProjectRow:
    id: int
    name: str
    status: Optional[str]
    progress_percent: Optional[int]

    start_date: Optional[str]
    end_date: Optional[str]
    rating: Optional[int]
    notes: Optional[str]

@dataclass
class ProjectPatternRow:
    project_id: int
    pattern_id: int


class ProjectRepository:
    def _row_to_domain(self, project_row: ProjectRow, gauge_row: ProjectGaugeRow | None, project_pattern_rows: list[ProjectPatternRow]) -> Project:
        if gauge_row:
            gauge = Gauge(
                float(gauge_row.stitches) if gauge_row.stitches is not None else None,
                float(gauge_row.rows) if gauge_row.rows is not None else None,
                width=Centimeters(gauge_row.width_cm) if gauge_row.width_cm is not None else None,
                height=Centimeters(gauge_row.height_cm) if gauge_row.height_cm is not None else None
            )
        else:
            gauge = None

        pattern_ids = []
        for project_pattern_row in project_pattern_rows:
            assert project_pattern_row.project_id == project_row.id
            pattern_id = PatternId(project_pattern_row.pattern_id)
            pattern_ids.append(pattern_id)

        return Project(
            id=ProjectId(project_row.id),
            name=project_row.name,
            status=ProjectStatus(project_row.status),
            progress_percent=project_row.progress_percent if project_row.progress_percent is not None else 0,

            pattern_ids=pattern_ids,
            actual_gauge=gauge,
            start_date=date.fromisoformat(project_row.start_date) if project_row.start_date is not None else None,
            end_date=date.fromisoformat(project_row.end_date) if project_row.end_date is not None else None,
            rating=project_row.rating,
            notes=project_row.notes
        )

    def _get_gauge(self, project_id: int) -> ProjectGaugeRow | None:
        if not project_id:
            return None
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM project_gauge WHERE project_id = ?', (project_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return ProjectGaugeRow(**dict(row))

    def _get_gauge_batch(self, project_ids: set[int]) -> dict[int, ProjectGaugeRow]:
        if not project_ids:
            return {}
        db = get_db()
        placeholders = ','.join('?' for _ in project_ids)
        cursor = db.execute(
            f'SELECT * FROM project_gauge WHERE project_id IN ({placeholders})', tuple(project_ids),
        )
        result = {}
        for raw_row in cursor.fetchall():
            row = ProjectGaugeRow(**dict(raw_row))
            result[row.project_id] = row
        return result

    def _get_project_patterns_batch(self, project_ids: set[int]) -> dict[int, list[ProjectPatternRow]]:
        if not project_ids:
            return {}
        db = get_db()
        placeholders = ','.join('?' for _ in project_ids)
        cursor = db.execute(
            f'SELECT * FROM project_patterns WHERE project_id IN ({placeholders})', tuple(project_ids),
        )
        result = defaultdict(list)
        for raw_row in cursor.fetchall():
            row = ProjectPatternRow(**dict(raw_row))
            result[row.project_id].append(row)
        return result


    def get_all(self) -> list[Project]:
        db = get_db()
        cursor = db.execute('SELECT * FROM project')
        project_rows = [ProjectRow(**dict(row)) for row in cursor.fetchall()]
        project_ids = {row.id for row in project_rows}
        gauge_rows_by_id = self._get_gauge_batch(project_ids)
        project_pattern_rows_by_id = self._get_project_patterns_batch(project_ids)
        projects = []
        for project_row in project_rows:
            gauge_row = gauge_rows_by_id.get(project_row.id)
            project_pattern_row = project_pattern_rows_by_id.get(project_row.id, [])
            projects.append(self._row_to_domain(project_row, gauge_row, project_pattern_row))
        return projects

    def get_by_id(self, project_id: ProjectId) -> Optional[Project]:
        db = get_db()
        cursor = db.execute('SELECT * FROM project WHERE id = ?', (project_id.value,))
        row = cursor.fetchone()

        if row is None:
            return None

        project_row = ProjectRow(**dict(row))
        gauge_row = self._get_gauge(project_row.id)

        cursor = db.execute('SELECT * FROM project_patterns WHERE project_id = ?', (project_id.value,))
        project_pattern_rows = [ProjectPatternRow(**dict(row)) for row in cursor.fetchall()]

        return self._row_to_domain(project_row, gauge_row, project_pattern_rows)

    def _save_gauge(self, gauge: Gauge, project_id: int) -> None:
        db = get_db()
        db.execute(
            '''INSERT INTO project_gauge (project_id, stitches, rows, width_cm, height_cm) VALUES (?, ?, ?, ?, ?)''',
            (project_id, gauge.stitches, gauge.rows, gauge.width.value, gauge.height.value)
        )

    def add(self, project: Project) -> Project:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO project (
                name, status, progress_percent, start_date, end_date, rating, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                project.name, project.status, project.progress_percent,
                project.start_date, project.end_date, project.rating, project.notes
            )
        )
        project.id = ProjectId(cursor.lastrowid)
        self._add_patterns(project)
        if project.actual_gauge:
            self._save_gauge(project.actual_gauge, project.id.value)
        db.commit()
        return project

    def _add_patterns(self, project: Project) -> None:
        db = get_db()
        for pattern_id in project.pattern_ids:
            db.execute(
                '''INSERT INTO project_patterns (
                    project_id, pattern_id
                ) VALUES (?, ?)''',
                (
                    project.id.value, pattern_id.value
                )
            )

    def update(self, project: Project) -> None:
        db = get_db()
        db.execute(
            '''UPDATE project SET
                name = ?, status = ?, progress_percent = ?, 
                start_date = ?, end_date = ?, rating = ?, notes = ?
            WHERE id = ?''',
            (
                project.name, project.status, project.progress_percent,
                project.start_date, project.end_date, project.rating, project.notes, project.id.value
            )
        )
        db.execute('DELETE FROM project_gauge WHERE project_id = ?', (project.id.value,))
        db.execute('DELETE FROM project_patterns WHERE project_id = ?', (project.id.value,))
        self._add_patterns(project)
        if project.actual_gauge:
            self._save_gauge(project.actual_gauge, project.id.value)
        db.commit()

    def delete(self, project_id: ProjectId) -> None:
        db = get_db()
        db.execute('DELETE FROM project_gauge WHERE project_id = ?', (project_id.value,))
        db.execute('DELETE FROM project_patterns WHERE project_id = ?', (project_id.value,))
        db.execute('DELETE FROM project WHERE id = ?', (project_id.value,))
        db.commit()
