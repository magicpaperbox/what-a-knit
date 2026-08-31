# Task: Frontend File Split

Started: 2026-08-27
Status: in progress

## Goal

Split large frontend files into smaller CSS and JavaScript files so the chart editor remains readable while adding selection, clipboard, transforms, zoom, and preview behavior.

## Current Context

`static/css/style.css` is now a global CSS entrypoint made of imports.
`static/js/charts.js` is loaded only on the chart editor page and has about 660 lines.
`templates/base.html` now loads `/static/css/style.css` and exposes a `{% block styles %}` in the page head.
`templates/charts/create_chart.html` loads `/static/js/charts.js` in its scripts block and adds a chart-specific CSS link.
`static/css/charts.css` exists and now imports smaller chart CSS files from `static/css/charts/`.
Global CSS has been split into foundation, layout, pages, components, and responsive folders under `static/css/`.
The CSS split and related UI work were visually checked and committed as `e3e1768 more css and ui`.
After that commit, the Charts navigation icon was changed to use `/static/icons/chart.png`; that image and the one-line template reference are pending a separate commit.

## Decisions Made

- Start with CSS because it is safer to split page-specific chart styles first.
- Keep code and file names in English.
- Avoid a large all-at-once frontend refactor before chart selection behavior is built.
- Chart-specific CSS lives in `static/css/charts.css`.
- Chart CSS is split into token, layout, palette, SVG, and responsive files.
- Global CSS stays reusable and app-wide in `static/css/style.css` and its imported folders.
- Chart-only selectors and chart-only variables should not go into the global CSS folders.
- Shared CSS custom properties for repeated radii, focus rings, control sizes, button spacing, and common transitions live in `static/css/foundation/tokens.css`.
- JavaScript splitting is intentionally left for the user to do next.

## Relevant Files

- `templates/base.html`
- `templates/charts/create_chart.html`
- `static/css/style.css`
- `static/css/foundation/fonts.css`
- `static/css/foundation/tokens.css`
- `static/css/foundation/base.css`
- `static/css/layout/shell.css`
- `static/css/layout/navigation.css`
- `static/css/layout/page-title.css`
- `static/css/layout/footer.css`
- `static/css/pages/home.css`
- `static/css/pages/projects.css`
- `static/css/components/section-header.css`
- `static/css/components/resources.css`
- `static/css/components/details.css`
- `static/css/components/forms.css`
- `static/css/components/feedback.css`
- `static/css/components/buttons.css`
- `static/css/components/modals.css`
- `static/css/components/tables.css`
- `static/css/components/icons.css`
- `static/css/responsive/mobile.css`
- `static/css/responsive/640.css`
- `static/css/responsive/768.css`
- `static/css/responsive/900.css`
- `static/css/responsive/1024.css`
- `static/css/charts.css`
- `static/css/charts/tokens.css`
- `static/css/charts/layout.css`
- `static/css/charts/palette.css`
- `static/css/charts/svg.css`
- `static/css/charts/responsive.css`
- `static/js/charts.js`

## Where We Stopped

`templates/base.html` has the needed `{% block styles %}`.
`templates/charts/create_chart.html` links `/static/css/charts.css`.
The chart editor CSS was moved from `static/css/style.css` to `static/css/charts.css`.
`static/css/style.css` no longer contains chart-specific selectors or chart-only CSS variables.
`static/css/charts.css` now acts as the import entrypoint for smaller chart CSS files.
`static/css/style.css` now acts as the import entrypoint for smaller global CSS files.
CSS validation checks passed for whitespace and balanced braces.
The user confirmed the visual check passed and committed the completed CSS/UI work.

## Next Small Step

Commit the pending chart navigation icon change separately if desired. Then move JavaScript in small steps when the user is ready, keeping `static/js/charts.js` behavior unchanged during the split.
Future selection/highlight styles can be added to `static/css/charts/svg.css` or a new focused chart CSS file.

## Open Questions

- Should JavaScript be split with plain ordered script tags first, or should the project switch `charts.js` to browser modules with `type="module"` later?
