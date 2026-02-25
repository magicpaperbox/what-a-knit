import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        # Pobieramy ścieżkę do bazy z konfiguracji aplikacji
        db_path = current_app.config.get('DATABASE_PATH')
        
        # Nawiązujemy połączenie z plikiem SQLite
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        # Ustawiamy row_factory na sqlite3.Row, co m.in. pozwala na
        # dostęp do kolumn po nazwach (jak w słownikach: row['name'])
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read())

def init_app(app):
    # Rejestrujemy funkcję zamykającą bazę po zakończeniu każdego żądania HTTP
    app.teardown_appcontext(close_db)
