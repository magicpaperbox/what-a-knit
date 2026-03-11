from flask import render_template, Blueprint

charts_api = Blueprint('charts', __name__)

@charts_api.get("/charts")
def chart():
    return render_template("charts/create_chart.html")