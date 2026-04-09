from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import abort

tools_api = Blueprint('tools', __name__, url_prefix="/tools")


@tools_api.get('')
def index():
    return render_template('tools/index.html')
