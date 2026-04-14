from flask import Blueprint, render_template, redirect, request

from tools.domain import ToolKind, ToolMaterial
from tools.mappers import ToolFormData, tool_kinds_with_field
from tools.repository import ToolsRepository

tools_api = Blueprint('tools', __name__, url_prefix="/tools")
repo = ToolsRepository()


def _render_tool_form(
    form_data: ToolFormData,
    error: str | None = None,
):
    return render_template(
        'tools/form.html',
        mode="add",
        form_action="/tools/add",
        form_data=form_data,
        error=error,
        tool_kinds=ToolKind,
        materials=ToolMaterial,
        tool_kinds_with_size=tool_kinds_with_field("size"),
        tool_kinds_with_length=tool_kinds_with_field("length"),
    )


@tools_api.get('')
def index():
    tools = repo.get_all()
    return render_template('tools/index.html', tools=tools)


@tools_api.get('/add')
def create_tool_form():
    return _render_tool_form(ToolFormData.empty())


@tools_api.post('/add')
def create_tool():
    form_data = ToolFormData.from_request_form(request.form)
    try:
        new_tool = form_data.to_domain()
        repo.add(new_tool)
        return redirect("/tools")
    except Exception as error:
        return _render_tool_form(form_data, error=str(error))
