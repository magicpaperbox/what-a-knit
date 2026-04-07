from modules.patterns.domain import PatternId
from modules.patterns.repository import PatternRepository
from modules.projects.repository import ProjectRepository


class DeletePatternUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        pattern_repository: PatternRepository
    ):
        self._project_repository = project_repository
        self._pattern_repository = pattern_repository

    def delete_pattern(self, pattern_id: PatternId) -> None:
        self._project_repository.unlink_pattern(pattern_id)
        self._pattern_repository.delete(pattern_id)