from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from modules.patterns.domain import Gauge, Pattern, PatternId
from modules.projects.domain import Project, ProjectId, ProjectStatus


@dataclass(frozen=True)
class SelectedPatternFormData:
    id: int
    name: str


@dataclass
class ProjectFormData:
    name: str = ""
    progress_percent: str = ""
    gauge_stitches: str = ""
    gauge_rows: str = ""
    start_date: str = ""
    end_date: str = ""
    notes: str = ""
    selected_patterns: list[SelectedPatternFormData] = field(default_factory=list)
    image_blob: bytes | None = None
    image_mime_type: str | None = None

    @classmethod
    def empty(cls) -> ProjectFormData:
        return ProjectFormData()

    @classmethod
    def from_domain(cls, project: Project, selected_patterns: list[Pattern]) -> ProjectFormData:
        return ProjectFormData(
            name=project.name,
            progress_percent="" if project.progress_percent is None else str(project.progress_percent),
            gauge_stitches="" if project.actual_gauge is None or project.actual_gauge.stitches is None else str(project.actual_gauge.stitches),
            gauge_rows="" if project.actual_gauge is None or project.actual_gauge.rows is None else str(project.actual_gauge.rows),
            start_date="" if project.start_date is None else project.start_date.isoformat(),
            end_date="" if project.end_date is None else project.end_date.isoformat(),
            notes=project.notes or "",
            selected_patterns=[
                SelectedPatternFormData(id=pattern.id.value, name=pattern.name)
                for pattern in selected_patterns
                if pattern.id is not None
            ],
            image_blob=project.image_blob,
            image_mime_type=project.image_mime_type
        )

    def to_domain(self, project_id: ProjectId | None = None) -> Project:
        stitches = self.normalize_gauge_value(self.gauge_stitches)
        rows = self.normalize_gauge_value(self.gauge_rows)
        if stitches is not None or rows is not None:
            actual_gauge = Gauge(stitches=stitches, rows=rows)
        else:
            actual_gauge = None

        start_date = None if self.start_date == "" else date.fromisoformat(self.start_date)
        end_date = None if self.end_date == "" else date.fromisoformat(self.end_date)

        pattern_ids = [
            PatternId(selected_pattern.id)
            for selected_pattern in self.selected_patterns
        ]

        progress_percent = int(self.progress_percent) if self.progress_percent else None

        project = Project(
            id=project_id,
            name=self.name,
            status=ProjectStatus.NOT_STARTED,
            progress_percent=progress_percent,
            pattern_ids=pattern_ids,
            actual_gauge=actual_gauge,
            start_date=start_date,
            end_date=end_date,
            rating=None,
            notes=self.notes,
            image_blob=self.image_blob,
            image_mime_type=self.image_mime_type or None
        )

        project.update_status_from_progress()
        return project

    @classmethod
    def from_request_form(
        cls,
        form,
        files,
        available_patterns: list[Pattern],
        existing_project: Project | None = None,
    ) -> ProjectFormData:
        patterns_by_id = {
            pattern.id.value: pattern
            for pattern in available_patterns
            if pattern.id is not None
        }
        selected_patterns = []
        for pattern_id in form.getlist('pattern_id', type=int):
            pattern = patterns_by_id.get(pattern_id)
            if pattern is None:
                continue
            selected_patterns.append(
                SelectedPatternFormData(id=pattern_id, name=pattern.name)
            )

        uploaded_image = files.get('image')
        if uploaded_image is not None and uploaded_image.filename:
            image_blob = uploaded_image.read()
            image_mime_type = uploaded_image.mimetype or None
        elif existing_project is not None:
            image_blob = existing_project.image_blob
            image_mime_type = existing_project.image_mime_type
        else:
            image_blob = None
            image_mime_type = None

        return ProjectFormData(
            name=form.get('name', ''),
            progress_percent=form.get('progress_percent', ''),
            gauge_stitches=form.get('gauge_stitches', ''),
            gauge_rows=form.get('gauge_rows', ''),
            start_date=form.get('start_date', ''),
            end_date=form.get('end_date', ''),
            notes=form.get('notes', ''),
            selected_patterns=selected_patterns,
            image_blob=image_blob,
            image_mime_type=image_mime_type,
        )

    def selected_patterns_to_dicts(self) -> list[dict]:
        return [{"id": pattern.id, "name": pattern.name} for pattern in self.selected_patterns]


    @staticmethod
    def normalize_gauge_value(raw: str) -> float | None:
        if raw == "":
            return None

        value = float(raw)
        if value <= 0:
            return None

        return value
