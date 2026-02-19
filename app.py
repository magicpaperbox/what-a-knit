from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask("what a knit")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///knit.db'
db = SQLAlchemy(app)

class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) #cannot be empty
    type = db.Column(db.String(50))
    subtype = db.Column(db.String(50))
    tool = db.Column(db.String(20))
    needle_size = db.Column(db.String(20))
    skeins = db.Column(db.String(20))
    skeins_needed = db.Column(db.Integer)
    language = db.Column(db.String(50))
    designer = db.Column(db.String(50))
    yarn_bought = db.Column(db.String(3))
    difficulty = db.Column(db.Integer)
    status = db.Column(db.String(50))
    completion = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    notes = db.Column(db.String(500))


# patterns=[
#     {
#         'name': 'Monday sweater',
#         'type': 'sweater',
#         'subtype': 'raglan',
#         'tool': 'needles',
#         'needle_size': '4mm',
#         'yarn_bought': True,
#         'difficulty': 1,
#         'status': 'in progress',
#         'completion': 60,
#         'rating': 5,
#         'language': 'polish',
#         'designer' : 'Petite knit',
#         'notes': ''
#     },
#     {
#         'name': 'Boucle hat',
#         'type': 'hat',
#         'subtype': 'double folded',
#         'tool': 'needles',
#         'needle_size': '4mm',
#         'yarn_bought': True,
#         'difficulty': 3,
#         'status': 'in progress',
#         'completion': 90,
#         'rating': 3,
#         'language': None,
#         'designer': 'me',
#         'notes': ''
#     },
#     {
#         'name': 'Wesley socks',
#         'type': 'socks',
#         'subtype': 'heel flap',
#         'tool': 'needles',
#         'needle_size': '2.5mm',
#         'yarn_bought': False,
#         'difficulty': None,
#         'status': 'not started',
#         'completion': 0,
#         'rating': None,
#         'language': 'polish',
#         'designer': 'Knitted moments',
#         'notes': ''
#     },
# ]

@app.route('/')
def main_page():
    # Przykładowe dane do przekazania do template
    return render_template(
        'main_page.html',
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

@app.route('/pattern/<int:pattern_id>')
def pattern_detail(pattern_id):
    pattern = db.get_or_404(Pattern, pattern_id)
    return render_template('pattern_detail.html', pattern=pattern)


@app.route('/projects')
def projects():
    patterns=Pattern.query.all() #give me all records from table - list[Objects]
    return render_template('projects.html', patterns=patterns)

@app.route('/add', methods=['GET', 'POST'])
def add_pattern():
    if request.method == 'POST':
        new_pattern = Pattern(
            name=request.form['name'],
            type=request.form['type'],
            subtype=request.form['subtype'],
            tool=request.form['tool'],
            needle_size=request.form['needle_size'],
            skeins=request.form['skeins'],
            skeins_needed=request.form.get('skeins_needed', type=int),
            language=request.form['language'],
            designer=request.form['designer'],
            yarn_bought=request.form['yarn_bought'],
            difficulty=None,
            status='not started',
            completion=0,
            rating=None,
            notes=request.form['notes']
        )
        db.session.add(new_pattern)
        db.session.commit()
        return redirect(f'/pattern/{new_pattern.id}')
    return render_template('add_pattern.html')

if __name__ == '__main__':
    app.run(debug=True)
