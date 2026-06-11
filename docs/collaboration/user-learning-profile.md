# User Learning Profile

Last updated: 2026-06-11

## Current Comfort Zone

- Comfortable with Python loops and conditional statements.
- Working in a Flask project with server-rendered templates, SQLite, and plain JavaScript.
- Prefers understanding the reason behind a solution, not only receiving the final code.

## Currently Learning

- Classes and object-oriented programming concepts in Python.
- Layered application structure: API/routes, domain objects, mappers/form-data objects, repositories, services, and use cases.
- Form data flow from HTML through Flask into domain objects and SQLite.
- Plain JavaScript and browser APIs.
- Frontend state flow: how JavaScript state and DOM inputs update each other over time.

## Needs Extra Clarity Around

- Object-oriented design and the role of classes.
- Which application layer owns a specific responsibility.
- The difference between template issues, backend issues, JavaScript issues, database issues, and form-data issues.
- JavaScript standard library and browser DOM APIs; explanations should name exact functions such as `querySelector`, `addEventListener`, or `classList.add`.
- The difference between initial rendering from state to the DOM and later DOM events that write user changes back into state.
- SVG drawing concepts in JavaScript, especially layers, `x`/`y` coordinates, `setAttribute`, and converting numbers to strings with `.toString()`.

## Explanation Style That Works Well

- Polish explanations with code and commit messages in English.
- Small steps focused on one concrete change at a time.
- Clear labels for the layer being discussed: backend, template, JavaScript, database, or form data.
- Direct references to full file paths and function names.
- Beginner-friendly context before deeper design suggestions.
- Python analogies help, especially when explaining JavaScript collections, loops, and data flow.
- Documentation with concrete examples and method-level patterns, not only dry conceptual descriptions.
- Prefers project instructions to be operational, consistently structured, and not duplicated across sections.
- Explaining:
  - how it works now,
  - how it should work,
  - why the current version does not work,
  - what assumption caused the problem.

## Explanation Style To Avoid

- Giving a complete implementation too early when the user asked for guidance.
- Reviewing unrelated missing pieces while the user is intentionally working in tiny steps.
- Vague references such as "here", "there", or "in edit" without a file and function name.
- Asking the user to paste code that is already available in the repository.

## Already Explained Topics

- Flask and Jinja2 basics are documented in `notes/01_flask_jinja2_basics.md`.
- Database and form basics are documented in `notes/02_baza_danych_i_formularze.md`.
- JavaScript helper basics are documented in `notes/03_javascript_helpers.md`.
- Chart SVG/grid notes are documented in `notes/04_generator_siatki_svg.md` and `notes/05_kod_charts_js_wyjasniony.md`.
- Flask from scratch is documented in `notes/06_jak_dziala_flask_od_zera.md`.
- Application layers are documented in `notes/07_warstwy_aplikacji.md`.
- DOM methods and JavaScript utilities are documented in `notes/08_javascript_dom_i_przydatne_metody.md`.
- Optional chaining with `?.`, `Array.isArray`, and the ternary `? :` operator are documented in `notes/08_javascript_dom_i_przydatne_metody.md`.
- Searching where to change formatting/code is documented in `notes/09_jak_szukac_gdzie_zmienic_formatowanie.md` and `notes/10_jak_szukac_rzeczy_w_kodzie.md`.

## Recurring Confusions Or Watch Points

- Keep layer explanations separate. If the problem is in a template, explain it as a template problem first.
- For small oversights such as unused imports, typos, or leftover code, say directly that it was probably a forgotten cleanup.
- Do not assume knowledge of JavaScript library functions or browser APIs.
