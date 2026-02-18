from flask import Flask, render_template
from datetime import datetime

app = Flask("what a knit")

patterns=[
    {
        'name': 'Monday sweater',
        'type': 'sweater',
        'subtype': 'raglan',
        'tool': 'needles',
        'needle_size': '4mm',
        'yarn_bought': True,
        'difficulty': 1,
        'status': 'in progress',
        'completion': 60,
        'rating': 5,
        'language': 'polish',
        'designer' : 'Petite knit',
        'notes': ''
    },
    {
        'name': 'Boucle hat',
        'type': 'hat',
        'subtype': 'double folded',
        'tool': 'needles',
        'needle_size': '4mm',
        'yarn_bought': True,
        'difficulty': 3,
        'status': 'in progress',
        'completion': 90,
        'rating': 3,
        'language': None,
        'designer': 'me',
        'notes': ''
    },
    {
        'name': 'Wesley socks',
        'type': 'socks',
        'subtype': 'heel flap',
        'tool': 'needles',
        'needle_size': '2.5mm',
        'yarn_bought': False,
        'difficulty': None,
        'status': 'not started',
        'completion': 0,
        'rating': None,
        'language': 'polish',
        'designer': 'Knitted moments',
        'notes': ''
    },
]

@app.route('/')
def hello_world():
    # Przykładowe dane do przekazania do template
    return render_template(
        'index.html',
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
        message='Witaj w świecie Jinja2!',
        patterns=patterns,
    )

@app.route('/pattern/<int:pattern_id>')
def pattern_detail(pattern_id):
    pattern = patterns[pattern_id]
    return render_template('pattern_detail.html', pattern=pattern)

if __name__ == '__main__':
    app.run(debug=True)
