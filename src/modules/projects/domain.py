from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional

from datetime import date

from modules.patterns.domain import PatternId, Gauge


@dataclass(frozen=True)
class ProjectId:
    value: int

class ProjectStatus(StrEnum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    FINISHED = "finished"
    FROGGED = "frogged"

@dataclass
class Project:
    id: Optional[ProjectId]
    name: str
    status: ProjectStatus
    progress_percent: int | None

    pattern_ids: list[PatternId] = field(default_factory=list)
    actual_gauge: Optional[Gauge] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    rating: Optional[int] = None
    notes: Optional[str] = None

    def normalize(self):
        if self.progress_percent is None or self.progress_percent == 0:
            self.status = ProjectStatus.NOT_STARTED
        elif self.progress_percent == 100:
            self.status = ProjectStatus.FINISHED
        elif 100 > self.progress_percent > 0:
            self.status = ProjectStatus.IN_PROGRESS

