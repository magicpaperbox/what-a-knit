# Task: Chart Colors

Started: 2026-06-02
Status: in progress

## Goal

Add color chart editing so the user can pick a new color, paint cells with it, and reuse colors that are already present on the chart.

## Current Context

The backend/domain side already has `Color`, `ColorChart`, and form-data mapping for `kind == "color"`.
The chart editor JavaScript is the current focus.
Color cells can now be drawn on the SVG chart with `drawCellColor`.
The color palette now refreshes after painting a cell in color mode.
`drawCellColor` now ignores cell values that do not start with `#`, so symbol names are not rendered as black SVG fills in color mode.
The shared palette UI was renamed from symbol-specific names to chart palette names, because it now serves both symbols and colors.
Used colors are now rendered as buttons, and clicking one sets `state.selectedColor`.
Used color buttons now show their color as the button background.
Clicking a used color now re-renders the palette, so the visible color picker stays in sync with `state.selectedColor`.
The color palette now uses CSS classes for the color picker, swatch buttons, swatches, labels, and active selected state.
The palette summary updates immediately when the color picker changes `state.selectedColor`.
The color palette now renders as square swatches, and the selected color summary sits below the palette.
The color picker is now a larger square above the smaller saved-color swatches.
The native color picker is styled so the selected color directly fills the large picker square.
On mobile, the chart palette sticks close to the top of the viewport, with the large color picker on the left and saved color swatches in a smaller grid on the right.
The mobile color picker was reduced to 90px square and the sticky palette offset was tightened to 2px.

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
`static/js/charts.js` now has `drawCellColor`, and `renderChart` calls it when `state.kind === "color"`.
The JavaScript file has been reorganized into sections so the editor flow is easier to navigate.
`handleChartClick` now calls `renderColorPalette()` after painting when `state.kind === "color"`.
`drawCellColor` now guards against non-color values before setting the SVG `fill` attribute.
The template, CSS, and JavaScript now use neutral palette names such as `chartPalette`, `chartPaletteTitle`, and `chartPaletteSummary`.
Used color buttons now update `state.selectedColor` on click.
Used color buttons now have inline dynamic background colors from their hex values.
Used color button clicks now call `renderColorPalette()` after updating `state.selectedColor`.
The selected color is shown with an `is-active` class on the matching color button.
The shared palette element gets a mode class (`chart-palette--symbols` or `chart-palette--colors`) so symbols can stay as list buttons while colors render as square swatches.
Saved color buttons are grouped in `chart-color-swatches`, which lets mobile lay them out beside the larger color picker without changing the desktop layout.
The user is learning how this JavaScript/SVG drawing flow works.

## Next Small Step

Polish or extract any repeated palette button styling if it becomes annoying to maintain.

## Open Questions

- Should an empty color cell clear on click, or should there be a separate "clear cell" option in color mode?
