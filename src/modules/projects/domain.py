from dataclasses import dataclass
from typing import Optional



@dataclass
class Project:
    """
    Reprezentacja domenowa – czyli obiekt, którym nasza aplikacja będzie żonglować w kodzie.
    Zwróć uwagę, że 'id' jest opcjonalne, bo nowy projekt, który dopiero tworzymy,
    nie ma jeszcze swojego numerka z bazy. Mamy też podane wartości domyślne dla nowych projektów.
    """
    name: str
    id: Optional[int] = None
    type: Optional[str] = None
    subtype: Optional[str] = None
    tool: Optional[str] = None
    needle_size: Optional[str] = None
    skeins: Optional[str] = None
    skeins_needed: Optional[int] = None
    pattern_language: Optional[str] = None
    designer: Optional[str] = None
    yarn_bought: Optional[str] = None
    difficulty: Optional[int] = None
    status: str = 'not started'
    completion: int = 0
    rating: Optional[int] = None
    notes: Optional[str] = None
