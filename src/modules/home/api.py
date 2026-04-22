from datetime import datetime

from flask import Blueprint, render_template

from modules.patterns.repository import PatternRepository
from modules.projects.domain import ProjectStatus
from modules.projects.repository import ProjectRepository
from modules.yarn.service import YarnService
from tools.domain import ToolKind
from tools.repository import ToolsRepository

home_api = Blueprint('home', __name__)
project_repo = ProjectRepository()
pattern_repo = PatternRepository()
yarn_service = YarnService()
tools_repo = ToolsRepository()


def _format_meters(value: float) -> str:
    return f"{value:g}"

@home_api.route('/')
def index():
    projects = project_repo.get_all()
    patterns = pattern_repo.get_all()
    yarns = yarn_service.get_all_yarns()
    tools = tools_repo.get_all()

    active_project_count = sum(project.status != ProjectStatus.FINISHED for project in projects)

    total_yarn_grams = 0
    total_yarn_meters = 0.0
    for yarn in yarns:
        skeins = yarn_service.get_skeins_for_yarn(yarn.id)
        for skein in skeins:
            total_yarn_grams += skein.current_weight.grams
            total_yarn_meters += skein.remaining_length(yarn).value

    hook_kinds = {
        ToolKind.SHORT_CROCHET_HOOK,
        ToolKind.STRAIGHT_TUNISIAN_CROCHET_HOOK,
        ToolKind.FIXED_CIRCULAR_TUNISIAN_CROCHET_HOOK,
    }
    needle_kinds = {
        ToolKind.STRAIGHT_NEEDLES,
        ToolKind.FIXED_CIRCULAR_NEEDLES,
        ToolKind.INTERCHANGEABLE_CIRCULAR_NEEDLE_TIPS,
        ToolKind.DOUBLE_POINTED_NEEDLES,
    }
    hook_count = sum(tool.kind in hook_kinds for tool in tools)
    needle_count = sum(tool.kind in needle_kinds for tool in tools)

    return render_template(
        'home/index.html',
        title='What a knit!',
        username='Klaudia',
        current_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        is_logged_in=True,
        project_count=len(projects),
        active_project_count=active_project_count,
        pattern_count=len(patterns),
        yarn_grams=total_yarn_grams,
        yarn_meters=_format_meters(total_yarn_meters),
        tool_count=len(tools),
        hook_count=hook_count,
        needle_count=needle_count,
    )
