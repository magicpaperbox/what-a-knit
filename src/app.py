import os
from flask import Flask
from modules.home.api import home_api
from modules.projects.api import projects_api
from modules.charts.charts import charts_api
from modules.yarn.api import yarn_api
import infra.db

def create_app():
    # Calculate absolute paths to templates, static folder, and database
    # This assumes app.py is in src/ and templates/static/instance are in the project root
    src_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(src_dir)
    template_dir = os.path.join(project_root, 'templates')
    static_dir = os.path.join(project_root, 'static')
    db_path = os.path.join(project_root, 'instance', 'knit.db')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['DATABASE_PATH'] = db_path
    
    # Inicjujemy nasz moduł bazy danych, żeby wiedział, że ma zamykać połączenie po HTTP
    infra.db.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(home_api)
    app.register_blueprint(projects_api)
    app.register_blueprint(charts_api)
    app.register_blueprint(yarn_api)
    
    with app.app_context():
        # Tworzy schemat bazy, jeśli nie istnieje (zastępuje wywołanie SQLAlchemy)
        infra.db.init_db()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
