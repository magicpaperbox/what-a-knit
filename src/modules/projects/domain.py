from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class ProjectId:
    value: int

@dataclass
class Project:
    id: Optional[ProjectId]
    name: str
    my_tool_size: Optional[list[str]] = None
    my_gauge: Optional[str] = None
    yarn_bought: Optional[str] = None
    status: str = 'not started'
    completion: int = 0
    rating: Optional[int] = None
    notes: Optional[str] = None

