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
