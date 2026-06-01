# Form Data Flow

This document explains how form data should move through the application.
Forms are one of the easiest places to mix layers, so this project keeps the flow explicit.

## Core Idea

HTML form data enters Flask as strings.
Even values that look like numbers, booleans, or enum names arrive as text.

The application should convert those strings deliberately before saving or using them as domain data.

## Preferred Flow

```text
HTML form
-> request.form
-> FormData.from_request_form(...)
-> FormData.to_domain(...)
-> repository/service/use case
-> SQLite
-> redirect or render_template
```

## Step By Step

### 1. HTML Form

Templates define input names.
Those names become keys in `request.form`.

Example responsibility:

- `templates/patterns/form.html` defines fields for pattern data.

The template should render fields and current values.
It should not decide how strings become domain objects.

### 2. Flask Route

The route reads `request.form` and passes it to a form-data class.

Example:

```python
form_data = PatternFormData.from_request_form(request.form)
```

The route should stay small:

- collect request data,
- call conversion logic,
- call repository/service/use case,
- decide whether to redirect or re-render the form.

### 3. Form Data Object

A form-data class stores raw or lightly normalized form values.

Example:

- `PatternFormData` in `src/modules/patterns/mappers.py`.

This class is allowed to know form field names because it is the translation layer between HTML and Python domain objects.

## Reference Example: Form Data Class

Use this shape as the default pattern for modules that need add/edit forms.
The exact fields will change per module, but the method set should stay familiar.

This example mirrors `PatternFormData` from `src/modules/patterns/mappers.py`:

```python
from __future__ import annotations

from dataclasses import dataclass

from modules.patterns.domain import (
    Gauge,
    Pattern,
    PatternCategory,
    PatternDifficultyLevel,
    PatternId,
)


@dataclass
class PatternFormData:
    name: str = ""
    description: str = ""
    category: str = ""
    subcategory: str = ""
    gauge_stitches: str = ""
    gauge_rows: str = ""
    has_pattern: str = ""
    pattern_language: str = ""
    author: str = ""
    difficulty_level: str = ""

    @classmethod
    def empty(cls) -> PatternFormData:
        return cls()

    @classmethod
    def from_domain(cls, pattern: Pattern) -> PatternFormData:
        return cls(
            name=pattern.name,
            description=pattern.description,
            category=pattern.category.name,
            subcategory=pattern.subcategory or "",
            gauge_stitches="" if pattern.target_gauge is None or pattern.target_gauge.stitches is None else str(pattern.target_gauge.stitches),
            gauge_rows="" if pattern.target_gauge is None or pattern.target_gauge.rows is None else str(pattern.target_gauge.rows),
            has_pattern="yes" if (pattern.pattern_language or pattern.author or pattern.difficulty_level) else "no",
            pattern_language=pattern.pattern_language or "",
            author=pattern.author or "",
            difficulty_level="" if pattern.difficulty_level is None else pattern.difficulty_level.value,
        )

    @classmethod
    def from_request_form(cls, form) -> PatternFormData:
        return cls(
            name=form.get("name", ""),
            description=form.get("description", ""),
            category=form.get("category", ""),
            subcategory=form.get("subcategory", ""),
            gauge_stitches=form.get("gauge_stitches", ""),
            gauge_rows=form.get("gauge_rows", ""),
            has_pattern=form.get("has_pattern", ""),
            pattern_language=form.get("pattern_language", ""),
            author=form.get("author", ""),
            difficulty_level=form.get("difficulty_level", ""),
        )

    def to_domain(self, pattern_id: PatternId | None = None) -> Pattern:
        stitches = self.normalize_gauge_value(self.gauge_stitches)
        rows = self.normalize_gauge_value(self.gauge_rows)

        if stitches is not None or rows is not None:
            target_gauge = Gauge(stitches=stitches, rows=rows)
        else:
            target_gauge = None

        if self.has_pattern == "no":
            pattern_language = None
            author = None
            difficulty_level = None
        else:
            pattern_language = self.pattern_language or None
            author = self.author or None
            difficulty_level = PatternDifficultyLevel(self.difficulty_level) if self.difficulty_level else None

        return Pattern(
            id=pattern_id,
            name=self.name,
            description=self.description,
            target_gauge=target_gauge,
            category=PatternCategory[self.category],
            subcategory=self.subcategory or None,
            pattern_language=pattern_language,
            author=author,
            difficulty_level=difficulty_level,
        )

    @staticmethod
    def normalize_gauge_value(raw: str) -> float | None:
        if raw == "":
            return None

        value = float(raw)
        if value <= 0:
            return None

        return value
```

## Where Each Method Is Used

Use the methods consistently:

- `empty()` is for rendering a blank add form.
- `from_domain(...)` is for rendering an edit form from an existing domain object.
- `from_request_form(request.form)` is for POST routes after the user submits a form.
- `to_domain(...)` is for converting form strings into a domain object before calling a repository, service, or use case.
- Helper methods such as `normalize_gauge_value(...)` keep small conversion rules named and testable.

Typical route usage:

```python
@patterns_api.get("/add")
def create_pattern_form():
    return _render_pattern_form(PatternFormData.empty())


@patterns_api.post("/add")
def create_pattern():
    form_data = PatternFormData.from_request_form(request.form)
    new_pattern = form_data.to_domain()
    new_pattern = repo.add(new_pattern)
    return redirect(f"/patterns/{new_pattern.id.value}")


@patterns_api.get("/<int:pattern_id>/edit")
def edit_pattern_form(pattern_id: int):
    pattern = get_pattern_or_404(PatternId(pattern_id))
    form_data = PatternFormData.from_domain(pattern)
    return _render_pattern_form(form_data, pattern_id=pattern_id)


@patterns_api.post("/<int:pattern_id>/edit")
def edit_pattern(pattern_id: int):
    form_data = PatternFormData.from_request_form(request.form)
    edited_pattern = form_data.to_domain(PatternId(pattern_id))
    repo.update(edited_pattern)
    return redirect(f"/patterns/{pattern_id}")
```

The route decides what happens next.
The form-data class decides how raw form strings become domain-shaped data.
The repository decides how domain-shaped data is saved.

### 4. Conversion To Domain

The form-data object converts strings into domain values.

Common conversions:

- empty string `""` -> `None`,
- numeric string -> `float` or `int`,
- enum string -> enum value,
- checkbox/select value -> explicit boolean or option,
- related object id string -> id value object.

Example:

```python
edited_pattern = form_data.to_domain(PatternId(pattern_id))
```

If a helper function is needed, name it clearly.
For example, `PatternFormData.normalize_gauge_value()` converts a raw gauge string into `float | None`.

### 5. Repository Or Use Case

The repository receives domain objects or explicit values.
It should not parse raw `request.form`.

Repositories should focus on:

- SQL,
- row-to-domain conversion,
- saving and loading data.

Use cases or services should handle higher-level application behavior, especially when more than one repository is involved.

### 6. Database

SQLite stores the final values.
At this point, data should already be converted into the shape expected by the schema.

## Edit Forms

For edit screens, data usually flows in the opposite direction first:

```text
SQLite
-> repository
-> domain object
-> FormData.from_domain(...)
-> template
```

This lets the same template render both add and edit forms.

## Layer Boundaries

Keep these rules in mind:

- Templates own field names and display.
- Routes own request/response flow.
- Form-data classes own parsing and conversion from form strings.
- Domain objects own application concepts.
- Repositories own SQL.

## Beginner-Friendly Debugging Questions

When something breaks in a form, ask:

1. Does the HTML input have the expected `name`?
2. Does `request.form.get("field_name")` use the same name?
3. Is the value still a string?
4. Where is the string converted into `int`, `float`, enum, boolean, or `None`?
5. Does the repository receive domain-shaped data, not raw form-shaped data?
6. Does the database schema accept that value?
