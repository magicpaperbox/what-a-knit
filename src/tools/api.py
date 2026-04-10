from flask import Blueprint, render_template, redirect
from tools.domain import ToolKind, ToolMaterial
from tools.mappers import parse_tool_from_form, tool_kinds_with_field
from tools.repository import ToolsRepository

tools_api = Blueprint('tools', __name__, url_prefix="/tools")
repo = ToolsRepository()

@tools_api.get('')
def index():
    tools = repo.get_all()
    return render_template('tools/index.html', tools=tools)


@tools_api.get('/add')
def create_tool_form():
    return render_template(
        'tools/add.html',
        tool_kinds=ToolKind,
        materials=ToolMaterial,
        tool_kinds_with_size=tool_kinds_with_field("size"),
        tool_kinds_with_length=tool_kinds_with_field("length"),
    )

@tools_api.post('/add')
def create_tool():
    new_tool = parse_tool_from_form()
    repo.add(new_tool)
    return redirect("/tools")
