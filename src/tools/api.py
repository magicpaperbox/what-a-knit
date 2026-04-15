from flask import Blueprint, render_template, redirect, request, abort

from tools.domain import ToolKind, ToolMaterial, ToolId
from tools.mappers import ToolFormData, tool_kinds_with_field
from tools.repository import ToolsRepository

tools_api = Blueprint('tools', __name__, url_prefix="/tools")
repo = ToolsRepository()


def _get_tool_or_404(tool_id: ToolId):
    tool = repo.get_by_id(tool_id)
    if tool is None:
        abort(404, f"Tool id {tool_id.value} does not exist.")
    return tool


def _render_tool_form(
    form_data: ToolFormData,
    tool_id: int | None = None,
    error: str | None = None,
):
    mode = "edit" if tool_id else "add"
    form_action = f"/tools/{tool_id}/edit" if tool_id else "/tools/add"
    return render_template(
        'tools/form.html',
        mode=mode,
        form_action=form_action,
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


@tools_api.get('/<int:tool_id>')
def details(tool_id: int):
    tool = _get_tool_or_404(ToolId(tool_id))
    return render_template('tools/details.html', tool=tool)


@tools_api.get('/<int:tool_id>/edit')
def edit_tool_form(tool_id: int):
    tool = _get_tool_or_404(ToolId(tool_id))
    form_data = ToolFormData.from_domain(tool)
    return _render_tool_form(form_data, tool_id=tool_id)


@tools_api.post('/<int:tool_id>/edit')
def edit_tool(tool_id: int):
    _get_tool_or_404(ToolId(tool_id))
    form_data = ToolFormData.from_request_form(request.form)
    try:
        updated_tool = form_data.to_domain(ToolId(tool_id))
        repo.update(updated_tool)
        return redirect(f"/tools/{tool_id}")
    except Exception as error:
        return _render_tool_form(form_data, tool_id=tool_id, error=str(error))


@tools_api.post('/<int:tool_id>/delete')
def delete_tool(tool_id: int):
    _get_tool_or_404(ToolId(tool_id))
    repo.delete(ToolId(tool_id))
    return redirect("/tools")


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
