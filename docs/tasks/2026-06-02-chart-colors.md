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
The chart type radio controls are now a styled segmented control inside the main chart toolbar.
The chart palette now lives inside the form directly above the chart; on wide desktop it is placed in a side column, and on narrow/mobile layouts it stays above the chart and becomes sticky only after scrolling past it.
The chart toolbar now uses explicit grid areas: on mobile rows and columns share a row and update/save share a row; on wide desktop title and sizing fields sit on the first row, while chart type and actions sit below.
The chart type segmented control now has label spacing matching the other toolbar fields and no longer uses a gray selected state.

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
The palette panel was moved from being a sibling of the editor section to being part of `chartEditorForm`, which allows different desktop and narrow/mobile placement through CSS grid.
The mobile chart editor section now has extra top padding so the heading spacing matches the rest of the app more closely.
The chart type selector spacing and selected-state colors were polished in light and dark mode.
The user is learning how this JavaScript/SVG drawing flow works.
Color charts saved in the backend can load back into the edit form with correct `cells_json`, but `static/js/charts.js` currently normalizes every loaded cell through symbol-only validation, so hex color values are replaced with `null` before rendering.
The user fixed the load order in `static/js/charts.js` so `state.kind` is set before `readSerializedCells(...)`, and confirmed that saved color charts now reopen with filled color cells.

## Next Small Step

Continue with small cleanup or explanation around `normalizeCells` if needed.

## Open Questions

- Should an empty color cell clear on click, or should there be a separate "clear cell" option in color mode?
