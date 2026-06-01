# Architecture

This project is a small Flask application organized around simple, explicit layers.
The goal is not to hide complexity behind a framework. The goal is to make the flow of data visible and learnable.

## Source Layout

- `src/app.py` creates the Flask app, configures templates/static paths, initializes SQLite, and registers module blueprints.
- `src/infra/db.py` owns the SQLite connection lifecycle and database initialization.
- `src/schema.sql` defines the database schema.
- `src/modules/<module>/api.py` contains Flask routes for one module.
- `src/modules/<module>/domain.py` contains domain concepts used by that module.
- `src/modules/<module>/mappers.py` translates between external data shapes and domain objects.
- `src/modules/<module>/repository.py` contains SQL queries and persistence logic.
- `src/modules/<module>/service.py` is used when a module needs logic that is larger than one route or repository call.
- `src/use_cases/` contains cross-module application actions.
- `templates/` contains Jinja2 templates.
- `static/js/` contains plain JavaScript for browser behavior.
- `static/css/` contains application styles.
- `tests/` contains tests.

## Layer Responsibilities

### API Layer

Files named `api.py` are the Flask boundary.

They should:

- define routes with Flask blueprints,
- read request data,
- call form-data helpers, repositories, services, or use cases,
- choose redirects or templates,
- pass prepared data to templates.

They should not:

- contain any SQL queries,
- contain complicated business rules,
- make templates responsible for parsing raw form data.

Example: `src/modules/patterns/api.py` uses `PatternFormData.from_request_form(request.form)`, converts it to a domain object, then calls `PatternRepository`.

### Domain Layer

Files named `domain.py` describe project concepts in Python.

They should:

- hold dataclasses, enums, identifiers, and small domain rules,
- use domain language such as `Pattern`, `Gauge`, `PatternId`, `YarnWeightCategory`,
- stay independent from Flask request objects and raw SQLite rows.
- Implement complex business logic.

They should not:

- import Flask request objects,
- execute SQL,
- know about HTML form field names.

### Mapper / Form Data Layer

Files named `mappers.py` translate between shapes of data.

Common responsibilities:

- convert `request.form` strings into explicit form-data objects,
- normalize empty strings into `None` when needed,
- convert form-data objects into domain objects,
- convert domain objects back into form-data objects for edit forms.

Example: `PatternFormData` in `src/modules/patterns/mappers.py` stores form fields as strings, then `to_domain()` converts them into a `Pattern`.

### Repository Layer

Files named `repository.py` own database access.

They should:

- use `infra.db.get_db()`,
- execute SQL,
- map SQLite rows into domain objects,
- commit changes after writes.

They should not:

- read directly from `request.form`,
- render templates,
- decide browser redirects.

Current repositories use raw `sqlite3` intentionally so SQL stays visible.

### Service And Use Case Layer

Use `service.py` inside a module when one module needs reusable application logic.
Use `src/use_cases/` when the action coordinates more than one module.

Example: `src/use_cases/delete_pattern_use_case.py` coordinates pattern deletion rules outside a single route.

## Preferred Request Flow

For a form-based feature, prefer this flow:

```text
HTML form
-> Flask route in api.py
-> FormData.from_request_form(request.form)
-> FormData.to_domain()
-> repository/service/use case
-> SQLite
-> redirect or render_template()
```

This keeps each layer small and makes debugging easier for a beginner.

## Template Responsibilities

Templates should:

- display prepared data,
- render forms,
- use simple conditionals and loops,
- keep naming aligned with form-data classes.

Templates should not:

- contain business rules,
- parse domain values,
- make database-related decisions.

## JavaScript Responsibilities

Plain JavaScript in `static/js/` should handle browser-only interaction:

- DOM updates,
- click/change/input events,
- small UI helpers,
- dynamic form behavior,
- client-side drawing or editing when needed.

JavaScript should not become the only place where important backend rules are enforced.
If a rule matters for saved data, validate or normalize it in Python too.

## When Adding A Feature

Prefer changing the smallest layer that owns the problem:

- Route or request/response issue: `api.py`.
- Form parsing issue: `mappers.py` or the relevant form-data class.
- Domain concept issue: `domain.py`.
- SQL or persistence issue: `repository.py` or `src/schema.sql`.
- UI display issue: `templates/`.
- Browser interaction issue: `static/js/`.

When the same logic starts appearing in multiple routes, consider moving it into a service or use case.
