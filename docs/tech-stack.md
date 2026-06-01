# Tech Stack And Intentional Constraints

This project intentionally uses a simple stack.
The goal is to learn the foundations before adding heavier abstractions.

## Python

Python is the main backend language.
The project uses Python dataclasses, enums, and small explicit modules to model the application.

Why:

- Python is readable for learning backend concepts.
- Dataclasses make simple data objects easier to see and understand.
- Explicit modules make it easier to discuss where code belongs.

## Flask

Flask is used as a minimal web framework.

The project uses Flask for:

- routes,
- blueprints,
- `request`,
- `redirect`,
- `render_template`,
- app setup.

Why:

- Flask exposes the request/response model clearly.
- It does not force a large project structure.
- It makes it easier to learn what the application code is doing.

## Jinja2 Templates

Jinja2 is used for HTML templates.

Why:

- It keeps server-rendered pages simple.
- It makes backend-to-template data flow visible.
- It helps practice loops, conditionals, and form rendering without adding a frontend framework.

## SQLite With Raw SQL

The project uses SQLite through Python's built-in `sqlite3` module.
It does not use an ORM for now.

Why:

- Raw SQL makes database interaction visible.
- It helps learn tables, columns, joins, constraints, `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
- It avoids hiding important database concepts too early.

Important project file:

- `src/infra/db.py` manages SQLite connections.
- `src/schema.sql` defines the schema.
- repository files contain SQL queries.

## Plain JavaScript

The project uses browser JavaScript without a frontend framework.

Why:

- It helps learn DOM basics before React/Vue/Svelte-level abstractions.
- It keeps browser behavior close to the HTML that uses it.
- It makes functions like `querySelector`, `querySelectorAll`, `addEventListener`, `classList`, and `fetch` easier to learn directly.

## CSS Without A UI Framework

The project uses custom CSS.

Why:

- It helps learn layout, spacing, typography, and component styling directly.
- It keeps the visual design under project control.
- It avoids learning a CSS framework before understanding CSS itself.

## Dependency And Runtime Notes

The project uses `pyproject.toml` and `uv.lock`.
Dependencies are intentionally small.

Current core dependencies:

- `flask`
- `gunicorn`

Development/helper dependencies are listed in the `dev` dependency group.

## Current Philosophy

Prefer:

- explicit code over clever abstractions,
- small functions over hidden magic,
- visible SQL over an ORM,
- plain JavaScript over a frontend framework,
- simple Flask routes over framework-heavy patterns,
- learning-friendly structure over premature optimization.

Do not add large frameworks or architectural patterns unless the user explicitly wants to discuss that tradeoff.
