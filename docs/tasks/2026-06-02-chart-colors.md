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
On 2026-08-24, the user returned to chart saving. Current code already redirects newly saved charts to `/charts/<id>/edit` in `src/modules/charts/api.py:create_chart`, so the next useful check is whether the submitted form sends the correct `kind` and `cells_json`.
The production 500 is now suspected to come from an old SQLite `chart` table schema. The old table may be missing `kind` and may still have required `rows`/`columns` columns, while the current code expects `id`, `kind`, `name`, `cell_size`, and `cells_json` only.
The user clarified that existing chart data is not important, but other tables such as yarn, projects, and patterns must be preserved. This means the fix can reset only the `chart` table instead of migrating old chart rows.
Important decision: do not commit an unconditional `DROP TABLE chart` inside app startup code. Either run the drop once manually on the production database, or commit a conditional ensure function that drops/recreates `chart` only when the existing columns do not match the expected schema.
`ALTER TABLE` was considered, but the old chart table likely also has required `rows`/`columns` columns that the current repository no longer writes. Adding only `kind` would not fix inserts, so a conditional drop/recreate of only `chart` remains the simpler fix while chart data is disposable.
The current local attempt adds `_reset_chart_table(db)` before `schema.sql` and drops `chart` when `kind` is missing. This is close, but the condition should also catch old schema leftovers such as `rows`/`columns`, in case `kind` was already added manually to an otherwise old table.
The next editor feature is a color erase tool. In symbol mode, selecting `knit` already writes `null` to a cell. In color mode, `handleChartClick` currently always writes `state.selectedColor`, so the JavaScript needs a separate color tool state such as `paint` vs `erase`; the backend already accepts `null` color cells.
`static/js/charts.js` now renders color tools separately from saved color swatches, using `state.colorTool` for `paint`/`erase`. Choosing the color picker or a saved color switches back to paint mode. `static/css/style.css` now has compact icon-only buttons for paint and erase.
The next feature is drag painting/erasing over multiple SVG cells. `state.isPainting` already exists and can track whether pointer drag painting is active.
The single-cell mutation and rendering logic has now been extracted into `applyCurrentToolToCell(row, column)`.
`getCellPositionFromEvent(event)` now correctly returns `{row, column}` or no value when the event is outside a chart cell. `handleChartClick(event)` uses this helper and passes the returned position into `applyCurrentToolToCell`, so ordinary single-cell clicking works again.
`handleChartPointerDown(event)` now gets the cell position, guards against events outside cells, sets `state.isPainting = true`, and paints the first cell. It is registered on the chart's `pointerdown` event.
`handleChartPointerUp()` now sets `state.isPainting = false` and is registered on `document`, so releasing the pointer outside the chart also stops painting.
`handleChartPointerMove(event)` now correctly returns when `state.isPainting` is false, obtains the cell under the moving pointer, guards against a missing position, and applies the current tool.
`handleChartPointerMove(event)` is registered on the chart's `pointermove` event.

Desktop testing revealed that `pointerup` is observed outside the chart but appears not to run while interacting inside it. The likely cause is the interaction between `pointerover` and full SVG re-rendering: `applyCurrentToolToCell()` calls `renderChart()`, which clears `svg.innerHTML` and recreates the hit cell under the pointer, potentially triggering another `pointerover` repeatedly and preventing the interaction from settling normally.
Changing the listener from `pointerover` to `pointermove` fixed the interaction in manual testing. The handler is now named `handleChartPointerMove`, and the temporary pointer-up console log has been removed.

Decision: `handleChartPointerDown` will replace `handleChartClick`; both should not remain registered because an ordinary click also produces `pointerdown`, which would apply the tool twice.
The next requested behavior is locking the chart type after a chart is created: if a saved symbol chart is opened in edit mode, the user should not be able to accidentally switch it to color mode and overwrite symbol cells as colors, and the same should apply in the opposite direction.
Current code still renders active `kind` radio controls in `templates/charts/create_chart.html`, changes `state.kind` from those controls in `static/js/charts.js:init()`, and persists submitted `kind` in `src/modules/charts/repository.py:update()`.
`templates/charts/create_chart.html` now disables both chart type radio inputs in edit mode and adds a hidden `kind` input in edit mode, so the current kind is still submitted even though the visible radios are not clickable.
`static/css/style.css` now gives disabled chart type options a gray, locked appearance, with a separate disabled-and-checked style so the current type is still visible but no longer looks editable.
On wide desktop layouts, `static/css/style.css` now lets the chart toolbar actions use three columns and resets the delete button from full-row spanning to a normal grid item, so Update grid, Save changes, and Delete chart can sit on one line.
The toolbar layout was adjusted again: `Update grid` now lives inside `chart-inputs-group` next to Rows, Columns, and Box size. The metrics group is 2x2 by default and 4 columns on wide desktop. `chart-actions` now contains only Save and Delete; Delete no longer spans a full row, and a single Save button spans the action area in create mode.
`Chart type` was moved out of the toolbar and into `chart-palette-panel`, above the dynamic Symbols/Colors palette. The toolbar no longer has a `kind` grid area; on wide desktop its actions row now spans both toolbar columns.
The `Chart type` legend and the dynamic `Symbols`/`Colors` palette heading now share the same font size, weight, color, and line height in `static/css/style.css`.
Spacing in `chart-palette-panel` was tuned so `Chart type` has breathing room above the segmented control and the type selector is separated more clearly from the palette below, including on narrow layouts.
The `Chart type` spacing now uses an explicit `legend` bottom margin instead of relying on fieldset grid gap, so the heading no longer sits too close to the segmented control.
The wide desktop `chart-palette-panel` no longer sets `max-height` and `overflow-y: auto`, because moving `Chart type` into the panel made the internal scrollbar appear.
The header-level `New empty chart` link was moved into the chart toolbar action area. In edit mode it still says `New empty chart`; in create mode the same `/charts` link is shown as `Reset chart`. Chart actions now get a mode class: create mode uses two action columns, while edit mode uses three action columns so Save, Delete, and New empty chart can sit in one row on non-mobile layouts. On mobile, actions stack in one column.
The action mode CSS now uses more specific selectors such as `.chart-actions.chart-actions--edit`, because a later generic `.chart-actions` media query was overriding the three-column edit layout.

## Next Small Step

Add the backend safeguard in `src/modules/charts/api.py:edit_chart()` by preserving the existing chart kind during edit saves instead of trusting the submitted form value.

## Open Questions

- Should an empty color cell clear on click, or should there be a separate "clear cell" option in color mode?
