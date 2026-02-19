import os
from flask import Flask
from extensions import db
from modules.home.api import home_api
from modules.projects.api import projects_api

def create_app():
    # Calculate absolute paths to templates, static folder, and database
    # This assumes app.py is in src/ and templates/static/instance are in the project root
    src_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(src_dir)
    template_dir = os.path.join(project_root, 'templates')
    static_dir = os.path.join(project_root, 'static')
    db_path = os.path.join(project_root, 'instance', 'knit.db')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(home_api)
    app.register_blueprint(projects_api)
    
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        import models
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
