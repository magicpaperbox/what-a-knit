from dataclasses import dataclass
from typing import Optional
from infra.db import get_db
from modules.projects.domain import Project


@dataclass
class ProjectRow:
    id: int
    name: str
    type: Optional[str]
    subtype: Optional[str]
    tool: Optional[str]
    needle_size: Optional[str]
    skeins: Optional[str]
    skeins_needed: Optional[int]
    pattern_language: Optional[str]
    designer: Optional[str]
    yarn_bought: Optional[str]
    difficulty: Optional[int]
    status: Optional[str]
    completion: Optional[int]
    rating: Optional[int]
    notes: Optional[str]

class ProjectRepository:
    def _row_to_domain(self, row: ProjectRow) -> Project:
        return Project(
            id=row.id,
            name=row.name,
            type=row.type,
            subtype=row.subtype,
            tool=row.tool,
            needle_size=row.needle_size,
            skeins=row.skeins,
            skeins_needed=row.skeins_needed,
            pattern_language=row.pattern_language,
            designer=row.designer,
            yarn_bought=row.yarn_bought,
            difficulty=row.difficulty,
            status=row.status if row.status else 'not started',
            completion=row.completion if row.completion is not None else 0,
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

    def get_by_id(self, project_id: int) -> Optional[Project]:
        db = get_db()
        cursor = db.execute('SELECT * FROM project WHERE id = ?', (project_id,))
        row = cursor.fetchone()

        if row is None:
            return None
        
        project_row = ProjectRow(**dict(row))
        return self._row_to_domain(project_row)

    def add(self, project: Project) -> Project:
        db = get_db()
        cursor = db.execute(
            '''INSERT INTO project (
                name, type, subtype, tool, needle_size, skeins, 
                skeins_needed, pattern_language, designer, yarn_bought, 
                difficulty, status, completion, rating, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                project.name, project.type, project.subtype, project.tool,
                project.needle_size, project.skeins, project.skeins_needed,
                project.pattern_language, project.designer, project.yarn_bought,
                project.difficulty, project.status, project.completion,
                project.rating, project.notes
            )
        )
        db.commit()
        project.id = cursor.lastrowid
        return project

    def update(self, project: Project) -> None:
        db = get_db()
        db.execute(
            '''UPDATE project SET 
                name = ?, type = ?, subtype = ?, tool = ?, needle_size = ?, 
                skeins = ?, skeins_needed = ?, pattern_language = ?, 
                designer = ?, yarn_bought = ?, difficulty = ?, status = ?, 
                completion = ?, rating = ?, notes = ?
            WHERE id = ?''',
            (
                project.name, project.type, project.subtype, project.tool,
                project.needle_size, project.skeins, project.skeins_needed,
                project.pattern_language, project.designer, project.yarn_bought,
                project.difficulty, project.status, project.completion,
                project.rating, project.notes, project.id
            )
        )
        db.commit()

    def delete(self, project_id: int) -> None:
        db = get_db()
        db.execute('DELETE FROM project WHERE id = ?', (project_id,))
        db.commit()
