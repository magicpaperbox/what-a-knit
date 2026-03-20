from dataclasses import dataclass
from typing import Optional
from infra.db import get_db
from modules.projects.domain import Project, ProjectId, ProjectStatus


@dataclass
class ProjectRow:
    id: int
    name: str
    status: Optional[str]
    actual_gauge: Optional[str]
    progress_percent: Optional[int]
    rating: Optional[int]
    notes: Optional[str]

class ProjectRepository:
    def _row_to_domain(self, row: ProjectRow) -> Project:
        return Project(
            id=ProjectId(row.id),
            name=row.name,
            status=ProjectStatus(row.status),
            actual_gauge=row.actual_gauge,
            progress_percent=row.progress_percent if row.progress_percent is not None else 0,
            rating=row.rating,
            notes=row.notes
        )

    def get_all(self) -> list[Project]:
        db = get_db()
        cursor = db.execute('SELECT * FROM project')
        rows = cursor.fetchall()

        projects = []
        for row in rows:
            project_row = ProjectRow(**dict(row))
            projects.append(self._row_to_domain(project_row))
        return projects

    def get_by_id(self, project_id: ProjectId) -> Optional[Project]:
        db = get_db()
        cursor = db.execute('SELECT * FROM project WHERE id = ?', (project_id.value,))
        row = cursor.fetchone()

        if row is None:
            return None

        project_row = ProjectRow(**dict(row))
        return self._row_to_domain(project_row)

    def add(self, project: Project) -> Project:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO project (
                name, my_tool_size, my_gauge, yarn_bought,
                status, completion, rating, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                project.name, project.my_tool_size, project.my_gauge,
                project.yarn_bought, project.status, project.completion,
                project.rating, project.notes
            )
        )
        db.commit()
        project.id = ProjectId(cursor.lastrowid)
        return project

    def update(self, project: Project) -> None:
        db = get_db()
        db.execute(
            '''UPDATE project SET
                name = ?, my_tool_size = ?, my_gauge = ?, yarn_bought = ?,
                status = ?, completion = ?, rating = ?, notes = ?
            WHERE id = ?''',
            (
                project.name, project.my_tool_size, project.my_gauge,
                project.yarn_bought, project.status, project.completion,
                project.rating, project.notes, project.id.value
            )
        )
        db.commit()

    def delete(self, project_id: ProjectId) -> None:
        db = get_db()
        db.execute('DELETE FROM project WHERE id = ?', (project_id.value,))
        db.commit()
