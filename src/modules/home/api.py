from flask import Blueprint, render_template
from datetime import datetime

home_api = Blueprint('home', __name__)

@home_api.route('/')
def index():
    return render_template(
        'home/index.html',
        title='What a knit!',
        username='Klaudia',
        current_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        is_logged_in=True,
        yarn_count=3,
        yarn_weight=100,
        yarns=[
            {'color': 'Czerwona', 'weight': 100},
            {'color': 'Niebieska', 'weight': 150},
            {'color': 'Zielona', 'weight': 200}
        ],
    )
