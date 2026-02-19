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
    pattern_language = db.Column(db.String(50))
    designer = db.Column(db.String(50))
    yarn_bought = db.Column(db.String(3))
    difficulty = db.Column(db.Integer)
    status = db.Column(db.String(50))
    completion = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    notes = db.Column(db.String(500))


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
    patterns = Pattern.query.all()
    return render_template('projects.html', patterns=patterns)

@app.route('/add', methods=['GET', 'POST'])
def add_pattern():
    if request.method == 'POST':
        new_pattern = Pattern(
            name=request.form['name'],
            type=request.form.get('type'),
            subtype=request.form.get('subtype'),
            tool=request.form.get('tool'),
            needle_size=request.form.get('needle_size'),
            skeins=request.form.get('skeins'),
            skeins_needed=request.form.get('skeins_needed', type=int),
            pattern_language=request.form.get('pattern_language'),
            designer=request.form.get('designer'),
            yarn_bought=request.form.get('yarn_bought'),
            difficulty=None,
            status='not started',
            completion=0,
            rating=None,
            notes=request.form.get('notes')
        )
        db.session.add(new_pattern)
        db.session.commit()
        return redirect(f'/pattern/{new_pattern.id}')
    return render_template('add_pattern.html')

@app.route('/pattern/<int:pattern_id>/delete', methods=['POST'])
def delete_pattern(pattern_id):
    pattern = db.get_or_404(Pattern, pattern_id)
    db.session.delete(pattern)
    db.session.commit()
    return redirect('/projects')

@app.route('/pattern/<int:pattern_id>/edit', methods=['GET', 'POST'])
def edit_pattern(pattern_id):
    pattern = db.get_or_404(Pattern, pattern_id)
    if request.method == 'POST':
        pattern.name = request.form['name']
        pattern.type = request.form.get('type')
        pattern.subtype = request.form.get('subtype')
        pattern.tool = request.form.get('tool')
        pattern.needle_size = request.form.get('needle_size')
        pattern.skeins = request.form.get('skeins')
        pattern.skeins_needed = request.form.get('skeins_needed', type=int)
        pattern.pattern_language = request.form.get('pattern_language')
        pattern.designer = request.form.get('designer')
        pattern.yarn_bought = request.form.get('yarn_bought')
        pattern.difficulty = None
        pattern.status = 'not started'
        pattern.completion = 0
        pattern.rating = None
        pattern.notes = request.form.get('notes')
        db.session.commit()
        return redirect(f'/pattern/{pattern.id}')
    return render_template('edit_pattern.html', pattern=pattern)

@app.route('/pattern/<int:pattern_id>/edit', methods=['GET'])
def search_by_needle_size(needle_size: str, wanted_size: str):
    filter(Pattern.needle_size.contains(wanted_size))

if __name__ == '__main__':
    app.run(debug=True)
