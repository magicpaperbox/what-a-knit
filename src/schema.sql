CREATE TABLE IF NOT EXISTS project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    subtype VARCHAR(50),
    tool VARCHAR(20),
    needle_size VARCHAR(20),
    skeins VARCHAR(20),
    skeins_needed INTEGER,
    pattern_language VARCHAR(50),
    designer VARCHAR(50),
    yarn_bought VARCHAR(3),
    difficulty INTEGER,
    status VARCHAR(50) DEFAULT 'not started',
    completion INTEGER DEFAULT 0,
    rating INTEGER,
    notes VARCHAR(500)
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
