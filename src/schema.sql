CREATE TABLE IF NOT EXISTS pattern (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    pattern_language VARCHAR(50),
    author VARCHAR(50),
    difficulty_level VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS pattern_gauge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id INTEGER NOT NULL,
    stitches REAL,
    rows REAL,
    width_cm REAL DEFAULT 10.0,
    height_cm REAL DEFAULT 10.0,
    FOREIGN KEY (pattern_id) REFERENCES pattern(id)
);

CREATE TABLE IF NOT EXISTS tool (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(80) NOT NULL,
    size_mm REAL,
    length_cm REAL,
    material VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(50),
    progress_percent INTEGER DEFAULT 0,
    start_date VARCHAR(20),
    end_date VARCHAR(20),
    rating INTEGER,
    notes VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS project_gauge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    stitches REAL,
    rows REAL,
    width_cm REAL DEFAULT 10.0,
    height_cm REAL DEFAULT 10.0,
    FOREIGN KEY (project_id) REFERENCES project(id)
);

CREATE TABLE IF NOT EXISTS project_patterns (
    project_id INTEGER NOT NULL,
    pattern_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, pattern_id),
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (pattern_id) REFERENCES pattern(id)
);

CREATE TABLE IF NOT EXISTS yarn (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    color_shade VARCHAR(100) NOT NULL,
    weight_category VARCHAR(20) NOT NULL,
    full_weight_grams INTEGER NOT NULL,
    full_length_meters REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS yarn_fiber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    yarn_id INTEGER NOT NULL,
    fiber_type VARCHAR(20) NOT NULL,
    percentage INTEGER NOT NULL,
    FOREIGN KEY (yarn_id) REFERENCES yarn(id)
);

CREATE TABLE IF NOT EXISTS skein (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    yarn_id INTEGER NOT NULL,
    current_weight_grams INTEGER NOT NULL,
    FOREIGN KEY (yarn_id) REFERENCES yarn(id)
);
