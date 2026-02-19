from extensions import db

class Project(db.Model):
    __tablename__ = 'project'
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
