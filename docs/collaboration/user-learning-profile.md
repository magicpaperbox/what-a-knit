# User Learning Profile

Last updated: 2026-08-26

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
- JavaScript pointer/mouse events for drag interactions on SVG chart cells.

## Needs Extra Clarity Around

- Object-oriented design and the role of classes.
- Which application layer owns a specific responsibility.
- Repository method roles, especially the difference between fetching rows, grouping rows for many parent objects, mapping rows to domain objects, and saving domain objects.
- The difference between template issues, backend issues, JavaScript issues, database issues, and form-data issues.
- JavaScript standard library and browser DOM APIs; explanations should name exact functions such as `querySelector`, `addEventListener`, or `classList.add`.
- The difference between initial rendering from state to the DOM and later DOM events that write user changes back into state.
- The difference between calculating a temporary value inside a JavaScript event handler and saving that value into `state` so rendering can use it.
- SVG drawing concepts in JavaScript, especially layers, `x`/`y` coordinates, `setAttribute`, and converting numbers to strings with `.toString()`.
- Drag-to-paint interaction flow in JavaScript: starting an action, continuing it while moving over cells, and stopping it when the pointer is released.

## Explanation Style That Works Well

- Polish explanations with code and commit messages in English.
- Small steps focused on one concrete change at a time.
- Clear labels for the layer being discussed: backend, template, JavaScript, database, or form data.
- Direct references to full file paths and function names.
- Beginner-friendly context before deeper design suggestions.
- UI suggestions should preserve a slightly retro visual direction rather than pushing the app toward a generic modern SaaS style.
- For UI decisions, explain the practical trade-off clearly, for example decorative centering versus easier scanning in list/inventory views.
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
- JavaScript logical OR `||` and simple guard conditions were explained while checking `drawCellColor`.
- Searching where to change formatting/code is documented in `notes/09_jak_szukac_gdzie_zmienic_formatowanie.md` and `notes/10_jak_szukac_rzeczy_w_kodzie.md`.
- Python `zip(...)` for pairing lists in a `for` loop is documented in `notes/13_python_zip.md`.
- HTML form `name`, `value`, `id`, `label for`, and Flask `form.getlist(...)` flow is documented in `notes/14_html_form_name_value_getlist.md`.
- HTML `disabled` inputs, hidden inputs, and CSS adjacent sibling selectors such as `input:disabled + span` were explained while locking chart type selection in edit mode.

## Recurring Confusions Or Watch Points

- Keep layer explanations separate. If the problem is in a template, explain it as a template problem first.
- For small oversights such as unused imports, typos, or leftover code, say directly that it was probably a forgotten cleanup.
- Do not assume knowledge of JavaScript library functions or browser APIs.
