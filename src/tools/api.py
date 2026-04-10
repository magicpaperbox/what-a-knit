from flask import Blueprint, render_template, redirect
from tools.domain import ToolCategory, ToolMaterial
from tools.mappers import parse_tool_from_form
from tools.repository import ToolsRepository

tools_api = Blueprint('tools', __name__, url_prefix="/tools")
repo = ToolsRepository()

@tools_api.get('')
def index():
    tools = repo.get_all()
    return render_template('tools/index.html', tools=tools)


@tools_api.get('/add')
def create_tool_form():
    return render_template('tools/add.html', tool_categories=ToolCategory, materials=ToolMaterial)

@tools_api.post('/add')
def create_tool():
    new_tool = parse_tool_from_form()
    repo.add(new_tool)
    return redirect("/tools")