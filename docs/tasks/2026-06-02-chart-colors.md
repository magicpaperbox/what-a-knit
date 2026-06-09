# Task: Chart Colors

Started: 2026-06-02
Status: in progress

## Goal

Add color chart editing so the user can pick a new color, paint cells with it, and reuse colors that are already present on the chart.

## Current Context

The backend/domain side already has `Color`, `ColorChart`, and form-data mapping for `kind == "color"`.
The chart editor JavaScript is the current focus.

## Decisions Made

- A newly picked color from the browser color picker should become the selected color only.
- A newly picked color should not appear in the reusable color list until it is actually painted onto a chart cell.
- The reusable color list should be derived from colors currently used in `state.cells`.
- Clicking an already-used color in the color list should select it for painting.
- Color mode should use hex strings such as `#ffffff`, matching the backend `Color` class.

## Relevant Files

- `static/js/charts.js`
- `templates/charts/create_chart.html`
- `src/modules/charts/domain.py`
- `src/modules/charts/mappers.py`
- `tests/charts/test_color.py`
- `tests/charts/test_color_chart.py`

## Where We Stopped

The user clarified the desired color palette behavior.
`static/js/charts.js` has an unfinished `renderColorPalette` area and still needs color-mode JavaScript logic.

## Next Small Step

Explain and/or implement the JavaScript state flow for:
selected color, used colors derived from cells, painting cells, and refreshing the color palette after painting.

## Open Questions

- Should an empty color cell clear on click, or should there be a separate "clear cell" option in color mode?
