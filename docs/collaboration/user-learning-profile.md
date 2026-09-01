# User Learning Profile

Last updated: 2026-09-01

## Current Comfort Zone

- Comfortable with Python loops and conditional statements.
- Working in a Flask project with server-rendered templates, SQLite, and plain JavaScript.
- Prefers understanding the reason behind a solution, not only receiving the final code.

## Currently Learning

- Classes and object-oriented programming concepts in Python.
- Layered application structure: API/routes, domain objects, mappers/form-data objects, repositories, services, and use cases.
- Form data flow from HTML through Flask into domain objects and SQLite.
- Plain JavaScript and browser APIs.
- CSS file organization and CSS custom properties used as design tokens.
- Frontend state flow: how JavaScript state and DOM inputs update each other over time.
- JavaScript pointer/mouse events for drag interactions on SVG chart cells.

## Needs Extra Clarity Around

- Object-oriented design and the role of classes.
- Which application layer owns a specific responsibility.
- Repository method roles, especially the difference between fetching rows, grouping rows for many parent objects, mapping rows to domain objects, and saving domain objects.
- The difference between template issues, backend issues, JavaScript issues, database issues, and form-data issues.
- JavaScript standard library and browser DOM APIs; explanations should name exact functions such as `querySelector`, `addEventListener`, or `classList.add`.
- The difference between a single DOM element and a list of DOM elements returned by `querySelectorAll`, especially when using `.forEach(...)` and `.classList`.
- CSS custom properties, especially when they act like reusable constants for repeated colors, spacing, radii, borders, shadows, and transitions.
- The difference between initial rendering from state to the DOM and later DOM events that write user changes back into state.
- The difference between calculating a temporary value inside a JavaScript event handler and saving that value into `state` so rendering can use it.
- SVG drawing concepts in JavaScript, especially layers, `x`/`y` coordinates, `setAttribute`, and converting numbers to strings with `.toString()`.
- The difference between plain JavaScript data objects and DOM/SVG nodes: `appendChild(...)` can append an element such as an SVG `text` or `rect`, but not a data object such as selection `bounds`.
- Drag-to-paint interaction flow in JavaScript: starting an action, continuing it while moving over cells, and stopping it when the pointer is released.
- Separating similar pointer interactions in JavaScript, such as hover, painting, and temporary area selection, so one state flag does not accidentally mean several different things.
- Helper function inputs and outputs: parameters themselves introduce local variables whose values come from call arguments; they do not need separate `const` declarations. Show the actual function header and the matching call together before using proposed parameter names in calculations. Distinguish whole point objects from coordinates and input data from returned results.

## Explanation Style That Works Well

- Polish explanations with code and commit messages in English.
- Small, coherent functional stages that group related changes, such as one complete pointer interaction. Avoid splitting each assignment or word into a separate review cycle.
- After a successful implementation review, provide the next coherent step without waiting for another "what next?" message, unless the user is asking only a focused conceptual question or wants to pause.
- Clear labels for the layer being discussed: backend, template, JavaScript, database, or form data.
- Direct references to full file paths and function names.
- When several loops look alike, provide a unique searchable line and explain what that block draws; file links and line numbers alone may not be enough to locate it.
- Clearly separate explanations of existing behavior from edit instructions. State the exact target function before discussing related functions, so background context does not sound like an instruction to move code.
- When the user points to a specific line or asks about named variables, answer that exact question first and stop. Do not append a broader review of the surrounding function until the focused point is resolved.
- When the user says she is lost, pause edit instructions and explain one data-flow connection using a concrete call and its parameters. Mark illustrative code as explanation rather than something to insert; do not combine input shapes, calculations, naming, and return syntax in one corrective checklist.
- Beginner-friendly context before deeper design suggestions.
- UI suggestions should preserve a slightly retro visual direction rather than pushing the app toward a generic modern SaaS style.
- For retro UI polish, prefers flat fills and clear borders over soft blurry shadows, especially for navigation hover and active states.
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
- Changing a state flag does not stop function execution; `return` exits the function. When explaining a guard, distinguish the condition checked by `if` from assignments and `return` executed inside its body. Discussed in `handleChartPointerDown` when separating tool selection from painting.
- Rectangle selection uses two endpoint cells to describe an entire area. Both endpoints initially identify the clicked cell; during dragging the start stays fixed and the end changes. Equal initial endpoints do not limit selection to one cell.
- `Math.min` and `Math.max` can turn selection endpoints into direction-independent row and column bounds, including a drag toward smaller indices.
- JavaScript `return (a, b)` uses the comma operator and returns only the last value, unlike a Python tuple return. Return an object with named fields when several related results are needed.
- Used `console.log(bounds)` in `renderChart` and expanded nested objects in the browser console to inspect the helper's returned selection bounds.
- Searching where to change formatting/code is documented in `notes/09_jak_szukac_gdzie_zmienic_formatowanie.md` and `notes/10_jak_szukac_rzeczy_w_kodzie.md`.
- Python `zip(...)` for pairing lists in a `for` loop is documented in `notes/13_python_zip.md`.
- HTML form `name`, `value`, `id`, `label for`, and Flask `form.getlist(...)` flow is documented in `notes/14_html_form_name_value_getlist.md`.
- HTML `disabled` inputs, hidden inputs, and CSS adjacent sibling selectors such as `input:disabled + span` were explained while locking chart type selection in edit mode.
- JavaScript `const` reassignment, assigning a boolean expression directly to a constant, `&&` short-circuiting, and the difference between `node --check` syntax validation and runtime errors are documented in `notes/08_javascript_dom_i_przydatne_metody.md`.
- Converting a bottom-up displayed row index to the chart grid's top-down array index with `state.rows - 1 - row` was explained using a 12-row chart mapping.

## Recurring Confusions Or Watch Points

- Keep layer explanations separate. If the problem is in a template, explain it as a template problem first.
- For small oversights such as unused imports, typos, or leftover code, say directly that it was probably a forgotten cleanup.
- Do not assume knowledge of JavaScript library functions or browser APIs.
